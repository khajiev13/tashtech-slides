/* TashTech Slides runtime — no requests, analytics or dependencies.
   Frontend-slides-inspired interactions: motion, fragments, wheel/swipe nav,
   hover-revealed editor, autosave, tilt, parallax and counter animation. */
(() => {
  'use strict';
  const doc = document;
  const html = doc.documentElement;
  const viewport = doc.getElementById('viewport');
  const stage = doc.getElementById('stage');
  const slides = [...doc.querySelectorAll('#stage > .slide')];
  const counter = doc.getElementById('counter');
  const notesPanel = doc.getElementById('notes-panel');
  const notesBody = doc.getElementById('notes-body');
  const status = doc.getElementById('live-status');
  const previousButton = doc.getElementById('previous');
  const nextButton = doc.getElementById('next');
  const notesToggle = doc.getElementById('notes-toggle');
  const editToggle = doc.getElementById('edit-toggle');
  const saveButton = doc.getElementById('save-html');
  const fullscreenButton = doc.getElementById('fullscreen');
  const hotzone = doc.querySelector('.edit-hotzone');
  const labels = ({
    en: {prev:'Previous',next:'Next',notes:'Notes',edit:'Edit',save:'Save HTML',full:'Full screen',notesTitle:'Speaker notes',warning:'Visible on this screen. Not a private presenter display.',empty:'No speaker notes for this slide.',slide:'Slide',restore:'Draft restored from browser autosave.'},
    uz: {prev:'Oldingi',next:'Keyingi',notes:'Izohlar',edit:'Tahrirlash',save:'HTML saqlash',full:'To‘liq ekran',notesTitle:'O‘qituvchi izohlari',warning:'Ushbu ekranda ko‘rinadi. Bu alohida maxfiy oynacha emas.',empty:'Bu slayd uchun izoh yo‘q.',slide:'Slayd',restore:'Brauzerdagi avtomatik saqlangan nusxa tiklandi.'},
    ru: {prev:'Назад',next:'Далее',notes:'Заметки',edit:'Правка',save:'Сохранить HTML',full:'Полный экран',notesTitle:'Заметки докладчика',warning:'Видны на этом экране. Это не приватный режим докладчика.',empty:'Для этого слайда нет заметок.',slide:'Слайд',restore:'Черновик восстановлен из автосохранения браузера.'}
  })[html.lang] || {prev:'Previous',next:'Next',notes:'Notes',edit:'Edit',save:'Save HTML',full:'Full screen',notesTitle:'Speaker notes',warning:'Visible on this screen.',empty:'No notes.',slide:'Slide',restore:'Draft restored.'};
  doc.querySelectorAll('[data-ui]').forEach(el => { el.textContent = labels[el.dataset.ui] || el.textContent; });

  const motion = (doc.body.dataset.motion || 'subtle').toLowerCase();
  const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const autosaveKey = 'tashtech-slides::autosave::' + (doc.body.dataset.autosave || doc.title || 'deck');
  let index = 0;
  let editing = false;
  let touch = null;
  let wheelLock = false;
  let hideTimeout = null;
  let autosaveTimeout = null;
  let currentParallax = null;

  const canAnimate = () => motion !== 'none' && !reduceMotion;
  const hashIndex = () => {
    const match = location.hash.match(/^#slide-(\d+)$/);
    return match ? Number(match[1]) - 1 : 0;
  };
  const stageScale = () => {
    const s = Math.min(viewport.clientWidth / 1920, viewport.clientHeight / 1080);
    stage.style.setProperty('--deck-scale', String(s));
  };
  const byStep = (a, b) => {
    const av = Number(a.dataset.step || Number.MAX_SAFE_INTEGER);
    const bv = Number(b.dataset.step || Number.MAX_SAFE_INTEGER);
    return av === bv ? 0 : av - bv;
  };
  const getFragments = (slide) => [...slide.querySelectorAll('.fragment,[data-step]')].sort(byStep);
  const getFragmentIndex = (slide) => Number(slide.dataset.fragmentIndex || '-1');
  const applyFragments = (slide, upto) => {
    const fragments = getFragments(slide);
    fragments.forEach((node, i) => {
      const visible = i <= upto;
      node.classList.toggle('fragment-visible', visible);
      node.setAttribute('aria-hidden', String(!visible));
      if (node.tagName === 'DETAILS' && visible && node.dataset.autoOpen !== 'false') node.open = true;
      if (node.tagName === 'DETAILS' && !visible && node.dataset.autoOpen !== 'false') node.open = false;
    });
    slide.dataset.fragmentIndex = String(upto);
    return fragments.length;
  };
  const resetSlideState = (slide) => {
    slide.classList.remove('active', 'visible', 'leaving');
    slide.setAttribute('aria-hidden', 'true');
    slide.inert = true;
    applyFragments(slide, -1);
    slide.querySelectorAll('[data-count-to]').forEach(node => {
      node.textContent = node.dataset.countFrom || '0';
      delete node.dataset.countAnimated;
    });
  };
  const animateCounters = (slide) => {
    slide.querySelectorAll('[data-count-to]').forEach(node => {
      if (node.dataset.countAnimated === 'true') return;
      const from = Number(node.dataset.countFrom || '0');
      const to = Number(node.dataset.countTo || node.getAttribute('data-count-to') || '0');
      const decimals = Number(node.dataset.countDecimals || '0');
      const suffix = node.dataset.countSuffix || '';
      const duration = Math.max(250, Number(node.dataset.countDuration || (motion === 'expressive' ? 1100 : 700)));
      node.dataset.countAnimated = 'true';
      if (!canAnimate()) {
        node.textContent = to.toFixed(decimals) + suffix;
        return;
      }
      const start = performance.now();
      const tick = (now) => {
        const t = Math.min(1, (now - start) / duration);
        const eased = 1 - Math.pow(1 - t, 3);
        const value = from + (to - from) * eased;
        node.textContent = value.toFixed(decimals) + suffix;
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  };
  const updateNotes = () => {
    const text = slides[index]?.querySelector('.speaker-notes')?.textContent.trim();
    notesBody.textContent = text || labels.empty;
    notesBody.style.whiteSpace = 'pre-wrap';
  };
  const updateStatus = () => {
    const title = slides[index].dataset.title || slides[index].querySelector('h1,h2')?.textContent || '';
    status.textContent = `${labels.slide} ${index + 1}: ${title}`;
  };
  const updateControls = () => {
    counter.textContent = `${index + 1} / ${slides.length}`;
    previousButton.disabled = index === 0 && getFragmentIndex(slides[index]) < 0;
    const totalFragments = getFragments(slides[index]).length;
    nextButton.disabled = index === slides.length - 1 && getFragmentIndex(slides[index]) >= totalFragments - 1;
  };
  const updateHash = () => {
    try { history.replaceState(null, '', `#slide-${index + 1}`); }
    catch (_) { location.hash = `slide-${index + 1}`; }
  };
  const activateSlide = (slide) => {
    slide.classList.remove('leaving');
    slide.classList.add('active');
    slide.setAttribute('aria-hidden', 'false');
    slide.inert = false;
    void slide.offsetWidth;
    requestAnimationFrame(() => slide.classList.add('visible'));
    applyFragments(slide, -1);
    animateCounters(slide);
    enableParallax(slide);
  };
  const showSlide = (n, updateHashValue = true) => {
    if (!slides.length) return;
    const nextIndex = Math.max(0, Math.min(slides.length - 1, Number.isFinite(n) ? Math.floor(n) : 0));
    if (slides[index] && slides[index] !== slides[nextIndex]) {
      const previous = slides[index];
      previous.classList.remove('visible');
      previous.classList.add('leaving');
      previous.inert = true;
      window.setTimeout(() => { if (!previous.classList.contains('active')) previous.classList.remove('leaving'); }, canAnimate() ? 400 : 0);
    }
    slides.forEach((slide, i) => {
      if (i !== nextIndex) resetSlideState(slide);
    });
    index = nextIndex;
    activateSlide(slides[index]);
    updateNotes();
    updateStatus();
    updateControls();
    if (updateHashValue) updateHash();
  };
  const revealNext = () => {
    const slide = slides[index];
    const fragments = getFragments(slide);
    const current = getFragmentIndex(slide);
    if (current < fragments.length - 1) {
      applyFragments(slide, current + 1);
      updateControls();
      return true;
    }
    return false;
  };
  const revealPrevious = () => {
    const slide = slides[index];
    const current = getFragmentIndex(slide);
    if (current >= 0) {
      applyFragments(slide, current - 1);
      updateControls();
      return true;
    }
    return false;
  };
  const next = () => { if (!revealNext()) showSlide(index + 1); };
  const previous = () => { if (!revealPrevious()) showSlide(index - 1); };
  const setNotes = (open) => {
    notesPanel.hidden = !open;
    notesToggle.setAttribute('aria-pressed', String(open));
    updateNotes();
  };
  const queueAutosave = () => {
    clearTimeout(autosaveTimeout);
    autosaveTimeout = window.setTimeout(() => {
      try { window.localStorage.setItem(autosaveKey, serialize()); }
      catch (_) { /* ignore quota/private mode issues */ }
    }, 200);
  };
  const setEdit = (enabled) => {
    editing = Boolean(enabled);
    doc.body.classList.toggle('editing', editing);
    editToggle.classList.toggle('active', editing);
    editToggle.setAttribute('aria-pressed', String(editing));
    doc.querySelectorAll('[data-editable]').forEach(el => {
      if (editing) {
        el.setAttribute('contenteditable', 'plaintext-only');
        el.setAttribute('spellcheck', 'true');
      } else {
        el.removeAttribute('contenteditable');
        el.removeAttribute('spellcheck');
      }
    });
    if (!editing) queueAutosave();
  };
  const serialize = () => {
    const copy = html.cloneNode(true);
    const body = copy.querySelector('body');
    body.classList.remove('editing');
    copy.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
    copy.querySelector('#notes-panel').setAttribute('hidden', '');
    copy.querySelector('#edit-toggle').classList.remove('show', 'active');
    copy.querySelectorAll('#stage > .slide').forEach((slide, i) => {
      slide.classList.toggle('active', i === 0);
      slide.classList.toggle('visible', i === 0);
      slide.classList.remove('leaving');
      slide.setAttribute('aria-hidden', String(i !== 0));
      if (i === 0) slide.removeAttribute('inert'); else slide.setAttribute('inert', '');
      slide.dataset.fragmentIndex = '-1';
      [...slide.querySelectorAll('.fragment,[data-step]')].forEach(fragment => {
        fragment.classList.remove('fragment-visible');
        fragment.setAttribute('aria-hidden', 'true');
        if (fragment.tagName === 'DETAILS' && fragment.dataset.autoOpen !== 'false') fragment.removeAttribute('open');
      });
    });
    copy.querySelector('#stage').removeAttribute('style');
    copy.querySelectorAll('[aria-pressed]').forEach(el => el.setAttribute('aria-pressed', 'false'));
    return '<!DOCTYPE html>\n' + copy.outerHTML;
  };
  const save = () => {
    const url = URL.createObjectURL(new Blob([serialize()], {type:'text/html;charset=utf-8'}));
    const link = doc.createElement('a');
    link.href = url;
    link.download = (doc.title.replace(/[^\p{L}\p{N} _-]/gu, '').trim() || 'tashtech-slides') + '.html';
    link.click();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  const fullScreen = async () => {
    try {
      if (doc.fullscreenElement) await doc.exitFullscreen();
      else await doc.documentElement.requestFullscreen();
    } catch (_) {
      status.textContent = 'Full screen is unavailable in this browser context.';
    }
  };
  const maybeRestoreAutosave = () => {
    try {
      const saved = window.localStorage.getItem(autosaveKey);
      const current = '<!DOCTYPE html>\n' + html.outerHTML;
      if (!saved || saved === current || window.sessionStorage.getItem(autosaveKey + '::restored') === '1') return;
      window.sessionStorage.setItem(autosaveKey + '::restored', '1');
      doc.open();
      doc.write(saved);
      doc.close();
      return true;
    } catch (_) {
      return false;
    }
    return false;
  };

  class TiltEffect {
    constructor(element) {
      this.element = element;
      this.element.addEventListener('mousemove', this.onMove.bind(this));
      this.element.addEventListener('mouseleave', this.onLeave.bind(this));
      this.element.addEventListener('mouseenter', () => this.element.classList.add('tilting'));
    }
    onMove(e) {
      if (!canAnimate()) return;
      const rect = this.element.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      this.element.style.setProperty('--tilt-x', `${(-y * 8).toFixed(2)}deg`);
      this.element.style.setProperty('--tilt-y', `${(x * 10).toFixed(2)}deg`);
    }
    onLeave() {
      this.element.classList.remove('tilting');
      this.element.style.removeProperty('--tilt-x');
      this.element.style.removeProperty('--tilt-y');
    }
  }
  const enableParallax = (slide) => {
    if (currentParallax) viewport.removeEventListener('pointermove', currentParallax);
    const nodes = [...slide.querySelectorAll('[data-parallax]')];
    if (!nodes.length || !canAnimate()) return;
    currentParallax = (event) => {
      const rect = viewport.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      nodes.forEach(node => {
        const depth = Number(node.dataset.parallax || '16');
        node.style.transform = `translate(${(x * depth).toFixed(1)}px, ${(y * depth).toFixed(1)}px)`;
      });
    };
    viewport.addEventListener('pointermove', currentParallax);
  };

  if (maybeRestoreAutosave()) return;

  slides.forEach((slide, i) => {
    slide.id = `slide-${i + 1}`;
    slide.setAttribute('role', 'group');
    slide.setAttribute('aria-roledescription', 'slide');
    slide.setAttribute('aria-label', `${i + 1} / ${slides.length}`);
    slide.dataset.fragmentIndex = '-1';
    const footer = slide.querySelector('.page-number');
    if (footer) footer.textContent = String(i + 1).padStart(2, '0');
    slide.querySelectorAll('[data-count-to]').forEach(node => {
      node.textContent = node.dataset.countFrom || '0';
    });
    slide.querySelectorAll('[data-tilt]').forEach(node => new TiltEffect(node));
  });

  previousButton.addEventListener('click', previous);
  nextButton.addEventListener('click', next);
  notesToggle.addEventListener('click', () => setNotes(notesPanel.hidden));
  editToggle.addEventListener('click', () => setEdit(!editing));
  saveButton.addEventListener('click', save);
  fullscreenButton.addEventListener('click', fullScreen);
  doc.addEventListener('input', (event) => { if (editing && event.target.closest('[data-editable]')) queueAutosave(); });
  doc.addEventListener('keydown', event => {
    const textInput = event.target.closest('input,textarea,[contenteditable]');
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 's') { event.preventDefault(); save(); return; }
    if (event.key === 'Escape') { setNotes(false); setEdit(false); return; }
    if (textInput || event.ctrlKey || event.metaKey || event.altKey) return;
    if (['ArrowRight', 'ArrowDown', 'PageDown'].includes(event.key) || (event.key === ' ' && !event.shiftKey)) { event.preventDefault(); next(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(event.key) || (event.key === ' ' && event.shiftKey)) { event.preventDefault(); previous(); }
    else if (event.key === 'Home') { event.preventDefault(); showSlide(0); }
    else if (event.key === 'End') { event.preventDefault(); showSlide(slides.length - 1); }
    else if (event.key.toLowerCase() === 'n') setNotes(notesPanel.hidden);
    else if (event.key.toLowerCase() === 'e') setEdit(!editing);
    else if (event.key.toLowerCase() === 'f') fullScreen();
  });
  viewport.addEventListener('touchstart', e => {
    if (!editing && !e.target.closest('a,button,summary,details')) touch = {x:e.changedTouches[0].clientX, y:e.changedTouches[0].clientY};
  }, {passive:true});
  viewport.addEventListener('touchend', e => {
    if (!touch) return;
    const dx = e.changedTouches[0].clientX - touch.x;
    const dy = e.changedTouches[0].clientY - touch.y;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) (dx < 0 ? next : previous)();
    touch = null;
  }, {passive:true});
  viewport.addEventListener('wheel', e => {
    if (wheelLock || editing || e.target.closest('[contenteditable],summary,details')) return;
    if (Math.abs(e.deltaY) < 18) return;
    e.preventDefault();
    wheelLock = true;
    (e.deltaY > 0 ? next : previous)();
    window.setTimeout(() => { wheelLock = false; }, 420);
  }, {passive:false});

  if (hotzone) {
    hotzone.addEventListener('mouseenter', () => { clearTimeout(hideTimeout); editToggle.classList.add('show'); });
    hotzone.addEventListener('mouseleave', () => {
      hideTimeout = window.setTimeout(() => { if (!editing) editToggle.classList.remove('show'); }, 400);
    });
    hotzone.addEventListener('click', () => setEdit(!editing));
    editToggle.addEventListener('mouseenter', () => clearTimeout(hideTimeout));
    editToggle.addEventListener('mouseleave', () => {
      hideTimeout = window.setTimeout(() => { if (!editing) editToggle.classList.remove('show'); }, 400);
    });
  }

  let printState = [];
  window.addEventListener('beforeprint', () => {
    printState = [...doc.querySelectorAll('details')].map(el => [el, el.open]);
    printState.forEach(([el]) => el.open = true);
    slides.forEach(slide => {
      slide.inert = false;
      slide.setAttribute('aria-hidden', 'false');
      slide.classList.add('active', 'visible');
      const fragments = getFragments(slide);
      if (fragments.length) applyFragments(slide, fragments.length - 1);
      slide.querySelectorAll('[data-count-to]').forEach(node => {
        const to = Number(node.dataset.countTo || '0');
        const decimals = Number(node.dataset.countDecimals || '0');
        node.textContent = to.toFixed(decimals) + (node.dataset.countSuffix || '');
      });
    });
  });
  window.addEventListener('afterprint', () => {
    printState.forEach(([el, open]) => el.open = open);
    showSlide(index, false);
  });
  window.addEventListener('hashchange', () => showSlide(hashIndex(), false));
  window.addEventListener('resize', stageScale);
  if (window.ResizeObserver) new ResizeObserver(stageScale).observe(viewport);

  window.TashTechDeck = {
    goTo: (i) => showSlide(i),
    next, previous, setNotes, setEdit, serialize,
    revealNext, revealPrevious,
    get index() { return index; },
    get count() { return slides.length; },
    get motion() { return motion; },
    get editing() { return editing; }
  };

  showSlide(hashIndex(), false);
  stageScale();
  if (canAnimate()) window.setTimeout(() => {
    try { status.textContent = labels.restore && window.sessionStorage.getItem(autosaveKey + '::restored') === '1' ? labels.restore : status.textContent; }
    catch (_) { /* ignore */ }
  }, 30);
})();
