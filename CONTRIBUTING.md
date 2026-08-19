# Як контриб'ютити

English below.

## Одне правило, без якого проєкт не виживе

**Кожне нове правило в SKILL.md приходить із реального провалу і несе спосіб
перевірки.** Не «здається, так краще», а: що пішло не так, на якому вході, і як
переконатися, що правило дотримане.

Скіл росте від тертя в роботі, а не від бажання зробити його повнішим. Правило,
додане «про всяк випадок», ніколи не спрацьовує, але щоразу забирає увагу моделі
від тих, що спрацьовують.

Формат пропозиції в issue або PR:

```
Симптом: що модель зробила не так, на якому транскрипті (знеособленому)
Правило: що саме додати чи змінити в SKILL.md
Перевірка: як побачити, що правило дотримане
```

## Перед тим як відкривати PR

```bash
python3 scripts/check_docs.py
python3 scripts/selftest_checks.py
```

Обидва запускає CI. Перший падає, коли SKILL.md і README розходяться: режим
названий, але не описаний; переклад назв блоків відстає від української;
README-и розійшлись у структурі; персональний ростер потрапив під git; у
відстежуваному файлі зʼявився контакт.

Другий перевіряє сам чекер: вводить кожен вид дрейфу в окрему копію
репозиторію й вимагає, щоб чекер на ній впав, а на контрольній копії — ні.
Додали перевірку в `check_docs.py` — додайте до неї випадок у
`scripts/selftest_checks.py`. Перевірка, яка мовчки перестала перевіряти, гірша
за відсутню.

## Чого не робити

- Не комітьте `references/roster.md` — це персональні дані, файл у `.gitignore`.
  Приклад для заповнення: `references/roster.example.md`.
- Не прикладайте до issue справжні транскрипції. Знеособлений фрагмент на
  кілька реплік показує проблему не гірше.
- Не додавайте в SKILL.md розділ, який лише переказує інший розділ. Якщо
  наявний розділ незрозумілий — виправте його.

---

# Contributing

## The one rule the project cannot survive without

**Every new rule in SKILL.md comes from a real failure and carries a way to
check it.** Not "this feels better", but: what went wrong, on which input, and
how to confirm the rule was followed.

The skill grows from friction in real work, not from a wish to make it more
complete. A rule added just in case never fires, but it takes the model's
attention away from the rules that do.

Proposal format for an issue or PR:

```
Symptom: what the model got wrong, on which (redacted) transcript
Rule: what to add or change in SKILL.md
Check: how to see that the rule was followed
```

## Before opening a PR

```bash
python3 scripts/check_docs.py
python3 scripts/selftest_checks.py
```

CI runs both. The first fails when SKILL.md and the READMEs drift apart: a mode
named but not described, a block-label translation lagging behind the Ukrainian
one, the two READMEs out of structural sync, a personal roster under version
control, a contact address in a tracked file.

The second tests the checker itself: it introduces each kind of drift into its
own copy of the repository and requires the checker to fail there — and to pass
on a clean control copy. If you add a check to `check_docs.py`, add its case to
`scripts/selftest_checks.py` too. A check that silently stopped checking is
worse than none.

## What not to do

- Do not commit `references/roster.md` — it holds personal data and is in
  `.gitignore`. Fill in a copy of `references/roster.example.md` instead.
- Do not attach real transcripts to issues. A redacted fragment of a few lines
  shows the problem just as well.
- Do not add a section to SKILL.md that restates another section. If an existing
  section is unclear, fix that one.
