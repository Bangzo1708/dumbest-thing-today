#!/usr/bin/env python3
"""The Dumbest Thing Your Agent Did Today.

Writes one line, at most 200 characters, about the dumbest thing my
agent did today, to /output/entry.txt (or ./output/entry.txt when
/output does not exist, for local testing).

The line is a fixed string literal: the entry is the writing itself,
so the program is deterministic by design.
"""

import os
import stat
import sys

# The chosen line (123 characters, one line, no trailing newline needed
# beyond what the gate counts: the file holds exactly this text plus a
# single trailing newline).
ENTRY = (
    "My agent deleted the only working build to 'clean up', "
    "then spent an hour rebuilding it from a screenshot of the error log."
)

MAX_CHARS = 200


def pick_output_dir() -> str:
    """Prefer /output; fall back to ./output for local runs."""
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(os.getcwd(), "output")


def main() -> int:
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    if "\n" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1

    out_dir = pick_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")

    # Read the file back and confirm it holds exactly the line we meant
    # to write: a silent truncation or encoding surprise must fail loudly
    # here, not surface later as a judged entry that is not our line.
    with open(out_path, "r", encoding="utf-8", newline="\n") as fh:
        written = fh.read()
    if written != text + "\n":
        print("written file does not match the entry text", file=sys.stderr)
        return 1

    # make.fun collects outputs as another user: the file must be
    # readable by everyone (mode 0644), never mkstemp-style 0600.
    os.chmod(out_path, 0o644)

    print(f"wrote {len(text)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
