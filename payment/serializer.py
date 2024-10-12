from rest_framework import serializers
from payment.models import Payment
from django.core.validators import MinValueValidator


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class StartPaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(5.00)],
        required=True
    )
