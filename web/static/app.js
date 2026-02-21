const I18N = {
  en: {
    title: "AI Hub",
    subtitle: "Confirm Only",
    theme: "Theme",
    language: "Language",
    scan: "Scan",
    confirm: "Confirm Selected",
    selectAll: "Select All (Filtered)",
    clearSelection: "Clear Selection",
    search: "Search",
    searchPlaceholder: "Search path or filename",
    categoryFilter: "Category Filter",
    familyFilter: "Family Filter",
    sizeMin: "Size Min (MB)",
    sizeMax: "Size Max (MB)",
    total: "Total",
    filtered: "Filtered",
    selected: "Selected",
    thCategory: "Category",
    thName: "Name",
    thSize: "Size",
    thFamily: "Family",
    emptyConfirm: "No items to confirm.",
    details: "Details",
    detailEmpty: "Select a row to see details.",
    labelName: "Name:",
    labelPath: "Path:",
    labelCategory: "Category:",
    labelFamily: "Family:",
    labelSize: "Size:",
    labelRules: "Matched Rules:",
    recommendations: "Recommendations",
    recommendRefresh: "Refresh Recommendations",
    recommendEmpty: "No recommendations yet.",
    all: "All",
    statusReady: "Status: Ready",
    statusLoaded: "Status: Loaded plan",
    statusScanning: "Status: Scanning...",
    statusScanFailed: "Status: Scan failed",
    statusConfirming: "Status: Confirming...",
    statusConfirmFailed: "Status: Confirm failed",
    actionScanComplete: "Scan complete",
    actionNoSelection: "No items selected.",
    actionMoved: "Moved",
    statusRecommendRefreshing: "Status: Refreshing recommendations...",
    statusRecommendFailed: "Status: Recommendations refresh failed",
  },
  zh: {
    title: "AI Hub",
    subtitle: "仅确认",
    theme: "主题",
    language: "语言",
    scan: "扫描",
    confirm: "确认选中",
    selectAll: "全选（筛选后）",
    clearSelection: "清空选择",
    search: "搜索",
    searchPlaceholder: "搜索路径或文件名",
    categoryFilter: "分类筛选",
    familyFilter: "家族筛选",
    sizeMin: "最小大小（MB）",
    sizeMax: "最大大小（MB）",
    total: "总数",
    filtered: "已筛选",
    selected: "已选择",
    thCategory: "分类",
    thName: "名称",
    thSize: "大小",
    thFamily: "家族",
    emptyConfirm: "没有需要确认的项目。",
    details: "详情",
    detailEmpty: "选择一行查看详情。",
    labelName: "名称：",
    labelPath: "路径：",
    labelCategory: "分类：",
    labelFamily: "家族：",
    labelSize: "大小：",
    labelRules: "匹配规则：",
    recommendations: "推荐",
    recommendRefresh: "刷新推荐",
    recommendEmpty: "暂无推荐。",
    all: "全部",
    statusReady: "状态：就绪",
    statusLoaded: "状态：已加载计划",
    statusScanning: "状态：扫描中...",
    statusScanFailed: "状态：扫描失败",
    statusConfirming: "状态：确认中...",
    statusConfirmFailed: "状态：确认失败",
    actionScanComplete: "扫描完成",
    actionNoSelection: "未选择任何项目。",
    actionMoved: "已移动",
    statusRecommendRefreshing: "状态：刷新推荐中...",
    statusRecommendFailed: "状态：刷新推荐失败",
  },
};

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
  lang: "en",
};

function t(key) {
  return (I18N[state.lang] && I18N[state.lang][key]) || I18N.en[key] || key;
}

