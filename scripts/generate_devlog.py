import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitHub repository and token
REPO = "seung-gu/smart-labeler"
GITHUB_TOKEN = os.environ.get("GH_TOKEN")
if not GITHUB_TOKEN:
    raise EnvironmentError("Missing GH_TOKEN in environment variables.")

# Set headers for GitHub API requests
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

# Get the latest commit message from the local Git log
def get_latest_commit_message():
    return os.popen("git log -1 --pretty=%B").read().strip()

# Extract issue numbers (e.g. #3) from commit message
def extract_referenced_issues(commit_message):
    return list(set(re.findall(r"#(\d+)", commit_message)))

# Fetch title and body of a specific issue
def fetch_issue_detail(issue_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    issue = res.json()
    return {
        "number": issue["number"],
        "title": issue["title"],
        "body": issue.get("body", "")
    }

# Fetch comments of a specific issue
def fetch_issue_comments(issue_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}/comments"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    comments = res.json()
    return [c["body"] for c in comments]

# Read existing devlog content
def load_existing_log(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Append new entries to devlog.md
def write_devlog(entries, out_path="docs/devlog.md"):
    existing = load_existing_log(out_path)
    today = datetime.now().strftime("%Y-%m-%d")
    new_block = [f"\n## {today}\n"]

    for entry in entries:
        line = f"- #{entry['number']} {entry['title']}"
        extra_lines = []

        # Collect any missing body lines
        if entry["body"]:
            for body_line in entry["body"].strip().splitlines():
                formatted = f"  ➤ {body_line}"
                if formatted not in existing:
                    extra_lines.append(formatted)

        # Collect any missing comment lines
        for comment in entry.get("comments", []):
            for comment_line in comment.strip().splitlines():
                formatted = f"  💬 {comment_line}"
                if formatted not in existing:
                    extra_lines.append(formatted)

        if line in existing:
            # If title exists, only append missing body/comments (with title first)
            if extra_lines:
                new_block.append(line)
                new_block.extend(extra_lines)
                new_block.append("")
            continue

        # New issue entry entirely
        new_block.append(line)
        new_block.extend(extra_lines)
        new_block.append("")

    # Nothing to add
    if len(new_block) <= 2:
        print("⚠️ No new entries to append. Skipping.")
        return

    # Insert into today's section if it already exists
    if today in existing:
        updated = ""
        found = False
        for line in existing.splitlines():
            updated += line + "\n"
            if line.strip() == f"## {today}":
                found = True
                break
        remaining = existing.split(f"## {today}", 1)[1].splitlines()[1:]
        updated += "\n".join(new_block[2:]) + "\n" + "\n".join(remaining)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(updated)
    else:
        # Append entire new section
        with open(out_path, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(new_block) + "\n")

    print("✅ Devlog updated with:", entries)

# Prompt user to manually enter issue numbers
def manual_input_mode():
    print("✍️ Manual mode activated.")
    issue_numbers = input("Enter issue numbers (comma-separated, e.g. 1,2,3): ")
    return [num.strip() for num in issue_numbers.split(",") if num.strip().isdigit()]


if __name__ == "__main__":
    print("📡 Fetching latest commit info...")
    commit_msg = get_latest_commit_message()
    issue_numbers = extract_referenced_issues(commit_msg)

    if not issue_numbers:
        print("⚠️ No issue references found in commit. Entering manual mode...")
        issue_numbers = manual_input_mode()
        if not issue_numbers:
            print("❌ No issues entered. Exiting.")
            exit()

    entries = []
    for num in issue_numbers:
        detail = fetch_issue_detail(num)
        comments = fetch_issue_comments(num)
        detail["comments"] = comments
        entries.append(detail)

    write_devlog(entries)
