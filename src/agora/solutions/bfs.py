from collections import deque
from decimal import Decimal
from typing import Callable

from agora.models import Node


def bfs_factory(wallet: list[Decimal], price: Decimal) -> Callable[[], tuple[list[Decimal], int]]:

    if not wallet or price <= 0:
        raise ValueError("Invalid wallet or price")

    elif sum(wallet) < price:
        raise ValueError(f"Insufficient funds: {sum(wallet)} < {price}")

    shortest_path: list[Decimal] = wallet
    least_cost: int = len(wallet)

    def breadth_first_search() -> tuple[list[Decimal], int]:
        nonlocal shortest_path, least_cost
        queue: deque = deque()
        visited: set[tuple[Decimal, ...]] = set()

        root = Node(name="root", wallet=wallet, balance=price, path=[], cost=0)

        queue.append(root)
        visited.add(root.wallet_hash)

        while queue:
            current: Node = queue.popleft()

            if current.cost >= least_cost:
                continue

            if current.balance == 0:
                least_cost = current.cost
                shortest_path = current.path
                continue

            for ccy in current.denominations:
                node = Node.create_child(ccy, current)

                if node.wallet_hash in visited:
                    continue

                queue.append(node)
                visited.add(node.wallet_hash)

        return shortest_path, least_cost

    return breadth_first_search


if __name__ == "__main__":
    from agora.helper import populate_wallet

    price = Decimal("105.06")
    wallet = populate_wallet(
        {
            "100": 100,
            "20": 4,
            "10": 2,
            "1": 5,
            "0.25": 1,
            "0.10": 6,
            "0.05": 3,
            "0.01": 5,
        }
    )

    path, cost = bfs_factory(wallet, price)()

    print(f"Path: {path}")
