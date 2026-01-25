/**
 * AI Stack Graph Renderer
 * Adapts the D3 Graph Engine to the "Nexus Archive" UI
 */

(function (global) {
  "use strict";

  class GraphRenderer {
    constructor(engine) {
      this.engine = engine;
      
      // UI Elements
      this.sidebar = document.getElementById("detail-sidebar");
      this.searchInput = document.getElementById("graph-search");
      this.filterContainer = document.getElementById("active-filters");
      
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

    _init() {
      this._bindToolbar();
      this._bindSearch();
      this._bindSidebar();
      this._renderFilters();
      this._bindEvents();
      this._startLiveStats();
    }

    // ===== UI Bindings =====

    _bindToolbar() {
      // Zoom In
      document.getElementById("btn-zoom-in")?.addEventListener("click", () => {
        const t = this.engine.transform;
        this.engine.transform = { ...t, k: Math.min(3, t.k * 1.2) };
      });

      // Zoom Out
      document.getElementById("btn-zoom-out")?.addEventListener("click", () => {
        const t = this.engine.transform;
        this.engine.transform = { ...t, k: Math.max(0.3, t.k / 1.2) };
      });

      // Reset
      document.getElementById("btn-reset")?.addEventListener("click", () => {
        this.engine.resetView();
        this._closeSidebar();
      });

      // Fit
      document.getElementById("btn-fit")?.addEventListener("click", () => {
        // Simple mock fit, effectively a reset in this engine version
        this.engine.resetView();
      });
    }

    _bindSearch() {
      if (!this.searchInput) return;
      this.searchInput.addEventListener("input", (e) => {
        this.engine.search(e.target.value);
      });
    }

    _bindSidebar() {
      document.getElementById("btn-close-sidebar")?.addEventListener("click", () => {
        this._closeSidebar();
      });

      document.getElementById("btn-focus-node")?.addEventListener("click", () => {
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
        btn.addEventListener("click", () => {
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

    _openSidebar(node) {
      if (!this.sidebar) return;
      
      // Populate Fields
      this.fields.id.textContent = `HEX_${node.id.toUpperCase().substring(0,6)}`;
      this.fields.title.textContent = node.name;
      this.fields.layer.textContent = node.layer_name || "UNKNOWN LAYER";
      this.fields.layer.style.color = node.color;
      
      this.fields.desc.textContent = node.description || "No secure data available for this node. Access restricted or packet loss detected.";
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
      this.engine.selectedNode = null;
    }

    // ===== Event Handling =====

    _bindEvents() {
      // Node Select -> Open Sidebar
      this.engine.container.addEventListener("graph:nodeSelect", (e) => {
        if (e.detail) {
          this._openSidebar(e.detail);
        }
      });

      // Background Click -> Close Sidebar
      this.engine.container.addEventListener("graph:viewReset", () => {
        this._closeSidebar();
      });
    }

    // ===== Visual Fluff =====

    _startLiveStats() {
      const pingEl = document.getElementById("sys-ping");
      const memEl = document.getElementById("sys-mem");
      
      if (!pingEl || !memEl) return;

      setInterval(() => {
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
  }

  global.GraphRenderer = GraphRenderer;

})(typeof window !== "undefined" ? window : this);
