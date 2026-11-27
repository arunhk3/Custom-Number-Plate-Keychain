"""Build keychain-designer.html from src/template.html + src/fonts.json (+ Bambu Studio template).

If bambu-template.3mf (a project saved from Bambu Studio) is in the repo root, its
Metadata/project_settings.config is extracted to src/bambu_project_settings.json first.
That file is embedded so exported 3MFs open as full Bambu Studio projects with your
printer, process and filament settings (no "old Bambu Studio" warning, per-part settings kept).
"""
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
template_3mf = root / "bambu-template.3mf"
settings_json = root / "src" / "bambu_project_settings.json"

# Filament preset options, from Bambu Studio src/libslic3r/Preset.cpp (s_Preset_filament_options).
# Used to tell per-filament lists apart from per-extruder-variant lists of the same length.
FILAMENT_OPTIONS = set(json.loads((Path(__file__).parent / "bambu_filament_options.json").read_text(encoding="utf-8")))

if template_3mf.exists():
    with zipfile.ZipFile(template_3mf) as z:
        cfg = json.loads(z.read("Metadata/project_settings.config"))
    n_fil = len(cfg["filament_colour"])
    n_var = len(cfg["filament_self_index"])
    per_fil, per_fil_var = [], []
    for k, v in cfg.items():
        if not isinstance(v, list):
            continue
        if k in FILAMENT_OPTIONS or k.startswith("filament_"):
            if len(v) == n_fil:
                per_fil.append(k)
            elif len(v) == n_var and k in FILAMENT_OPTIONS:
                per_fil_var.append(k)
    settings_json.write_text(json.dumps({
        "source": template_3mf.name,
        "config": cfg,
        "perFilament": sorted(per_fil),
        "perFilamentVariant": sorted(per_fil_var),
    }, indent=1), encoding="utf-8")
    print(f"Extracted {template_3mf.name}: Bambu Studio {cfg.get('version')}, {cfg.get('printer_settings_id')}, "
          f"{cfg.get('print_settings_id')}, {n_fil} filaments")

bambu = settings_json.read_text(encoding="utf-8") if settings_json.exists() else "null"
template = (root / "src" / "template.html").read_text(encoding="utf-8")
fonts = (root / "src" / "fonts.json").read_text(encoding="utf-8")
out = root / "keychain-designer.html"
out.write_text(template.replace("__FONTS__", fonts).replace("__BAMBU__", bambu), encoding="utf-8")
print(f"Built {out} ({out.stat().st_size // 1024} KB)")
