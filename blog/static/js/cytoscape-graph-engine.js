/**
 * AI Stack knowledge-graph runtime.
 * Cytoscape owns graph rendering; a separate canvas owns semantic particles.
 */
(function (global) {
    "use strict";

    const MODES = new Set(["overview", "community", "focus"]);
    const MAX_PARTICLES = 24;
    const COMMUNITY_FIELD_FPS = 24;
    const PARTICLE_FPS = 30;
    const MAX_OVERLAY_PIXELS = 8 * 1024 * 1024;
    const LABEL_EXPAND_ZOOM = 1.25;
    const DEFAULT_LABEL_RANK_LIMIT = 48;
    const OVERVIEW_COMPACT_WIDTH = 720;
    const OVERVIEW_ROUTE_LIMIT = 8;
    const OVERVIEW_RING_PLAN = [
        { count: 6, radiusX: 38, radiusY: 29, phase: -Math.PI / 2 },
        { count: 10, radiusX: 68, radiusY: 50, phase: -Math.PI / 2 + 0.18 },
        { count: 14, radiusX: 102, radiusY: 74, phase: -Math.PI / 2 + 0.08 },
        { count: 18, radiusX: 134, radiusY: 96, phase: -Math.PI / 2 + 0.25 }
    ];
    const OVERVIEW_WIDE_SLOTS = [
        [0.16, 0.25],
        [0.24, 0.74],
        [0.5, 0.49],
        [0.76, 0.74],
        [0.84, 0.25]
    ];
    const OVERVIEW_COMPACT_SLOTS = [
        [0.24, 0.2],
        [0.22, 0.72],
        [0.5, 0.46],
        [0.78, 0.72],
        [0.76, 0.2]
    ];
    const OVERVIEW_LAYER_COLORS = {
        language: "#58ddd2",
        framework: "#30cdbd",
        model: "#efad53",
        application: "#67bfd4",
        scenario: "#9ccbd2"
    };
    const COMMUNITY_DETAIL_RESERVE = 306;
    const COMMUNITY_COMPACT_WIDTH = 900;
    const COMMUNITY_SIDE_DETAIL_MIN_WIDTH = 720;
    const COMMUNITY_TOP_INSET = 22;
    const COMMUNITY_BOTTOM_INSET = 54;
    const COMMUNITY_CONTEXT_SLOTS = [
        [0.363, 0.144],
        [0.572, 0.156],
        [0.798, 0.16],
        [0.124, 0.342],
        [0.89, 0.36],
        [0.14, 0.61],
        [0.33, 0.78],
        [0.8, 0.7],
        [0.56, 0.93],
        [0.91, 0.55]
    ];
    const COMMUNITY_COMPACT_SLOTS = [
        [0.16, 0.18],
        [0.84, 0.18],
        [0.2, 0.82],
        [0.8, 0.82],
        [0.5, 0.06]
    ];
    const FOCUS_CONTEXT_SLOTS = [
        [0.19, 0.2],
        [0.79, 0.19],
        [0.13, 0.51],
        [0.85, 0.5],
        [0.25, 0.81],
        [0.72, 0.82]
    ];
    const FOCUS_COMPACT_SLOTS = [
        [0.18, 0.17],
        [0.82, 0.17],
        [0.12, 0.48],
        [0.88, 0.48],
        [0.25, 0.79],
        [0.75, 0.79]
    ];
    const FOCUS_INNER_LIMIT = 8;
    const FOCUS_GROUP_SIZE = 3;
    const FOCUS_GROUP_LIMIT = 6;
    const DEFAULT_INDEX_URL = "/data/tag-graph/index.json";
    const DEFAULT_WORKER_URL = "/js/data-parser-worker.js";
    const GRAPH_FONT_FALLBACKS = Object.freeze({
        sans: "system-ui, sans-serif",
        mono: "monospace",
        labelSize: 12,
        smallLabelSize: 10,
        featureLabelSize: 11,
        minLabelSize: 10,
        labelWeight: 500,
        strongLabelWeight: 600
    });
    let resolvedGraphFontFamilies = null;

    function readCssFontFamily(propertyName, fallback) {
        const documentElement = global.document?.documentElement;
        if (!documentElement || typeof global.getComputedStyle !== "function") {
            return fallback;
        }
        const value = global.getComputedStyle(documentElement)
            .getPropertyValue(propertyName)
            .trim();
        return value || fallback;
    }

    function readCssNumber(propertyName, fallback) {
        const documentElement = global.document?.documentElement;
        if (!documentElement || typeof global.getComputedStyle !== "function") {
            return fallback;
        }
        const value = Number.parseFloat(
            global.getComputedStyle(documentElement)
                .getPropertyValue(propertyName)
                .trim()
        );
        return Number.isFinite(value) ? value : fallback;
    }

    function graphFontFamilies() {
        if (!resolvedGraphFontFamilies) {
            resolvedGraphFontFamilies = Object.freeze({
                sans: readCssFontFamily("--site-font-sans", GRAPH_FONT_FALLBACKS.sans),
                mono: readCssFontFamily("--site-font-mono", GRAPH_FONT_FALLBACKS.mono),
                labelSize: readCssNumber("--graph-node-label-size", GRAPH_FONT_FALLBACKS.labelSize),
                smallLabelSize: readCssNumber("--graph-node-label-small-size", GRAPH_FONT_FALLBACKS.smallLabelSize),
                featureLabelSize: readCssNumber("--graph-node-label-feature-size", GRAPH_FONT_FALLBACKS.featureLabelSize),
                minLabelSize: readCssNumber("--graph-node-label-min-size", GRAPH_FONT_FALLBACKS.minLabelSize),
                labelWeight: readCssNumber("--graph-node-label-weight", GRAPH_FONT_FALLBACKS.labelWeight),
                strongLabelWeight: readCssNumber("--graph-node-label-strong-weight", GRAPH_FONT_FALLBACKS.strongLabelWeight)
            });
        }
        return resolvedGraphFontFamilies;
    }

    function asArray(value) {
        return Array.isArray(value) ? value : [];
    }

    function asNumber(value, fallback = 0) {
        const number = Number(value);
        return Number.isFinite(number) ? number : fallback;
    }

    function endpointId(endpoint) {
        if (endpoint && typeof endpoint === "object") {
            return String(endpoint.id || endpoint.data?.id || "");
        }
        return endpoint == null ? "" : String(endpoint);
    }

    function createAbortError(message = "Graph operation cancelled") {
        if (typeof global.DOMException === "function") {
            return new global.DOMException(message, "AbortError");
        }
        const error = new Error(message);
        error.name = "AbortError";
        return error;
    }

    function normalizeGraph(payload) {
        const source = payload?.graph && typeof payload.graph === "object"
            ? payload.graph
            : (payload || {});
        const nodes = asArray(source.nodes)
            .filter((node) => node && node.id != null)
            .map((node) => {
                const id = String(node.id);
                return {
                    ...node,
                    id,
                    name: String(node.name || node.label || node.legacy_id || id),
                    degree: asNumber(node.degree ?? node.connections, 0),
                    weighted_degree: asNumber(node.weighted_degree ?? node.weightedDegree, 0),
                    rank: asNumber(node.rank ?? node.pagerank ?? node.score, 0),
                    article_count: asNumber(node.article_count ?? node.articleCount, 0)
                };
            });
        const nodeIds = new Set(nodes.map((node) => node.id));
        const links = (asArray(source.links).length > 0 ? source.links : asArray(source.edges))
            .map((link, index) => {
                const sourceId = endpointId(link?.source);
                const targetId = endpointId(link?.target);
                if (!sourceId || !targetId || !nodeIds.has(sourceId) || !nodeIds.has(targetId)) {
                    return null;
                }
                const weight = asNumber(link.weight ?? link.strength ?? link.value, 1);
                return {
                    ...link,
                    id: String(link.id || `edge:${sourceId}:${targetId}:${index}`),
                    source: sourceId,
                    target: targetId,
                    weight,
                    strength: asNumber(link.strength ?? weight, weight)
                };
            })
            .filter(Boolean);
        return {
            nodes,
            links,
            layers: source.layers || payload?.layers || {},
            stats: source.stats || payload?.stats || {}
        };
    }

    function mergeGraphs(leftPayload, rightPayload) {
        const left = normalizeGraph(leftPayload);
        const right = normalizeGraph(rightPayload);
        const nodes = new Map(left.nodes.map((node) => [node.id, node]));
        const links = new Map(left.links.map((link) => [link.id, link]));
        right.nodes.forEach((node) => nodes.set(node.id, { ...(nodes.get(node.id) || {}), ...node }));
        right.links.forEach((link) => links.set(link.id, link));
        return {
            nodes: Array.from(nodes.values()),
            links: Array.from(links.values()),
            layers: { ...left.layers, ...right.layers },
            stats: { ...left.stats, ...right.stats }
        };
    }

    class CytoscapeGraphEngine {
        constructor(container, input = {}) {
            this.container = typeof container === "string"
                ? global.document?.querySelector(container)
                : container;
            if (!this.container) throw new Error("Graph container not found");

            this.options = this._isLegacyData(input) ? {} : (input || {});
            this.data = {
                nodes: [],
                links: [],
                layers: {},
                stats: {},
                defaults: {},
                generated_at: null,
                version: 1
            };
            this.coreGraph = { nodes: [], links: [], layers: {}, stats: {} };
            this.currentGraph = this.coreGraph;
            this.communityGraph = null;
            this.expandedCommunityId = null;
            this._detailCommunityId = null;
            this._defaultCommunityExpansion = null;
            this.mode = "overview";
            this.layoutMode = "overview";
            this.cy = null;
            this.worker = null;
            this.selectedNode = null;
            this.selectedNodeId = null;
            this.hoveredNode = null;
            this.visibleLayers = new Set();
            this.isDestroyed = false;
            this.reducedMotion = Boolean(
                global.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches
            );

            this._requestSequence = 0;
            this._modeSequence = 0;
            this._searchSequence = 0;
            this._pendingRequests = new Map();
            this._operationRequests = new Map();
            this._activeLayout = null;
            this._layoutRunning = false;
            this._layoutInterrupted = false;
            this._layoutFallback = null;
            this._labelsExpanded = null;
            this._paused = false;
            this._particles = [];
            this._particleFrame = null;
            this._particleTimestamp = 0;
            this._particleDirtyRects = [];
            this._overlayCanvas = null;
            this._overlayContext = null;
            this._overlayWidth = 0;
            this._overlayHeight = 0;
            this._fieldCanvas = null;
            this._fieldContext = null;
            this._fieldWidth = 0;
            this._fieldHeight = 0;
            this._fieldFrame = null;
            this._fieldTimestamp = 0;
            this._fieldDirty = false;
            this._fieldPaintCount = 0;
            this._communityFields = [];
            this._resizeObserver = null;
            this._resizeFitTimer = null;
            this._containerPositionBefore = null;
            this._motionListenerType = null;

            this._handleWindowResize = () => this._handleViewportResize();
            this._handleVisibilityChange = () => {
                if (global.document?.hidden) this.pause();
                else this.resume();
            };
            this._handleMotionChange = (event) => {
                this.reducedMotion = Boolean(event.matches);
                this._syncParticles();
                this._stopCommunityFieldLoop(false);
                this._scheduleCommunityFieldDraw();
            };

            if (this._isLegacyData(input)) {
                try {
                    this._initializeFromLegacyData(input);
                    this.ready = Promise.resolve(this);
                } catch (error) {
                    this._emitError("bootstrap", error);
                    this.ready = Promise.reject(error);
                }
            } else {
                this.ready = this._bootstrapFromWorker();
            }
        }

        _isLegacyData(input) {
            return Boolean(input && (Array.isArray(input.nodes) || Array.isArray(input.links)));
        }

        _initializeFromLegacyData(rawData) {
            const graph = normalizeGraph(rawData);
            this.data = {
                ...this.data,
                ...rawData,
                nodes: graph.nodes,
                links: graph.links,
                layers: { ...(rawData.layers || {}), ...(graph.layers || {}) },
                stats: { ...(rawData.stats || {}), ...(graph.stats || {}) },
                defaults: rawData.defaults || {},
                generated_at: rawData.generated_at || null,
                version: asNumber(rawData.version, 1)
            };
            this.coreGraph = graph;
            this.currentGraph = graph;
            const initiallyVisible = asArray(rawData.initial_visible_layers);
            const layers = initiallyVisible.length > 0
                ? initiallyVisible
                : graph.nodes.map((node) => node.layer).filter(Boolean);
            this.visibleLayers = new Set(layers);
            this._createCytoscape(graph);
            this._emitReady();
        }

        async _bootstrapFromWorker() {
            try {
                this._createWorker();
                const payload = await this._request("bootstrap", {
                    indexUrl: this.options.indexUrl || DEFAULT_INDEX_URL,
                    baseUrl: this.options.baseUrl || ""
                }, { operationKey: "bootstrap" });
                if (this.isDestroyed) throw createAbortError();

                const graph = normalizeGraph(payload.graph);
                this.data = {
                    ...this.data,
                    version: asNumber(payload.version, 1),
                    generated_at: payload.generated_at || null,
                    defaults: payload.defaults || {},
                    layers: { ...(payload.layers || {}), ...(graph.layers || {}) },
                    stats: { ...(graph.stats || {}), ...(payload.stats || {}) },
                    capabilities: payload.capabilities || {},
                    nodes: graph.nodes,
                    links: graph.links
                };
                this.coreGraph = graph;
                this.currentGraph = graph;
                const defaults = asArray(payload.defaults?.initial_visible_layers);
                const layers = defaults.length > 0
                    ? defaults
                    : graph.nodes.map((node) => node.layer).filter(Boolean);
                this.visibleLayers = new Set(layers);
                this._createCytoscape(graph);
                this._emitReady();
                return this;
            } catch (error) {
                if (error?.name !== "AbortError") this._emitError("bootstrap", error);
                throw error;
            }
        }

        _createWorker() {
            const workerUrl = this.options.workerUrl || DEFAULT_WORKER_URL;
            if (typeof this.options.workerFactory === "function") {
                this.worker = this.options.workerFactory(workerUrl);
            } else {
                const WorkerConstructor = global.Worker;
                if (typeof WorkerConstructor !== "function") {
                    throw new Error("Web Worker is not available");
                }
                this.worker = new WorkerConstructor(workerUrl);
            }
            if (!this.worker) throw new Error("Unable to create graph worker");

            this._workerMessageHandler = (event) => this._handleWorkerMessage(event?.data || {});
            this._workerErrorHandler = (event) => {
                const error = event?.error || new Error(event?.message || "Graph worker failed");
                this._rejectPendingRequests(error);
                this._emitError("worker", error);
            };

            if (typeof this.worker.addEventListener === "function") {
                this.worker.addEventListener("message", this._workerMessageHandler);
                this.worker.addEventListener("error", this._workerErrorHandler);
            } else {
                this.worker.onmessage = this._workerMessageHandler;
                this.worker.onerror = this._workerErrorHandler;
            }
        }

        _request(operation, payload = {}, options = {}) {
            if (this.isDestroyed) return Promise.reject(createAbortError());
            if (!this.worker) return Promise.reject(new Error("Graph worker is not initialized"));

            const operationKey = options.operationKey || operation;
            if (options.cancelPrevious !== false) this._cancelOperation(operationKey);
            const id = `graph:${operation}:${++this._requestSequence}`;

            return new Promise((resolve, reject) => {
                this._pendingRequests.set(id, { resolve, reject, operation, operationKey });
                this._operationRequests.set(operationKey, id);
                try {
                    this.worker.postMessage({ id, type: operation, payload });
                } catch (error) {
                    this._pendingRequests.delete(id);
                    if (this._operationRequests.get(operationKey) === id) {
                        this._operationRequests.delete(operationKey);
                    }
                    reject(error);
                }
            });
        }

        _handleWorkerMessage(message) {
            if (this.isDestroyed) return;
            if (message.type === "progress" || message.type === "parsing") {
                this._emit("graph:progress", message);
                return;
            }
            const pending = this._pendingRequests.get(message.id);
            if (!pending) return;
            this._pendingRequests.delete(message.id);
            if (this._operationRequests.get(pending.operationKey) === message.id) {
                this._operationRequests.delete(pending.operationKey);
            }

            if (message.type === "success") {
                pending.resolve(message.data || {});
                return;
            }
            if (message.type === "cancelled") {
                pending.reject(createAbortError());
                return;
            }
            const error = new Error(message.error || `${pending.operation} failed`);
            pending.reject(error);
        }

        _cancelOperation(operationKey) {
            const requestId = this._operationRequests.get(operationKey);
            if (!requestId || !this.worker) return;
            this._operationRequests.delete(operationKey);
            try {
                this.worker.postMessage({
                    id: `graph:cancel:${++this._requestSequence}`,
                    type: "cancel",
                    payload: { requestId }
                });
            } catch (_) {
                // Worker errors are handled by its error event.
            }
        }

        _rejectPendingRequests(error) {
            this._pendingRequests.forEach(({ reject }) => reject(error));
            this._pendingRequests.clear();
            this._operationRequests.clear();
        }

        _createCytoscape(graph) {
            const cytoscapeFactory = global.cytoscape;
            if (typeof cytoscapeFactory !== "function") {
                throw new Error("Cytoscape.js is not available");
            }
            this.cy = cytoscapeFactory({
                container: this.container,
                elements: this._formatElements(graph),
                style: this._getStylesheet(),
                layout: {
                    ...this._getLayoutOptions("overview"),
                    animate: false,
                    animationDuration: 0
                },
                minZoom: 0.12,
                maxZoom: 4,
                textureOnViewport: true,
                hideEdgesOnViewport: graph.links.length > 1500,
                motionBlur: false,
                boxSelectionEnabled: false
            });
            this._bindCytoscapeEvents();
            this._initOverlay();
            this.cy.ready(() => this._settleInitialViewport());
        }

        _settleInitialViewport() {
            if (this.isDestroyed || !this.cy || this.mode !== "overview") return false;
            this._syncOverviewDensity(this.container?.getBoundingClientRect?.() || {});
            this.cy.zoom?.(1);
            this.cy.pan?.({ x: 0, y: 0 });
            this._scheduleCommunityFieldDraw();
            this._emitViewportChange("initial-layout");
            return true;
        }

        _focusSemanticGroupKey(node) {
            const communityId = String(node?.community_id ?? node?.community ?? "").trim();
            if (communityId && communityId !== "community:other" && communityId !== "other") {
                return `community:${communityId}`;
            }
            const category = String(node?.category ?? "").trim();
            if (category && !["article_tag", "tag", "concept", "other"].includes(category)) {
                return `category:${category}`;
            }
            const layer = String(node?.layer ?? "unknown").trim() || "unknown";
            return `layer:${layer}`;
        }

        _buildFocusScenePlan(graphPayload, strengthByNode = new Map()) {
            const graph = normalizeGraph(graphPayload);
            const selectedId = String(this.selectedNodeId || "");
            const compareFocusNodes = (left, right) =>
                asNumber(strengthByNode.get(String(right.id)), 0) -
                    asNumber(strengthByNode.get(String(left.id)), 0) ||
                asNumber(left.rank, Number.MAX_SAFE_INTEGER) -
                    asNumber(right.rank, Number.MAX_SAFE_INTEGER) ||
                String(left.id).localeCompare(String(right.id));
            const neighbors = graph.nodes
                .filter((node) => String(node.id) !== selectedId && node.layer !== "community")
                .sort(compareFocusNodes);
            const innerCount = Math.min(
                FOCUS_INNER_LIMIT,
                Math.max(0, neighbors.length <= FOCUS_INNER_LIMIT + 2
                    ? neighbors.length
                    : Math.ceil(neighbors.length / 3))
            );
            const inner = neighbors.slice(0, innerCount);
            const context = neighbors.slice(innerCount);
            const nodes = new Map();
            if (selectedId) nodes.set(selectedId, { role: "core", groupIndex: -1, groupOrder: 0 });
            inner.forEach((node, index) => {
                nodes.set(String(node.id), {
                    role: "inner",
                    groupIndex: -1,
                    groupOrder: index
                });
            });

            const semanticGroups = new Map();
            context.forEach((node) => {
                const key = this._focusSemanticGroupKey(node);
                if (!semanticGroups.has(key)) semanticGroups.set(key, []);
                semanticGroups.get(key).push(node);
            });
            const chunks = [];
            Array.from(semanticGroups.entries())
                .sort((left, right) => {
                    const leftOrder = context.indexOf(left[1][0]);
                    const rightOrder = context.indexOf(right[1][0]);
                    return leftOrder - rightOrder || left[0].localeCompare(right[0]);
                })
                .forEach(([key, groupNodes]) => {
                    for (let offset = 0; offset < groupNodes.length; offset += FOCUS_GROUP_SIZE) {
                        chunks.push({
                            key: `${key}:${Math.floor(offset / FOCUS_GROUP_SIZE)}`,
                            nodes: groupNodes.slice(offset, offset + FOCUS_GROUP_SIZE)
                        });
                    }
                });
            chunks.sort((left, right) => {
                const leftNode = left.nodes[0];
                const rightNode = right.nodes[0];
                return compareFocusNodes(leftNode, rightNode) || left.key.localeCompare(right.key);
            });
            while (chunks.length > FOCUS_GROUP_LIMIT) {
                const overflow = chunks.pop();
                let targetIndex = 0;
                for (let index = 1; index < chunks.length; index += 1) {
                    if (chunks[index].nodes.length < chunks[targetIndex].nodes.length) {
                        targetIndex = index;
                    }
                }
                chunks[targetIndex].nodes.push(...overflow.nodes);
                chunks[targetIndex].nodes.sort(compareFocusNodes);
            }
            chunks.forEach((group, groupIndex) => {
                group.nodes.forEach((node, groupOrder) => {
                    nodes.set(String(node.id), {
                        role: "context",
                        groupIndex,
                        groupOrder,
                        isGroupAnchor: groupOrder === 0,
                        groupKey: group.key
                    });
                });
            });
            return { nodes, groups: chunks };
        }

        _overviewNodeScore(node) {
            const rank = Math.max(0, asNumber(node?.rank, 0));
            const rankSignal = rank > 0 ? 8 / Math.log2(rank + 2) : 0;
            return Math.log1p(Math.max(0, asNumber(node?.article_count, 0))) * 1.6 +
                Math.log1p(Math.max(0, asNumber(node?.weighted_degree, 0))) * 1.2 +
                Math.log1p(Math.max(0, asNumber(node?.degree, 0))) + rankSignal;
        }

        _buildOverviewScenePlan(graphPayload) {
            const graph = normalizeGraph(graphPayload);
            const layerMetadata = { ...(this.data?.layers || {}), ...(graph.layers || {}) };
            const groups = new Map();
            graph.nodes.forEach((node) => {
                const layer = String(node.layer || "unknown");
                if (!groups.has(layer)) groups.set(layer, []);
                groups.get(layer).push(node);
            });
            const orderedLayers = Array.from(groups.keys()).sort((left, right) =>
                asNumber(layerMetadata[left]?.level, Number.MAX_SAFE_INTEGER) -
                    asNumber(layerMetadata[right]?.level, Number.MAX_SAFE_INTEGER) ||
                left.localeCompare(right)
            );
            const nodes = new Map();
            const layers = [];
            orderedLayers.forEach((layer, layerIndex) => {
                const layerNodes = groups.get(layer).slice().sort((left, right) =>
                    this._overviewNodeScore(right) - this._overviewNodeScore(left) ||
                    asNumber(left.rank, Number.MAX_SAFE_INTEGER) -
                        asNumber(right.rank, Number.MAX_SAFE_INTEGER) ||
                    String(left.id).localeCompare(String(right.id))
                );
                const maximumScore = Math.max(
                    1,
                    ...layerNodes.map((node) => this._overviewNodeScore(node))
                );
                const metadata = layerMetadata[layer] || {};
                const layerName = String(metadata.name || layerNodes[0]?.layer_name || layer);
                const color = OVERVIEW_LAYER_COLORS[layer] || metadata.color || "#58ddd2";
                layerNodes.forEach((node, layerOrder) => {
                    const anchor = layerOrder === 0;
                    const normalizedScore = Math.max(
                        0,
                        Math.min(1, this._overviewNodeScore(node) / maximumScore)
                    );
                    nodes.set(String(node.id), {
                        role: anchor ? "anchor" : "satellite",
                        layer,
                        layerIndex,
                        layerOrder,
                        layerCount: layerNodes.length,
                        layerName,
                        color,
                        primary: layer === "model",
                        key: !anchor && layerOrder <= 2,
                        visualSize: anchor ? 21 : 5.5 + normalizedScore * 7.5,
                        label: anchor
                            ? `${String(layerIndex + 1).padStart(2, "0")}  ${layerName}\n${node.name} · ${layerNodes.length} 节点`
                            : node.name
                    });
                });
                layers.push({
                    id: layer,
                    index: layerIndex,
                    name: layerName,
                    color,
                    count: layerNodes.length,
                    anchorId: String(layerNodes[0]?.id || "")
                });
            });
            return { nodes, layers };
        }

        _formatElements(graphPayload) {
            const graph = normalizeGraph(graphPayload);
            const isOverviewMode = this.mode === "overview";
            const isFocusMode = this.mode === "focus";
            const layerMetadata = { ...(this.data.layers || {}), ...(graph.layers || {}) };
            const overviewScene = isOverviewMode
                ? this._buildOverviewScenePlan(graph)
                : { nodes: new Map(), layers: [] };
            const nodeLayerById = new Map(graph.nodes.map((node) => [
                String(node.id),
                String(node.layer || "unknown")
            ]));
            const communityScale = Math.max(1, ...graph.nodes
                .filter((node) => node.layer === "community" && node.id !== "community:other")
                .map((node) => Math.log1p(asNumber(node.node_count ?? node.degree, 0))));
            const edgeScale = Math.max(1, ...graph.links
                .map((link) => Math.log1p(asNumber(link.weight ?? link.strength, 1))));
            const focusStrengthByNode = new Map();
            if (isFocusMode) {
                graph.links.forEach((link) => {
                    const strength = asNumber(link.weight ?? link.strength, 1);
                    [link.source, link.target].forEach((nodeId) => {
                        focusStrengthByNode.set(
                            String(nodeId),
                            Math.max(strength, focusStrengthByNode.get(String(nodeId)) || 0)
                        );
                    });
                });
            }
            const focusStrengthScale = Math.max(
                1,
                ...Array.from(focusStrengthByNode.values(), (value) => Math.log1p(value))
            );
            const focusScene = isFocusMode
                ? this._buildFocusScenePlan(graph, focusStrengthByNode)
                : { nodes: new Map(), groups: [] };
            const hotspotOrder = new Map(graph.nodes
                .filter((node) => node.graph_role === "community-hotspot")
                .sort((left, right) =>
                    asNumber(left.rank, Number.MAX_SAFE_INTEGER) -
                        asNumber(right.rank, Number.MAX_SAFE_INTEGER) ||
                    String(left.id).localeCompare(String(right.id))
                )
                .map((node, index) => [String(node.id), index]));
            const nodes = graph.nodes.map((node) => {
                const layer = layerMetadata[node.layer] || {};
                const rankImportance = asNumber(node.rank) > 0 ? 100 / asNumber(node.rank) : 0;
                const importance = Math.max(
                    rankImportance,
                    asNumber(node.weighted_degree),
                    asNumber(node.degree),
                    asNumber(node.article_count)
                );
                const classes = [];
                const overviewRole = overviewScene.nodes.get(String(node.id));
                if (overviewRole) {
                    classes.push(
                        "overview-node",
                        `overview-${overviewRole.role}`,
                        `overview-layer-${overviewRole.layer}`
                    );
                    if (overviewRole.primary) classes.push("overview-primary");
                    if (overviewRole.key) classes.push("overview-key");
                }
                if (node.layer === "community") classes.push("community-node");
                if (node.layer === "community") {
                    const communityRank = asNumber(node.rank, 0);
                    if (communityRank === 8) classes.push("community-label-left");
                    else if (communityRank === 9) classes.push("community-label-right");
                    else if (communityRank === 10) classes.push("community-label-low");
                    else classes.push("community-label-top");
                }
                if (node.graph_role) classes.push(String(node.graph_role));
                const isFocusCore = isFocusMode && String(node.id) === String(this.selectedNodeId);
                if (isFocusMode && node.layer !== "community") {
                    classes.push("focus-node", isFocusCore ? "focus-core" : "focus-neighbor");
                    const focusRole = focusScene.nodes.get(String(node.id));
                    if (focusRole?.role) classes.push(`focus-${focusRole.role}`);
                    if (focusRole?.isGroupAnchor) classes.push("focus-group-anchor");
                }
                if (node.graph_role === "community-hotspot") {
                    const hotspotIndex = hotspotOrder.get(String(node.id)) || 0;
                    let ringOffset = 0;
                    let ringCount = 5;
                    let phase = -Math.PI / 2;
                    if (hotspotIndex >= 13) {
                        ringOffset = 13;
                        ringCount = 11;
                        phase += 0.08;
                    } else if (hotspotIndex >= 5) {
                        ringOffset = 5;
                        ringCount = 8;
                        phase += 0.2;
                    }
                    const angle = phase +
                        ((hotspotIndex - ringOffset) / Math.max(1, ringCount)) * Math.PI * 2;
                    if (Math.cos(angle) < 0) classes.push("hotspot-label-left");
                }
                if (
                    this._shouldDeferLabel(node) ||
                    (overviewRole?.role === "satellite" && !overviewRole.key)
                ) {
                    classes.push("deferred-label");
                }
                const communityImportance = Math.log1p(asNumber(
                    node.node_count ?? node.degree ?? node.article_count,
                    0
                )) / communityScale;
                const hotspotImportance = Math.log1p(Math.max(0, importance)) / Math.log1p(100);
                const focusStrength = focusStrengthByNode.get(String(node.id)) || 0;
                const focusImportance = Math.log1p(focusStrength) / focusStrengthScale;
                const focusTier = focusImportance >= 0.68 ? 3 : focusImportance >= 0.38 ? 2 : 1;
                const communityLabel = node.layer === "community"
                    ? `${String(Math.max(0, asNumber(node.rank, 0))).padStart(2, "0")}  ${node.name}\n${node.graph_role === "community-anchor" ? "展开中 · " : ""}${asNumber(node.node_count ?? node.degree, 0)} 节点`
                    : overviewRole?.label || node.name;
                return {
                    data: {
                        ...node,
                        label: communityLabel,
                        layerName: node.layer_name || layer.name || node.layer || "Unknown",
                        color: node.color || layer.color || "#4db6ac",
                        visualSize: overviewRole
                            ? overviewRole.visualSize
                            : isFocusMode && node.layer !== "community"
                            ? (isFocusCore ? 32 : 10 + Math.max(0, Math.min(1, focusImportance)) * 12)
                            : node.graph_role === "community-hotspot"
                                ? Math.min(10, 5.2 + Math.max(0, Math.min(1, hotspotImportance)) * 4.8)
                                : Math.min(64, 22 + Math.log1p(Math.max(0, importance)) * 7),
                        focusStrength,
                        focusTier,
                        focusSceneRole: focusScene.nodes.get(String(node.id))?.role || "",
                        focusGroupIndex: focusScene.nodes.get(String(node.id))?.groupIndex ?? -1,
                        focusGroupOrder: focusScene.nodes.get(String(node.id))?.groupOrder ?? -1,
                        communityVisualSize: 15 + Math.max(0, communityImportance) * 8,
                        overviewVisualSize: overviewRole?.visualSize || 0,
                        overviewSceneRole: overviewRole?.role || "",
                        overviewLayerIndex: overviewRole?.layerIndex ?? -1,
                        overviewLayerOrder: overviewRole?.layerOrder ?? -1,
                        overviewLayerCount: overviewRole?.layerCount ?? 0,
                        overviewLayerName: overviewRole?.layerName || "",
                        overviewColor: overviewRole?.color || node.color || layer.color || "#58ddd2"
                    },
                    classes: classes.join(" ")
                };
            });
            const edges = graph.links.map((link, index) => {
                const type = String(link.type || "");
                const classes = [];
                if (isOverviewMode) {
                    const sourceLayer = nodeLayerById.get(String(link.source));
                    const targetLayer = nodeLayerById.get(String(link.target));
                    classes.push(
                        "overview-link",
                        sourceLayer === targetLayer
                            ? "overview-inner-link"
                            : "overview-cross-link"
                    );
                }
                if (type === "community") classes.push("community-link");
                if (type === "community-member") classes.push("community-member-link");
                if (isFocusMode) {
                    classes.push("focus-link");
                    const sourceRole = focusScene.nodes.get(String(link.source))?.role;
                    const targetRole = focusScene.nodes.get(String(link.target))?.role;
                    if (sourceRole === "context" || targetRole === "context") {
                        classes.push("focus-context-link");
                    } else {
                        classes.push("focus-inner-link");
                    }
                }
                let source = link.source;
                let target = link.target;
                if (
                    type === "community" && this.expandedCommunityId &&
                    target === this.expandedCommunityId && source !== this.expandedCommunityId
                ) {
                    source = link.target;
                    target = link.source;
                }
                return {
                    data: {
                        ...link,
                        source,
                        target,
                        weight: asNumber(link.weight ?? link.strength, 1),
                        visualWeight: Math.log1p(asNumber(link.weight ?? link.strength, 1)) / edgeScale,
                        curveOffset: isFocusMode
                            ? (index % 2 === 0 ? -1 : 1) * (8 + (index % 4) * 3)
                            : 0
                    },
                    classes: classes.join(" ")
                };
            });
            return { nodes, edges };
        }

        _getStylesheet() {
            const fonts = graphFontFamilies();
            return [
                {
                    selector: "node",
                    style: {
                        width: "data(visualSize)",
                        height: "data(visualSize)",
                        "background-color": "data(color)",
                        "background-opacity": 0.9,
                        label: "data(label)",
                        color: "#e5f8f7",
                        "font-family": fonts.sans,
                        "font-size": fonts.labelSize,
                        "font-weight": fonts.labelWeight,
                        "min-zoomed-font-size": fonts.minLabelSize,
                        "text-valign": "bottom",
                        "text-halign": "center",
                        "text-margin-y": 8,
                        "text-wrap": "ellipsis",
                        "text-max-width": 128,
                        "text-outline-color": "#071019",
                        "text-outline-width": 3,
                        "border-width": 1.5,
                        "border-color": "data(color)",
                        "border-opacity": 0.75,
                        "transition-property": "opacity, border-width, border-opacity, background-opacity",
                        "transition-duration": "180ms"
                    }
                },
                {
                    selector: "node.overview-node",
                    style: {
                        shape: "ellipse",
                        width: "data(overviewVisualSize)",
                        height: "data(overviewVisualSize)",
                        "background-color": "#071923",
                        "background-opacity": 0.72,
                        "border-color": "data(overviewColor)",
                        "border-width": 1.1,
                        "border-opacity": 0.94,
                        "underlay-color": "data(overviewColor)",
                        "underlay-padding": 3,
                        "underlay-opacity": 0.035,
                        "overlay-opacity": 0,
                        color: "#d8eeee",
                        "font-size": fonts.smallLabelSize,
                        "font-weight": fonts.labelWeight,
                        "min-zoomed-font-size": fonts.minLabelSize,
                        "text-margin-y": 5,
                        "text-outline-width": 2.2,
                        "text-max-width": 76
                    }
                },
                {
                    selector: "node.overview-node.overview-satellite",
                    style: {
                        "background-opacity": 0.5,
                        "underlay-opacity": 0.018
                    }
                },
                {
                    selector: "node.overview-node.overview-key",
                    style: {
                        "background-opacity": 0.78,
                        "border-width": 1.3,
                        "font-size": fonts.smallLabelSize,
                        "text-background-color": "#071019",
                        "text-background-opacity": 0.64,
                        "text-background-padding": 1.5
                    }
                },
                {
                    selector: "node.overview-node.overview-anchor",
                    style: {
                        width: 21,
                        height: 21,
                        "background-color": "#0a2930",
                        "background-opacity": 0.96,
                        "border-width": 2.2,
                        "underlay-padding": 7,
                        "underlay-opacity": 0.1,
                        "text-valign": "top",
                        "text-halign": "center",
                        "text-margin-y": -88,
                        "font-size": fonts.featureLabelSize,
                        "font-weight": fonts.strongLabelWeight,
                        "text-wrap": "wrap",
                        "text-max-width": 116,
                        "text-background-color": "#07131b",
                        "text-background-opacity": 0.9,
                        "text-background-padding": 3.5,
                        "text-background-shape": "roundrectangle",
                        "text-border-color": "data(overviewColor)",
                        "text-border-width": 1,
                        "text-border-opacity": 0.62
                    }
                },
                {
                    selector: "node.overview-node.overview-anchor.overview-primary",
                    style: {
                        "background-color": "#6b4212",
                        "background-opacity": 0.92,
                        "border-color": "#f8c15c",
                        "underlay-color": "#d97706",
                        "underlay-opacity": 0.14,
                        color: "#f8d18b",
                        "text-border-color": "#8b5a1b"
                    }
                },
                {
                    selector: "node.overview-node.overview-anchor.overview-primary.overview-primary-muted",
                    style: {
                        "background-color": "#0a2930",
                        "background-opacity": 0.96,
                        "border-color": "data(overviewColor)",
                        "underlay-color": "data(overviewColor)",
                        "underlay-opacity": 0.1,
                        color: "#d8eeee",
                        "text-border-color": "data(overviewColor)"
                    }
                },
                {
                    selector: "node.overview-node.overview-compact",
                    style: {
                        width: "mapData(overviewVisualSize, 5, 21, 4, 13)",
                        height: "mapData(overviewVisualSize, 5, 21, 4, 13)",
                        "font-size": fonts.smallLabelSize,
                        "text-max-width": 56
                    }
                },
                {
                    selector: "node.overview-node.overview-anchor.overview-compact",
                    style: {
                        width: 15,
                        height: 15,
                        "text-margin-y": -47,
                        "font-size": fonts.smallLabelSize,
                        "text-max-width": 78,
                        "text-background-padding": 2.5
                    }
                },
                {
                    selector: "node.overview-key-mobile-hidden",
                    style: { label: "", "text-opacity": 0 }
                },
                {
                    selector: "node.overview-key-mobile-hidden.search-match",
                    style: { label: "data(label)", "text-opacity": 1 }
                },
                {
                    selector: "node.community-node",
                    style: {
                        shape: "ellipse",
                        width: "data(communityVisualSize)",
                        height: "data(communityVisualSize)",
                        "text-valign": "top",
                        "text-margin-y": -12,
                        "font-size": fonts.featureLabelSize,
                        "font-weight": fonts.strongLabelWeight,
                        "text-wrap": "wrap",
                        "text-max-width": 118,
                        "text-background-color": "#07131b",
                        "text-background-opacity": 0.84,
                        "text-background-padding": 3.5,
                        "text-background-shape": "roundrectangle",
                        "text-border-color": "#244c56",
                        "text-border-width": 1,
                        "text-border-opacity": 0.7,
                        "background-color": "#0e3038",
                        "background-opacity": 0.86,
                        "border-color": "#33e6d2",
                        "border-width": 1.7,
                        "border-opacity": 0.9
                    }
                },
                {
                    selector: "node.community-node.community-context",
                    style: {
                        "overlay-opacity": 0,
                        "text-margin-y": -102
                    }
                },
                {
                    selector: "node.community-node.community-context.community-label-left",
                    style: {
                        "text-valign": "center",
                        "text-halign": "left",
                        "text-margin-x": -112,
                        "text-margin-y": 0
                    }
                },
                {
                    selector: "node.community-node.community-context.community-label-right",
                    style: {
                        "text-valign": "center",
                        "text-halign": "right",
                        "text-margin-x": 112,
                        "text-margin-y": 0
                    }
                },
                {
                    selector: "node.community-node.community-context.community-label-low",
                    style: {
                        "text-valign": "top",
                        "text-halign": "center",
                        "text-margin-x": 0,
                        "text-margin-y": -52
                    }
                },
                {
                    selector: "node.community-node.community-compact",
                    style: {
                        "font-size": fonts.smallLabelSize,
                        "text-max-width": 82,
                        "text-valign": "top",
                        "text-halign": "center",
                        "text-margin-x": 0,
                        "text-margin-y": -52
                    }
                },
                {
                    selector: "node.community-node.community-anchor.community-compact",
                    style: { "text-margin-y": -96 }
                },
                {
                    selector: "node.community-compact-hidden",
                    style: { display: "none" }
                },
                {
                    selector: "node.community-node.community-anchor",
                    style: {
                        width: 21,
                        height: 21,
                        "background-color": "#d97706",
                        "background-opacity": 0.98,
                        "border-color": "#f8c15c",
                        "border-width": 2.4,
                        "overlay-color": "#d97706",
                        "overlay-padding": 8,
                        "overlay-opacity": 0.16,
                        color: "#f8c15c",
                        "text-background-color": "#160f08",
                        "text-border-color": "#8b5a1b",
                        "text-margin-y": -145
                    }
                },
                {
                    selector: "node.community-hotspot",
                    style: {
                        shape: "ellipse",
                        width: "data(visualSize)",
                        height: "data(visualSize)",
                        "background-color": "#a96820",
                        "background-opacity": 0.92,
                        "border-color": "#efad53",
                        "border-width": 0.9,
                        color: "#ead2ad",
                        "font-size": fonts.smallLabelSize,
                        "font-weight": fonts.labelWeight,
                        "min-zoomed-font-size": fonts.minLabelSize,
                        "text-valign": "center",
                        "text-halign": "right",
                        "text-margin-x": 6,
                        "text-margin-y": 0,
                        "text-wrap": "ellipsis",
                        "text-max-width": 76,
                        "text-outline-width": 2,
                        "text-background-color": "#071019",
                        "text-background-opacity": 0.72,
                        "text-background-padding": 2
                    }
                },
                {
                    selector: "node.community-hotspot.hotspot-label-left",
                    style: {
                        "text-halign": "left",
                        "text-margin-x": -6
                    }
                },
                {
                    selector: "node.community-hotspot.community-compact-label-hidden",
                    style: { label: "", "text-opacity": 0 }
                },
                {
                    selector: "node.deferred-label",
                    style: { label: "", "text-opacity": 0 }
                },
                {
                    selector: "node.deferred-label.label-visible",
                    style: { label: "data(label)", "text-opacity": 1 }
                },
                {
                    selector: "node:selected, node.focus-root",
                    style: {
                        "background-color": "#13282d",
                        "border-width": 2.4,
                        "border-color": "#f2a53a",
                        "border-opacity": 1,
                        "background-opacity": 0.94,
                        "underlay-color": "#f2a53a",
                        "underlay-padding": 6,
                        "underlay-opacity": 0.1,
                        "overlay-opacity": 0
                    }
                },
                {
                    selector: "node.community-anchor:selected, node.community-anchor.focus-root",
                    style: {
                        "border-width": 2.4,
                        "border-color": "#f8c15c",
                        "overlay-color": "#d97706",
                        "overlay-padding": 9,
                        "overlay-opacity": 0.1
                    }
                },
                {
                    selector: "node.search-match",
                    style: {
                        "border-width": 4,
                        "border-color": "#f8c15c",
                        "border-opacity": 1,
                        "background-opacity": 1
                    }
                },
                {
                    selector: "node.focus-neighbor",
                    style: {
                        "background-color": "#071923",
                        "background-opacity": 0.38,
                        "border-color": "#4db6ac",
                        "border-width": 1.25,
                        "border-opacity": 0.88,
                        "underlay-color": "#33e6d2",
                        "underlay-padding": 3,
                        "underlay-opacity": 0.045,
                        "overlay-opacity": 0,
                        color: "#c8d8dc",
                        "font-size": fonts.smallLabelSize,
                        "font-weight": fonts.labelWeight,
                        "text-margin-y": 6,
                        "text-outline-width": 2.2
                    }
                },
                {
                    selector: "node.focus-neighbor.is-hovered",
                    style: {
                        "background-opacity": 0.54,
                        "border-color": "#75e6d8",
                        "border-width": 2,
                        "underlay-padding": 5,
                        "underlay-opacity": 0.13
                    }
                },
                {
                    selector: "node.focus-neighbor:selected",
                    style: {
                        "background-color": "#d97706",
                        "background-opacity": 0.22,
                        "border-color": "#f2a53a",
                        "border-width": 2.1,
                        "underlay-color": "#f2a53a",
                        "underlay-padding": 6,
                        "underlay-opacity": 0.12
                    }
                },
                {
                    selector: "node.focus-core",
                    style: {
                        width: 32,
                        height: 32,
                        "background-color": "#d97706",
                        "background-opacity": 0.24,
                        "border-color": "#f2a53a",
                        "border-width": 2.4,
                        "border-opacity": 1,
                        "underlay-color": "#f2a53a",
                        "underlay-padding": 7,
                        "underlay-opacity": 0.14,
                        "overlay-opacity": 0,
                        color: "#fff2d5",
                        "font-size": fonts.labelSize,
                        "font-weight": fonts.strongLabelWeight,
                        "text-margin-y": 7,
                        "text-outline-width": 3
                    }
                },
                {
                    selector: "node.focus-inner",
                    style: {
                        "background-color": "#a96820",
                        "background-opacity": 0.86,
                        "border-color": "#efad53",
                        "border-width": 1.25,
                        "border-opacity": 0.96,
                        color: "#ead2ad",
                        "underlay-color": "#d97706",
                        "underlay-padding": 2,
                        "underlay-opacity": 0.04
                    }
                },
                {
                    selector: "node.focus-context",
                    style: {
                        label: "",
                        "text-opacity": 0,
                        "background-color": "#071923",
                        "background-opacity": 0.58,
                        "border-color": "#5fe1d6",
                        "border-width": 1.15,
                        "border-opacity": 0.9,
                        "underlay-opacity": 0
                    }
                },
                {
                    selector: "node.focus-context.focus-group-anchor",
                    style: {
                        label: "data(label)",
                        "text-opacity": 1,
                        width: 18,
                        height: 18,
                        "background-opacity": 0.78,
                        "border-color": "#33e6d2",
                        "border-width": 1.9,
                        "underlay-color": "#33e6d2",
                        "underlay-padding": 5,
                        "underlay-opacity": 0.06,
                        "font-size": fonts.smallLabelSize,
                        "font-weight": fonts.strongLabelWeight,
                        "text-valign": "top",
                        "text-halign": "center",
                        "text-margin-y": -42,
                        "text-wrap": "ellipsis",
                        "text-max-width": 86,
                        "text-background-color": "#07131b",
                        "text-background-opacity": 0.9,
                        "text-background-padding": 3.5,
                        "text-background-shape": "roundrectangle",
                        "text-border-color": "#244c56",
                        "text-border-width": 1,
                        "text-border-opacity": 0.78
                    }
                },
                {
                    selector: "node.focus-context.label-visible",
                    style: { label: "data(label)", "text-opacity": 1 }
                },
                {
                    selector: "node.faded",
                    style: { opacity: 0.12, "text-opacity": 0.08 }
                },
                {
                    selector: "edge",
                    style: {
                        width: "mapData(weight, 0, 20, 0.6, 3)",
                        "line-color": "#4db6ac",
                        "line-opacity": 0.2,
                        "curve-style": "bezier",
                        "target-arrow-shape": "none",
                        "transition-property": "opacity, line-opacity, width",
                        "transition-duration": "180ms"
                    }
                },
                {
                    selector: "edge.overview-link",
                    style: {
                        width: "mapData(visualWeight, 0, 1, 0.35, 0.85)",
                        "line-color": "#58b8b4",
                        "line-opacity": 0.018,
                        "curve-style": "unbundled-bezier",
                        "control-point-distances": 18,
                        "control-point-weights": 0.5,
                        "target-arrow-shape": "none"
                    }
                },
                {
                    selector: "edge.overview-inner-link",
                    style: {
                        "line-opacity": 0.15,
                        "curve-style": "straight"
                    }
                },
                {
                    selector: "edge.overview-cross-link",
                    style: {
                        "line-opacity": 0.012,
                        "line-style": "solid"
                    }
                },
                {
                    selector: "edge.community-link",
                    style: {
                        width: "mapData(visualWeight, 0, 1, 0.7, 2.2)",
                        "line-color": "#3ebfb4",
                        "line-opacity": 0.035,
                        "line-style": "dashed",
                        "line-dash-pattern": [8, 8],
                        "curve-style": "unbundled-bezier",
                        "control-point-distances": 28,
                        "control-point-weights": 0.5,
                        "target-arrow-shape": "none"
                    }
                },
                {
                    selector: "edge.community-member-link",
                    style: {
                        width: "mapData(visualWeight, 0, 1, 0.5, 1.6)",
                        "line-color": "#d97706",
                        "line-opacity": 0.3,
                        "line-style": "solid",
                        "curve-style": "straight"
                    }
                },
                {
                    selector: "edge.highlighted",
                    style: {
                        width: 2.6,
                        "line-color": "#33e6d2",
                        "line-opacity": 0.9,
                        "target-arrow-shape": "none"
                    }
                },
                {
                    selector: "edge.community-member-link.highlighted",
                    style: {
                        width: "mapData(visualWeight, 0, 1, 0.65, 1.35)",
                        "line-color": "#d9902e",
                        "line-opacity": 0.44,
                        "target-arrow-shape": "none"
                    }
                },
                {
                    selector: "edge.community-route",
                    style: {
                        width: 0.1,
                        "line-color": "#75e6d8",
                        "line-opacity": 0,
                        "line-style": "dashed",
                        "line-dash-pattern": [10, 7],
                        "target-arrow-shape": "none",
                        "target-arrow-color": "#75e6d8",
                        "arrow-scale": 0.72
                    }
                },
                {
                    selector: "edge.faded",
                    style: { opacity: 0.04 }
                },
                {
                    selector: "edge.focus-link",
                    style: {
                        width: "mapData(visualWeight, 0, 1, 0.45, 1.15)",
                        "line-color": "#54cfc2",
                        "line-opacity": "mapData(visualWeight, 0, 1, 0.1, 0.28)",
                        "curve-style": "unbundled-bezier",
                        "control-point-distances": "data(curveOffset)",
                        "control-point-weights": 0.48,
                        "target-arrow-shape": "none"
                    }
                },
                {
                    selector: "edge.focus-link.highlighted",
                    style: {
                        width: "mapData(visualWeight, 0, 1, 0.65, 1.45)",
                        "line-color": "#75e6d8",
                        "line-opacity": "mapData(visualWeight, 0, 1, 0.24, 0.52)"
                    }
                },
                {
                    selector: "edge.focus-inner-link",
                    style: {
                        width: "mapData(visualWeight, 0, 1, 0.55, 1.25)",
                        "line-color": "#d9902e",
                        "line-opacity": "mapData(visualWeight, 0, 1, 0.18, 0.42)",
                        "curve-style": "straight"
                    }
                },
                {
                    selector: "edge.focus-context-link",
                    style: {
                        width: 0.65,
                        "line-color": "#5fe1d6",
                        "line-opacity": 0.035,
                        "line-style": "dashed",
                        "line-dash-pattern": [7, 9],
                        "curve-style": "unbundled-bezier"
                    }
                },
                {
                    selector: "edge.focus-context-link.highlighted",
                    style: {
                        width: 1.1,
                        "line-color": "#75e6d8",
                        "line-opacity": 0.42
                    }
                },
                {
                    selector: ".layer-hidden",
                    style: { display: "none" }
                }
            ];
        }

        _communitySceneMetrics(bounds = {}, hasSelection = false) {
            const width = Math.max(320, asNumber(bounds.width, 960));
            const height = Math.max(360, asNumber(bounds.height, 720));
            const usesSideDetail = Boolean(
                hasSelection && width > COMMUNITY_SIDE_DETAIL_MIN_WIDTH
            );
            const detailReserve = usesSideDetail
                ? Math.min(COMMUNITY_DETAIL_RESERVE, Math.max(0, width - 320))
                : 0;
            const safeWidth = Math.max(320, width - detailReserve);
            const compact = width <= COMMUNITY_COMPACT_WIDTH || height < 560;
            const topInset = compact ? 30 : COMMUNITY_TOP_INSET + 36;
            const bottomInset = compact ? 72 : COMMUNITY_BOTTOM_INSET;
            const safeHeight = Math.max(260, height - topInset - bottomInset);
            const sceneScale = Math.max(0.48, Math.min(1, safeWidth / 963));
            return {
                width,
                height,
                compact,
                usesSideDetail,
                detailReserve,
                safeWidth,
                safeHeight,
                topInset,
                bottomInset,
                sceneScale
            };
        }

        _overviewSceneMetrics(bounds = {}, hasSelection = false) {
            const width = Math.max(320, asNumber(bounds.width, 1180));
            const height = Math.max(360, asNumber(bounds.height, 720));
            const usesSideDetail = Boolean(
                hasSelection && width > COMMUNITY_SIDE_DETAIL_MIN_WIDTH
            );
            const detailReserve = usesSideDetail
                ? Math.min(COMMUNITY_DETAIL_RESERVE, Math.max(0, width - 320))
                : 0;
            const safeWidth = Math.max(320, width - detailReserve);
            const compact = safeWidth <= OVERVIEW_COMPACT_WIDTH || height < 520;
            const topInset = compact ? 52 : 76;
            const bottomInset = compact ? 54 : 62;
            const safeHeight = Math.max(250, height - topInset - bottomInset);
            const sceneScale = Math.max(
                0.42,
                Math.min(1.16, safeWidth / 1180, safeHeight / 640)
            );
            return {
                width,
                height,
                compact,
                usesSideDetail,
                detailReserve,
                safeWidth,
                safeHeight,
                topInset,
                bottomInset,
                sceneScale
            };
        }

        _overviewLayerSlots(orderedLayers, compact = false) {
            const layers = asArray(orderedLayers).map(String);
            const baseSlots = compact ? OVERVIEW_COMPACT_SLOTS : OVERVIEW_WIDE_SLOTS;
            if (layers.length <= baseSlots.length) return baseSlots.slice(0, layers.length);

            const primaryIndex = Math.max(0, layers.indexOf("model"));
            const slots = new Array(layers.length);
            slots[primaryIndex] = compact ? [0.5, 0.46] : [0.5, 0.49];
            const outerIndices = layers
                .map((_, index) => index)
                .filter((index) => index !== primaryIndex);
            const radiusX = compact ? 0.32 : 0.36;
            const radiusY = compact ? 0.29 : 0.31;
            outerIndices.forEach((layerIndex, orbitIndex) => {
                const angle = -Math.PI / 2 +
                    (orbitIndex / Math.max(1, outerIndices.length)) * Math.PI * 2;
                slots[layerIndex] = [
                    0.5 + Math.cos(angle) * radiusX,
                    0.49 + Math.sin(angle) * radiusY
                ];
            });
            return slots;
        }

        _overviewPresetPositions(nodes, bounds = {}) {
            const metrics = this._overviewSceneMetrics(
                bounds,
                Boolean(this.selectedNode?.length > 0)
            );
            const {
                compact,
                safeWidth,
                safeHeight,
                topInset,
                sceneScale
            } = metrics;
            const sourceNodes = asArray(nodes).map((node) =>
                typeof node?.data === "function" ? node.data() : node
            ).filter(Boolean);
            const groups = new Map();
            sourceNodes.forEach((node) => {
                const layer = String(node.layer || "unknown");
                if (!groups.has(layer)) groups.set(layer, []);
                groups.get(layer).push(node);
            });
            const layerMetadata = this.data?.layers || {};
            const orderedLayers = Array.from(groups.keys()).sort((left, right) =>
                asNumber(layerMetadata[left]?.level, Number.MAX_SAFE_INTEGER) -
                    asNumber(layerMetadata[right]?.level, Number.MAX_SAFE_INTEGER) ||
                left.localeCompare(right)
            );
            const slots = this._overviewLayerSlots(orderedLayers, compact);
            const positions = {};
            orderedLayers.forEach((layer, layerIndex) => {
                const slot = slots[layerIndex];
                const center = {
                    x: safeWidth * slot[0],
                    y: topInset + safeHeight * slot[1]
                };
                const layerNodes = groups.get(layer).slice().sort((left, right) =>
                    asNumber(left.overviewLayerOrder, Number.MAX_SAFE_INTEGER) -
                        asNumber(right.overviewLayerOrder, Number.MAX_SAFE_INTEGER) ||
                    this._overviewNodeScore(right) - this._overviewNodeScore(left) ||
                    String(left.id).localeCompare(String(right.id))
                );
                const anchor = layerNodes.find((node) =>
                    node.overviewSceneRole === "anchor"
                ) || layerNodes[0];
                if (anchor) positions[String(anchor.id)] = center;
                const satellites = layerNodes.filter((node) => !anchor || node.id !== anchor.id);
                let offset = 0;
                OVERVIEW_RING_PLAN.forEach((ring) => {
                    const ringNodes = satellites.slice(offset, offset + ring.count);
                    ringNodes.forEach((node, index) => {
                        const angle = ring.phase +
                            (index / Math.max(1, ringNodes.length)) * Math.PI * 2;
                        positions[String(node.id)] = {
                            x: center.x + Math.cos(angle) * ring.radiusX * sceneScale,
                            y: center.y + Math.sin(angle) * ring.radiusY * sceneScale
                        };
                    });
                    offset += ringNodes.length;
                });
                satellites.slice(offset).forEach((node, index, overflow) => {
                    const angle = -Math.PI / 2 + 0.31 +
                        (index / Math.max(1, overflow.length)) * Math.PI * 2;
                    positions[String(node.id)] = {
                        x: center.x + Math.cos(angle) * 164 * sceneScale,
                        y: center.y + Math.sin(angle) * 116 * sceneScale
                    };
                });
            });
            return positions;
        }

        _communityPresetPositions(nodes, bounds = {}, selectedId = null) {
            const metrics = this._communitySceneMetrics(
                bounds,
                Boolean(selectedId && (
                    this._detailCommunityId === String(selectedId) ||
                    this.selectedNode?.length > 0
                ))
            );
            const {
                compact,
                height,
                safeWidth,
                safeHeight,
                topInset,
                sceneScale
            } = metrics;
            const sourceNodes = asArray(nodes).map((node) =>
                typeof node?.data === "function" ? node.data() : node
            ).filter(Boolean);
            const communities = sourceNodes.filter((node) => node.layer === "community")
                .sort((left, right) => {
                    const rankDifference = asNumber(left.rank, Number.MAX_SAFE_INTEGER) -
                        asNumber(right.rank, Number.MAX_SAFE_INTEGER);
                    return rankDifference || String(left.id).localeCompare(String(right.id));
                });
            const hotspots = sourceNodes.filter((node) =>
                node.graph_role === "community-hotspot"
            ).sort((left, right) => {
                const rankDifference = asNumber(left.rank, Number.MAX_SAFE_INTEGER) -
                    asNumber(right.rank, Number.MAX_SAFE_INTEGER);
                return rankDifference || String(left.id).localeCompare(String(right.id));
            });
            const selected = selectedId
                ? communities.find((node) => String(node.id) === String(selectedId))
                : null;
            const center = {
                x: safeWidth * (compact ? 0.5 : 0.477),
                y: height * (compact ? 0.455 : 0.46)
            };
            const positions = {};

            const defaultCenter = communities[Math.min(communities.length - 1, 4)] || null;
            if (compact) {
                const compactAnchor = selected || defaultCenter;
                if (compactAnchor) positions[String(compactAnchor.id)] = center;
                communities.filter((node) => !compactAnchor || node.id !== compactAnchor.id)
                    .forEach((node, index) => {
                        const [xRatio, yRatio] = COMMUNITY_COMPACT_SLOTS[
                            index % COMMUNITY_COMPACT_SLOTS.length
                        ];
                        positions[String(node.id)] = {
                            x: safeWidth * xRatio,
                            y: topInset + safeHeight * yRatio
                        };
                    });
            } else {
                let slotIndex = 0;
                communities.forEach((node) => {
                    if (defaultCenter && node.id === defaultCenter.id) {
                        positions[String(node.id)] = center;
                        return;
                    }
                    const [xRatio, yRatio] = COMMUNITY_CONTEXT_SLOTS[
                        slotIndex % COMMUNITY_CONTEXT_SLOTS.length
                    ];
                    positions[String(node.id)] = {
                        x: safeWidth * xRatio,
                        y: topInset + safeHeight * yRatio
                    };
                    slotIndex += 1;
                });
                if (selected && defaultCenter && selected.id !== defaultCenter.id) {
                    const selectedHome = positions[String(selected.id)];
                    positions[String(selected.id)] = center;
                    positions[String(defaultCenter.id)] = selectedHome;
                }
            }

            const ringPlan = [
                { count: 5, radiusX: 50 * sceneScale, radiusY: 40 * sceneScale, phase: -Math.PI / 2 },
                { count: 8, radiusX: 92 * sceneScale, radiusY: 68 * sceneScale, phase: -Math.PI / 2 + 0.2 },
                { count: 11, radiusX: 146 * sceneScale, radiusY: 106 * sceneScale, phase: -Math.PI / 2 + 0.08 }
            ];
            let hotspotIndex = 0;
            for (const ring of ringPlan) {
                const ringNodes = hotspots.slice(hotspotIndex, hotspotIndex + ring.count);
                ringNodes.forEach((node, index) => {
                    const angle = ring.phase + (index / Math.max(1, ringNodes.length)) * Math.PI * 2;
                    positions[String(node.id)] = {
                        x: center.x + Math.cos(angle) * ring.radiusX,
                        y: center.y + Math.sin(angle) * ring.radiusY
                    };
                });
                hotspotIndex += ringNodes.length;
            }
            return positions;
        }

        _focusPresetPositions(nodes, bounds = {}) {
            const metrics = this._communitySceneMetrics(bounds, true);
            const {
                compact,
                height,
                safeWidth,
                safeHeight,
                topInset,
                sceneScale
            } = metrics;
            const sourceNodes = asArray(nodes).map((node) =>
                typeof node?.data === "function" ? node.data() : node
            ).filter(Boolean);
            const center = {
                x: safeWidth * (compact ? 0.5 : 0.477),
                y: height * (compact ? 0.48 : 0.47)
            };
            const positions = {};
            const core = sourceNodes.find((node) => node.focusSceneRole === "core") ||
                sourceNodes.find((node) => String(node.id) === String(this.selectedNodeId));
            if (core) positions[String(core.id)] = center;

            const inner = sourceNodes
                .filter((node) => node.focusSceneRole === "inner")
                .sort((left, right) =>
                    asNumber(left.focusGroupOrder, Number.MAX_SAFE_INTEGER) -
                        asNumber(right.focusGroupOrder, Number.MAX_SAFE_INTEGER) ||
                    String(left.id).localeCompare(String(right.id))
                );
            const firstRingCount = Math.min(3, inner.length);
            inner.forEach((node, index) => {
                const firstRing = index < firstRingCount;
                const ringIndex = firstRing ? index : index - firstRingCount;
                const ringCount = firstRing
                    ? firstRingCount
                    : Math.max(1, inner.length - firstRingCount);
                const phase = firstRing ? -Math.PI / 2 : -Math.PI / 2 + 0.24;
                const angle = phase + (ringIndex / Math.max(1, ringCount)) * Math.PI * 2;
                const radiusX = (firstRing ? 54 : 112) * sceneScale;
                const radiusY = (firstRing ? 42 : 78) * sceneScale;
                positions[String(node.id)] = {
                    x: center.x + Math.cos(angle) * radiusX,
                    y: center.y + Math.sin(angle) * radiusY
                };
            });

            const groups = new Map();
            sourceNodes.filter((node) => node.focusSceneRole === "context")
                .forEach((node) => {
                    const groupIndex = Math.max(0, asNumber(node.focusGroupIndex, 0));
                    if (!groups.has(groupIndex)) groups.set(groupIndex, []);
                    groups.get(groupIndex).push(node);
                });
            const slots = compact ? FOCUS_COMPACT_SLOTS : FOCUS_CONTEXT_SLOTS;
            Array.from(groups.entries())
                .sort((left, right) => left[0] - right[0])
                .forEach(([groupIndex, groupNodes], index) => {
                    const [xRatio, yRatio] = slots[index % slots.length];
                    const groupCenter = {
                        x: safeWidth * xRatio,
                        y: topInset + safeHeight * yRatio
                    };
                    groupNodes.sort((left, right) =>
                        asNumber(left.focusGroupOrder, Number.MAX_SAFE_INTEGER) -
                            asNumber(right.focusGroupOrder, Number.MAX_SAFE_INTEGER) ||
                        String(left.id).localeCompare(String(right.id))
                    );
                    const anchor = groupNodes[0];
                    if (anchor) positions[String(anchor.id)] = groupCenter;
                    const satellites = groupNodes.slice(1);
                    satellites.forEach((node, satelliteIndex) => {
                        const angle = -Math.PI / 2 +
                            (satelliteIndex / Math.max(1, satellites.length)) * Math.PI * 2;
                        const orbitX = (compact ? 34 : 54) * sceneScale;
                        const orbitY = (compact ? 26 : 40) * sceneScale;
                        positions[String(node.id)] = {
                            x: groupCenter.x + Math.cos(angle) * orbitX,
                            y: groupCenter.y + Math.sin(angle) * orbitY
                        };
                    });
                    groupNodes.forEach((node) => {
                        if (!positions[String(node.id)]) positions[String(node.id)] = groupCenter;
                    });
                });
            return positions;
        }

        _syncOverviewDensity(bounds = {}) {
            if (!this.cy) return;
            const metrics = this._overviewSceneMetrics(
                bounds,
                Boolean(this.selectedNode?.length > 0)
            );
            this.cy.nodes(".overview-node").forEach((node) => {
                node.toggleClass("overview-compact", metrics.compact);
                node.toggleClass(
                    "overview-key-mobile-hidden",
                    metrics.compact &&
                        node.hasClass("overview-key") &&
                        asNumber(node.data("overviewLayerOrder"), 0) > 1
                );
            });
        }

        _syncOverviewPrimaryState() {
            if (!this.cy || this.mode !== "overview") return;
            const selectedLayer = this.selectedNode?.data?.("layer") || null;
            this.cy.nodes(".overview-primary").forEach((node) => {
                node.toggleClass(
                    "overview-primary-muted",
                    Boolean(selectedLayer && selectedLayer !== "model")
                );
            });
        }

        _syncCommunityDensity(mode, bounds = {}) {
            if (!this.cy) return;
            if (mode === "overview") {
                this._syncOverviewDensity(bounds);
                return;
            }
            const metrics = this._communitySceneMetrics(
                bounds,
                Boolean(this.expandedCommunityId)
            );
            const compact = mode === "community" && metrics.compact;
            const communities = [];
            const hotspots = [];
            this.cy.nodes().forEach((node) => {
                if (node.data("layer") === "community") communities.push(node);
                if (node.data("graph_role") === "community-hotspot") hotspots.push(node);
            });
            communities.sort((left, right) =>
                asNumber(left.data("rank"), Number.MAX_SAFE_INTEGER) -
                    asNumber(right.data("rank"), Number.MAX_SAFE_INTEGER) ||
                left.id().localeCompare(right.id())
            );
            const visibleIds = new Set();
            if (compact) {
                const limit = this.expandedCommunityId ? 5 : 6;
                if (this.expandedCommunityId) visibleIds.add(String(this.expandedCommunityId));
                for (const node of communities) {
                    if (visibleIds.size >= limit) break;
                    visibleIds.add(node.id());
                }
            }
            communities.forEach((node) => {
                node.toggleClass("community-compact", compact);
                node.toggleClass(
                    "community-compact-hidden",
                    compact && !visibleIds.has(node.id())
                );
            });
            hotspots.sort((left, right) =>
                asNumber(left.data("rank"), Number.MAX_SAFE_INTEGER) -
                    asNumber(right.data("rank"), Number.MAX_SAFE_INTEGER) ||
                left.id().localeCompare(right.id())
            );
            hotspots.forEach((node, index) => {
                node.toggleClass("community-compact-label-hidden", compact && index >= 6);
            });
        }

        _hasCommunityCellNodes(nodes = null) {
            const sourceNodes = nodes || this.cy?.nodes?.().map((node) => node.data()) || [];
            if (sourceNodes.length === 0) return true;
            return sourceNodes.some((node) => {
                const data = typeof node?.data === "function" ? node.data() : node;
                return data?.layer === "community";
            });
        }

        _getLayoutOptions(mode) {
            const animate = !this.reducedMotion;
            const bounds = this.container && typeof this.container.getBoundingClientRect === "function"
                ? this.container.getBoundingClientRect()
                : null;
            const compact = Boolean(bounds && bounds.width < 640);
            if (mode === "overview") {
                const nodes = this.cy?.nodes?.().map((node) => node.data()) ||
                    this.currentGraph?.nodes || [];
                const positions = this._overviewPresetPositions(nodes, bounds || {});
                return {
                    name: "preset",
                    positions: (node) => positions[node.id()] || {
                        x: Math.max(1, asNumber(bounds?.width, 1180)) / 2,
                        y: Math.max(1, asNumber(bounds?.height, 720)) / 2
                    },
                    fit: false,
                    zoom: 1,
                    pan: { x: 0, y: 0 },
                    animate: false,
                    animationDuration: 0
                };
            }
            if (mode === "community") {
                const nodes = this.cy?.nodes?.().map((node) => node.data()) || [];
                if (!this._hasCommunityCellNodes(nodes)) {
                    return {
                        name: "concentric",
                        fit: true,
                        padding: compact ? 68 : 42,
                        animate: false,
                        animationDuration: 0,
                        minNodeSpacing: compact ? 42 : 58,
                        levelWidth: () => 2,
                        concentric: (node) => {
                            const rank = asNumber(node.data("rank"), 0);
                            return rank > 0 ? 100 / rank : asNumber(node.degree(), 1);
                        }
                    };
                }
                const positions = this._communityPresetPositions(
                    nodes,
                    bounds || {},
                    this.expandedCommunityId
                );
                return {
                    name: "preset",
                    positions: (node) => positions[node.id()] || {
                        x: Math.max(1, asNumber(bounds?.width, 960)) / 2,
                        y: Math.max(1, asNumber(bounds?.height, 720)) / 2
                    },
                    fit: false,
                    zoom: 1,
                    pan: { x: 0, y: 0 },
                    animate: false,
                    animationDuration: 0
                };
            }
            if (mode === "focus") {
                const nodes = this.cy?.nodes?.().map((node) => node.data()) || [];
                const positions = this._focusPresetPositions(nodes, bounds || {});
                return {
                    name: "preset",
                    positions: (node) => positions[node.id()] || {
                        x: Math.max(1, asNumber(bounds?.width, 960)) / 2,
                        y: Math.max(1, asNumber(bounds?.height, 720)) / 2
                    },
                    fit: false,
                    zoom: 1,
                    pan: { x: 0, y: 0 },
                    animate: false,
                    animationDuration: 0
                };
            }
            return {
                name: "concentric",
                fit: true,
                padding: compact ? 72 : 44,
                animate: false,
                animationDuration: 0,
                minNodeSpacing: 54,
                levelWidth: () => 1,
                concentric: (node) => {
                    if (node.id() === this.selectedNodeId) return 1000;
                    const rank = asNumber(node.data("rank"), 0);
                    return rank > 0 ? 100 / rank : asNumber(node.degree(), 1);
                }
            };
        }

        _shouldDeferLabel(node) {
            if (node?.graph_role === "community-hotspot") return false;
            if (node?.layer !== "tag" && node?.layer !== "concept") return false;
            const rank = asNumber(node.rank, 0) > 0
                ? asNumber(node.rank)
                : asNumber(node.label_rank, 0);
            const rankLimit = Math.max(1, asNumber(
                this.options?.labelRankLimit,
                DEFAULT_LABEL_RANK_LIMIT
            ));
            return rank <= 0 || rank > rankLimit;
        }

        _labelsShouldBeExpanded() {
            return Boolean(this.cy && asNumber(this.cy.zoom(), 0) >= LABEL_EXPAND_ZOOM);
        }

        _updateSemanticLabels(force = false) {
            if (!this.cy || this.isDestroyed) return;
            const expanded = this._labelsShouldBeExpanded();
            if (!force && expanded === this._labelsExpanded) return;
            this._labelsExpanded = expanded;
            const deferred = this.cy.nodes(".deferred-label");
            deferred.toggleClass("label-visible", expanded);
            if (this.selectedNode?.length > 0) this.selectedNode.addClass("label-visible");
            if (this.hoveredNode?.length > 0) this.hoveredNode.addClass("label-visible");
        }

        _runLayout(mode) {
            if (!this.cy || this.isDestroyed) return;
            this.cy.stop?.();
            this._activeLayout?.stop?.();
            this._layoutFallback = null;
            const bounds = this.container?.getBoundingClientRect?.() || {};
            this._syncCommunityDensity(mode, bounds);
            const semanticPreset = mode === "overview" || mode === "focus" ||
                (mode === "community" && this._hasCommunityCellNodes());
            if (semanticPreset) {
                this.cy.zoom(1);
                this.cy.pan({ x: 0, y: 0 });
            }
            let options = this._getLayoutOptions(mode);
            try {
                this._activeLayout = this.cy.layout(options);
                this._trackLayoutLifecycle(this._activeLayout);
                this._bindCommunityFieldDraw(this._activeLayout, mode, semanticPreset);
                this._activeLayout.run();
            } catch (error) {
                if (mode !== "community") throw error;
                this._layoutFallback = "grid";
                options = {
                    name: "grid",
                    fit: true,
                    padding: this.container.getBoundingClientRect().width < 640 ? 68 : 42,
                    animate: !this.reducedMotion,
                    animationDuration: this.reducedMotion ? 0 : 420
                };
                this._activeLayout = this.cy.layout(options);
                this._trackLayoutLifecycle(this._activeLayout);
                this._bindCommunityFieldDraw(this._activeLayout, mode, false);
                this._activeLayout.run();
            }
        }

        _trackLayoutLifecycle(layout) {
            this._layoutRunning = Boolean(layout);
            if (!layout) return;
            const finish = () => {
                if (this._activeLayout === layout) this._layoutRunning = false;
            };
            if (typeof layout.one === "function") {
                layout.one("layoutstop", finish);
                return;
            }
            if (typeof layout.on === "function") {
                const once = () => {
                    layout.off?.("layoutstop", once);
                    finish();
                };
                layout.on("layoutstop", once);
                return;
            }
            this._layoutRunning = false;
        }

        _bindCommunityFieldDraw(layout, mode, lockViewport = false) {
            if (!layout || !["overview", "community", "focus"].includes(mode)) return;
            const finish = () => {
                if (this.isDestroyed || this._paused || this.mode !== mode) return;
                if (lockViewport) {
                    this.cy?.zoom?.(1);
                    this.cy?.pan?.({ x: 0, y: 0 });
                }
                this._scheduleCommunityFieldDraw();
                this._emitViewportChange("layout-density");
            };
            if (typeof layout.one === "function") {
                layout.one("layoutstop", finish);
            } else if (typeof layout.on === "function") {
                const once = () => {
                    layout.off?.("layoutstop", once);
                    finish();
                };
                layout.on("layoutstop", once);
            }
        }

        _replaceGraph(graphPayload, mode, options = {}) {
            if (!this.cy || this.isDestroyed) return;
            this._stopCommunityFieldLoop(!["overview", "community", "focus"].includes(mode));
            const graph = normalizeGraph(graphPayload);
            this.currentGraph = graph;
            this.data = {
                ...this.data,
                nodes: graph.nodes,
                links: graph.links,
                layers: { ...(this.data.layers || {}), ...(graph.layers || {}) },
                stats: { ...(this.data.stats || {}), ...(graph.stats || {}) }
            };
            if (!options.keepVisibility) {
                graph.nodes.forEach((node) => {
                    if (node.layer) this.visibleLayers.add(node.layer);
                });
            }

            this.selectedNode = null;
            this.hoveredNode = null;
            this._labelsExpanded = null;
            this._particles = [];
            this._stopParticleLoop(true);
            const elements = this._formatElements(graph);
            this.cy.batch(() => {
                this.cy.elements().remove();
                this.cy.add([...elements.nodes, ...elements.edges]);
            });
            this._applyLayerVisibility();
            this._updateSemanticLabels(true);
            this._runLayout(mode);
            this._scheduleCommunityFieldDraw();
        }

        _bindCytoscapeEvents() {
            this.cy.on("tap", "node", (event) => {
                const selected = this._selectNode(event.target);
                if (
                    selected?.layer === "community" &&
                    this.mode === "community" &&
                    selected.id !== this.expandedCommunityId
                ) {
                    this.expandCommunity(selected.id).catch((error) => {
                        if (error?.name !== "AbortError") this._emitError("community", error);
                    });
                } else if (selected?.layer === "community" && this.mode === "community") {
                    this._reserveExpandedCommunityDetail(selected.id);
                }
            });
            this.cy.on("mouseover", "node", (event) => {
                this.hoveredNode = event.target;
                event.target.addClass("is-hovered");
                event.target.addClass("label-visible");
                if (!this.selectedNode) this._highlightNode(event.target);
                this._emit("nodeHover", this._getNodeData(event.target));
            });
            this.cy.on("mouseout", "node", () => {
                if (this.hoveredNode && this.hoveredNode !== this.selectedNode) {
                    this.hoveredNode.removeClass("is-hovered");
                    this.hoveredNode.toggleClass("label-visible", this._labelsShouldBeExpanded());
                }
                this.hoveredNode = null;
                if (this.selectedNode) this._highlightNode(this.selectedNode);
                else this._clearHighlights();
                this._emit("nodeHover", null);
            });
            this.cy.on("tap", (event) => {
                if (event.target === this.cy) this.clearSelection();
            });
            this.cy.on("zoom", () => {
                this._updateSemanticLabels();
                this._scheduleCommunityFieldDraw();
                this._emitViewportChange("zoom");
            });
            this.cy.on("pan", () => this._scheduleCommunityFieldDraw());
            this.cy.on("position", "node", () => this._scheduleCommunityFieldDraw());
            this.cy.on("resize", () => this._resizeOverlay());
        }

        _reserveExpandedCommunityDetail(nodeId) {
            const wantedId = String(nodeId || "");
            if (
                !wantedId ||
                this.mode !== "community" ||
                wantedId !== this.expandedCommunityId ||
                this._detailCommunityId === wantedId
            ) {
                return false;
            }
            this._detailCommunityId = wantedId;
            this._runLayout("community");
            return true;
        }

        _selectNode(node, options = {}) {
            if (!node || node.length === 0) return null;
            this.cy.elements().unselect();
            this.cy.nodes().removeClass("focus-root");
            node.select();
            this.selectedNode = node;
            this.selectedNodeId = node.id();
            if (options.focusRoot) node.addClass("focus-root");
            this._syncOverviewPrimaryState();
            this._updateSemanticLabels(true);
            this._highlightNode(node);
            this._scheduleCommunityFieldDraw();
            const data = this._getNodeData(node);
            this._emit("graph:selectionchange", { node: data, nodeId: data.id });
            this._emit("nodeSelect", data);
            if (this.mode === "overview") this._runLayout("overview");
            return data;
        }

        _highlightNode(node) {
            if (!this.cy || !node || node.length === 0) return;
            const neighborhood = node.neighborhood().add(node);
            this.cy.elements().removeClass("highlighted faded community-route");
            if (node.data("layer") === "community" && this.mode === "community") {
                // Community mode is a scene, not a generic neighborhood filter. Keep every
                // context field legible and reserve emphasis for the selected community's
                // real member links and inter-community routes.
                node.connectedEdges().forEach((edge) => {
                    if (edge.data("type") === "community") edge.addClass("community-route");
                    if (edge.data("type") === "community-member") edge.addClass("highlighted");
                });
                this._syncParticles();
                this._scheduleCommunityFieldDraw();
                return;
            }
            if (this.mode === "focus" && node.data("focusSceneRole") === "core") {
                // The field canvas carries one semantic route per outer cell. Highlighting
                // every raw incident edge here would recreate the old long-spoke fan.
                node.connectedEdges().forEach((edge) => {
                    if (edge.hasClass("focus-inner-link")) edge.addClass("highlighted");
                });
                this._syncParticles();
                this._scheduleCommunityFieldDraw();
                return;
            }
            this.cy.elements().not(neighborhood).addClass("faded");
            node.connectedEdges().addClass("highlighted").removeClass("faded");
            neighborhood.removeClass("faded");
            this._syncParticles();
            this._scheduleCommunityFieldDraw();
        }

        _clearHighlights() {
            if (!this.cy) return;
            this.cy.elements().removeClass("highlighted faded community-route");
            this._syncParticles();
            this._scheduleCommunityFieldDraw();
        }

        _getNodeData(node) {
            const data = node?.data?.() || {};
            return {
                ...data,
                id: data.id,
                name: data.name || data.label || data.id,
                layer: data.layer,
                layerName: data.layer_name || data.layerName || data.layer,
                article_count: asNumber(data.article_count, 0),
                articles: asNumber(data.article_count ?? data.articles, 0),
                degree: asNumber(data.degree ?? data.connections, 0),
                connections: asNumber(data.degree ?? data.connections, 0),
                weighted_degree: asNumber(data.weighted_degree, 0),
                rank: asNumber(data.rank, 0),
                community: data.community ?? data.community_id ?? null,
                community_id: data.community_id ?? data.community ?? null,
                node_count: asNumber(data.node_count ?? data.member_count, 0),
                member_ids: asArray(data.member_ids),
                graph_role: data.graph_role || null
            };
        }

        getCommunityInsights(nodeId) {
            const wantedId = String(nodeId || "");
            const graph = normalizeGraph(this.currentGraph || {});
            const community = graph.nodes.find((node) =>
                node.id === wantedId && node.layer === "community"
            );
            if (!community) {
                return {
                    memberCount: 0,
                    visibleMembers: 0,
                    connectionStrength: 0,
                    topMembers: [],
                    relatedCommunities: []
                };
            }

            const memberIds = new Set(asArray(community.member_ids).map(String));
            const memberLinks = graph.links.filter((link) =>
                link.type === "community-member" &&
                (link.source === wantedId || link.target === wantedId)
            );
            memberLinks.forEach((link) => {
                memberIds.add(link.source === wantedId ? link.target : link.source);
            });
            const visibleMembers = graph.nodes
                .filter((node) => node.id !== wantedId && (
                    node.graph_role === "community-hotspot" ||
                    node.community_id === wantedId ||
                    memberIds.has(node.id)
                ))
                .sort((left, right) =>
                    asNumber(right.weighted_degree ?? right.degree, 0) -
                        asNumber(left.weighted_degree ?? left.degree, 0) ||
                    asNumber(left.rank, Number.MAX_SAFE_INTEGER) -
                        asNumber(right.rank, Number.MAX_SAFE_INTEGER) ||
                    left.name.localeCompare(right.name)
                );
            let topMembers = visibleMembers.slice(0, 6).map((node) => ({
                id: node.id,
                name: node.name,
                degree: asNumber(node.degree, 0),
                weightedDegree: asNumber(node.weighted_degree, 0),
                articleCount: asNumber(node.article_count, 0)
            }));
            if (topMembers.length === 0) {
                topMembers = asArray(community.member_ids).slice(0, 6).map((memberId) => ({
                    id: String(memberId),
                    name: String(memberId).replace(/^[^:]+:/, ""),
                    degree: 0,
                    weightedDegree: 0,
                    articleCount: 0
                }));
            }

            const nodeById = new Map(graph.nodes.map((node) => [node.id, node]));
            const relatedCommunities = graph.links
                .filter((link) => link.type === "community" &&
                    (link.source === wantedId || link.target === wantedId))
                .map((link) => {
                    const relatedId = link.source === wantedId ? link.target : link.source;
                    const related = nodeById.get(relatedId);
                    return related?.layer === "community" ? {
                        id: relatedId,
                        name: related.name,
                        weight: asNumber(link.weight ?? link.strength, 0)
                    } : null;
                })
                .filter(Boolean)
                .sort((left, right) => right.weight - left.weight || left.name.localeCompare(right.name))
                .slice(0, 6);
            return {
                memberCount: Math.max(
                    asNumber(community.node_count ?? community.degree, 0),
                    asArray(community.member_ids).length,
                    visibleMembers.length
                ),
                visibleMembers: visibleMembers.length,
                connectionStrength: relatedCommunities.reduce((sum, item) => sum + item.weight, 0),
                topMembers,
                relatedCommunities
            };
        }

        _defaultCommunityAnchorId(graphPayload) {
            const communities = normalizeGraph(graphPayload).nodes
                .filter((node) => node.layer === "community" && node.id !== "community:other")
                .sort((left, right) =>
                    asNumber(left.rank, Number.MAX_SAFE_INTEGER) -
                        asNumber(right.rank, Number.MAX_SAFE_INTEGER) ||
                    String(left.id).localeCompare(String(right.id))
                );
            if (communities.length === 0) return "";
            return communities[communities.length >= 5 ? 4 : 0].id;
        }

        _queueDefaultCommunityExpansion(communityId, requestSequence) {
            const task = this._loadDefaultCommunityExpansion(communityId, requestSequence);
            this._defaultCommunityExpansion = task;
            task.finally(() => {
                if (this._defaultCommunityExpansion === task) {
                    this._defaultCommunityExpansion = null;
                }
            });
            return task;
        }

        async _loadDefaultCommunityExpansion(communityId, requestSequence) {
            try {
                const expansion = await this._request("focus", {
                    nodeId: communityId,
                    nodeLimit: 24,
                    edgeLimit: 80
                }, { operationKey: "view" });
                if (
                    requestSequence !== this._modeSequence ||
                    this.isDestroyed ||
                    this.mode !== "community" ||
                    expansion.node?.layer !== "community"
                ) {
                    return false;
                }
                this._detailCommunityId = null;
                this.expandedCommunityId = expansion.node.id || communityId;
                this.selectedNodeId = this.expandedCommunityId;
                this.communityGraph = normalizeGraph(expansion.graph);
                this._replaceGraph(expansion.graph, "community");
                this._emit("graph:modechange", {
                    ...this._modeDetail("community"),
                    progressive: true,
                    phase: "detail"
                });
                return true;
            } catch (error) {
                // A stale request is expected when the user switches mode or selects another
                // community while the default shard is still in flight. Summary cells remain.
                if (error?.name === "AbortError") return false;
                return false;
            }
        }

        async setMode(mode, options = {}) {
            await this.ready;
            if (this.isDestroyed) throw createAbortError();
            const nextMode = String(mode || "").toLowerCase();
            if (!MODES.has(nextMode)) {
                const error = new Error(`Unsupported graph mode: ${mode}`);
                this._emitError("modechange", error);
                throw error;
            }
            if (nextMode === "focus") {
                const nodeId = this._resolveFocusTargetId(options.nodeId || this.selectedNodeId);
                if (!nodeId) {
                    const error = new Error("No graph node is available for focus mode");
                    this._emitError("focus", error);
                    throw error;
                }
                return this.focusNode(nodeId);
            }

            this.clearSelection({ reflow: false });

            const requestSequence = ++this._modeSequence;
            const previousMode = this.mode;
            try {
                let graph;
                if (nextMode === "overview") {
                    this._cancelOperation("view");
                    graph = this.coreGraph;
                } else if (this.worker) {
                    const response = await this._request("community", { limit: 24 }, {
                        operationKey: "view",
                        cancelPrevious: true
                    });
                    graph = response.graph;
                } else {
                    graph = this._buildLegacyCommunityGraph();
                }
                if (requestSequence !== this._modeSequence || this.isDestroyed) return this.mode;

                this.mode = nextMode;
                this.layoutMode = nextMode;
                this._detailCommunityId = null;
                this.selectedNodeId = null;
                this.expandedCommunityId = null;
                if (nextMode === "community") this.communityGraph = normalizeGraph(graph);
                this._replaceGraph(graph, nextMode);
                this._emit("graph:modechange", this._modeDetail(previousMode));
                if (nextMode === "community" && this.worker) {
                    const defaultCommunityId = this._defaultCommunityAnchorId(graph);
                    if (defaultCommunityId) {
                        this._queueDefaultCommunityExpansion(
                            defaultCommunityId,
                            requestSequence
                        );
                    }
                }
                return this.mode;
            } catch (error) {
                if (error?.name === "AbortError") return this.mode;
                this._emitError("modechange", error);
                throw error;
            }
        }

        _resolveFocusTargetId(nodeId) {
            const currentNodes = asArray(this.currentGraph?.nodes);
            const coreNodes = asArray(this.coreGraph?.nodes);
            const requestedId = String(nodeId || "");
            const requestedNode = requestedId
                ? currentNodes.find((node) => node.id === requestedId) ||
                    coreNodes.find((node) => node.id === requestedId)
                : null;

            if (requestedNode?.layer === "community") {
                const memberIds = new Set(asArray(requestedNode.member_ids).map(String));
                asArray(this.currentGraph?.links).forEach((link) => {
                    if (link.type !== "community-member") return;
                    if (link.source === requestedId) memberIds.add(String(link.target));
                    if (link.target === requestedId) memberIds.add(String(link.source));
                });
                const members = currentNodes
                    .filter((node) => node.layer !== "community" && (
                        node.community_id === requestedId || memberIds.has(node.id)
                    ))
                    .sort((left, right) =>
                        asNumber(right.weighted_degree, 0) - asNumber(left.weighted_degree, 0) ||
                        asNumber(right.degree, 0) - asNumber(left.degree, 0) ||
                        asNumber(left.rank, Number.MAX_SAFE_INTEGER) -
                            asNumber(right.rank, Number.MAX_SAFE_INTEGER) ||
                        String(left.name || left.id).localeCompare(String(right.name || right.id))
                    );
                if (members[0]?.id) return members[0].id;
                const listedMember = asArray(requestedNode.member_ids).find(Boolean);
                if (listedMember) return String(listedMember);
            }

            if (requestedId && requestedNode?.layer !== "community") return requestedId;
            const candidates = (coreNodes.length > 0 ? coreNodes : currentNodes)
                .filter((node) => node.layer !== "community" && node.id)
                .sort((left, right) => {
                    const leftRank = asNumber(left.rank, 0) > 0
                        ? asNumber(left.rank)
                        : Number.MAX_SAFE_INTEGER;
                    const rightRank = asNumber(right.rank, 0) > 0
                        ? asNumber(right.rank)
                        : Number.MAX_SAFE_INTEGER;
                    return leftRank - rightRank ||
                        asNumber(right.weighted_degree, 0) - asNumber(left.weighted_degree, 0) ||
                        asNumber(right.degree, 0) - asNumber(left.degree, 0) ||
                        String(left.name || left.id).localeCompare(String(right.name || right.id));
                });
            return candidates[0]?.id || "";
        }

        async focusNode(nodeId) {
            await this.ready;
            if (this.isDestroyed) throw createAbortError();
            const wantedId = String(nodeId || "");
            if (!wantedId) throw new Error("focusNode requires a node id");
            const requestSequence = ++this._modeSequence;
            const previousMode = this.mode;
            try {
                let response;
                if (this.worker) {
                    response = await this._request("focus", {
                        nodeId: wantedId,
                        nodeLimit: 24,
                        edgeLimit: 80
                    }, { operationKey: "view", cancelPrevious: true });
                } else {
                    response = this._buildLegacyFocusGraph(wantedId);
                }
                if (requestSequence !== this._modeSequence || this.isDestroyed) return null;

                if (response.node?.layer === "community") {
                    return this._applyCommunityExpansion(response, previousMode);
                }

                this.mode = "focus";
                this.layoutMode = "focus";
                this._detailCommunityId = null;
                this.expandedCommunityId = null;
                this.selectedNodeId = response.node?.id || wantedId;
                this._replaceGraph(response.graph, "focus");
                const node = this.cy.getElementById(this.selectedNodeId);
                const selected = node && node.length > 0
                    ? this._selectNode(node, { focusRoot: true })
                    : null;
                this._emit("graph:modechange", this._modeDetail(previousMode));
                if (node && node.length > 0) {
                    this.cy.animate({ pan: { x: 0, y: 0 }, zoom: 1 }, {
                        duration: this.reducedMotion ? 0 : 450,
                        easing: "ease-out-cubic"
                    });
                }
                return selected;
            } catch (error) {
                if (error?.name === "AbortError") return null;
                this._emitError("focus", error);
                throw error;
            }
        }

        async expandCommunity(nodeId) {
            await this.ready;
            if (this.isDestroyed) throw createAbortError();
            const wantedId = String(nodeId || "");
            if (!wantedId) throw new Error("expandCommunity requires a community id");
            const requestSequence = ++this._modeSequence;
            const previousMode = this.mode;
            try {
                let response;
                if (this.worker) {
                    response = await this._request("focus", {
                        nodeId: wantedId,
                        nodeLimit: 24,
                        edgeLimit: 80
                    }, { operationKey: "view", cancelPrevious: true });
                } else {
                    response = this._buildLegacyFocusGraph(wantedId);
                }
                if (requestSequence !== this._modeSequence || this.isDestroyed) return null;
                if (response.node?.layer !== "community") {
                    throw new Error(`${wantedId} is not a community node`);
                }
                return this._applyCommunityExpansion(response, previousMode);
            } catch (error) {
                if (error?.name === "AbortError") return null;
                this._emitError("community", error);
                throw error;
            }
        }

        _applyCommunityExpansion(response, previousMode) {
            this.mode = "community";
            this.layoutMode = "community";
            this.expandedCommunityId = response.node?.id || null;
            this._detailCommunityId = this.expandedCommunityId;
            this.selectedNodeId = this.expandedCommunityId;
            this._replaceGraph(response.graph, "community");
            const node = this.cy.getElementById(this.expandedCommunityId);
            const selected = node && node.length > 0
                ? this._selectNode(node, { focusRoot: true })
                : null;
            this._emit("graph:modechange", this._modeDetail(previousMode));
            this._scheduleCommunityFieldDraw();
            return selected;
        }

        _modeDetail(previousMode) {
            const visible = this.getVisibleCounts();
            return {
                mode: this.mode,
                previousMode,
                visibleNodes: visible.nodes,
                visibleEdges: visible.edges,
                layoutFallback: this._layoutFallback,
                expandedCommunityId: this.expandedCommunityId
            };
        }

        _emitViewportChange(reason = "viewport") {
            const detail = {
                reason,
                zoom: asNumber(this.cy?.zoom?.(), 1)
            };
            if (reason !== "zoom") {
                const visible = this.getVisibleCounts();
                detail.visibleNodes = visible.nodes;
                detail.visibleEdges = visible.edges;
            }
            this._emit("graph:viewportchange", detail);
            return detail;
        }

        getVisibleCounts() {
            if (!this.cy) {
                return {
                    nodes: this.currentGraph?.nodes?.length || 0,
                    edges: this.currentGraph?.links?.length || 0
                };
            }
            const hiddenNode = (node) =>
                node.hasClass?.("layer-hidden") || node.hasClass?.("community-compact-hidden");
            let nodes = 0;
            const nodeCollection = this.cy.nodes?.();
            if (typeof nodeCollection?.forEach === "function") {
                nodeCollection.forEach((node) => {
                    if (!hiddenNode(node)) nodes += 1;
                });
            } else {
                nodes = asNumber(nodeCollection?.length, 0);
            }
            let edges = 0;
            const edgeCollection = this.cy.edges?.();
            if (typeof edgeCollection?.forEach === "function") {
                edgeCollection.forEach((edge) => {
                    if (
                        !edge.hasClass?.("layer-hidden") &&
                        !hiddenNode(edge.source()) &&
                        !hiddenNode(edge.target())
                    ) {
                        edges += 1;
                    }
                });
            } else {
                edges = asNumber(edgeCollection?.length, 0);
            }
            return { nodes, edges };
        }

        _buildLegacyCommunityGraph() {
            const nodes = [...this.currentGraph.nodes]
                .sort((left, right) => {
                    const rightRank = asNumber(right.rank, 0) > 0 ? asNumber(right.rank) : Number.POSITIVE_INFINITY;
                    const leftRank = asNumber(left.rank, 0) > 0 ? asNumber(left.rank) : Number.POSITIVE_INFINITY;
                    if (leftRank !== rightRank) return leftRank - rightRank;
                    const rightScore = asNumber(right.weighted_degree) || asNumber(right.degree);
                    const leftScore = asNumber(left.weighted_degree) || asNumber(left.degree);
                    return rightScore - leftScore;
                })
                .slice(0, 24);
            const ids = new Set(nodes.map((node) => node.id));
            const links = this.currentGraph.links
                .filter((link) => ids.has(link.source) && ids.has(link.target))
                .slice(0, 80);
            return { nodes, links, layers: this.currentGraph.layers, stats: this.currentGraph.stats };
        }

        _buildLegacyFocusGraph(nodeId) {
            const selected = this.currentGraph.nodes.find((node) =>
                node.id === nodeId || node.legacy_id === nodeId
            );
            if (!selected) throw new Error(`Node not found: ${nodeId}`);
            const incident = this.currentGraph.links.filter((link) =>
                link.source === selected.id || link.target === selected.id
            );
            const neighborIds = [];
            for (const link of incident) {
                const id = link.source === selected.id ? link.target : link.source;
                if (!neighborIds.includes(id)) neighborIds.push(id);
                if (neighborIds.length >= 24) break;
            }
            const ids = new Set([selected.id, ...neighborIds]);
            return {
                node: selected,
                graph: {
                    nodes: this.currentGraph.nodes.filter((node) => ids.has(node.id)),
                    links: this.currentGraph.links
                        .filter((link) => ids.has(link.source) && ids.has(link.target))
                        .slice(0, 80),
                    layers: this.currentGraph.layers,
                    stats: this.currentGraph.stats
                }
            };
        }

        clearSelection(options = {}) {
            if (!this.cy || this.isDestroyed) return;
            const shouldReflowCommunity = options.reflow !== false &&
                this.mode === "community" &&
                Boolean(this._detailCommunityId);
            const shouldReflowOverview = options.reflow !== false &&
                this.mode === "overview" &&
                Boolean(this.selectedNode?.length > 0);
            this._modeSequence += 1;
            this._cancelOperation("view");
            this.cy.elements().unselect();
            this.cy.nodes().removeClass("focus-root search-match");
            this.selectedNode = null;
            this.selectedNodeId = null;
            this._detailCommunityId = null;
            this.hoveredNode = null;
            this._syncOverviewPrimaryState();
            this._updateSemanticLabels(true);
            this._clearHighlights();
            this._emit("graph:selectionchange", { node: null, nodeId: null });
            this._emit("nodeSelect", null);
            if (shouldReflowCommunity) this._runLayout("community");
            if (shouldReflowOverview) this._runLayout("overview");
        }

        async search(query) {
            await this.ready;
            const searchSequence = ++this._searchSequence;
            const value = String(query || "").trim();
            if (!value) {
                this._cancelOperation("search");
                this._applySearchMatches([]);
                return [];
            }
            try {
                let items;
                if (this.worker) {
                    const response = await this._request("search", { query: value, limit: 10 }, {
                        operationKey: "search",
                        cancelPrevious: true
                    });
                    items = asArray(response.items).slice(0, 10);
                } else {
                    const folded = value.toLocaleLowerCase();
                    items = this.currentGraph.nodes
                        .filter((node) => [node.name, node.description, node.layer_name]
                            .filter(Boolean).join(" ").toLocaleLowerCase().includes(folded))
                        .slice(0, 10);
                }
                if (searchSequence !== this._searchSequence || this.isDestroyed) return [];
                this._applySearchMatches(items);
                return items;
            } catch (error) {
                if (error?.name === "AbortError") return [];
                this._emitError("search", error);
                throw error;
            }
        }

        _applySearchMatches(items) {
            if (!this.cy) return;
            const ids = new Set(asArray(items).map((item) => String(item.id)));
            this.cy.nodes(".search-match").forEach((node) => {
                node.removeClass("search-match");
                if (String(node.id()) !== String(this.selectedNodeId || "")) {
                    node.toggleClass(
                        "label-visible",
                        node.hasClass("deferred-label") && this._labelsShouldBeExpanded()
                    );
                }
            });
            if (ids.size === 0) return;
            this.cy.nodes().forEach((node) => {
                if (ids.has(node.id())) node.addClass("search-match label-visible");
            });
        }

        async toggleLayer(layer) {
            await this.ready;
            const layerId = String(layer || "");
            if (!layerId) return false;
            if (this.visibleLayers.has(layerId)) this.visibleLayers.delete(layerId);
            else this.visibleLayers.add(layerId);
            const isVisible = this.visibleLayers.has(layerId);
            if (
                !isVisible &&
                String(this.selectedNode?.data?.("layer") || "") === layerId
            ) {
                this.clearSelection({ reflow: false });
            }
            this._applyLayerVisibility();
            const visible = this.getVisibleCounts();
            this._emit("graph:layerchange", {
                layer: layerId,
                visible: isVisible,
                visibleLayers: Array.from(this.visibleLayers),
                visibleNodes: visible.nodes,
                visibleEdges: visible.edges
            });
            return isVisible;
        }

        _applyLayerVisibility() {
            if (!this.cy) return;
            this.cy.batch(() => {
                this.cy.nodes().forEach((node) => {
                    node.toggleClass("layer-hidden", !this.visibleLayers.has(node.data("layer")));
                });
                this.cy.edges().forEach((edge) => {
                    const visible = this.visibleLayers.has(edge.source().data("layer")) &&
                        this.visibleLayers.has(edge.target().data("layer"));
                    edge.toggleClass("layer-hidden", !visible);
                });
            });
            this._syncParticles();
            this._scheduleCommunityFieldDraw();
        }

        filterByLayer(layer) {
            return this.toggleLayer(layer);
        }

        addGraphData(partial) {
            if (!this.cy || this.isDestroyed) return;
            const merged = mergeGraphs(this.currentGraph, partial);
            this.coreGraph = mergeGraphs(this.coreGraph, partial);
            this._replaceGraph(merged, this.mode, { keepVisibility: true });
        }

        getCommunityVisualState() {
            return {
                fieldCount: this._communityFields.length,
                expandedCommunityId: this.expandedCommunityId,
                paintCount: this._fieldPaintCount,
                animationFrame: this._fieldFrame,
                reducedMotion: this.reducedMotion
            };
        }

        _initCommunityField() {
            if (this._fieldCanvas || !global.document) return;
            const canvas = global.document.createElement("canvas");
            canvas.className = "graph-field-overlay";
            canvas.setAttribute("aria-hidden", "true");
            canvas.style.position = "absolute";
            canvas.style.inset = "0";
            canvas.style.width = "100%";
            canvas.style.height = "100%";
            canvas.style.pointerEvents = "none";
            canvas.style.zIndex = "0";
            this.container.appendChild(canvas);
            this._fieldCanvas = canvas;
            this._fieldContext = canvas.getContext("2d");
        }

        _resizeCommunityField(width, height, pixelRatio) {
            if (!this._fieldCanvas || !this._fieldContext) return;
            this._fieldWidth = width;
            this._fieldHeight = height;
            this._fieldCanvas.style.width = `${width}px`;
            this._fieldCanvas.style.height = `${height}px`;
            const targetWidth = Math.round(width * pixelRatio);
            const targetHeight = Math.round(height * pixelRatio);
            if (this._fieldCanvas.width !== targetWidth) this._fieldCanvas.width = targetWidth;
            if (this._fieldCanvas.height !== targetHeight) this._fieldCanvas.height = targetHeight;
            this._fieldContext.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
        }

        _fieldDescriptors() {
            if (this.mode === "overview") return this._overviewFieldDescriptors();
            if (this.mode === "focus") return this._focusFieldDescriptors();
            return this._communityFieldDescriptors();
        }

        _overviewFieldDescriptors() {
            if (!this.cy || this.mode !== "overview") return [];
            const groups = new Map();
            this.cy.nodes(":visible").forEach((node) => {
                if (!node.data("overviewSceneRole")) return;
                const layer = String(node.data("layer") || "unknown");
                if (!groups.has(layer)) groups.set(layer, []);
                groups.get(layer).push(node);
            });
            const selectedLayer = this.selectedNode?.data?.("layer") || null;
            const metrics = this._overviewSceneMetrics(
                { width: this._fieldWidth, height: this._fieldHeight },
                Boolean(this.selectedNode?.length > 0)
            );
            const zoom = Math.max(0.05, asNumber(this.cy.zoom?.(), 1));
            const renderScale = metrics.sceneScale * zoom;
            const descriptors = [];
            Array.from(groups.entries())
                .sort((left, right) =>
                    asNumber(left[1][0]?.data("overviewLayerIndex"), Number.MAX_SAFE_INTEGER) -
                        asNumber(right[1][0]?.data("overviewLayerIndex"), Number.MAX_SAFE_INTEGER) ||
                    left[0].localeCompare(right[0])
                )
                .forEach(([layer, nodes]) => {
                    const anchorNode = nodes.find((node) =>
                        node.data("overviewSceneRole") === "anchor"
                    ) || nodes[0];
                    if (!anchorNode) return;
                    const anchorPosition = anchorNode.renderedPosition();
                    if (
                        anchorPosition.x < 0 || anchorPosition.x > this._fieldWidth ||
                        anchorPosition.y < 0 || anchorPosition.y > this._fieldHeight
                    ) {
                        return;
                    }
                    let memberRadius = 0;
                    nodes.forEach((node) => {
                        const position = node.renderedPosition();
                        memberRadius = Math.max(
                            memberRadius,
                            Math.hypot(position.x - anchorPosition.x, position.y - anchorPosition.y)
                        );
                    });
                    const isActive = selectedLayer
                        ? layer === selectedLayer
                        : layer === "model";
                    const availableOuterRadius = Math.min(
                        anchorPosition.x / 1.1,
                        (this._fieldWidth - anchorPosition.x) / 1.1,
                        anchorPosition.y / 0.91,
                        (this._fieldHeight - anchorPosition.y) / 0.91
                    ) - 4;
                    if (availableOuterRadius <= 8) return;
                    const naturalRadius = Math.max(
                        34 * renderScale,
                        Math.min(154 * renderScale, memberRadius + 24 * renderScale)
                    );
                    const radius = Math.max(
                        8,
                        Math.min(naturalRadius, availableOuterRadius * 0.72)
                    );
                    const contourStep = Math.max(
                        0,
                        Math.min(
                            10 * renderScale,
                            (availableOuterRadius - radius) / 5
                        )
                    );
                    descriptors.push({
                        id: `overview:${layer}`,
                        layer,
                        order: asNumber(anchorNode.data("overviewLayerIndex"), descriptors.length),
                        x: anchorPosition.x,
                        y: anchorPosition.y,
                        radius,
                        memberCount: nodes.length,
                        anchor: isActive,
                        scale: metrics.sceneScale,
                        renderScale,
                        contourStep,
                        pulseScale: renderScale,
                        maxOuterRadius: availableOuterRadius,
                        rank: asNumber(anchorNode.data("overviewLayerIndex"), 0) + 1,
                        scene: "overview",
                        color: isActive
                            ? "rgba(217, 119, 6, 1)"
                            : "rgba(77, 182, 172, 1)",
                        fillColor: isActive
                            ? "rgba(217, 119, 6, 0.055)"
                            : "rgba(38, 166, 154, 0.022)",
                        syntheticSatellites: false
                    });
                });
            return descriptors;
        }

        _overviewFieldRoutes(descriptors) {
            if (!this.cy || this.mode !== "overview") return [];
            const byLayer = new Map(descriptors.map((descriptor) => [
                descriptor.layer,
                descriptor
            ]));
            const aggregated = new Map();
            this.cy.edges(":visible").forEach((edge) => {
                const sourceLayer = String(edge.source().data("layer") || "unknown");
                const targetLayer = String(edge.target().data("layer") || "unknown");
                if (sourceLayer === targetLayer || !byLayer.has(sourceLayer) || !byLayer.has(targetLayer)) {
                    return;
                }
                let source = byLayer.get(sourceLayer);
                let target = byLayer.get(targetLayer);
                if (source.order > target.order) [source, target] = [target, source];
                const key = `${source.layer}->${target.layer}`;
                const current = aggregated.get(key) || { source, target, count: 0, weight: 0 };
                current.count += 1;
                current.weight += Math.max(0, asNumber(edge.data("weight"), 1));
                aggregated.set(key, current);
            });
            return Array.from(aggregated.values())
                .sort((left, right) =>
                    left.source.order - right.source.order ||
                    left.target.order - right.target.order ||
                    right.count - left.count
                )
                .slice(0, OVERVIEW_ROUTE_LIMIT);
        }

        _overviewRouteStyle(route, strength = 0) {
            const normalizedStrength = Math.max(0, Math.min(1, asNumber(strength, 0)));
            const routeScale = Math.max(
                0.25,
                (asNumber(route?.source?.renderScale, 1) +
                    asNumber(route?.target?.renderScale, 1)) / 2
            );
            return {
                opacity: 0.34 + normalizedStrength * 0.3,
                width: (0.8 + normalizedStrength * 1.05) * routeScale,
                arrowSize: (6 + normalizedStrength * 2) * routeScale,
                dash: [7 * routeScale, 9 * routeScale]
            };
        }

        _communityFieldDescriptors() {
            if (!this.cy || this.mode !== "community") return [];
            const visibleNodes = [];
            this.cy.nodes(":visible").forEach((node) => {
                if (node.data("layer") === "community") visibleNodes.push(node);
            });
            const hasAnchor = visibleNodes.some((node) => node.id() === this.expandedCommunityId);
            const metrics = this._communitySceneMetrics(
                { width: this._fieldWidth, height: this._fieldHeight },
                Boolean(hasAnchor && (
                    this._detailCommunityId === this.expandedCommunityId ||
                    this.selectedNode?.length > 0
                ))
            );
            const { compact, sceneScale } = metrics;
            const contextScale = compact
                ? Math.max(0.34, sceneScale * 0.78)
                : sceneScale * sceneScale;
            const descriptors = visibleNodes.map((node) => {
                const position = node.renderedPosition();
                const memberCount = Math.max(1, asNumber(
                    node.data("node_count") ?? node.data("degree"),
                    1
                ));
                const anchor = node.id() === this.expandedCommunityId;
                const baseRadius = Math.max(
                    84,
                    Math.min(116, 72 + Math.log1p(memberCount) * 6)
                );
                let radius = Math.max(20, baseRadius * contextScale);
                if (anchor) {
                    let memberRadius = 0;
                    node.connectedEdges().forEach((edge) => {
                        if (edge.data("type") !== "community-member") return;
                        const other = edge.source().id() === node.id() ? edge.target() : edge.source();
                        const otherPosition = other.renderedPosition();
                        memberRadius = Math.max(
                            memberRadius,
                            Math.hypot(otherPosition.x - position.x, otherPosition.y - position.y)
                        );
                    });
                    radius = Math.max(
                        92 * sceneScale,
                        Math.min(196 * sceneScale, memberRadius + 34 * sceneScale)
                    );
                }
                return {
                    id: node.id(),
                    x: position.x,
                    y: position.y,
                    radius,
                    memberCount,
                    anchor,
                    scale: sceneScale,
                    rank: asNumber(node.data("rank"), 0),
                    scene: "community",
                    syntheticSatellites: !anchor
                };
            });
            if (compact && descriptors.length > 1) {
                descriptors.forEach((descriptor) => {
                    if (descriptor.anchor) return;
                    const nearestDistance = descriptors.reduce((nearest, other) => {
                        if (other === descriptor) return nearest;
                        return Math.min(
                            nearest,
                            Math.hypot(other.x - descriptor.x, other.y - descriptor.y)
                        );
                    }, Number.POSITIVE_INFINITY);
                    const contourGrowth = 5 * 10 * sceneScale * sceneScale;
                    const radiusLimit = nearestDistance * 0.38 - contourGrowth;
                    descriptor.radius = Math.max(
                        20,
                        Math.min(descriptor.radius, Math.max(20, radiusLimit))
                    );
                });
            }
            return descriptors;
        }

        _focusFieldDescriptors() {
            if (!this.cy || this.mode !== "focus") return [];
            const visibleNodes = [];
            this.cy.nodes(":visible").forEach((node) => {
                if (node.data("focusSceneRole")) visibleNodes.push(node);
            });
            const core = visibleNodes.find((node) => node.data("focusSceneRole") === "core") ||
                visibleNodes.find((node) => node.id() === this.selectedNodeId);
            if (!core) return [];
            const metrics = this._communitySceneMetrics(
                { width: this._fieldWidth, height: this._fieldHeight },
                true
            );
            const { compact, sceneScale } = metrics;
            const corePosition = core.renderedPosition();
            let innerRadius = 0;
            visibleNodes.forEach((node) => {
                if (node.data("focusSceneRole") !== "inner") return;
                const position = node.renderedPosition();
                innerRadius = Math.max(
                    innerRadius,
                    Math.hypot(position.x - corePosition.x, position.y - corePosition.y)
                );
            });
            const descriptors = [{
                id: `focus:${core.id()}`,
                x: corePosition.x,
                y: corePosition.y,
                radius: Math.max(
                    (compact ? 70 : 104) * sceneScale,
                    Math.min((compact ? 112 : 170) * sceneScale, innerRadius + 30 * sceneScale)
                ),
                memberCount: visibleNodes.filter((node) =>
                    node.data("focusSceneRole") === "inner"
                ).length + 1,
                anchor: true,
                scale: sceneScale,
                rank: 0,
                scene: "focus",
                syntheticSatellites: false
            }];
            const groups = new Map();
            visibleNodes.forEach((node) => {
                if (node.data("focusSceneRole") !== "context") return;
                const groupIndex = Math.max(0, asNumber(node.data("focusGroupIndex"), 0));
                if (!groups.has(groupIndex)) groups.set(groupIndex, []);
                groups.get(groupIndex).push(node);
            });
            Array.from(groups.entries())
                .sort((left, right) => left[0] - right[0])
                .forEach(([groupIndex, nodes]) => {
                    const groupAnchor = nodes.find((node) => node.hasClass?.("focus-group-anchor")) ||
                        nodes.sort((left, right) =>
                            asNumber(left.data("focusGroupOrder"), Number.MAX_SAFE_INTEGER) -
                                asNumber(right.data("focusGroupOrder"), Number.MAX_SAFE_INTEGER) ||
                            left.id().localeCompare(right.id())
                        )[0];
                    const position = groupAnchor.renderedPosition();
                    let groupRadius = 0;
                    nodes.forEach((node) => {
                        const memberPosition = node.renderedPosition();
                        groupRadius = Math.max(
                            groupRadius,
                            Math.hypot(memberPosition.x - position.x, memberPosition.y - position.y)
                        );
                    });
                    descriptors.push({
                        id: `focus-group:${groupIndex}`,
                        x: position.x,
                        y: position.y,
                        radius: Math.max(
                            46 * sceneScale,
                            Math.min(92 * sceneScale, groupRadius + 30 * sceneScale)
                        ),
                        memberCount: nodes.length,
                        anchor: false,
                        scale: sceneScale,
                        rank: groupIndex + 1,
                        scene: "focus",
                        syntheticSatellites: false
                    });
                });
            return descriptors;
        }

        _fieldSeed(value) {
            let seed = 2166136261;
            for (const character of String(value || "")) {
                seed ^= character.codePointAt(0);
                seed = Math.imul(seed, 16777619);
            }
            return (seed >>> 0) / 4294967295;
        }

        _drawFieldContour(context, descriptor, radius, color, opacity, phase = 0) {
            const points = 36;
            const seed = this._fieldSeed(descriptor.id);
            context.beginPath();
            for (let index = 0; index <= points; index += 1) {
                const angle = (index / points) * Math.PI * 2;
                const noise = 1 + Math.sin(angle * 3 + seed * 8 + phase) * 0.055 +
                    Math.cos(angle * 5 + seed * 5) * 0.035;
                const x = descriptor.x + Math.cos(angle) * radius * noise;
                const y = descriptor.y + Math.sin(angle) * radius * 0.82 * noise;
                if (index === 0) context.moveTo(x, y);
                else context.lineTo(x, y);
            }
            context.closePath();
            context.strokeStyle = color;
            context.globalAlpha = opacity;
            context.lineWidth = descriptor.anchor ? 1.2 : 0.8;
            context.stroke();
        }

        _drawFieldRoute(context, source, target, index = 0, options = {}) {
            const dx = target.x - source.x;
            const dy = target.y - source.y;
            const length = Math.max(1, Math.hypot(dx, dy));
            const unitX = dx / length;
            const unitY = dy / length;
            const ellipseInset = (field) => {
                const radiusX = Math.max(1, field.radius * 0.94);
                const radiusY = Math.max(1, field.radius * 0.68);
                return 1 / Math.sqrt(
                    (unitX * unitX) / (radiusX * radiusX) +
                    (unitY * unitY) / (radiusY * radiusY)
                );
            };
            const startInset = Math.min(ellipseInset(source) * 1.04, length * 0.42);
            const endInset = Math.min(ellipseInset(target) * 0.96, length * 0.42);
            const startX = source.x + unitX * startInset;
            const startY = source.y + unitY * startInset;
            const endX = target.x - unitX * endInset;
            const endY = target.y - unitY * endInset;
            const curve = (index % 2 === 0 ? 1 : -1) * Math.min(28, length * 0.04);
            const controlX = Math.max(
                4,
                Math.min(this._fieldWidth - 4, (startX + endX) / 2 - unitY * curve)
            );
            const controlY = Math.max(
                4,
                Math.min(this._fieldHeight - 4, (startY + endY) / 2 + unitX * curve)
            );
            context.setLineDash(options.dash || [8, 8]);
            context.beginPath();
            context.moveTo(startX, startY);
            context.quadraticCurveTo(controlX, controlY, endX, endY);
            context.strokeStyle = options.color || "rgba(95, 225, 214, 0.66)";
            context.globalAlpha = asNumber(options.opacity, 0.72);
            context.lineWidth = asNumber(options.width, 1.05);
            context.stroke();

            const arrowAngle = Math.atan2(endY - controlY, endX - controlX);
            const arrowSize = asNumber(options.arrowSize, 8);
            context.setLineDash([]);
            context.beginPath();
            context.moveTo(endX, endY);
            context.lineTo(
                endX - Math.cos(arrowAngle - 0.5) * arrowSize,
                endY - Math.sin(arrowAngle - 0.5) * arrowSize
            );
            context.lineTo(
                endX - Math.cos(arrowAngle + 0.5) * arrowSize,
                endY - Math.sin(arrowAngle + 0.5) * arrowSize
            );
            context.closePath();
            context.fillStyle = options.arrowColor || "rgba(117, 230, 216, 0.84)";
            context.globalAlpha = Math.min(1, asNumber(options.opacity, 0.72) + 0.12);
            context.fill();
            context.setLineDash([]);
        }

        _drawCommunityField(timestamp = 0) {
            if (!this._fieldContext || this.isDestroyed) return;
            const context = this._fieldContext;
            context.clearRect(0, 0, this._fieldWidth, this._fieldHeight);
            if (!["overview", "community", "focus"].includes(this.mode) || !this.cy) {
                this._communityFields = [];
                return;
            }

            const descriptors = this._fieldDescriptors();
            this._communityFields = descriptors;
            const phase = (asNumber(timestamp, 0) % 2400) / 2400;
            context.save();
            context.lineJoin = "round";
            context.lineCap = "round";

            const anchorDescriptor = descriptors.find((descriptor) => descriptor.anchor);
            if (this.mode === "overview") {
                const routes = this._overviewFieldRoutes(descriptors);
                const maximumCount = Math.max(1, ...routes.map((route) => route.count));
                routes.forEach((route, index) => {
                    const strength = Math.max(0, Math.min(1, route.count / maximumCount));
                    this._drawFieldRoute(
                        context,
                        route.source,
                        route.target,
                        index,
                        this._overviewRouteStyle(route, strength)
                    );
                });
            } else if (anchorDescriptor) {
                const contexts = descriptors.filter((descriptor) => !descriptor.anchor);
                contexts.forEach((descriptor, index) => {
                    this._drawFieldRoute(context, anchorDescriptor, descriptor, index);
                });
            }

            for (const descriptor of descriptors) {
                const color = descriptor.color || (
                    descriptor.anchor ? "rgba(217, 119, 6, 1)" : "rgba(77, 182, 172, 1)"
                );
                const fillColor = descriptor.fillColor || (
                    descriptor.anchor ? "rgba(217, 119, 6, 0.055)" : "rgba(38, 166, 154, 0.022)"
                );
                context.beginPath();
                context.ellipse(
                    descriptor.x,
                    descriptor.y,
                    descriptor.radius * 0.94,
                    descriptor.radius * 0.68,
                    0,
                    0,
                    Math.PI * 2
                );
                context.fillStyle = fillColor;
                context.globalAlpha = 1;
                context.fill();

                for (let contour = 0; contour < 6; contour += 1) {
                    const contourStep = descriptor.contourStep ??
                        10 * descriptor.scale * descriptor.scale;
                    this._drawFieldContour(
                        context,
                        descriptor,
                        descriptor.radius + contour * contourStep,
                        color,
                        descriptor.anchor ? 0.27 - contour * 0.038 : 0.15 - contour * 0.022,
                        contour * 0.42
                    );
                }

                if (!descriptor.anchor && descriptor.syntheticSatellites) {
                    const minimumSatellites = descriptor.scale < 0.7 ? 5 : 7;
                    const satellites = Math.max(minimumSatellites, Math.min(
                        descriptor.scale < 0.7 ? 8 : 12,
                        Math.round(4 + Math.log2(descriptor.memberCount))
                    ));
                    const seed = this._fieldSeed(descriptor.id);
                    const points = [];
                    for (let index = 0; index < satellites; index += 1) {
                        const angle = seed * Math.PI * 2 + (index / satellites) * Math.PI * 2;
                        const orbitScale = [0.34, 0.58, 0.78][index % 3];
                        const orbit = descriptor.radius * orbitScale;
                        const x = descriptor.x + Math.cos(angle) * orbit;
                        const y = descriptor.y + Math.sin(angle) * orbit * 0.78;
                        points.push({ x, y });
                    }
                    context.strokeStyle = "rgba(95, 225, 214, 0.24)";
                    context.globalAlpha = 0.75;
                    context.lineWidth = 0.65;
                    points.forEach((point, index) => {
                        context.beginPath();
                        context.moveTo(descriptor.x, descriptor.y);
                        context.lineTo(point.x, point.y);
                        context.stroke();
                        if (index % 2 === 0 && points.length > 2) {
                            const neighbor = points[(index + 2) % points.length];
                            context.beginPath();
                            context.moveTo(point.x, point.y);
                            context.lineTo(neighbor.x, neighbor.y);
                            context.stroke();
                        }
                    });
                    points.forEach((point, index) => {
                        context.beginPath();
                        const pointRadius = 3.1 + (index % 3) * 0.8;
                        context.arc(point.x, point.y, pointRadius, 0, Math.PI * 2);
                        context.fillStyle = "rgba(8, 37, 42, 0.92)";
                        context.globalAlpha = 1;
                        context.fill();
                        context.strokeStyle = "rgba(117, 230, 216, 0.82)";
                        context.lineWidth = 0.85;
                        context.stroke();
                        context.beginPath();
                        context.arc(point.x, point.y, 1.15, 0, Math.PI * 2);
                        context.fillStyle = "rgba(117, 230, 216, 0.9)";
                        context.fill();
                    });
                    for (let ring = 0; ring < 3; ring += 1) {
                        context.beginPath();
                        context.arc(descriptor.x, descriptor.y, 6 + ring * 5, 0, Math.PI * 2);
                        context.strokeStyle = "rgba(117, 230, 216, 0.24)";
                        context.globalAlpha = 0.8 - ring * 0.16;
                        context.lineWidth = 0.8;
                        context.stroke();
                    }
                }

                if (descriptor.anchor) {
                    const pulseScale = descriptor.pulseScale || descriptor.scale;
                    const pulseRadius = (offset) => Math.min(
                        asNumber(descriptor.maxOuterRadius, Number.POSITIVE_INFINITY),
                        descriptor.radius + offset * pulseScale
                    );
                    context.setLineDash([4, 8]);
                    for (let pulseRing = 0; pulseRing < 2; pulseRing += 1) {
                        const ringRadius = pulseRadius(22 + pulseRing * 18);
                        context.beginPath();
                        context.ellipse(
                            descriptor.x,
                            descriptor.y,
                            ringRadius,
                            ringRadius * 0.82,
                            0,
                            0,
                            Math.PI * 2
                        );
                        context.strokeStyle = "rgba(217, 119, 6, 0.42)";
                        context.globalAlpha = 0.36 - pulseRing * 0.1;
                        context.lineWidth = 0.85;
                        context.stroke();
                    }
                    context.setLineDash([]);
                    this._drawFieldContour(
                        context,
                        descriptor,
                        pulseRadius(12 + phase * 26),
                        color,
                        0.28 * (1 - phase),
                        phase * Math.PI * 2
                    );
                }
            }
            context.restore();
            this._fieldPaintCount += 1;
        }

        _shouldPaintCommunityFrame(timestamp) {
            return !this._fieldTimestamp ||
                asNumber(timestamp, 0) - this._fieldTimestamp >= 1000 / COMMUNITY_FIELD_FPS;
        }

        _communityFieldTick(timestamp) {
            this._fieldFrame = null;
            if (this._paused || this.isDestroyed ||
                !["overview", "community", "focus"].includes(this.mode)) return;
            if (!this._fieldDirty) return;
            if (!this._shouldPaintCommunityFrame(timestamp)) {
                this._fieldFrame = global.requestAnimationFrame?.((nextTimestamp) =>
                    this._communityFieldTick(nextTimestamp)
                ) || null;
                return;
            }
            this._fieldTimestamp = asNumber(timestamp, 0);
            this._fieldDirty = false;
            this._drawCommunityField(timestamp);
        }

        _scheduleCommunityFieldDraw() {
            if (!this._fieldContext || this.isDestroyed || this._paused) return;
            if (!["overview", "community", "focus"].includes(this.mode)) {
                this._stopCommunityFieldLoop(true);
                this._communityFields = [];
                return;
            }
            this._fieldDirty = true;
            if (this._fieldFrame) return;
            this._fieldFrame = global.requestAnimationFrame?.((timestamp) =>
                this._communityFieldTick(timestamp)
            ) || null;
            if (!this._fieldFrame) {
                this._fieldDirty = false;
                this._drawCommunityField(0);
            }
        }

        _stopCommunityFieldLoop(clearCanvas = false) {
            if (this._fieldFrame) {
                global.cancelAnimationFrame?.(this._fieldFrame);
                this._fieldFrame = null;
            }
            this._fieldTimestamp = 0;
            this._fieldDirty = false;
            if (clearCanvas && this._fieldContext) {
                this._fieldContext.clearRect(0, 0, this._fieldWidth, this._fieldHeight);
            }
        }

        _initOverlay() {
            if (this._overlayCanvas || !global.document) return;
            this._initCommunityField();
            const canvas = global.document.createElement("canvas");
            canvas.className = "graph-particle-overlay";
            canvas.setAttribute("aria-hidden", "true");
            canvas.style.position = "absolute";
            canvas.style.inset = "0";
            canvas.style.width = "100%";
            canvas.style.height = "100%";
            canvas.style.pointerEvents = "none";
            canvas.style.zIndex = "4";

            const computedPosition = global.getComputedStyle?.(this.container)?.position;
            if (!computedPosition || computedPosition === "static") {
                this._containerPositionBefore = this.container.style.position;
                this.container.style.position = "relative";
            }
            this.container.appendChild(canvas);
            this._overlayCanvas = canvas;
            this._overlayContext = canvas.getContext("2d");
            this._resizeOverlay();

            if (typeof global.ResizeObserver === "function") {
                this._resizeObserver = new global.ResizeObserver(() => this._handleViewportResize());
                this._resizeObserver.observe(this.container);
            }
            global.addEventListener?.("resize", this._handleWindowResize, { passive: true });
            global.document?.addEventListener?.("visibilitychange", this._handleVisibilityChange);
            this._motionQuery = global.matchMedia?.("(prefers-reduced-motion: reduce)") || null;
            if (typeof this._motionQuery?.addEventListener === "function") {
                this._motionQuery.addEventListener("change", this._handleMotionChange);
                this._motionListenerType = "event";
            } else if (typeof this._motionQuery?.addListener === "function") {
                this._motionQuery.addListener(this._handleMotionChange);
                this._motionListenerType = "legacy";
            }
        }

        _resolveOverlayPixelRatio(width, height) {
            const requested = Math.min(2, Math.max(1, asNumber(global.devicePixelRatio, 1)));
            const cssPixels = Math.max(1, asNumber(width, 1) * asNumber(height, 1));
            const budgetRatio = Math.sqrt(MAX_OVERLAY_PIXELS / cssPixels);
            return Math.max(0.25, Math.min(requested, budgetRatio));
        }

        _resizeOverlay() {
            if (!this._overlayCanvas || !this._overlayContext || this.isDestroyed) return;
            const rect = this.container.getBoundingClientRect();
            const width = Math.max(1, Math.round(rect.width));
            const height = Math.max(1, Math.round(rect.height));
            const pixelRatio = this._resolveOverlayPixelRatio(width, height);
            this._overlayWidth = width;
            this._overlayHeight = height;
            this._overlayCanvas.style.width = `${width}px`;
            this._overlayCanvas.style.height = `${height}px`;
            const targetWidth = Math.round(width * pixelRatio);
            const targetHeight = Math.round(height * pixelRatio);
            if (this._overlayCanvas.width !== targetWidth) this._overlayCanvas.width = targetWidth;
            if (this._overlayCanvas.height !== targetHeight) this._overlayCanvas.height = targetHeight;
            this._overlayContext.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
            this._resizeCommunityField(width, height, pixelRatio);
            this._scheduleCommunityFieldDraw();
        }

        _handleViewportResize() {
            if (this.isDestroyed) return;
            this._resizeOverlay();
            this.cy?.resize?.();

            if (this._resizeFitTimer !== null) {
                global.clearTimeout?.(this._resizeFitTimer);
            }
            const refit = () => {
                this._resizeFitTimer = null;
                if (!this.cy || this.isDestroyed) return;
                if (this.mode === "overview") {
                    this._runLayout("overview");
                    return;
                }
                if (this.mode === "community") {
                    this._runLayout("community");
                    return;
                }
                if (this.mode === "focus") {
                    this._runLayout("focus");
                    if (this.cy.zoom() > 1) this.cy.zoom(1);
                    return;
                }
            };
            if (typeof global.setTimeout === "function") {
                this._resizeFitTimer = global.setTimeout(refit, 120);
            } else {
                refit();
            }
        }

        _syncParticles() {
            if (!this.cy || !this._overlayContext || this.isDestroyed || this.reducedMotion) {
                this._particles = [];
                this._stopParticleLoop(true);
                return;
            }
            const edges = [];
            let candidates;
            if (this.mode === "community" && this.selectedNode?.data?.("layer") === "community") {
                candidates = this.cy.edges(".community-route");
            } else if (this.mode === "focus") {
                candidates = this.cy.edges(".focus-inner-link.highlighted");
            } else {
                candidates = this.cy.edges(".highlighted");
            }
            candidates.forEach((edge) => {
                if (typeof edge.visible !== "function" || edge.visible()) edges.push(edge);
            });
            edges.sort((left, right) =>
                asNumber(right.data("weight"), 1) - asNumber(left.data("weight"), 1)
            );
            const previous = new Map(this._particles.map((particle) => [particle.edgeId, particle]));
            this._particles = edges.slice(0, MAX_PARTICLES).map((edge, index) => {
                const old = previous.get(edge.id());
                return old || {
                    edgeId: edge.id(),
                    progress: (index * 0.61803398875) % 1,
                    speed: 0.12 + (index % 7) * 0.012,
                    size: 1.5 + (index % 3) * 0.35,
                    reverse: index % 2 === 1
                };
            });
            if (this._particles.length === 0) this._stopParticleLoop(true);
            else this._startParticleLoop();
        }

        _startParticleLoop() {
            if (this._particleFrame || this._paused || this.reducedMotion ||
                global.document?.hidden || this.isDestroyed || this._particles.length === 0) {
                return;
            }
            this._particleFrame = global.requestAnimationFrame?.((time) => this._drawParticles(time)) || null;
        }

        _drawParticles(timestamp) {
            this._particleFrame = null;
            if (!this._overlayContext || this._paused || this.reducedMotion ||
                global.document?.hidden || this.isDestroyed) {
                this._stopParticleLoop(true);
                return;
            }
            if (
                this._particleTimestamp &&
                timestamp - this._particleTimestamp < 1000 / PARTICLE_FPS
            ) {
                this._startParticleLoop();
                return;
            }
            const elapsed = this._particleTimestamp
                ? Math.min(0.05, Math.max(0, (timestamp - this._particleTimestamp) / 1000))
                : 0;
            this._particleTimestamp = timestamp;
            const context = this._overlayContext;
            this._particleDirtyRects.forEach(({ x, y, width, height }) => {
                context.clearRect(x, y, width, height);
            });
            const dirtyRects = [];
            context.save();
            context.fillStyle = "rgba(77, 255, 232, 0.95)";
            context.shadowColor = "rgba(51, 230, 210, 0.9)";
            context.shadowBlur = 9;

            for (const particle of this._particles) {
                const edge = this.cy.getElementById(particle.edgeId);
                if (!edge || edge.length === 0 || (edge.visible && !edge.visible())) continue;
                particle.progress = (particle.progress + elapsed * particle.speed) % 1;
                const progress = particle.reverse ? 1 - particle.progress : particle.progress;
                const point = this._pointOnRenderedEdge(edge, progress);
                if (!point) continue;
                const { x, y } = point;
                if (x < -12 || x > this._overlayWidth + 12 || y < -12 || y > this._overlayHeight + 12) {
                    continue;
                }
                context.beginPath();
                context.arc(x, y, particle.size, 0, Math.PI * 2);
                context.fill();
                dirtyRects.push({ x: x - 17, y: y - 17, width: 34, height: 34 });
            }
            context.restore();
            this._particleDirtyRects = dirtyRects;
            this._startParticleLoop();
        }

        _pointOnRenderedEdge(edge, progress) {
            const t = Math.max(0, Math.min(1, asNumber(progress, 0)));
            try {
                const source = edge.renderedSourceEndpoint?.() || edge.source?.()?.renderedPosition?.();
                const target = edge.renderedTargetEndpoint?.() || edge.target?.()?.renderedPosition?.();
                if (!source || !target) return null;
                const midpoint = edge.renderedMidpoint?.();
                if (!midpoint) {
                    return {
                        x: source.x + (target.x - source.x) * t,
                        y: source.y + (target.y - source.y) * t
                    };
                }
                const inverse = 1 - t;
                const control = {
                    x: 2 * midpoint.x - (source.x + target.x) / 2,
                    y: 2 * midpoint.y - (source.y + target.y) / 2
                };
                return {
                    x: inverse * inverse * source.x + 2 * inverse * t * control.x + t * t * target.x,
                    y: inverse * inverse * source.y + 2 * inverse * t * control.y + t * t * target.y
                };
            } catch (_) {
                return null;
            }
        }

        _stopParticleLoop(clearCanvas = false) {
            if (this._particleFrame) {
                global.cancelAnimationFrame?.(this._particleFrame);
                this._particleFrame = null;
            }
            this._particleTimestamp = 0;
            this._particleDirtyRects = [];
            if (clearCanvas && this._overlayContext) {
                this._overlayContext.clearRect(0, 0, this._overlayWidth, this._overlayHeight);
            }
        }

        pause() {
            if (this.isDestroyed || this._paused) return;
            this._paused = true;
            this._layoutInterrupted = Boolean(this._layoutRunning);
            this.container.closest?.(".graph-workbench")?.classList?.add?.("is-paused");
            this._activeLayout?.stop?.();
            this._stopParticleLoop(true);
            this._stopCommunityFieldLoop(false);
        }

        resume() {
            if (this.isDestroyed || !this._paused) return;
            const restoreLayout = Boolean(this._layoutInterrupted && this.cy);
            this._paused = false;
            this._layoutInterrupted = false;
            this.container.closest?.(".graph-workbench")?.classList?.remove?.("is-paused");
            this._resizeOverlay();
            if (restoreLayout) this._runLayout(this.mode);
            this._syncParticles();
            this._scheduleCommunityFieldDraw();
        }

        zoomIn() {
            if (!this.cy) return;
            this.cy.animate({ zoom: Math.min(this.cy.maxZoom(), this.cy.zoom() * 1.25) }, {
                duration: this.reducedMotion ? 0 : 220,
                easing: "ease-out-cubic"
            });
        }

        zoomOut() {
            if (!this.cy) return;
            this.cy.animate({ zoom: Math.max(this.cy.minZoom(), this.cy.zoom() / 1.25) }, {
                duration: this.reducedMotion ? 0 : 220,
                easing: "ease-out-cubic"
            });
        }

        _fitCurrentGraph(padding = 36) {
            if (!this.cy || this.cy.elements(":visible").length === 0) return;
            this.cy.animate({ fit: { eles: this.cy.elements(":visible"), padding } }, {
                duration: this.reducedMotion ? 0 : 420,
                easing: "ease-out-cubic"
            });
        }

        fitToScreen() {
            if (["overview", "community", "focus"].includes(this.mode)) {
                this._runLayout(this.mode);
                return;
            }
            this._fitCurrentGraph(32);
        }

        resetView() {
            this.clearSelection({ reflow: false });
            if (this.mode !== "overview") {
                return this.setMode("overview");
            }
            this._runLayout("overview");
            return Promise.resolve(this.mode);
        }

        _emitReady() {
            this._emit("graph:ready", {
                mode: this.mode,
                version: this.data.version,
                generated_at: this.data.generated_at,
                stats: this.data.stats,
                visibleNodes: this.currentGraph.nodes.length,
                visibleEdges: this.currentGraph.links.length
            });
        }

        _emitError(operation, error) {
            this._emit("graph:error", {
                operation,
                message: error?.message || String(error),
                error
            });
        }

        _emit(eventName, detail) {
            if (!this.container?.dispatchEvent) return;
            let event;
            if (typeof global.CustomEvent === "function") {
                event = new global.CustomEvent(eventName, { detail });
            } else if (global.document?.createEvent) {
                event = global.document.createEvent("CustomEvent");
                event.initCustomEvent(eventName, false, false, detail);
            } else {
                return;
            }
            this.container.dispatchEvent(event);
        }

        destroy() {
            if (this.isDestroyed) return;
            this.isDestroyed = true;
            this._modeSequence += 1;
            this._searchSequence += 1;
            this._detailCommunityId = null;
            this._defaultCommunityExpansion = null;
            this._activeLayout?.stop?.();
            this._stopParticleLoop(true);
            this._stopCommunityFieldLoop(true);
            this._rejectPendingRequests(createAbortError("Graph engine destroyed"));

            if (this.worker) {
                if (typeof this.worker.removeEventListener === "function") {
                    this.worker.removeEventListener("message", this._workerMessageHandler);
                    this.worker.removeEventListener("error", this._workerErrorHandler);
                }
                this.worker.terminate?.();
                this.worker = null;
            }

            this._resizeObserver?.disconnect?.();
            this._resizeObserver = null;
            if (this._resizeFitTimer !== null) {
                global.clearTimeout?.(this._resizeFitTimer);
                this._resizeFitTimer = null;
            }
            global.removeEventListener?.("resize", this._handleWindowResize);
            global.document?.removeEventListener?.("visibilitychange", this._handleVisibilityChange);
            if (this._motionListenerType === "event") {
                this._motionQuery?.removeEventListener?.("change", this._handleMotionChange);
            } else if (this._motionListenerType === "legacy") {
                this._motionQuery?.removeListener?.(this._handleMotionChange);
            }
            this._motionListenerType = null;
            this._motionQuery = null;

            this._overlayCanvas?.remove?.();
            this._overlayCanvas = null;
            this._overlayContext = null;
            this._fieldCanvas?.remove?.();
            this._fieldCanvas = null;
            this._fieldContext = null;
            this._communityFields = [];
            this.container.closest?.(".graph-workbench")?.classList?.remove?.("is-paused");
            if (this._containerPositionBefore !== null) {
                this.container.style.position = this._containerPositionBefore;
                this._containerPositionBefore = null;
            }

            this.cy?.destroy?.();
            this.cy = null;
            this.selectedNode = null;
            this.selectedNodeId = null;
            this.hoveredNode = null;
            this._particles = [];
        }
    }

    global.CytoscapeGraphEngine = CytoscapeGraphEngine;
})(typeof window !== "undefined" ? window : this);
