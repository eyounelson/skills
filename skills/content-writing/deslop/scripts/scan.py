#!/usr/bin/env python3
"""Flag Signs-of-AI-writing tells in a draft.

Advisory: a hit marks a place to look, not a verdict. The watch phrases come from
source/words-to-watch.json (rebuilt by refresh.py); the structural checks below
cover tells the page describes without a word list.

Usage:
  scan.py draft.md          scan a file ("-" reads stdin)
  scan.py draft.md --all    also list low-signal hits, which are otherwise only counted
"""

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
WATCH_LIST = SKILL_DIR / "source" / "words-to-watch.json"

# Watch phrases that ordinary prose uses all the time. They count toward density
# but are only listed with --all.
LOW_SIGNAL = {
    "such as", "key", "here is a", "let me know", "is listed in", "refers to",
    "associated with", "connected with/to", "boasts/features/maintains/offers [a]",
    "Overall", "challenge", "clearer", "matters", "practical", "steady", "echoed",
    "valuable", "robust", "rich", "featuring", "I'm sorry", "contributing to ...",
    "ensuring ...", "enhancing ...", "encompassing ...",
}

WILDCARD = r"[\w'’-]+(?:\s+[\w'’-]+){0,4}?"
SUFFIXES = r"(?:s|es|d|ed|ing|ly)?"

# Tells the page describes by shape rather than by word list.
STRUCTURAL = [
    ("Superficial analysis (-ing tail)",
     r",\s+(?:highlighting|underscoring|emphasizing|reflecting|symbolizing|showcasing|contributing|fostering|"
     r"ensuring|cementing|solidifying|marking|demonstrating|illustrating|creating|offering|enhancing|"
     r"cultivating|signaling|signalling|reinforcing|embodying|positioning)\b"),
    ("Negative parallelism (not just X, but Y)",
     r"\bnot\s+(?:only|just|merely|simply)\b[^.!?]{0,100}?\bbut\b|\b(?:isn't|aren't|wasn't|doesn't|don't)\s+just\b"),
    ("Negative parallelism (not X, it's Y)",
     r"\b(?:it's|it is|this is|that's|that is|isn't|is not|wasn't|was not)\s+not\b[^.!?]{0,80}?[,;:—–]\s*(?:it's|it is|but|rather)\b"
     r"|\b(?:isn't|is not|wasn't|was not|aren't|are not)\s+[^.!?,;]{1,60}?\s*[—–;]\s*(?:it's|it is|they're|it was)\b"),
    ("Negative parallelism (no X, no Y, just Z)",
     r"\b(?:no|not)\s+[\w'-]+(?:\s+[\w'-]+)?,\s+(?:no|not)\s+[\w'-]+[^.!?]{0,60}?\bjust\b"),
    ("Y rather than X", r"\brather than\b"),
    ("Didactic disclaimer",
     r"\b(?:it(?:'s| is) (?:important|crucial|essential|worth) (?:to (?:note|remember|recognize|consider)|noting))\b"
     r"|\bshould not be confused with\b|\bworth noting\b"),
    ("Section summaries", r"(?im)^\W*(?:in summary|in conclusion|to sum up|in short|ultimately|overall)\b"),
    ("Outline-like conclusions about challenges and future prospects",
     r"\bdespite (?:its|their|these|this|the)\b[^.!?]{0,80}?\bchallenges?\b|\b(?:faces|face|facing) (?:several |many |numerous |significant )?challenges\b"
     r"|\b(?:future (?:outlook|prospects|directions))\b|\bcontinues? to (?:thrive|evolve)\b"),
    ("Chatbot leftovers",
     r"\b(?:great question|absolutely right|happy to help|hope this helps|feel free to)\b|^\s*(?:certainly|of course|sure)!"
     r"|\bas an ai\b|\bmy (?:last )?(?:knowledge|training) (?:update|cutoff)\b"),
    ("Placeholder text", r"\[(?:your|insert|add|describe|link|name|date|company|[A-Z][a-z]+ [A-Z][a-z]+)[^\]]{0,60}\](?!\()|\b(?:xx|XX)-(?:xx|XX)\b"),
    # A bolded link is an index entry ("- **[name](path)**: ..."), not an inline header.
    ("Inline-header list item", r"^\s*(?:[-*•]|\d+\.)\s+\*\*[^*\[]{1,60}\*\*\s*:"),
    ("Emoji leading a heading or list item",
     r"^\s*(?:#{1,6}\s*|[-*•]\s+)?[\U0001F300-\U0001FAFF☀-➿⭐✅]"),
    ("Spaced em dash", r"\s—\s"),
]

SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "with"}


def phrase_to_regex(phrase):
    """Compile a 'Words to watch' entry, keeping the page's notation:
    a/b alternates words, [x/y] alternates phrases, [placeholder] matches a few
    words, and ... joins fragments that sit apart in one sentence."""
    fragments = [f for f in re.split(r"\.{3,}|…", phrase) if re.search(r"[A-Za-z]", f)]
    parts = []
    for fragment in fragments:
        slots = []

        def hold(match):
            inner = match.group(1)
            if "/" in inner:
                options = [r"\s+".join(map(re.escape, option.split())) for option in inner.split("/")]
                slots.append("(?:" + "|".join(options) + ")")
            else:
                slots.append(WILDCARD)
            return f"\x00{len(slots) - 1}\x00"

        held = re.sub(r"\[([^\]]*)\]", hold, fragment.strip(" ,"))
        tokens = []
        for token in held.split():
            options = []
            for option in token.split("/"):
                slot = re.fullmatch(r"\x00(\d+)\x00", option)
                options.append(slots[int(slot.group(1))] if slot else re.escape(option))
            tokens.append(options[0] if len(options) == 1 else "(?:" + "|".join(options) + ")")
        pattern = r"\s+".join(tokens)
        if len(tokens) == 1 and re.fullmatch(r"[A-Za-z]+(?:/[A-Za-z]+)*", fragment.strip()):
            # A bare word on the page stands for its inflections too (underscore -> underscored).
            stems = [w[:-1] + "(?:e|es|ed|ing)" if w.endswith("e") else w + SUFFIXES
                     for w in fragment.strip().split("/")]
            pattern = "(?:" + "|".join(stems) + ")"
        parts.append(pattern)
    return re.compile(r"(?<![\w])" + r"[^.!?\n]{0,80}?".join(parts) + r"(?![\w])", re.IGNORECASE)


def load_watch_list():
    if not WATCH_LIST.exists():
        sys.exit(f"Missing {WATCH_LIST}. Run scripts/refresh.py first.")
    data = json.loads(WATCH_LIST.read_text())
    compiled = {}
    for entry in data["entries"]:
        phrase = entry["phrase"]
        if phrase not in compiled:
            compiled[phrase] = {"regex": phrase_to_regex(phrase), "sections": []}
        compiled[phrase]["sections"].append(entry["section"])
    return data, compiled


def prose_lines(text):
    """Blank out fenced and inline code so line numbers stay true."""
    lines, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            lines.append("")
            continue
        lines.append("" if in_fence else re.sub(r"`[^`]*`", "", line))
    return lines


def context(line, start, end, width=50):
    left = line[max(0, start - width):start].lstrip()
    right = line[end:end + width].rstrip()
    return f"…{left}[{line[start:end]}]{right}…"


def title_case_headings(lines):
    hits = []
    for number, line in enumerate(lines, 1):
        match = re.match(r"^\s*#{1,6}\s+(.+)$", line)
        if not match:
            continue
        words = [w for w in re.findall(r"[A-Za-z][\w'-]*", match.group(1))[1:] if w.lower() not in SMALL_WORDS]
        if len(words) >= 2 and all(w[0].isupper() for w in words):
            hits.append((number, match.group(1).strip()))
    return hits


