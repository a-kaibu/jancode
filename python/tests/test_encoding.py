import pytest

from jancode import encode

# Outputs of the previous implementation, kept to guard against regressions.
EXPECTED = {
    "4933032010579": "10100010110100001011110100011010100001001101101010111001011001101110010100111010001001110100101",
    "4901234567894": "10100010110100111001100100100110100001001110101010100111010100001000100100100011101001011100101",
    "0000000000000": "10100011010001101000110100011010001101000110101010111001011100101110010111001011100101110010101",
    "96385074": "1010001011010111101111010110111010101001110111001010001001011100101",
    "49123456": "1010100011000101100110010010011010101000010101110010011101010000101",
}


@pytest.mark.parametrize(("number", "expected"), EXPECTED.items())
def test_encode(number, expected):
    assert encode(number) == expected


@pytest.mark.parametrize(("number", "length"), [("4933032010579", 95), ("96385074", 67)])
def test_encode_length_and_guards(number, length):
    bits = encode(number)
    center = length // 2
    assert len(bits) == length
    assert bits[:3] == bits[-3:] == "101"
    assert bits[center - 2 : center + 3] == "01010"


@pytest.mark.parametrize("number", ["4933032010578", "96385072", "123", "１２３４５６７８"])
def test_encode_rejects_invalid(number):
    with pytest.raises(ValueError):
        encode(number)
