(() => {
  const pages = [...document.querySelectorAll('section.page')];
  const names = pages.map(el => el.id.slice(2));
  function show() {
    const hash = decodeURIComponent(location.hash.slice(1) || 'home');
    if (hash === 'update' && pages.length) {
      const url = new URL('../lavri-cut-update/', location.href);
      url.searchParams.set('platform', document.body.dataset.platform || 'claude');
      location.replace(url.href);
      return;
    }
    if (!pages.length) return;
    const target = document.getElementById(hash);
    const parent = target && target.closest('.page');
    const name = names.includes(hash) ? hash : parent ? parent.id.slice(2) : 'home';
    pages.forEach(el => el.classList.toggle('on', el.id === 'p-' + name));
    document.querySelectorAll('.tabs a[data-page]').forEach(a => {
      if (a.dataset.page === name) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    if (target && !names.includes(hash)) target.scrollIntoView({ block: 'start', behavior: 'instant' });
    else window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
  }
  addEventListener('hashchange', show);
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (link && link.hash === location.hash && pages.length) {
      event.preventDefault();
      show();
    }
    const button = event.target.closest('.copy');
    if (!button) return;
    const pre = button.closest('.copybox').querySelector('pre');
    const done = () => {
      const original = button.textContent;
      button.textContent = 'Скопировано ✓';
      setTimeout(() => { button.textContent = original; }, 1800);
    };
    const select = () => {
      const range = document.createRange(); range.selectNodeContents(pre);
      const selection = getSelection(); selection.removeAllRanges(); selection.addRange(range);
      button.textContent = 'Выделено — скопируйте';
    };
    if (navigator.clipboard) navigator.clipboard.writeText(pre.textContent).then(done, select);
    else select();
  });
  show();
})();
