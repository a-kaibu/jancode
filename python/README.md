# JANcode

## What is this

Library to validate JAN codes (EAN-13 / EAN-8) and render them as SVG barcodes.  
<https://pypi.org/project/jancode/>  

![jancode](https://raw.githubusercontent.com/yashikota/jancode/master/example.png)

## Features

- Standard (13 digit) and short (8 digit) JAN codes
- Check digit calculation and validation
- SVG output with human readable digits and GS1 quiet zones
- No runtime dependencies

## Example

```py
import jancode

number = "4933032010579"

jancode.calculate_check_digit("493303201057")  # "9"
jancode.is_valid(number)  # True
jancode.encode(number)  # "10100010110100001011..." (95 modules, 67 for JAN-8)
svg = jancode.to_svg(number)
```

Codes are passed as `str` so that leading zeros are kept.  
`encode()` and `to_svg()` raise `ValueError` for an invalid code, while `is_valid()` returns `False`.

`to_svg()` accepts two drawing parameters:

- `module_width`: displayed width of one module in px (default `2`)
- `bar_height`: height of the bars in modules (default `69`)

The library does not write files. Save the SVG yourself if needed:

```py
from pathlib import Path

Path("barcode.svg").write_text(jancode.to_svg("4933032010579"), encoding="utf-8")
```

Note that producing an SVG does not by itself guarantee that a printed label meets GS1 size and print quality requirements.

## Migrating from 1.x

`generate()` has been removed and codes must be strings:

```py
# 1.x
jancode.generate(4933032010579, "./img")

# 2.x
Path("img/4933032010579.svg").write_text(jancode.to_svg("4933032010579"), encoding="utf-8")
```

## Development

Uses [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run pytest
uv run ruff check .
uv run mypy
uv build
```
