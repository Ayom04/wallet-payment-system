from django.contrib import admin
from user.models import User
from user.models import Otp

# Register your models here.

admin.site.register(User)
admin.site.register(Otp)
