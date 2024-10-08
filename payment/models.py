from django.db import models
import uuid
from user.models import User


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        FULFILLED = 'FULFILLED', 'Fulfilled'
    payment_id = models.CharField(
        max_length=255, default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user_id = models.ForeignKey(
        User, related_name='user_payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    payment_reference = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_id
