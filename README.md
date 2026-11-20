# Number Plate Keychain Designer

A single-page web app for designing Indian number-plate style keychains, previewing them in 3D, and exporting a ready-to-slice multi-colour 3MF for a Bambu Lab P1S + AMS.

## Run it

Double-click `keychain-designer.html`. It opens in any modern browser.
An internet connection is needed the first time, because the 3D preview loads three.js (v0.160) from cdn.jsdelivr.net.

## Folder layout

| Path | What it is |
|---|---|
| `keychain-designer.html` | The built app (template + fonts in one file). This is the file to open or upload to the website. |
| `src/template.html` | App source. Edit this, not the built file. It contains a `__FONTS__` placeholder. |
| `src/fonts.json` | Glyph outlines for the three fonts, extracted from the font files. |
| `tools/extract_fonts.py` | Regenerates `src/fonts.json` from .ttf files (needs Python + fontTools). |
| `fonts/` | Source .ttf files and their OFL licences, used by `extract_fonts.py`. |
| `tools/build.py` | Puts `fonts.json` into `template.html` to produce `keychain-designer.html`. |

## Rebuild after editing

```
python tools/build.py
```

To change fonts, put the .ttf in `fonts/`, edit the font list at the bottom of `tools/extract_fonts.py`, then run:

```
pip install fonttools
python tools/extract_fonts.py
python tools/build.py
```

Fonts used (all SIL Open Font License): Roboto Condensed ExtraBold (instanced from Roboto variable), Anton, Archivo Black.

## How the export works

- **Download 3MF** gives one .3mf file: the keychain is a single object, with one part per colour (Plate, Text + border, Side band, Band emblem).
- Each colour already has a filament number: the plate colour is filament 1, then each new colour gets the next number. Parts with the same colour (usually plate and emblem) share a filament. The 3D view's legend shows F1, F2, F3.
- In Bambu Studio: open the .3mf, then point filaments 1, 2, 3 at the right AMS slots/colours, and slice.
- **Batch export** puts every line into one 3MF, laid out on a 256 mm plate. If they don't fit, use Arrange in Bambu Studio.
- On the Claude-hosted copy of the page, the .3mf comes inside a .zip (that page can't save .3mf directly). The local `keychain-designer.html` saves the .3mf itself.
- Default size: **70 x 15 x 3 mm** overall (length includes the ring tab). Set Length x Height x Thickness in the **Dimensions** boxes at the top of the page, or pick a quick size (50x12x3, 60x15x3, 70x15x3, 80x18x3.5, 100x20x4).
- Stack for 3 mm total: 2.0 mm base, 0.6 mm raised text/border/band, emblem a further 0.4 mm on top of the band. "Total thickness" sets the overall height; the base takes up the rest.
- With a fixed length, "Max text height" is an upper limit: the text shrinks to fit the length (a warning shows if it drops under 3 mm). Tick "Length fits the text automatically" to keep the text size and let the plate grow instead.
- Weight = solid volume x 1.24 g/cm3 (PLA), an upper bound. Price = grams x rate + flat fee (defaults ₹3/g + ₹5).

## Status

- Tested: 2D layout, fonts, presets, auto/fixed length, warnings, SVG export, 3MF package structure (valid zip + XML).
- Not yet verified: 3D preview in a real browser, and that Bambu Studio opens the 3MF with the parts and filaments assigned as intended.

## Ideas for later

1. Embed on the A4 3D Printing website as a custom-keychain page.
2. Carry the filament colours into the 3MF too (so Bambu Studio's filament list matches without manual setup).
3. Two-sided plates and hole position options.
4. Two-line plate layout and Tamil text.
5. Customer order flow (send design + quantity on WhatsApp).
