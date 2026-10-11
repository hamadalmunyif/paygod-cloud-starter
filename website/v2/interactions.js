/* V2 UI only: no verification, policy or payment actions are implemented here. */
(() => {
  const rail = document.querySelector('[data-rail]');
  if (!rail) return;
  const cards = [...rail.querySelectorAll('[data-stage]')];
  const next = document.querySelector('[data-next]');
  const prev = document.querySelector('[data-prev]');
  const counter = document.querySelector('[data-counter]');
  let active = 0;
  let dragging = false;
  let pointerStart = 0;
  let startScroll = 0;
  let suppressClick = false;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function select(index, shouldScroll = true) {
    active = (index + cards.length) % cards.length;
    cards.forEach((card, i) => card.classList.toggle('is-active', i === active));
    if (counter) counter.textContent = String(active + 1).padStart(2, '0') + ' / ' + String(cards.length).padStart(2, '0');
    if (shouldScroll) cards[active].scrollIntoView({ behavior: reduced ? 'instant' : 'smooth', block: 'nearest', inline: 'center' });
  }
  next?.addEventListener('click', () => select(active + 1));
  prev?.addEventListener('click', () => select(active - 1));
  cards.forEach((card, i) => {
    card.addEventListener('focus', () => select(i, false));
    card.addEventListener('pointerenter', () => { if (!dragging) select(i, false); });
  });
  rail.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      select(active + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  /* Native touch scrolling stays enabled. Mouse drag allows desktop slide browsing. */
  rail.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'mouse' || event.button !== 0) return;
    dragging = true;
    suppressClick = false;
    pointerStart = event.clientX;
    startScroll = rail.scrollLeft;
  });
  rail.addEventListener('pointermove', event => {
    if (!dragging) return;
    const delta = event.clientX - pointerStart;
    if (Math.abs(delta) > 8) {
      suppressClick = true;
      rail.scrollLeft = startScroll - delta;
    }
  });
  function endDrag() { dragging = false; }
  rail.addEventListener('pointerup', endDrag);
  rail.addEventListener('pointercancel', endDrag);
  rail.addEventListener('pointerleave', endDrag);
  rail.addEventListener('click', event => {
    if (suppressClick) {
      event.preventDefault();
      event.stopPropagation();
      suppressClick = false;
    }
  }, true);
  select(0, false);
})();
