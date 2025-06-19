"""
Main entry point for generating the devlog.
Supports both automatic and manual issue selection modes.
Automatically detects CI environments to skip prompts.
"""

from github_api import (
    get_latest_commit_message,
    extract_referenced_issues,
    fetch_issue_detail,
    fetch_issue_comments
)
from devlog_writer import write_devlog
from user_prompt import manual_input_mode
import os

if __name__ == "__main__":
    # Use manual input only if not in CI and user chooses to
    use_manual = os.getenv("CI") != "true" and input("🛠 Manual update? (y/N): ").strip().lower() == "y"

    if use_manual:
        issue_numbers = manual_input_mode()
    else:
        print("📡 Fetching latest commit info...")
        commit_msg = get_latest_commit_message()
        issue_numbers = extract_referenced_issues(commit_msg)

        if not issue_numbers:
            print("⚠️ No issue references found in commit. Skipping devlog update.")
            exit(0)

    if not issue_numbers:
        print("❌ No issues entered. Exiting.")
        exit()

    # Build entry list from issue data and comments
    entries = []
    for num in issue_numbers:
        detail = fetch_issue_detail(num)
        detail["comments"] = fetch_issue_comments(num)
        entries.append(detail)

    # Output devlog path detection
    devlog_path = "docs/devlog.md" if os.path.exists("docs") else "../docs/devlog.md"
    write_devlog(entries, out_path=devlog_path)