function applyLang(lang) {
  state.lang = lang;
  localStorage.setItem("aihub-lang", lang);
  document.getElementById("title").textContent = t("title");
  document.getElementById("subtitle").textContent = t("subtitle");
  document.getElementById("theme-label").textContent = t("theme");
  document.getElementById("lang-label").textContent = t("language");
  document.getElementById("scan").textContent = t("scan");
  document.getElementById("confirm").textContent = t("confirm");
  document.getElementById("select-all").textContent = t("selectAll");
  document.getElementById("clear-selection").textContent = t("clearSelection");
  document.getElementById("search-label").textContent = t("search");
  document.getElementById("search").placeholder = t("searchPlaceholder");
  document.getElementById("filter-category-label").textContent = t("categoryFilter");
  document.getElementById("filter-family-label").textContent = t("familyFilter");
  document.getElementById("size-min-label").textContent = t("sizeMin");
  document.getElementById("size-max-label").textContent = t("sizeMax");
  document.getElementById("count-total-label").textContent = t("total");
  document.getElementById("count-filtered-label").textContent = t("filtered");
  document.getElementById("count-selected-label").textContent = t("selected");
  document.getElementById("th-category").textContent = t("thCategory");
  document.getElementById("th-name").textContent = t("thName");
  document.getElementById("th-size").textContent = t("thSize");
  document.getElementById("th-family").textContent = t("thFamily");
  document.getElementById("empty-state").textContent = t("emptyConfirm");
  document.getElementById("detail-title").textContent = t("details");
  document.getElementById("detail-empty").textContent = t("detailEmpty");
  document.getElementById("label-name").textContent = t("labelName");
  document.getElementById("label-path").textContent = t("labelPath");
  document.getElementById("label-category").textContent = t("labelCategory");
  document.getElementById("label-family").textContent = t("labelFamily");
  document.getElementById("label-size").textContent = t("labelSize");
  document.getElementById("label-rules").textContent = t("labelRules");
  document.getElementById("recommend-title").textContent = t("recommendations");
  document.getElementById("recommend-refresh").textContent = t("recommendRefresh");
  document.getElementById("recommend-empty").textContent = t("recommendEmpty");
  document.getElementById("status").textContent = t("statusReady");
  renderFilters();
}

function loadLang() {
  const saved = localStorage.getItem("aihub-lang") || "en";
  document.getElementById("lang-select").value = saved;
  applyLang(saved);
}

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
    option.textContent = value === "all" ? t("all") : value;
    categorySelect.appendChild(option);
  });
  Array.from(families).sort().forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value === "all" ? t("all") : value;
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
    document.getElementById("status").textContent = t("statusLoaded");
  } catch (err) {
    document.getElementById("status").textContent = `${t("statusScanFailed")} (${err.message})`;
  }
}

async function scan() {
  try {
    document.getElementById("status").textContent = t("statusScanning");
    const result = await fetchJson("/api/scan", { method: "POST" });
    document.getElementById("action-result").textContent = `${t("actionScanComplete")}: ${result.plan.confirm.length}`;
    await refreshPlan();
  } catch (err) {
    document.getElementById("status").textContent = `${t("statusScanFailed")} (${err.message})`;
  }
}

async function confirmSelected() {
  const paths = Array.from(state.selected);
  if (paths.length === 0) {
    document.getElementById("action-result").textContent = t("actionNoSelection");
    return;
  }
  try {
    document.getElementById("status").textContent = t("statusConfirming");
    const result = await fetchJson("/api/confirm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paths }),
    });
    document.getElementById("action-result").textContent = `${t("actionMoved")}: ${result.moved}`;
    state.selected.clear();
    await refreshPlan();
  } catch (err) {
    document.getElementById("status").textContent = `${t("statusConfirmFailed")} (${err.message})`;
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

function renderRecommendations(data) {
  const list = document.getElementById("recommendations");
  list.innerHTML = "";
  if (!data.domains || data.domains.length === 0) {
    document.getElementById("recommend-empty").style.display = "block";
    return;
  }
  document.getElementById("recommend-empty").style.display = "none";
  data.domains.forEach((domain) => {
    const block = document.createElement("div");
    block.className = "recommend-block";
    const title = document.createElement("div");
    title.className = "recommend-title";
    title.textContent = `${domain.domain}: ${domain.best ? domain.best.name : "-"}`;
    block.appendChild(title);
    if (domain.best && domain.best.description) {
      const desc = document.createElement("div");
      desc.className = "recommend-desc";
      desc.textContent = domain.best.description;
      block.appendChild(desc);
    }
    if (domain.alternatives && domain.alternatives.length > 0) {
      const alt = document.createElement("div");
      alt.className = "recommend-alt";
      alt.textContent = domain.alternatives.map((a) => a.name).join(", ");
      block.appendChild(alt);
    }
    list.appendChild(block);
  });
}

async function refreshRecommendations() {
  try {
    const data = await fetchJson("/api/recommendations");
    renderRecommendations(data);
  } catch (err) {
    document.getElementById("status").textContent = `${t("statusRecommendFailed")} (${err.message})`;
  }
}

async function refreshRecommendationsNow() {
  try {
    document.getElementById("status").textContent = t("statusRecommendRefreshing");
    await fetchJson("/api/recommendations/refresh", { method: "POST" });
    await refreshRecommendations();
  } catch (err) {
    document.getElementById("status").textContent = `${t("statusRecommendFailed")} (${err.message})`;
  }
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
  document.getElementById("lang-select").addEventListener("change", (event) => {
    applyLang(event.target.value);
  });
  document.getElementById("recommend-refresh").addEventListener("click", refreshRecommendationsNow);

  loadTheme();
  loadLang();
  refreshPlan();
  refreshRecommendations();
});
