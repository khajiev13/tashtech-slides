# Logo and artwork rules

Use `assets/manifest.json` as the machine-readable asset index. All paths are relative to the skill root.

| Asset ID | File | Native pixels | Background | Use |
|---|---|---:|---|---|
| `tt-monogram` | `assets/logos/tt-monogram-orange-on-white.png` | 422×276 | Opaque white | Small content-slide mark |
| `tt-wordmark` | `assets/logos/tt-wordmark-orange-on-white.png` | 1209×157 | Opaque white | Cover, closing, formal introduction |
| `tt-circle` | `assets/logos/tt-circle-orange-transparent.png` | 2048×2046 | Transparent | Selected covers / section openings |
| `scholars-artwork` | `assets/artwork/scholars-heritage-transparent.png` | 1254×1254 | Transparent | Optional heritage illustration only |

The first two are margin-trimmed derivatives with 12 px retained white padding. No logo was vector-traced, recolored or generated. The wordmark PNG comes from a JPEG and retains its source-quality limitations. The circle and scholars files are exact copies. Five originals include the alternate monogram JPEG, retained for provenance but not preferred for rendering.

## Placement

Use the monogram at approximately 82 px wide in the content header. On a dark slide, retain its white plaque; do not filter it to white. Use the wordmark at roughly 620 px on covers, less than its native width. The circle generally works at 450–600 px for a cover; preserve its almost-square aspect ratio. Do not force a perfect 1:1 raster crop.

Working clear-space rule: leave at least one quarter of the displayed monogram's visible height around a compact mark, and at least 24 design pixels around the wordmark. These are proposed practical rules, not certified university brand standards. Do not place essential text inside the circle, over its perimeter lettering, or behind the scholars artwork.

Use a white background behind the monogram/wordmark because their supplied backgrounds are white. The circle's apparently black areas in some viewers are transparency, not a black disk; inspect its alpha channel before flattening it. On dark backgrounds, keep the full circle at 100% opacity and check the lettering's legibility. White is the preferred backdrop when lettering matters.

## Integrity and rights

Do not distort, skew, outline, animate, recolor or reconstruct the marks. Do not recreate outlined university lettering as normal HTML text. Do not invent a white logo or an SVG master. A future approved SVG should be stored as a separate asset with its own source and rights record.

Do not identify the illustrated scholars by name from the image, describe the artwork as a verified institutional seal, or suggest historical provenance not supplied by the owner. The artwork has rough colored edge artifacts; use sparingly and never clean it up destructively in place.

The software license does not grant trademark rights. Assets remain subject to their owners' permissions. Include them for authorized university presentation workflows, not as freely licensed branding for other institutions.
