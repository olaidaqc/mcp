async function fetchJson(url, options = {}) {
  const resp = await fetch(url, options);
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`${resp.status} ${resp.statusText} ${text}`);
  }
  return resp.json();
}

const state = {
  items: [],
  filtered: [],
  selected: new Set(),
  activePath: null,
};

function formatSize(bytes) {
  if (!bytes || bytes <= 0) return "-";
  const units = ["B", "KB", "MB", "GB", "TB"];
  let value = bytes;
  let idx = 0;
  while (value >= 1024 && idx < units.length - 1) {
    value /= 1024;
    idx += 1;
  }
  return `${value.toFixed(value >= 10 || idx === 0 ? 0 : 1)} ${units[idx]}`;
}

function getName(path) {
  if (!path) return "";
  const parts = path.split(/[/\\]/);
  return parts[parts.length - 1];
}

function applyFilters() {
  const search = document.getElementById("search").value.trim().toLowerCase();
  const category = document.getElementById("filter-category").value;
  const family = document.getElementById("filter-family").value;
  const sizeMin = parseFloat(document.getElementById("size-min").value || "0");
  const sizeMax = parseFloat(document.getElementById("size-max").value || "0");
  const minBytes = sizeMin > 0 ? sizeMin * 1024 * 1024 : 0;
  const maxBytes = sizeMax > 0 ? sizeMax * 1024 * 1024 : 0;

  state.filtered = state.items.filter((item) => {
    const name = getName(item.path).toLowerCase();
    const path = (item.path || "").toLowerCase();
    const matchSearch = !search || name.includes(search) || path.includes(search);
    const matchCategory = category === "all" || item.category === category;
    const itemFamily = item.family || "Unknown";
    const matchFamily = family === "all" || itemFamily === family;
    const size = item.size_bytes || 0;
    const matchMin = minBytes === 0 || size >= minBytes;
    const matchMax = maxBytes === 0 || size <= maxBytes;
    return matchSearch && matchCategory && matchFamily && matchMin && matchMax;
  });
}

function renderFilters() {
  const categorySelect = document.getElementById("filter-category");
  const familySelect = document.getElementById("filter-family");
  const currentCategory = categorySelect.value || "all";
  const currentFamily = familySelect.value || "all";
  const categories = new Set(["all"]);
  const families = new Set(["all"]);
  state.items.forEach((item) => {
    categories.add(item.category || "Unknown");
    families.add(item.family || "Unknown");
  });
  categorySelect.innerHTML = "";
  familySelect.innerHTML = "";
  Array.from(categories).sort().forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value === "all" ? "All" : value;
    categorySelect.appendChild(option);
  });
  Array.from(families).sort().forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value === "all" ? "All" : value;
    familySelect.appendChild(option);
  });
  categorySelect.value = categories.has(currentCategory) ? currentCategory : "all";
  familySelect.value = families.has(currentFamily) ? currentFamily : "all";
}

function updateCounts() {
  document.getElementById("count-total").textContent = state.items.length;
  document.getElementById("count-filtered").textContent = state.filtered.length;
  document.getElementById("count-selected").textContent = state.selected.size;
}

function renderTable() {
  const tbody = document.getElementById("plan-body");
  tbody.innerHTML = "";
  if (state.filtered.length === 0) {
    document.getElementById("empty-state").style.display = "block";
  } else {
    document.getElementById("empty-state").style.display = "none";
  }

  state.filtered.forEach((item) => {
    const row = document.createElement("tr");
    row.dataset.path = item.path;
    if (state.selected.has(item.path)) {
      row.classList.add("selected");
    }
    if (state.activePath === item.path) {
      row.classList.add("active");
    }

    const checkboxCell = document.createElement("td");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = state.selected.has(item.path);
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) {
        state.selected.add(item.path);
      } else {
        state.selected.delete(item.path);
      }
      updateCounts();
      renderTable();
    });
    checkboxCell.appendChild(checkbox);

    const categoryCell = document.createElement("td");
    categoryCell.textContent = item.category || "-";

    const nameCell = document.createElement("td");
    nameCell.textContent = getName(item.path);

    const sizeCell = document.createElement("td");
    sizeCell.textContent = formatSize(item.size_bytes || 0);

    const familyCell = document.createElement("td");
    familyCell.textContent = item.family || "Unknown";

    row.appendChild(checkboxCell);
    row.appendChild(categoryCell);
    row.appendChild(nameCell);
    row.appendChild(sizeCell);
    row.appendChild(familyCell);

    row.addEventListener("click", (event) => {
      if (event.target.tagName.toLowerCase() === "input") {
        return;
      }
      state.activePath = item.path;
      renderDetails(item);
      renderTable();
    });

    tbody.appendChild(row);
  });
  updateCounts();
}

