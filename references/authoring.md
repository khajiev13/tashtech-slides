# Authoring HTML decks

## Files and dependency boundary

Author one self-contained HTML file directly. No Python, npm, framework, package installation, server or other skill is required for this workflow. Viewing needs a modern browser with JavaScript.

1. Copy `templates/presentation.html` into the requested output file.
2. Replace `{{CSS}}` with the contents of `styles/tashtech-tokens.css` followed by `styles/viewport-base.css`; replace `{{JS}}` with `templates/runtime.js`.
3. Replace `{{SLIDES}}` with authored `section.slide` elements using the structure below. Set `{{LANG}}`, `{{TITLE}}`, `{{MODE}}`, `{{PURPOSE}}`, `{{MOTION}}`, `{{AUTOSAVE_KEY}}`, `{{VERSION}}` (from `VERSION`) and any `{{FOOTER}}` tokens. HTML-escape metadata values. Motion is `none`, `subtle` or `expressive`; default to `subtle`.
4. Resolve each `{{asset:ASSET-ID}}` through `assets/manifest.json`, embedding the corresponding image bytes as a base64 data URI using available file tools. Do not leave relative asset paths or macros in the final HTML.
5. Preserve the runtime, controls and stage structure. Open the final HTML in a browser and follow `export-and-validation.md`.

If Python 3.10+ is already available, `scripts/create_deck.py` automates this assembly using only its standard library. The command examples below are optional conveniences, not prerequisites.

## Author one or more sections

Write an HTML fragment, for example `lecture-slides.html`:

```html
<section class="slide" data-mode="lecture" data-title="Binary place values">
  <header class="slide-header">
    <span class="section-label">Fundamentals of Computer Science</span>
    <img class="corner-mark" src="{{asset:tt-monogram}}"
         alt="Tashkent University of Technology">
  </header>
  <div class="slide-main" data-fit>
    <p class="eyebrow">Worked example</p>
    <h2 data-editable>Binary digits have positional weights.</h2>
    <div class="panel warm" data-panel>
      <p class="equation" aria-label="Binary 1011 equals decimal 11">
        1011<sub>2</sub> = 8 + 0 + 2 + 1 = 11<sub>10</sub>
      </p>
    </div>
    <p class="caption">This example uses unsigned binary representation.</p>
  </div>
  <footer class="slide-footer">
    <span class="footer-label">{{FOOTER}}</span>
    <span class="page-number"></span>
  </footer>
  <aside class="speaker-notes">Ask students to convert 1101₂. Answer: 13₁₀.</aside>
</section>
```

Duplicate the section structure for each slide. Keep `section.slide` as a **direct child of the stage**. Use `data-title` for a concise accessible navigation label. Use a real heading on every content slide. Let the runtime assign slide IDs/page numbers; avoid duplicate IDs on repeated chart definitions. Add `data-fit` to panels whose fixed dimensions need checking; mark sibling blocks with `data-panel` for overlap checks. `data-allow-overlap` is only for deliberately decorative elements, not a way to suppress genuine errors.

Supported macros: `{{TITLE}}`, `{{FOOTER}}`, `{{LANG}}`, `{{MODE}}`, `{{PURPOSE}}`, `{{VERSION}}` and `{{asset:ASSET-ID}}`. Asset macros belong in `src`; the builder substitutes a data URI. Literal JavaScript/CSS braces are not template syntax. Metadata is HTML-escaped. The slide fragment itself is trusted authoring input, not an HTML sanitizer: never render unreviewed executable content from external documents.

## Purpose-aware building

Use `--purpose` with one of the IDs in `presentation-purposes.md`. It selects a default visual mode and, when `--slides` is omitted, the matching localized starter text. `--mode` is an optional visual override. Neither option rewrites an authored fragment: the author must supply suitable content and any per-slide `data-mode` / `data-purpose` attributes. Avoid contradicting the intended global purpose.

No purpose/mode creates a General/Institutional starter. Explicit legacy `--mode lecture` continues to infer Teaching; `--mode research` infers Research. This keeps older explicit calls usable while removing the automatic lecture assumption.

Examples:

```bash
python3 "$SKILL_DIR/scripts/create_deck.py" --purpose leadership --title "Decision briefing" --output ./brief.html
python3 "$SKILL_DIR/scripts/create_deck.py" --purpose training --lang uz --title "Xodimlar uchun trening" --output ./training.html
```

## Build and edit

```bash
python3 "$SKILL_DIR/scripts/create_deck.py" \
  --title "Binary numbers" --footer "Computer Science / Week 1" \
  --mode lecture --lang en --slides ./lecture-slides.html \
  --output ./lecture.html
```

Without `--slides`, the builder creates a three-slide **starting point**, not a finished presentation. Supply source-grounded content before presenting it. Optional `--css` appends an authored CSS file; it must preserve brand/stage invariants. `--force` explicitly permits replacing an existing HTML output. Prefer revising the source fragment and rebuilding instead of repeatedly patching generated HTML.

For new content images, read the image bytes and encode them as `data:image/png;base64,...` or the correct media type. Keep meaningful alt text. The default validation/export path renders a self-contained document in memory; external or relative resource files are not a supported final delivery. Embed SVG diagrams inline with a `title`/`desc`, or use the image-generation tools available to the agent for genuinely illustrative visuals. Do not generate logos or redraw supplied technical diagrams without preserving their meaning.

## Runtime controls

Arrow keys, Page Up/Down, Home/End and space navigate. N toggles notes on the same screen. E enables **plaintext** editing on `data-editable` elements. Ctrl/Cmd+S or Save HTML creates a new downloadable HTML file with edits. Editing a heading may remove its original colored spans; use the source fragment for rich formatting. F requests full screen; the browser may deny it in embedded contexts. Horizontal swipes navigate on touch devices. The toolbar remains outside the authored stage.

The text editor is not a drag-and-drop slide builder, autosave system or private presenter display. Do not mark whole columns or nested rich layouts as editable. Revalidate after text edits because a longer heading may no longer fit.

The public runtime API is `window.TashTechDeck`: `goTo(index)`, `next()`, `previous()`, `setNotes(boolean)`, `setEdit(boolean)`, `serialize()`, and read-only `index` / `count`. Indices are zero-based. A normal browser URL can include `#slide-3` to open slide 3. No local storage, analytics, remote requests or background publication is used.

## Citations and reference slides

Put a short human-readable source line beside an evidence-heavy figure (author/organization, year, page or section). Add a reference slide with the full title, date and resolvable URL/DOI when available. Place hyperlinks in `a` elements, not in essential text that exists only behind a hover. Preserve page numbers from the source, not invented PDF indexing. If sources are extensive, provide a separate references/notes document rather than shrinking the slide to unreadable size.
