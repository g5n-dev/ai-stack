/**
 * AI Stack Cytoscape Graph Engine
 * 基于 Cytoscape.js 的炫酷图谱渲染引擎
 */

(function (global) {
    "use strict";

    class CytoscapeGraphEngine {
        constructor(container, data) {
            this.container = typeof container === "string"
                ? document.querySelector(container)
                : container;

            if (!this.container) {
                throw new Error("Graph container not found");
            }

            this.data = this._prepareData(data);
            this.layoutMode = (this.data && this.data.layout_mode) || "layered";
            this._layeredPositions = this._computeLayeredPositionsFromRawNodes(this.data.nodes);
            this.cy = null;
            this.isDestroyed = false;
            this.visibleLayers = new Set(
                Array.isArray(this.data.initial_visible_layers) && this.data.initial_visible_layers.length > 0
                    ? this.data.initial_visible_layers
                    : Object.keys(this.data.layers || {})
            );
            this.loadedLayers = new Set();
            this.fullLayers = new Set(Array.isArray(this.data.full_layers) ? this.data.full_layers : []);
            this.loadedNodeIds = new Set();
            this.loadedEdgeIds = new Set();
            this.pendingEdges = new Map();
            this.splitBaseUrl = this.data.split_base_url || "";
            this.splitFiles = this.data.split_files || {};
            this.searchQuery = "";
            this.hoveredNode = null;
            this.selectedNode = null;
            this.particles = [];
            this.animationFrame = null;
            this._relayoutTimer = null;
            this._activeLayout = null;

            this._initCytoscape();
            this._initAnimations();
            this._bindEvents();
        }

        _getLayoutOptions(override = {}) {
            if (this.layoutMode === "layered") {
                const animate = override.animate !== false;
                const positions = override.positions || this._layeredPositions || {};
                return {
                    name: "preset",
                    fit: false,
                    animate,
                    animationDuration: typeof override.animationDuration === "number" ? override.animationDuration : 900,
                    positions
                };
            }

            return {
                name: 'cose-bilkent',
                animate: true,
                animationDuration: 1200,
                animationEasing: 'ease-out-cubic',
                randomize: false,
                nodeRepulsion: 4500,
                idealEdgeLength: 100,
                edgeElasticity: 0.45,
                nestingFactor: 1.2,
                gravity: 1,
                numIter: 1200,
                tile: true,
                tilingPaddingVertical: 10,
                tilingPaddingHorizontal: 10,
                stopAfter: 700,
                ...override
            };
        }

        _scheduleRelayout(opts = {}) {
            if (this.isDestroyed || !this.cy) return;
            const shouldRelayout = opts.relayout !== false;
            if (!shouldRelayout) return;

            const delay = typeof opts.delay === "number" ? opts.delay : 40;
            if (this._relayoutTimer) clearTimeout(this._relayoutTimer);
            this._relayoutTimer = setTimeout(() => {
                if (this.isDestroyed || !this.cy) return;
                if (this._activeLayout && typeof this._activeLayout.stop === "function") {
                    try { this._activeLayout.stop(); } catch (_) { }
                }
                const animate = opts.animate !== false;
                if (this.layoutMode === "layered") {
                    this._applyLayeredLayout({ animate });
                    return;
                }
                const layout = this.cy.layout(this._getLayoutOptions({ animate }));
                this._activeLayout = layout;
                layout.run();
            }, delay);
        }

        _normalizeLevel(value) {
            const num = typeof value === "number" ? value : Number(value);
            return Number.isFinite(num) ? num : 0;
        }

        _computeLayeredPositionsFromRawNodes(rawNodes) {
            const nodes = Array.isArray(rawNodes) ? rawNodes : [];
            const groups = new Map();

            for (const node of nodes) {
                if (!node || !node.id) continue;
                const layer = node.layer;
                const level = this._normalizeLevel(
                    node.level != null ? node.level : (layer && this.data.layers && this.data.layers[layer] ? this.data.layers[layer].level : 0)
                );
                if (!groups.has(level)) groups.set(level, []);
                groups.get(level).push(node);
            }

            const levels = Array.from(groups.keys()).sort((a, b) => a - b);
            const minLevel = levels.length > 0 ? levels[0] : 0;
            const positions = {};
            const rankSep = 260;
            const nodeSep = 170;

            for (const level of levels) {
                const list = groups.get(level) || [];
                list.sort((a, b) => {
                    const da = typeof a.degree === "number" ? a.degree : (typeof a.connections === "number" ? a.connections : 0);
                    const db = typeof b.degree === "number" ? b.degree : (typeof b.connections === "number" ? b.connections : 0);
                    if (db !== da) return db - da;
                    return String(a.id).localeCompare(String(b.id));
                });

                const center = (list.length - 1) / 2;
                for (let i = 0; i < list.length; i += 1) {
                    const node = list[i];
                    positions[node.id] = {
                        x: (i - center) * nodeSep,
                        y: (level - minLevel) * rankSep
                    };
                }
            }

            return positions;
        }

        _computeLayeredPositionsFromCyNodes() {
            if (!this.cy) return {};
            const groups = new Map();
            const nodes = this.cy.nodes();

            nodes.forEach((node) => {
                const data = node.data();
                const level = this._normalizeLevel(
                    data.level != null ? data.level : (data.layer && this.data.layers && this.data.layers[data.layer] ? this.data.layers[data.layer].level : 0)
                );
                if (!groups.has(level)) groups.set(level, []);
                groups.get(level).push(node);
            });

            const levels = Array.from(groups.keys()).sort((a, b) => a - b);
            const minLevel = levels.length > 0 ? levels[0] : 0;
            const positions = {};
            const rankSep = 260;
            const nodeSep = 170;

            for (const level of levels) {
                const list = groups.get(level) || [];
                list.sort((a, b) => {
                    const da = typeof a.data("degree") === "number" ? a.data("degree") : 0;
                    const db = typeof b.data("degree") === "number" ? b.data("degree") : 0;
                    if (db !== da) return db - da;
                    return String(a.id()).localeCompare(String(b.id()));
                });

                const center = (list.length - 1) / 2;
                for (let i = 0; i < list.length; i += 1) {
                    const node = list[i];
                    positions[node.id()] = {
                        x: (i - center) * nodeSep,
                        y: (level - minLevel) * rankSep
                    };
                }
            }

            return positions;
        }

        _applyLayeredLayout(opts = {}) {
            if (this.isDestroyed || !this.cy) return;
            const animate = opts.animate !== false;
            this._layeredPositions = this._computeLayeredPositionsFromCyNodes();
            const layout = this.cy.layout(this._getLayoutOptions({ animate, positions: this._layeredPositions }));
            this._activeLayout = layout;
            layout.run();
        }

        _prepareData(rawData) {
            const data = rawData || {};
            data.nodes = Array.isArray(data.nodes) ? data.nodes : [];
            data.links = Array.isArray(data.links) ? data.links : [];
            data.layers = data.layers || {};

            const derivedLayers = {};
            data.nodes.forEach(node => {
                if (!derivedLayers[node.layer]) {
                    derivedLayers[node.layer] = {
                        name: node.layer_name || node.layer,
                        level: node.level || 1
                    };
                }
            });
            data.layers = { ...(data.layers || {}), ...derivedLayers };

            return data;
        }

        _initCytoscape() {
            this.cy = cytoscape({
                container: this.container,
                elements: this._formatElements(),
                style: this._getStylesheet(),
                layout: this._getLayoutOptions({ animate: true, positions: this._layeredPositions }),
                wheelSensitivity: 0.3,
                minZoom: 0.1,
                maxZoom: 5,
                textureOnViewport: true,
                motionBlur: true,
                motionBlurOpacity: 0.1
            });

            this._applyInitialZoom();
            this._initParticles();
        }

        _formatNodeElement(node) {
            const element = {
                data: {
                    id: node.id,
                    label: node.name,
                    layer: node.layer,
                    layerName: node.layer_name,
                    level: node.level,
                    color: node.color,
                    category: node.category,
                    description: node.description,
                    connections: node.connections || node.degree || 0,
                    degree: node.degree || node.connections || 0
                },
                classes: `layer-${node.layer}`
            };
            const pos = this._layeredPositions && this._layeredPositions[node.id];
            if (pos) element.position = pos;
            return element;
        }

        _formatEdgeElement(link, index) {
            return {
                data: {
                    id: link.id || `edge-${link.source}-${link.target}`,
                    source: link.source,
                    target: link.target,
                    strength: link.strength || 1,
                    index: typeof index === "number" ? index : 0
                },
                classes: 'link'
            };
        }

        _formatElements() {
            const nodes = [];
            const edges = [];

            this.data.nodes.forEach((node) => {
                if (!node || !node.id) return;
                this.loadedNodeIds.add(node.id);
                if (node.layer) this.loadedLayers.add(node.layer);
                nodes.push(this._formatNodeElement(node));
            });

            this.data.links.forEach((link, index) => {
                if (!link || !link.source || !link.target) return;
                const edgeId = link.id || `edge-${link.source}-${link.target}`;
                if (this.loadedEdgeIds.has(edgeId)) return;
                this.loadedEdgeIds.add(edgeId);
                edges.push(this._formatEdgeElement({ ...link, id: edgeId }, index));
            });

            return { nodes, edges };
        }

        async ensureLayerLoaded(layer) {
            if (!layer) return;
            if ((layer === "tag" || layer === "concept")) {
                if (this.fullLayers.has(layer) || this.loadedLayers.has(layer)) return;
            } else {
                if (this.loadedLayers.has(layer)) return;
            }

            const base = this.splitBaseUrl || "";
            const files = this.splitFiles || {};

            let url = null;
            if (layer === "tag") url = files.tag ? `${base}${files.tag}` : null;
            if (layer === "concept") url = files.concept ? `${base}${files.concept}` : null;

            if (!url) {
                this.loadedLayers.add(layer);
                return;
            }

            const payload = await this._loadJson(url);
            if (this.isDestroyed) return;
            const nodes = Array.isArray(payload?.nodes) ? payload.nodes : [];
            const links = Array.isArray(payload?.links) ? payload.links : [];
            this.addGraphData({ nodes, links, layers: payload?.layers || {} });
            if (layer === "tag" || layer === "concept") {
                this.fullLayers.add(layer);
            } else {
                this.loadedLayers.add(layer);
            }
        }

        async toggleLayer(layer) {
            if (!layer) return;
            const currentlyVisible = this.visibleLayers.has(layer);
            if (!currentlyVisible) {
                await this.ensureLayerLoaded(layer);
                if (this.isDestroyed) return;
                this.visibleLayers.add(layer);
            } else {
                this.visibleLayers.delete(layer);
            }
            this._applyLayerVisibility();
        }

        addGraphData(partial) {
            const nodes = Array.isArray(partial?.nodes) ? partial.nodes : [];
            const links = Array.isArray(partial?.links) ? partial.links : [];
            const incomingLayers = partial?.layers || {};

            this.data.layers = { ...(this.data.layers || {}), ...(incomingLayers || {}) };

            const extent = this.cy ? this.cy.extent() : null;
            const cx = extent ? (extent.x1 + extent.x2) / 2 : 0;
            const cy = extent ? (extent.y1 + extent.y2) / 2 : 0;
            const spread = Math.max(600, extent ? Math.min(1600, (extent.x2 - extent.x1 + extent.y2 - extent.y1) / 2) : 900);

            const newNodeEles = [];
            nodes.forEach((node) => {
                if (!node || !node.id) return;
                if (this.loadedNodeIds.has(node.id)) return;
                this.loadedNodeIds.add(node.id);
                if (node.layer) this.loadedLayers.add(node.layer);
                const ele = this._formatNodeElement(node);
                ele.position = {
                    x: cx + (Math.random() - 0.5) * spread,
                    y: cy + (Math.random() - 0.5) * spread
                };
                newNodeEles.push(ele);
                this.data.nodes.push(node);
            });

            if (newNodeEles.length > 0) {
                this.cy.add(newNodeEles);
            }

            links.forEach((link) => {
                if (!link || !link.source || !link.target) return;
                const edgeId = link.id || `edge-${link.source}-${link.target}`;
                if (this.loadedEdgeIds.has(edgeId)) return;
                const normalized = { ...link, id: edgeId };

                const hasSource = this.loadedNodeIds.has(normalized.source);
                const hasTarget = this.loadedNodeIds.has(normalized.target);

                if (!hasSource || !hasTarget) {
                    this.pendingEdges.set(edgeId, normalized);
                    return;
                }

                this.loadedEdgeIds.add(edgeId);
                this.cy.add(this._formatEdgeElement(normalized, this.loadedEdgeIds.size));
                this.data.links.push(normalized);
            });

            if (this.pendingEdges.size > 0) {
                const ready = [];
                for (const [edgeId, link] of this.pendingEdges.entries()) {
                    if (!this.loadedNodeIds.has(link.source) || !this.loadedNodeIds.has(link.target)) continue;
                    this.pendingEdges.delete(edgeId);
                    if (this.loadedEdgeIds.has(edgeId)) continue;
                    this.loadedEdgeIds.add(edgeId);
                    ready.push(this._formatEdgeElement(link, this.loadedEdgeIds.size));
                    this.data.links.push(link);
                }
                if (ready.length > 0) {
                    this.cy.add(ready);
                }
            }

            this._applyLayerVisibility();
            const relayout = newNodeEles.length > 0 && newNodeEles.length <= 1200;
            this._scheduleRelayout({ relayout, animate: newNodeEles.length <= 600 });
        }

        _applyLayerVisibility() {
            this.cy.nodes().forEach(node => {
                const nodeLayer = node.data('layer');
                if (this.visibleLayers.has(nodeLayer)) {
                    node.style('display', 'element');
                } else {
                    node.style('display', 'none');
                }
            });

            this.cy.edges().forEach(edge => {
                const source = edge.source();
                const target = edge.target();
                if (this.visibleLayers.has(source.data('layer')) &&
                    this.visibleLayers.has(target.data('layer'))) {
                    edge.style('display', 'element');
                } else {
                    edge.style('display', 'none');
                }
            });
        }

        _loadJson(url) {
            const fetchUrl = url;
            if (global.dataWorkerFactory) {
                return global.dataWorkerFactory(fetchUrl);
            }
            return fetch(fetchUrl).then(r => {
                if (!r.ok) throw new Error(`HTTP error! status: ${r.status}`);
                return r.json();
            });
        }

        _getStylesheet() {
            const styles = [];

            styles.push({
                selector: 'node',
                style: {
                    'width': 'mapData(degree, 0, 10, 20, 60)',
                    'height': 'mapData(degree, 0, 10, 20, 60)',
                    'background-color': 'data(color)',
                    'label': 'data(label)',
                    'color': '#d1d5db',
                    'font-size': '12px',
                    'font-family': '"Space Mono", monospace',
                    'font-weight': '400',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'text-outline-color': '#0a111a',
                    'text-outline-width': '3px',
                    'border-width': '2px',
                    'border-color': '#0df2f2',
                    'border-opacity': '0.3',
                    'overlay-color': '#0df2f2',
                    'overlay-padding': '0px',
                    'overlay-opacity': '0',
                    'transition-property': 'width, height, border-width, border-opacity, overlay-opacity, background-opacity',
                    'transition-duration': '0.3s',
                    'text-opacity': '0.7'
                }
            });

            styles.push({
                selector: 'node:selected',
                style: {
                    'border-width': '4px',
                    'border-color': '#0df2f2',
                    'border-opacity': '1',
                    'overlay-color': '#0df2f2',
                    'overlay-padding': '8px',
                    'overlay-opacity': '0.3',
                    'text-opacity': '1',
                    'font-size': '14px',
                    'font-weight': '700'
                }
            });

            styles.push({
                selector: 'node:hover',
                style: {
                    'border-width': '3px',
                    'border-color': '#0df2f2',
                    'border-opacity': '0.8',
                    'overlay-color': '#0df2f2',
                    'overlay-padding': '5px',
                    'overlay-opacity': '0.2',
                    'text-opacity': '1',
                    'font-size': '13px',
                    'font-weight': '600'
                }
            });

            styles.push({
                selector: 'node.faded',
                style: {
                    'opacity': '0.2',
                    'text-opacity': '0.1'
                }
            });

            styles.push({
                selector: 'edge',
                style: {
                    'width': '1px',
                    'line-color': '#0df2f2',
                    'line-opacity': '0.15',
                    'target-arrow-shape': 'none',
                    'target-arrow-color': '#0df2f2',
                    'curve-style': 'bezier',
                    'transition-property': 'width, line-opacity',
                    'transition-duration': '0.3s'
                }
            });

            styles.push({
                selector: 'edge:selected',
                style: {
                    'width': '3px',
                    'line-opacity': '0.9',
                    'line-style': 'dashed',
                    'line-dash-offset': 'data(offset)',
                    'line-dash-pattern': '8 12'
                }
            });

            styles.push({
                selector: 'edge:hover',
                style: {
                    'width': '2px',
                    'line-opacity': '0.6'
                }
            });

            styles.push({
                selector: 'edge.highlighted',
                style: {
                    'width': '2.5px',
                    'line-opacity': '0.8',
                    'line-color': '#0df2f2',
                    'source-arrow-shape': 'triangle',
                    'source-arrow-color': '#0df2f2',
                    'source-arrow-fill': 'filled',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': '#0df2f2',
                    'target-arrow-fill': 'filled'
                }
            });

            styles.push({
                selector: 'edge.faded',
                style: {
                    'opacity': '0.05'
                }
            });

            return styles;
        }

        _applyInitialZoom() {
            this.cy.ready(() => {
                this.cy.fit(undefined, 50);
                this.cy.animate({
                    zoom: this.cy.zoom() * 0.85,
                    center: { eles: this.cy.nodes() }
                }, {
                    duration: 800,
                    easing: 'ease-out-cubic'
                });
                this._initBackgroundEffect();
            });
        }

        _initBackgroundEffect() {
            this.bgCanvas = document.createElement('canvas');
            this.bgCanvas.style.position = 'absolute';
            this.bgCanvas.style.top = '0';
            this.bgCanvas.style.left = '0';
            this.bgCanvas.style.pointerEvents = 'none';
            this.bgCanvas.style.zIndex = '0';
            this.container.appendChild(this.bgCanvas);

            this.bgCtx = this.bgCanvas.getContext('2d');
            this._updateBackgroundSize();

            window.addEventListener('resize', () => this._updateBackgroundSize());
        }

        _updateBackgroundSize() {
            const rect = this.container.getBoundingClientRect();
            this.bgCanvas.width = rect.width;
            this.bgCanvas.height = rect.height;
        }

        _renderBackgroundEffect() {
            if (!this.bgCtx) return;

            const width = this.bgCanvas.width;
            const height = this.bgCanvas.height;
            const time = Date.now() / 1000;

            this.bgCtx.clearRect(0, 0, width, height);

            const gridSize = 50;
            const offsetX = (time * 20) % gridSize;
            const offsetY = (time * 10) % gridSize;

            this.bgCtx.strokeStyle = 'rgba(38, 166, 154, 0.08)';
            this.bgCtx.lineWidth = 0.5;

            for (let x = -gridSize + offsetX; x < width + gridSize; x += gridSize) {
                this.bgCtx.beginPath();
                this.bgCtx.moveTo(x, 0);
                this.bgCtx.lineTo(x, height);
                this.bgCtx.stroke();
            }

            for (let y = -gridSize + offsetY; y < height + gridSize; y += gridSize) {
                this.bgCtx.beginPath();
                this.bgCtx.moveTo(0, y);
                this.bgCtx.lineTo(width, y);
                this.bgCtx.stroke();
            }

            const numStars = 30;
            for (let i = 0; i < numStars; i++) {
                const x = (Math.sin(time * 0.1 + i * 123.456) * 0.5 + 0.5) * width;
                const y = (Math.cos(time * 0.15 + i * 789.012) * 0.5 + 0.5) * height;
                const radius = (Math.sin(time * 2 + i) * 0.5 + 0.5) * 2;
                const opacity = (Math.sin(time * 3 + i * 0.5) * 0.5 + 0.5) * 0.3;

                this.bgCtx.beginPath();
                this.bgCtx.arc(x, y, radius, 0, Math.PI * 2);
                this.bgCtx.fillStyle = `rgba(13, 242, 242, ${opacity})`;
                this.bgCtx.fill();
            }
        }

        _initParticles() {
            this.particles = [];
            const numParticles = Math.min(this.data.links.length, 100);

            for (let i = 0; i < numParticles; i++) {
                const linkIndex = Math.floor(Math.random() * this.data.links.length);
                const link = this.data.links[linkIndex];

                this.particles.push({
                    source: link.source.id,
                    target: link.target.id,
                    progress: Math.random(),
                    speed: 0.005 + Math.random() * 0.01,
                    size: 2 + Math.random() * 2,
                    opacity: 0.3 + Math.random() * 0.4
                });
            }
        }

        _updateParticles() {
            const canvas = this.container.querySelector('canvas');
            if (!canvas) return;

            const ctx = canvas.getContext('2d');
            if (!ctx) return;

            const width = canvas.width;
            const height = canvas.height;
            const pan = this.cy.pan();
            const zoom = this.cy.zoom();

            this.particles.forEach(particle => {
                particle.progress += particle.speed;
                if (particle.progress >= 1) {
                    particle.progress = 0;
                }

                const source = this.cy.getElementById(particle.source);
                const target = this.cy.getElementById(particle.target);

                if (source.length === 0 || target.length === 0) return;

                const sourcePos = source.position();
                const targetPos = target.position();

                const x = sourcePos.x + (targetPos.x - sourcePos.x) * particle.progress;
                const y = sourcePos.y + (targetPos.y - sourcePos.y) * particle.progress;

                const screenX = (x + pan.x) * zoom + width / 2;
                const screenY = (y + pan.y) * zoom + height / 2;

                if (screenX < 0 || screenX > width || screenY < 0 || screenY > height) return;

                ctx.beginPath();
                ctx.arc(screenX, screenY, particle.size * zoom, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(13, 242, 242, ${particle.opacity})`;
                ctx.fill();

                ctx.beginPath();
                ctx.arc(screenX, screenY, particle.size * 2 * zoom, 0, Math.PI * 2);
                const gradient = ctx.createRadialGradient(
                    screenX, screenY, 0,
                    screenX, screenY, particle.size * 4 * zoom
                );
                gradient.addColorStop(0, `rgba(13, 242, 242, ${particle.opacity * 0.3})`);
                gradient.addColorStop(1, 'rgba(13, 242, 242, 0)');
                ctx.fillStyle = gradient;
                ctx.fill();
            });
        }

        _initAnimations() {
            let offset = 0;
            const animate = () => {
                if (this.isDestroyed) return;
                offset -= 0.5;
                this.cy.edges(':selected').style('line-dash-offset', offset);
                if (this.hoveredNode || this.selectedNode) {
                    this._updateHighlights();
                }
                this._updateParticles();
                this._getNodePulse();
                this._renderBackgroundEffect();
                this.animationFrame = requestAnimationFrame(animate);
            };
            animate();
        }

        _updateHighlights() {
            const focus = this.hoveredNode || this.selectedNode;
            if (!focus) {
                this.cy.elements().removeClass('faded highlighted');
                return;
            }

            const neighborhood = focus.neighborhood().add(focus);
            const nonNeighborhood = this.cy.elements().not(neighborhood);

            nonNeighborhood.addClass('faded');
            neighborhood.removeClass('faded');

            neighborhood.connectedEdges().addClass('highlighted');
        }

        _getNodePulse() {
            const canvas = this.container.querySelector('canvas');
            if (!canvas) return;

            const ctx = canvas.getContext('2d');
            if (!ctx) return;

            const width = canvas.width;
            const height = canvas.height;
            const pan = this.cy.pan();
            const zoom = this.cy.zoom();
            const time = Date.now() / 1000;

            this.cy.nodes(':selected').forEach(node => {
                const pos = node.position();
                const screenX = (pos.x + pan.x) * zoom + width / 2;
                const screenY = (pos.y + pan.y) * zoom + height / 2;
                const baseRadius = node.width('px') / 2 * zoom;
                const pulseRadius = baseRadius + (Math.sin(time * 3) * 0.5 + 0.5) * 10 * zoom;

                if (screenX < 0 || screenX > width || screenY < 0 || screenY > height) return;

                ctx.beginPath();
                ctx.arc(screenX, screenY, pulseRadius, 0, Math.PI * 2);
                const gradient = ctx.createRadialGradient(
                    screenX, screenY, baseRadius,
                    screenX, screenY, pulseRadius
                );
                gradient.addColorStop(0, 'rgba(13, 242, 242, 0.4)');
                gradient.addColorStop(1, 'rgba(13, 242, 242, 0)');
                ctx.fillStyle = gradient;
                ctx.fill();
            });
        }

        _bindEvents() {
            this.cy.on('tap', 'node', (evt) => {
                const node = evt.target;
                this._selectNode(node);
            });

            this.cy.on('mouseover', 'node', (evt) => {
                const node = evt.target;
                this.hoveredNode = node;
                this._updateHighlights();
                this._emit('nodeHover', this._getNodeData(node));
            });

            this.cy.on('mouseout', 'node', () => {
                this.hoveredNode = null;
                this._updateHighlights();
                this._emit('nodeHover', null);
            });

            this.cy.on('tap', (evt) => {
                if (evt.target === this.cy) {
                    this._deselectNode();
                }
            });

            this.cy.on('dragfree', 'node', () => {
                this.cy.fit(undefined, 50);
            });
        }

        _selectNode(node) {
            this.selectedNode = node;
            this.cy.elements().unselect();
            node.select();
            this._updateHighlights();
            this._emit('nodeSelect', this._getNodeData(node));
        }

        _deselectNode() {
            this.selectedNode = null;
            this.cy.elements().unselect();
            this.cy.elements().removeClass('faded highlighted');
            this._emit('nodeSelect', null);
        }

        _getNodeData(node) {
            const data = node.data();
            return {
                id: data.id,
                name: data.label,
                layer: data.layer,
                layerName: data.layerName,
                level: data.level,
                color: data.color,
                category: data.category,
                description: data.description,
                connections: data.connections,
                degree: data.degree
            };
        }

        _emit(eventName, data) {
            const event = new CustomEvent(eventName, { detail: data });
            this.container.dispatchEvent(event);
        }

        zoomIn() {
            this.cy.animate({
                zoom: this.cy.zoom() * 1.3
            }, {
                duration: 300,
                easing: 'ease-out-cubic'
            });
        }

        zoomOut() {
            this.cy.animate({
                zoom: this.cy.zoom() * 0.7
            }, {
                duration: 300,
                easing: 'ease-out-cubic'
            });
        }

        resetView() {
            this.cy.fit(undefined, 50);
        }

        fitToScreen() {
            this.cy.fit(undefined, 30);
            this.cy.animate({
                zoom: this.cy.zoom() * 0.85
            }, {
                duration: 800,
                easing: 'ease-out-cubic'
            });
        }

        focusNode(nodeId) {
            const node = this.cy.getElementById(nodeId);
            if (node.length > 0) {
                this._selectNode(node);
                this.cy.animate({
                    center: { eles: node },
                    zoom: 2
                }, {
                    duration: 800,
                    easing: 'ease-out-cubic'
                });
            }
        }

        filterByLayer(layer) {
            Promise.resolve(this.toggleLayer(layer)).catch(() => {
            });
        }

        search(query) {
            this.searchQuery = query.toLowerCase();

            if (!query) {
                this.cy.nodes().removeClass('faded');
                return;
            }

            this.cy.nodes().forEach(node => {
                const label = (node.data('label') || '').toLowerCase();
                const description = (node.data('description') || '').toLowerCase();
                const layerName = (node.data('layerName') || '').toLowerCase();

                if (label.includes(query) ||
                    description.includes(query) ||
                    layerName.includes(query)) {
                    node.removeClass('faded');
                    node.animate({
                        style: { 'border-width': '3px', 'border-opacity': '0.8' }
                    }, { duration: 200 });
                } else {
                    node.addClass('faded');
                    node.style({ 'border-width': '2px', 'border-opacity': '0.3' });
                }
            });
        }

        destroy() {
            this.isDestroyed = true;
            if (this.animationFrame) {
                cancelAnimationFrame(this.animationFrame);
                this.animationFrame = null;
            }
            if (this.cy) {
                this.cy.destroy();
                this.cy = null;
            }
            this.hoveredNode = null;
            this.selectedNode = null;
            this.particles = [];
        }
    }

    global.CytoscapeGraphEngine = CytoscapeGraphEngine;

})(typeof window !== "undefined" ? window : this);
