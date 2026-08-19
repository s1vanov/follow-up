# Actionable Follow-Up (English translation)

This is a reading translation of `SKILL.md`. The working file is the Ukrainian
`SKILL.md`: that is the one Claude loads. Keep this file in step with it, or
translate your changes back if you write them here first. CI compares the
structure of the two files and fails when one grows a section the other lacks.

Turns raw meeting or call text into a short follow-up built on ARCV+:
**A**ctions, **R**esponsible, **C**learly, **V**erbs (perfective), plus separate
**Decisions** and **Open Questions** blocks.

## When to use

- The user sends a meeting or call transcript and wants a follow-up out of it.
- The user writes: "make a follow-up", "write up the meeting", "pull the action
  items", "what did we agree".
- The user sends raw notes from a conversation with a client or the team.

Do NOT use when:

- The user asks for a letter, a message or a reminder and there is no transcript.
  The word "follow-up" in the request is not a reason; the text of the
  conversation is. (If there is a transcript and a message to a participant is
  needed, that is a mode inside this skill, not a separate case.)
- The user asks for a translation of the transcript without structuring it.
- The user asks for verbatim minutes. That is a different document, one that
  keeps the whole course of the discussion.
- The text carries no signs of a meeting: no agreements, no decisions, no tasks.

## Output language

- Default: **Ukrainian**.
- If the user names another language in the request ("in English", "по-русски",
  "po polsku"), use that language for the whole output, block labels included
  (`## Decisions`, `## Действия`).
- Do not translate proper names: participants, companies, products.

## How it works

### Step 0. Ask about the format before you start

Before generating anything, ask **one** question through AskUserQuestion: which
output is needed. Allow several answers (`multiSelect: true`), because a general
follow-up and a separate breakdown are often both wanted. If AskUserQuestion is
unavailable in the environment, ask the same question as plain text, as a
numbered list, and wait for the answer.

Four options as buttons, in this order:

1. **General follow-up (recommended)** — the short ARCV+ document described below.
2. **Problems, solutions and expectations** — what hurts, what was proposed, what
   the client expects.
3. **Tasks by owner** — expanded tasks for named people, with the "how exactly".
4. **Full technical detail** — every stated requirement for the code or the
   implementation, uncut.

Two more modes are not on buttons but are described in "Output modes" below. The
user reaches them through "Other" or by naming them: **Retrospective in four
blocks**, **A deep dive into one topic or project** and **A message to a meeting
participant**.

When NOT to ask:

