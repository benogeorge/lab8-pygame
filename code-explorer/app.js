import { explorerData } from "./data.js";

const state = {
  query: "",
  filter: "All",
  selectedPath: explorerData.files[0]?.path ?? ""
};

const statsEl = document.getElementById("stats");
const filtersEl = document.getElementById("filters");
const treeEl = document.getElementById("tree");
const matchCountEl = document.getElementById("match-count");
const fileTitleEl = document.getElementById("file-title");
const fileMetaEl = document.getElementById("file-meta");
const codeEl = document.getElementById("code");
const insightsEl = document.getElementById("insights");
const highlightsEl = document.getElementById("highlights");
const searchEl = document.getElementById("search");
const copyButton = document.getElementById("copy-button");

const fileTypes = ["All", ...new Set(explorerData.files.map((f) => f.type))];

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderStats() {
  statsEl.innerHTML = explorerData.project.stats
    .map((item) => `<article class="stat"><span>${item.label}</span><strong>${item.value}</strong></article>`)
    .join("");
}

function renderFilters() {
  filtersEl.innerHTML = fileTypes
    .map((type) => `<button type="button" class="${state.filter === type ? "active" : ""}" data-filter="${type}">${type}</button>`)
    .join("");

  filtersEl.querySelectorAll("[data-filter]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.filter = btn.dataset.filter;
      renderFilters();
      renderTree();
    });
  });
}

function filterFiles() {
  const q = state.query.trim().toLowerCase();
  return explorerData.files.filter((file) => {
    const typeOk = state.filter === "All" || file.type === state.filter;
    if (!typeOk) {
      return false;
    }

    if (!q) {
      return true;
    }

    const text = [file.path, file.summary, file.type, file.language, ...(file.tags ?? [])].join(" ").toLowerCase();
    return text.includes(q);
  });
}

function renderTree() {
  const files = filterFiles();
  matchCountEl.textContent = `${files.length} file${files.length === 1 ? "" : "s"}`;

  if (files.length > 0 && !files.some((f) => f.path === state.selectedPath)) {
    state.selectedPath = files[0].path;
  }

  treeEl.innerHTML = files
    .map(
      (file) => `<button type="button" data-path="${file.path}" class="${state.selectedPath === file.path ? "active" : ""}">
        <strong>${file.path}</strong>
        <small>${file.type} | ${file.language}</small>
      </button>`
    )
    .join("");

  treeEl.querySelectorAll("[data-path]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.selectedPath = btn.dataset.path;
      renderTree();
    });
  });

  if (files.length === 0) {
    fileTitleEl.textContent = "No matching file";
    fileMetaEl.textContent = "Try a different search or filter";
    codeEl.textContent = "No results.";
    insightsEl.innerHTML = "";
    return;
  }

  const selected = explorerData.files.find((f) => f.path === state.selectedPath) ?? files[0];
  renderFile(selected);
}

function renderFile(file) {
  fileTitleEl.textContent = file.path;
  fileMetaEl.textContent = `${file.type} | ${file.language} | ${file.size}`;

  const lines = file.snippet.split("\n");
  codeEl.innerHTML = lines
    .map((line, index) => `<span class="line ${index < 8 ? "hot" : ""}">${escapeHtml(line)}</span>`)
    .join("");

  insightsEl.innerHTML = file.highlights
    .map((point, i) => `<article class="insight"><h3>Note ${i + 1}</h3><p>${point}</p></article>`)
    .join("");
}

function renderArchitecture() {
  highlightsEl.innerHTML = explorerData.architecture
    .map((item) => `<article class="highlight"><h3>${item.title}</h3><p>${item.body}</p></article>`)
    .join("");
}

searchEl.addEventListener("input", () => {
  state.query = searchEl.value;
  renderTree();
});

copyButton.addEventListener("click", async () => {
  const selected = explorerData.files.find((f) => f.path === state.selectedPath);
  if (!selected) {
    return;
  }

  try {
    await navigator.clipboard.writeText(selected.snippet);
    copyButton.textContent = "Copied";
  } catch {
    copyButton.textContent = "Copy Failed";
  }

  setTimeout(() => {
    copyButton.textContent = "Copy Snippet";
  }, 900);
});

renderStats();
renderFilters();
renderArchitecture();
renderTree();
