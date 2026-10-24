"""Encoding of JAN-8 / JAN-13 into module bit strings."""

from jancode.checksum import is_valid

# fmt: off
# Left-hand odd parity (L), left-hand even parity (G) and right-hand (R) patterns.
L_PATTERNS = (
    "0001101", "0011001", "0010011", "0111101", "0100011",
    "0110001", "0101111", "0111011", "0110111", "0001011",
)
G_PATTERNS = (
    "0100111", "0110011", "0011011", "0100001", "0011101",
    "0111001", "0000101", "0010001", "0001001", "0010111",
)
R_PATTERNS = (
    "1110010", "1100110", "1101100", "1000010", "1011100",
    "1001110", "1010000", "1000100", "1001000", "1110100",
)

# Parity of the six left-hand digits of JAN-13, selected by the leading digit.
PARITY_PATTERNS = (
    "LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG",
    "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL",
)

# fmt: on

EDGE_GUARD = "101"
CENTER_GUARD = "01010"


def encode(number: str) -> str:
    """Return the bar pattern of ``number`` as a string of ``0``/``1`` modules.

    The result includes the guard patterns: 67 modules for JAN-8 and 95 for
    JAN-13. Raises ``ValueError`` if ``number`` is not a valid JAN code.
    """
    if not is_valid(number):
        raise ValueError(f"Invalid JAN code: {number!r}")

    if len(number) == 13:
        parity = PARITY_PATTERNS[int(number[0])]
        left, right = number[1:7], number[7:]
    else:
        parity = "L" * 4
        left, right = number[:4], number[4:]

    left_bits = "".join(
        (L_PATTERNS if p == "L" else G_PATTERNS)[int(d)] for p, d in zip(parity, left)
    )
    right_bits = "".join(R_PATTERNS[int(d)] for d in right)
    return EDGE_GUARD + left_bits + CENTER_GUARD + right_bits + EDGE_GUARD