function renderDetails(item) {
  const empty = document.getElementById("detail-empty");
  const content = document.getElementById("detail-content");
  if (!item) {
    empty.classList.remove("hidden");
    content.classList.add("hidden");
    return;
  }
  empty.classList.add("hidden");
  content.classList.remove("hidden");
  document.getElementById("detail-name").textContent = getName(item.path);
  document.getElementById("detail-path").textContent = item.path || "";
  document.getElementById("detail-category").textContent = item.category || "";
  document.getElementById("detail-family").textContent = item.family || "Unknown";
  document.getElementById("detail-size").textContent = formatSize(item.size_bytes || 0);
  document.getElementById("detail-rules").textContent = (item.matched_rules || []).join(", ") || "-";
}

async function refreshPlan() {
  try {
    const plan = await fetchJson("/api/plan");
    state.items = plan.confirm || [];
    state.selected = new Set(Array.from(state.selected).filter((path) => state.items.find((i) => i.path === path)));
    renderFilters();
    applyFilters();
    renderTable();
    renderDetails(state.items.find((item) => item.path === state.activePath));
    document.getElementById("status").textContent = "Status: Loaded plan";
  } catch (err) {
    document.getElementById("status").textContent = `Status: Failed to load plan (${err.message})`;
  }
}

async function scan() {
  try {
    document.getElementById("status").textContent = "Status: Scanning...";
    const result = await fetchJson("/api/scan", { method: "POST" });
    document.getElementById("action-result").textContent = `Scan complete: ${result.plan.confirm.length} items`;
    await refreshPlan();
  } catch (err) {
    document.getElementById("status").textContent = `Status: Scan failed (${err.message})`;
  }
}

async function confirmSelected() {
  const paths = Array.from(state.selected);
  if (paths.length === 0) {
    document.getElementById("action-result").textContent = "No items selected.";
    return;
  }
  try {
    document.getElementById("status").textContent = "Status: Confirming...";
    const result = await fetchJson("/api/confirm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paths }),
    });
    document.getElementById("action-result").textContent = `Moved: ${result.moved}`;
    state.selected.clear();
    await refreshPlan();
  } catch (err) {
    document.getElementById("status").textContent = `Status: Confirm failed (${err.message})`;
  }
}

function selectAllFiltered() {
  state.filtered.forEach((item) => state.selected.add(item.path));
  updateCounts();
  renderTable();
}

function clearSelection() {
  state.selected.clear();
  updateCounts();
  renderTable();
}

function applyTheme(theme) {
  document.body.setAttribute("data-theme", theme);
  localStorage.setItem("aihub-theme", theme);
}

function loadTheme() {
  const saved = localStorage.getItem("aihub-theme") || "light";
  applyTheme(saved);
  document.getElementById("theme-select").value = saved;
}

window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("scan").addEventListener("click", scan);
  document.getElementById("confirm").addEventListener("click", confirmSelected);
  document.getElementById("select-all").addEventListener("click", selectAllFiltered);
  document.getElementById("clear-selection").addEventListener("click", clearSelection);
  document.getElementById("search").addEventListener("input", () => {
    applyFilters();
    renderTable();
  });
  document.getElementById("filter-category").addEventListener("change", () => {
    applyFilters();
    renderTable();
  });
  document.getElementById("filter-family").addEventListener("change", () => {
    applyFilters();
    renderTable();
  });
  document.getElementById("size-min").addEventListener("input", () => {
    applyFilters();
    renderTable();
  });
  document.getElementById("size-max").addEventListener("input", () => {
    applyFilters();
    renderTable();
  });
  document.getElementById("theme-select").addEventListener("change", (event) => {
    applyTheme(event.target.value);
  });

  loadTheme();
  refreshPlan();
});
