# Validation and PDF export

## Setup once on the author's computer

```bash
python3 -m pip install -r "$SKILL_DIR/requirements-tools.txt"
python3 -m playwright install chromium
```

Use a virtual environment when appropriate. Viewing a built HTML deck does not require these packages. Tools never install software automatically. Existing system Chromium can be selected with `--chromium /absolute/path/to/chromium` or `TT_CHROMIUM_BINARY`; do not change browser security policies to run the tools.

## Validate before delivery

```bash
python3 "$SKILL_DIR/scripts/validate_deck.py" ./presentation.html
python3 "$SKILL_DIR/scripts/validate_deck.py" ./presentation.html \
  --browser --screenshots ./review --report ./validation.json
```

Static checks run using the standard library: slides, required IDs, document language, missing alt attributes, duplicate IDs, unresolved macros and remote/missing resources. Browser checks use Chromium at 1920×1080, 1280×720 and 390×844; verify stage ratio and bounds, selected text/panel overflow, broken images, same-parent panel overlap, footer intrusion, navigation, notes and JavaScript errors. `details` answers are opened during checking because the expanded state must fit too.

The document is rendered **from local HTML bytes in memory**. Outgoing HTTP(S) requests are blocked. The final HTML must embed its assets, not rely on a separate directory or CDN. The browser-helper module also contains an optional loopback preview context, but the default checks/export do not start a server or navigate to local URLs. This supports managed environments that restrict `file://` or network navigation.

Exit code 0 means implemented checks passed; 1 means validation findings; 2 means tooling/input failure. Reports/screenshots are diagnostic files and can be replaced by subsequent runs. Deck/PDF outputs require `--force` to overwrite. The script is a heuristic: it does not certify subject matter, correct data, every possible overlapping element, legal permissions, full contrast or semantic accessibility. Visually inspect **every slide**, not only the cover. At least one small viewport should be reviewed with the toolbar visible.

## Export

```bash
python3 "$SKILL_DIR/scripts/export_pdf.py" ./presentation.html ./presentation.pdf
```

The exporter reruns static/browser validation and stops on errors. It prints one 20×11.25-inch page per 1920×1080 slide with zero margins and background graphics. This preserves selectable HTML text and avoids making every page a screenshot. Image-based figures remain raster images. Animations become static. Answers in `details` are expanded. Speaker notes and the toolbar are excluded. Add `--force` only when replacing an existing PDF is intentional.

Manually open the PDF and inspect its page count, ratio, glyphs, images, tables, links and text selection. Browser versions/font substitutions can change wrapping. Tests on the development machine do not replace checking a changed deck or the presentation environment.

## Browser print fallback

Open the built HTML and use Print / Save as PDF. Enable background graphics, turn off browser headers/footers, and use the CSS-defined 16:9 page size when supported. Standard A4/Letter may rescale or letterbox content. The automated exporter is the repeatable path; browser print dialogs vary. Do not claim a PDF was created until a PDF file actually exists and has been inspected.

## Sharing

Distribute the self-contained HTML and/or PDF through the university-approved channel. The runtime contains no hosting or email function. Sharing is a separate authorized action. HTML includes speaker notes and hidden answers; remove private material from any version not authorized to contain it. PDF is static and not an editable PowerPoint file.
