from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework.decorators import api_view
from payment.serializer import StartPaymentSerializer
from wallet.models import Wallet
from drf_yasg.utils import swagger_auto_schema
from payment.services import PaymentService
from payment.models import Payment
from wallet.utils import credit, debit
from rest_framework.permissions import IsAuthenticated
from user.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


@swagger_auto_schema(
    methods=["post"],
    request_body=StartPaymentSerializer,
    operation_summary="Start Payment",
    operation_description="Start a payment transaction"
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def payment_checkout(request):
    serializer = StartPaymentSerializer(data=request.data)
    if serializer.is_valid():
        amount = serializer.validated_data["amount"]

        payment_service = PaymentService()
        initialize_payment = payment_service.start_payment(
            email=request.user.email,
            amount=amount)

        if initialize_payment["status"] != True:
            return Response({
                "message": "Payment Failed",
            }, status=status.HTTP_400_BAD_REQUEST)

        Payment.objects.create(
            user_id=request.user,
            wallet_id=Wallet.objects.get(user_id=request.user),
            amount=serializer.validated_data["amount"],
            payment_reference=initialize_payment["data"]["reference"],
            payment_status=Payment.PaymentType.PENDING
        )

        print(initialize_payment["data"]["reference"])

        return Response({"message": "Payment Successful",
                        "data": {
                            "authorization_url": initialize_payment["data"]["authorization_url"],
                        }}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=["get"],
    operation_summary="Verify Payment",
    operation_description="Verify a payment transaction"
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_payment(request, payment_reference):

    check_payment_status = Payment.objects.filter(
        payment_reference=payment_reference).first()

    if check_payment_status.payment_status == Payment.PaymentType.FULFILLED:
        return Response({
            "message": "Invalid Payment Reference",
        }, status=status.HTTP_400_BAD_REQUEST)

    payment_service = PaymentService()

    verify_payment = payment_service.verify_payment(
        payment_reference=payment_reference)

    if verify_payment["data"]["status"] != "success":
        return Response({
            "message": "Payment Failed",
            "data": verify_payment
        }, status=status.HTTP_400_BAD_REQUEST)

    if check_payment_status.amount != (verify_payment["data"]["amount"] / 100):
        return Response({
            "message": "Payment Amount Mismatch",
        }, status=status.HTTP_400_BAD_REQUEST)

    check_payment_status.payment_status = Payment.PaymentType.FULFILLED
    check_payment_status.save()

    credit(check_payment_status.amount, request.user, "Wallet funding")

    return Response({
        "message": "Payment Successful and Wallet Funded"
    }, status=status.HTTP_200_OK)
