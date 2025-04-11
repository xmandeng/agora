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
    node = Node(name="test", wallet=wallet, balance=Decimal("0"), path=[], cost=0)
    assert node.wallet == expected, "Wallet improperly sorted"


def test_wallet_hash():
    wallet = [Decimal("1"), Decimal("2"), Decimal("3")]
    node = Node(name="test", wallet=wallet, balance=Decimal("0"), path=[], cost=0)
    assert node.wallet_hash == (Decimal("3"), Decimal("2"), Decimal("1")), "Wallet hash mismatch"


@pytest.mark.parametrize(
    "balance, expected",
    [
        (
            Decimal("-1"),
            [Decimal("1.00")],
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
def test_change_path(balance, expected):
    node = Node(name="test", wallet=[], balance=balance, path=[], cost=0)
    assert node.path == expected, "Change path not properly calculated"


@pytest.mark.parametrize(
    "balance, path, expected",
    [
        (
            Decimal("-1"),
            test_path := [Decimal("5")],
            len(test_path) + 1,
        ),
        (
            Decimal("0"),
            test_path,
            len(test_path),
        ),
        (
            Decimal("1"),
            test_path,
            len(test_path),
        ),
    ],
    ids=["negative", "zero", "positive"],
)
def test_change_cost(balance, path, expected):
    node = Node(name="test", wallet=[], balance=balance, path=path, cost=len(path))
    assert node.cost == expected, "Cost not properly calculated"


@pytest.mark.parametrize(
    "balance, expected",
    [
        (
            Decimal("-1"),
            Decimal("0"),
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
def test_change_balance(balance, expected):
    node = Node(name="test", wallet=[], balance=balance, path=[], cost=0)
    assert node.balance == expected, "Balance not properly updated"
