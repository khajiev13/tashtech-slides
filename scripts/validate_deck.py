#!/usr/bin/env python3
"""Check a TashTech HTML deck. --browser adds offline Chromium layout checks."""
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


LAYOUT_JS = r'''() => {
  const slide=document.querySelector('.slide.active'), stage=document.getElementById('stage');
  const stageRect=stage.getBoundingClientRect(), view=document.getElementById('viewport').getBoundingClientRect();
  const issues=[];
  if(!slide) return ['No active slide'];
  const scale=stageRect.width / 1920;
  const label=el => (el.tagName.toLowerCase()+' '+(el.className?.baseVal || el.className || '')+' '+el.textContent.trim().slice(0,65)).trim();
  if(Math.abs(stageRect.width/stageRect.height-16/9)>0.002) issues.push('Stage is not 16:9');
  if(stageRect.left<view.left-2 || stageRect.right>view.right+2 || stageRect.top<view.top-2 || stageRect.bottom>view.bottom+2) issues.push('Stage falls outside viewport');
  const visible=el => { const c=getComputedStyle(el);return c.display!=='none' && c.visibility!=='hidden' && el.getBoundingClientRect().width>0; };
  slide.querySelectorAll('img').forEach(el=>{ if(!el.complete || !el.naturalWidth) issues.push('Broken image: '+el.alt); });
  const tracked=[...slide.querySelectorAll('[data-fit], [data-panel], .panel, h1,h2,h3,p,pre,table,img,.slide-header,.slide-footer,.flow,.timeline')];
  tracked.filter(visible).forEach(el=>{
    const r=el.getBoundingClientRect(), tolerance=3*scale;
    if(el.closest('.speaker-notes') || el.hasAttribute('data-allow-overlap')) return;
    if(r.left<stageRect.left-tolerance || r.right>stageRect.right+tolerance || r.top<stageRect.top-tolerance || r.bottom>stageRect.bottom+tolerance) issues.push('Outside slide: '+label(el));
    if(el.clientHeight>0 && el.scrollHeight>el.clientHeight+4) issues.push('Vertical overflow: '+label(el));
    if(el.clientWidth>0 && el.scrollWidth>el.clientWidth+4) issues.push('Horizontal overflow: '+label(el));
  });
  const panels=[...slide.querySelectorAll('[data-panel], .panel')].filter(visible);
  for(let i=0;i<panels.length;i++) for(let j=i+1;j<panels.length;j++) {
    const a=panels[i],b=panels[j];
    if(a.parentElement!==b.parentElement || a.hasAttribute('data-allow-overlap') || b.hasAttribute('data-allow-overlap')) continue;
    const ra=a.getBoundingClientRect(),rb=b.getBoundingClientRect();
    if(Math.min(ra.right,rb.right)-Math.max(ra.left,rb.left)>3*scale && Math.min(ra.bottom,rb.bottom)-Math.max(ra.top,rb.top)>3*scale) issues.push('Sibling panels overlap: '+label(a)+' / '+label(b));
  }
  const footer=slide.querySelector('.slide-footer');
  if(footer) {
    const ft=footer.getBoundingClientRect().top;
    slide.querySelectorAll('.slide-main > *').forEach(el=>{
      if(visible(el) && el.getBoundingClientRect().bottom>ft-6*scale) issues.push('Content intrudes into footer: '+label(el));
    });
  }
  return [...new Set(issues)];
}'''


def browser_audit(path: Path, screenshot_dir: Path | None = None, executable: str | None = None) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError('Browser checks need Playwright: python -m pip install playwright; python -m playwright install chromium') from exc
    from browser_helpers import launch_browser, wait_for_deck, serve_deck
    errors = []; viewports = []; requests = []
    with sync_playwright() as pw:
        browser = launch_browser(pw, executable)
        try:
            context = browser.new_context(viewport={'width':1920,'height':1080}, reduced_motion='reduce')
            context.route(re.compile(r'^https?://'), lambda route: (requests.append(route.request.url), route.abort()))
            page = context.new_page()
            page.on('pageerror',lambda exc: errors.append(f'JavaScript: {exc}'))
            page.set_content(path.read_text(encoding='utf-8'), wait_until='load')
            wait_for_deck(page)
            count=page.evaluate('window.TashTechDeck.count')
            # Open interactive answers: final content must also fit in printable state.
            page.evaluate("document.querySelectorAll('details').forEach(el => el.open=true)")
            for width,height in [(1920,1080),(1280,720),(390,844)]:
                page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(80)
                start=len(errors)
                for i in range(count):
                    page.evaluate('(n) => window.TashTechDeck.goTo(n)',i)
                    page.wait_for_timeout(15)
                    errors.extend(f'{width}x{height} slide {i+1}: {issue}' for issue in page.evaluate(LAYOUT_JS))
                    if screenshot_dir and width == 1920:
                        screenshot_dir.mkdir(parents=True,exist_ok=True)
                        page.locator('#stage').screenshot(path=str(screenshot_dir/f'slide-{i+1:02}.png'))
                viewports.append({'width':width,'height':height,'slides_checked':count,'errors':len(errors)-start})
            page.evaluate('window.TashTechDeck.goTo(0)');page.keyboard.press('ArrowRight')
            expected=1 if count>1 else 0
            if page.evaluate('window.TashTechDeck.index')!=expected: errors.append('Right-arrow navigation failed.')
            page.keyboard.press('Home')
            if page.evaluate('window.TashTechDeck.index')!=0: errors.append('Home navigation failed.')
            page.keyboard.press('End')
            if page.evaluate('window.TashTechDeck.index')!=count-1: errors.append('End navigation failed.')
            page.keyboard.press('n')
            if page.locator('#notes-panel').is_hidden(): errors.append('Notes keyboard toggle failed.')
            page.keyboard.press('Escape')
            if not page.locator('#notes-panel').is_hidden(): errors.append('Escape did not close notes.')
            if requests: errors.append('Unexpected remote requests: '+', '.join(sorted(set(requests))))
            context.close()
        finally:
            browser.close()
    return {'errors':errors,'viewports':viewports,'offline_network_requests':len(requests)}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--browser',action='store_true')
    parser.add_argument('--screenshots',type=Path)
    parser.add_argument('--report',type=Path)
    parser.add_argument('--chromium',help='Explicit Chromium executable path')
    args=parser.parse_args()
    try:
        if not args.input.is_file(): raise FileNotFoundError(args.input)
        result=static_audit(args.input)
        if args.browser:
            rendered=browser_audit(args.input,args.screenshots,args.chromium)
            result['browser']=rendered
            result['errors'].extend(rendered['errors'])
        result['passed']=not result['errors']
        result['scope']='Heuristic structure/layout checks; does not certify factual accuracy, contrast, semantic accessibility or every overlap.'
        rendered=json.dumps(result,ensure_ascii=False,indent=2)
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(rendered+'\n',encoding='utf-8')
        print(rendered)
        return 0 if result['passed'] else 1
    except Exception as exc:
        print(f'Error: {exc}',file=sys.stderr)
        return 2

if __name__=='__main__': raise SystemExit(main())
