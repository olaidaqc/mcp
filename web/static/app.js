async function fetchJson(url, options = {}) {
  const resp = await fetch(url, options);
  return resp.json();
}

async function refreshPlan() {
  const plan = await fetchJson('/api/plan');
  document.getElementById('plan').textContent = JSON.stringify(plan, null, 2);
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

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('scan').addEventListener('click', scan);
  document.getElementById('apply').addEventListener('click', applyAuto);
  refreshPlan();
});
