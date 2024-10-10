from django.urls import path
from user.views import create_user, login, UserView

urlpatterns = [
    path("create", create_user, name="create_user"),
    path("login", login, name="login"),
    path("profile", UserView.as_view(), name="profile"),
]
