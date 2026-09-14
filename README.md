# TashTech Slides skill

Reusable `tashtech-slides` skill for source-grounded, university-branded HTML presentations, with browser PDF printing.

This repository contains the skill and its runtime resources only. Demos, generated presentations, development plans, tests, evaluation reports, and caches from the source package are excluded.

## Install

Clone this repository into your agent’s skills directory as `tashtech-slides`, then invoke `$tashtech-slides`. See [SKILL.md](SKILL.md) for the workflow.

## Zero-install workflow

The agent authors a single HTML file with inline CSS/JavaScript and embedded images. No npm, frameworks, build tools, Python packages, server, external service or other skill is required. Open the result in a modern browser and use Print / Save as PDF when needed.

The optional `scripts/create_deck.py` and `scripts/validate_deck.py` helpers use Python 3.10+ and its standard library only. Python is not required for direct HTML authoring or viewing. For PowerPoint input, use a reader already available in your environment or supply a PDF/image/text export.

## Rights and provenance

See [LICENSE](LICENSE), [ATTRIBUTION.md](ATTRIBUTION.md), and [asset manifest](assets/manifest.json). The software license excludes university marks and artwork. This is a proposed presentation system, not an approved university brand manual.
