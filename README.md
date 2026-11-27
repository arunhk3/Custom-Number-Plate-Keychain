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
| `tools/build.py` | Puts `fonts.json` and the Bambu project settings into `template.html` to produce `keychain-designer.html`. |
| `bambu-template.3mf` | A project saved from your own Bambu Studio (printer, process, AMS filaments, ironing). Only its settings are used. Kept out of git. |
| `src/bambu_project_settings.json` | Settings extracted from `bambu-template.3mf` by `build.py`; embedded in every exported 3MF. |
| `tools/bambu_filament_options.json` | Bambu Studio's filament option names, used to resize the filament list. |

## Rebuild after editing

```
python tools/build.py
```

To change printer, process, filament or ironing settings: set them up in Bambu Studio, save the project over `bambu-template.3mf`, and run `python tools/build.py` again.

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
- The 3MF is a full Bambu Studio project built from `bambu-template.3mf`: it opens with your printer, process and filament profiles, and the filament colours already set (no "old Bambu Studio" warning). Extra colours reuse the template's filament profiles in turn.
- Ironing: Top surfaces, 50 mm/s, 30% flow, except the **Band emblem** part, which has ironing off (its fine detail smears).
- Each keychain object uses the Arachne wall generator, so thin features (fine text) are printed rather than dropped.
- The band wheel is a simplified Ashoka Chakra with 8 spokes, each 0.85 mm wide (about two nozzle lines). The real emblem's 24 spokes are too fine to slice at keychain size.
- In Bambu Studio: open the .3mf, check the filaments map to the right AMS slots, and slice.
- **Batch export** puts every line into one 3MF, laid out on a 256 mm plate. If they don't fit, use Arrange in Bambu Studio.
- On the Claude-hosted copy of the page, the .3mf comes inside a .zip (that page can't save .3mf directly). The local `keychain-designer.html` saves the .3mf itself.
- Default size: **70 x 18 x 3 mm** overall (length includes the ring tab). Set Length x Height x Thickness in the **Dimensions** boxes at the top of the page, or pick a quick size (50x12x3, 60x15x3, 70x18x3, 80x18x3.5, 100x20x4).
- Stack for 3 mm total: 2.0 mm base, 0.6 mm raised text/border/band, emblem a further 0.4 mm on top of the band. "Total thickness" sets the overall height; the base takes up the rest.
- With a fixed length, "Max text height" is an upper limit: the text shrinks to fit the length (a warning shows if it drops under 3 mm). Tick "Length fits the text automatically" to keep the text size and let the plate grow instead.
- Weight = solid volume x 1.24 g/cm3 (PLA), an upper bound. Price = grams x rate + flat fee (defaults ₹3/g + ₹5).

## Status

- Tested: 2D layout, fonts, presets, auto/fixed length, warnings, SVG export, 3MF package structure (valid zip + XML).
- Tested: exported 3MF in a real browser carries the template's project settings, resized for 1-5 colours, with ironing off on the emblem part.
- Not yet verified: opening that 3MF in Bambu Studio itself.

## Ideas for later

1. Embed on the A4 3D Printing website as a custom-keychain page.
2. Two-sided plates and hole position options.
3. Two-line plate layout and Tamil text.
5. Customer order flow (send design + quantity on WhatsApp).
