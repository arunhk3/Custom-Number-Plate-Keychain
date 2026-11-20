"""Build keychain-designer.html from src/template.html + src/fonts.json."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
template = (root / "src" / "template.html").read_text(encoding="utf-8")
fonts = (root / "src" / "fonts.json").read_text(encoding="utf-8")
out = root / "keychain-designer.html"
out.write_text(template.replace("__FONTS__", fonts), encoding="utf-8")
print(f"Built {out} ({out.stat().st_size // 1024} KB)")
