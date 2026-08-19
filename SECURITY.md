# Security & Privacy

Українською нижче / Ukrainian version below.

## What this skill touches

`actionable-follow-up` is a prompt-level skill: a Markdown instruction file plus
an optional local reference file. It has no runtime, no dependencies and makes
no network calls of its own.

- **Reads:** the meeting transcript you paste or attach, and
  `references/roster.md` if you created one.
- **Writes:** nothing on disk. The follow-up is returned as chat output.
- **Executes:** nothing.

The one script in this repository, `scripts/check_docs.py`, is a documentation
consistency checker for contributors. It reads Markdown files in the repository
and writes nothing.

## The real risk is the input, not the skill

Meeting transcripts are usually the most sensitive text an agency handles:
prices, client complaints, staff assessments, unreleased plans. Whatever model
you run this skill on receives that text in full. Before pasting a transcript,
make sure the deployment you use is one your client agreement allows.

`references/roster.md` contains names and roles of real people. It is listed in
`.gitignore` on purpose. If you fork this repository, verify that your own
roster never gets committed:

```bash
git check-ignore -v references/roster.md
```

## Reporting

Found a problem with the skill's rules — for example an instruction that makes
the model leak part of a transcript into an unrelated block — open an issue in
this repository. Do not attach the transcript that triggered it; a redacted
fragment of a few lines is enough.

---

# Безпека і приватність

## Чого торкається скіл

`actionable-follow-up` — це скіл рівня промпту: файл інструкцій у Markdown плюс
необовʼязковий локальний довідник. Він не має рантайму, залежностей і не робить
жодних мережевих запитів.

- **Читає:** транскрипцію, яку ви вставили або приклали, і `references/roster.md`,
  якщо ви його створили.
- **Пише:** нічого на диск. Follow-up повертається як відповідь у чаті.
- **Виконує:** нічого.

Єдиний скрипт у репозиторії, `scripts/check_docs.py`, перевіряє узгодженість
документації для контриб'юторів. Він читає Markdown-файли й нічого не змінює.

## Справжній ризик — це вхід, а не скіл

Транскрипції зустрічей — зазвичай найчутливіший текст, який проходить через
агенцію: ціни, претензії клієнтів, оцінки співробітників, невипущені плани.
Модель, на якій ви запускаєте скіл, отримує цей текст цілком. Перед тим як
вставляти транскрипт, переконайтесь, що ваш договір із клієнтом дозволяє саме
цей спосіб обробки.

`references/roster.md` містить імена й ролі реальних людей. Він навмисно
внесений у `.gitignore`. Якщо ви форкнули репозиторій — перевірте, що ваш
власний ростер не потрапляє в коміти:

```bash
git check-ignore -v references/roster.md
```

## Як повідомити про проблему

Якщо знайшли проблему в правилах скіла — наприклад інструкцію, через яку модель
переносить частину транскрипту в чужий блок — відкрийте issue у цьому
репозиторії. Не прикладайте транскрипт, на якому це сталося: достатньо
знеособленого фрагмента на кілька реплік.
