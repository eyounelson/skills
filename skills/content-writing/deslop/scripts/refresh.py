#!/usr/bin/env python3
"""Pull the latest Wikipedia:Signs of AI writing and rebuild the scanner's watch list.

Writes into the skill's source/ folder:
  signs.wiki            raw wikitext of the current revision (for looking up examples)
  words-to-watch.json   every "Words to watch" phrase and AI-vocabulary era word, by section
  REVISION              revid and timestamp of the snapshot

Prints what changed since the previous snapshot: sections added or removed, and
watch-list phrases added or removed. references/signs.md is curated by hand, so a
reported change means an agent should review it against the new snapshot.

Usage:
  refresh.py           fetch, report, and write the new snapshot
  refresh.py --check   fetch and report only. Exit 0: up to date. Exit 1: the page
                       text changed (new examples, rewording). Exit 2: sections or
                       watch-list phrases changed, so references/signs.md needs review.
                       Exit 3: the fetch or parse failed.
"""

import argparse
import json
import re
import sys
import traceback
import urllib.parse
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = SKILL_DIR / "source"
API = "https://en.wikipedia.org/w/api.php"
TITLE = "Wikipedia:Signs of AI writing"
USER_AGENT = "deslop-skill/1.0 (content-writing skill; reads Wikipedia:Signs_of_AI_writing)"

# Top-level sections about Wikipedia's own machinery (citations, edit summaries,
# AfC drafts, wikitext) or about detection itself. Their tells don't carry over
# to general content writing, so their phrases stay out of the watch list.
SKIP_SECTIONS = {
    "Caveats",
    "Citations",
    "Comment-specific indicators",
    "Edit summaries",
    "Markup irregularities",
    "Miscellaneous",
    "Signs of human writing",
    "Ineffective indicators",
    "See also",
    "Notes",
    "References",
    "Further reading",
    "External links",
}

HEADING = re.compile(r"^(={2,4})\s*(.*?)\s*\1\s*$")
QUOTED = re.compile(r"(?<!')''(?!')(.+?)(?<!')''(?!')")
ERA = re.compile(r"^\*\s*'''(.+?)'''\s*(?:\((.*?)\))?\s*:(.*)$")


def fetch():
    params = urllib.parse.urlencode({
        "action": "query",
        "prop": "revisions",
        "titles": TITLE,
        "rvprop": "ids|timestamp|content",
        "rvslots": "main",
        "format": "json",
        "formatversion": "2",
    })
    request = urllib.request.Request(f"{API}?{params}", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.load(response)
    revision = data["query"]["pages"][0]["revisions"][0]
    meta = {"revid": revision["revid"], "timestamp": revision["timestamp"]}
    return meta, revision["slots"]["main"]["content"]


def strip_noise(wikitext):
    # Code samples and comments hold fake headings; refs hold citation noise.
    text = re.sub(r"<!--.*?-->", "", wikitext, flags=re.S)
    text = re.sub(r"<syntaxhighlight.*?</syntaxhighlight>", "", text, flags=re.S)
    text = re.sub(r"<ref[^>]*/>", "", text)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.S)
    return text


def clean_phrase(raw):
    phrase = re.sub(r"<[^>]+>", "", raw)
    phrase = phrase.replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", phrase).strip()


def parse(wikitext):
    """Return (headings, entries) from the page's wikitext."""
    headings = []
    entries = []
    top = sub = ""
    for line in strip_noise(wikitext).splitlines():
        match = HEADING.match(line)
        if match:
            level, title = len(match.group(1)), clean_phrase(match.group(2))
            if level == 2:
                top, sub = title, ""
            elif level == 3:
                sub = title
            headings.append(("  " * (level - 2)) + title)
            continue
        if top in SKIP_SECTIONS:
            continue
        section = sub or top
        historical = top == "Historical indicators"
        if "Words to watch:" in line:
            for raw in QUOTED.findall(line.split("Words to watch:", 1)[1]):
                phrase = clean_phrase(raw)
                if re.search(r"[A-Za-z]", phrase):
                    entries.append({"section": section, "phrase": phrase, "historical": historical})
            continue
        era = ERA.match(line)
        if era and "AI vocabulary" in section:
            label = clean_phrase(era.group(1))
            if era.group(2):
                label += f" ({clean_phrase(era.group(2))})"
            for raw in QUOTED.findall(era.group(3)):
                phrase = clean_phrase(raw)
                if re.search(r"[A-Za-z]", phrase):
                    entries.append({"section": f"AI vocabulary, {label}", "phrase": phrase, "historical": False})
    return headings, entries


def load_previous():
    path = SOURCE_DIR / "words-to-watch.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


UP_TO_DATE, TEXT_CHANGED, STRUCTURE_CHANGED, FAILED = 0, 1, 2, 3


def report(previous, meta, headings, entries):
    """Print what changed and return UP_TO_DATE, TEXT_CHANGED or STRUCTURE_CHANGED."""
    print(f"Live revision: {meta['revid']} ({meta['timestamp']})")
    if previous is None:
        print("No previous snapshot: writing the first one.")
        return STRUCTURE_CHANGED
    print(f"Snapshot revision: {previous['revid']} ({previous['timestamp']})")
    if previous["revid"] == meta["revid"]:
        print("Up to date.")
        return UP_TO_DATE

    old_headings, new_headings = set(previous["headings"]), set(headings)
    old_entries = {(e["section"], e["phrase"]) for e in previous["entries"]}
    new_entries = {(e["section"], e["phrase"]) for e in entries}

    def show(title, items):
        if items:
            print(f"\n{title}:")
            for item in sorted(items):
                print(f"  {item if isinstance(item, str) else f'[{item[0]}] {item[1]}'}")

    show("Sections added", {h.strip() for h in new_headings - old_headings})
    show("Sections removed", {h.strip() for h in old_headings - new_headings})
    show("Watch phrases added", new_entries - old_entries)
    show("Watch phrases removed", old_entries - new_entries)
    if old_headings == new_headings and old_entries == new_entries:
        print("\nPage text changed, but no section or watch-list changes (likely new examples or rewording).")
        return TEXT_CHANGED
    print("\nNext: review references/signs.md against these changes, reading the new"
          " sections in source/signs.wiki. Skip anything specific to Wikipedia's machinery.")
    return STRUCTURE_CHANGED


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report only; exit 1 on text changes, 2 on structural changes")
    args = parser.parse_args()

    meta, wikitext = fetch()
    headings, entries = parse(wikitext)
    status = report(load_previous(), meta, headings, entries)

    if args.check:
        sys.exit(status)
    if status == UP_TO_DATE:
        return

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    (SOURCE_DIR / "signs.wiki").write_text(wikitext)
    (SOURCE_DIR / "REVISION").write_text(f"{meta['revid']} {meta['timestamp']}\n")
    snapshot = {**meta, "headings": headings, "entries": entries}
    (SOURCE_DIR / "words-to-watch.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote snapshot {meta['revid']} with {len(entries)} watch phrases to {SOURCE_DIR}.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # An uncaught exception exits 1, which --check uses for "text changed".
        traceback.print_exc()
        sys.exit(FAILED)
