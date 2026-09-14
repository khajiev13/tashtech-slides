# Relationship to Frontend Slides

Upstream: https://github.com/zarazhangrui/frontend-slides
Reviewed: 14 September 2026. The upstream main branch is mutable; this package does not pin or claim a specific upstream commit.

This is **TashTech Slides — University Edition 2.1.0**, expanded from TashTech Slides 1.0.0, inspired by the Frontend Slides skill. It is not an official Frontend Slides v2, a Zara Zhang endorsement or an exact feature-parity fork. Its runtime, builder and tests are a focused independent implementation of the requested university presentation adaptation. See ATTRIBUTION.md and LICENSE.

| Area | Frontend Slides observed workflow | TashTech adaptation |
|---|---|---|
| Core output | Single HTML with inline CSS/JS | Retained, with selected bundled images embedded |
| Stage | Fixed 1920×1080, uniform scaling | Retained |
| Styling | Multiple unrelated presets / visual exploration | Three shared modes; purpose-based selection; neutral General/Institutional fallback |
| Typography | Web-font-oriented design guidance | Explicit offline fallback stack; no font binaries |
| Discovery | Style previews by default | Avoid unnecessary style questions when the brand/mode is already specified |
| Content structure | Broad presentation use | Nine purposes: general, teaching, research, leadership, partnership, admissions, staff training, student projects and events |
| Authority and audience | Reviewed per task | Explicit distinctions between facts, proposals, student work and synthetic examples; internal/external review |
| Marks | User images evaluated per task | Manifest-indexed TashTech marks, originals and usage/rights notes |
| Inline editing | Browser editing workflow | Plaintext edits on opt-in elements and Save HTML |
| PDF | Screenshot-based export described upstream | Browser print with selectable HTML text |
| Conversion | Extract PPTX and redesign | Existing source readers or readable exports; explicit fidelity warnings |
| Sharing | Optional hosting workflow | No deployment bundled; explicit permission required for publication |
| Validation | Source guidance and viewport rules | Optional standard-library static checker plus browser review |

The upstream MIT notice is retained. The software license does not license university trademarks or supplied artwork.
