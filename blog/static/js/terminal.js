/* 2049 Terminal Interaction
 * - Command input + history
 * - Minimal command router (help/ls/open/search/home/posts/tags/about/clear)
 * - Typewriter output
 * - Enhances rain + fog density (optional)
 */

(function terminalCommandLibrary(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.AIStackTerminalCommands = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function createTerminalCommandApi() {
  "use strict";

  const COMMANDS = Object.freeze([
    { id: "help", label: "HELP", usage: "help", description: "显示全部命令", aliases: ["?", "帮助"], featured: 0 },
    { id: "ls", label: "LS", usage: "ls [数量]", description: "列出当前页面条目", aliases: ["list", "dir", "列表"], featured: 1 },
    { id: "open", label: "OPEN", usage: "open <序号>", description: "打开指定条目", aliases: ["打开"], featured: 2 },
    { id: "search", label: "SEARCH", usage: "search <关键词>", description: "检索当前内容", aliases: ["find", "搜索", "查找"], featured: 3 },
    { id: "home", label: "HOME", usage: "home", description: "返回首页", aliases: ["首页"] },
    { id: "posts", label: "POSTS", usage: "posts", description: "进入情报归档", aliases: ["文章", "归档列表"] },
    { id: "tags", label: "TAGS", usage: "tags", description: "浏览标签", aliases: ["标签"] },
    { id: "scenarios", label: "SCENARIOS", usage: "scenarios", description: "进入知识图谱", aliases: ["场景"] },
    { id: "about", label: "ABOUT", usage: "about", description: "查看项目介绍", aliases: ["关于"] },
    { id: "archive", label: "ARCHIVE", usage: "archive", description: "进入时间归档", aliases: ["时间归档"] },
    { id: "clear", label: "CLEAR", usage: "clear", description: "清空终端输出", aliases: ["cls", "清空"] },
    { id: "graph", label: "GRAPH", usage: "graph <命令>", description: "操作当前知识图谱", aliases: ["图谱"] },
    { id: "graph reset", label: "GRAPH RESET", usage: "graph reset", description: "复位图谱视图", aliases: ["图谱 复位"] },
    { id: "graph focus", label: "GRAPH FOCUS", usage: "graph focus <节点>", description: "聚焦图谱节点", aliases: ["图谱 聚焦"] },
    { id: "graph filter", label: "GRAPH FILTER", usage: "graph filter <图层>", description: "筛选图谱图层", aliases: ["图谱 筛选"] },
    { id: "graph search", label: "GRAPH SEARCH", usage: "graph search <关键词>", description: "检索图谱节点", aliases: ["图谱 搜索"] },
  ]);

  const MAX_INPUT_LENGTH = 240;

  function boundedCommandSource(value) {
    return String(value || "")
      .slice(0, MAX_INPUT_LENGTH)
      .normalize("NFKC")
      .slice(0, MAX_INPUT_LENGTH)
      .trim()
      .replace(/\s+/g, " ");
  }

  function normalizeCommandText(value) {
    return boundedCommandSource(value).toLocaleLowerCase("zh-CN");
  }

  function editDistance(left, right) {
    const a = Array.from(left);
    const b = Array.from(right);
    const matrix = Array.from({ length: a.length + 1 }, () => new Array(b.length + 1).fill(0));
    for (let i = 0; i <= a.length; i += 1) matrix[i][0] = i;
    for (let j = 0; j <= b.length; j += 1) matrix[0][j] = j;
    for (let i = 1; i <= a.length; i += 1) {
      for (let j = 1; j <= b.length; j += 1) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        matrix[i][j] = Math.min(
          matrix[i - 1][j] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j - 1] + cost
        );
        if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
          matrix[i][j] = Math.min(matrix[i][j], matrix[i - 2][j - 2] + 1);
        }
      }
    }
    return matrix[a.length][b.length];
  }

  function scoreCandidate(query, candidate) {
    if (!query) return 1000;
    if (candidate === query) return 1400;
    if (candidate.startsWith(query)) return 1200 - Math.min(120, candidate.length - query.length);
    if (query.startsWith(`${candidate} `)) return 1120 - Math.min(120, query.length - candidate.length);
    if (candidate.includes(query)) return 960 - candidate.indexOf(query) * 8;

    const distance = editDistance(query, candidate);
    const scale = Math.max(query.length, candidate.length, 1);
    const similarity = 1 - distance / scale;
    if (similarity < 0.38) return Number.NEGATIVE_INFINITY;
    return Math.round(760 * similarity - distance * 8);
  }

  function rankCommandSuggestions(value, limit) {
    const query = normalizeCommandText(value);
    const max = Math.max(1, Math.min(Number(limit) || 4, 8));
    if (!query) {
      return COMMANDS.filter((item) => Number.isInteger(item.featured))
        .sort((a, b) => a.featured - b.featured)
        .slice(0, max)
        .map((item) => ({ ...item, match: "featured", score: 1000 - item.featured }));
    }

    return COMMANDS.map((item) => {
      const candidates = [item.id, ...(item.aliases || [])].map(normalizeCommandText);
      const score = Math.max(...candidates.map((candidate) => scoreCandidate(query, candidate)));
      const exact = candidates.includes(query);
      const prefix = !exact && candidates.some((candidate) => candidate.startsWith(query));
      return { ...item, score, match: exact ? "exact" : prefix ? "prefix" : "fuzzy" };
    })
      .filter((item) => Number.isFinite(item.score))
      .sort((a, b) => b.score - a.score || a.id.localeCompare(b.id))
      .slice(0, max);
  }

  function resolveFragmentedCommand(source) {
    const parts = source ? source.split(" ") : [];
    const commands = COMMANDS
      .filter((item) => /^[a-z]+$/u.test(item.id))
      .sort((left, right) => right.id.length - left.id.length);
    for (const command of commands) {
      const letters = Array.from(command.id);
      if (parts.length < letters.length) continue;
      const prefix = parts.slice(0, letters.length);
      if (!prefix.every((part, index) => normalizeCommandText(part) === letters[index])) continue;
      return {
        command: command.id,
        args: parts.slice(letters.length).join(" ").trim(),
        exact: true,
        suggestion: command,
      };
    }
    return null;
  }

  function resolveCommand(value) {
    const source = boundedCommandSource(value);
    const fragmented = resolveFragmentedCommand(source);
    if (fragmented) return fragmented;
    const normalizedSource = normalizeCommandText(source);
    const nestedMatch = COMMANDS
      .filter((item) => item.id.includes(" "))
      .flatMap((item) => [item.id, ...(item.aliases || [])].map((candidate) => ({
        item,
        candidate: normalizeCommandText(candidate),
      })))
      .filter(({ candidate }) => normalizedSource === candidate || normalizedSource.startsWith(`${candidate} `))
      .sort((left, right) => right.candidate.length - left.candidate.length)[0];

    if (nestedMatch) {
      const [parent, ...subcommand] = nestedMatch.item.id.split(" ");
      const suffix = source.slice(nestedMatch.candidate.length).trim();
      return {
        command: parent,
        args: [subcommand.join(" "), suffix].filter(Boolean).join(" "),
        exact: true,
        suggestion: nestedMatch.item,
      };
    }

    const parts = source ? source.split(" ") : [];
    const token = normalizeCommandText(parts.shift() || "");
    const args = parts.join(" ").trim();
    const command = COMMANDS.find((item) => {
      if (item.id.includes(" ")) return false;
      return [item.id, ...(item.aliases || [])].map(normalizeCommandText).includes(token);
    });
    if (command) return { command: command.id, args, exact: true, suggestion: command };

    const suggestion = rankCommandSuggestions(token, 1)[0] || null;
    return {
      command: token,
      args,
      exact: false,
      suggestion: suggestion && suggestion.score >= 390 ? suggestion : null,
    };
  }

  function applyCommandCompletion(value, suggestion) {
    if (!suggestion || !suggestion.id) return "";
    const source = boundedCommandSource(value);
    const parts = source ? source.split(" ") : [];
    if (!suggestion.id.includes(" ") && parts.length > 1) {
      return `${suggestion.id} ${parts.slice(1).join(" ")}`;
    }
    return `${suggestion.id} `;
  }

  return Object.freeze({
    commands: COMMANDS,
    maxInputLength: MAX_INPUT_LENGTH,
    normalizeCommandText,
    rankCommandSuggestions,
    resolveCommand,
    applyCommandCompletion,
  });
});