def rhythm(lines):
    prose = " ".join(line for line in lines if line.strip() and not re.match(r"^\s*(#|[-*•]|\d+\.)\s", line))
    words = re.findall(r"[\w'’-]+", prose)
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", prose) if re.search(r"\w", s)]
    lengths = [len(re.findall(r"[\w'’-]+", s)) for s in sentences]
    all_words = len(re.findall(r"[\w'’-]+", " ".join(lines)))
    return all_words, words, lengths


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help='draft to scan, or "-" for stdin')
    parser.add_argument("--all", action="store_true", help="list low-signal hits too")
    args = parser.parse_args()

    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text()
    lines = prose_lines(text)
    data, watch = load_watch_list()

    word_hits, seen = [], set()
    for phrase, item in watch.items():
        for number, line in enumerate(lines, 1):
            for match in item["regex"].finditer(line):
                key = (number, match.start(), match.end())
                if key in seen:
                    continue
                seen.add(key)
                word_hits.append((number, match, line, phrase, item["sections"][0], phrase in LOW_SIGNAL))
    word_hits.sort(key=lambda hit: (hit[0], hit[1].start()))

    def already_flagged(number, match):
        return any(n == number and m.start() < match.end() and match.start() < m.end() for n, m, *_ in word_hits)

    structural_hits = []
    for name, pattern in STRUCTURAL:
        regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        for number, line in enumerate(lines, 1):
            for match in regex.finditer(line):
                if not already_flagged(number, match):
                    structural_hits.append((number, match, line, name))
    structural_hits += [(n, None, h, "Title Case heading") for n, h in title_case_headings(lines)]
    structural_hits.sort(key=lambda hit: hit[0])

    print(f"Watch list: Wikipedia revision {data['revid']} ({data['timestamp'][:10]})\n")

    print("== Watch-list phrases ==")
    shown = [h for h in word_hits if args.all or not h[5]]
    for number, match, line, phrase, section, low in shown:
        flag = " (low signal)" if low else ""
        print(f"L{number:<4} [{section}] {phrase!r}{flag}\n      {context(line, match.start(), match.end())}")
    hidden = len(word_hits) - len(shown)
    if not shown:
        print("  none")
    if hidden:
        print(f"  + {hidden} low-signal hits (use --all to list)")

    print("\n== Structural tells ==")
    for number, match, line, name in structural_hits:
        detail = context(line, match.start(), match.end()) if match else line
        print(f"L{number:<4} [{name}]\n      {detail}")
    if not structural_hits:
        print("  none")

    total_words, prose_words, lengths = rhythm(lines)
    print("\n== Rhythm ==")
    per_100 = 100 * len(word_hits) / max(total_words, 1)
    print(f"words: {total_words} | watch-list hits: {len(word_hits)} ({per_100:.1f} per 100 words)")
    if len(lengths) >= 2:
        mean, spread = statistics.mean(lengths), statistics.pstdev(lengths)
        note = ""
        if len(lengths) >= 8 and spread < 5:
            note = "  <- uniform sentence length"
        print(f"sentences: {len(lengths)} | mean length: {mean:.1f} words | spread (stdev): {spread:.1f}{note}")
    dashes = text.count("—")
    print(f"em dashes: {dashes} ({1000 * dashes / max(total_words, 1):.1f} per 1000 words)")
    if len(lengths) >= 8 and dashes == 0 and not re.search(r"[;:()]", "\n".join(lines)):
        print("  no dashes, colons, semicolons or parentheses at all: punctuation may read flattened")
    triplets = len(re.findall(r"\b[\w'-]+(?:\s[\w'-]+){0,2},\s[\w'-]+(?:\s[\w'-]+){0,2},?\s(?:and|or)\s[\w'-]+", "\n".join(lines)))
    print(f"'X, Y, and Z' series: {triplets}")

    counts = Counter(section for *_, section, _ in word_hits) + Counter(name for *_, name in structural_hits)
    if counts:
        print("\n== Hits by category ==")
        for name, count in counts.most_common():
            print(f"  {count:>3}  {name}")


if __name__ == "__main__":
    main()
