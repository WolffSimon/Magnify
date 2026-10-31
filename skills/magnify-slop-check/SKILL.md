---
name: magnify-slop-check
description: Run a mechanical check on a draft for banned devices, assistant vocabulary, runs of same-word openers, verbless sentences and repeated numbers, before any reader sees it.
---

# Magnify slop check

A pattern can catch some faults. A reader is needed for the rest. Run this check first so the cold reviewer's attention goes on what only a reader can find.

## Run it

```
python scripts/slop_check.py DRAFT.md
python scripts/slop_check.py DRAFT.docx --bans my_bans.txt
```

It reads .md, .txt and .docx files. A .docx needs `pip install python-docx`. In Markdown it ignores headings, code, tables and link addresses.

## What it reports

- **FAULT** is a device the law bans. The list covers:
  - em dashes
  - antithesis ("not X but Y", "rather than", "less X than Y")
  - the fronted noun phrase ("X is what I do")
  - absolute constructions ("having built", "with costs held")
  - "under" used as a metaphor
  - "operating system" used as a metaphor
  - assistant vocabulary and self-certifying adjectives
  - intensifiers and use-mention words ("genuinely", "plainly")
  - throat-clearing
  - more than two "I built the X that Y" sentences in one document
  - three or more sentences in a row starting with the same word

  Fix each one, or keep a one-line reason.
- **ADVISORY** is worth a look. It covers sentences with no finite verb that the check could find, and numbers that appear more than once. Both are often faults and sometimes correct. A number may appear twice when the plain sentence needs it.

The exit code is 1 when there is a fault, so the check can gate a pipeline. With `--strict`, advisories also return 1.

## The person's own bans

Every writer collects words they hate. Keep them in a text file, one regular expression per line, with an optional label after ` ## `:

```
# my bans
\bstakeholders? alignment\b ## my ban: say who agreed to what
\bjourney\b ## my ban: unless someone travelled
\bthe ask\b ## my ban: a nouned verb
```

Pass the file with `--bans`. Add to it every time the person corrects a draft. That file and the person's dated rulings are how the law becomes theirs.

## What it cannot catch

Documents that quote the banned devices, such as the law itself, fail the check by design. Run it on drafts.

It cannot catch rhythm, relevance, composition fraud (true facts assembled into a false claim), echoes of the brief, invented facts or missing evidence. Those need `magnify-cold-review`.
