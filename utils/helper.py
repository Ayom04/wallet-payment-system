import random


def generate_otp(num=6):
    if num < 6:
        return random.randint(100000, 999999)

    return random.randint(10**(num-1), 10**num-1)
