const statusEl = document.getElementById("status");
const actionsEl = document.getElementById("actions");
const logsEl = document.getElementById("logs");
const refreshBtn = document.getElementById("refresh");
const lastUpdateEl = document.getElementById("last-update");

async function fetchStatus() {
  const resp = await fetch("/api/status");
  const data = await resp.json();
  renderStatus(data.status || []);
  lastUpdateEl.textContent = new Date().toLocaleTimeString();
}

async function fetchLogs() {
  const resp = await fetch("/api/logs?limit=200");
  const data = await resp.json();
  logsEl.textContent = (data.lines || []).join("\n");
}

function renderStatus(items) {
  statusEl.innerHTML = "";
  items.forEach((item) => {
    const row = document.createElement("div");
    row.className = "status-item";
    const badge = document.createElement("span");
    badge.className = "badge " + (item.ok ? "ok" : "err");
    const label = document.createElement("span");
    label.textContent = item.label;
    row.appendChild(badge);
    row.appendChild(label);
    statusEl.appendChild(row);
  });
}

async function fetchActions() {
  const resp = await fetch("/api/actions");
  const data = await resp.json();
  actionsEl.innerHTML = "";
  (data.actions || []).forEach((action, idx) => {
    const btn = document.createElement("button");
    btn.textContent = action.label || `Action ${idx + 1}`;
    btn.onclick = async () => {
      btn.disabled = true;
      await fetch(`/api/action/${idx}`, { method: "POST" });
      btn.disabled = false;
      await fetchLogs();
    };
    actionsEl.appendChild(btn);
  });
}

refreshBtn.addEventListener("click", async () => {
  await fetchStatus();
  await fetchLogs();
});

async function init() {
  await fetchActions();
  await fetchStatus();
  await fetchLogs();
  setInterval(fetchStatus, 5000);
  setInterval(fetchLogs, 2000);
}

init();
