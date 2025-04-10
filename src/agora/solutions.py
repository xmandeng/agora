from collections import deque
from decimal import Decimal
from typing import Callable, Optional

from agora.helper import return_change
from agora.models import Node


def bfs_factory(wallet: list[Decimal], price: Decimal) -> Callable[[], tuple[list[Decimal], int]]:

    if not wallet or price <= 0:
        raise ValueError("Invalid wallet or price")

    elif sum(wallet) < price:
        raise ValueError(f"Insufficient funds: {sum(wallet)} < {price}")

    shortest_path: Optional[list[Decimal]] = None
    least_cost: int = len(wallet)

    def bfs() -> tuple[list[Decimal], int]:
        nonlocal shortest_path, least_cost

        root = Node(name="root", wallet=wallet, balance=price, path=[], cost=0)

        queue: deque = deque()
        queue.append(root)

        visited: set[tuple[Decimal, ...]] = {root.hashable_wallet}

        while queue:
            current: Node = queue.popleft()
            if current.cost >= least_cost:
                continue

            if current.balance < 0:
                change = return_change(-1 * current.balance)

                current.path += change
                current.cost += len(change)
                current.balance += sum(change)

                if current.cost >= least_cost:
                    continue

            if current.balance == 0:
                shortest_path = current.path
                least_cost = current.cost
                continue

            for cash in current.wallet:

                new_wallet = current.wallet.copy()
                new_wallet.remove(cash)

                state = Node(
                    name=str(cash),
                    wallet=new_wallet,
                    balance=current.balance - cash,
                    path=current.path + [cash],
                    cost=current.cost + 1,
                )

                if state.hashable_wallet in visited:
                    continue
                else:
                    queue.append(state)
                    visited.add(state.hashable_wallet)

        return shortest_path or [], least_cost

    return bfs


if __name__ == "__main__":
    from agora.helper import populate_wallet

    price: Decimal = Decimal("15.06")
    money: dict[str, int] = {
        "100": 1,
        "20": 4,
        "10": 2,
        "1": 5,
        "0.25": 1,
        "0.10": 6,
        "0.05": 3,
        "0.01": 5,
    }

    # setup wallet
    wallet = populate_wallet(money)

    bfs = bfs_factory(wallet, price)
    path, cost = bfs()

    print(f"Path: {path}")
