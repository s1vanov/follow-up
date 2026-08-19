#!/usr/bin/env python3
"""Documentation consistency check for the follow-up skill.

Pulls facts out of SKILL.md and fails when the documentation contradicts them.
Run: python3 scripts/check_docs.py

The Ukrainian strings below are search patterns matched against SKILL.md, which
is written in Ukrainian. They are data, not messages: do not translate them.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
READMES = [ROOT / "README.md", ROOT / "README.en.md"]

errors: list[str] = []

# Contacts deliberately kept in the public version. Every entry carries a note on
# who approved it and when. An empty set means the repository holds no contacts.
ALLOWED_CONTACTS: set[str] = set()


def tracked_files() -> list[str]:
    """Files under version control; outside a git repository, every text file."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.split()
    except FileNotFoundError:
        pass
    return [str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
            if p.is_file() and p.suffix in {".md", ".py", ".yml", ".yaml", ".txt"}
            and ".git" not in p.parts]


def fail(msg: str) -> None:
    errors.append(msg)


def section(text: str, title: str) -> str:
    """The body of a section, from its heading to the next one of the same level."""
    level = title.count("#")
    m = re.search(rf"(?m)^{re.escape(title)}\s*$", text)
    if not m:
        fail(f"SKILL.md has no section {title!r}")
        return ""
    rest = text[m.end():]
    nxt = re.search(rf"(?m)^#{{1,{level}}} ", rest)
    return rest[: nxt.start()] if nxt else rest


def main() -> int:
    skill = SKILL.read_text(encoding="utf-8")

    # 1. Every mode named in Step 0 has its own section under output modes.
    step0 = section(skill, "### Крок 0. Запитай формат перед стартом")
    modes = {re.sub(r"\s*\(рекомендовано\)", "", m).strip()
             for m in re.findall(r"\*\*(.+?)\*\*", step0)}
    modes = {m for m in modes if not m.startswith("Загальний follow-up")
             and not m.startswith("одне")}
    out_modes = section(skill, "## Режими виходу")
    declared = set(re.findall(r"(?m)^### (.+?)\s*$", out_modes))
    for m in sorted(modes):
        if m not in declared:
            fail(f"mode {m!r} is named in Step 0 but has no section under output modes")

    # 2. The frontmatter description mentions every mode, by keyword.
    desc = skill.split("---", 2)[1]
    keywords = ["проблеми та рішення", "задачі по виконавцях", "технічні деталі",
                "ретро", "деталі по одній темі", "повідомлення учаснику"]
    for kw in keywords:
        if kw not in desc.lower():
            fail(f"the frontmatter description does not mention the mode {kw!r}")

    # 3. Block labels are translated equally fully into every language.
    tpl = re.search(r"(?s)Шаблон:\s*```(.+?)```", skill)
    if not tpl:
        fail("the template block was not found in SKILL.md")
        expected = 0
    else:
        ua = re.findall(r"(?m)^([А-ЯІЇЄҐ][^:\n]*):", tpl.group(1))
        expected = len(set(ua)) + 1  # plus the conditional note line
    for lang in ("Англійська", "Російська", "Польська"):
        line = re.search(rf"(?m)^- {lang}: (`[^\n]+)$", skill)
        if not line:
            fail(f"no block-label translation line for {lang!r}")
            continue
        n = len(re.findall(r"`[^`]+:`", line.group(1)))
        if n != expected:
            fail(f"{lang}: {n} translated block labels, expected {expected}")

    # 4. Every file named in SKILL.md exists, or has an .example twin.
    for ref in sorted(set(re.findall(r"`(references/[\w./-]+)`", skill))):
        p = ROOT / ref
        example = p.with_name(p.stem + ".example" + p.suffix)
        if not p.exists() and not example.exists():
            fail(f"SKILL.md references {ref}, which is missing from the repository")

    # 5. The self-check list is numbered without gaps.
    chk = re.search(r"(?s)\*\*Самоперевірка перед видачею.*?\n\n(.+?)\n\n[А-ЯA-Z#]", skill)
    if chk:
        nums = [int(x) for x in re.findall(r"(?m)^(\d+)\. ", chk.group(1))]
        if nums != list(range(1, len(nums) + 1)):
            fail(f"the self-check list numbering is broken: {nums}")
    else:
        fail("the self-check list was not found")

    # 6. The two READMEs have the same number of sections.
    counts = {p.name: len(re.findall(r"(?m)^## ", p.read_text(encoding="utf-8")))
              for p in READMES if p.exists()}
    if len(counts) != len(READMES):
        fail(f"one README is missing: found {sorted(counts)}")
    elif len(set(counts.values())) != 1:
        fail(f"the READMEs drifted apart in structure: {counts}")

    # 7. The personal roster did not slip under version control.
    try:
        tracked = subprocess.run(["git", "ls-files", "*roster.md"],
                                 cwd=ROOT, capture_output=True, text=True).stdout.split()
        leaked = [f for f in tracked if not f.endswith(".example.md")]
        for f in leaked:
            fail(f"{f} is tracked by git and holds personal data")
    except FileNotFoundError:
        pass

    # 8. No contact channels in tracked files. The pattern is assembled from
    # pieces on purpose: written out whole, this file would match itself.
    at = chr(64)
    tel = "t" + "el" + chr(58)          # kept split for the same reason
    phone = r"\+" + "38" + "0"
    contact = re.compile(
        r"[A-Za-z0-9._%+-]+" + at + r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        + r"|t\.me/|wa\.me/|linkedin\.com/in/|" + tel + "|" + phone,
        re.I,
    )
    for rel in tracked_files():
        path = ROOT / rel
        if not path.exists():
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for hit in contact.findall(line):
                if hit in ALLOWED_CONTACTS:
                    continue
                fail(f"{rel}:{i} contains the contact {hit!r}; see ALLOWED_CONTACTS")

    # 9. The translation of the skill keeps up with the original structurally.
    en = ROOT / "references" / "SKILL.en.md"
    if not en.exists():
        fail("references/SKILL.en.md is missing: the English translation")
    else:
        ua_h = re.findall(r"(?m)^(#{2,3}) ", skill)
        en_h = re.findall(r"(?m)^(#{2,3}) ", en.read_text(encoding="utf-8"))
        if len(ua_h) != len(en_h):
            fail(f"SKILL.md has {len(ua_h)} headings, the translation has "
                 f"{len(en_h)}: a section was added to one file and not the other")
        elif ua_h != en_h:
            fail("heading levels in SKILL.md and the translation diverged")

    for e in errors:
        print(f"FAIL: {e}")
    if errors:
        print(f"\n{len(errors)} problem(s) in the documentation")
        return 1
    print("OK: documentation is consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
