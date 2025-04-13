from dataclasses import dataclass
from decimal import Decimal

from agora.helpers import calculate_change


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

    @classmethod
    def create_child_node(cls, denomination: Decimal, parent: "Node") -> "Node":
        return cls(
            name=str(denomination),
            wallet=parent.pick_from_wallet(denomination),
            balance=parent.balance - denomination,
            path=parent.path + [denomination],
            cost=parent.cost + 1,
        )

    @property
    def hash(self) -> tuple[Decimal, ...]:
        return tuple(self.wallet)

    @property
    def denominations(self) -> list[Decimal]:
        return sorted(set(self.wallet), reverse=True)

    def pick_from_wallet(self, denomination: Decimal) -> list[Decimal]:
        if denomination not in self.wallet:
            raise ValueError(f"Denomination {denomination} not in wallet")

        new_wallet: list[Decimal] = self.wallet.copy()
        new_wallet.remove(denomination)
        return new_wallet

    def return_change(self) -> None:
        change = calculate_change(-1 * self.balance)
        self.path += change
        self.cost += len(change)
        self.balance += sum(change)
