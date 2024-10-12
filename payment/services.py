import requests
from django.conf import settings


class PaymentService:
    def __init__(self):
        # Initialize payment URL and secret from settings
        self.payment_url = settings.ENV_VARIABLES.get('PAYMENT_BASE_URL')
        self.payment_secret = settings.ENV_VARIABLES.get('PAYMENT_SECRET_KEY')

    def start_payment(self, email, amount):
        """Start a payment transaction."""
        amount_in_kobo = amount * 100
        response = requests.post(
            url=f"{self.payment_url}/transaction/initialize",
            json={"email": email, "amount": amount_in_kobo},
            headers={"Authorization": f"Bearer {self.payment_secret}"}
        )
        return response.json()

    def verify_payment(self, payment_reference):
        """Verify the payment transaction."""
        response = requests.get(
            url=f"{self.payment_url}/transaction/verify/{payment_reference}",
            headers={"Authorization": f"Bearer {self.payment_secret}"}
        )
        return response.json()
