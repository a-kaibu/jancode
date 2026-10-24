"""Check digit calculation and validation (GS1 modulo 10)."""


def _is_digits(value: str, lengths: tuple[int, ...]) -> bool:
    return len(value) in lengths and value.isascii() and value.isdecimal()


def calculate_check_digit(data: str) -> str:
    """Return the check digit for the 7 (JAN-8) or 12 (JAN-13) data digits.

    Weights 3 and 1 alternate from the rightmost data digit, which makes the
    same rule work for both lengths.
    """
    if not isinstance(data, str) or not _is_digits(data, (7, 12)):
        raise ValueError("Expected 7 or 12 ASCII digits")

    total = sum(int(digit) * (3 if i % 2 == 0 else 1) for i, digit in enumerate(reversed(data)))
    return str(-total % 10)


def is_valid(number: str) -> bool:
    """Return whether ``number`` is an 8 or 13 digit JAN code with a correct check digit."""
    if not isinstance(number, str) or not _is_digits(number, (8, 13)):
        return False
    return number[-1] == calculate_check_digit(number[:-1])
