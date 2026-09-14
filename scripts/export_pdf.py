#!/usr/bin/env python3
"""Print a local TashTech HTML deck to a 16:9 PDF with selectable text."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys


def export_pdf(source: Path, output: Path, force: bool = False, executable: str | None = None) -> None:
    if not source.is_file(): raise FileNotFoundError(source)
    if output.suffix.lower() != '.pdf': raise ValueError('Output must end in .pdf.')
    if output.exists() and not force: raise FileExistsError(f'{output} exists; pass --force to replace it.')
    from validate_deck import static_audit, browser_audit
    static=static_audit(source)
    if static['errors']: raise ValueError('Static validation failed: '+'; '.join(static['errors']))
    validation=browser_audit(source,executable=executable)
    if validation['errors']: raise ValueError('Browser validation failed: '+'; '.join(validation['errors'][:10]))
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError('Install Playwright: python -m pip install playwright; python -m playwright install chromium') from exc
    from browser_helpers import launch_browser, wait_for_deck, serve_deck
    with sync_playwright() as pw:
        browser=launch_browser(pw,executable)
        try:
            context=browser.new_context(viewport={'width':1920,'height':1080}, reduced_motion='reduce')
            context.route(re.compile(r'^https?://'),lambda route: route.abort())
            page=context.new_page();page.set_content(source.read_text(encoding='utf-8'),wait_until='load');wait_for_deck(page)
            page.evaluate("document.querySelectorAll('details').forEach(el=>el.open=true)")
            page.evaluate("document.querySelectorAll('.slide').forEach(el=>{el.inert=false;el.setAttribute('aria-hidden','false')})")
            output.parent.mkdir(parents=True,exist_ok=True)
            page.pdf(path=str(output),width='20in',height='11.25in',prefer_css_page_size=True,
                     print_background=True,display_header_footer=False,
                     margin={'top':'0','right':'0','bottom':'0','left':'0'},tagged=True,outline=True)
            context.close()
        finally: browser.close()


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('output',type=Path,nargs='?')
    parser.add_argument('--force',action='store_true')
    parser.add_argument('--chromium')
    args=parser.parse_args()
    try:
        output=args.output or args.input.with_suffix('.pdf')
        export_pdf(args.input,output,args.force,args.chromium)
        print(f'Created {output}. Notes excluded; interactive answers expanded; animations are static.')
        return 0
    except Exception as exc:
        print(f'Error: {exc}',file=sys.stderr);return 1

if __name__=='__main__': raise SystemExit(main())
