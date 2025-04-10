from decimal import Decimal

import pytest

import agora.helper as helper


@pytest.fixture(scope="session")
def wallet() -> list[Decimal]:
    money: dict[str, int] = {
        "100": 1,
        "20": 4,
        "10": 2,
        "1": 5,
        "0.25": 1,
        "0.10": 6,
        "0.05": 3,
    }
    return helper.populate_wallet(money)


@pytest.mark.parametrize(
    "price, picks, expected",
    [
        (Decimal("15.05"), 2, 13),
        (Decimal("150.05"), 2, 0),
    ],
)
def test_path_validation(wallet, price, picks, expected):
    all_paths = len(helper.find_viable_combinations(wallet, picks, price))

    assert all_paths == expected, f"Expected {expected}, but got {all_paths}"
