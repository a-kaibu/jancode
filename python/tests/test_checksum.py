import pytest

from jancode import calculate_check_digit, is_valid


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("493303201057", "9"),
        ("490123456789", "4"),
        ("000000000000", "0"),
        ("9638507", "4"),
        ("4912345", "6"),
        ("0000000", "0"),
    ],
)
def test_calculate_check_digit(data, expected):
    assert calculate_check_digit(data) == expected


@pytest.mark.parametrize(
    "data",
    [
        "",
        "123456",
        "12345678",
        "12345678901",
        "1234567890123",
        "123456a",
        "１２３４５６７",
        1234567,
    ],
)
def test_calculate_check_digit_rejects_invalid_input(data):
    with pytest.raises(ValueError):
        calculate_check_digit(data)


@pytest.mark.parametrize("number", ["4933032010579", "96385074", "00000000", "0000000000000"])
def test_is_valid(number):
    assert is_valid(number)


@pytest.mark.parametrize(
    "number",
    [
        "4933032010578",
        "96385072",
        "",
        "9638507",
        "1234567890",
        "１２３４５６７８",
        "9638507a",
        " 96385074",
        96385074,
        None,
    ],
)
def test_is_valid_rejects(number):
    assert not is_valid(number)
