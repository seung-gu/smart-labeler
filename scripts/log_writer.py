"""
Shared logic for writing log files (devlog/doclog).
- Ensures no duplicate issue numbers
- Appends under existing date if already logged
"""

import re
from datetime import datetime
import os

def load_existing_log(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def write_log(entries, out_path, include_body=False):
    """
    entries: List of dicts with keys: number, title, body (optional), url (optional)
    include_body: True for doclog, False for devlog
    """
    existing = load_existing_log(out_path)
    existing_numbers = set(re.findall(r"\[#(\d+)]", existing))
    today = datetime.now().strftime("%Y-%m-%d")

    lines = existing.strip().splitlines()
    output = lines.copy()
    new_blocks = []

    if f"## {today}" not in lines:
        output += ["", "----", f"## {today}"]

    for entry in entries:
        num = str(entry["number"])
        if num in existing_numbers:
            continue  # Skip duplicates

        title_line = f"### - [#{num}]({entry.get('url')}) {entry['title']}".strip()
        block = ["", title_line]

        if include_body and entry.get("body"):
            block += entry["body"].strip().splitlines()

        new_blocks += block + [""]

    if not new_blocks:
        print("⚠️ No new entries to append.")
        return

    output += new_blocks
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output).strip() + "\n")

    print(f"✅ Appended {len(new_blocks)//2} entries to {out_path}")
