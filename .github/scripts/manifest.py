"""projects/ klasöründeki HTML dosyalarını tarar ve projects.json üretir."""
import json
import re
import subprocess
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "projects"
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def last_commit_date(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out
    except Exception:
        return ""


def main() -> None:
    items = []
    for f in sorted(PROJECTS.glob("*.html")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        m = TITLE_RE.search(text)
        items.append({
            "file": f.name,
            "name": f.stem,
            "title": unescape(" ".join(m.group(1).split())) if m else "",
            "updated": last_commit_date(f),
        })
    (ROOT / "projects.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"{len(items)} proje bulundu.")


if __name__ == "__main__":
    main()
