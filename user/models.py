from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from user.managers import UserManager


class User(AbstractBaseUser):
    user_id = models.UUIDField(
        max_length=255, default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    email = models.EmailField(max_length=255, unique=True, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=255, unique=True)
    nin = models.IntegerField(unique=True)
    is_nin_verified = models.BooleanField(default=False)
    bvn = models.IntegerField(unique=True)
    is_bvn_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField()
    is_user_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_active(self):
        return self.is_active

    @property
    def is_user_verified(self):
        return self.is_user_verified

    @property
    def is_nin_verified(self):
        return self.is_nin_verified
