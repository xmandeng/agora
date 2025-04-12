from decimal import Decimal

import pytest

import agora.helpers as helpers
from agora.solutions.naive import naive_factory


@pytest.fixture(scope="session")
def wallet() -> list[Decimal]:
    money: dict[str, int] = {
        "100": 10,
        "20": 4,
        "10": 2,
        "1": 5,
        "0.25": 1,
        "0.10": 6,
        "0.05": 3,
        "0.01": 5,
    }
    return helpers.populate_wallet(money)


@pytest.mark.regression
@pytest.mark.parametrize(
    "price, expected",
    [
        (
            Decimal("15.05"),
            ((Decimal("20"), Decimal("0.05")), [Decimal("5.00")]),
        ),
        (
            Decimal("105.06"),
            ((Decimal("100"), Decimal("10"), Decimal("0.05"), Decimal("0.01")), [Decimal("5.00")]),
        ),
        (
            Decimal("150.05"),
            ((Decimal("100"), Decimal("100"), Decimal("0.05")), [Decimal("50.00")]),
        ),
    ],
    ids=["Price: $15.05", "Price: 105.06", "Price: $150.05"],
)
def test_naive(wallet, price, expected):
    result = naive_factory(wallet, price)()
    assert result == expected, f"Expected {expected}, but got {result}"
