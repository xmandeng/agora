from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Node:
    name: str
    wallet: list[Decimal]
    balance: Decimal
    path: list[Decimal]
    cost: int

    def __post_init__(self):
        self.wallet = sorted(self.wallet)

    @property
    def hashable_wallet(self) -> tuple[Decimal, ...]:
        return tuple(self.wallet)
