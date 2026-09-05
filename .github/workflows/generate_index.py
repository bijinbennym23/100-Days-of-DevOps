import json
import re
from pathlib import Path

DAYS_DIR = Path("days")
MANIFEST = Path("days.json")
README = Path("README.md")

def collect_days():
    entries = []
    for f in sorted(DAYS_DIR.glob("day-*.md")):
        match = re.match(r"day-(\d+)-(.+)\.md", f.name)
        if not match:
            continue
        day_num, slug = match.groups()
        title = f.read_text().splitlines()[0].lstrip("# ").strip()
        entries.append({
            "day": int(day_num),
            "title": title,
            "file": f"days/{f.name}"
        })
    return sorted(entries, key=lambda e: e["day"])

def write_manifest(entries):
    MANIFEST.write_text(json.dumps(entries, indent=2) + "\n")

def write_readme(entries):
    lines = ["# 100 Days of DevOps\n", f"Progress: {len(entries)}/100\n", "## Index\n"]
    for e in entries:
        lines.append(f"- [Day {e['day']}: {e['title']}]({e['file']})")
    README.write_text("\n".join(lines) + "\n")

if __name__ == "__main__":
    entries = collect_days()
    write_manifest(entries)
    write_readme(entries)