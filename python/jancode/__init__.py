"""Validate and encode JAN (EAN-8 / EAN-13) codes and render them as SVG."""

from importlib.metadata import version

from jancode.checksum import calculate_check_digit, is_valid
from jancode.encoding import encode
from jancode.svg import to_svg

__version__ = version("jancode")

__all__ = ["calculate_check_digit", "encode", "is_valid", "to_svg"]
