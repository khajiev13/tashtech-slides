# TashTech Slides skill

Reusable `tashtech-slides` skill for source-grounded, university-branded HTML presentations, with optional PDF export and PowerPoint content extraction.

This repository contains the skill and its runtime resources only. Demos, generated presentations, development plans, tests, evaluation reports, and caches from the source package are excluded.

## Install

Clone this repository into your agent’s skills directory as `tashtech-slides`, then invoke `$tashtech-slides`. See [SKILL.md](SKILL.md) for the workflow.

## Dependencies

The HTML builder requires Python 3.10+ and uses only the standard library. To enable browser validation and PDF export, run from this directory:

```bash
python3 -m pip install -r requirements-tools.txt
python3 -m playwright install chromium
```

For optional PowerPoint content extraction:

```bash
python3 -m pip install -r requirements-pptx.txt
```

## Rights and provenance

See [LICENSE](LICENSE), [ATTRIBUTION.md](ATTRIBUTION.md), and [asset manifest](assets/manifest.json). The software license excludes university marks and artwork. This is a proposed presentation system, not an approved university brand manual.
