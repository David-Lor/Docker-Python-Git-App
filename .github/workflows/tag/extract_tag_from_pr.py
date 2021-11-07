"""EXTRACT TAG FROM PR Script
This script extracts the tag version from a Pull Request body,
given the JSON Output returned by the Action https://github.com/marketplace/actions/get-current-pull-request.
The JSON Output must be given through an environment variable named "PR_JSON_DATA".
The Pull Request body must contain a line that starts with "Tag" or "Tags", followed by a version in style x.x.x,
being x a number (case ignored, words after version ignored)
The tag is written to a file. If no tag can be exported from the Pull Request body, the file is written blank.
"""

import os
import re
import json
from typing import Optional

PR_JSON_DATA_ENV = "PR_JSON_DATA"
VERSION_FILE = "version.txt"


def _get_pr_data() -> dict:
    """Acquire the PR data from environment variable"""
    data_raw = os.getenv(PR_JSON_DATA_ENV)
    if not data_raw:
        print("No PR JSON data given!")
        exit(1)

    return json.loads(data_raw)


def _is_valid_version(version: str) -> bool:
    """Returns True if the given string matches a version like "x.x.x" (being x numbers)"""
    return bool(re.match(r"^(\d+\.)?(\d+\.)?(\*|\d+)$", version))


def _extract_tag(pr_data: dict) -> Optional[str]:
    pr_body: str = pr_data["body"]

    for line in pr_body.splitlines():
        line = line.strip().lower()
        if line.startswith("tag ") or line.startswith("tags "):
            for chunk in line.split():
                chunk = chunk.strip()
                if _is_valid_version(chunk):
                    print(f"Found tag \"{chunk}\" in PR body!")
                    return chunk

    print("No tag found in PR body!")


def _save_tag(tag: Optional[str]):
    if not tag:
        tag = ""
    with open(VERSION_FILE, "w") as file:
        file.write(tag)
        print(f"Tag \"{tag}\" saved to file \"{VERSION_FILE}\"")


def main():
    pr_data = _get_pr_data()
    tag = _extract_tag(pr_data)
    _save_tag(tag)


if __name__ == "__main__":
    main()
