"""
GitHub API utility functions.
Handles issue fetching, comment retrieval, and commit parsing.
Relies on authentication headers defined in config.py.
"""
import re
import requests
import os
from config import REPO, HEADERS


def get_latest_commit_message():
    """Returns the latest commit message from local Git log."""
    return os.popen("git log -1 --pretty=%B").read().strip()

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

def get_latest_commit_sha():
    return os.popen("git rev-parse HEAD").read().strip()

def extract_issue_number_from_commit(message):
    # For merge commits: extract from branch name
    merge_match = re.match(r"Merge pull request #\d+ from .+/(\d+)-", message)
    if merge_match:
        return merge_match.group(1)
    # For normal commits: extract from #<number>
    match = re.search(r"#(\d+)", message)
    return match.group(1) if match else None

def is_merge_commit(message):
    return re.match(r"Merge pull request #\d+ from .+/\d+-", message) is not None
