---
name: deslop
description: "De-slop prose: write and edit content free of the tells catalogued in Wikipedia's Signs of AI writing (inflated significance, '-ing' analysis tails, AI vocabulary, 'not just X but Y', reflexive triplets, chatbot leftovers). Use whenever writing or editing prose meant for readers (blog posts, articles, newsletters, social posts, product or landing-page copy, emails, bios, docs), and whenever the user says text sounds like AI or asks to humanize, de-slop, or clean up a draft."
---

# De-slop

Language models regress to the mean. Specific, unusual facts get smoothed into generic, positive statements that could describe anything, and the statements get louder to compensate: "inventor of the first train-coupling device" becomes "a revolutionary titan of industry". [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) catalogues the marks this leaves. Nearly every tell in it is the same failure: a sentence asserting a verdict where a fact should be.

So the fix is *specific*, never *synonym*. Swapping "underscores" for "emphasizes" keeps the empty move and only hides it. Fix the move: put the fact in, or cut the sentence.

Script paths below are relative to this skill's directory.

## Writing

Draft from the targets below. Leave `references/signs.md` unread until the review pass: reading a list of phrases to avoid before drafting primes exactly those phrases.

- Lead with the concrete: names, numbers, dates, what happened, what it does. Let the reader judge significance.
- Plain verbs: *is, are, has, was; wrote, used, moved, tried*.
- State relationships outright: "was CEO of", "taught physics at".
- Name the source and match the real count: one reviewer is one reviewer.
- Commit where the claim holds ("was the first", "is the only"); qualify where it doesn't ("tends to", "perhaps").
- Group in whatever number is true. Two reasons is a fine number of reasons.
- Use one name for one thing, and repeat it.
- Mix sentence lengths and punctuation: commas, colons, parentheses, semicolons, the odd dash.
- Format to the content: lists only for parallel items, sentence-case headings, bold rarely.
- Stop when the content stops: no recap, no challenges-and-outlook coda, no offer of more help.

Persuasive copy still persuades, with specifics: "settles in 4 hours instead of 3 days" beats "seamless, lightning-fast payments".

Then run the review pass on the draft.

## Review pass

Applies to every draft, whether written under this skill or handed over by the user.

1. Save the text to a file if it isn't one, and scan it: `python3 scripts/scan.py draft.md`. The scanner catches listed words and recognizable shapes. It misses a vague attribution or empty verdict phrased in fresh words, so it is the first sweep, not the review.
2. Read `references/signs.md` and check the text against every category in it, including categories the scanner reported nothing for.
3. Rewrite each hit by fixing the move behind it; each category in `signs.md` gives the fix. A hit stays only when it is earned: the word is literal ("a landscape painting"), or the claim is specific and sourced.
4. Take specifics only from the source material, the user, or verifiable fact. A vague sentence with no fact behind it gets deleted. Where the piece genuinely needs the missing fact, mark the gap inline as `[needs: …]` and list it for the user. An invented statistic replacing a vague claim trades a style problem for a falsehood.
5. Re-scan. The pass is done when every remaining hit is one deliberately kept and every category in `signs.md` has been checked.

Keep the author's voice, register, and structure; de-slopping is not a rewrite into a house style. The overcorrection tells at the end of `signs.md` (no dashes at all, every sentence 8 to 20 words, synonym rotation) are tells too.

## Output

- Writing: the finished piece, plus any `[needs: …]` gaps.
- Editing: the cleaned text, then a short note naming the moves fixed (e.g. "cut 4 significance claims; replaced 'associated with' with the actual roles"), any `[needs: …]` gaps, and any hits kept with the reason.

## Keeping the catalog current

The Wikipedia page changes as models change; each model generation brings its own vocabulary. `source/` holds a snapshot of the page (revision in `source/REVISION`) and the scanner's watch list built from it.

`python3 scripts/refresh.py` pulls the live page, rebuilds `source/words-to-watch.json`, and reports sections and watch phrases added or removed. `--check` reports without writing; it exits 0 when up to date, 1 when only the page text changed, 2 when sections or watch phrases changed, and 3 when the fetch failed. A reported change means `references/signs.md` needs review against the new sections in `source/signs.wiki`: add a category for a new general-writing tell, revise one whose description changed, update the revision line at the top, and skip tells about Wikipedia's own machinery (citations, wikitext, edit summaries, draft review).
