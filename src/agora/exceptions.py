from decimal import Decimal


class InsufficientFundsError(ValueError):
    """Exception raised when there are insufficient funds for a transaction."""

    pass


class NegativePriceError(ValueError):
    """Exception raised when there are insufficient funds for a transaction."""

    pass


class EmptyWalletError(ValueError):
    """Exception raised when there are insufficient funds for a transaction."""

    pass


def check_for_sufficient_funds(wallet: list[Decimal], price: Decimal) -> None:
    if not wallet:
        raise EmptyWalletError("Invalid wallet or price")

    if price <= 0:
        raise NegativePriceError("Invalid wallet or price")

    elif sum(wallet) < price:
        raise InsufficientFundsError(f"Insufficient funds: {sum(wallet)} < {price}")
