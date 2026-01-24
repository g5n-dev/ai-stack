/* 2049 Terminal Interaction
 * - Command input + history
 * - Minimal command router (help/ls/open/search/home/posts/tags/about/clear)
 * - Typewriter output
 * - Enhances rain + fog density (optional)
 */

(function () {
  function $(selector, root) {
    return (root || document).querySelector(selector);
  }

  function $all(selector, root) {
    return Array.from((root || document).querySelectorAll(selector));
  }

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
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

  function ensureOverlay() {
    let overlay = $("#terminal-overlay");
    if (overlay) return overlay;

    overlay = document.createElement("div");
    overlay.id = "terminal-overlay";
    overlay.className = "terminal-overlay";
    overlay.setAttribute("aria-live", "polite");
    overlay.innerHTML =
      '<div class="terminal-overlay-panel glass-panel rounded-xl">' +
      '<div class="terminal-overlay-header">' +
      '<span class="terminal-overlay-title">SYS_LOG</span>' +
      '<button class="terminal-overlay-close" type="button" aria-label="Close log">×</button>' +
      "</div>" +
      '<div class="terminal-log" id="terminal-log"></div>' +
      "</div>";

    document.body.appendChild(overlay);

    const closeBtn = $(".terminal-overlay-close", overlay);
    closeBtn.addEventListener("click", () => overlay.classList.remove("is-open"));

    return overlay;
  }

  async function typeInto(el, text, speedMs) {
    const speed = clamp(Number(speedMs || 12), 2, 40);
    if (!el) return;

    // Long outputs: print immediately (keeps UI responsive).
    if ((text || "").length > 520) {
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
    // Prefer explicit links, else fall back to the table rows.
    const links = $all("a[href][data-entry-link]");
    if (links.length) return links;

    const tableLinks = $all("table a[href]");
    return tableLinks.filter((a) => a.getAttribute("href") && a.getAttribute("href").startsWith("/"));
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

    const [cmd, ...rest] = input.split(/\s+/);
    const arg = rest.join(" ").trim();

    switch (cmd.toLowerCase()) {
      case "help": {
        await logLine("info", "Commands: help | ls [n] | open <n> | search <kw> | home | posts | tags | scenarios | about | archive | clear | graph [cmd]");
        await logLine("info", "Tips: On /posts/ you can use `search` to filter the table; `open 3` opens the 3rd visible entry.");
        await logLine("info", "Graph cmds: graph reset | graph focus <node> | graph filter <layer> | graph search <kw>");
        return;
      }
      case "home": {
        window.location.href = "/";
        return;
      }
      case "posts":
      case "ls": {
        if (cmd.toLowerCase() === "posts") {
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
      default: {
        await logLine("err", `ERR: unknown command '${cmd}'. Type 'help'.`);
      }
    }
  }

  function initTerminal() {
    const input = $(".terminal-input");
    if (!input) return;

    const history = [];
    let historyIndex = -1;

    input.addEventListener("keydown", async (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const value = input.value;
        input.value = "";
        history.unshift(value);
        historyIndex = -1;
        await runCommand(value);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        if (!history.length) return;
        historyIndex = clamp(historyIndex + 1, 0, history.length - 1);
        input.value = history[historyIndex] || "";
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        if (!history.length) return;
        historyIndex = clamp(historyIndex - 1, -1, history.length - 1);
        input.value = historyIndex === -1 ? "" : history[historyIndex] || "";
      } else if (e.key === "Escape") {
        const overlay = $("#terminal-overlay");
        if (overlay) overlay.classList.remove("is-open");
      }
    });

    const execBtn = $(".terminal-exec");
    if (execBtn) {
      execBtn.addEventListener("click", async () => {
        const value = input.value;
        if (!String(value || "").trim()) return;
        input.value = "";
        history.unshift(value);
        historyIndex = -1;
        await runCommand(value);
        input.focus();
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
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
  });
})();
