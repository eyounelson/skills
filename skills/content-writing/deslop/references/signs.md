# Signs of AI writing: review catalog

Distilled from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), revision 1383697236 (2026-11-04). The `WP:` shortcut after each heading names the matching section of the page, for looking up more examples in `source/signs.wiki`. Tells about Wikipedia's own machinery (citation markup, edit summaries, draft submissions) are left out.

Check the text against every category. Each one gives the tell, what it looks like, and the fix. One instance of a tell rarely matters; density does. These tells cluster: where there is one, look for others nearby.

## Contents

- Content: inflated significance, name-dropped coverage, source-describing, superficial analysis, vague connection, weasel attribution, challenges-and-outlook, "X and Y" headings
- Language: AI vocabulary, copula avoidance, negative parallelism, rule of three, defining the label
- Style and formatting
- Chatbot leftovers: collaborative talk, hedging disclaimers, placeholders
- Older tells still worth catching: puffery, section summaries, em dashes, elegant variation
- Calibration: what is not a tell, what human prose has, overcorrection

---

## Content

### Inflated significance and legacy (WP:AILEGACY)

The text claims that an ordinary fact marks, represents, or contributes to something larger, even for etymology or population figures. Sometimes it admits the subject is minor and then claims importance anyway.

Looks like: *stands/serves as, is a testament/reminder, a pivotal/crucial/key role or moment, underscores its importance, reflects broader trends, marking a shift, setting the stage for, evolving landscape, indelible mark, deeply rooted*; "has sparked debate about…", "raises questions about…"; "though it saw limited use, it contributes to the broader history of…"; "this distinction matters because…".

Instead: state the fact and stop. If the significance is real, show it with a second fact (what changed, for whom, by how much). "Founded in 1989, marking a pivotal moment in regional statistics" becomes "Founded in 1989; before that, Spain's national institute produced Catalonia's statistics."

### Name-dropped coverage and recognition (WP:AIATTR)

The text proves importance by listing where the subject was covered and what kind of outlets those are, rather than saying what the coverage reported.

Looks like: *featured/profiled/cited in, independent coverage, national media outlets, tech/business/trade publications, a leading expert, maintains an active social media presence*; "has been featured in Wired, Vogue, and other prominent outlets".

Instead: report what a source said, attributed to it. "Wired called it the first X to do Y" carries information; "featured in Wired" carries none.

### Describing the source instead of using it (WP:AIIDENTIFY)

The text dwells on how a website, database, or record *identifies* or *lists* the subject.

Looks like: "his personal website identifies him as…", "records list her as…", "was identified by [source] as…", "his professional profile lists…".

Instead: state the fact ("He is a retired civil servant") and attribute only when the claim is contested or self-reported ("He says he…").

### Superficial analysis (WP:SUPERFICIAL)

A present-participle clause tacked onto the end of a factual sentence, editorializing about what the fact means. Newer models pin these verdicts on named sources that never said them.

Looks like: "…, highlighting/underscoring/emphasizing its…", "…, reflecting/symbolizing…", "…, contributing to the…", "…, fostering/cultivating…", "…, ensuring…", "…, enhancing…", *valuable insights, aligns/resonates with*.

Instead: delete the clause. If the meaning matters, make it its own sentence with its own evidence. "The station has 6 platforms, reflecting its continued relevance" becomes "The station has 6 platforms."

### Vague connection or association (WP:AICONNECT)

Two things are said to be "associated with" or "connected to" each other instead of stating the relationship.

Looks like: *associated with, in connection with, connected to, in association with*; "became associated with musical education in Knokke"; "ventured into politics as a candidate".

Instead: name the relationship. "Taught violin in Knokke." "Was a candidate."

### Weasel attribution and inflated consensus (WP:AIWEASEL)

Opinions attributed to unnamed authorities, one source presented as many, or "such as" before a list that is actually complete.

Looks like: *experts argue, observers have noted, industry reports suggest, some critics argue, researchers and conservationists, several publications* (backed by one); "such as X and Y" when X and Y are all there is.

Instead: name who said it and match the real count. "A 2024 Gartner report estimates…" or "One reviewer, at The Verge, wrote…". Drop "such as" when the list is complete.

