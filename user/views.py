from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework.decorators import api_view
from user.serializer import UserSerializer, LoginSerializer
from user.authentication import JWTAuthentication
from wallet.models import Wallet
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.helper import generate_otp
from user.models import Otp, User
from services.email import send_email
from django.utils import timezone
from datetime import timedelta


@swagger_auto_schema(
    method='post',
    operation_description="Create a new user",
    request_body=UserSerializer,
    responses={201: "User Created", 400: "Bad Request"})
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

        otp_code = generate_otp()
        Otp.objects.create(user_id=user, otp_code=otp_code)
        context = {
            "name": f"{user.first_name} {user.last_name}",
            "otp": otp_code
        }
        # send_email("Your One-Time Password (OTP)",
        #            user.email, "emails/otp.html", context)

        return Response({"message": "user created successfully", "data": {"user": serializer.data, wallet_balance: wallet_balance}}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Login a user",
    request_body=LoginSerializer,
    responses={200: "Login Successful", 400: "Bad Request"})
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

    @swagger_auto_schema(
        operation_description="Get user details",
        responses={200: UserSerializer})
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update user details",
        request_body=UserSerializer,
        responses={200: UserSerializer, 400: "Bad Request"})
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete user",
        responses={204: "User deleted Successfully"})
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "User deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='get',
    operation_description="Verify user",
    responses={200: "User Verified", 400: "Bad Request"})
@api_view(['GET'])
def verify_user(request, otp, email):
    try:

        check_otp = Otp.objects.filter(otp_code=otp).values().first()
        user = User.objects.filter(email=email).values().first()

        if user.get('is_user_verified'):
            return Response({"message": "User is already verified."}, status=status.HTTP_400_BAD_REQUEST)

        otp_creation_time = check_otp.get('created_at')
        if otp_creation_time and (timezone.now() - otp_creation_time) > timedelta(minutes=1):
            return Response({"message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.filter(email=email).update(is_user_verified=True)

        Otp.objects.filter(otp_code=otp).delete()

        return Response({"message": "User Verified"}, status=status.HTTP_200_OK)

    except Otp.DoesNotExist:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Resend OTP",
    responses={200: "OTP Sent", 400: "Bad Request"})
@api_view(['GET'])
def resend_otp(request, email):
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    otp_code = generate_otp()
    Otp.objects.create(user_id=user, otp_code=otp_code)
    context = {
        "name": f"{user.first_name} {user.last_name}",
        "otp": otp_code
    }
    send_email("Your One-Time Password (OTP)",
               user.email, "emails/otp.html", context)

    return Response({"message": "OTP Sent"}, status=status.HTTP_200_OK)
