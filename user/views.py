from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework.decorators import api_view
from user.serializer import UserSerializer, LoginSerializer
from user.authentication import JWTAuthentication
from wallet.models import Wallet
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        try:

            wallet = Wallet.objects.get(user_id=user)

            wallet_balance = round(float(wallet.amount_after), 2)
        except Wallet.DoesNotExist:
            wallet_balance = 0.00

        return Response({"message": "user created successfully", "data": {"user": serializer.data, wallet_balance: wallet_balance}}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        token = JWTAuthentication.create_token(user)

        print(token.access_token)

        return Response({
            "message": "Login Successful",
        },
            status=status.HTTP_200_OK,
            headers={"Authorization": token.access_token})

    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "User deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
