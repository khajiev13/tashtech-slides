# TashTech presentation design guide

Version 2.1.0 · 14 September 2026 · Proposed presentation system, not a university-approved brand manual.

## What was verified

The user supplied five raster images. Their originals and SHA-256 checksums are preserved in `assets/originals/` and `assets/manifest.json`. The official website was inspected for the English institution name, orange TT identity, outlined/solid wordmark treatment and language context. Exact CSS tokens and the deployed font family could not be independently retrieved. Website content is not a substitute for an approved visual identity manual.

Pixel sampling of the clean supplied monogram gave RGB (230, 69, 25), `#E64519`, as the dominant orange. The supplied circular mark is predominantly RGB (229, 69, 25), `#E54519`. Preserve that difference in original images; use the former for slide accents. JPEGs contain many nearby compression colors.

## Design tokens

| Token | Value | Status / role |
|---|---|---|
| `--tt-orange` | `#E64519` | Sampled monogram accent; big headlines, rules, markers, charts |
| `--tt-orange-text` | `#B73513` | Proposed darker orange for small text on white |
| `--tt-ink` | `#202426` | Proposed main text / research section background |
| `--tt-muted` | `#596167` | Proposed secondary text on white |
| `--tt-paper` | `#FFFFFF` | Main content background |
| `--tt-surface` | `#F3F4F4` | Proposed light neutral panels |
| `--tt-warm` | `#FFF2EB` | Proposed selected explanation/callout panels |
| `--tt-line` | `#D9DEDF` | Proposed nonessential dividers |

Orange is an accent, not a substitute for visual hierarchy. Keep most lecture content on white. Use dark slides mainly for research covers and true section changes. Thin panel borders are decorative; chart categories must also have labels or patterns. For scientific figures that genuinely require other colors, preserve the source legend and use a suitable accessible scientific palette within the figure; do not change the surrounding university design.

## Typography

Proposed offline stack: `Arial, "Helvetica Neue", Helvetica, sans-serif`; code: `"Courier New", Courier, monospace`. These names are choices for portable presentation rendering, **not verified official typefaces**. No font files or remote font requests are included. A machine may substitute an installed font; test wrapping and Cyrillic/Uzbek glyphs on the actual presentation computer.

At 1920×1080: cover 104–118 px, content heading 68–76 px, body 34–38 px, labels 23–27 px, code 28–32 px, references 21–24 px. Prefer the upper end for projection. Footers are nonessential metadata. Do not fit extra content by lowering type below the comfortable range. A PDF page here is 20×11.25 inches; at a different physical print size the apparent text size changes.

## Layout rhythm

Author inside a 1920×1080 stage. Safe area: 96 px left/right, 64 px top, 100 px bottom. Header: 54 px; main inter-block spacing: 32–34 px; column gutters: 32–56 px. Footer sits below the content with a rule and slide number. Prefer square or minimally rounded surfaces. A section title can be large, but it should not collide with a mark.

Use a deliberate sequence: a conceptual diagram, a worked calculation, a code trace, an evidence chart, an activity, a summary. Avoid a whole deck of interchangeable cards. Keep the full logo visible; do not use a cropped logo as an abstract diagonal. Diagonal accents may echo the mark without re-drawing it, but are optional and not necessary for a good lecture.

## Three shared visual modes

Select purpose first using `presentation-purposes.md`. Teaching and staff training normally use Lecture, research and student projects use Research, and other purposes use Institutional. With no meaningful purpose supplied, use a neutral General/Institutional draft rather than assuming a lecture. These are not department-specific sub-brands.

**Lecture:** white backgrounds, large explanatory text, short examples, minimal mark in the header. Speaker-led by default. Full wordmark on cover/closing; circular mark optional.

**Research:** same content typography and white evidence slides; charcoal covers/dividers; explicit method, comparison, uncertainty, limitations and citations. Do not turn all data slides dark.

**Institutional:** stronger wordmark/circle presence on opening/closing, clear formal hierarchy, timelines and decision layouts. No unsourced achievements, unsigned commitments or invented partner logos.

Modes are an authored design vocabulary. A `data-mode` attribute alone does not invent new layouts: choose appropriate cover and content classes as documented in `slide-layouts.md`.

## Brand review before institutional rollout

Ask the university's communications owner to confirm the exact official color, fonts, approved logo master, minimum size and clear-space rules. Replace working rules when approved standards arrive, while preserving provenance and regression-testing the demonstration deck. Do not silently overwrite supplied originals.
