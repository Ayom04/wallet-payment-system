from user.models import User
from django.conf import settings
from rest_framework import authentication, status
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
# from rest_framework_simplejwt.exceptions import
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken, TokenError


class JWTAuthentication(authentication.BasicAuthentication):

    @classmethod
    def create_token(cls, user):

        if not user.is_active:
            raise AuthenticationFailed(
                {"error": "Account is not active"}, code=status.HTTP_401_UNAUTHORIZED)

        # if not user.is_user_verified:
        #     raise AuthenticationFailed(
        #         {"error": "Account is not verified"}, code=status.HTTP_401_UNAUTHORIZED)
        token = RefreshToken.for_user(user)
        token['email'] = user.email
        token['_id'] = str(uuid.uuid4())

        return token

    @classmethod
    def get_token_from_headers(cls, token):
        try:
            token_type, token = token.split(' ')
            if token_type != 'Bearer':
                raise AuthenticationFailed(
                    {"error": "Unauthorized Access..."}, code=status.HTTP_401_UNAUTHORIZED)
            return token
        except ValueError:
            raise AuthenticationFailed(
                {"error": "Unauthorized Access..."}, code=status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def get_user_from_token(cls, token):
        payload = token.payload
        email = payload.get('email')

        try:
            user = User.objects.filter(email=email).first()
            return user
        except User.DoesNotExist:
            return None

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)

        if auth_header is None:
            raise AuthenticationFailed(
                {"error": "Authorization header is missing"}, code=status.HTTP_401_UNAUTHORIZED)

        token = JWTAuthentication.get_token_from_headers(auth_header)
        if isinstance(token, Response):
            return token

        try:
            jwt_token = UntypedToken(token)
        except TokenError as e:
            print("Token validation error:", str(e))
            raise AuthenticationFailed({"error": str(e)},
                                       code=status.HTTP_401_UNAUTHORIZED)

        user = JWTAuthentication.get_user_from_token(jwt_token)

        if user is None:
            raise AuthenticationFailed(
                {"error": "Unauthorized Access..."}, code=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            raise AuthenticationFailed(
                {"error": "Sorry, You're not allowed to carry out this operation."}, code=status.HTTP_401_UNAUTHORIZED)

        # if not user.is_user_verified:
        #     raise AuthenticationFailed(
        #         {"error": "User is not verified"}, code=status.HTTP_401_UNAUTHORIZED)

        return user, token
