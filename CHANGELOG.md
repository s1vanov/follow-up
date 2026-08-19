# Changelog

Формат — [Keep a Changelog](https://keepachangelog.com/uk/1.1.0/),
версії — [SemVer](https://semver.org/lang/uk/).

## [Unreleased]

### Додано

- Розділ «Сумнівні місця»: зіпсовані транскрибацією слова, які впливають на пункт,
  більше не добудовуються правдоподібним синонімом. Дія формулюється на тому, що чути
  напевно, а сумнів виноситься окремим блоком питань після виходу — цитата з таймкодом,
  прочитання, питання на «так» або «ні». Дев'ятий пункт чеклісту самоперевірки це
  перевіряє.

- `references/SKILL.en.md` — повний англійський переклад скіла для читання й
  адаптації. Робочим лишається український `SKILL.md`: саме він завантажується
  в модель, тож розмір промпту не росте.
- Дев'ята перевірка в `check_docs.py`: структурна парність оригіналу й
  перекладу. Якщо розділ додали в один файл і забули в іншому, збірка падає.
- Англійські блоки в `CHANGELOG.md` і `references/roster.example.md`.

### Змінено

- Повідомлення `check_docs.py` і `selftest_checks.py` тепер англійською. Українські
  рядки, що лишились у коді, — це шаблони пошуку по українському `SKILL.md`, а не
  текст для читача.

### English

Added an "Uncertain passages" section: a word damaged by transcription that bears on an
item is no longer filled in with a plausible synonym. The item is written on what is
certainly audible, and the doubt is raised in a separate block of questions after the
output, each with the quote and its timestamp, the reading, and a yes-or-no question. A
ninth point in the self-check list enforces it.

Added `references/SKILL.en.md`, a full English translation of the skill for
reading and adapting. The Ukrainian `SKILL.md` stays the working file: it is the
one Claude loads, so the prompt does not grow. A ninth check in `check_docs.py`
compares the structure of the original and the translation and fails when a
section exists in one file only. `CHANGELOG.md` and
`references/roster.example.md` gained English blocks, and both scripts now report
in English. The Ukrainian strings left in the code are search patterns matched
against the Ukrainian `SKILL.md`, not text for a reader.

## [0.2.0] — 2026-08-19

### Змінено — увага, ламає шлях встановлення

- Скіл і репозиторій перейменовані з `actionable-follow-up` на `follow-up`:
  виклик тепер `/follow-up`, клон іде в `~/.claude/skills/follow-up`. Хто
  встановлював раніше — перевстановіть за командою з README; стара адреса
  репозиторію більше не редиректить.
- Коротка назва частіше збігається з побутовим вживанням слова, тому в описі й
  у розділі «Коли застосовувати» явно сказано: слово «follow-up» у запиті саме
  по собі не є приводом викликати скіл — приводом є транскрипція або сирі
  нотатки з розмови.

### Додано

- Перевірка контактних каналів у `check_docs.py`: жоден відстежуваний файл не
  містить пошти, месенджера чи телефона, а свідомі винятки живуть у
  `ALLOWED_CONTACTS` з поміткою, хто їх підтвердив.
- `scripts/selftest_checks.py` — самоперевірка чекера: вісім видів дрейфу в
  окремих копіях репозиторію плюс контрольна копія. Запускається в CI.

### Змінено

- Контактна адреса прибрана з SECURITY.md — звіти йдуть через issues.
- Права `GITHUB_TOKEN` у воркфлоу обмежені до `contents: read`.
- `roster.md` ігнорується в будь-якій теці, не лише в `references/`.

### English

Breaking: the install path changed. The skill and the repository were renamed
from actionable-follow-up to follow-up. The call is now `/follow-up` and the
clone goes to `~/.claude/skills/follow-up`. If you installed it earlier,
reinstall using the command in the README; the old repository URL no longer
redirects. Because the short name overlaps with everyday use of the word, the
skill now states explicitly that "follow-up" in a request is not by itself a
reason to invoke it: a transcript or raw notes are.

Added: a contact check in `check_docs.py`, so no tracked file can carry an email,
a messenger handle or a phone number, with deliberate exceptions listed in
`ALLOWED_CONTACTS`. Added `scripts/selftest_checks.py`, which tests the checker
itself by introducing each kind of drift into its own copy of the repository.
Both run in CI. `GITHUB_TOKEN` in the workflow is limited to `contents: read`,
`roster.md` is ignored in any directory, and the contact address was removed from
SECURITY.md.

## [0.1.0] — 2026-08-19

Перший публічний зріз. До цього скіл жив локально й пройшов 10 реальних
зустрічей; усі зміни нижче зроблені за результатами розбору цих сесій.

### Додано

- Крок 0: питання про режим виходу перед стартом (AskUserQuestion, 4 кнопки).
- Розділ «Режими виходу»: проблеми та рішення, задачі по виконавцях, повні
  технічні деталі, ретро (АПД), повідомлення учаснику, деталі по одній темі.
- Розділ «Стиль формулювань»: стоп-списки укр/англ, правило «пиши словами
  зустрічі», прогін прозових блоків через `humanizer`.
- Драбина джерел дати зустрічі; заборона конвертувати відносні терміни, коли
  дата зустрічі — припущення.
- Перевірка атрибуції лейблів спікерів за трьома сигналами; рядок `Увага:` у
  шапці, коли лейбли переплутані.
- Обовʼязкові роль і сторона кожного учасника; заборона ставити компанію
  замість людини.
- Нормалізація імен і чекліст самоперевірки з 8 пунктів перед видачею.
- `references/roster.example.md` — канонічні імена, ролі й сторони.
- `scripts/check_docs.py` — перевірка узгодженості SKILL.md і README.

### Змінено

- Заборона markdown тепер діє на всю сесію, а не на першу відповідь.
- Горизонтальні лінії (`---`, `___`, `***`) явно внесені в заборонені елементи.

### English

First public cut. Before this the skill lived locally and went through ten real
meetings; every change below came out of reviewing those sessions.

Added: Step 0, a question about the output mode before anything is generated; six
output modes (problems and solutions, tasks by owner, full technical detail, a
retrospective in four blocks, a message to a participant, a deep dive into one
topic); a wording-style section with Ukrainian and English stop-lists and the
rule to write in the words of the meeting; a ladder of sources for the meeting
date and a ban on converting relative terms when that date is a guess; an
attribution check for swapped speaker labels; mandatory role and side for every
participant; name normalization and an eight-point self-check before the output
is handed over; `references/roster.example.md`; `scripts/check_docs.py`.

Changed: the ban on markdown now holds for the whole session, not just the first
answer; horizontal rules are named explicitly among the forbidden elements.
