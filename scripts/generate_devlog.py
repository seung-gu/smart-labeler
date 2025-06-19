import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Your GitHub repo (format: username/repo)
REPO = "seung-gu/smart-labeler"

# GitHub token (make sure it's available in env)
GITHUB_TOKEN = os.environ.get("GH_TOKEN")
if not GITHUB_TOKEN:
    raise EnvironmentError("Missing GH_TOKEN in environment variables.")

# Get latest commit message
def get_latest_commit_message():
    result = os.popen("git log -1 --pretty=%B").read().strip()
    return result

# Extract referenced issue numbers like #3 from commit message
def extract_referenced_issues(commit_message):
    return list(set(re.findall(r"#(\d+)", commit_message)))

# Get issue list (open + closed, excluding pull requests)
def fetch_issues(issue_numbers):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    selected_issues = []
    for num in issue_numbers:
        url = f"https://api.github.com/repos/{REPO}/issues/{num}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            issue = response.json()
            if "pull_request" not in issue:
                selected_issues.append(issue)
    return selected_issues

# Group issues by date
def group_by_date(issues):
    grouped = {}
    for issue in issues:
        created_date = issue["created_at"][:10]  # YYYY-MM-DD
        grouped.setdefault(created_date, []).append(f"- #{issue['number']} {issue['title']}")
    return grouped

# Write to markdown
def write_devlog(grouped_issues, out_path="docs/devlog.md"):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# 📘 Development Log (Auto-updated from recent push)\n\n")
        for date in sorted(grouped_issues.keys(), reverse=True):
            f.write(f"## {date}\n")
            f.write("\n".join(grouped_issues[date]) + "\n\n")

if __name__ == "__main__":
    commit_msg = get_latest_commit_message()
    print(f"📃 Latest commit message: {commit_msg}")

    issue_numbers = extract_referenced_issues(commit_msg)
    print(f"🔢 Referenced issues: {issue_numbers}")

    if not issue_numbers:
        print("⚠️ No issue references found in latest commit. Devlog not updated.")
    else:
        issues = fetch_issues(issue_numbers)
        grouped = group_by_date(issues)
        write_devlog(grouped)
        print("✅ Devlog written to docs/devlog.md")