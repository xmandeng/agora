from decimal import Decimal

import pytest

from agora.models import Node


@pytest.mark.parametrize(
    "wallet, expected",
    [
        (
            [Decimal("1"), Decimal("2"), Decimal("3"), Decimal("4")],
            [Decimal("4"), Decimal("3"), Decimal("2"), Decimal("1")],
        ),
        (
            [Decimal("1"), Decimal("2"), Decimal("1"), Decimal("3")],
            [Decimal("3"), Decimal("2"), Decimal("1"), Decimal("1")],
        ),
        (
            [Decimal("4"), Decimal("3"), Decimal("2"), Decimal("1")],
            [Decimal("4"), Decimal("3"), Decimal("2"), Decimal("1")],
        ),
    ],
    ids=["ascending", "dupes", "descending"],
)
def test_wallet_order(wallet, expected):
    node = Node(Decimal("20"), wallet=wallet, balance=Decimal("0"), path=[], cost=0)
    assert node.wallet == expected, "Wallet improperly sorted"


def test_hash():
    wallet = [Decimal("1"), Decimal("2"), Decimal("3")]
    node = Node(value=Decimal("20"), wallet=wallet, balance=Decimal("0"), path=[], cost=0)
    assert node.hash == (Decimal("3"), Decimal("2"), Decimal("1")), "Wallet hash mismatch"


@pytest.mark.parametrize(
    "balance, expected",
    [
        (
            Decimal("-1"),
            [],
        ),
        (
            Decimal("0"),
            [],
        ),
        (
            Decimal("1"),
            [],
        ),
    ],
    ids=["negative", "zero", "positive"],
)
def test_return_change_path(balance, expected):
    node = Node(value=Decimal("20"), wallet=[], balance=balance, path=[], cost=0)
    assert node.path == expected, "Change path not properly calculated"


@pytest.mark.parametrize(
    "balance, path, expected",
    [
        (
            Decimal("-1"),
            [Decimal("5")],
            1,
        ),
        (
            Decimal("0"),
            [Decimal("5")],
            len([Decimal("5")]),
        ),
        (
            Decimal("1"),
            [Decimal("5")],
            len([Decimal("5")]),
        ),
    ],
    ids=["negative", "zero", "positive"],
)
def test_return_change_cost(balance, path, expected):
    node = Node(value=Decimal("20"), wallet=[], balance=balance, path=path, cost=len(path))
    assert node.cost == expected, "Cost not properly calculated"


@pytest.mark.parametrize(
    "balance, expected",
    [
        (
            Decimal("-1"),
            Decimal("-1"),
        ),
        (
            Decimal("0"),
            Decimal("0"),
        ),
        (
            Decimal("1"),
            Decimal("1"),
        ),
    ],
    ids=["negative", "zero", "positive"],
)
def test_return_change_balance(balance, expected):
    node = Node(value=Decimal("20"), wallet=[], balance=balance, path=[], cost=0)
    assert node.balance == expected, "Balance not properly updated"
