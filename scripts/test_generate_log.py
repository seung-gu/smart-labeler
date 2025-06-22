import tempfile
import os
from datetime import datetime

from scripts.generate_log import write_doclog
from scripts.generate_log import write_devlog

def test_write_devlog():
    issue = {
        "number": 1,
        "title": "Test Issue",
        "commit_msg": "Fix bug #1",
        "commit_sha": "abcdef1234567890"
    }
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as tf:
        devlog_path = tf.name

    # First write
    write_devlog(issue, devlog_path)
    with open(devlog_path, encoding="utf-8") as f:
        content1 = f.read()
    print("First devlog write:\n", content1)
    assert "### - [#1]" in content1
    assert "Fix bug #1" in content1

    # Duplicate write (should not duplicate entry for same date)
    write_devlog(issue, devlog_path)
    with open(devlog_path, encoding="utf-8") as f:
        content2 = f.read()
    print("Second devlog write (should be unchanged):\n", content2)
    assert content1 == content2

    os.remove(devlog_path)

def test_write_doclog():
    issue = {
        "number": 2,
        "title": "Doc Issue",
        "body": "This is a doc issue body."
    }
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as tf:
        doclog_path = tf.name

    # First write
    write_doclog(issue, doclog_path)
    with open(doclog_path, encoding="utf-8") as f:
        content1 = f.read()
    print("First doclog write:\n", content1)
    assert "### - [#2]" in content1
    assert "This is a doc issue body." in content1

    # Overwrite with updated body
    issue["body"] = "Updated body."
    write_doclog(issue, doclog_path)
    with open(doclog_path, encoding="utf-8") as f:
        content2 = f.read()
    print("Second doclog write (should be updated):\n", content2)
    assert "Updated body." in content2
    assert "This is a doc issue body." not in content2

    os.remove(doclog_path)

