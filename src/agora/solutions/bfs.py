from collections import deque
from decimal import Decimal
from typing import Callable

from agora.exceptions import check_for_sufficient_funds
from agora.models import Node


def bfs_factory(wallet: list[Decimal], price: Decimal) -> Callable[[], tuple[list[Decimal], int]]:
    check_for_sufficient_funds(wallet, price)

    shortest_path: list[Decimal] = wallet
    least_cost: int = len(wallet)

    def breadth_first_search() -> tuple[list[Decimal], int]:
        nonlocal shortest_path, least_cost

        queue: deque = deque()
        visited: set[tuple[Decimal, ...]] = set()

        root = Node(name="root", wallet=wallet, balance=price, path=[], cost=0)

        queue.append(root)
        visited.add(root.hash)

        while queue:
            parent: Node = queue.popleft()

            if parent.cost >= least_cost:
                continue

            if parent.balance == 0:
                least_cost = parent.cost
                shortest_path = parent.path
                continue

            for currency in parent.denominations:
                child = Node.create_child_node(currency, parent)

                if child.hash in visited:
                    continue

                queue.append(child)
                visited.add(child.hash)

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
