#!/usr/bin/env python3
"""Magnify slop check: a mechanical first pass over a draft before a human or a cold reviewer reads it.

Usage:
    python slop_check.py DRAFT [--bans BANS_FILE] [--strict]

DRAFT may be .md, .txt or .docx (.docx needs python-docx: pip install python-docx).
BANS_FILE is optional: one regular expression per line, with an optional label after " ## ".
Lines starting with # are comments. Use it for the person's own banned words and phrases.

Findings:
    FAULT     a banned device; fix it or have a reason
    ADVISORY  worth a look; often right, sometimes not (repeated numbers, verbless sentences)

Exit code: 1 if any FAULT is found (or any finding at all with --strict), else 0.
The checker catches what a pattern can catch. Rhythm, composition fraud and relevance need a reader:
run magnify-cold-review after this.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

# (pattern, label). Case-insensitive. Extend with --bans rather than editing here.
FAULTS = [
    (r"—", "em dash"),
    (r"\bnot (?:just |only |merely |simply )?[\w' ,-]{1,40}?,? but\b", "antithesis: not X but Y"),
    (r"\brather than\b", "antithesis: rather than"),
    (r"\bless (?:a|an) [\w -]{1,30} than\b", "antithesis: less X than Y"),
    (r"\bis (?:what|how|where|the one|the thing|the work) (?:I|we)\b", "fronted noun phrase: X is what I Y"),
    (r"\bhaving (?:\w+ed|run|built|led|written|made|taken|held|grown|set|kept|won)\b", "absolute construction: having done"),
    (r"\bwith [\w ]{1,30} (?:held|maintained|kept|intact|in place|unchanged)\b", "absolute construction: with X held"),
    (r"\bunder (?:a |the |my |its |our |their |his |her )?(?:\w+ )?(?:governance|controls?|standards?|accountability|budget|brief|policy|policies|review|audit|management|supervision|leadership|framework)\b", "metaphorical 'under'"),
    (r"\boperating system\b", "'operating system' (a metaphor unless it means software)"),
    (r"\b(?:delve|delving)\b", "assistant vocabulary"),
    (r"\bleverag(?:e|es|ed|ing)\b", "assistant vocabulary"),
    (r"\b(?:seamless(?:ly)?|robust|world-class|best-in-class|cutting-edge|game-?changer|synerg(?:y|ies))\b", "self-certifying or stock adjective"),
    (r"\b(?:passionate|proven track record|results-driven|dynamic professional)\b", "self-certifying phrase"),
    (r"\b(?:elevate|elevating|unlock(?:s|ing)? the power|navigate the complexities|in today's fast-paced)\b", "assistant vocabulary"),
    (r"\b(?:landscape|ecosystem|tapestry|realm)\b", "assistant vocabulary (check it is literal)"),
    (r"\badjacen(?:t|cy)\b", "assistant vocabulary: say the relation"),
    (r"\b(?:both|other) sides? of the table\b", "stock phrase: say which sides"),
    (r"\b(?:earns? its (?:place|keep)|does the (?:heavy lifting|work)|moves the needle|at the end of the day)\b", "mannered phrase"),
    (r"\b(?:strong|trump|wild|calling) card\b|\bcards? (?:to play|on the table)\b", "mannered phrase: card"),
    (r"\b(?:genuinely|truly|really|deeply|incredibly)\b", "intensifier"),
    (r"\b(?:plainly|candidly|simply put|to be clear|frankly)\b", "use-mention: show it, don't say it"),
    (r"\bit'?s worth noting\b|\bit is worth noting\b|\bimportantly,", "throat-clearing"),
    (r"\b(?:the challenge|the problem|the role|the need) (?:your|the) (?:brief|posting|job description) (?:describes|names|sets out)\b", "performative syntax: pointing at the reader's document"),
]

ADVISORY_VERBS = re.compile(
    r"\b(?:am|is|are|was|were|be|been|being|has|have|had|do|does|did|will|would|can|could|should|may|might|must|shall|"
    r"\w+ed|ran|run|runs|built|builds?|wrote|writes?|led|leads?|made|makes?|took|takes?|held|holds?|grew|grows?|set|sets|"
    r"kept|keeps?|went|goes|came|comes?|said|says?|gave|gives?|got|gets?|saw|sees?|found|brought|brings?|cut|cuts|paid|pays?|"
    r"won|wins?|lost|loses?|met|meets?|taught|teaches|told|tells?|felt|feels?|began|begins?|spent|spends?|stood|stands?|"
    r"sold|sells?|drew|draws?|knew|knows?|fell|falls?|rose|rises?|left|leaves?|put|puts|need|needs|use|uses|work|works|"
    r"serve|serves|help|helps|want|wants|start|starts|show|shows|mean|means|cover|covers|include|includes|seem|seems|"
    r"ask|asks|tell|let|lets|give|keep|hold|bring|stop|stops|move|moves|live|lives|speak|speaks|spoke|read|reads|"
    r"send|sends|add|adds|check|checks|fix|fixes|find|finds|offer|offers|raise|raises|try|tries|call|calls|quote|quotes|"
    r"name|names|state|states|open|opens|close|closes|leave|drop|drops|mark|marks|write|say|go|make|take|see|look|looks|"
    r"zip|copy|paste|outrank|outranks|install|upload|pass|returns?|remove|removes|replace|replaces|review|reviews|suggest|"
    r"suggests|deal|deals|reject|rejects|accept|accepts|turn|turns|becomes?|became|trade|trades|mention|mentions|list|lists|"
    r"match|matches|sort|sorts|choose|chooses|chose|decide|decides|explain|explains|describe|describes|compare|apply|applies|"
    r"export|exports|finish|finishes|record|records|draft|drafts|answer|answers|own|owns|lead|manage|manages|report|reports|"
    r"matter|matters|happen|happens|happened|depend|depends|belong|belongs|exist|exists|collect|collects|prefer|prefers|"
    r"label|labels|contact|contacts)\b",
    re.I,
)

CLEVELAND = re.compile(r"\b(?:I|we) (?:built|created|wrote|designed|led|ran|launched|made|developed|founded) the [\w-]+(?: [\w-]+){0,3} (?:that|which|who)\b", re.I)


def load_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        try:
            from docx import Document
        except ImportError:
            sys.exit("python-docx is needed for .docx files: pip install python-docx")
        doc = Document(str(path))
        parts = [p.text for p in doc.paragraphs]
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    parts.extend(p.text for p in cell.paragraphs)
        return "\n".join(parts)
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in (".md", ".markdown"):
        text = re.sub(r"```.*?```", " ", text, flags=re.S)       # code blocks
        text = re.sub(r"`[^`]*`", " ", text)                       # inline code
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)      # links: keep the words
        text = re.sub(r"^\s{0,3}#{1,6} .*$", " ", text, flags=re.M)  # headings
        text = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", text, flags=re.M)  # list markers
        text = re.sub(r"^\s*>\s?", "", text, flags=re.M)          # quotes
        text = re.sub(r"[*_]{1,3}", "", text)                      # emphasis
        text = re.sub(r"^\|.*\|$", " ", text, flags=re.M)         # tables
    return text


def load_bans(path):
    bans = []
    if not path:
        return bans
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        pattern, _, label = line.partition(" ## ")
        bans.append((pattern.strip(), label.strip() or "the person's own ban"))
    return bans


def sentences(text):
    flat = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])", flat) if s.strip()]


def context(text, start, end, width=45):
    left = max(0, start - width)
    return text[left:end + width].replace("\n", " ").strip()


def repeated_numbers(text):
    months = "January|February|March|April|May|June|July|August|September|October|November|December"
    text = re.sub(rf"\b\d{{1,2}}(?:st|nd|rd|th)? (?:{months})\b|\b(?:{months}) \d{{1,2}}\b", " ", text)  # dates are not receipts
    found = re.findall(r"(?<![\w.])(?:[$£€]\s?)?\d[\d,]*(?:\.\d+)?(?:%|m|k|bn)?", text)
    found = [n.rstrip(",.") for n in found]
    found = [n for n in found if len(re.sub(r"\D", "", n)) >= 2]
    found = [n for n in found if not re.fullmatch(r"(?:19|20)\d\d", n) and n not in ("24", "10")]
    return {n: c for n, c in Counter(found).items() if c > 1}


def main():
    parser = argparse.ArgumentParser(description="Magnify slop check")
    parser.add_argument("draft")
    parser.add_argument("--bans", help="file of extra banned patterns, one per line")
    parser.add_argument("--strict", action="store_true", help="exit 1 on advisories too")
    args = parser.parse_args()

    path = Path(args.draft)
    text = load_text(path)
    faults, advisories = [], []

    for pattern, label in FAULTS + load_bans(args.bans):
        for m in re.finditer(pattern, text, flags=re.I):
            if re.match(r"\.\w", text[m.end():m.end() + 2]):
                continue  # part of a name such as Elevate.Tech or Seamless.ai
            faults.append(f"FAULT     {label}: ... {context(text, m.start(), m.end())} ...")

    sents = sentences(text)

    cleveland = [s for s in sents if CLEVELAND.search(s)]
    if len(cleveland) > 2:
        for s in cleveland:
            faults.append(f"FAULT     object with a career ({len(cleveland)} in the document; two at most): {s[:110]}")

    # Runs of same-word openers, counted within each paragraph (list items are separate paragraphs).
    for paragraph in text.splitlines():
        run_word, run = None, []
        for s in sentences(paragraph) + [""]:
            first = re.match(r"[\"'(]*([A-Za-z']+)", s)
            word = first.group(1).lower() if first else None
            if word and word == run_word:
                run.append(s)
                continue
            if len(run) >= 3:
                faults.append(f"FAULT     {len(run)} sentences in a row begin with '{run_word}': {run[0][:70]} ...")
            run_word, run = word, [s]

    for s in sents:
        if len(s.split()) >= 7 and not ADVISORY_VERBS.search(s) and not s.endswith(":"):
            advisories.append(f"ADVISORY  no finite verb found (a menu, not a sentence?): {s[:110]}")

    for number, count in sorted(repeated_numbers(text).items(), key=lambda x: -x[1]):
        advisories.append(f"ADVISORY  {number} appears {count} times (once is usually enough)")

    for line in faults + advisories:
        print(line)
    print(f"\n{len(faults)} fault(s), {len(advisories)} advisory note(s) in {path.name}.")
    if faults or (args.strict and advisories):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
