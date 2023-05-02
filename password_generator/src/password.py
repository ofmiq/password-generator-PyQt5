import secrets
from enum import IntEnum
from math import log2


class PasswordComplexity(IntEnum):
    Deplorable = 0
    Weak = 30
    Good = 50
    Strong = 70
    Excellent = 120


def new_password(length: int, chars: str) -> str:
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password


def get_entropy(length: int, characters_num: int) -> float:
    try:
        entropy = length * log2(characters_num)
    except ValueError:
        return 0.0
    return round(entropy, 2)
