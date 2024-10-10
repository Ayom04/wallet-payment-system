from django.db import models
import uuid
from user.models import User


class Wallet(models.Model):
    wallet_id = models.UUIDField(
        max_length=255, default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user_id = models.ForeignKey(
        User, related_name='user_wallet', on_delete=models.CASCADE)
    amount_before = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.00)
    amount_after = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.wallet_id)

    def get_wallet_balance(self):
        return self.amount_after
