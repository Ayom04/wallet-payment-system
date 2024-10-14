from django.db import models
import uuid
from user.models import User


class Otp(models.Model):
    otp_id = models.UUIDField(
        max_length=255, default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_otp')
    otp_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.otp_id)
