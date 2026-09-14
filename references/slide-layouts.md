# Layout library

Choose the layout by its communicative job. Use the CSS classes from the package; avoid building unrelated design systems. The 24-slide University Edition demo combines learning examples, synthetic research values, decision briefings and other clearly illustrative university scenarios. These recipes do not establish institutional policy or facts.

| Layout | HTML/CSS recipe | Guidance | Demo slide |
|---|---|---|---:|
| University cover | `.slide.cover.institutional-cover` → `.cover-layout` | One strong title, shared marks, concise context | 1 |
| Three-mode overview | `.grid-3` with `.stack.rule` | Three parallel modes, not three department identities | 2 |
| Purpose-selection table | `table` with real headers | Route by the audience's intended outcome | 3 |
| Learning section | `.slide.dark` → `.section-layout` | Large section number and clear transition | 4 |
| Worked example | `.grid-2.ratio-60` + table + `.panel.warm` | Given values, transformation and result | 5 |
| Learning activity | question + code + `details.answer` | Clear task; expanded answer must fit print | 6 |
| Research cover | `.slide.cover.dark` | Full wordmark on a white plaque | 7 |
| Evidence chart | `.bar-chart` + labels + takeaway | Units, baseline, source, uncertainty and synthetic labels | 8 |
| Interpretation / limits | `.grid-2` with panels | Separate observation from unsupported inference | 9 |
| Leadership section | `.slide.dark` → `.section-layout` | Frame the decision, not a classroom objective | 10 |
| Decision briefing | two panels + source/status line | Question, evidence needs, recommendation, decision sought | 11 |
| Options comparison | table + `.callout` | Benefits and trade-offs; no invented budgets | 12 |
| Partnership cover | `.slide.cover.institutional-cover` | Mutual interest and discussion status | 13 |
| Proposed workstreams | `.timeline` + `.callout` | Proposed scope, dependencies and next discussion | 14 |
| Status distinction | two panels + visible `.badge` | A proposal is not a signed commitment | 15 |
| Admissions cover | institutional cover + subtitle | Approved claims, not promotional guarantees | 16 |
| Applicant pathway | `.flow` with `.step` and `.arrow` | Verify the actual process; do not invent dates or links | 17 |
| Staff training | task/practice panels + question | Safe examples and reviewed procedures | 18 |
| Student-project cover | research cover + authorship label | Actual contribution without implying endorsement | 19 |
| Student evidence | `.grid-2` and `.rule` | Own contribution, evidence and limitations | 20 |
| Event programme | `.timeline` + status line | Confirm details or visibly mark drafts | 21 |
| Audience-specific copies | two panels + context labels | Hidden content review; labels are not access controls | 22 |
| Asset comparison | `.grid-3` + intact images | Natural aspect ratios and background requirements | 23 |
| Closing / action | branded cover + next action | Match the purpose, not a universal quiz/recap | 24 |

## Additional patterns

**Quote:** one short accurately attributed quotation, ample space, original source in a readable line. Do not invent quotes or present a paraphrase inside quotation marks.

**Scientific figure:** give the figure most of the slide, with one takeaway heading and a short source line. Split an unreadably dense multi-panel figure across multiple slides. Do not color-filter a scientific image to match the university palette.

**Comparison table:** generally 3–5 columns, no more than about 5 substantive rows at body scale. Split long tables by comparison dimension, keeping column headings and citations. These counts are practical starting points, not absolute content limits.

**References:** use 3–5 clearly readable citations per slide, or separate a reading bibliography from the speaker-led presentation. Never reduce source text to illegible decorative microtype.

**Reading-first deck:** use fewer transitions and more self-contained explanations. Expand with additional slides or a companion handout; do not place a page of prose into one slide. Explicitly distinguish supplementary appendix slides from the primary talk.


## Additional teaching recipes retained

**Learning objectives:** `.objective` with `.index` and short text. Use measurable verbs. For other purposes the same visual rows can express a purpose, evidence or next action without being called learning outcomes.

**Code trace:** `.grid-2` with `pre > code` and a small trace table. Use a tested excerpt, language/context and readable line lengths.

**Equation/calculation:** `.equation` with definitions and a units table. Define symbols and assumptions. Keep essential equations as real text where possible and inspect PDF glyphs.

**Recap:** `.grid-3` or a brief takeaway with a concluding question. Appropriate for teaching; use a decision, proposal or next action when that better serves another purpose.
