import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils.path_utils import get_target_directory

load_dotenv()

REPO = "seung-gu/smart-labeler"
GITHUB_TOKEN = os.getenv("GH_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_latest_commit_message():
    return os.popen("git log -1 --pretty=%B").read().strip()

def get_latest_commit_sha():
    return os.popen("git rev-parse HEAD").read().strip()

def extract_issue_number_from_commit(message):
    match = re.search(r"#(\d+)", message)
    return match.group(1) if match else None

def is_merge_commit(message):
    return re.match(r"Merge pull request #\d+ from .+/\d+-", message) is not None

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

def load_log(path):
    return open(path, "r", encoding="utf-8").read() if os.path.exists(path) else ""

def write_devlog(issue, devlog_path):
    devlog_existing = load_log(devlog_path)
    today = datetime.now().strftime("%Y-%m-%d")
    date_header = f"## {today}"
    # Only add if not already present for today/title
    today_section = devlog_existing.split(date_header)[-1] if date_header in devlog_existing else ""
    issue_line = f"### - [#{issue['number']}](https://github.com/{REPO}/issues/{issue['number']}) {issue['title']}"
    if issue_line not in today_section:
        if date_header not in devlog_existing:
            devlog_existing += f"\n----\n{date_header}\n"
        devlog_block = [issue_line]
        short_sha = issue["commit_sha"][:7]
        sha_url = f"https://github.com/{REPO}/commit/{issue['commit_sha']}"
        commit_line = f"- 🔧 Commit: {issue['commit_msg']}  \n  [`{short_sha}`]({sha_url})"
        devlog_block.append(commit_line)
        devlog_block.append("")
        with open(devlog_path, "w", encoding="utf-8") as f:
            f.write(devlog_existing.rstrip() + "\n" + "\n".join(devlog_block))
        print(f"✅ Devlog updated: #{issue['number']}")

def write_doclog(issue, doclog_path):
    doclog_existing = load_log(doclog_path)
    today = datetime.now().strftime("%Y-%m-%d")
    if f"## {today}" not in doclog_existing:
        doclog_existing += f"\n----\n## {today}\n"
    # Remove previous block for this issue
    pattern = rf"### - \[#{issue['number']}\]\(.*?\).*?(?=\n### - \[#\d+\]|$)"
    doclog_existing = re.sub(pattern, "", doclog_existing, flags=re.DOTALL).strip()
    doclog_block = [f"### - [#{issue['number']}](https://github.com/{REPO}/issues/{issue['number']}) {issue['title']}"]
    if issue.get("body"):
        doclog_block += issue["body"].strip().splitlines()
    doclog_block.append("")
    with open(doclog_path, "w", encoding="utf-8") as f:
        f.write(doclog_existing.rstrip() + "\n" + "\n".join(doclog_block) + "\n")
    print(f"📚 Doclog updated: #{issue['number']}")

if __name__ == "__main__":
    commit_msg = get_latest_commit_message()
    commit_sha = get_latest_commit_sha()
    root = get_target_directory("smart-labeler")
    devlog_path = root / "docs" / "devlog.md"
    doclog_path = root / "docs" / "doclog.md"

    # PR Merge: update doclog only
    if is_merge_commit(commit_msg):
        issue_num = extract_issue_number_from_commit(commit_msg)
        if issue_num:
            issue = fetch_issue_detail(issue_num)
            write_doclog(issue, doclog_path)
    # Normal commit: update devlog only
    elif "#"+str(extract_issue_number_from_commit(commit_msg)) in commit_msg and "--ignore-devlog" not in commit_msg:
        issue_num = extract_issue_number_from_commit(commit_msg)
        if issue_num:
            issue = fetch_issue_detail(issue_num)
            issue.update({"commit_msg": commit_msg, "commit_sha": commit_sha})
            write_devlog(issue, devlog_path)