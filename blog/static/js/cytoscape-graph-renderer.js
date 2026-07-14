/**
 * DOM workbench adapter for CytoscapeGraphEngine.
 * All data-derived content is written through textContent/createElement.
 */
(function (global) {
    "use strict";

    const MODE_LABELS = {
        overview: "总览",
        community: "社区",
        focus: "邻域"
    };

    const STAGE_LABELS = {
        overview: "OVERVIEW / CORE ONLY",
        community: "COMMUNITY / PULSE FIELD",
        focus: "FOCUS / 1-HOP NEIGHBORHOOD"
    };

    function setText(element, value, fallback = "—") {
        if (!element) return;
        const normalized = value === null || value === undefined || value === ""
            ? fallback
            : String(value);
        element.textContent = normalized;
    }

    function clearChildren(element) {
        if (!element) return;
        while (element.firstChild) element.removeChild(element.firstChild);
    }

    function formatMetric(value, fallback = "0") {
        const number = Number(value);
        if (!Number.isFinite(number)) return fallback;
        return new Intl.NumberFormat("zh-CN", { maximumFractionDigits: 2 }).format(number);
    }

    class CytoscapeGraphRenderer {
        constructor(engine) {
            if (!engine) throw new Error("Graph renderer requires an engine");
            this.engine = engine;
            this._listeners = [];
            this._searchTimer = null;
            this._searchSequence = 0;
            this._searchItems = [];
            this._activeSearchIndex = -1;
            this._active = false;
            this._busy = false;
            this._detailNode = null;

            this.elements = {
                workbench: global.document.getElementById("graph-workbench"),
                loading: global.document.getElementById("graph-loading"),
                error: global.document.getElementById("graph-error"),
                errorMessage: global.document.getElementById("graph-error-message"),
                liveState: global.document.getElementById("graph-live-state"),
                search: global.document.getElementById("graph-search"),
                searchResults: global.document.getElementById("graph-search-results"),
                searchStatus: global.document.getElementById("graph-search-status"),
                detail: global.document.getElementById("graph-detail"),
                detailClose: global.document.getElementById("graph-detail-close"),
                detailFocus: global.document.getElementById("detail-focus-node"),
                detailKicker: global.document.getElementById("detail-kicker"),
                detailCommunityStatus: global.document.getElementById("detail-community-status"),
                detailCommunityPulse: global.document.getElementById("detail-community-pulse"),
                detailCommunityInsights: global.document.getElementById("detail-community-insights"),
                detailCommunityMembers: global.document.getElementById("detail-community-members"),
                detailCommunityLinks: global.document.getElementById("detail-community-links"),
                detailCommunityMemberCount: global.document.getElementById("detail-community-member-count"),
                stageMode: global.document.getElementById("stage-mode-label"),
                capacity: global.document.getElementById("graph-capacity"),
                consoleScope: global.document.getElementById("console-scope"),
                zoomLevel: global.document.getElementById("graph-zoom-level"),
                stats: {
                    nodes: global.document.getElementById("stat-visible-nodes"),
                    edges: global.document.getElementById("stat-visible-edges"),
                    articles: global.document.getElementById("stat-total-articles"),
                    mode: global.document.getElementById("stat-mode"),
                    generatedAt: global.document.getElementById("stat-generated-at")
                },
                detailFields: {
                    name: global.document.getElementById("detail-name"),
                    id: global.document.getElementById("detail-id"),
                    layer: global.document.getElementById("detail-layer"),
                    category: global.document.getElementById("detail-category"),
                    description: global.document.getElementById("detail-description"),
                    articles: global.document.getElementById("detail-articles"),
                    degree: global.document.getElementById("detail-degree"),
                    weightedDegree: global.document.getElementById("detail-weighted-degree"),
                    rank: global.document.getElementById("detail-rank"),
                    community: global.document.getElementById("detail-community")
                },
                detailLabels: {
                    id: global.document.getElementById("detail-label-id"),
                    layer: global.document.getElementById("detail-label-layer"),
                    category: global.document.getElementById("detail-label-category"),
                    community: global.document.getElementById("detail-label-community"),
                    articles: global.document.getElementById("detail-label-articles"),
                    degree: global.document.getElementById("detail-label-degree"),
                    weightedDegree: global.document.getElementById("detail-label-weighted-degree"),
                    rank: global.document.getElementById("detail-label-rank")
                }
            };
            this.modeButtons = Array.from(global.document.querySelectorAll("[data-graph-mode]"));
            this.layerInputs = Array.from(global.document.querySelectorAll("[data-graph-layer]"));

            this.activate();
        }

        activate() {
            if (this._active) return this;
            this._active = true;
            this._bindToolbar();
            this._bindModes();
            this._bindLayers();
            this._bindSearch();
            this._bindDetail();
            this._bindEngineEvents();
            this._bindKeyboardShortcuts();

            Promise.resolve(this.engine.ready)
                .then(() => this._syncReadyState())
                .catch((error) => this._showError(error));
            return this;
        }

        _listen(target, type, handler, options) {
            if (!target?.addEventListener) return;
            target.addEventListener(type, handler, options);
            this._listeners.push({ target, type, handler, options });
        }

        _bindToolbar() {
            this._listen(global.document.getElementById("btn-zoom-in"), "click", () => {
                this.engine.zoomIn();
            });
            this._listen(global.document.getElementById("btn-zoom-out"), "click", () => {
                this.engine.zoomOut();
            });
            this._listen(global.document.getElementById("btn-fit"), "click", () => {
                this.engine.fitToScreen();
            });
            this._listen(global.document.getElementById("btn-reset"), "click", async () => {
                try {
                    await this.engine.resetView();
                    this._closeDetail();
                    this._clearSearch();
                } catch (error) {
                    this._showError(error);
                }
            });
        }

        _bindModes() {
            this.modeButtons.forEach((button) => {
                this._listen(button, "click", async () => {
                    if (this._busy) return;
                    const mode = button.dataset.graphMode;
                    if (!mode) return;
                    this._setBusy(true);
                    try {
                        await this.engine.setMode(mode);
                    } catch (error) {
                        this._showError(error);
                    } finally {
                        this._setBusy(false);
                    }
                });
            });
        }

        _bindLayers() {
            this.layerInputs.forEach((input) => {
                this._listen(input, "change", async () => {
                    const layer = input.dataset.graphLayer;
                    if (!layer) return;
                    input.disabled = true;
                    try {
                        const visible = await this.engine.toggleLayer(layer);
                        input.checked = visible;
                        this._updateStats();
                    } catch (error) {
                        input.checked = !input.checked;
                        this._showError(error);
                    } finally {
                        input.disabled = false;
                    }
                });
            });
        }

        _bindSearch() {
            const input = this.elements.search;
            if (!input) return;
            this._listen(input, "input", () => {
                if (this._searchTimer) global.clearTimeout(this._searchTimer);
                const query = input.value;
                if (!query.trim()) {
                    this._clearSearch(false);
                    this.engine.search("").catch(() => {});
                    return;
                }
                const sequence = ++this._searchSequence;
                setText(this.elements.searchStatus, "正在搜索…", "");
                this._searchTimer = global.setTimeout(async () => {
                    try {
                        const items = await this.engine.search(query);
                        if (sequence !== this._searchSequence) return;
                        this._renderSearchResults(items);
                    } catch (error) {
                        if (sequence !== this._searchSequence) return;
                        this._renderSearchResults([]);
                        this._showError(error);
                    }
                }, 100);
            });

            this._listen(input, "keydown", (event) => {
                if (event.key === "ArrowDown") {
                    event.preventDefault();
                    this._moveSearchSelection(1);
                } else if (event.key === "ArrowUp") {
                    event.preventDefault();
                    this._moveSearchSelection(-1);
                } else if (event.key === "Enter") {
                    if (this._searchItems.length === 0) return;
                    event.preventDefault();
                    const index = this._activeSearchIndex >= 0 ? this._activeSearchIndex : 0;
                    this._chooseSearchResult(this._searchItems[index]);
                } else if (event.key === "Escape") {
                    event.preventDefault();
                    this._clearSearch();
                    this.engine.clearSelection();
                }
            });
        }

        _bindDetail() {
            this._listen(this.elements.detailClose, "click", () => {
                this.engine.clearSelection();
                this._closeDetail();
            });
            this._listen(this.elements.detailFocus, "click", async () => {
                const nodeId = this.engine.selectedNodeId;
                if (!nodeId || this._busy) return;
                this._setBusy(true);
                try {
                    if (this._detailNode?.layer === "community") {
                        if (this.engine.expandedCommunityId === nodeId) this.engine.fitToScreen();
                        else await this.engine.expandCommunity(nodeId);
                    } else {
                        await this.engine.focusNode(nodeId);
                    }
                } catch (error) {
                    this._showError(error);
                } finally {
                    this._setBusy(false);
                }
            });
        }

        _bindEngineEvents() {
            const container = this.engine.container;
            this._listen(container, "graph:ready", (event) => this._syncReadyState(event.detail));
            this._listen(container, "graph:modechange", (event) => {
                const mode = event.detail?.mode || this.engine.mode;
                this._setActiveMode(mode);
                this._updateStats(event.detail);
                this._syncLayerInputs();
            });
            this._listen(container, "graph:selectionchange", (event) => {
                const node = event.detail?.node || null;
                if (node) this._openDetail(node);
                else this._closeDetail();
                this._syncFocusControls(Boolean(node));
                this._updateStats();
            });
            this._listen(container, "graph:layerchange", () => {
                this._syncLayerInputs();
                this._updateStats();
            });
            this._listen(container, "graph:viewportchange", (event) => {
                const zoom = Number(event.detail?.zoom);
                if (Number.isFinite(zoom)) {
                    setText(this.elements.zoomLevel, `${Math.round(zoom * 100)}%`);
                }
            });
            this._listen(container, "graph:error", (event) => {
                this._showError(event.detail?.message || "图谱操作失败");
            });
            this._listen(container, "graph:progress", (event) => {
                const progress = Number(event.detail?.progress);
                if (Number.isFinite(progress)) {
                    setText(this.elements.liveState, `同步 ${Math.max(0, Math.min(100, progress))}%`);
                }
            });
        }

        _bindKeyboardShortcuts() {
            this._listen(global.document, "keydown", (event) => {
                if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
                    event.preventDefault();
                    this.elements.search?.focus();
                    this.elements.search?.select();
                    return;
                }
                if (event.key === "Escape" && global.document.activeElement !== this.elements.search) {
                    this.engine.clearSelection();
                    this._closeDetail();
                }
            });
        }

        _renderSearchResults(items) {
            const list = this.elements.searchResults;
            if (!list) return;
            clearChildren(list);
            this._searchItems = Array.isArray(items) ? items.slice(0, 10) : [];
            this._activeSearchIndex = -1;

            this._searchItems.forEach((item, index) => {
                const option = global.document.createElement("li");
                option.id = `graph-search-option-${index}`;
                option.setAttribute("role", "option");
                option.setAttribute("aria-selected", "false");

                const button = global.document.createElement("button");
                button.type = "button";
                button.className = "graph-search-result";
                const title = global.document.createElement("span");
                title.className = "graph-search-result__name";
                title.textContent = String(item.name || item.id || "未知节点");
                const meta = global.document.createElement("span");
                meta.className = "graph-search-result__meta";
                const rank = Number(item.rank) > 0 ? ` · #${item.rank}` : "";
                meta.textContent = `${item.layer || "node"}${rank}`;
                button.append(title, meta);
                this._listen(button, "click", () => this._chooseSearchResult(item));
                option.appendChild(button);
                list.appendChild(option);
            });

            const hasResults = this._searchItems.length > 0;
            list.hidden = !hasResults;
            this.elements.search?.setAttribute("aria-expanded", String(hasResults));
            setText(
                this.elements.searchStatus,
                hasResults ? `找到 ${this._searchItems.length} 个结果` : "未找到匹配节点",
                ""
            );
        }

        _moveSearchSelection(delta) {
            if (this._searchItems.length === 0) return;
            const length = this._searchItems.length;
            this._activeSearchIndex = (this._activeSearchIndex + delta + length) % length;
            const options = Array.from(this.elements.searchResults?.querySelectorAll("[role='option']") || []);
            options.forEach((option, index) => {
                const active = index === this._activeSearchIndex;
                option.setAttribute("aria-selected", String(active));
                option.classList.toggle("is-active", active);
                if (active) option.scrollIntoView({ block: "nearest" });
            });
            const active = options[this._activeSearchIndex];
            if (active) this.elements.search?.setAttribute("aria-activedescendant", active.id);
        }

        async _chooseSearchResult(item) {
            if (!item?.id || this._busy) return;
            this._setBusy(true);
            this._hideSearchResults();
            try {
                await this.engine.focusNode(item.id);
            } catch (error) {
                this._showError(error);
            } finally {
                this._setBusy(false);
            }
        }

        _hideSearchResults() {
            if (this.elements.searchResults) this.elements.searchResults.hidden = true;
            this.elements.search?.setAttribute("aria-expanded", "false");
            this.elements.search?.removeAttribute("aria-activedescendant");
            this._activeSearchIndex = -1;
        }

        _clearSearch(clearInput = true) {
            this._searchSequence += 1;
            if (this._searchTimer) {
                global.clearTimeout(this._searchTimer);
                this._searchTimer = null;
            }
            if (clearInput && this.elements.search) this.elements.search.value = "";
            clearChildren(this.elements.searchResults);
            this._searchItems = [];
            this._hideSearchResults();
            setText(this.elements.searchStatus, "", "");
        }

        _openDetail(node) {
            const fields = this.elements.detailFields;
            const labels = this.elements.detailLabels;
            const isCommunity = node.layer === "community";
            const insight = isCommunity
                ? this.engine.getCommunityInsights(node.id)
                : null;
            this._detailNode = node;
            setText(fields.name, node.name || node.id);
            setText(fields.id, node.id);
            setText(fields.layer, isCommunity ? "标签社区" : (node.layerName || node.layer));
            setText(fields.category, isCommunity ? "聚合社区" : (node.category || "general"));
            setText(
                fields.description,
                node.description || (isCommunity
                    ? `${node.name || "当前"}社区汇聚 ${formatMetric(insight.memberCount)} 个标签热点，按真实关联强度展示与相邻社区的共现流。`
                    : "该节点暂无摘要。"),
                "该节点暂无摘要。"
            );
            setText(
                fields.degree,
                formatMetric(isCommunity
                    ? (node.node_count ?? insight.memberCount ?? node.degree)
                    : (node.degree ?? node.connections))
            );
            setText(
                fields.articles,
                formatMetric(isCommunity
                    ? insight.topMembers.length
                    : (node.article_count ?? node.articles))
            );
            setText(
                fields.weightedDegree,
                formatMetric(isCommunity
                    ? insight.connectionStrength
                    : node.weighted_degree)
            );
            setText(fields.rank, Number(node.rank) > 0 ? `#${node.rank}` : "—");
            setText(fields.community, isCommunity ? node.id : (node.community_id ?? node.community ?? "—"));
            setText(this.elements.detailKicker, isCommunity ? "COMMUNITY INTELLIGENCE" : "NODE INTELLIGENCE");
            setText(labels.id, isCommunity ? "社区 ID" : "ID");
            setText(labels.layer, "图层");
            setText(labels.category, "类别");
            setText(labels.community, isCommunity ? "社区标识" : "社区");
            setText(labels.articles, isCommunity ? "核心节点" : "文章");
            setText(labels.degree, isCommunity ? "节点数量" : "连接");
            setText(labels.weightedDegree, isCommunity ? "连接强度" : "加权度");
            setText(labels.rank, isCommunity ? "社区排名" : "排名");
            if (this.elements.detailCommunityStatus) {
                this.elements.detailCommunityStatus.hidden = !isCommunity;
                setText(
                    this.elements.detailCommunityStatus,
                    isCommunity && Number(node.rank) > 0
                        ? String(Number(node.rank)).padStart(2, "0")
                        : "—"
                );
            }
            if (this.elements.detailCommunityPulse) {
                this.elements.detailCommunityPulse.hidden = !isCommunity;
                const state = this.elements.detailCommunityPulse.querySelector("strong");
                setText(
                    state,
                    isCommunity && this.engine.expandedCommunityId === node.id
                        ? "活跃 · 已展开"
                        : "活跃 · 聚合态"
                );
            }
            if (this.elements.detailCommunityInsights) {
                this.elements.detailCommunityInsights.hidden = !isCommunity;
            }
            if (isCommunity) this._renderCommunityInsights(insight);
            else {
                clearChildren(this.elements.detailCommunityMembers);
                clearChildren(this.elements.detailCommunityLinks);
            }
            setText(
                this.elements.detailFocus,
                isCommunity
                    ? (this.engine.expandedCommunityId === node.id ? "适配社区势场" : "展开中心热点")
                    : "进入节点邻域"
            );

            const panel = this.elements.detail;
            if (!panel) return;
            panel.dataset.detailKind = isCommunity ? "community" : "node";
            panel.classList.toggle("is-community", isCommunity);
            this.elements.workbench?.classList.add("has-detail");
            panel.hidden = false;
            panel.setAttribute("aria-hidden", "false");
            panel.classList.remove("animate__fadeOutRight");
            panel.classList.add("animate__fadeInRight", "is-open");
        }

        _renderCommunityInsights(insight) {
            const members = this.elements.detailCommunityMembers;
            const links = this.elements.detailCommunityLinks;
            clearChildren(members);
            clearChildren(links);
            setText(
                this.elements.detailCommunityMemberCount,
                `${formatMetric(insight?.memberCount)} 节点`
            );

            (insight?.topMembers || []).slice(0, 6).forEach((member) => {
                const item = global.document.createElement("li");
                const rank = global.document.createElement("span");
                rank.className = "detail-intel-list__rank";
                rank.setAttribute("aria-hidden", "true");
                const name = global.document.createElement("strong");
                name.textContent = String(member.name || member.id || "未知热点");
                const metric = global.document.createElement("span");
                metric.className = "detail-intel-list__metric";
                const score = member.weightedDegree || member.degree || member.articleCount || 0;
                metric.textContent = score > 0 ? formatMetric(score) : "热点";
                item.append(rank, name, metric);
                members?.appendChild(item);
            });

            (insight?.relatedCommunities || []).slice(0, 4).forEach((related) => {
                const item = global.document.createElement("li");
                const arrow = global.document.createElement("img");
                arrow.className = "detail-intel-list__arrow";
                arrow.src = String(links?.dataset.arrowIcon || "/vendor/material-symbols/arrow-forward.svg");
                arrow.alt = "";
                arrow.width = 16;
                arrow.height = 16;
                const name = global.document.createElement("strong");
                name.textContent = String(related.name || related.id || "关联社区");
                const metric = global.document.createElement("span");
                metric.className = "detail-intel-list__metric";
                metric.textContent = formatMetric(related.weight);
                item.append(arrow, name, metric);
                links?.appendChild(item);
            });
        }

        _closeDetail() {
            this._detailNode = null;
            this.elements.workbench?.classList.remove("has-detail");
            const panel = this.elements.detail;
            if (!panel) return;
            panel.classList.remove("animate__fadeInRight", "is-open");
            panel.setAttribute("aria-hidden", "true");
            panel.hidden = true;
        }

        _setBusy(busy) {
            this._busy = Boolean(busy);
            this.modeButtons.forEach((button) => {
                button.disabled = this._busy;
            });
            if (this.elements.detailFocus) {
                this.elements.detailFocus.disabled = this._busy || !this.engine.selectedNodeId;
            }
            setText(this.elements.liveState, this._busy ? "计算中" : "在线");
        }

        _setActiveMode(mode) {
            this.modeButtons.forEach((button) => {
                const active = button.dataset.graphMode === mode;
                button.classList.toggle("is-active", active);
                button.setAttribute("aria-pressed", String(active));
            });
            setText(this.elements.stats.mode, MODE_LABELS[mode] || mode);
            setText(this.elements.stageMode, STAGE_LABELS[mode] || String(mode).toUpperCase());
            this.elements.workbench?.classList.remove(
                "is-mode-overview",
                "is-mode-community",
                "is-mode-focus"
            );
            this.elements.workbench?.classList.add(`is-mode-${mode}`);
        }

        _syncFocusControls(hasSelection) {
            const focusButton = this.modeButtons.find((button) => button.dataset.graphMode === "focus");
            if (focusButton) focusButton.disabled = this._busy;
            if (this.elements.detailFocus) this.elements.detailFocus.disabled = this._busy || !hasSelection;
        }

        _syncLayerInputs() {
            this.layerInputs.forEach((input) => {
                input.checked = this.engine.visibleLayers.has(input.dataset.graphLayer);
            });
        }

        _syncReadyState() {
            if (!this.engine?.cy || this.engine.isDestroyed) return;
            if (this.elements.loading) this.elements.loading.hidden = true;
            if (this.elements.error) this.elements.error.hidden = true;
            setText(this.elements.liveState, "在线");
            this._setActiveMode(this.engine.mode || "overview");
            this._syncLayerInputs();
            this._syncFocusControls(Boolean(this.engine.selectedNodeId));
            setText(this.elements.zoomLevel, `${Math.round((this.engine.cy?.zoom?.() || 1) * 100)}%`);
            this._updateStats();
        }

        _updateStats(detail = {}) {
            const visibleNodes = detail.visibleNodes ?? this.engine.cy?.nodes(":visible")?.length ?? 0;
            const visibleEdges = detail.visibleEdges ?? this.engine.cy?.edges(":visible")?.length ?? 0;
            const stats = this.engine.data?.stats || {};
            const totalArticles = stats.total_articles ?? stats.tag_stats?.total_articles ?? 0;
            setText(this.elements.stats.nodes, formatMetric(visibleNodes));
            setText(this.elements.stats.edges, formatMetric(visibleEdges));
            setText(this.elements.stats.articles, formatMetric(totalArticles));
            setText(this.elements.stats.mode, MODE_LABELS[this.engine.mode] || this.engine.mode);
            setText(this.elements.stats.generatedAt, this._formatGeneratedAt(this.engine.data?.generated_at));
            setText(
                this.elements.capacity,
                `${MODE_LABELS[this.engine.mode] || "当前"}预算：${visibleNodes} 节点 / ${visibleEdges} 连线`
            );
            setText(
                this.elements.consoleScope,
                `${MODE_LABELS[this.engine.mode] || "当前"}范围：${visibleNodes} 节点 / ${visibleEdges} 连线`
            );
        }

        _formatGeneratedAt(value) {
            if (!value) return "—";
            const date = new Date(value);
            if (Number.isNaN(date.getTime())) return String(value);
            return new Intl.DateTimeFormat("zh-CN", {
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                hour12: false
            }).format(date);
        }

        _showError(error) {
            const message = error?.message || String(error || "图谱操作失败");
            setText(this.elements.errorMessage, message);
            if (this.elements.error) this.elements.error.hidden = false;
            setText(this.elements.liveState, "连接失败");
        }

        destroy() {
            if (!this._active) return;
            this._active = false;
            this._searchSequence += 1;
            if (this._searchTimer) global.clearTimeout(this._searchTimer);
            this._searchTimer = null;
            this._listeners.forEach(({ target, type, handler, options }) => {
                target.removeEventListener?.(type, handler, options);
            });
            this._listeners = [];
            this._searchItems = [];
            this.elements.workbench?.classList.remove("has-detail");
            this.engine = null;
        }
    }

    global.CytoscapeGraphRenderer = CytoscapeGraphRenderer;
})(typeof window !== "undefined" ? window : this);
