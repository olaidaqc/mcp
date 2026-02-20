async function fetchJson(url, options = {}) {
  const resp = await fetch(url, options);
  return resp.json();
}

function renderConfirmList(plan) {
  const container = document.getElementById('confirm-list');
  container.innerHTML = '';
  if (!plan.confirm || plan.confirm.length === 0) {
    container.textContent = 'No items to confirm.';
    return;
  }
  plan.confirm.forEach((item, idx) => {
    const row = document.createElement('div');
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.id = `confirm-${idx}`;
    cb.value = item.path;
    const label = document.createElement('label');
    label.htmlFor = cb.id;
    label.textContent = `${item.category}: ${item.path}`;
    row.appendChild(cb);
    row.appendChild(label);
    container.appendChild(row);
  });
}

async function refreshPlan() {
  const plan = await fetchJson('/api/plan');
  document.getElementById('plan').textContent = JSON.stringify(plan, null, 2);
  renderConfirmList(plan);
}

async function scan() {
  const result = await fetchJson('/api/scan', { method: 'POST' });
  document.getElementById('status').textContent = JSON.stringify(result, null, 2);
  await refreshPlan();
}

async function applyAuto() {
  const result = await fetchJson('/api/apply-auto', { method: 'POST' });
  document.getElementById('status').textContent = JSON.stringify(result, null, 2);
  await refreshPlan();
}

async function confirmSelected() {
  const checked = Array.from(document.querySelectorAll('#confirm-list input[type="checkbox"]:checked'));
  const paths = checked.map((cb) => cb.value);
  const result = await fetchJson('/api/confirm', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ paths }),
  });
  document.getElementById('status').textContent = JSON.stringify(result, null, 2);
  await refreshPlan();
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('scan').addEventListener('click', scan);
  const applyButton = document.getElementById('apply');
  applyButton.disabled = true;
  applyButton.addEventListener('click', applyAuto);
  document.getElementById('confirm').addEventListener('click', confirmSelected);
  refreshPlan();
});