### Challenges-and-outlook formula (WP:FACESCHALLENGES)

A closing section or paragraph that opens "Despite its [praise], X faces several challenges…" and ends with a vaguely upbeat assessment or speculation about future initiatives. The tell is the rigid formula, not any mention of difficulty.

Looks like: *despite its… faces several challenges, despite these challenges, continues to thrive/evolve, future outlook, future prospects, positions it as a critical…*.

Instead: put each real problem where it belongs in the piece, stated with specifics (what, since when, how big). End on the last real point.

### "X and Y" headings, "Awards and recognition" (WP:AISIGNS "Awards and recognition")

Headings built as pairs ("Challenges and Legacy", "Impact and Recognition"), and a recognition section, are near-ubiquitous in generated articles.

Instead: headings that name the actual content ("2023 funding round", "Why settlements take 3 days"). Fold awards into the narrative where they happened.

## Language

### AI vocabulary (WP:AIVOCAB)

Specific words that LLMs overuse, which co-occur. Take the list literally: an overused word does not make its synonyms suspect, and swapping one for a synonym fixes nothing if the sentence is still empty.

By era (the most recent era is the one current models produce):

- 2023 to mid-2024: *additionally* (opening a sentence), *boasts* (meaning "has"), *bolstered, crucial, delve, emphasizing, enduring, garner, intricate/intricacies, interplay, key, landscape* (abstract), *meticulously, pivotal, underscore, tapestry* (abstract), *testament, valuable, vibrant*
- Mid-2024 to mid-2025: *align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant*
- Mid-2025 to mid-2026: *emphasizing, enhance, highlighting, showcasing*, plus the coverage words above
- Mid-2026 on: *challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally*, with sentences held to roughly 8 to 20 words and heavy use of plain periods and commas
- Any era: *deep dive, robust, meticulous, showcase*; Grok also overuses *causal, empirical, correlate*

Instead: usually the sentence carrying the word is the problem (a significance claim, a participle tail). Fix that, and the word goes with it. Where the sentence is sound, use the plain word: *has* for *boasts*, *shows* or nothing for *underscores*.

### Copula avoidance (WP:AINOCOPULA)

"Is" and "are" replaced by *serves as, stands as, functions as, represents, marks*, and "has" by *boasts, features, offers, maintains*. AI copyedits "improve" text this way.

Instead: "Gallery 825 is LAAA's exhibition space. It has four rooms." Not "serves as… features four separate spaces".

### Negative parallelism (WP:AIPARALLEL)

Framing that corrects a misconception nobody held. Three forms:

- Not just X, but Y: "not only dismissive but also harsh", "it doesn't just undermine X; it questions Y", "isn't just sourcing, it's framing".
- Not X, but Y: "not a mirror but a portal", "This isn't X, it's Y", "no X, no Y, just Z".
- Y rather than X (common in recent output): "a bridge between tools rather than a replacement for them", "rather than simply retelling the legend, the film…".

Instead: state Y. Mention X only when a reader would plausibly believe X, and then say who believes it.

### Rule of three (WP:RO3)

Reflexive triplets, of adjectives ("trust, transparency, and inclusion") or of phrases, used to make thin analysis look complete.

Instead: list what is true, in whatever number. One precise adjective beats three vague ones. Two reasons is a fine number of reasons.

### Defining the label instead of the subject

Openings that treat a title or topic name as an entity: "Catchment area refers to…", "The 'List of songs about Mexico' is a curated compilation…".

Instead: start with the subject itself. "A hospital's catchment area is the region its patients come from."

## Style and formatting (WP:AISIGNS Style)

- Title Case Headings: use sentence case unless the publication's style says otherwise.
- Bold scattered through prose: bold almost nothing; let sentence structure carry emphasis.
- Inline-header lists ("- **Speed**: Payments settle quickly"): write a paragraph when the items are connected; keep a list only when the content is genuinely parallel items.
- Emoji at the start of headings or list items: remove.
- Curly quotes and apostrophes where the surrounding text uses straight ones: match the destination.
- Markdown in a destination that doesn't render it (asterisks in an email, `##` in a CMS field): use the destination's formatting.

## Chatbot leftovers

