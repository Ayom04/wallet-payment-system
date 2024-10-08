from django.db import models
import uuid
from user.models import User
# Create your models here.


class Transcation(models.Model):
    class TransactionType(models.TextChoices):
        DEBIT = 'DEBIT', 'Debit'
        CREDIT = 'CREDIT', 'Credit'

    class TransactionStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        ROLLBACK_INITIATED = 'ROLLBACK_INITIATED', 'Rollback Initiated'
        ROLLBACK_FAILED = 'ROLLBACK_FAILED', 'Rollback Failed'
        ROLLBACK_COMPLETED = 'ROLLBACK_COMPLETED', 'Rollback Completed'

    transaction_id = models.UUIDField(
        max_length=255, default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user_id = models.ForeignKey(
        User, related_name='user_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_type = models.CharField(
        max_length=255, choices=TransactionType.choices)
    transaction_status = models.CharField(
        max_length=255, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_id
