"""
Handles reading, formatting, and writing the devlog markdown file.
Ensures no duplicate date blocks and supports full overwrite of daily blocks.
"""

import os
import re
from datetime import datetime
from config import REPO

def load_existing_log(path):
    """Reads the existing devlog content if available."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def write_devlog(entries, out_path=None):
    """
    Writes or updates the devlog with new issue entries.
    Fully replaces today's section if it already exists.
    """
    existing = load_existing_log(out_path)
    today = datetime.now().strftime("%Y-%m-%d")
    new_block = [f"\n----\n## {today}"]

    for entry in entries:
        issue_url = f"https://github.com/{REPO}/issues/{entry['number']}"
        title_line = f"### - [#{entry['number']}]({issue_url}) {entry['title']}"
        block_lines = [title_line]

        if entry["body"]:
            block_lines += [f"{line}" for line in entry["body"].strip().splitlines()]

        new_block += block_lines + [""]

    # Remove duplicate today's block if it already exists
    if f"## {today}" in existing:
        pattern = rf"----\n## {today}.*?(?=\n----|\Z)"
        existing = re.sub(pattern, "", existing, flags=re.DOTALL).strip()

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(existing.rstrip() + "\n" + "\n".join(new_block) + "\n")

    print("✅ Devlog updated with:", entries)
