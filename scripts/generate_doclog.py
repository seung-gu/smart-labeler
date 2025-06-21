from github_api import fetch_mr_prs, fetch_issue_detail, fetch_issue_comments
from log_writer import write_log
import re

if __name__ == "__main__":
    prs = fetch_mr_prs()  # [MR] PRs only
    entries = []

    for pr in prs:
        match = re.search(r"#(\d+)", pr["title"])
        if not match:
            continue
        issue_num = match.group(1)
        issue = fetch_issue_detail(issue_num)
        issue["comments"] = fetch_issue_comments(issue_num)
        issue["url"] = f"https://github.com/seung-gu/smart-labeler/issues/{issue_num}"
        issue["body"] += "\n" + "\n".join(issue["comments"])
        entries.append(issue)

    write_log(entries, out_path="docs/doclog.md", include_body=True)
