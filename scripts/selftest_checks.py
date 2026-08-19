#!/usr/bin/env python3
"""Самоперевірка scripts/check_docs.py.

Вводить кожен вид дрейфу окремо в свіжу копію репозиторію й вимагає, щоб чекер
на ньому впав. Контрольна копія без дефектів має пройти. Чекер, який мовчки
перестав перевіряти, виглядає так само зелено, як справний, — цей скрипт і є
різницею між ними.

Копії створюються в новій тимчасовій теці й НЕ прибираються за собою: крок,
який навмисно щось ламає, не повинен ще й видаляти теки — так він упирається в
захисти середовища й тихо випадає з процесу.

Запуск: python3 scripts/selftest_checks.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IGNORE = shutil.ignore_patterns(".git", "roster.md", "__pycache__", "*.pyc")

# Підроблена адреса збирається з частин: інакше цей файл спіймався б власною
# перевіркою на контакти.
FAKE_EMAIL = "someone" + chr(64) + "example.com"


def mutate_file(case_dir: Path, rel: str, old: str, new: str, expect: int = 1) -> None:
    """expect=1 — шаблон має бути унікальним; expect=0 — замінити всі входження."""
    p = case_dir / rel
    text = p.read_text(encoding="utf-8")
    found = text.count(old)
    if found == 0 or (expect == 1 and found != 1):
        raise SystemExit(f"[{rel}] шаблон дрейфу не знайдено або не унікальний: {old!r}")
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


def drift_contact(d: Path) -> None:
    p = d / "README.md"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "## Статус", f"Питання — на {FAKE_EMAIL}\n\n## Статус", 1), encoding="utf-8")


CASES = [
    ("режим без розділу", drift_missing_section),
    ("frontmatter без режиму", drift_frontmatter),
    ("переклад назв блоків відстає", drift_translations),
    ("посилання на відсутній файл", drift_missing_file),
    ("розрив нумерації чеклісту", drift_numbering),
    ("README розійшлись", drift_readme_parity),
    ("ростер під версійним контролем", drift_tracked_roster),
    ("контакт у документації", drift_contact),
]


def run_checker(case_dir: Path) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "scripts/check_docs.py"],
                       cwd=case_dir, capture_output=True, text=True)
    first = r.stdout.strip().splitlines()
    return r.returncode, (first[0] if first else "")


def main() -> int:
    base = Path(tempfile.mkdtemp(prefix="afu-selftest-"))
    print(f"копії для перевірки: {base}\n")
    failures = 0

    for i, (name, drift) in enumerate(CASES, 1):
        d = base / f"case{i}"
        shutil.copytree(ROOT, d, ignore=IGNORE)
        drift(d)
        code, line = run_checker(d)
        caught = code != 0
        failures += 0 if caught else 1
        print(f"{'ловить' if caught else 'ПРОПУСТИВ':10} | {name:32} | rc={code} | {line}")

    control = base / "control"
    shutil.copytree(ROOT, control, ignore=IGNORE)
    code, line = run_checker(control)
    if code != 0:
        failures += 1
    print(f"{'ок' if code == 0 else 'ПРОВАЛ':10} | {'контроль без дефектів':32} | rc={code} | {line}")

    print()
    if failures:
        print(f"{failures} перевірок(ки) не спрацювали — чекер осліп")
        return 1
    print(f"усі {len(CASES)} видів дрейфу спіймані, контроль чистий")
    return 0


if __name__ == "__main__":
    sys.exit(main())
