# follow-up

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-orange.svg)](CHANGELOG.md)
[![Docs check](https://github.com/s1vanov/follow-up/actions/workflows/check-docs.yml/badge.svg)](https://github.com/s1vanov/follow-up/actions/workflows/check-docs.yml)

**Українська версія: [README.md](README.md)**

A Claude skill that turns a meeting transcript into a follow-up you can send as
is: every action owned by exactly one person, decisions and open questions kept
apart, plain text with no markdown.

## Why it exists

You come out of a client call with forty minutes of machine transcript and ten
minutes before the next meeting. Asking a model to "summarise this" gets you a
retelling — who said what, in which order. A week later nobody can extract from
that retelling who was supposed to send the quote.

This skill produces a different artefact. Every action has **one** owner, a
perfective verb and an observable result. A date appears only if a date was
actually spoken. The output pastes into Telegram, Gmail, Worksection or Notion
without cleaning asterisks and hashes out of it by hand.

## What it does

It splits the conversation into six blocks: a header listing every attendee with
their role and side, a two-sentence context, decisions as forward-looking rules,
numbered actions, a by-owner digest and open questions.

It asks which output you need before it starts. Besides the general follow-up
there are: problems and proposed solutions, expanded per-owner tasks, full
technical detail for engineering meetings, a four-block retrospective, a deep
dive into one topic, and a short message to one meeting participant.

Default output language is Ukrainian; English, Russian and Polish are supported
including block labels.

## How it differs from built-in AI summaries

tldv, Fireflies, Otter and similar recorders already produce a summary and a
list of action items. The difference comes down to three things, each of which
cost a mistake on a real meeting:

- **They trust speaker labels.** When a recording mixes up who is speaking —
  and it does — the client and the project manager swap places along with their
  tasks. This skill verifies attribution against what people actually say and
  flags the correction in the header.
- **They invent deadlines.** "ASAP" and "soon" become dates. Here a date only
  comes from a spoken one, and if the meeting date itself is unknown, relative
  terms are not converted at all.
- **They return markdown.** Bold, headings, emoji — all of it has to be stripped
  before the text goes to a client.

## Installation

Claude Code:

```bash
git clone https://github.com/s1vanov/follow-up.git ~/.claude/skills/follow-up
```

Then, for reliable role detection, copy the roster and fill in your team:

```bash
cp ~/.claude/skills/follow-up/references/roster.example.md ~/.claude/skills/follow-up/references/roster.md
```

To verify, type `/follow-up` in Claude Code — the skill should appear
in the list.

## Usage

Paste the transcript after the command, or attach a file:

```
/follow-up
```

The skill asks one question about the format and returns the result. If you
already know the format, name it in the call ("detailed", "problems only",
"make it a retro") and no question is asked.

## Roster

`references/roster.md` holds your people: canonical name, spelling variants seen
in transcripts, role, side. The skill takes roles from there instead of guessing.
The file is deliberately in `.gitignore` — it contains personal data. Only
`roster.example.md` ships in the repository.

The skill works without a roster; roles are then inferred from the text and more
often stay marked `[уточнити роль]`.

## Limits

- **Tested on ten real meetings at a single agency** — Ukrainian and English,
  tldv transcripts and .txt exports from recorders. Not tested in other domains
  such as healthcare, legal or public sector.
- **The meeting date is the weak point of any transcript.** If it appears
  neither in the text, nor in the file name, nor in the recording link, the
  skill uses today's date marked `(припущення)` and does **not** convert
  relative terms ("by Friday") into concrete dates.
- **Swapped-label detection is signal-based.** It needs either
  self-identification in the conversation ("my name is…", "what's your name?")
  or a roster to check against. With neither, roles stay `[уточнити роль]`,
  which beats a confident error.
- **This is not a transcript.** It does not reproduce the discussion verbatim,
  by design.
- **Requires an environment that supports Agent Skills.** The format question in
  Step 0 uses AskUserQuestion; where that tool is unavailable, the skill asks in
  plain text.

## Status

Version 0.1.0, pre-1.0. Used daily by one author at one agency; nobody else has
installed it yet. The style rules and stop-lists are tuned for Ukrainian
business writing and are less tested in other output languages.

## License

CC BY 4.0 — see [LICENSE](LICENSE). Fork it, change it, use it commercially;
keep the attribution.
