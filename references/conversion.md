# Restyling and conversion

## Existing HTML

Read the source and inspect every slide first. Record slide order, notes, citations, figures and interaction states. Keep a copy. Restyle only after distinguishing essential content from decorative elements. Preserve citations and speaker notes; split overfull slides rather than shrinking them. Keep the same TashTech mode through revisions unless the user asks for a change. Rebuild embedded asset references and validate the resulting self-contained deck.

## PowerPoint input

Use a source reader already available in the host environment, or ask the user to export the source as PDF, slide images, or readable text. This skill does not bundle a PowerPoint converter or require installing one. Do not silently install packages.

This is content-guided redesign, not automatic pixel-perfect conversion. Compare the source’s rendered slides with its extracted structure. SmartArt, formulas, embedded media, vector pictures, backgrounds, animations and complex charts/crops may need manual reconstruction. Report unreadable material instead of silently dropping it. Legacy `.ppt` files likewise need an existing reader or a readable export.

Build a slide-by-slide inventory and map original figures/notes to the restyled slides. Preserve all content unless a condensed adaptation was requested. Mark unknown/unreadable material and ask for the needed source rather than inventing it. For charts, use real values and units, not an attractive illustration masquerading as source data.

## PDF, DOCX and course notes

Use the host's appropriate document-reading tools. Render visual pages when parsed text misses a figure, equation or table. Do not treat OCR or disconnected retrieval snippets as complete chapter coverage. Keep a source-to-slide map for long material. Turn headings into a teaching progression rather than pasting paragraphs into cards.

## Output boundaries

Native output: self-contained HTML, with PDF available through browser printing. The skill does not generate editable `.pptx` by itself. When editable PowerPoint is specifically required, use a separate PPTX-authoring capability and transfer the same branding, layouts, assets and verification rules. Be explicit about which deliverables are editable and which are static.
