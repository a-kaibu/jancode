"""SVG rendering of encoded JAN bar patterns."""

from jancode.encoding import encode

# Quiet zones (left, right) in modules, as specified by GS1.
QUIET_ZONES = {95: (11, 7), 67: (7, 7)}
# Default bar_height (69) is the GS1 nominal 22.85 mm at a 0.33 mm module.
# Guard bars extend below the other bars by this many modules.
GUARD_EXTENSION = 5
FONT_SIZE = 8
TEXT_AREA = 10


def _guard_modules(length: int) -> set[int]:
    center = length // 2
    return {0, 1, 2, *range(center - 2, center + 3), length - 3, length - 2, length - 1}


def _text_positions(length: int) -> list[float]:
    """Return the x centre (in modules, relative to the first bar) of each digit."""
    center = length // 2
    half = (center - 2 - 3) // 7  # digits on each side of the centre guard
    left = [3 + 7 * i + 3.5 for i in range(half)]
    right = [center + 3 + 7 * i + 3.5 for i in range(half)]
    if length == 95:
        return [-QUIET_ZONES[95][0] / 2, *left, *right]
    return left + right


def render(bits: str, text: str, *, module_width: float = 2, bar_height: float = 69) -> str:
    """Render a 67 or 95 module bit string and its human readable ``text`` as SVG.

    Coordinates in the ``viewBox`` are in modules. ``module_width`` sets the
    displayed size of one module in px, and ``bar_height`` the height of the
    regular bars in modules.
    """
    if len(bits) not in QUIET_ZONES:
        raise ValueError("Expected a 67 or 95 module bit string")
    if module_width <= 0 or bar_height <= 0:
        raise ValueError("module_width and bar_height must be positive")

    quiet_left, quiet_right = QUIET_ZONES[len(bits)]
    width = quiet_left + len(bits) + quiet_right
    height = bar_height + TEXT_AREA
    guards = _guard_modules(len(bits))

    elements = []
    start = None
    for i, bit in enumerate(bits + "0"):
        if bit == "1" and start is None:
            start = i
        elif bit != "1" and start is not None:
            h = bar_height + GUARD_EXTENSION if start in guards else bar_height
            elements.append(
                f'<rect x="{quiet_left + start}" y="0" width="{i - start}" height="{h:g}"/>'
            )
            start = None

    text_y = bar_height + FONT_SIZE
    for x, char in zip(_text_positions(len(bits)), text):
        elements.append(f'<text x="{quiet_left + x:g}" y="{text_y:g}">{char}</text>')

    body = "\n".join(f"    {e}" for e in elements)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width * module_width:g}" height="{height * module_width:g}" '
        f'viewBox="0 0 {width} {height:g}">\n'
        f'  <rect width="100%" height="100%" fill="#fff"/>\n'
        f'  <g fill="#000" font-family="monospace" font-size="{FONT_SIZE}" text-anchor="middle">\n'
        f"{body}\n"
        "  </g>\n"
        "</svg>\n"
    )


def to_svg(number: str, *, module_width: float = 2, bar_height: float = 69) -> str:
    """Return ``number`` as an SVG barcode string.

    Raises ``ValueError`` if ``number`` is not a valid JAN code.
    """
    return render(encode(number), number, module_width=module_width, bar_height=bar_height)
