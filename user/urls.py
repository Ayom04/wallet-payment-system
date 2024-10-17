from django.urls import path
from user.views import create_user, login, UserView, verify_user, resend_otp, start_forget_password, reset_password

urlpatterns = [
    path("create", create_user, name="create_user"),
    path("login", login, name="login"),
    path("profile", UserView.as_view(), name="profile"),
    path("verify/<str:email>/<str:otp>", verify_user, name="verify_user"),
    path("resend-otp/<str:email>", resend_otp, name="resend_otp"),
    path("forget-password", start_forget_password, name="start_forget_password"),
    path("reset-password", reset_password, name="reset_password")
]
