"""
Centralized configuration loader for environment variables and GitHub headers.
All tokens and repo-level constants should be defined here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

REPO = "seung-gu/smart-labeler"
GITHUB_TOKEN = os.getenv("GH_TOKEN")

if not GITHUB_TOKEN:
    raise EnvironmentError("Missing GH_TOKEN in environment variables.")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}