### Collaborative talk (WP:COLLABCOMM)

Text addressed to the person who prompted the model, pasted into the content.

Looks like: *Certainly!, Of course!, You're absolutely right!, I hope this helps, Would you like…, let me know, is there anything else, here is a…, a more detailed breakdown*; "In this section, we will discuss…"; advice to verify before publishing.

Instead: delete. The content starts with content.

### Hedging disclaimers (WP:AIDISCLAIMER)

Drawing attention to gaps instead of filling or omitting them. Three generations:

- Didactic (2023–24): "It's important to note…", "It is crucial to differentiate…", "It's important to remember…".
- Source gaps (2024–25): "while specific details are limited", "not widely documented", "based on available information", "in the provided sources"; for people, "maintains a low profile". Often followed by what the information "likely" is, which is speculation.
- Corrective framing (mid-2026 on): "should be treated as [tradition] rather than [fact]", "does not by itself establish…", "should not be confused with…".

Instead: say what is known, attributed. Leave out what is not known. A caveat the reader needs gets one plain sentence ("The company has not published revenue figures") with no lecture.

### Placeholders and knowledge cutoffs (WP:AIPLACEHOLDER, WP:AICUTOFF)

Unfilled template slots and model self-reference.

Looks like: *[Your Name], [Describe the specific section…], (Add your URL here), 2026-xx-xx*; "as of my last knowledge update"; "as an AI language model".

Instead: fill the slot with real information, or ask the user for it. Never ship a bracket.

## Older tells still worth catching

These are less common in current model output but still appear, especially in marketing copy and in output from older or cheaper models.

### Promotional puffery (WP:AIPUFFERY)

Travel-brochure and press-release tone.

Looks like: *nestled, in the heart of, boasts a, vibrant, rich (heritage/history), profound, groundbreaking, renowned, diverse array, natural beauty, commitment to, exemplifies, seamlessly*; "offers visitors a fascinating glimpse into…".

Instead: the concrete detail the adjective was standing in for. Marketing copy may persuade, and persuades best with specifics: a number, a named customer, a before-and-after.

### Section summaries (WP:CONCLUSION)

Paragraphs or pieces ending by restating themselves: *In summary, In conclusion, Overall, Ultimately*.

Instead: end on the last new thing. Long documents may have a real summary at the top for skimmers; that is different from a recap at the bottom.

### Em dashes (WP:AIDASH)

Em dashes used formulaically to punch up clauses, typically with spaces around them (" — "), where a human would use a comma, colon, or parentheses.

Instead: use the punctuation the sentence needs. An occasional dash is fine. Removing every dash and leaving only commas and periods is its own tell (see Overcorrection).

### Elegant variation (WP:AIELEVAR)

Rotating synonyms to avoid repeating a noun: "the artists… non-conformist creators… these like-minded painters".

Instead: repeat the right word. Readers track one name for one thing.

## Calibration

### Not tells (WP:AISIGNS "Ineffective indicators")

Leave these alone; "fixing" them damages good writing:

- Correct grammar and spelling.
- A mix of casual and formal registers.
- Formal or academic vocabulary in general (only the specific listed words are tells).
- Transition words in isolation (*consequently, notably*); only a formulaic run of them is a sign.
- Prose that is merely plain.

### What human prose has (WP:HUMANSIGNS)

Patterns measured as more common in human writing than in generated text. Use them as targets:

- Simple *is/has* phrases: "there is a", "it has a".
- Plain verbs over stiff synonyms: *wrote* not *authored*, *moved* not *relocated*, *used* not *utilized*, *tried* not *attempted*, *died* not *passed away*.
- Definite claims where true: "one of the best", "is the only", "was the first".
- Qualifiers and intensifiers: *very, perhaps, tends to*.
- The occasional wordy construction: *in order to, as a result of, the fact that*.

### Overcorrection

The newest tells come from models trained to avoid the old ones. Avoid trading one set for another:

- No dashes, colons, semicolons, or parentheses anywhere; only periods and commas.
- Every sentence 8 to 20 words long. Vary length: some short, some long.
- Synonym rotation to dodge a word on the list.
- Deleting so much that the piece loses facts the reader needed.
