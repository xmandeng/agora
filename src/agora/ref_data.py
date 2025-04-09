from decimal import Decimal

USD_DENOMINATIONS: list[str] = [
    "0.01",
    "0.05",
    "0.10",
    "0.25",
    # "0.50", # Rarely used
    "1.00",
    "5.00",
    "10.00",
    "20.00",
    "50.00",
    "100.00",
]

DENOMINATION_IN_DECIMAL: list[Decimal] = [
    Decimal(denomination) for denomination in USD_DENOMINATIONS
]
