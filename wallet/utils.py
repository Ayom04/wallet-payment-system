from transaction.models import Transaction
from wallet.models import Wallet
from payment.models import Payment


def credit(amount, user, comment=None):
    wallet = Wallet.objects.get(user_id=user)
    amount_after = wallet.amount_after + amount
    update_wallet(user, wallet, wallet.amount_after, amount_after)
    Transaction.objects.create(
        user_id=user, wallet_id=wallet, amount=amount, transaction_type='credit', comment=comment)
    return True


def debit(amount, user, comment=None):
    wallet = Wallet.objects.get(user_id=user)
    if wallet.amount_after < amount:
        return False
    amount_after = wallet.amount_after - amount

    update_wallet(user, wallet, wallet.amount_after, amount_after)

    Transaction.objects.create(
        user_id=user, wallet_id=wallet, amount=amount, transaction_type='debit', comment=comment)
    return True


def update_wallet(user, wallet, initial_amount, amount_after):
    wallet.amount_before = initial_amount
    wallet.amount_after = amount_after
    wallet.save()
    return wallet
