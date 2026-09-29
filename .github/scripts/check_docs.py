"""Validate the documentation delivered by this disposable pilot."""

from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    documents = sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts and ".forge" not in path.parts)
    errors = []
    if not (ROOT / "README.md").is_file():
        errors.append("README.md is missing")
    for document in documents:
        text = document.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"{document.relative_to(ROOT)} is empty")
        if not re.search(r"^#\s+\S", text, re.MULTILINE):
            errors.append(f"{document.relative_to(ROOT)} needs a top-level heading")
        for raw in LINK.findall(text):
            target = raw.split()[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            candidate = (document.parent / unquote(parsed.path)).resolve()
            if not candidate.is_relative_to(ROOT) or not candidate.exists():
                errors.append(f"{document.relative_to(ROOT)} has a missing relative link: {target}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(documents)} Markdown document(s) and relative links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
