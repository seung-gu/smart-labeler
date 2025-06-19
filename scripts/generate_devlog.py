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
def write_devlog(entries, out_path=None):
    existing = load_existing_log(out_path)
    today = datetime.now().strftime("%Y-%m-%d")
    new_block = [f"\n----\n## {today}"]

    for entry in entries:
        issue_url = f"https://github.com/{REPO}/issues/{entry['number']}"
        title_line = f"### - [#{entry['number']}]({issue_url}) {entry['title']}"
        block_lines = [title_line]

        # Add body content
        if entry["body"]:
            for body_line in entry["body"].strip().splitlines():
                formatted = f"{body_line}"
                block_lines.append(formatted)

        new_block.extend(block_lines)
        new_block.append("")

    # Remove existing today's section
    if f"## {today}" in existing:
        pattern = rf"----\n## {today}.*?(?=\n----|\Z)"
        existing = re.sub(pattern, "", existing, flags=re.DOTALL).strip()

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(existing.rstrip() + "\n" + "\n".join(new_block) + "\n")

    print("✅ Devlog updated with:", entries)

# Prompt user to manually enter issue numbers
def manual_input_mode():
    print("✍️ Manual mode activated.")
    url = f"https://api.github.com/repos/{REPO}/issues?state=all&per_page=100"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    issues = [issue for issue in res.json() if "pull_request" not in issue]

    print("📝 Available Issues:")
    for issue in issues:
        print(f"  #{issue['number']}: {issue['title']}")

    issue_numbers = input("Enter issue numbers to include (comma-separated): ")
    return [num.strip() for num in issue_numbers.split(",") if num.strip().isdigit()]

if __name__ == "__main__":
    use_manual = os.getenv("CI") != "true" and input("🛠 Manual update? (y/N): ").strip().lower() == "y"

    if use_manual:
        issue_numbers = manual_input_mode()
    else:
        print("📡 Fetching latest commit info...")
        commit_msg = get_latest_commit_message()
        issue_numbers = extract_referenced_issues(commit_msg)

        if not issue_numbers:
            print("⚠️ No issue references found in commit. Skipping devlog update.")
            sys.exit(0)

    if not issue_numbers:
        print("❌ No issues entered. Exiting.")
        exit()

    entries = []
    for num in issue_numbers:
        detail = fetch_issue_detail(num)
        comments = fetch_issue_comments(num)
        detail["comments"] = comments
        entries.append(detail)

    devlog_path = "docs/devlog.md" if os.path.exists("docs") else "../docs/devlog.md"
    write_devlog(entries, out_path=devlog_path)
