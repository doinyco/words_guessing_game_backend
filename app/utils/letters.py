import random

LETTER_POOL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_letter():
    return random.choice(LETTER_POOL)