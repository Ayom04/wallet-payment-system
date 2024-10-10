from rest_framework import serializers
from user.models import User
from rest_framework import status
# from wallet.serializer import WalletSerializer


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})

    class Meta:
        model = User
        exclude = ["user_id", "created_at", "updated_at", "is_active", "is_admin", "is_staff",
                   "is_superuser", "is_bvn_verified", "is_nin_verified", "is_user_verified"]
        read_only_fields = ['user_id', "created_at", "updated_at", "password", "is_active", "is_admin",
                            "is_staff", "is_superuser", "is_bvn_verified", "is_nin_verified", "is_user_verified"]
        extra_kwargs = {
            'password': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data['password']
        confirm_password = validated_data.pop('confirm_password')
        email = self.validated_data['email']

        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}, code=status.HTTP_400_BAD_REQUEST)

        check_user_exists = User.objects.filter(email=email).exists()
        if check_user_exists:
            raise serializers.ValidationError(
                {"email": "User with this email already exists"}, code=status.HTTP_400_BAD_REQUEST)
        print(validated_data)
        user = User.objects.create_user(
            **validated_data
        )

        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):

        read_only_fields = [
            "is_active", "is_admin", "is_staff", "is_superuser",
            "is_bvn_verified", "is_nin_verified", "is_user_verified",
            "password", "confirm_password"
        ]

        for field in read_only_fields:
            validated_data.pop(field, None)

        print(validated_data)
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if not user:
                raise ValueError(
                    {"meassage": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

            if not user.check_password(password):
                raise serializers.ValidationError(
                    {"message": "Invalid email or password"}, code=status.HTTP_400_BAD_REQUEST)
            if not user.is_active:
                raise serializers.ValidationError(
                    {"message": "User is not active"}, code=status.HTTP_400_BAD_REQUEST)
            return user
        raise serializers.ValidationError(
            {"message": "Email and password are required"}, code=status.HTTP_400_BAD_REQUEST)

        """
        pass the email and password to the authenticate method
        check if the user exists
        if the user exists, check if the password is correct
        if the password is correct, return the user
        if the password is incorrect, raise a validation error
        check the user's is_active status
        if the user is active, return the user
        if the user is not active, raise a validation error
        
        """
