"""Write one funny single-line developer excuse to entry.txt.

The excuse is a single line, at most 200 characters, written to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when the variable
is unset). The file is written with no trailing newline, then read back
and validated against the competition gate before the program exits.
"""

import os
import sys

EXCUSE = (
    "It passed all the tests \u2014 which is how we know the tests were "
    "written by the same person who wrote the bug."
)


def validate(text: str) -> str | None:
    """Return an error message when *text* fails the gate, else None."""
    if not 1 <= len(text) <= 200:
        return f"entry is {len(text)} characters, must be 1-200"
    if not text.strip():
        return "entry is only whitespace"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    return None


def main() -> int:
    error = validate(EXCUSE)
    if error is not None:
        print(f"error: {error}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = EXCUSE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)

    with open(path, "rb") as handle:
        read_back = handle.read()
    text = read_back.decode("utf-8")

    if read_back != data:
        print("error: entry.txt did not round-trip byte-identically", file=sys.stderr)
        return 1
    error = validate(text)
    if error is not None:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Wrote {path}: {len(text)} characters")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
