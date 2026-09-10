#!/usr/bin/env python3
"""
Regenerates the README.md index table and days.json manifest
by scanning all day-*.md files in the repo root.

Convention each day file must follow:

    # Day 5: SELinux Installation and Configuration

    **Category:** Linux / Security

    ... rest of content ...

Run manually with:  python scripts/update_index.py
Run automatically via .github/workflows/update-index.yml on every push
that touches a day-*.md file.
"""

import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DAY_FILE_RE = re.compile(r"^day-(\d+)-(.+)\.md$")
TITLE_RE = re.compile(r"^#\s*Day\s*\d+:\s*(.+)$", re.IGNORECASE)
CATEGORY_RE = re.compile(r"^\*\*Category:\*\*\s*(.+)$")

START_MARKER = "<!-- INDEX_START -->"
END_MARKER = "<!-- INDEX_END -->"


def get_added_date(filepath):
    """Date the file was first committed (git history), YYYY-MM-DD."""
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%as", "--", filepath],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        dates = out.splitlines()
        return dates[-1] if dates else ""
    except Exception:
        return ""


def parse_day_file(filename):
    path = os.path.join(ROOT, filename)
    m = DAY_FILE_RE.match(filename)
    day_num = int(m.group(1))
    title, category = "", "Uncategorized"

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not title:
                tm = TITLE_RE.match(line)
                if tm:
                    title = tm.group(1).strip()
                    continue
            cm = CATEGORY_RE.match(line)
            if cm:
                category = cm.group(1).strip()
                break

    return {
        "day": day_num,
        "title": title or filename,
        "category": category,
        "date": get_added_date(path),
        "path": filename,
    }


def main():
    entries = [
        parse_day_file(fname)
        for fname in os.listdir(ROOT)
        if DAY_FILE_RE.match(fname)
    ]
    entries.sort(key=lambda e: e["day"])

    # --- days.json ---
    with open(os.path.join(ROOT, "days.json"), "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
        f.write("\n")

    # --- README table ---
    rows = [
        "| Day | Topic | Category | Date | Link |",
        "|-----|-------|----------|------|------|",
    ]
    for e in entries:
        rows.append(
            f"| {e['day']:02d} | {e['title']} | {e['category']} | {e['date']} | "
            f"[{e['path']}](./{e['path']}) |"
        )
    table = "\n".join(rows)

    readme_path = os.path.join(ROOT, "README.md")
    with open(readme_path, encoding="utf-8") as f:
        content = f.read()

    replacement = f"{START_MARKER}\n{table}\n{END_MARKER}"
    pattern = re.compile(re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(replacement, content)
    else:
        content += f"\n\n{replacement}\n"

    # keep the day-count badge in sync
    badge_re = re.compile(r"(!\[Days\]\(https://img\.shields\.io/badge/days-)(\d+)(%2F\d+-blue\))")
    content = badge_re.sub(lambda m: f"{m.group(1)}{len(entries):02d}{m.group(3)}", content)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated README.md and days.json with {len(entries)} day(s).")


if __name__ == "__main__":
    main()
