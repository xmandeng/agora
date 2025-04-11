from dataclasses import dataclass
from decimal import Decimal

from agora.helper import return_change


@dataclass
class Node:
    name: str
    wallet: list[Decimal]
    balance: Decimal
    path: list[Decimal]
    cost: int

    def __post_init__(self):
        self.wallet = sorted(self.wallet, reverse=True)
        if self.balance < 0:
            self.return_change()

    @property
    def wallet_hash(self) -> tuple[Decimal, ...]:
        return tuple(self.wallet)

    @property
    def denominations(self) -> set[Decimal]:
        return set(self.wallet)

    def pick_from_wallet(self, denomination: Decimal) -> list[Decimal]:
        new_wallet: list[Decimal] = self.wallet.copy()
        new_wallet.remove(denomination)
        return new_wallet

    def return_change(self) -> None:
        change = return_change(-1 * self.balance)
        self.path += change
        self.cost += len(change)
        self.balance += sum(change)
