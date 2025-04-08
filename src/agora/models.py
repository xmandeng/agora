# from pydantic import BaseModel, Field
from dataclasses import dataclass

"""
Algorithm: Top of Mind

1. Verify you have enough money in your wallet to make a payment - raise a ValueError if not.
2. Find the largest note less than the payment amount.
3. Find the smallest note greater than the payment amount.
"""


@dataclass
class Wallet:
    pass


@dataclass
class Node:

    id: str
    name: str
    value: float
    wallet: list[float]
    description: str
