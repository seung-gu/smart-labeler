import os
import re
from datetime import datetime

from scripts.config import REPO
from scripts.github_api import get_latest_commit_message, is_merge_commit, \
    extract_issue_number_from_commit, fetch_issue_detail, get_unpushed_commits, extract_issue_number_from_branch
from utils.path_utils import get_target_directory


def load_log(path):
    return open(path, "r", encoding="utf-8").read() if os.path.exists(path) else ""

def write_devlog(issue, devlog_path):
    devlog_existing = load_log(devlog_path)

    today = datetime.now().strftime("%Y-%m-%d")
    date_header = f"## {today}"
    issue_line = f"### - [#{issue['number']}](https://github.com/{REPO}/issues/{issue['number']}) {issue['title']}"
    short_sha = issue["commit_sha"][:7]
    sha_url = f"https://github.com/{REPO}/commit/{issue['commit_sha']}"
    commit_line = f"- 🔧 Commit: {issue['commit_msg']}  \n  [`{short_sha}`]({sha_url})"

    # Ensure today's section exists
    if date_header not in devlog_existing:
        devlog_existing += f"\n----\n{date_header}\n"

    # Split into lines for easier manipulation
    lines = devlog_existing.splitlines()
    # Find today's section start
    try:
        date_idx = lines.index(date_header)
    except ValueError:
        date_idx = len(lines)
        lines.append(date_header)

    # Find issue block under today's section
    try:
        issue_idx = lines.index(issue_line, date_idx)
    except ValueError:
        # Insert issue line after date header
        issue_idx = date_idx + 1
        lines.insert(issue_idx, issue_line)

    # Find where to insert the commit line (after issue line, before next issue or end)
    insert_idx = issue_idx + 1
    while insert_idx < len(lines) and not lines[insert_idx].startswith("### - "):
        if short_sha in lines[insert_idx]:
            # Already logged
            return
        insert_idx += 1

    # Insert commit line
    lines.insert(insert_idx, commit_line)
    # Write back
    with open(devlog_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    print(f"✅ Devlog updated: #{issue['number']} {short_sha}")

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
    root = get_target_directory("smart-labeler")
    devlog_path = root / "docs" / "devlog.md"
    doclog_path = root / "docs" / "doclog.md"

    issue_num = extract_issue_number_from_branch()

    # PR Merge: update doclog only
    commit_msg = get_latest_commit_message()
    if is_merge_commit(commit_msg):
        issue_num = extract_issue_number_from_commit(commit_msg)
        if issue_num:
            issue = fetch_issue_detail(issue_num)
            write_doclog(issue, doclog_path)

    # Normal commit: update devlog only
    elif issue_num is not None:
        for sha, msg in get_unpushed_commits():
            if f"#{issue_num}" in msg and "--ignore-devlog" not in msg:
                issue = fetch_issue_detail(issue_num)
                issue.update({"commit_msg": msg, "commit_sha": sha})
                write_devlog(issue, devlog_path)