(function () {
  if (typeof document === "undefined") return;

  const commandApi = globalThis.AIStackTerminalCommands;

  function $(selector, root) {
    return (root || document).querySelector(selector);
  }

  function $all(selector, root) {
    return Array.from((root || document).querySelectorAll(selector));
  }

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function getPxNumber(value) {
    const n = Number.parseFloat(value || "0");
    return Number.isFinite(n) ? n : 0;
  }

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function getQueryParam(name) {
    try {
      const url = new URL(window.location.href);
      return url.searchParams.get(name) || "";
    } catch (_) {
      return "";
    }
  }

  function setQueryParam(name, value) {
    const url = new URL(window.location.href);
    if (!value) {
      url.searchParams.delete(name);
    } else {
      url.searchParams.set(name, value);
    }
    window.history.replaceState({}, "", url.toString());
  }

  function parseYearMonth(value) {
    const m = /^(\d{4})-(\d{2})$/.exec(String(value || "").trim());
    if (!m) return null;
    return { year: m[1], month: m[2], yearMonth: `${m[1]}-${m[2]}` };
  }

  function parseYear(value) {
    const m = /^(\d{4})$/.exec(String(value || "").trim());
    return m ? m[1] : "";
  }

  function setActiveArchiveLink(params) {
    const links = $all('a[href^="/posts/?year="], a[href^="/posts/?month="]');
    links.forEach((a) => {
      a.classList.remove("bg-muted-teal/10", "text-off-white/80");
    });

    if (!params) return;
    const selector = `a[href="/posts/?${params}"]`;
    const active = $(selector);
    if (active) active.classList.add("bg-muted-teal/10", "text-off-white/80");
  }

  function applyPostsTimeFilterFromQuery() {
    const groups = $all(".posts-month-group");
    if (!groups.length) return;

    const ym = parseYearMonth(getQueryParam("month"));
    const year = parseYear(getQueryParam("year"));

    const shouldFilter = Boolean(ym || year);
    if (!shouldFilter) return;

    let visibleRows = 0;
    let visibleGroups = 0;

    groups.forEach((el) => {
      const groupYM = String(el.getAttribute("data-year-month") || "");
      const groupYear = String(el.getAttribute("data-year") || groupYM.split("-")[0] || "");

      const show = ym ? groupYM === ym.yearMonth : groupYear === year;
      el.style.display = show ? "" : "none";

      if (show) {
        visibleGroups += 1;
        visibleRows += $all("tbody tr", el).length;
      }
    });

    const countEl = document.getElementById("posts-count");
    if (countEl) countEl.textContent = String(visibleRows);

    const emptyEl = document.getElementById("posts-empty");
    if (emptyEl) emptyEl.classList.toggle("hidden", visibleRows > 0);

    setActiveArchiveLink(ym ? `month=${ym.yearMonth}` : `year=${year}`);
  }

  function ensureOverlay() {
    let overlay = $("#terminal-overlay");
    if (overlay) return overlay;

    overlay = document.createElement("div");
    overlay.id = "terminal-overlay";
    overlay.className = "terminal-overlay";
    overlay.innerHTML =
      '<div class="terminal-overlay-panel glass-panel rounded-xl">' +
      '<div class="terminal-overlay-header">' +
      '<span class="terminal-overlay-title">SYS_LOG</span>' +
      '<button class="terminal-overlay-close" type="button" aria-label="Close log">×</button>' +
      "</div>" +
      '<div class="terminal-log" id="terminal-log" role="log"></div>' +
      "</div>";

    document.body.appendChild(overlay);

    const closeBtn = $(".terminal-overlay-close", overlay);
    closeBtn.addEventListener("click", () => overlay.classList.remove("is-open"));

    return overlay;
  }

  async function typeInto(el, text, speedMs) {
    const speed = clamp(Number(speedMs || 12), 2, 40);
    if (!el) return;

    const reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    // Long outputs and reduced-motion sessions print immediately to stay responsive.
    if (reducedMotion || (text || "").length > 520) {
      el.textContent = text;
      return;
    }

    el.textContent = "";
    for (let i = 0; i < text.length; i++) {
      el.textContent += text[i];
      // Slight randomness feels more human/terminal.
      // eslint-disable-next-line no-await-in-loop
      await sleep(speed + Math.random() * 8);
    }
  }

  async function logLine(kind, text) {
    const overlay = ensureOverlay();
    overlay.classList.add("is-open");

    const log = $("#terminal-log");
    const line = document.createElement("div");
    line.className = `terminal-line terminal-line-${kind || "info"}`;
    log.appendChild(line);

    await typeInto(line, text, 10);

    // Keep latest visible.
    log.scrollTop = log.scrollHeight;
  }

  function clearLog() {
    const overlay = ensureOverlay();
    const log = $("#terminal-log");
    log.innerHTML = "";
    overlay.classList.remove("is-open");
  }

  function getEntryLinks() {
    function isVisible(link) {
      let element = link;
      while (element && element !== document.documentElement) {
        if (element.hidden || element.getAttribute("aria-hidden") === "true") return false;
        const style = window.getComputedStyle(element);
        if (style.display === "none" || style.visibility === "hidden") return false;
        element = element.parentElement;
      }
      return true;
    }

    // Prefer explicit links, else fall back to the table rows.
    const links = $all("a[href][data-entry-link]").filter(isVisible);
    if (links.length) return links;

    const tableLinks = $all("table a[href]");
    return tableLinks.filter(
      (a) => a.getAttribute("href") && a.getAttribute("href").startsWith("/") && isVisible(a)
    );
  }

  function listEntries(limit) {
    const links = getEntryLinks();
    const max = clamp(Number(limit || 20), 1, 50);
    const items = links.slice(0, max).map((a, idx) => {
      const title = (a.getAttribute("data-entry-title") || a.textContent || "").trim().replace(/\s+/g, " ");
      const href = a.getAttribute("href");
      const n = String(idx + 1).padStart(2, "0");
      return `${n}  ${title}  ->  ${href}`;
    });
    return items.length ? items : ["(no entries found on this page)"];
  }

  function openEntry(n) {
    const idx = Number(n) - 1;
    if (Number.isNaN(idx)) return null;
    const links = getEntryLinks();
    if (idx < 0 || idx >= links.length) return null;
    return links[idx].getAttribute("href");
  }

  function normalize(str) {
    return (str || "").toLowerCase().trim();
  }

  function filterTable(keyword) {
    const q = normalize(keyword);
    const rows = $all("tbody tr");
    if (!rows.length) return { total: 0, shown: 0 };

    let shown = 0;
    rows.forEach((tr) => {
      const text = normalize(tr.textContent);
      const match = !q || text.includes(q);
      tr.style.display = match ? "" : "none";
      if (match) shown += 1;
    });

    return { total: rows.length, shown };
  }

  async function runCommand(raw) {
    const input = String(raw || "").trim();
    if (!input) return;

    await logLine("cmd", `CMD:// ${input}`);

    const parsed = commandApi.resolveCommand(input);
    const cmd = parsed.command;
    const arg = parsed.args;
    const rest = arg ? arg.split(/\s+/) : [];

    if (!parsed.exact) {
      if (parsed.suggestion) {
        await logLine(
          "err",
          `ERR: unknown command '${cmd}'. Did you mean '${parsed.suggestion.id}'? Press TAB to complete.`
        );
      } else {
        await logLine("err", `ERR: unknown command '${cmd}'. Type 'help'.`);
      }
      return;
    }

    switch (cmd) {
      case "help": {
        await logLine("info", "Commands are case-insensitive: HELP | LS [n] | OPEN <n> | SEARCH <kw> | HOME | POSTS | TAGS | SCENARIOS | ABOUT | ARCHIVE | CLEAR");
        await logLine("info", "Tips: type a prefix or approximate command, then press TAB / → to complete; ↑ / ↓ selects a suggestion.");
        await logLine("info", "Graph cmds: GRAPH RESET | GRAPH FOCUS <node> | GRAPH FILTER <layer> | GRAPH SEARCH <kw>");
        return;
      }
      case "home": {
        window.location.href = "/";
        return;
      }
      case "posts":
      case "ls": {
        if (cmd === "posts") {
          window.location.href = "/posts/";
          return;
        }
        const lines = listEntries(rest[0] || 20);
        for (const line of lines) {
          // eslint-disable-next-line no-await-in-loop
          await logLine("out", line);
        }
        return;
      }
      case "tags": {
        window.location.href = "/tags/";
        return;
      }
      case "scenarios": {
        window.location.href = "/scenarios/";
        return;
      }
      case "about": {
        window.location.href = "/about/";
        return;
      }
      case "archive": {
        window.location.href = "/archive/";
        return;
      }
      case "open": {
        const href = openEntry(rest[0]);
        if (!href) {
          await logLine("err", "ERR: usage `open <n>` and n must exist on this page (try `ls`).");
          return;
        }
        window.location.href = href;
        return;
      }
      case "search": {
        // If page has table rows, filter in place; else redirect to /posts/?q=
        const hasRows = $all("tbody tr").length > 0;
        if (hasRows) {
          const { total, shown } = filterTable(arg);
          setQueryParam("q", arg);
          await logLine("info", `FILTER: ${shown}/${total} visible`);
          return;
        }
        window.location.href = `/posts/?q=${encodeURIComponent(arg)}`;
        return;
      }
      case "clear": {
        clearLog();
        return;
      }
      case "graph": {
        // 图谱命令：graph reset | graph focus <node> | graph filter <layer> | graph search <kw>
        if (!arg) {
          await logLine("err", "ERR: usage `graph <cmd>` where cmd is reset/focus/filter/search");
          return;
        }
        const graphCmd = arg.split(/\s+/)[0];
        const graphArg = arg.substring(graphCmd.length).trim();

        // 检查是否存在图谱实例
        if (typeof window.graphEngine === "undefined") {
          await logLine("err", "ERR: graph not available on this page. Navigate to /scenarios/ first.");
          return;
        }

        switch (graphCmd.toLowerCase()) {
          case "reset": {
            window.graphEngine.resetView();
            await logLine("info", "GRAPH:// view reset");
            return;
          }
          case "focus": {
            if (!graphArg) {
              await logLine("err", "ERR: usage `graph focus <node_id>`");
              return;
            }
            const node = window.graphEngine.getNodeInfo(graphArg);
            if (node) {
              window.graphEngine.focusNode(graphArg);
              await logLine("info", `GRAPH:// focused on "${node.name}"`);
            } else {
              await logLine("err", `ERR: node "${graphArg}" not found`);
            }
            return;
          }
          case "filter": {
            if (!graphArg) {
              await logLine("err", "ERR: usage `graph filter <layer1,layer2,...>`");
              await logLine("info", "Available layers: language, framework, model, application, scenario");
              return;
            }
            const layers = graphArg.split(",").map((l) => l.trim().toLowerCase());
            const validLayers = ["language", "framework", "model", "application", "scenario"];
            const invalid = layers.filter((l) => !validLayers.includes(l));
            if (invalid.length > 0) {
              await logLine("err", `ERR: invalid layers: ${invalid.join(", ")}`);
              return;
            }
            window.graphEngine.filterLayers(layers);
            await logLine("info", `GRAPH:// filtered to: ${layers.join(", ")}`);
            return;
          }
          case "search": {
            window.graphEngine.search(graphArg);
            await logLine("info", `GRAPH:// searching for: "${graphArg}"`);
            return;
          }
          default: {
            await logLine("err", `ERR: unknown graph command '${graphCmd}'. Try 'help'.`);
          }
        }
        return;
      }
      default:
        return;
    }
  }

  function ensureMeasureEl(host) {
    let el = $(".terminal-measure", host);
    if (el) return el;
    el = document.createElement("span");
    el.className = "terminal-measure";
    host.appendChild(el);
    return el;
  }

  function updateCaretForHost(host) {
    if (!host) return;
    const input = $(".terminal-input", host);
    const caret = $(".terminal-caret", host);
    if (!input || !caret) return;

    const measure = ensureMeasureEl(host);
    const inputStyle = window.getComputedStyle(input);
    measure.style.font = inputStyle.font;
    measure.style.letterSpacing = inputStyle.letterSpacing;

    const caretIndex = Number.isInteger(input.selectionStart) ? input.selectionStart : input.value.length;
    const value = String(input.value || "").slice(0, caretIndex).replace(/ /g, "\u00A0");
    measure.textContent = value;

    const paddingLeft = getPxNumber(inputStyle.paddingLeft);
    const inputLeft = input.offsetLeft || 0;
    const measureWidth = measure.getBoundingClientRect().width;
    const caretWidth = caret.getBoundingClientRect().width || 10;
    const hostStyle = window.getComputedStyle(host);
    const caretStart = getPxNumber(hostStyle.getPropertyValue("--terminal-caret-start"));

    const minLeft = inputLeft + (input.value ? paddingLeft : caretStart);
    const maxLeft = inputLeft + input.clientWidth - caretWidth;
    const textLeft = inputLeft + paddingLeft;
    const desiredLeft = input.value ? textLeft + measureWidth - input.scrollLeft : minLeft;
    const left = clamp(desiredLeft, minLeft, maxLeft);
    host.style.setProperty("--terminal-caret-left", `${Math.round(left)}px`);
  }

  function preferredPlaceholder() {
    const path = String(window.location.pathname || "");
    if (path.startsWith("/scenarios")) return "输入命令…  GRAPH / SEARCH / OPEN / HELP";
    if (path.startsWith("/tags")) return "输入命令…  POSTS / OPEN 1 / HELP";
    if (path.startsWith("/about")) return "输入命令…  HOME / POSTS / TAGS / HELP";
    return "输入命令…  HELP / LS / OPEN 1 / SEARCH 关键词";
  }

  function enhanceCommandInput(input, host) {
    if (!host || !commandApi || host.dataset.commandEnhanced === "true") return null;
    host.dataset.commandEnhanced = "true";
    const commandBar = input.closest("footer");
    if (commandBar) commandBar.classList.add("terminal-command-bar");

    const listId = `terminal-command-list-${Math.random().toString(36).slice(2, 9)}`;
    input.placeholder = preferredPlaceholder();
    input.setAttribute("aria-label", "终端命令输入");
    input.setAttribute("role", "combobox");
    input.setAttribute("aria-autocomplete", "list");
    input.setAttribute("aria-controls", listId);
    input.setAttribute("aria-expanded", "false");
    input.setAttribute("aria-haspopup", "listbox");

    const panel = document.createElement("div");
    panel.className = "terminal-suggestions";
    panel.hidden = true;
    panel.setAttribute("aria-label", "命令建议");

    const heading = document.createElement("div");
    heading.className = "terminal-suggestions__heading";
    const headingLabel = document.createElement("span");
    headingLabel.textContent = "COMMAND MATCH";
    const headingKey = document.createElement("span");
    headingKey.textContent = "TAB / → 补全";
    heading.append(headingLabel, headingKey);

    const list = document.createElement("div");
    list.id = listId;
    list.className = "terminal-suggestions__list";
    list.setAttribute("role", "listbox");

    const live = document.createElement("span");
    live.className = "terminal-sr-only";
    live.setAttribute("aria-live", "polite");
    live.setAttribute("aria-atomic", "true");
    panel.append(heading, list, live);
    host.appendChild(panel);

    let suggestions = [];
    let activeIndex = 0;
    let blurTimer = 0;
    let compositionRefreshTimer = 0;
    let composing = false;

    function closeSuggestions() {
      panel.hidden = true;
      input.setAttribute("aria-expanded", "false");
      input.removeAttribute("aria-activedescendant");
    }

    function acceptSuggestion() {
      const suggestion = suggestions[activeIndex];
      if (!suggestion) return false;
      input.value = commandApi.applyCommandCompletion(input.value, suggestion);
      input.setSelectionRange(input.value.length, input.value.length);
      updateCaretForHost(host);
      closeSuggestions();
      return true;
    }

    function suggestionQuery() {
      const parsed = commandApi.resolveCommand(input.value);
      if (parsed.exact && parsed.args && parsed.command !== "graph") return null;
      if (!parsed.exact && parsed.args) return parsed.command;
      return input.value;
    }

    function renderSuggestions() {
      const query = suggestionQuery();
      suggestions = query === null ? [] : commandApi.rankCommandSuggestions(query, 4);
      activeIndex = clamp(activeIndex, 0, Math.max(0, suggestions.length - 1));
      list.replaceChildren();

      suggestions.forEach((suggestion, index) => {
        const option = document.createElement("button");
        option.type = "button";
        option.id = `${listId}-option-${index}`;
        option.className = "terminal-suggestion";
        option.setAttribute("role", "option");
        option.setAttribute("aria-selected", String(index === activeIndex));
        option.tabIndex = -1;

        const label = document.createElement("strong");
        label.className = "terminal-suggestion__label";
        label.textContent = suggestion.label;
        const description = document.createElement("span");
        description.className = "terminal-suggestion__description";
        description.textContent = `${suggestion.usage} · ${suggestion.description}`;
        const match = document.createElement("span");
        match.className = `terminal-suggestion__match terminal-suggestion__match--${suggestion.match}`;
        match.textContent = suggestion.match === "fuzzy" ? "近似" : suggestion.match === "featured" ? "推荐" : "匹配";
        option.append(label, description, match);

        option.addEventListener("pointerdown", (event) => {
          if (event.pointerType === "mouse") event.preventDefault();
        });
        option.addEventListener("click", () => {
          activeIndex = index;
          acceptSuggestion();
          input.focus();
        });
        option.addEventListener("pointerenter", () => {
          activeIndex = index;
          Array.from(list.children).forEach((child, childIndex) => {
            child.setAttribute("aria-selected", String(childIndex === activeIndex));
          });
          input.setAttribute("aria-activedescendant", `${listId}-option-${activeIndex}`);
        });
        list.appendChild(option);
      });

      const shouldOpen = document.activeElement === input && suggestions.length > 0;
      panel.hidden = !shouldOpen;
      input.setAttribute("aria-expanded", String(shouldOpen));
      if (shouldOpen) {
        input.setAttribute("aria-activedescendant", `${listId}-option-${activeIndex}`);
        live.textContent = `找到 ${suggestions.length} 条命令建议，首选 ${suggestions[activeIndex].label}`;
      } else {
        input.removeAttribute("aria-activedescendant");
      }
    }

    function moveSuggestion(direction) {
      if (panel.hidden || !suggestions.length) return false;
      activeIndex = (activeIndex + direction + suggestions.length) % suggestions.length;
      renderSuggestions();
      return true;
    }

    input.addEventListener("input", (event) => {
      if (composing || event.isComposing) {
        closeSuggestions();
        return;
      }
      window.clearTimeout(compositionRefreshTimer);
      activeIndex = 0;
      renderSuggestions();
    });
    input.addEventListener("compositionstart", () => {
      window.clearTimeout(compositionRefreshTimer);
      composing = true;
      host.dataset.commandComposing = "true";
      closeSuggestions();
    });
    input.addEventListener("compositionend", () => {
      composing = false;
      delete host.dataset.commandComposing;
      activeIndex = 0;
      compositionRefreshTimer = window.setTimeout(() => {
        renderSuggestions();
        updateCaretForHost(host);
      }, 0);
    });
    input.addEventListener("focus", () => {
      window.clearTimeout(blurTimer);
      renderSuggestions();
    });
    input.addEventListener("blur", () => {
      blurTimer = window.setTimeout(closeSuggestions, 120);
    });

    return {
      acceptSuggestion,
      closeSuggestions,
      moveSuggestion,
      refresh: renderSuggestions,
      isComposing: () => composing,
      isOpen: () => !panel.hidden,
      hasSuggestions: () => suggestions.length > 0,
    };
  }

  function initTerminal() {
    const input = $(".terminal-input");
    if (!input) return;
    if (input.dataset.terminalInitialized === "true") return;
    input.dataset.terminalInitialized = "true";
    input.maxLength = commandApi.maxInputLength;
    input.inputMode = "latin";
    input.autocapitalize = "off";
    input.setAttribute("autocorrect", "off");
    const host = input.closest(".terminal-caret-host");

    const suggestionsUi = enhanceCommandInput(input, host);
    const history = [];
    let historyIndex = -1;

    async function submitCurrentCommand({ restoreFocus = false } = {}) {
      if (suggestionsUi?.isComposing()) return false;
      const value = input.value;
      if (!String(value || "").trim()) return false;
      input.value = "";
      history.unshift(value);
      historyIndex = -1;
      suggestionsUi?.closeSuggestions();
      if (host) updateCaretForHost(host);
      await runCommand(value);
      if (restoreFocus) input.focus();
      return true;
    }

    if (host) {
      updateCaretForHost(host);
      input.addEventListener("input", () => updateCaretForHost(host));
      input.addEventListener("focus", () => updateCaretForHost(host));
      input.addEventListener("click", () => updateCaretForHost(host));
      input.addEventListener("select", () => updateCaretForHost(host));
      input.addEventListener("keyup", () => updateCaretForHost(host));
      window.addEventListener("resize", () => updateCaretForHost(host));
    }

    input.addEventListener("keydown", async (e) => {
      if (e.isComposing || e.keyCode === 229 || suggestionsUi?.isComposing()) return;
      if (e.key === "Tab" && e.shiftKey) return;

      if (
        (e.key === "Tab" || e.key === "ArrowRight") &&
        suggestionsUi &&
        suggestionsUi.isOpen() &&
        suggestionsUi.hasSuggestions() &&
        (e.key === "Tab" || input.selectionStart === input.value.length)
      ) {
        e.preventDefault();
        suggestionsUi.acceptSuggestion();
      } else if (e.key === "Enter") {
        e.preventDefault();
        await submitCurrentCommand();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        if (suggestionsUi && suggestionsUi.moveSuggestion(-1)) return;
        if (!history.length) return;
        historyIndex = clamp(historyIndex + 1, 0, history.length - 1);
        input.value = history[historyIndex] || "";
        input.setSelectionRange(input.value.length, input.value.length);
        if (suggestionsUi) suggestionsUi.refresh();
        if (host) updateCaretForHost(host);
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        if (suggestionsUi && suggestionsUi.moveSuggestion(1)) return;
        if (!history.length) return;
        historyIndex = clamp(historyIndex - 1, -1, history.length - 1);
        input.value = historyIndex === -1 ? "" : history[historyIndex] || "";
        input.setSelectionRange(input.value.length, input.value.length);
        if (suggestionsUi) suggestionsUi.refresh();
        if (host) updateCaretForHost(host);
      } else if (e.key === "Escape") {
        if (suggestionsUi && suggestionsUi.isOpen()) {
          e.preventDefault();
          e.stopPropagation();
          suggestionsUi.closeSuggestions();
          return;
        }
        const overlay = $("#terminal-overlay");
        if (overlay) overlay.classList.remove("is-open");
      }
    });

    const execBtn = $(".terminal-exec");
    if (execBtn) {
      execBtn.addEventListener("click", async () => {
        if (suggestionsUi?.isComposing()) return;
        await submitCurrentCommand({ restoreFocus: true });
      });
    }

    // Boot line (only once per session)
    try {
      const key = "ai-stack-booted";
      if (!sessionStorage.getItem(key)) {
        sessionStorage.setItem(key, "1");
        // show a tiny boot sequence
        logLine("info", "SYS:// boot sequence complete");
        logLine("info", "HINT:// type 'help' to list commands");
      }
    } catch (_) {
      // ignore
    }

    applyPostsTimeFilterFromQuery();

    // Apply query filter if present.
    const q = getQueryParam("q");
    if (q) {
      const hasRows = $all("tbody tr").length > 0;
      if (hasRows) filterTable(q);
    }
  }

  function initRainFog() {
    const rain = $(".rain-container");
    if (rain) {
      // If only a few streaks exist, add more for "light rain" density.
      const existing = rain.children.length;
      const target = 34;
      const toAdd = Math.max(0, target - existing);
      for (let i = 0; i < toAdd; i++) {
        const d = document.createElement("div");
        d.className = "rain-streak";
        const left = Math.random() * 100;
        const duration = 1.1 + Math.random() * 2.2;
        const delay = Math.random() * 2.2;
        const height = 55 + Math.random() * 70;
        const opacity = 0.08 + Math.random() * 0.18;
        d.style.left = `${left}%`;
        d.style.height = `${height}px`;
        d.style.opacity = `${opacity}`;
        d.style.animation = `rain-fall ${duration}s linear infinite`;
        d.style.animationDelay = `${delay}s`;
        rain.appendChild(d);
      }
    }

    const fog = $(".fog-container");
    if (fog) {
      // If fog markup is missing, seed a few layers.
      const existing = fog.children.length;
      if (existing < 3) {
        const mk = (klass, style, animClass) => {
          const el = document.createElement("div");
          el.className = `${klass} ${animClass}`;
          Object.assign(el.style, style || {});
          fog.appendChild(el);
        };
        mk("fog-cloud", { top: "10%", left: "-20%" }, "animate-fog");
        mk("fog-grey", { top: "40%", right: "-20%" }, "animate-fog-slow");
        mk("fog-cloud", { bottom: "-10%", left: "10%", opacity: "0.03" }, "animate-fog");
      }

      // Ensure there is a subtle teal "smoke" layer on all pages.
      if (!fog.querySelector(".fog-teal")) {
        const teal = document.createElement("div");
        teal.className = "fog-teal animate-smoke-reverse";
        teal.style.top = "18%";
        teal.style.left = "-10%";
        teal.style.opacity = "0.05";
        fog.appendChild(teal);
      }

      // Add a warm amber smoke layer to enrich depth.
      if (!fog.querySelector(".fog-amber")) {
        const amber = document.createElement("div");
        amber.className = "fog-amber animate-smoke";
        amber.style.bottom = "-25%";
        amber.style.left = "-35%";
        amber.style.opacity = "0.04";
        fog.appendChild(amber);
      }
    }
  }

  function updateCurrentTime() {
    const timeEl = document.getElementById("current-time");
    if (timeEl) {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, "0");
      const day = String(now.getDate()).padStart(2, "0");
      const hours = String(now.getHours()).padStart(2, "0");
      const minutes = String(now.getMinutes()).padStart(2, "0");
      const seconds = String(now.getSeconds()).padStart(2, "0");
      timeEl.textContent = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    initRainFog();
    initTerminal();
    if (!document.querySelector("[data-site-clock][data-site-clock-ready='true']")) {
      updateCurrentTime();
      setInterval(updateCurrentTime, 1000);
    }
  });
})();
