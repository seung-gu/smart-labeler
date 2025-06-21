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
    Appends new issue entries to today's section in devlog.
    - Does not duplicate issue numbers
    - Avoids repeating today's date if already present
    """
    existing = load_existing_log(out_path)
    existing_issue_numbers = set(re.findall(r"\[#(\d+)]", existing))
    today = datetime.now().strftime("%Y-%m-%d")

    lines = existing.strip().splitlines()
    output = lines.copy()
    new_entries = []

    # Check if today's header already exists
    today_exists = any(line.strip() == f"## {today}" for line in lines)

    if not today_exists:
        output += ["", "----", f"## {today}"]

    for entry in entries:
        if str(entry["number"]) in existing_issue_numbers or "[MR]" in entry["title"]:
            continue  # Skip already logged issues or PRs marked [MR]

        issue_url = f"https://github.com/{REPO}/issues/{entry['number']}"
        title_line = f"### - [#{entry['number']}]({issue_url}) {entry['title']}"
        block = ["", title_line]

        if entry["body"]:
            block += entry["body"].strip().splitlines()

        block.append("")
        new_entries += block

    if not new_entries:
        print("⚠️ No new entries to append. Skipping.")
        return

    output += new_entries

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output).strip() + "\n")

    print(f"✅ Appended {len(new_entries)//2} issue(s) to devlog.")

