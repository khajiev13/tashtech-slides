# Teaching and training guidance

These are working authoring recommendations, not a statement of TashTech's academic policy.

## Plan around understanding

Use the audience's prior knowledge, language and learning objectives. A first-year introduction and a graduate research seminar need different assumptions. Do not ask the instructor to repeat information already in their brief. When only a topic is supplied, agree on scope or clearly state a reasonable starting assumption.

For a lecture, organize the progression as question → explanation → worked example → student attempt → feedback → recap. This is a flexible pattern, not a mandatory six-slide cycle. Add time for questions and activities instead of assuming that every minute must contain a new slide.

State learning outcomes with observable verbs such as describe, compare, calculate, trace, interpret or design. Avoid using “understand” as the only testable objective. Give each important concept an example appropriate to the learners.

## Source coverage and factual integrity

Read the actual chapter/notes, including figures, definitions, equations and exercises. A partial search result is not enough to promise comprehensive chapter coverage. For a long input, keep a working table with source section/page, concept, destination slide and treatment (explained, illustrated, exercise, appendix). Do not silently omit difficult sections.

Maintain a boundary between material from the source, the instructor's additions and newly authored illustrations. Preserve source citations; compute examples independently. Never fabricate references, page numbers, experimental outcomes, university facts or names. If the source has an apparent error, flag it and explain the discrepancy rather than quietly copying or “correcting” it.

## Worked examples

Present the given data and assumptions, explain the method, show intermediate steps, then interpret the answer. Do not hide a unit conversion or key algebraic step just to produce a cleaner slide. Spread a long derivation over multiple slides with consistent notation.

For equations, define symbols and state applicable conditions. Use semantic MathML or vector math when the host supports it reliably. The package's simple `.equation` block supports plain symbols, superscripts and subscripts without a remote math library. Complex mathematics may require a separate rendering tool; embed its output and provide a text equivalent. Test the actual output and PDF.

For code, use the smallest meaningful snippet and a separate runnable source file when needed. Identify the language/version and whether the snippet is an excerpt. Test it in the appropriate local environment where available; disclose unexecuted code. Prefer a trace table or input/output example to unexplained syntax coloring.

## Activities and answers

Provide clear instructions, a realistic duration and the expected reasoning. An exercise should test a stated objective, not an unrelated trick. Separate instructor guidance from the student-facing task.

Use `details.answer` only for low-stakes teaching reveals. HTML recipients can inspect closed answers and notes. The PDF exporter expands answers automatically. For exams or answer-free handouts, author a separate student version with those elements actually removed; hiding them is not redaction.

## Density and language

Speaker-led slides: one main idea, large text, usually 1–3 short points plus a purposeful visual. Put the extended explanation in notes or a handout. Reading-first slides may be more self-contained, but no internal scrolling or unreadable type is acceptable.

Match English, Uzbek or Russian as requested. Keep technical terms consistent, and preserve code keywords/symbols. Check Uzbek Oʻ/Gʻ and Cyrillic glyphs on the actual computer. Do not translate the English wordmark or create substitute institution names inside logos. For bilingual instruction, either use restrained paired terms or two separate language decks rather than doubling every paragraph.

## Final instructor review

Check all numerical results, language, source coverage, exercise answers and teaching sequence. Confirm that students can read the smallest essential content from the back of the room. Check the real projector and browser when practical. The automated validator cannot judge subject-matter accuracy or classroom pedagogy.


## Staff training adaptation

For staff onboarding and practical process training, start with the actual task, reviewed procedure and prerequisites. Use a demonstration, safe practice scenario and the supplied help route. Replace student-specific assumptions with the staff audience's experience; a process lesson is not automatically a course lecture. Do not expose live credentials or personal records, or present training advice as newly approved university policy. See `institutional-content.md` for claim status and sharing review.
