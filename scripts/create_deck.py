#!/usr/bin/env python3
"""Build one offline TashTech HTML deck. Python 3.10+, standard library only."""
from __future__ import annotations
import argparse
import base64
import html
from html.parser import HTMLParser
import json
import mimetypes
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODES = ('lecture', 'research', 'institutional')
MOTIONS = ('none', 'subtle', 'expressive')
LANGUAGES = ('en', 'uz', 'ru')
PURPOSES = ('general', 'teaching', 'research', 'leadership', 'partnership',
            'admissions', 'training', 'student-project', 'event')


class _SlideFinder(HTMLParser):
    """Recognize exact HTML class tokens rather than matching attribute text."""
    def __init__(self) -> None:
        super().__init__()
        self.found = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = dict(attrs).get('class') or ''
        if tag == 'section' and 'slide' in classes.split():
            self.found = True


def asset_data_uri(asset_id: str) -> str:
    """Resolve a curated manifest asset, never an arbitrary external path."""
    manifest = json.loads((ROOT / 'assets/manifest.json').read_text(encoding='utf-8'))
    entry = next((a for a in manifest['assets'] if a['id'] == asset_id), None)
    if entry is None:
        raise ValueError(f'Unknown asset: {asset_id}')
    path = (ROOT / entry['path']).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError(f'Invalid asset path: {entry["path"]}')
    mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


def resolve_purpose(mode: str | None, purpose: str | None) -> tuple[str, str]:
    """Choose purpose first; explicit legacy modes retain their starter meaning."""
    if mode is not None and mode not in MODES:
        raise ValueError(f'Invalid mode: {mode}. Choose one of {MODES}.')
    if purpose is None:
        purpose = {'lecture': 'teaching', 'research': 'research'}.get(mode, 'general')
    if purpose not in PURPOSES:
        raise ValueError(f'Invalid purpose: {purpose}. Choose one of {PURPOSES}.')
    profiles = json.loads((ROOT / 'references/purpose-profiles.json').read_text(encoding='utf-8'))
    return mode or profiles['profiles'][purpose]['mode'], purpose


def starter_slides(title: str, mode: str, lang: str, footer: str, purpose: str) -> str:
    """A localized, purpose-aware starting point, not a factual finished deck."""
    profiles = json.loads((ROOT / 'references/purpose-profiles.json').read_text(encoding='utf-8'))
    words = profiles['profiles'][purpose]['text'][lang]
    notice = {
        'en': 'Starter template — replace with verified material.',
        'uz': 'Boshlang‘ich namuna — tekshirilgan mazmun bilan almashtiring.',
        'ru': 'Начальный шаблон — замените проверенными материалами.'
    }[lang]
    esc = html.escape
    def wrap(content: str, label: str, extra: str = '') -> str:
        return f'''<section class="slide {extra}" data-mode="{mode}" data-purpose="{purpose}" data-title="{esc(label)}">
<header class="slide-header"><span class="section-label">{esc(words['label'])}</span><img class="corner-mark" src="{{{{asset:tt-monogram}}}}" alt="Tashkent University of Technology"></header>
<div class="slide-main" data-fit>{content}</div>
<footer class="slide-footer"><span class="footer-label">{esc(footer)}</span><span class="page-number"></span></footer>
<aside class="speaker-notes">{esc(notice)} {esc(words['closing_prompt'])}</aside></section>'''
    cover_extra = 'cover dark' if mode == 'research' else 'cover institutional-cover' if mode == 'institutional' else 'cover'
    cover = (f'<div class="cover-layout"><div class="cover-copy"><p class="eyebrow">{esc(words["label"])}</p>'
             f'<h1 data-editable>{esc(title)}</h1><p class="subtitle" data-editable>{esc(words["tagline"])}</p>'
             f'<p class="caption">{esc(notice)}</p></div><div class="cover-art">'
             '<img class="circle-mark" src="{{asset:tt-circle}}" alt="Tashkent University of Technology circular mark"></div></div>')
    steps = ''.join(f'<div class="objective"><span class="index">0{i}</span><p data-editable>{esc(v)}</p></div>'
                    for i, v in enumerate(words['steps'], 1))
    frame = (f'<h2 data-editable>{esc(words["framing_title"])}</h2>'
             f'<p class="subtitle" data-editable>{esc(words["framing_prompt"])}</p><div class="stack">{steps}</div>')
    close = (f'<p class="eyebrow">{esc(words["label"])}</p><h2 data-editable>{esc(words["closing_title"])}</h2>'
             f'<div class="callout"><p data-editable>{esc(words["closing_prompt"])}</p></div>'
             f'<p class="caption">{esc(notice)}</p>')
    return '\n'.join([wrap(cover, title, cover_extra), wrap(frame, words['framing_title']),
                      wrap(close, words['closing_title'])])


