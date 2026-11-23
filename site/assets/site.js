(() => {
  'use strict';
  const current = document.body.dataset.page;
  document.querySelectorAll('[data-nav]').forEach(link => {
    if (link.dataset.nav === current) link.setAttribute('aria-current','page');
  });
  if (current !== 'atlas') return;
  const grid = document.getElementById('diagram-grid');
  const search = document.getElementById('diagram-search');
  const category = document.getElementById('category-filter');
  const count = document.getElementById('results-count');
  const empty = document.getElementById('empty-results');
  const dialog = document.getElementById('diagram-detail');
  const params = new URLSearchParams(location.search);
  let items = [];

  function show(item) {
    document.getElementById('detail-category').textContent = `${item.category} / LAYER ${item.level}`;
    document.getElementById('detail-title').textContent = item.title;
    document.getElementById('detail-description').textContent = item.description;
    const image = document.getElementById('detail-image');
    image.src = item.svg;
    image.alt = item.title + ' diagram';
    document.getElementById('detail-svg').href = item.svg;
    document.getElementById('detail-source').href = item.source;
    dialog.showModal();
    const next = new URL(location.href); next.searchParams.set('diagram', item.id);
    history.replaceState(null, '', next);
  }
  document.getElementById('close-detail').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {if (event.target === dialog) dialog.close();});
  dialog.addEventListener('close', () => {
    const next = new URL(location.href); next.searchParams.delete('diagram');
    history.replaceState(null, '', next);
  });
  function render() {
    const term = search.value.trim().toLowerCase();
    const filtered = items.filter(item => (!category.value || category.value === item.category) &&
      (!term || `${item.title} ${item.category} ${item.description}`.toLowerCase().includes(term)));
    grid.replaceChildren();
    for (const item of filtered) {
      const button = document.createElement('button'); button.className = 'diagram-card'; button.type = 'button';
      const image = document.createElement('img'); image.src = item.svg; image.loading = 'lazy'; image.alt = item.title;
      const content = document.createElement('div'); content.className = 'card-content';
      const tag = document.createElement('span'); tag.className = 'tag'; tag.textContent = `${item.category.toUpperCase()} · ${item.level}`;
      const h3 = document.createElement('h3'); h3.textContent = item.title;
      const p = document.createElement('p'); p.textContent = item.description;
      const open = document.createElement('span'); open.className = 'open'; open.textContent = 'Open diagram ↗';
      content.append(tag,h3,p,open); button.append(image,content); button.addEventListener('click', () => show(item)); grid.append(button);
    }
    count.textContent = `${filtered.length} of ${items.length} diagrams`;
    empty.hidden = filtered.length !== 0;
  }
  fetch('diagrams/catalog.json').then(response => {
    if (!response.ok) throw new Error('Catalog could not be loaded');
    return response.json();
  }).then(data => {
    items = data;
    for (const value of [...new Set(items.map(item => item.category))]) {
      const option = document.createElement('option'); option.value = value; option.textContent = value; category.append(option);
    }
    const selected = params.get('category'); if (selected) category.value = selected;
    search.addEventListener('input', render); category.addEventListener('change', render);
    render();
    const initial = items.find(item => item.id === params.get('diagram'));
    if (initial) show(initial);
  }).catch(error => {count.textContent = error.message;});
})();
