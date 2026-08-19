#!/usr/bin/env python3
"""Self-test for scripts/check_docs.py.

Introduces each kind of drift into its own fresh copy of the repository and
requires the checker to fail there. The control copy, with no defects, has to
pass. A checker that silently stopped checking looks exactly as green as a working
one, and this script is the difference between the two.

The copies are made in a new temporary directory and are NOT cleaned up: a step
that breaks things on purpose should not also be deleting directories, or it runs
into the environment guards and quietly drops out of the process.

The Ukrainian strings below are anchors matched against the Ukrainian source
files. They are data, not messages.

Run: python3 scripts/selftest_checks.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IGNORE = shutil.ignore_patterns(".git", "roster.md", "__pycache__", "*.pyc")

# The fake address is assembled from pieces, or this file would be caught by the
# contact check itself.
FAKE_EMAIL = "someone" + chr(64) + "example.com"


def mutate_file(case_dir: Path, rel: str, old: str, new: str, expect: int = 1) -> None:
    """expect=1: the anchor must be unique. expect=0: replace every occurrence."""
    p = case_dir / rel
    text = p.read_text(encoding="utf-8")
    found = text.count(old)
    if found == 0 or (expect == 1 and found != 1):
        raise SystemExit(f"[{rel}] drift anchor missing or not unique: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def drift_missing_section(d: Path) -> None:
    mutate_file(d, "SKILL.md", "### Повідомлення учаснику зустрічі",
                "### Повідомлення учаснику (інша назва)")


def drift_frontmatter(d: Path) -> None:
    mutate_file(d, "SKILL.md", "ретро (АПД),", "")


def drift_translations(d: Path) -> None:
    mutate_file(d, "SKILL.md", ", `Uwaga:`", "")


def drift_missing_file(d: Path) -> None:
    mutate_file(d, "SKILL.md", "`references/roster.md`", "`references/nonexistent.md`",
                expect=0)


def drift_numbering(d: Path) -> None:
    mutate_file(d, "SKILL.md", "\n5. Номери в «По виконавцях»",
                "\n7. Номери в «По виконавцях»")


def drift_readme_parity(d: Path) -> None:
    p = d / "README.en.md"
    p.write_text(p.read_text(encoding="utf-8") + "\n## Extra section\n\ntext\n",
                 encoding="utf-8")


def drift_tracked_roster(d: Path) -> None:
    shutil.copy(d / "references/roster.example.md", d / "references/roster.md")
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "add", "-f", "references/roster.md"], cwd=d, check=True)


def drift_translation(d: Path) -> None:
    mutate_file(d, "references/SKILL.en.md", "## Wording style", "Wording style")


def drift_contact(d: Path) -> None:
    p = d / "README.md"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "## Статус", f"Питання — на {FAKE_EMAIL}\n\n## Статус", 1), encoding="utf-8")


CASES = [
    ("mode without a section", drift_missing_section),
    ("frontmatter missing a mode", drift_frontmatter),
    ("block labels lagging in one language", drift_translations),
    ("reference to a missing file", drift_missing_file),
    ("broken self-check numbering", drift_numbering),
    ("READMEs out of sync", drift_readme_parity),
    ("roster under version control", drift_tracked_roster),
    ("contact in the documentation", drift_contact),
    ("skill translation lagging", drift_translation),
]


def run_checker(case_dir: Path) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "scripts/check_docs.py"],
                       cwd=case_dir, capture_output=True, text=True)
    first = r.stdout.strip().splitlines()
    return r.returncode, (first[0] if first else "")


def main() -> int:
    base = Path(tempfile.mkdtemp(prefix="afu-selftest-"))
    print(f"copies under test: {base}\n")
    failures = 0

    for i, (name, drift) in enumerate(CASES, 1):
        d = base / f"case{i}"
        shutil.copytree(ROOT, d, ignore=IGNORE)
        drift(d)
        code, line = run_checker(d)
        caught = code != 0
        failures += 0 if caught else 1
        print(f"{'caught' if caught else 'MISSED':10} | {name:34} | rc={code} | {line}")

    control = base / "control"
    shutil.copytree(ROOT, control, ignore=IGNORE)
    code, line = run_checker(control)
    if code != 0:
        failures += 1
    print(f"{'ok' if code == 0 else 'FAILED':10} | {'control, no defects':34} | rc={code} | {line}")

    print()
    if failures:
        print(f"{failures} check(s) did not fire: the checker has gone blind")
        return 1
    print(f"all {len(CASES)} kinds of drift caught, control clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
