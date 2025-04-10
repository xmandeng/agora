import logging
from decimal import Decimal
from typing import Callable

from agora.helper import find_viable_combinations, get_total, return_change

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def naive_factory(
    wallet: list[Decimal], price: Decimal
) -> Callable[[], tuple[tuple[Decimal, ...], list[Decimal]]]:

    best_combination: tuple[tuple[Decimal, ...], list[Decimal]] = (tuple(wallet), [])
    best_length: int = len(wallet)

    def naive() -> tuple[tuple[Decimal, ...], list[Decimal]]:
        nonlocal best_combination, best_length

        for picks in range(1, len(wallet) + 1):

            logger.debug(f"Trying combinations of {picks} item(s) from wallet")

            for combination in find_viable_combinations(wallet, picks, price):

                change = return_change(get_total(combination) - price)
                ccy_exchanged = len(combination) + len(change)

                if ccy_exchanged < best_length:
                    best_combination = (combination, change)
                    best_length = ccy_exchanged

            if best_length <= picks:
                logger.info("Stopped early. Best combination found.")
                break

        return best_combination

    return naive


if __name__ == "__main__":
    from agora.helper import populate_wallet

    price = Decimal("105.05")
    wallet = populate_wallet(
        {
            "100": 1,
            "20": 4,
            "10": 2,
            "1": 5,
            "0.25": 1,
            "0.10": 6,
            "0.05": 3,
            # "0.01": 5,
        }
    )

    # naive = naive_factory(wallet=wallet, price=price)
    tendered, change = naive_factory(wallet=wallet, price=price)()

    print(f"\nTendered: {list(tendered)}")
    print(f"Change:   {change}")
