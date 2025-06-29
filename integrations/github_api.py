"""
GitHub API utility functions.
Handles issue fetching, comment retrieval, and commit parsing.
Relies on authentication headers defined in config.py.
"""
import re
import requests
import os
from config.github_config import REPO, HEADERS


def get_unpushed_commits():
    """
    Returns a list of (sha, message) tuples for all unpushed commits on the current branch.
    ordered from oldest to newest.
    """
    branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    output = os.popen(f"git log origin/{branch}..HEAD --pretty=%H%x00%B%x00").read().strip()
    entries = output.split('\x00')
    commits = []
    for i in range(0, len(entries) - 1, 2):
        sha = entries[i].strip()
        msg = entries[i + 1].strip()
        if sha:
            commits.append((sha, msg))
    return list(reversed(commits))

def get_latest_commit_message():
    """Returns the latest commit message from local Git log."""
    return os.popen("git log -1 --pretty=%B").read().strip()

def get_latest_commit_sha():
    return os.popen("git rev-parse HEAD").read().strip()

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

def extract_issue_number_from_commit(message):
    # For merge commits: extract from branch name
    merge_match = re.match(r"Merge pull request #\d+ from .+/(\d+)-", message)
    if merge_match:
        return merge_match.group(1)
    # For normal commits: extract from #<number>
    match = re.search(r"#(\d+)", message)
    return match.group(1) if match else None

def extract_issue_number_from_branch():
    """Extracts the issue number from the current branch name."""
    branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    match = re.match(r"(\d+)[-_]", branch)
    return int(match.group(1)) if match else None

def is_merge_commit(message):
    return re.match(r"Merge pull request #\d+ from .+/\d+-", message) is not None
