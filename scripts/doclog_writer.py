from scripts.devlog_writer_dep import load_existing_log


def update_doclog_from_merge_request(pr, out_path=None):
    """
    Updates the doclog with content from a single pull request (treated as a merge request).
    Only applies if the PR title contains [MR].
    Replaces the block corresponding to that PR number if it exists.
    """
    existing = load_existing_log(out_path)
    pr_number = str(pr["number"])

    if "[MR]" not in pr["title"]:
        return

    pr_url = pr["html_url"]
    header = f"### - [#{pr_number}]({pr_url}) {pr['title']}"
    lines = ["----", header]

    if pr.get("body"):
        lines += pr["body"].strip().splitlines()

    for comment in pr.get("comments", []):
        lines += comment.strip().splitlines()

    block_text = "\n" + "\n".join(lines) + "\n"

    pattern = rf"----\n### - \[#{pr_number}\].*?(?=\n----|\Z)"
    existing = re.sub(pattern, "", existing, flags=re.DOTALL).strip()
    existing += block_text

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(existing + "\n")

    print(f"📚 Doclog updated from [MR] pull request #{pr_number}")