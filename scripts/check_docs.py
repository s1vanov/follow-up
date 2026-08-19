#!/usr/bin/env python3
"""Перевірка узгодженості документації actionable-follow-up.

Витягає факти з SKILL.md і падає, коли документація їм суперечить.
Запуск: python3 scripts/check_docs.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
READMES = [ROOT / "README.md", ROOT / "README.en.md"]

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def section(text: str, title: str) -> str:
    """Тіло розділу від його заголовка до наступного того ж рівня."""
    level = title.count("#")
    m = re.search(rf"(?m)^{re.escape(title)}\s*$", text)
    if not m:
        fail(f"немає розділу «{title}» у SKILL.md")
        return ""
    rest = text[m.end():]
    nxt = re.search(rf"(?m)^#{{1,{level}}} ", rest)
    return rest[: nxt.start()] if nxt else rest


def main() -> int:
    skill = SKILL.read_text(encoding="utf-8")

    # 1. Кожен режим із Кроку 0 має власний розділ у «Режими виходу».
    step0 = section(skill, "### Крок 0. Запитай формат перед стартом")
    modes = {re.sub(r"\s*\(рекомендовано\)", "", m).strip()
             for m in re.findall(r"\*\*(.+?)\*\*", step0)}
    modes = {m for m in modes if not m.startswith("Загальний follow-up")
             and not m.startswith("одне")}
    out_modes = section(skill, "## Режими виходу")
    declared = set(re.findall(r"(?m)^### (.+?)\s*$", out_modes))
    for m in sorted(modes):
        if m not in declared:
            fail(f"режим «{m}» названий у Кроці 0, але не описаний у «Режими виходу»")

    # 2. Опис у frontmatter згадує кожен режим (за ключовим словом).
    desc = skill.split("---", 2)[1]
    keywords = ["проблеми та рішення", "задачі по виконавцях", "технічні деталі",
                "ретро", "деталі по одній темі", "повідомлення учаснику"]
    for kw in keywords:
        if kw not in desc.lower():
            fail(f"frontmatter description не згадує режим «{kw}»")

    # 3. Назви блоків перекладені однаково повно в усіх мовах.
    tpl = re.search(r"(?s)Шаблон:\s*```(.+?)```", skill)
    if not tpl:
        fail("не знайдено блок «Шаблон:» у SKILL.md")
        expected = 0
    else:
        ua = re.findall(r"(?m)^([А-ЯІЇЄҐ][^:\n]*):", tpl.group(1))
        expected = len(set(ua)) + 1  # + умовний рядок «Увага:»
    for lang in ("Англійська", "Російська", "Польська"):
        line = re.search(rf"(?m)^- {lang}: (`[^\n]+)$", skill)
        if not line:
            fail(f"немає рядка перекладу назв блоків для мови «{lang}»")
            continue
        n = len(re.findall(r"`[^`]+:`", line.group(1)))
        if n != expected:
            fail(f"{lang}: {n} перекладених назв блоків, очікується {expected}")

    # 4. Кожен файл, названий у SKILL.md, існує (або має .example-двійника).
    for ref in sorted(set(re.findall(r"`(references/[\w./-]+)`", skill))):
        p = ROOT / ref
        example = p.with_name(p.stem + ".example" + p.suffix)
        if not p.exists() and not example.exists():
            fail(f"SKILL.md посилається на {ref}, якого немає в репозиторії")

    # 5. Чекліст самоперевірки пронумерований суцільно.
    chk = re.search(r"(?s)\*\*Самоперевірка перед видачею.*?\n\n(.+?)\n\n[А-ЯA-Z#]", skill)
    if chk:
        nums = [int(x) for x in re.findall(r"(?m)^(\d+)\. ", chk.group(1))]
        if nums != list(range(1, len(nums) + 1)):
            fail(f"нумерація чеклісту самоперевірки розірвана: {nums}")
    else:
        fail("не знайдено чекліст самоперевірки")

    # 6. Двомовні README мають однакову кількість розділів.
    counts = {p.name: len(re.findall(r"(?m)^## ", p.read_text(encoding="utf-8")))
              for p in READMES if p.exists()}
    if len(counts) != len(READMES):
        fail(f"бракує одного з README: знайдено {sorted(counts)}")
    elif len(set(counts.values())) != 1:
        fail(f"README розійшлись у структурі: {counts}")

    # 7. Персональний ростер не потрапив під версійний контроль.
    try:
        tracked = subprocess.run(["git", "ls-files", "references/roster.md"],
                                 cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if tracked:
            fail("references/roster.md відстежується git — це персональні дані")
    except FileNotFoundError:
        pass

    for e in errors:
        print(f"FAIL: {e}")
    if errors:
        print(f"\n{len(errors)} проблем(и) в документації")
        return 1
    print("OK: документація узгоджена")
    return 0


if __name__ == "__main__":
    sys.exit(main())
