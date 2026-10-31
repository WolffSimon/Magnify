# Magnify

Ask an AI to "write me a deck for X" and it has nothing of yours to work with. It fills the space with the average of everything it has read. That is AI slop. Magnify prevents it. When asked to write something, the AI first asks you a short series of questions for what only you know. Where the document depends on facts about the world, it sends research agents after the key questions and checks the answers at source. Then it drafts to a plain-English law, checks the draft mechanically, and has it read cold by a reviewer that has seen nothing else.

By Matthew Wolff Simon. This project is independent and is not affiliated with, endorsed by or sponsored by Anthropic. "Claude" is used only to name the assistant it was built with.

## Preface

I built Second while running a senior job search with Claude as staff. The lesson I took from it was about the request. A request such as "write my profile for this job" produced a polished page with nothing of mine in it. The model filled the gaps with things that sounded right: claims assembled from true facts into things I had never done, adjectives that vouched for me, and metaphors where the facts should have been.

The cure began before the first word. The assistant asked me numbered questions, and I answered them by voice note on a walk. It wrote only after that, from my answers. Then a reviewer that had never seen me, the build or the conversation read each draft against the job description and my style guide. That caught what still got through.

Magnify is that method, made general, for anyone who asks an AI to write something they will put their name to.

## How it works

1. **Ask.** A thin request triggers questions. Magnify asks who reads the document, what it must make them do, the facts and numbers only you hold, your own view, what must not be said, and the limits. The questions are numbered, so you can answer by voice note in any order. Anything you skip becomes a visible placeholder in the draft, never an invention.
2. **Research.** The AI looks at what the document depends on that you do not hold: the reader's organisation, a market, a rule, recent results. It turns those gaps into a few key questions and briefs research agents to answer them in parallel, with a date and a link for every claim. It checks the facts the argument rests on at their source, and marks the rest "as reported".
3. **Draft.** The AI writes from your answers and the verified findings to the writing law: plain, conservative English that opens on facts. The law bans the devices that mark machine prose.
4. **Check.** A script catches what a pattern can catch, such as em dashes, antithesis, assistant vocabulary, runs of sentences with the same opener, verbless sentences and repeated numbers. It also catches your own banned words.
5. **Review.** A fresh reviewer each round sees three things and nothing else: the target, the draft and the law. The AI triages every finding. A reviewer never adds a fact. The loop stops when no serious finding remains, or after three rounds.
6. **Hand over.** You get the document, the review scores, and a short numbered list of the decisions only you can make.

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
- `skills/magnify-research`: the key questions behind a document, the brief for each research agent, and the checks before any finding is used.
- `skills/magnify-prose-law`: the writing law. Read it in full before drafting. A summary of it is written in the register it bans.
- `skills/magnify-slop-check`: the checker, for .md, .txt and .docx files, with a file for your own banned words.
- `skills/magnify-cold-review`: the review loop and the reviewer's brief.
- `SYSTEM_PROMPT.md`: the whole method as one paste-in prompt, for assistants without skills.
- `RUNBOOK.md`: the order of operations.

## Installing it

**From Anthropic's directory (claude.ai, Cowork and Claude Code).** Once the listing is live, find Magnify in the directory at claude.ai/directory and add it. It then loads in Claude Code too.

**Claude Code, from this repository.** In your shell:

```
claude plugin marketplace add WolffSimon/Magnify
claude plugin install magnify-writing@wolffsimon
```

You can also copy the folders in `skills/` into `.claude/skills/` in a project, or into `~/.claude/skills/` for every project. Claude Code can run the cold review and the research with fresh subagents.

**Claude.ai, as uploaded skills.** Download the skill zips from this repository's Releases page. Then go to Settings, Capabilities, Skills, and upload each zip. Custom skills need a paid plan.

**Other assistants.** Paste `SYSTEM_PROMPT.md` into the custom instructions or the project instructions. For the cold review, open a new conversation each round, or use a second model. Give it only the brief from `magnify-cold-review` and the three files.

**The checker.** `python skills/magnify-slop-check/scripts/slop_check.py draft.md`. It needs Python 3.8 or later, plus `python-docx` for Word files.

## What it runs and what it sends

Magnify is a set of written instructions and one script. The script, `slop_check.py`, reads the file you give it and prints its findings. It makes no network connections and writes no files. The skills tell your assistant to ask you questions, to draft, and to start reviewer and research agents in your own session. Research uses your assistant's own web search and page-fetching tools. Magnify collects no data and sends nothing anywhere.

## Making it yours

The law is a starting point. Every writer has words they hate and forms they have corrected. Keep those in a dated list beside the law, and put the patterns in a bans file for the checker. Your rulings outrank the law and every reviewer. The law's own first rule applies too: where a rule and plain English conflict, the plain sentence wins.

## Licence

Prose and skills: CC BY 4.0. Scripts: MIT. See `LICENSE`.
