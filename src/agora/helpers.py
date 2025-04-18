from decimal import Decimal
from itertools import combinations

from agora.exceptions import InsufficientFundsError
from agora.ref_data import DECIMALIZED_DENOMINATIONS_USD


def populate_wallet(money: dict[str, int]) -> list[Decimal]:
    """Populate the wallet with the given amount."""
    wallet = []
    for denomination, count in money.items():
        wallet.extend([Decimal(denomination)] * count)
    return wallet


def get_total(wallet: list[Decimal] | tuple[Decimal, ...]) -> Decimal:
    return Decimal(sum(wallet))


def find_viable_combinations(
    wallet: list[Decimal], combination_length: int, target_price: Decimal
) -> list[tuple[Decimal, ...]]:
    """
    Generate a list of unique combinations from the wallet, where sum total equals or exceeds target_price

    DEV NOTES:

        (Q) Why do we return a filtered list?
        (A) To eliminate irrelavant combinations where InsufficientFundsError

        (Q) Why do we use a set?
        (A) This eliminates duplicate combinations that are not needed for the transaction

        (Q) Why do we sort the combinations?
        (A) This eliminates duplicate combinations that are not needed for the transaction

    EXAMPLE:

        Wallet: [20, 10, 10, 1, 1, 1, 1, 1, 0.25, 0.05, 0.05, 0.05]
        Price: 15.05

        Combination length: 2

        Unfiltered combinations: 13
        Combinations: {
                       (20, 0.05), (0.25, 0.05), (10, 0.05),
                       (0.05, 0.05), (1, 0.05), (1, 1),
                       (20, 1), (10, 1), (20, 10), (10, 10),
                       (20, 0.25), (10, 0.25), (1, 0.25)
                       }

        Filtered Result: [(20, 0.05), (20, 1), (20, 10), (20, 0.25), (10, 10)]

    """
    viable_combinations: set[tuple[Decimal, ...]] = {
        tuple(sorted(combination, reverse=True))
        for combination in combinations(wallet, combination_length)
        if sum(combination) >= target_price
    }

    if not viable_combinations:
        return []

    return sorted(viable_combinations, key=lambda combo: combo[0], reverse=True)


def calculate_change(balance: Decimal) -> list[Decimal]:
    zero_balance = Decimal("0")

    # exception handling
    if balance < zero_balance:
        raise InsufficientFundsError(f"Negative balance: {balance}")

    # base case
    if balance == zero_balance:
        return []

    # recursive case
    if balance > zero_balance:
        change = max(filter(lambda ccy: ccy <= balance, DECIMALIZED_DENOMINATIONS_USD))
        change_list = calculate_change(balance - change)
        change_list.append(change)

    return change_list


def find_acceptable_path(wallet: list[Decimal], balance: Decimal) -> list[Decimal]:

    if balance == 0:
        return []

    elif balance < 0:
        pick = -1 * max(filter(lambda ccy: ccy <= abs(balance), DECIMALIZED_DENOMINATIONS_USD))

    else:
        pick = min(wallet, key=lambda item: abs(balance - item))

    return [pick] + find_acceptable_path(wallet, balance - pick)