- The user already named the mode in the call ("detailed", "problems only", "make
  it a retro", "keep all the technical detail"). Do it, no questions.
- This is not the first request in the session: the follow-up exists and the user
  asks to expand it. Just do it.

If several modes are chosen, produce them one after another, each under its own
heading line, with a blank line between them. The format rules (plain text, one
owner, perfective verbs) are the same for every mode.

### Step 1. Extract eight things from the transcript

Read the transcript through once. Identify:

1. **Meeting topic** — one phrase.
2. **Meeting date** — work down this ladder of sources and stop at the first one
   that gives an answer:
   1. A date stated in the transcript.
   2. A date in the recording's file name or recorder metadata
      (`..._2026-08-14-10-24-29.txt` gives 14 August 2026).
   3. A date in the heading or the link to the recording (tldv and similar).
   4. Today's date. Only in this case append ` (припущення)`, the assumption mark.

   The mark goes on case 4 **only**. A date taken from the file or the transcript
   is a fact, not an assumption.

   Right after you fix the date, work out its **weekday** and count every relative
   deadline from it ("by Friday", "next week"). A wrong base date silently shifts
   every deadline in the action list. Exception: if the date came from rung 4,
   relative terms are not converted at all. See the date rule in Step 2.
3. **Attendees** — everyone who spoke or is named as present.

   **Check the attribution of the speaker labels before you assign roles.**
   Speaker labels in a recording are sometimes swapped between people. It happens,
   and this is exactly where the skill used to break: roles are inferred from the
   lines, and the lines are attributed to the wrong people. Check three signals:
   - **Self-identification.** "What's your name?" and the answer; "my name is…";
     "I'm on the client side"; "I'm moderating". If the person under label `A`
     calls themselves `B`, the labels are swapped.
   - **The roster.** If someone listed in `references/roster.md` as "our team"
     talks about their own business and asks for a website, that is not them.
   - **Side logic.** Whoever describes the process, the team and the timeline is
     the supplier; whoever describes their business and their need is the client.

   When you find a conflict, **trust the content of the lines, not the label**,
   and add a line to the header, after `Учасники:` (or after `Згадані:` when that
   line exists): `Увага: у записі переплутані лейбли спікерів, ролі відновлено за
   змістом розмови.` The reader has to know that checking against the recording
   blindly will mislead them.

   Then, for every participant, record the role and the side in the form
   `Name (role, side)`, where the side is our team, the client or a contractor:
   `Андрій Мельник (менеджер проєкту, наша команда)`, `John Smith (замовник,
   клієнт)`.
   - If the role or the side does not follow unambiguously from the transcript,
     write `[уточнити роль]`. Do not reconstruct a role from the order of the
     lines: that is exactly how the client and the project manager swap places
     and the actions land on the wrong people.
   - Before assigning roles, check `references/roster.md`: it holds canonical
     names, roles and sides for the people who show up regularly. The file wins
     over a guess from the transcript.
   - The attendee list holds **people, not companies**. Not `Northwind Beauty LLC
     (Віктор)` but `Віктор (власник, клієнт — Northwind Beauty LLC)`.
4. **Mentioned** — people who were NOT at the meeting but appear below as owners
   of tasks or as a source of information ("the assistant Oksana will set up the
   script"). Skip this item when there are none.
5. **Context** — one or two sentences explaining why this meeting happened and
   what it was broadly about. Not a retelling of the discussion: a bearing for
   someone who was not there. Skip it when the topic line already says everything
   ("1:1 with Ivan", "Team standup").
6. **Decisions** — what was settled as a **rule or condition going forward**, with
   no owner and no date.
7. **Actions** — concrete tasks someone has to carry out.
8. **Open questions** — unresolved, needs data, postponed, needs other people.

### Step 2. Write every action to the formula

```
[Owner] [perfective verb] [what exactly][, by a concrete date]. — [why, when it is not obvious]
```

The `by a concrete date` part is **optional**. Details below.

Rules:

- **The owner is one person.** Not "the team", not "we", not "someone". If the
  transcript assigns nobody, put whoever runs the meeting (PM or note taker) and
  add `[уточнити власника]`.
- **Perfective verb.** "Will prepare", "will send", "will publish", "will sign
  off", "will check". Not "work on", "discuss", "look into", "handle".
- **A date only if it was actually spoken at the meeting.** This one is strict:
  - If the transcript names a date, explicit ("by 15 May") or relative ("by
    Friday", "next week", "by the end of the month"), convert it into the human
    format of the output language, counting from the meeting date:
    - Ukrainian: `22 травня 2026 року`
    - Russian: `22 мая 2026 года`
    - English: `22 May 2026`
    - Polish: `22 maja 2026`
    - Others: follow the local norm for writing dates.
  - If the deadline **never came up** in the discussion, **end the wording with a
    full stop. No placeholder, no invented date, no "when there is time".** The
    user will add the date once it exists.
  - "ASAP", "soon", "by the end of the week" with nothing concrete behind them
    are **not dates**: they are figures of speech, not deadlines. The action goes
    out without one.
  - **A relative term is not converted when the meeting date is itself an
    assumption.** When the date came from rung 4 of the ladder (today's date with
    the `(припущення)` mark), "by Friday" or "today or tomorrow" is **not** turned
    into a concrete date: that would dress a guess up as a precise date. The
    action goes out without a date, and the term, if it matters, goes into Open
    questions in the words of the meeting ("promised today or tomorrow morning,
    date to confirm"). Conversion is allowed for rungs 1 to 3 only.
- **Why-tail (optional).** After the main wording you may add a short reason
  through ` — ` when the item looks arbitrary without it or depends on another
  action. When it is obvious anyway, leave it out.
- **Observable result.** If an action can be read two ways ("sort it out", "think
  about it"), rewrite it into a work artefact ("will post the report in Slack",
  "will publish the draft in Notion", "will get the contract signed").

### Step 3. Sort into blocks and mix nothing

- **Decisions are not actions.** A decision is a rule that holds from now on ("we
  split the payment into three instalments", "the release deadline is 30 June").
  An action is a one-off task with an owner and a date.
- **Open questions are not actions.** If it is known who looks for the answer and
  by when, it is an action. If not, it is an open question.
- **One item, one action.** If a sentence in the transcript carries two verbs with
  different results, split it into two numbered items.

### Step 4. Assemble the follow-up in the format below

## Output format

The output is **plain text with no markdown at all**. No `**`, `##`, `*`, `_`, no
backticks, no `[text](url)` links, no tables, no code blocks, no emoji, no
banners, no horizontal rules (`---`, `___`, `***`).

**This is a contract for the whole session, not for one artefact.** The ban on
markup holds for every following answer in this conversation: expanded detail, a
breakdown of problems, a retrospective, extracted tasks, a covering message to a
client, until the user explicitly asks otherwise. The most common failure of this
skill: the first follow-up is clean and the second answer comes back with
headings and bold, and the user cleans it out by hand. The text has to look
identical in Telegram (standard client), Gmail, Outlook, Slack, Worksection,
Notion, and when pasted into any other editor.

Structure:

- Header: `Зустріч:`, `Дата:`, `Учасники:` (mandatory, every one with role and
  side), plus `Згадані:` (when there are any) and the `Увага:` line about swapped
  labels (when you found some). Each on its own line.
- Blank line.
- The `Контекст:` block: one or two sentences of prose, no bullets, no lists.
  Skipped when the topic line is self-sufficient.
- Blank line.
- The name of every following block (`Рішення:`, `Дії:`, `По виконавцях:`,
  `Відкриті питання:`) on a line of its own.
- Blank line after the block name.
- The list of items.
- Actions are a numbered list (`1.`, `2.`, …). The numbering runs unbroken through
  the whole list.
- Decisions, open questions and the lines under "By owner" are bullets with a dash
  at the start of the line (`— `).
- **A blank line between every list item**, not only between blocks. Without it,
  messengers and email collapse the items into a wall of text and the list stops
  being readable. This applies to the numbered actions as much as to every bullet
  list.
- Blank line between blocks.

**Normalizing names.** Machine transcription is noisy, so names come out damaged.

- Take the spelling of a name from the speaker labels ("Petro Koval [00:00]:"),
  not from the body of the lines: inside the lines is where ASR mangles names most
  ("Oksan" for "Oksana", "Petr" for "Petro"). A label gives you **the spelling,
  not a guarantee** of who said the line: run the attribution check from Step 1
  before you assign roles and actions.
- One person, **one written form** through the whole document, in the alphabet of
  the output language. In a Ukrainian follow-up do not mix `Petro Koval` and
  `Петро Коваль`: pick the Cyrillic form and hold it everywhere, including the
  "By owner" block and every expansion.
- If `references/roster.md` exists, take canonical name forms, roles and sides
  from there, and use the transcript only for people the file does not list.

**The rule for the Context block.** Two sentences maximum, about 40 words in
total. No bullets, no numbering, no headings, no enumerations. It says **why**
people gathered and **what** the conversation was broadly about. It does not
repeat actions and decisions. When there is nothing to add beyond the topic line,
drop the block entirely.

**The "By owner" block.** After the actions, add a mini digest: every owner plus
the numbers of their items, comma separated. It lets a person find their own tasks
without rereading the whole list.

- Include this block **only when the actions have two or more distinct owners**.
  With a single owner it adds nothing.
- Sort by **descending number of tasks** (most first). On a tie, by order of first
  appearance in the action list.
- If one action has several co-owners, that person appears in several lines with
  that number.
- If there is an action marked `[уточнити власника]`, add a final separate line
  `— Без власника: <numbers>`.

Template:

```
Зустріч: <topic on one line>
Дата: <DD month YYYY> in the locale of the output language
Учасники: Name1 (role, side), Name2 (role, side), Name3 (role, side)
Згадані: NameX (role), NameY (role)

Контекст:

<one or two sentences on the purpose of the meeting and the range of topics>

Рішення:

— <decision 1>

— <decision 2>

Дії:

1. <Owner> <perfective verb> <what exactly> by <concrete date>. — <why, when needed>

2. <Owner> <perfective verb> <what exactly>. — <why, when needed>   ← no date, when it was not discussed

По виконавцях:

— Name1: 1, 3, 5

— Name2: 2, 4

— Name3: 6

Відкриті питання:

— <question 1>

— <question 2 — who looks for the answer and by when, when that is already known>
```

If a block has nothing in the transcript behind it (no decisions, say), drop the
block completely: do not leave a heading over emptiness.

**The self-check before you hand the output over (mandatory, every time).** Read
the generated text again and check it point by point:

1. The header and block names are spelled correctly, with no Latin homoglyphs
   inside Cyrillic words (`Zустріч:` instead of `Зустріч:` is a real bug this
   skill produced; `C`, `P`, `X`, `A`, `E`, `O`, `I` are the dangerous ones).
2. Every name is written in one and the same form throughout.
3. Every participant in the header has a role and a side; no company stands where
   a person should.
4. The action numbering is unbroken, with no gaps and no repeats.
5. Every number in "By owner" exists in the action list, and no action went
   missing.
6. No markdown anywhere, `---` and backticks included.
7. Dates are either taken from a source or absent. Nothing invented, no "soon".
8. The first sentence of every prose block is a fact, not a stock opener ("The
   meeting was broadly devoted to…", "It is important to note that…"). The
   stop-list is in "Wording style".

Translate the block names and the header along with the rest of the text when the
user sets another output language:

- English: `Meeting:`, `Date:`, `Attendees:`, `Mentioned:`, `Note:`, `Context:`,
  `Decisions:`, `Action items:`, `By owner:`, `Open questions:`
- Russian: `Встреча:`, `Дата:`, `Участники:`, `Упомянуты:`, `Внимание:`,
  `Контекст:`, `Решения:`, `Действия:`, `По исполнителям:`, `Открытые вопросы:`
- Polish: `Spotkanie:`, `Data:`, `Uczestnicy:`, `Wspomniani:`, `Uwaga:`,
  `Kontekst:`, `Decyzje:`, `Działania:`, `Wg odpowiedzialnych:`, `Pytania otwarte:`

## Wording style

The structural rules above strip the markup and the empty verbs, but not the
vocabulary. Slop gets into this skill through the prose blocks: Context, Problems
and solutions, Retrospective, a deep dive into one topic, a message to a
participant. The rules below cover them.

**The main rule: write in the words of the meeting.** If the call said "a
doorway to Amazon", write that, do not replace it with "an intermediate traffic
platform". A synonym that was not in the conversation is almost always longer and
weaker than the original, and it quietly shifts the meaning.

**A follow-up records, it does not comment.** No assessments, no emotion: "sadly",
"a great idea", "interestingly", "worth praising". If an assessment was voiced at
the meeting, it is a quotation from a participant, and then it is visible who gave
it.

### Stop-list, Ukrainian

On the left, what to cut or replace; on the right, what with:

- «наразі», «на даний момент» → «зараз», or nothing
- «важливо зазначити, що», «варто відзначити», «слід підкреслити» → delete, state
  the fact straight away
- «даний», «вищезазначений», «вищевказаний» → «цей»
- «з метою» → «щоб»
- «в рамках проєкту / зустрічі» → «на проєкті», «на зустрічі»
- «здійснити», «провести роботи з», «забезпечити виконання» → a concrete verb:
  «налаштує», «надішле», «перевірить»
- «оптимізувати процеси», «покращити взаємодію», «підвищити ефективність» → what
  exactly changes and where it will be visible
- «комплексний підхід», «глибока експертиза», «прозора комунікація», «синергія» →
  marketing clichés, no place in a follow-up
- «є важливим», «є необхідним» → «важливо», «треба»
- «Отже, підсумовуючи», «Давайте розглянемо», «Як ми бачимо» → meta-text, delete

Constructions that must not appear:

- Groups of three for the rhythm ("fast, clean and transparent"): keep what was
  actually said.
- "Not just X, but Y": an intensifier with no information.
- A rhetorical question opening a paragraph.
- A paragraph that opens with a generalization ("Overall the meeting showed
  that…") instead of a fact.

### Stop-list, English (for messages to a client)

- "I hope this message finds you well", "Just wanted to reach out / circle back /
  touch base" → straight to the point: "I'm writing about X"
- "leverage", "utilize", "facilitate", "streamline", "robust", "seamless",
  "cutting-edge", "holistic" → plain verbs and adjectives
- "It's worth noting that", "It's important to highlight" → delete
- "delve into", "in today's fast-paced world", "the landscape of" → delete
- "Looking forward to hearing from you!" together with "Let me know if you have
  any questions!" → one closing line at most, better none
- "not just X, but Y" → say it straight

### Running it through humanizer

Before handing the output over, run the prose blocks through the `humanizer`
skill (or `anthropic-skills:stop-slop`). This covers Context, the modes "Problems,
solutions and expectations", "Retrospective", "A deep dive into one topic" and "A
message to a meeting participant".

Do **not** run the numbered actions through humanizer: they are formulaic by
design (`[Owner] [perfective verb] [what exactly]`), and rewriting them only blurs
the formula.

## Output modes

The general follow-up above is the default. Below are the rest of the modes from
Step 0. All of them obey the same rules: clean plain text, one owner per action,
perfective verbs, a date only if it was spoken, a blank line between items.

### Problems, solutions and expectations

Each problem is a numbered item of three parts on three lines:

```
Проблеми та рішення:

1. Проблема: <what exactly does not work or hurts, in the words of the meeting>.
   Причина: <if a cause was named at the meeting; if not, the line is dropped>.
   Рішення: <what was proposed and by whom; if none was found, «не знайшли на зустрічі»>.

Очікування клієнта:

— <what the client expects from the work or the result>
```

Do not fuse the problem and the solution into one sentence, and do not invent a
solution nobody voiced.

### Tasks by owner

An expanded version of the action block for one person or for everyone. Per task:

```
Задачі для <Name>:

1. <What they will do — perfective verb, observable result>.
   Як саме: <the steps or requirements as they were stated at the meeting>.
   Результат: <what has to be visible at the end: a file, a message, access, a document>.
   Дедлайн: <the date, if it was discussed; the line is dropped if not>.
```

The wording stays such that the item can be pasted straight into a tracker.

### Full technical detail

The mode for engineering meetings: markup review, architecture discussion, code
requirements. Technical wording is **not compressed**: the detail is the value.

- Group by topic (buttons, headings, spacing, scripts); each topic gets a heading
  line of its own ending with a colon.
- Every requirement is a separate bullet: what to do, how to do it, and why that
  way, when the reason was voiced at the meeting.
- Carry the specifics over verbatim: classes, tags, sizes, property names, values.
- The action block with owners still goes at the end. Detail does not replace
  tasks.

### Retrospective in four blocks

Four blocks, each a heading line ending with a colon, numbered items inside:

```
1. Що було заплановано:
2. Що насправді відбулося:
3. Чому так сталося:
4. Що зробити по-іншому наступного разу:
```

Write the fourth block so that every item can be turned into a task with an
owner. In "Why it happened" rely only on causes named at the meeting; when no
cause was named, say so instead of offering your own hypothesis.

### A message to a meeting participant

A short text for a chat or an email, built on what was agreed, when the point is
to move the next step rather than forward the summary.

- The language is **the recipient's language**, not the language of the follow-up.
  If the meeting was in Ukrainian and the recipient speaks English, write in
  English.
- Length: up to 120 words. One message, not a three-paragraph letter.
- Structure: one sentence of context (what this refers to), then what has already
  been done or sent, then one concrete question or next step out of what was
  agreed.
- No "hope you're doing well", no signature, no two closing lines in a row.
- Ask about what genuinely stayed open according to the transcript, not "let me
  know if you have any questions".
- Mandatory pass through `humanizer` and the English stop-list above.

### A deep dive into one topic or project

An expanded retelling of one topic from the meeting, for someone who was not
there. Sub-blocks are heading lines ending with a colon (`Бекграунд клієнта:`,
`Що вже зроблено:`, `Що хоче клієнт:`, `Ризики:`). Prose, no markdown. Do not
retell the conversation line by line: gather it by topic.

## Example

**Input (a fragment of a transcript, meeting date 2026-05-12, a Monday):**

> Oleksii: Right, the deck. I'll do it by Friday.
> Maryna: And who are we showing it to?
> Oleksii: Acme first. Serhii, will you be on the call?
> Serhii: Yes, I'm moderating. By the way, have we settled the price?
> Oleksii: We keep $5000 a month, as agreed last time. Wait — will Maryna make Friday with her part?
> Maryna: If I get the brief, yes. I'm waiting for it today.

**Output (default output language, Ukrainian):**

```
Зустріч: Підготовка презентації для Acme
Дата: 12 травня 2026 року
Учасники: Олексій (акаунт-менеджер, наша команда), Марина (дизайнер, наша команда), Сергій (керівник, наша команда)

Рішення:

— Ціна для Acme — $5000 на місяць.

Дії:

1. Олексій надішле Марині бриф для її блоку презентації до 12 травня 2026 року. — Без брифу Марина не встигне до п'ятниці.

2. Марина підготує свій блок презентації до 15 травня 2026 року. — Залежить від брифу від Олексія.

3. Олексій збере фінальну презентацію для Acme до 15 травня 2026 року.

4. Сергій модеруватиме дзвінок з Acme.

По виконавцях:

— Олексій: 1, 3

— Марина: 2

— Сергій: 4

Відкриті питання:

— Дата дзвінка з Acme — [уточнити власника й дедлайн].
```

## What NOT to do

- **Do not retell the discussion narratively** ("First they talked about…, then
  moved on to…"). This is a follow-up, not minutes.
- **Do not leave an action without an owner.** When the owner is unknown, put the
  PM or the note taker and mark it `[уточнити власника]`.
- **Do not use imperfective verbs** ("work on", "discuss", "look into",
  "handle"). Rewrite them into "will do", "will discuss with X", "will check",
  "will pick up".
- **Do not invent a deadline that was not in the discussion.** If the meeting did
  not say by when, write the action without a date. No `[уточнити дедлайн]`, no
  "soon", no date added "by logic". The user will set it when it becomes clear.
- **Do not write "ASAP", "soon", "by the end of the week"** as a date. When a real
  concrete date was spoken, write it in the locale of the output language
  (`22 травня 2026 року`, not `2026-05-22`, not `22.05.2026`).
- **Do not mix decisions with actions** in one list. They are different things.
- **Do not invent items** that are not in the transcript. When something is
  missing, put `[уточнити …]` instead of filling the gap.
- **Do not use any markdown** — `**bold**`, `## headers`, `*italic*`,
  `_underline_`, backticks, `[text](url)` links, tables, code blocks, emoji, H1
  headings, horizontal rules (`---`, `___`, `***`). In the first answer and in
  every following one in this session. In Gmail, Worksection, the standard
  Telegram client and Outlook these characters render literally and the user has
  to clean them out by hand.
- **Do not write in clichés and officialese** («наразі», «в рамках проєкту»,
  «здійснити», «комплексний підхід», «важливо зазначити, що»). The stop-list and
  the replacements are in "Wording style"; run the prose blocks through
  `humanizer` before handing them over.
- **Do not change the output language** unless the user asks explicitly.
- **Do not take speaker labels on faith.** If the lines under one person's label
  belong to another, trust the content, not the caption, and mark it in the
  header. The check is described in Step 1.
- **Do not count deadlines from an assumed date.** When the meeting date carries
  the `(припущення)` mark, relative terms stay unconverted.
- **Do not guess a participant's role or side.** When the transcript does not show
  who is the client and who is the project manager, put `[уточнити роль]`. A
  mistake here scatters the actions across the wrong people and the whole
  follow-up has to be rewritten.
- **Do not write closing pleasantries** ("Thanks for the meeting, looking forward
  to confirmation!"). If a covering text is needed, the user will add it.
