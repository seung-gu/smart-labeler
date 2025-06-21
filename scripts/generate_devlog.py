from github_api import get_latest_commit_message, extract_referenced_issues, fetch_issue_detail
from log_writer import write_log


if __name__ == "__main__":
    commit_msg = get_latest_commit_message()
    if "--ignore-devlog" in commit_msg or "[MR]" in commit_msg:
        print("🚫 Skipping devlog update due to flag.")
        exit()

    issue_numbers = extract_referenced_issues(commit_msg)
    entries = []
    for num in issue_numbers:
        data = fetch_issue_detail(num)
        data["url"] = f"https://github.com/seung-gu/smart-labeler/issues/{num}"
        entries.append(data)

    write_log(entries, out_path="docs/devlog.md", include_body=False)
