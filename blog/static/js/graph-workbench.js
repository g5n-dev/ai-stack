/**
 * AI Stack graph page bootstrap.
 * Keeps Hugo markup declarative and owns page-level lifecycle and deep links.
 */
(function graphWorkbenchModule(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
    return;
  }

  root.AIStackGraphWorkbench = Object.freeze(api);
  api.bindGraphWorkbench(root.document, root);
}(typeof globalThis !== "undefined" ? globalThis : this, function createGraphWorkbenchApi() {
  "use strict";

  const READY_CLASS = "is-ready";
  const MODES = new Set(["overview", "community", "focus"]);
  const NODE_ID = /^(?:tech|tag|concept|community):[^\u0000-\u001f\u007f<>]{1,220}$/u;

  function parseGraphRequest(search = "") {
    const params = new URLSearchParams(typeof search === "string" ? search : "");
    const mode = String(params.get("mode") || "overview").toLowerCase();
    if (!MODES.has(mode)) return { mode: "overview", node: "" };
    if (mode !== "focus") return { mode, node: "" };
    const node = params.get("node") || "";
    if (!NODE_ID.test(node) || node !== node.trim()) return { mode: "overview", node: "" };
    return { mode: "focus", node };
  }

  async function applyGraphRequest(engine, request) {
    await Promise.resolve(engine.ready);
    const safeRequest = request?.mode === "focus"
      ? parseGraphRequest(`?mode=focus&node=${encodeURIComponent(request.node || "")}`)
      : parseGraphRequest(`?mode=${encodeURIComponent(request?.mode || "overview")}`);
    try {
      if (safeRequest.mode === "focus") {
        // focusNode owns the focus-mode transition and neighborhood load. Calling
        // setMode("focus") first asks the engine to resolve its current/default
        // node, which can render the wrong core before the deep link is applied.
        await engine.focusNode(safeRequest.node);
      } else if (engine.mode !== safeRequest.mode) {
        await engine.setMode(safeRequest.mode);
      }
      return {
        applied: true,
        mode: safeRequest.mode,
        node: safeRequest.node,
      };
    } catch (error) {
      try {
        await engine.setMode("overview");
      } catch (fallbackError) {
        return {
          applied: false,
          mode: "overview",
          node: "",
          message: `${error?.message || error}; ${fallbackError?.message || fallbackError}`,
        };
      }
      return {
        applied: false,
        mode: "overview",
        node: "",
        message: error?.message || String(error),
      };
    }
  }

  function setText(document, id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = String(value ?? "");
  }

  function showError(document, error) {
    const loading = document.getElementById("graph-loading");
    const panel = document.getElementById("graph-error");
    if (loading) loading.hidden = true;
    if (panel) panel.hidden = false;
    setText(document, "graph-error-message", error?.message || error || "数据暂时不可用。");
    setText(document, "graph-live-state", "连接失败");
  }

  function showReady(document, root) {
    const loading = document.getElementById("graph-loading");
    const panel = document.getElementById("graph-error");
    if (loading) loading.hidden = true;
    if (panel) panel.hidden = true;
    root.classList.add(READY_CLASS);
    setText(document, "graph-live-state", "在线");
  }

  function destroyCurrent(global) {
    if (global.graphRenderer && typeof global.graphRenderer.destroy === "function") {
      global.graphRenderer.destroy();
    }
    if (global.graphEngine && typeof global.graphEngine.destroy === "function") {
      global.graphEngine.destroy();
    }
    global.graphRenderer = null;
    global.graphEngine = null;
  }

  async function initialiseGraphWorkbench(document, global, search = global.location?.search || "") {
    const root = document.getElementById("graph-workbench");
    const container = document.getElementById("graph-container");
    if (!root || !container) return null;

    destroyCurrent(global);

    if (typeof global.cytoscape !== "function") {
      showError(document, new Error("Cytoscape 运行时未加载。"));
      return null;
    }
    if (typeof global.CytoscapeGraphEngine !== "function") {
      showError(document, new Error("图谱引擎未加载。"));
      return null;
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

      const request = parseGraphRequest(search);
      const outcome = await applyGraphRequest(engine, request);
      showReady(document, root);
      if (!outcome.applied) {
        setText(document, "graph-live-state", "在线 · 已回到总览");
        setText(document, "graph-search-status", `无法聚焦请求节点，已返回技术总览：${outcome.message}`);
        global.console?.warn("Graph deep link fallback", outcome.message);
      }
      return engine;
    } catch (error) {
      showError(document, error);
      global.console?.error("Graph bootstrap failed", error);
      return null;
    }
  }

  function bindGraphWorkbench(document, global) {
    if (!document || document.documentElement?.dataset.graphWorkbenchBound === "true") return;
    if (document.documentElement) document.documentElement.dataset.graphWorkbenchBound = "true";

    document.addEventListener("DOMContentLoaded", () => {
      initialiseGraphWorkbench(document, global);
    }, { once: true });

    document.addEventListener("visibilitychange", () => {
      const engine = global.graphEngine;
      if (!engine) return;
      if (document.hidden) engine.pause?.();
      else engine.resume?.();
    });

    global.addEventListener("pagehide", (event) => {
      if (event.persisted) {
        global.graphEngine?.pause?.();
        return;
      }
      destroyCurrent(global);
    });

    global.addEventListener("pageshow", (event) => {
      if (!event.persisted) return;
      if (global.graphEngine && !global.graphEngine.isDestroyed) {
        global.graphEngine.resume?.();
        return;
      }
      initialiseGraphWorkbench(document, global);
    });

    document.addEventListener("click", (event) => {
      if (event.target?.id === "graph-retry") initialiseGraphWorkbench(document, global);
    });
  }

  return {
    applyGraphRequest,
    bindGraphWorkbench,
    destroyCurrent,
    initialiseGraphWorkbench,
    parseGraphRequest,
  };
}));
