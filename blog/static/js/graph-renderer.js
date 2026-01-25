/**
 * AI Stack Graph Renderer
 * Adapts the D3 Graph Engine to the "Nexus Archive" UI
 */

(function (global) {
  "use strict";

  class GraphRenderer {
    constructor(engine) {
      this.engine = engine;
      this._typing = null;
      this._listeners = [];
      this._liveStatsTimer = null;

      // UI Elements
      this.sidebar = document.getElementById("detail-sidebar");
      this.searchInput = document.getElementById("graph-search");
      this.filterContainer = document.getElementById("active-filters");
      this.storyDock = document.getElementById("story-dock");
      this.storyFields = {
        title: document.getElementById("story-title"),
        subtitle: document.getElementById("story-subtitle"),
        status: document.getElementById("story-status"),
        lines: document.getElementById("story-lines"),
      };

      // Sidebar Fields
      this.fields = {
        id: document.getElementById("sidebar-id"),
        title: document.getElementById("sidebar-title"),
        layer: document.getElementById("sidebar-layer"),
        date: document.getElementById("sidebar-date"),
        category: document.getElementById("sidebar-category"),
        desc: document.getElementById("sidebar-desc"),
        connCount: document.getElementById("sidebar-connections-count"),
        connBar: document.getElementById("sidebar-connections-bar"),
        tags: document.getElementById("sidebar-tags"),
      };

      this._init();
    }

    _listen(target, type, handler, options) {
      if (!target || !target.addEventListener) return;
      target.addEventListener(type, handler, options);
      this._listeners.push({ target, type, handler, options });
    }

    _unlistenAll() {
      this._listeners.forEach(({ target, type, handler, options }) => {
        try {
          target.removeEventListener(type, handler, options);
        } catch (_) {
        }
      });
      this._listeners = [];
    }

    _init() {
      this._bindToolbar();
      this._bindSearch();
      this._bindSidebar();
      this._renderFilters();
      this._bindEvents();
      this._startLiveStats();
      this._setStoryIdle();
    }

    // ===== UI Bindings =====

    _bindToolbar() {
      // Zoom In
      const zoomIn = document.getElementById("btn-zoom-in");
      this._listen(zoomIn, "click", () => {
        const t = this.engine.transform;
        this.engine.transform = { ...t, k: Math.min(3, t.k * 1.2) };
      });

      // Zoom Out
      const zoomOut = document.getElementById("btn-zoom-out");
      this._listen(zoomOut, "click", () => {
        const t = this.engine.transform;
        this.engine.transform = { ...t, k: Math.max(0.3, t.k / 1.2) };
      });

      // Reset
      const reset = document.getElementById("btn-reset");
      this._listen(reset, "click", () => {
        this.engine.resetView();
        this._closeSidebar();
      });

      // Fit
      const fit = document.getElementById("btn-fit");
      this._listen(fit, "click", () => {
        // Simple mock fit, effectively a reset in this engine version
        this.engine.resetView();
      });
    }

    _bindSearch() {
      if (!this.searchInput) return;
      this._listen(this.searchInput, "input", (e) => {
        this.engine.search(e.target.value);
      });
    }

    _bindSidebar() {
      const close = document.getElementById("btn-close-sidebar");
      this._listen(close, "click", () => {
        this._closeSidebar();
      });

      const focus = document.getElementById("btn-focus-node");
      this._listen(focus, "click", () => {
        if (this.engine.selectedNode) {
          this.engine.focusNode(this.engine.selectedNode.id);
        }
      });
    }

    _renderFilters() {
      if (!this.filterContainer) return;
      this.filterContainer.innerHTML = "";

      const layers = this.engine.data.layers;
      const sortedLayers = Object.entries(layers).sort((a, b) => a[1].level - b[1].level);

      sortedLayers.forEach(([key, layer]) => {
        const btn = document.createElement("button");
        btn.className = "flex items-center gap-1 bg-surface-dark text-slate-400 text-[10px] px-2 py-0.5 rounded border border-surface-border hover:border-primary/50 hover:text-primary transition-colors";
        btn.innerHTML = `
          <div class="size-1.5 rounded-full" style="background-color: ${layer.color}"></div>
          <span>${layer.name}</span>
        `;

        // Simple toggle logic (engine supports filtering list)
        let isActive = true;
        this._listen(btn, "click", () => {
          isActive = !isActive;
          btn.style.opacity = isActive ? "1" : "0.4";
          // Re-calculate active layers
          const active = Array.from(this.filterContainer.children)
            .filter(c => c.style.opacity !== "0.4")
            .map((c, i) => sortedLayers[i][0]);

          this.engine.filterLayers(active);
        });

        this.filterContainer.appendChild(btn);
      });

      this.filterContainer.classList.remove("hidden");
    }

    // ===== Sidebar Logic =====

    _clearTyping() {
      if (this._typing?.timer) {
        clearTimeout(this._typing.timer);
      }
      if (this._typing?.caret && this._typing.caret.parentNode) {
        this._typing.caret.remove();
      }
      this._typing = null;
    }

    _typeText(el, text, opts = {}) {
      if (!el) return;
      const reduceMotion = global.matchMedia && global.matchMedia("(prefers-reduced-motion: reduce)").matches;
      const raw = (text || "").toString();
      const maxLen = typeof opts.maxLen === "number" ? opts.maxLen : 420;
      const content = raw.length > maxLen ? `${raw.slice(0, maxLen)}…` : raw;

      this._clearTyping();

      if (reduceMotion) {
        el.textContent = content;
        return;
      }

      el.textContent = "";
      const textNode = document.createTextNode("");
      const caret = document.createElement("span");
      caret.textContent = "▍";
      caret.className = "blink";
      caret.style.marginLeft = "2px";
      caret.style.color = "rgba(77,182,172,0.9)";
      el.appendChild(textNode);
      el.appendChild(caret);

      const speed = typeof opts.speed === "number" ? opts.speed : 14;
      const jitter = typeof opts.jitter === "number" ? opts.jitter : 10;
      const startDelay = typeof opts.startDelay === "number" ? opts.startDelay : 60;
      let i = 0;

      const step = () => {
        if (!this._typing || this._typing.el !== el) return;
        i = Math.min(content.length, i + 1);
        textNode.nodeValue = content.slice(0, i);
        if (i >= content.length) {
          caret.remove();
          this._typing = null;
          return;
        }
        this._typing.timer = setTimeout(step, speed + Math.floor(Math.random() * jitter));
      };

      this._typing = {
        el,
        caret,
        timer: setTimeout(step, startDelay),
      };
    }

    _openSidebar(node) {
      if (!this.sidebar) return;

      // Populate Fields
      this.fields.id.textContent = `HEX_${node.id.toUpperCase().substring(0, 6)}`;
      this.fields.title.textContent = node.name;
      this.fields.layer.textContent = node.layer_name || "UNKNOWN LAYER";
      this.fields.layer.style.color = node.color;

      if (this.fields.date) this.fields.date.textContent = this._formatTs().slice(0, 10);
      this._typeText(
        this.fields.desc,
        node.description || "No secure data available for this node. Access restricted or packet loss detected.",
        { speed: 12, jitter: 16, startDelay: 80, maxLen: 520 }
      );
      this.fields.category.textContent = (node.category || "General").toUpperCase();

      // Connections Metrics
      const linkCount = node._links ? node._links.length : 0;
      this.fields.connCount.textContent = linkCount;
      // Mock bar percentage (max 10 links = 100%)
      const pct = Math.min(100, linkCount * 10);
      this.fields.connBar.style.width = `${pct}%`;

      // Tags (Fake them based on category or properties)
      this.fields.tags.innerHTML = "";
      const tags = [node.layer, node.category, "SECURE"];
      tags.forEach(tag => {
        const span = document.createElement("span");
        span.className = "px-2 py-1 rounded bg-surface-border/50 text-slate-300 text-xs border border-transparent";
        span.textContent = `#${tag.toUpperCase()}`;
        this.fields.tags.appendChild(span);
      });

      this.sidebar.classList.remove("hidden-panel");
    }

    _closeSidebar() {
      if (this.sidebar) {
        this.sidebar.classList.add("hidden-panel");
      }
      this._clearTyping();
      this.engine.selectedNode = null;
    }

    _setStoryIdle() {
      if (!this.storyDock || !this.storyFields?.lines) return;
      if (this.storyFields.title) this.storyFields.title.textContent = "GRAPH_SESSION";
      if (this.storyFields.subtitle) this.storyFields.subtitle.textContent = "SECTOR_ID: AI_STACK // MODE: MAP";
      if (this.storyFields.status) this.storyFields.status.textContent = "LIVE";
      this.storyFields.lines.innerHTML = [
        "<div>BOOTSTRAP: LINK_STATUS=STABLE</div>",
        "<div>TIP: HOVER NODE TO TRACE ROUTES</div>",
        "<div>TIP: CLICK NODE TO LOCK FOCUS</div>",
      ].join("");
    }

    _formatTs(d = new Date()) {
      const pad = (n) => String(n).padStart(2, "0");
      return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
    }

    _updateStory(node, mode) {
      if (!this.storyDock || !this.storyFields?.lines) return;
      if (!node) {
        this._setStoryIdle();
        return;
      }

      const ts = this._formatTs();
      const linkCount = node._links ? node._links.length : 0;
      const layerName = (node.layer_name || node.layer || "UNKNOWN").toString().toUpperCase();
      const tag = mode === "select" ? "FOCUS_LOCK" : "TRACE";

      if (this.storyFields.title) this.storyFields.title.textContent = node.name || "UNKNOWN_NODE";
      if (this.storyFields.subtitle) this.storyFields.subtitle.textContent = `LAYER: ${layerName} // LINKS: ${linkCount}`;
      if (this.storyFields.status) this.storyFields.status.textContent = mode === "select" ? "LOCKED" : "LIVE";

      const lines = [
        `${ts} // ${tag}::${layerName}`,
        `NODE_ID=HEX_${String(node.id || "").toUpperCase().substring(0, 6)}`,
        `SIGNAL=OK // ROUTES=${linkCount}`,
        `DESC=${(node.description || "NO_SECURE_PAYLOAD").toString().slice(0, 72)}`,
      ];
      this.storyFields.lines.innerHTML = lines.map((l) => `<div>${l}</div>`).join("");
    }

    // ===== Event Handling =====

    _bindEvents() {
      // Node Select -> Open Sidebar
      this._listen(this.engine.container, "graph:nodeSelect", (e) => {
        if (e.detail) {
          this._openSidebar(e.detail);
          this._updateStory(e.detail, "select");
        }
      });

      this._listen(this.engine.container, "graph:nodeHover", (e) => {
        if (this.engine.selectedNode) return;
        this._updateStory(e.detail, "hover");
      });

      // Background Click -> Close Sidebar
      this._listen(this.engine.container, "graph:viewReset", () => {
        this._closeSidebar();
        this._setStoryIdle();
      });
    }

    // ===== Visual Fluff =====

    _startLiveStats() {
      const pingEl = document.getElementById("sys-ping");
      const memEl = document.getElementById("sys-mem");

      if (!pingEl || !memEl) return;

      this._liveStatsTimer = setInterval(() => {
        // Randomize Ping
        const ping = 8 + Math.floor(Math.random() * 24);
        pingEl.textContent = `${ping}ms`;

        // Randomize Mem occasionally
        if (Math.random() > 0.9) {
          const mem = 60 + Math.floor(Math.random() * 5);
          memEl.textContent = `${mem}TB`;
        }
      }, 2000);
    }

    destroy() {
      this._clearTyping();
      if (this._liveStatsTimer) {
        clearInterval(this._liveStatsTimer);
        this._liveStatsTimer = null;
      }
      this._unlistenAll();
      this.engine = null;
    }
  }

  global.GraphRenderer = GraphRenderer;

})(typeof window !== "undefined" ? window : this);
