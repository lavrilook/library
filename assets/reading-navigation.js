(() => {
  const nav = document.querySelector('.page-shortcuts');
  if (!nav) return;
  const top = nav.querySelector('[data-scroll="top"]');
  const section = nav.querySelector('[data-scroll="section"]');
  const sections = [...new Set(document.querySelectorAll(
    'main > section.category, main > section, .reading-content > .topic, main > article > section.example'
  ))];
  sections.forEach((el, i) => {
    if (!el.id) el.id = 'reading-section-' + (i + 1);
  });

  function update() {
    let current = sections[0];
    for (const el of sections) {
      if (el.getBoundingClientRect().top > 110) break;
      current = el;
    }
    if (section && current) section.href = '#' + current.id;
  }

  let queued = false;
  addEventListener('scroll', () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      update();
      queued = false;
    });
  }, { passive: true });
  addEventListener('resize', update);
  addEventListener('pageshow', update);

  if (top) top.addEventListener('click', event => {
    event.preventDefault();
    // Keep a single document scroll; delayed retries must not fight a new gesture.
    try {
      history.replaceState(history.state, '', location.pathname + location.search + '#page-top');
    } catch {}
    window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
    update();
  });
  update();
})();
