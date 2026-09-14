# Accessibility and readability

The package includes semantic headings, keyboard controls, off-slide navigation UI, hidden-slide `aria-hidden`/`inert`, alt-text slots and reduced-motion support. These are implementation aids, not an accessibility certification.

## Authoring checklist

Use one clear heading per slide. Set the document language (`en`, `uz`, `ru`) and avoid unsupported glyphs. Provide informative alt text for content images; use empty alt text only for genuinely decorative imagery. A logo should identify the university, not repeat every visible letter.

Use real table headings (`th` with `scope`) and explicit units. Give charts a text summary of the finding, category names, values and data source. Never distinguish two categories solely by orange versus charcoal. Give complex diagrams a logical reading order and a concise textual explanation in notes or a companion handout.

Keep ordinary text at a contrast of at least 4.5:1, with at least 3:1 for large text where applicable. The primary orange on white should be reserved for large text and graphic accents; use `--tt-orange-text` for small labels. The light rules are decorative, not the only way to indicate an interactive control. Recheck contrast after changing colors or adding a background image. The validator does not calculate full contrast across gradients, raster assets and transparency.

Prefer no animation for detailed lecture content. The runtime does not require animated entrances. If adding motion, respect `prefers-reduced-motion` and make the final state available in print. Never require hover, rapid timing, color perception or a mouse gesture to understand a slide. Do not add flashing effects.

The fixed stage deliberately does not reflow on phones. It preserves the presentation's composition, but small text may not be comfortable on a handheld screen without zoom. Provide the PDF and, when mobile or screen-reader reading is important, a linear text/HTML handout with the same meaning. That handout is distinct from the slide deck.

## Keyboard and notes

Check arrow keys, space, Home/End, N/E/F and buttons. Focus indicators must be visible. Navigation ignores text-entry controls to avoid moving slides while editing. Inactive slides are inert. The notes panel is on the same screen; it is neither private nor a dual-display presenter tool. Close it before projecting student-facing material.

## PDF

The exporter requests tagged PDF output, preserves selectable text where the source is text, and excludes runtime controls and notes. This does not guarantee PDF/UA conformance, perfect reading order, searchable text inside raster figures or accessible mathematical semantics. Inspect exported pages and text extraction; use specialist PDF accessibility remediation for a formal requirement.

## Sources

W3C WCAG 2.2, especially 1.1.1, 1.3.1, 1.4.3, 1.4.11 and 2.1.1: https://www.w3.org/TR/WCAG22/
