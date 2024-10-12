from django.urls import path
from payment.views import payment_checkout,  verify_payment

urlpatterns = [
    path("start/", payment_checkout, name="start_payment"),
    path("verify/<str:payment_reference>/",
         verify_payment, name="verify_payment"),
]
