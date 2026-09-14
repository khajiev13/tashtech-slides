"""Optional Playwright helpers. No downloads, no implicit package installation."""
from __future__ import annotations
import os
import shutil
from pathlib import Path


def launch_browser(playwright, executable: str | None = None):
    candidate = executable or os.environ.get('TT_CHROMIUM_BINARY')
    if not candidate and not Path(playwright.chromium.executable_path).exists():
        candidate = next((p for name in ('chromium', 'chromium-browser', 'google-chrome', 'chrome')
                          if (p := shutil.which(name))), None)
    kwargs = {'headless': True}
    if candidate:
        if not Path(candidate).is_file():
            raise ValueError(f'Chromium executable not found: {candidate}')
        kwargs['executable_path'] = candidate
    try:
        return playwright.chromium.launch(**kwargs)
    except Exception as exc:
        raise RuntimeError('Chromium did not start. Install it with: python -m playwright install chromium; '
                           'or set TT_CHROMIUM_BINARY to an existing browser executable. ' + str(exc)) from exc


def wait_for_deck(page):
    page.wait_for_function('window.TashTechDeck && window.TashTechDeck.count > 0', timeout=10000)
    page.evaluate('document.fonts.ready')
    page.evaluate('''async () => { await Promise.all([...document.images].map(image => image.decode().catch(() => {}))); }''')
    page.wait_for_timeout(80)

# Headless/managed Chromium may disallow file://. Serve only on loopback,
# only for the lifetime of a validation/export call; no public deployment.
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import quote

@contextmanager
def serve_deck(path: Path):
    root = path.resolve().parent
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, *_args):
            pass
        def send_head(self):
            resolved = Path(self.translate_path(self.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                self.send_error(404)
                return None
            return super().send_head()
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(root)))
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}/{quote(path.name)}'
    finally:
        server.shutdown(); server.server_close(); worker.join(timeout=2)
