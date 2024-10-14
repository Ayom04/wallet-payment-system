from rest_framework.serializers import ModelSerializer
from wallet.models import Wallet
from transaction.serializer import TransactionSerializer
from payment.serializer import PaymentSerializer


class WalletSerializer(ModelSerializer):
    wallet_transactions = TransactionSerializer(many=True, read_only=True)
    wallet_payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Wallet
        fields = ["amount_after", "wallet_transactions", "wallet_payments"]
