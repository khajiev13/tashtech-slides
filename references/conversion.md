# Restyling and conversion

## Existing HTML

Read the source and inspect every slide first. Record slide order, notes, citations, figures and interaction states. Keep a copy. Restyle only after distinguishing essential content from decorative elements. Preserve citations and speaker notes; split overfull slides rather than shrinking them. Keep the same TashTech mode through revisions unless the user asks for a change. Rebuild embedded asset references and validate the resulting self-contained deck.

## PowerPoint input

```bash
python3 -m pip install -r "$SKILL_DIR/requirements-pptx.txt"
python3 "$SKILL_DIR/scripts/extract_pptx.py" source.pptx ./extracted
```

The output contains `content.json`, extracted image files, slide/element order, basic bounds, table cells, text and available notes. The extractor recursively visits grouped shapes. Chart data is best-effort and always flagged for source review. The output directory must be new or empty, so prior files are not silently overwritten.

This is **content extraction for agent-assisted redesign**, not automatic pixel-perfect conversion. The agent must compare the source's rendered slides with the extracted structure. SmartArt, formulas, embedded media, vector pictures, master-slide backgrounds, animations, connectors, chart categories/styles and complex crops may require manual reconstruction. Unsupported shapes generate warnings; do not drop them without saying so. A legacy `.ppt` must first be converted with an appropriate local application.

Build a slide-by-slide inventory and map original figures/notes to the restyled slides. Preserve all content unless a condensed adaptation was requested. Mark unknown/unreadable material and ask for the needed source rather than inventing it. For charts, use real values and units, not an attractive illustration masquerading as source data.

## PDF, DOCX and course notes

Use the host's appropriate document-reading tools. Render visual pages when parsed text misses a figure, equation or table. Do not treat OCR or disconnected retrieval snippets as complete chapter coverage. Keep a source-to-slide map for long material. Turn headings into a teaching progression rather than pasting paragraphs into cards.

## Output boundaries

Implemented output: self-contained HTML and printable PDF. The skill does not generate editable `.pptx` by itself. When editable PowerPoint is specifically required, use a separate PPTX-authoring capability and transfer the same branding, layouts, assets and verification rules. Be explicit about which deliverables are editable and which are static.
