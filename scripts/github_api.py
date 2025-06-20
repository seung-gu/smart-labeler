"""
GitHub API utility functions.
Handles issue fetching, comment retrieval, and commit parsing.
Relies on authentication headers defined in config.py.
"""

import requests
import os
import re
from config import REPO, HEADERS

def get_latest_commit_message():
    """Returns the latest commit message from local Git log."""
    return os.popen("git log -1 --pretty=%B").read().strip()

def extract_referenced_issues(commit_message):
    """Extracts all issue numbers in the format #123 from a commit message."""
    return list(set(re.findall(r"#(\d+)", commit_message)))

def fetch_issue_detail(issue_number):
    """Fetches title and body of the specified issue."""
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    issue = res.json()
    return {
        "number": issue["number"],
        "title": issue["title"],
        "body": issue.get("body", "")
    }

def fetch_issue_comments(issue_number):
    """Fetches all comments associated with the specified issue."""
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}/comments"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return [c["body"] for c in res.json()]
