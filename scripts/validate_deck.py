#!/usr/bin/env python3
"""Check a TashTech HTML deck using only the Python standard library."""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse


class DeckParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = 0
        self.ids = []
        self.images = []
        self.resources = []
        self.language = None
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.language = a.get('lang')
        if tag == 'section' and 'slide' in a.get('class', '').split(): self.slides += 1
        if tag in ('h1','h2'): self.headings += 1
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'img': self.images.append(a)
        if tag in ('img','script','video','audio','source','iframe') and a.get('src'):
            self.resources.append(a['src'])
        if tag == 'link' and a.get('rel') in ('stylesheet','preload') and a.get('href'):
            self.resources.append(a['href'])


def static_audit(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    parser = DeckParser(); parser.feed(text)
    errors = []; warnings = []
    if not parser.slides: errors.append('No section.slide slides found.')
    for required in ('viewport','stage','controls'):
        if required not in parser.ids: errors.append(f'Missing required id: {required}')
    if not parser.language: errors.append('Missing document language (html lang).')
    if len(set(parser.ids)) != len(parser.ids): errors.append('Duplicate element IDs found.')
    if parser.headings < parser.slides: warnings.append('Some slides may lack a heading; check each slide manually.')
    for image in parser.images:
        if 'alt' not in image: errors.append('Image is missing an alt attribute.')
    resources = parser.resources + re.findall(r'url\(\s*[\"\']?([^\)\"\']+)', text)
    for resource in resources:
        resource = resource.strip()
        if resource.startswith(('data:','#','blob:')): continue
        parsed = urlparse(resource)
        if parsed.scheme in ('http','https') or resource.startswith('//'):
            errors.append(f'Remote resource breaks offline delivery: {resource[:160]}')
        elif parsed.scheme:
            errors.append(f'Unsupported resource scheme: {resource[:160]}')
        else:
            asset = (path.parent / unquote(parsed.path)).resolve()
            if not asset.is_file(): errors.append(f'Missing local resource: {resource[:160]}')
    if re.search(r'\{\{(?:asset:|TITLE\}\}|LANG\}\}|MODE\}\}|SLIDES\}\})', text):
        errors.append('Unresolved template macro found.')
    if '@font-face' in text: warnings.append('A font-face rule is present; check font licensing, offline behavior and glyph coverage.')
    if '.speaker-notes' in text: warnings.append('HTML may contain speaker notes/answers. Hidden content is readable by recipients; remove confidential notes before sharing.')
    return {'slide_count': parser.slides, 'errors': sorted(set(errors)), 'warnings': sorted(set(warnings))}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    try:
        if not args.input.is_file(): raise FileNotFoundError(args.input)
        result=static_audit(args.input)
        result['passed']=not result['errors']
        result['scope']='Static HTML structure/resource checks only; rendering, navigation, overflow, factual accuracy and accessibility require separate review.'
        rendered=json.dumps(result,ensure_ascii=False,indent=2)
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(rendered+'\n',encoding='utf-8')
        print(rendered)
        return 0 if result['passed'] else 1
    except Exception as exc:
        print(f'Error: {exc}',file=sys.stderr)
        return 2

if __name__=='__main__': raise SystemExit(main())
