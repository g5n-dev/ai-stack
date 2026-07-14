/**
 * AI Stack graph page bootstrap.
 * Keeps Hugo markup declarative and owns only page-level lifecycle/error state.
 */
(function (global) {
  "use strict";

  const READY_CLASS = "is-ready";

  function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = String(value ?? "");
  }

  function showError(error) {
    const loading = document.getElementById("graph-loading");
    const panel = document.getElementById("graph-error");
    if (loading) loading.hidden = true;
    if (panel) panel.hidden = false;
    setText("graph-error-message", error?.message || error || "数据暂时不可用。");
    setText("graph-live-state", "连接失败");
  }

  function showReady(root) {
    const loading = document.getElementById("graph-loading");
    const panel = document.getElementById("graph-error");
    if (loading) loading.hidden = true;
    if (panel) panel.hidden = true;
    root.classList.add(READY_CLASS);
    setText("graph-live-state", "在线");
  }

  function destroyCurrent() {
    if (global.graphRenderer && typeof global.graphRenderer.destroy === "function") {
      global.graphRenderer.destroy();
    }
    if (global.graphEngine && typeof global.graphEngine.destroy === "function") {
      global.graphEngine.destroy();
    }
    global.graphRenderer = null;
    global.graphEngine = null;
  }

  async function initialise() {
    const root = document.getElementById("graph-workbench");
    const container = document.getElementById("graph-container");
    if (!root || !container) return;

    destroyCurrent();

    if (typeof global.cytoscape !== "function") {
      showError(new Error("Cytoscape 运行时未加载。"));
      return;
    }
    if (typeof global.CytoscapeGraphEngine !== "function") {
      showError(new Error("图谱引擎未加载。"));
      return;
    }

    try {
      const engine = new global.CytoscapeGraphEngine(container, {
        indexUrl: root.dataset.indexUrl,
        workerUrl: root.dataset.workerUrl,
      });
      global.graphEngine = engine;

      if (typeof global.CytoscapeGraphRenderer === "function") {
        global.graphRenderer = new global.CytoscapeGraphRenderer(engine);
      }

      await Promise.resolve(engine.ready);
      showReady(root);
    } catch (error) {
      showError(error);
      global.console?.error("Graph bootstrap failed", error);
    }
  }

  document.addEventListener("DOMContentLoaded", initialise, { once: true });

  document.addEventListener("visibilitychange", () => {
    const engine = global.graphEngine;
    if (!engine) return;
    if (document.hidden) {
      engine.pause?.();
    } else {
      engine.resume?.();
    }
  });

  global.addEventListener("pagehide", (event) => {
    if (event.persisted) {
      global.graphEngine?.pause?.();
      return;
    }
    destroyCurrent();
  });

  global.addEventListener("pageshow", (event) => {
    if (!event.persisted) return;
    if (global.graphEngine && !global.graphEngine.isDestroyed) {
      global.graphEngine.resume?.();
      return;
    }
    initialise();
  });

  document.addEventListener("click", (event) => {
    if (event.target?.id === "graph-retry") initialise();
  });
})(window);
