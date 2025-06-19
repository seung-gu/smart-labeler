"""
Handles manual mode prompting for issue selection.
Used when not in CI environment and user chooses manual update.
"""

import requests
from config import REPO, HEADERS

def manual_input_mode():
    """Prompt the user to select issues by number."""
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
