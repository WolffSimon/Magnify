# Magnify

Ask an AI to "write me a deck for X" and it has nothing of yours to work with. It fills the space with the average of everything it has read. That is AI slop. Magnify prevents it. When asked to write something, the AI first asks you a short series of questions for what only you know. Then it drafts to a plain-English law, checks the draft mechanically, and has it read cold by a reviewer that has seen nothing else.

By Matthew Wolff Simon. This project is independent and is not affiliated with, endorsed by or sponsored by Anthropic. "Claude" is used only to name the assistant it was built with.

## Preface

I built Second while running a senior job search with Claude as staff. The lesson I took from it was about the request. A request such as "write my profile for this job" produced a polished page with nothing of mine in it. The model filled the gaps with things that sounded right: claims assembled from true facts into things I had never done, adjectives that vouched for me, and metaphors where the facts should have been.

The cure began before the first word. The assistant asked me numbered questions, and I answered them by voice note on a walk. It wrote only after that, from my answers. Then a reviewer that had never seen me, the build or the conversation read each draft against the job description and my style guide. That caught what still got through.

Magnify is that method, made general, for anyone who asks an AI to write something they will put their name to.

## How it works

1. **Ask.** A thin request triggers questions. Magnify asks who reads the document, what it must make them do, the facts and numbers only you hold, your own view, what must not be said, and the limits. The questions are numbered, so you can answer by voice note in any order. Anything you skip becomes a visible placeholder in the draft, never an invention.
2. **Draft.** The AI writes from your answers to the writing law: plain, conservative English that opens on facts. The law bans the devices that mark machine prose.
3. **Check.** A script catches what a pattern can catch, such as em dashes, antithesis, assistant vocabulary, runs of sentences with the same opener, verbless sentences and repeated numbers. It also catches your own banned words.
4. **Review.** A fresh reviewer each round sees three things and nothing else: the target, the draft and the law. The AI triages every finding. A reviewer never adds a fact. The loop stops when no serious finding remains, or after three rounds.
5. **Hand over.** You get the document, the review scores, and a short numbered list of the decisions only you can make.

An example. Asked for "a deck for our Q3 review", Magnify asks questions like these:

- Who is in the room, and what do you want them to decide?
- Which three numbers matter, and against what targets?
- What went wrong, in your own words?
- What happens next, and who does it?
- How long is the slot?
- Is there anything that must not be said?
- What should I work from, such as last quarter's deck or your notes?

## What is in it

- `skills/magnify-ask-first`: the questions before any draft. Use it whenever someone asks for writing they will send, publish or sign.
- `skills/magnify-prose-law`: the writing law. Read it in full before drafting. A summary of it is written in the register it bans.
- `skills/magnify-slop-check`: the checker, for .md, .txt and .docx files, with a file for your own banned words.
- `skills/magnify-cold-review`: the review loop and the reviewer's brief.
- `SYSTEM_PROMPT.md`: the whole method as one paste-in prompt, for assistants without skills.
- `RUNBOOK.md`: the order of operations.

## Deploying it

**Claude.ai (web and desktop; custom skills need a paid plan).** Zip each skill folder on its own, so that the zip contains the folder with `SKILL.md` inside it. Then go to Settings, Capabilities, Skills, and upload each zip. Ready-made zips are in `dist/`.

**Claude Code.** Copy the folders in `skills/` into `.claude/skills/` in a project, or into `~/.claude/skills/` for every project. Claude Code can run the cold review with a fresh subagent each round.

**Other assistants.** Paste `SYSTEM_PROMPT.md` into the custom instructions or the project instructions. For the cold review, open a new conversation each round, or use a second model. Give it only the brief from `magnify-cold-review` and the three files.

**The checker.** `python skills/magnify-slop-check/scripts/slop_check.py draft.md`. It needs Python 3.8 or later, plus `python-docx` for Word files.

## Making it yours

The law is a starting point. Every writer has words they hate and forms they have corrected. Keep those in a dated list beside the law, and put the patterns in a bans file for the checker. Your rulings outrank the law and every reviewer. The law's own first rule applies too: where a rule and plain English conflict, the plain sentence wins.

## Licence

Prose and skills: CC BY 4.0. Scripts: MIT. See `LICENSE`.
