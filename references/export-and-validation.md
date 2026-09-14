# Validation and PDF export

## Review in an existing browser

Open the self-contained HTML in a modern browser. No package installation or server is required. Inspect every slide at 1920×1080, 1280×720 and 390×844 using the browser’s responsive viewport controls when available. Check text/panel overflow, image loading and aspect ratios, footer intrusion, navigation, notes, editing and JavaScript errors. Expand interactive answers and check that they fit too. Review at least one small viewport with the toolbar visible.

Check source coverage, citations, chart units, contrast, language and readable font sizes separately. If no browser is available, report visual verification as incomplete; a static check cannot establish correct rendering.

## Optional static check

If Python 3.10+ is available, this helper uses only the standard library:

```bash
python3 "$SKILL_DIR/scripts/validate_deck.py" ./presentation.html --report ./validation.json
```

It checks slide structure, required IDs, document language, alt attributes, duplicate IDs, unresolved macros and remote/missing resources. Exit code 0 means the implemented static checks passed; 1 means findings; 2 means input/tool failure. It does not run a browser or certify layout, navigation, content accuracy or accessibility. Reports can be replaced on subsequent runs.

## PDF through browser printing

Open the HTML and choose Print / Save as PDF. Enable background graphics and disable browser headers/footers. Use the CSS-defined 16:9 page size when supported; A4/Letter may rescale or letterbox content. The print stylesheet makes animations static, expands answers and excludes speaker notes and controls. Review the preview before saving, and avoid overwriting an existing PDF unless intended.

Inspect the saved PDF’s page count, ratio, glyphs, images, tables, links and text selection. Browser versions and font substitutions can change wrapping. Do not claim a PDF was created until the file exists and has been inspected. No automated PDF exporter or browser installation is bundled.

## Sharing

Share HTML and/or PDF only through the user-authorized channel. HTML includes readable speaker notes and hidden answers; remove private material from copies not authorized to contain it. PDF is static, not an editable PowerPoint file.
