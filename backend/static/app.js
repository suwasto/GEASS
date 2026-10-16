/* All evidence comes from the same-origin API; browser code never calculates prices. */
'use strict';
const $ = id => document.getElementById(id);
const state = {page: 1, pageSize: 5, request: 0, caseRequest: 0, opener: null};
const el = (tag, text, className) => {
  const node = document.createElement(tag);
  if (text !== undefined && text !== null) node.textContent = String(text);
  if (className) node.className = className;
  return node;
};
function money(value) {
  if (value === null || value === undefined) return 'Unavailable';
  const raw = String(value);
  if (!/^-?\d+(?:\.\d+)?$/.test(raw)) return 'Unavailable';
  const [whole, fraction] = raw.split('.');
  return 'IDR ' + whole.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (fraction && /[1-9]/.test(fraction) ? '.' + fraction : '');
}
function readable(value) {
  if (value === null || value === undefined) return 'Not available';
  if (typeof value === 'string') return value;
  return JSON.stringify(value, null, 2);
}
async function api(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`Request failed (${response.status}). Please try again.`);
  return response.json();
}
function announce(message) { $('announcement').textContent = message; }
function errorMessage(container, message, retry) {
  container.replaceChildren(el('p', message));
  if (retry) {
    const button = el('button', 'Try again', 'button compact');
    button.onclick = retry;
    container.append(button);
  }
}
function options(id, values) {
  const select = $(id), current = select.value;
  const existing = new Set(Array.from(select.options).map(option => option.value));
  for (const value of values || []) {
    if (typeof value !== 'string' || existing.has(value)) continue;
    const option = el('option', value); option.value = value; select.append(option);
  }
  select.value = current;
}
async function loadPackages() {
  const request = ++state.request;
  const query = new URLSearchParams(new FormData($('filters')));
  for (const [key, value] of Array.from(query)) if (!value) query.delete(key);
  query.set('page', state.page); query.set('page_size', state.pageSize);
  $('package-rows').replaceChildren();
  $('radar-message').hidden = false;
  $('radar-message').classList.remove('error');
  $('radar-message').textContent = 'Loading packages…';
  $('previous').disabled = $('next').disabled = true;
  try {
    const data = await api('/api/packages?' + query);
    if (request !== state.request) return;
    options('region', data.regions); options('agency', data.agencies);
    $('package-count').textContent = data.total;
    $('radar-message').hidden = data.items.length > 0;
    $('radar-message').textContent = 'No packages match these filters. Try another search or clear a filter.';
    for (const item of data.items) {
      const row = el('tr'), title = el('td'), agency = el('td'), amount = el('td', money(item.total_pagu), 'numeric');
      const button = el('button', item.nama_paket, 'package-link');
      button.onclick = () => openCase(item.id_rup, button);
      title.append(button, el('span', item.normalized_item || item.id_rup, 'subline'));
      if (item.normalized_item) title.append(el('span', item.id_rup, 'subline'));
      agency.append(el('span', item.satker), el('span', item.region, 'subline'));
      const signal = el('td');
      signal.append(el('span', item.classification || 'Not assessed', 'badge' + (item.classification === 'NORMAL' ? ' normal' : '')));
      const evidence = el('td'); evidence.append(el('span', item.synthetic ? 'Synthetic fixture' : item.evidence_status, 'quiet'));
      const comparison = el('td', null, 'numeric');
      if (item.price_forensics?.status === 'grounded') {
        comparison.append(el('span', money(item.price_forensics.implied_unit_price)), el('span', 'Cap ' + money(item.price_forensics.benchmark_unit_price), 'subline'), el('span', 'Δ ' + money(item.price_forensics.delta_idr) + ' / ' + item.price_forensics.delta_percent + '%', 'subline'));
      } else comparison.append(el('span', 'Ungrounded', 'quiet'), el('span', 'Inspect missing evidence', 'subline'));
      row.append(title, agency, amount, comparison, signal, evidence); $('package-rows').append(row);
    }
    const start = data.total ? (data.page - 1) * data.page_size + 1 : 0;
    $('page-summary').textContent = `${start}–${Math.min(data.page * data.page_size, data.total)} of ${data.total} packages · Page ${data.page}`;
    $('previous').disabled = data.page <= 1;
    $('next').disabled = data.page * data.page_size >= data.total;
    announce(`${data.total} matching packages loaded.`);
  } catch (error) {
    if (request !== state.request) return;
    $('package-count').textContent = '—'; $('page-summary').textContent = 'Packages unavailable';
    $('radar-message').classList.add('error'); errorMessage($('radar-message'), error.message, loadPackages);
  }
}
function section(title) {
  const node = el('section', null, 'case-section'); node.append(el('h3', title)); return node;
}
function listEvidence(title, values) {
  const node = el('div'); node.append(el('h3', title));
  if (!values || !values.length) node.append(el('p', 'No evidence recorded in this fixture.'));
  else {
    const list = el('ul');
    for (const value of values) list.append(el('li', readable(value)));
    node.append(list);
  }
  return node;
}
function provenance(container, data) {
  container.append(el('pre', readable(data), 'source-data'));
  // Only explicit HTTP(S) source locators become clickable; fixture:// remains plain text.
  const links = el('div', null, 'source-links');
  function walk(value) {
    if (typeof value === 'string' && /^https?:\/\//i.test(value)) {
      try {
        const url = new URL(value);
        if (!['http:', 'https:'].includes(url.protocol)) return;
        const a = el('a', 'Open source: ' + url.hostname); a.href = url.href; a.target = '_blank'; a.rel = 'noopener noreferrer'; links.append(a);
      } catch (_) { /* A malformed locator remains visible as text. */ }
    } else if (Array.isArray(value)) value.forEach(walk);
    else if (value && typeof value === 'object') Object.values(value).forEach(walk);
  }
  walk(data); if (links.childNodes.length) container.append(links);
}
async function openCase(id, opener) {
  const request = ++state.caseRequest;
  if (opener) state.opener = opener;
  const dialog = $('investigation'), content = $('case-content');
  const heading = el('h2', 'Loading investigation…'); heading.id = 'case-title'; content.replaceChildren(heading);
  if (!dialog.open) dialog.showModal();
  $('close-case').focus();
  try {
    const item = await api('/api/packages/' + encodeURIComponent(id));
    if (!dialog.open || request !== state.caseRequest) return;
    renderCase(item);
  } catch (error) {
    if (!dialog.open || request !== state.caseRequest) return;
    heading.textContent = 'Investigation unavailable';
    const result = el('div'); errorMessage(result, error.message, () => openCase(id)); content.append(result);
  }
}
function renderCase(item) {
  const content = $('case-content'); content.replaceChildren();
  content.append(el('span', item.classification || 'Not assessed', 'badge' + (item.classification === 'NORMAL' ? ' normal' : '')));
  const title = el('h2', item.nama_paket); title.id = 'case-title'; content.append(title);
  content.append(el('div', `${item.id_rup} / ${item.satker} / ${item.region} / ${item.tahun_anggaran}`, 'case-meta'));
  if (item.normalized_item) content.append(el('p', 'Underlying item: ' + item.normalized_item));
  content.append(el('p', item.description));
  if (item.classification_reason) content.append(el('p', item.classification_reason));
  content.append(el('div', 'Synthetic offline fixture. This record does not describe a real procurement case. A signal is a prompt for verification, not an allegation.', 'notice'));
  const actions = el('div', null, 'case-actions');
  for (const [kind, label] of [['ppid', 'Download PPID request ↓'], ['audit', 'Download audit brief ↓']]) {
    const link = el('a', label, 'button' + (kind === 'ppid' ? ' primary' : ''));
    link.href = '/api/packages/' + encodeURIComponent(item.id_rup) + '/dossier?kind=' + kind;
    link.setAttribute('download', ''); actions.append(link);
  }
  content.append(actions, el('p', 'Draft Markdown documents only. Complete requester details and verify sources before use.', 'footnote'));
  const prices = section('01 / Deterministic price comparison'), price = item.price_forensics;
  prices.append(el('p', 'Planning ceiling: ' + money(item.total_pagu) + ' · Recorded volume: ' + readable(item.volume_pekerjaan)));
  if (price && price.status === 'grounded') {
    const grid = el('div', null, 'price-grid');
    for (const [label, value, css] of [['Implied unit price', price.implied_unit_price, ''], ['Benchmark unit price', price.benchmark_unit_price, ''], ['Difference per unit', price.delta_idr, ' delta']]) {
      const cell = el('div', null, 'price-cell' + css); cell.append(el('span', label), el('strong', money(value))); grid.append(cell);
    }
    prices.append(grid, el('p', `Quantity: ${readable(price.quantity)} ${price.unit || ''} · Difference: ${price.delta_percent === null ? 'Unavailable' : readable(price.delta_percent) + '%'}`));
    prices.append(el('p', price.reason));
    const source = el('details'); source.append(el('summary', 'Inspect benchmark source & applicability')); provenance(source, price.source); prices.append(source);
  } else prices.append(el('div', 'Ungrounded — ' + (price?.reason || 'A sufficiently comparable quantity or benchmark is unavailable. No price difference is calculated.'), 'notice'));
  content.append(prices);
  const reasoning = section('02 / Evidence & counterevidence');
  const columns = el('div', null, 'evidence-columns'); columns.append(listEvidence('Supporting evidence', item.supporting_evidence), listEvidence('Counterevidence / limitations', item.counterevidence));
  reasoning.append(columns); content.append(reasoning);
  const execution = section('03 / Tender execution'); content.append(execution);
  if (item.linkage?.tender_id) {
    execution.append(el('p', 'Linkage status: ' + item.linkage.status + '. This is a synthetic fixture relationship.'));
    loadTender(item.linkage.tender_id, execution);
  } else execution.append(el('div', 'No demonstrated planning-to-execution link. No tender or vendor relationship is inferred for this package.', 'notice'));
  const sources = section('04 / Provenance'); provenance(sources, item.provenance); content.append(sources);
  if (item.review_status) sources.append(el('p', 'Review status: ' + item.review_status));
}
async function loadTender(id, container) {
  const target = el('div'); target.append(el('p', 'Loading tender evidence…')); container.append(target);
  try {
    const tender = await api('/api/tenders/' + encodeURIComponent(id));
    target.replaceChildren(el('h3', tender.nama_tender || id));
    if (tender.hps !== undefined) target.append(el('p', 'HPS: ' + money(tender.hps)));
    if (tender.signals?.length) target.append(listEvidence('Execution signals — require verification', tender.signals));
    const wrapper = el('div', null, 'table-scroll'), table = el('table', null, 'tender-table'), head = el('thead'), row = el('tr');
    for (const label of ['Participant', 'Bid / HPS', 'Evaluation', 'Disqualification reason']) row.append(el('th', label));
    head.append(row); table.append(head);
    const body = el('tbody');
    for (const participant of tender.participants || []) {
      const tr = el('tr');
      tr.append(el('td', participant.nama_peserta + (participant.evaluation === 'winner' ? ' · Winner' : '')),
        el('td', money(participant.bid) + (participant.bid_to_hps_percent != null ? ' / ' + participant.bid_to_hps_percent + '%' : '')),
        el('td', participant.evaluation || 'Not recorded'),
        el('td', participant.alasan_gugur || 'None recorded'));
      body.append(tr);
    }
    if (!body.children.length) target.append(el('p', 'Participant evaluations unavailable.'));
    else {table.append(body); wrapper.append(table); target.append(wrapper);}
    const graphSection = section('Participant relationship graph'); target.append(graphSection);
    loadGraph(id, graphSection);
  } catch (error) { errorMessage(target, error.message, () => { target.remove(); loadTender(id, container); }); }
}
function svg(tag, attributes, text) {
  const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, String(value));
  if (text !== undefined) node.textContent = text;
  return node;
}
async function loadGraph(id, target) {
  const status = el('p', 'Loading relationships…'); target.append(status);
  try {
    const data = await api('/api/tenders/' + encodeURIComponent(id) + '/graph'); status.remove();
    const nodes = (data.nodes || []).slice(0, 18), ids = new Set(nodes.map(node => node.id));
    const edges = (data.edges || []).filter(edge => ids.has(edge.source) && ids.has(edge.target)).slice(0, 40);
    if (!nodes.length) {target.append(el('p', 'No graph evidence available.')); return;}
    const height = Math.max(260, Math.ceil(nodes.length / 3) * 110 + 50);
    const graph = svg('svg', {viewBox: `0 0 780 ${height}`, role: 'img', 'aria-label': 'Synthetic tender relationship graph. All relationships are listed in the table below.', class: 'graph'});
    const positions = new Map(nodes.map((node, i) => [node.id, {x: 35 + (i % 3) * 255, y: 35 + Math.floor(i / 3) * 110}]));
    for (const edge of edges) {
      const a = positions.get(edge.source), b = positions.get(edge.target);
      graph.append(svg('line', {x1: a.x + 95, y1: a.y + 24, x2: b.x + 95, y2: b.y + 24}));
    }
    for (const node of nodes) {
      const pos = positions.get(node.id), group = svg('g', {});
      group.append(svg('rect', {x: pos.x, y: pos.y, width: 205, height: 62, rx: 4}), svg('title', {}, node.label + ' / ' + node.type));
      group.append(svg('text', {x: pos.x + 12, y: pos.y + 24}, node.label.length > 29 ? node.label.slice(0, 27) + '…' : node.label));
      group.append(svg('text', {x: pos.x + 12, y: pos.y + 45, class: 'edge-label'}, node.type)); graph.append(group);
    }
    target.append(graph, el('p', 'Synthetic relationships only. Shared identifiers are candidates for manual review, not proof of affiliation or collusion.', 'graph-caption'));
    if (data.nodes.length > nodes.length || data.edges.length > edges.length) target.append(el('p', 'View limited to 18 nodes and 40 relationships for readability.', 'graph-caption'));
    const details = el('details'); details.open = true; details.append(el('summary', 'Accessible relationship table'));
    const wrapper = el('div', null, 'table-scroll'), table = el('table', null, 'tender-table'), head = el('thead'), tr = el('tr');
    for (const label of ['From', 'Relationship', 'To']) tr.append(el('th', label)); head.append(tr); table.append(head);
    const body = el('tbody'), labels = new Map(nodes.map(node => [node.id, node.label]));
    for (const edge of edges) { const row = el('tr'); row.append(el('td', labels.get(edge.source)), el('td', edge.label), el('td', labels.get(edge.target))); body.append(row); }
    table.append(body); wrapper.append(table); details.append(wrapper); target.append(details);
  } catch (error) { errorMessage(status, error.message, () => { status.remove(); loadGraph(id, target); }); }
}
async function loadHealth() {
  try {
    const health = await api('/api/health'); $('health').replaceChildren();
    for (const [source, value] of Object.entries(health.sources || {})) {
      const row = el('div', null, 'health-row'), label = el('div', source.replaceAll('_', ' ').toUpperCase());
      label.append(el('small', value.reason || '')); row.append(label, el('span', value.status.replaceAll('_', ' '))); $('health').append(row);
    }
    if (health.limitations?.length) $('health').append(el('p', health.limitations.join(' '), 'footnote'));
  } catch (error) { errorMessage($('health'), error.message, loadHealth); }
}
async function runFixture() {
  const button = $('run-button'); button.disabled = true; button.textContent = 'Running offline analysis…';
  $('run-status').replaceChildren(el('p', 'Running the local fixture pipeline. No cloud calls are made.')); $('run-spans').replaceChildren();
  try {
    const started = await api('/api/runs', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({mode: 'fixture'})});
    const run = await api('/api/runs/' + encodeURIComponent(started.id));
    $('run-status').replaceChildren(el('p', `${run.status} · ${run.package_count} packages · ${run.model_calls} model calls`), el('p', 'Run ' + run.id, 'quiet'));
    for (const span of run.spans || []) {
      const row = el('div', null, 'span-row'); row.append(el('span', span.name), el('span', `${span.status} / ${span.duration_ms} ms`)); $('run-spans').append(row);
    }
    announce('Offline fixture run ' + run.status + '.'); loadPackages();
  } catch (error) { errorMessage($('run-status'), error.message, runFixture); }
  finally { button.disabled = false; button.textContent = 'Run offline analysis ↗'; }
}
$('filters').onsubmit = event => { event.preventDefault(); state.page = 1; loadPackages(); };
for (const id of ['region', 'agency', 'anomaly_class']) $(id).onchange = () => { state.page = 1; loadPackages(); };
$('previous').onclick = () => { state.page--; loadPackages(); };
$('next').onclick = () => { state.page++; loadPackages(); };
$('run-button').onclick = runFixture;
$('close-case').onclick = () => $('investigation').close();
$('investigation').addEventListener('close', () => { state.caseRequest++; if (state.opener?.isConnected) state.opener.focus(); });
loadPackages(); loadHealth();
