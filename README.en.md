# follow-up

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-orange.svg)](CHANGELOG.md)
[![Docs check](https://github.com/s1vanov/follow-up/actions/workflows/check-docs.yml/badge.svg)](https://github.com/s1vanov/follow-up/actions/workflows/check-docs.yml)

**Українська версія: [README.md](README.md)**

A Claude skill. It turns a meeting transcript into an actionable follow-up: every
action has one owner, a perfective verb and a result you can see. Plain text, no
markdown.

## What makes a follow-up actionable

A meeting summary and an actionable follow-up are different documents. The first
retells the conversation, the second says who does what next. This skill builds
the second one, using a framework called ARCV+.

**Actions.** Only what someone has to do stays in the document. The course of the
discussion is not retold at all.

**Responsible.** The owner of an action is one person, not "the team" and not
"we". If nobody was named on the call, the item carries `[уточнити власника]`
instead of a silent assumption.

**Clearly.** Every wording is checked for a second reading. "Sort out the
integration" becomes "will post the list of missing fields in Slack".

**Verbs, perfective.** "Will prepare", "will send", "will sign off". An
imperfective verb ("work on", "look into") hides the moment when the task can be
called done.

There is also something a plain summary lacks: decisions and actions live in
separate blocks. A decision is a rule that holds from now on ("we split the
payment into three instalments"), with no owner and no date. An action is a
one-off task. Mixed into one list, the two turn the document back into notes. A
third block, open questions, holds what was left unresolved so it does not sink
between the actions.

One rule saves more often than the rest: a date appears only if it was said out
loud. "ASAP", "soon" and "by the end of the week" do not count as dates. The
action goes out without a deadline, and you set one yourself once it actually
exists.

## Why it exists

You come off a client call with forty minutes of machine transcript and ten
minutes before the next meeting. Ask a model to "summarise this" and you get a
retelling: who said what, in which order. A week later nobody can extract from it
who was supposed to send the quote.

The output of this skill pastes into Telegram, Gmail, Worksection or Notion
without cleaning asterisks and hashes out of it by hand.

## What the output looks like

```
Meeting: Preparing the Acme presentation
Date: 12 May 2026
Attendees: Oleksii (account manager, our team), Maryna (designer, our team)

Decisions:

— Price for Acme: $5000 per month.

Action items:

1. Oleksii will send Maryna the brief for her part of the deck by 12 May 2026. — Without the brief Maryna will not make Friday.

2. Maryna will prepare her part of the deck by 15 May 2026.

By owner:

— Oleksii: 1

— Maryna: 2

Open questions:

— Date of the call with Acme.
```

The blank line between items is deliberate: in messengers and email a dense list
collapses into a wall of text.

## Modes

The skill asks which output you need before it starts. Besides the general
follow-up there are five more: problems with proposed solutions, expanded
per-owner tasks, full technical detail for engineering meetings, a four-block
retrospective, a deep dive into one topic, and a short message to one participant.

Default output language is Ukrainian. English, Russian and Polish are supported,
block labels included.

## How it differs from built-in AI summaries

tldv, Fireflies, Otter and similar recorders already produce a summary and a list
of action items. The difference comes down to three things, and each of them cost
a mistake on a real meeting.

Recorders trust speaker labels. When a recording mixes up who is speaking, the
client and the project manager swap places along with their tasks. This skill
checks labels against what people actually say and flags the correction in the
header.

Recorders invent deadlines. "ASAP" becomes a date, a relative term is counted
from nothing in particular. Here a date only comes from a spoken one, and if the
meeting date itself is unknown, relative terms are not converted at all.

And what comes out is markdown. Bold, headings, emoji: all of it has to be
stripped before the text goes to a client.

## Installation

Claude Code:

```bash
git clone https://github.com/s1vanov/follow-up.git ~/.claude/skills/follow-up
```

Then, for reliable role detection, copy the roster and fill in your team:

```bash
cp ~/.claude/skills/follow-up/references/roster.example.md ~/.claude/skills/follow-up/references/roster.md
```

To verify, type `/follow-up` in Claude Code and check that the skill shows up in
the list.

The working skill file is Ukrainian: that is what Claude loads. A full English
translation for reading and adapting is in
[references/SKILL.en.md](references/SKILL.en.md), and CI fails when the two drift
apart in structure.

## Usage

Paste the transcript after the command, or attach a file:

```
/follow-up
```

The skill asks one question about the format and returns the result. If you
already know the format, name it in the call ("detailed", "problems only", "make
it a retro") and no question is asked.

## Roster

`references/roster.md` holds your people: canonical name, spelling variants seen
in transcripts, role, side. The skill takes roles from there instead of guessing.
The file is deliberately in `.gitignore` because it contains personal data. Only
`roster.example.md` ships in the repository.

The skill works without a roster; roles are then inferred from the text and more
often stay marked `[уточнити роль]`.

## Limits

Tested on ten real meetings at a single agency, in Ukrainian and English, on tldv
transcripts and .txt exports from recorders. Not tested in other domains such as
healthcare, legal or public sector.

The meeting date is the weak point of any transcript. If it appears neither in
the text, nor in the file name, nor in the recording link, the skill uses today's
date marked `(припущення)` and does not convert relative terms into concrete
dates.

Swapped-label detection is signal-based. It needs either self-identification in
the conversation or a roster to check against. With neither, roles stay marked
`[уточнити роль]`, which beats a confident error.

This is not a transcript. It does not reproduce the discussion verbatim, by
design.

Requires an environment that supports Agent Skills. The format question uses
AskUserQuestion; where that tool is unavailable, the skill asks in plain text.

## Status

Version 0.2.0, pre-1.0. Used daily by one author at one agency; nobody else has
installed it yet. The style rules and stop-lists are tuned for Ukrainian business
writing and are less tested in other output languages.

## License

CC BY 4.0, see [LICENSE](LICENSE). Fork it, change it, use it commercially, keep
the attribution.