def resolve_motion(mode: str, purpose: str, motion: str | None) -> str:
    """Choose a presentation motion profile."""
    if motion is not None and motion not in MOTIONS:
        raise ValueError(f'Invalid motion: {motion}. Choose one of {MOTIONS}.')
    if motion is not None:
        return motion
    if purpose == 'event':
        return 'expressive'
    if purpose in {'teaching', 'training', 'student-project'}:
        return 'subtle'
    if mode == 'research':
        return 'subtle'
    return 'subtle'


def build_deck(title: str = 'TashTech presentation', mode: str | None = None, lang: str = 'en',
               slides: str | None = None, footer: str = 'Tashkent University of Technology',
               extra_css: str = '', purpose: str | None = None, motion: str | None = None) -> str:
    """Return self-contained HTML. Custom slides are trusted HTML, not sanitized input."""
    mode, purpose = resolve_purpose(mode, purpose)
    motion = resolve_motion(mode, purpose, motion)
    if lang not in LANGUAGES:
        raise ValueError(f'Invalid language: {lang}. Choose one of {LANGUAGES}.')
    if not title.strip():
        raise ValueError('Title must not be empty.')
    if slides is None:
        slides = starter_slides(title, mode, lang, footer, purpose)
    finder = _SlideFinder()
    finder.feed(slides)
    if not finder.found:
        raise ValueError('Input must contain at least one section with class="slide".')
    values = {'TITLE': html.escape(title, quote=True), 'LANG': lang, 'MODE': mode,
              'FOOTER': html.escape(footer, quote=True), 'PURPOSE': purpose, 'MOTION': motion,
              'AUTOSAVE_KEY': html.escape(title, quote=True),
              'VERSION': html.escape((ROOT / 'VERSION').read_text(encoding='utf-8').strip(), quote=True)}
    for key, value in values.items():
        slides = slides.replace('{{' + key + '}}', value)
    cache: dict[str, str] = {}
    def resolve(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in cache:
            cache[key] = asset_data_uri(key)
        return cache[key]
    slides = re.sub(r'\{\{asset:([a-z0-9-]+)\}\}', resolve, slides)
    if re.search(r'\{\{(?:asset:|[A-Z_]+\}\})', slides):
        raise ValueError('Unresolved template token in slide content.')
    css = '\n'.join((ROOT / 'styles' / name).read_text(encoding='utf-8')
                    for name in ('tashtech-tokens.css', 'viewport-base.css')) + '\n' + extra_css
    script = (ROOT / 'templates/runtime.js').read_text(encoding='utf-8')
    template = (ROOT / 'templates/presentation.html').read_text(encoding='utf-8')
    values.update(CSS=css, JS=script, SLIDES=slides)
    return re.sub(r'\{\{([A-Z_]+)\}\}', lambda m: values[m.group(1)], template)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--title', default='TashTech presentation')
    parser.add_argument('--purpose', choices=PURPOSES, help='Content profile; defaults to general unless a legacy mode is explicit')
    parser.add_argument('--mode', choices=MODES, help='Optional visual override; otherwise selected by purpose')
    parser.add_argument('--lang', choices=LANGUAGES, default='en')
    parser.add_argument('--motion', choices=MOTIONS, help='Motion profile; otherwise selected from the purpose')
    parser.add_argument('--footer', default='Tashkent University of Technology')
    parser.add_argument('--slides', type=Path, help='HTML fragment containing section.slide elements')
    parser.add_argument('--css', type=Path, help='Optional extra CSS; brand and stage rules still apply')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--force', action='store_true', help='Explicitly permit replacing existing output')
    args = parser.parse_args()
    try:
        if args.output.exists() and not args.force:
            raise FileExistsError(f'{args.output} exists. Choose another path or pass --force.')
        if args.output.suffix.lower() not in ('.html', '.htm'):
            raise ValueError('Output must end in .html or .htm.')
        result = build_deck(args.title, args.mode, args.lang,
                            args.slides.read_text(encoding='utf-8') if args.slides else None,
                            args.footer, args.css.read_text(encoding='utf-8') if args.css else '',
                            purpose=args.purpose, motion=args.motion)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding='utf-8')
        print(f'Created {args.output} ({len(result.encode("utf-8")):,} bytes). Run validate_deck.py before delivery.')
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
