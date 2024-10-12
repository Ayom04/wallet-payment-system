from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from wallet.models import Wallet


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user_id=instance)


# @receiver(post_save, sender=User)
# def save_wallet(sender, instance, **kwargs):
#     wallet = instance.user_wallet

#     if wallet:
#         wallet.save()
#         print('Wallet saved')
#     else:
#         print('No wallet found for the user.')
