import xml.etree.ElementTree as ET

import pytest

from jancode import encode, to_svg
from jancode.svg import render

NS = {"svg": "http://www.w3.org/2000/svg"}


def bars(root):
    return [r for r in root.iterfind(".//svg:g/svg:rect", NS)]


def covered_modules(root, offset):
    modules = set()
    for rect in bars(root):
        x, w = int(rect.get("x")), int(rect.get("width"))
        modules.update(range(x - offset, x - offset + w))
    return modules


@pytest.mark.parametrize(
    ("number", "quiet_left", "quiet_right"),
    [("4933032010579", 11, 7), ("96385074", 7, 7)],
)
def test_render_bars_match_bits(number, quiet_left, quiet_right):
    bits = encode(number)
    root = ET.fromstring(render(bits, number))

    assert root.get("viewBox").split()[2] == str(quiet_left + len(bits) + quiet_right)
    assert covered_modules(root, quiet_left) == {i for i, b in enumerate(bits) if b == "1"}


@pytest.mark.parametrize("number", ["4933032010579", "96385074"])
def test_render_text(number):
    root = ET.fromstring(to_svg(number))
    texts = root.findall(".//svg:text", NS)
    assert "".join(t.text for t in texts) == number
    xs = [float(t.get("x")) for t in texts]
    assert xs == sorted(xs)


def test_guard_bars_are_longer():
    root = ET.fromstring(to_svg("96385074", bar_height=50))
    heights = {float(r.get("height")) for r in bars(root)}
    assert heights == {50, 55}
    assert float(bars(root)[0].get("height")) == 55


def test_module_width_scales_display_size_only():
    small = ET.fromstring(to_svg("96385074", module_width=1))
    large = ET.fromstring(to_svg("96385074", module_width=3))
    assert small.get("viewBox") == large.get("viewBox")
    assert float(large.get("width")) == 3 * float(small.get("width"))


def test_to_svg_rejects_invalid():
    with pytest.raises(ValueError):
        to_svg("96385072")


@pytest.mark.parametrize("bits", ["", "101", "1" * 94])
def test_render_rejects_bad_length(bits):
    with pytest.raises(ValueError):
        render(bits, "")


def test_public_api():
    import jancode

    assert sorted(jancode.__all__) == ["calculate_check_digit", "encode", "is_valid", "to_svg"]
