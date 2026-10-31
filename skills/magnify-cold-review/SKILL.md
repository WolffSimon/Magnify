---
name: magnify-cold-review
description: Review a finished draft with fresh reviewers who see only the target, the text and the style law. Triage the findings, iterate up to three rounds, then hand over.
---

# Magnify cold review

A writer cannot see their own draft cold, and neither can the assistant that wrote it. This loop gives the draft to a reader who knows nothing else. That reader sees the target, the text and the style law, and nothing of how the draft was made. Each round uses a new reviewer, so no reviewer marks its own earlier advice.

## Before the first round

1. Finish the draft. Run `magnify-slop-check` on it and fix what it finds.
2. Export the draft to plain text if it is in another format.
3. Write the **target** if there is no brief, posting or request to use. It is a short file covering three things:
   - who reads the document first (a recruiter, a board, a customer, a stranger on LinkedIn)
   - what that reader is looking for
   - what the document must do for them
4. Have the **style law** ready: `magnify-prose-law`, plus the person's own list of rulings.

## Each round

Start a fresh agent or a new conversation that has seen nothing of the work. Give it the brief below, with the three paths filled in, and nothing else. It does not get the source material, the conversation or the earlier rounds.

> You are reviewing a document written for one reader. You have not seen how it was written and you have no other information about its author or subject. Read three files in full before you write anything: the target, which says who reads this document and why ({TARGET_PATH}); the document, as plain text ({DOC_PATH}); and the style law, which is binding on every sentence ({STYLE_PATH}).
>
> Review it wearing two hats in turn. First, the reader named in the target. Decide whether this document does its job for them, and why. Find every thing that reader needs which the document does not answer with a concrete instance. Look for anything that reader would not understand, and any claim that reads as larger than its evidence. Note any place where the document disagrees with itself in scale or wording, and anything that departs from what a normal document of this kind looks like in a way that raises a question before the evidence is read.
>
> Second, the style law's auditor. Check every sentence and name the rule each fault breaks. Watch especially for fronted noun phrases and thesis openers, "I [verb] the [thing] that [did something]", stacked reduced relatives, absolute constructions, sentences without a finite verb, rhetorical triplets, antithesis in any form, mannered metaphor, "under" in any sense but physically beneath, and runs of more than two sentences beginning with the same word.
>
> Rules: do not rewrite the document or edit any file. Never suggest adding facts or experience; where something is unanswered, say what kind of evidence would answer it. Never suggest disclosing a gap or a weakness. Quote the exact words for every finding. Keep it under 900 words.
>
> Return exactly three parts. VERDICT: does it do its job, yes or no; a score out of 10; one sentence of reason. FINDINGS: numbered, most severe first, at most 20. Each finding gives severity (high, medium or low) | location | exact quote | category | why, in one sentence | direction, in one sentence. KEEP: the three strongest things in the document, so nobody cuts them.

## Triage

Deal with every finding in one of three ways:

- **Accept it.** Make the change, and check that the change is still true against the source record.
- **Reject it with a reason**, in one line.
- **Turn it into a question for the person.**

Four rules hold whatever the reviewer says:

1. **A reviewer never adds a fact.** "Mention your budget" becomes a question, never a sentence.
2. **The person's rulings outrank any reviewer** on length, on what to confess, on what to leave out, and on wording they have approved.
3. **A reviewer that asks for a banned device is wrong.** Examples are a gap confessed or a slogan added. Reject it and cite the rule.
4. **"Keep" items are protected** unless the person says otherwise.

After applying the changes, run `magnify-slop-check` again. Re-check any hard limits too: pages, characters, word counts.

## When to stop

Stop when a round returns no high or medium finding, or after the third round. More rounds after that mostly trade one reviewer's taste for another's.

## Hand over

Give the person four things:

- the document
- the verdicts and scores, round by round
- a short numbered list of the decisions only they can make
- the findings kept against the reviewers, each with a one-line reason

Record each round in the document's version note. That record is how the next draft avoids the same faults.
