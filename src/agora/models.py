from dataclasses import dataclass
from decimal import Decimal

# from pydantic import BaseModel, Field
from agora.helpers import calculate_change
from agora.ref_data import DECIMALIZED_DENOMINATIONS_USD


# TODO: convert to immutable Pydantic model
@dataclass
class Node:
    value: Decimal
    wallet: list[Decimal]
    balance: Decimal
    path: list[Decimal]
    cost: int

    def __post_init__(self):
        if self.balance >= 0:
            self.wallet = sorted(self.wallet, reverse=True)
        elif self.balance < 0:
            change = -1 * max(
                filter(lambda ccy: ccy <= abs(self.balance), DECIMALIZED_DENOMINATIONS_USD)
            )
            self.wallet = [change] + sorted(self.wallet, reverse=True)

    @classmethod
    def create_child_node(cls, denomination: Decimal, parent: "Node") -> "Node":
        return cls(
            value=denomination,
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

    def is_viable(self, denomination: Decimal) -> bool:
        wallet_filter = [item for item in self.wallet if item > 0 and item <= denomination]
        return self.balance - sum(wallet_filter) <= 0
