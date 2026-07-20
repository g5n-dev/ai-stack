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
            this._intelligenceSequence = 0;
            this._intelligenceAbort = null;
            this._busyFocusOrigin = null;

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
                detailNodeIntelligence: global.document.getElementById("detail-node-intelligence"),
                detailIntelligenceStatus: global.document.getElementById("detail-intelligence-status"),
                detailIntelligenceList: global.document.getElementById("detail-intelligence-list"),
                detailTrendLink: global.document.getElementById("detail-trend-link"),
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
                    this._syncModeUrl("overview");
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
                        if (mode === "focus" && this.engine.selectedNodeId) {
                            this._syncFocusUrl(this.engine.selectedNodeId);
                        } else {
                            this._syncModeUrl(mode);
                        }
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
                const nodeId = this._detailNode?.id || this.engine.selectedNodeId;
                if (!nodeId || this._busy) return;
                this._setBusy(true, "正在加载节点邻域…");
                let failure = null;
                try {
                    if (this._detailNode?.layer === "community") {
                        if (this.engine.expandedCommunityId === nodeId) this.engine.fitToScreen();
                        else await this.engine.expandCommunity(nodeId);
                    } else if (
                        this.engine.mode === "focus" &&
                        this._detailNode?.focusSceneRole === "core"
                    ) {
                        this._syncFocusUrl(nodeId);
                        this._closeDetail();
                    } else {
                        const focus = global.AIStackGraphWorkbench?.focusSelectedNode;
                        if (typeof focus === "function") await focus(this.engine, nodeId);
                        else await this.engine.focusNode(nodeId);
                        this._setActiveMode("focus");
                        this._syncFocusUrl(nodeId);
                        this._closeDetail();
                    }
                } catch (error) {
                    failure = error;
                } finally {
                    this._setBusy(false);
                }
                if (failure) this._showError(failure);
                else if (this.engine.mode === "focus") {
                    setText(this.elements.liveState, "节点邻域已就绪");
                    this._focusGraphStage();
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
            this._listen(container, "graph:layerchange", (event) => {
                this._syncLayerInputs();
                this._updateStats(event.detail);
            });
            this._listen(container, "graph:viewportchange", (event) => {
                const zoom = Number(event.detail?.zoom);
                if (Number.isFinite(zoom)) {
                    setText(this.elements.zoomLevel, `${Math.round(zoom * 100)}%`);
                }
                if (event.detail?.reason !== "zoom") {
                    this._updateStats(event.detail || {});
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
                this._setActiveMode("focus");
                this._syncFocusUrl(item.id);
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
                this._detailFocusLabel(node, isCommunity)
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
            this._loadNodeIntelligence(node);
        }

        _detailFocusLabel(node, isCommunity = node?.layer === "community") {
            if (isCommunity) {
                return this.engine.expandedCommunityId === node?.id
                    ? "适配社区势场"
                    : "展开中心热点";
            }
            if (this.engine.mode !== "focus") return "进入节点邻域";
            return node?.focusSceneRole === "core"
                ? "收起详情，查看完整邻域"
                : "以此节点重新聚焦";
        }

        _syncFocusUrl(nodeId) {
            try {
                const builder = global.AIStackGraphWorkbench?.focusRequestUrl;
                const next = typeof builder === "function"
                    ? builder(global.location.href, nodeId)
                    : null;
                if (next) global.history?.replaceState?.(global.history.state, "", next);
            } catch (error) {
                global.console?.warn?.("Unable to persist graph focus URL", error);
            }
        }

        _syncModeUrl(mode) {
            try {
                const builder = global.AIStackGraphWorkbench?.modeRequestUrl;
                const next = typeof builder === "function"
                    ? builder(global.location.href, mode)
                    : null;
                if (next) global.history?.replaceState?.(global.history.state, "", next);
            } catch (error) {
                global.console?.warn?.("Unable to persist graph mode URL", error);
            }
        }

        _loadNodeIntelligence(node) {
            const section = this.elements.detailNodeIntelligence;
            const list = this.elements.detailIntelligenceList;
            const loader = global.AIStackGraphIntelligence?.loadNodeIntelligence;
            this._intelligenceSequence += 1;
            const sequence = this._intelligenceSequence;
            this._intelligenceAbort?.abort?.();
            this._intelligenceAbort = null;
            clearChildren(list);
            if (!section || node?.layer === "community" || !String(node?.id || "").startsWith("tag:")) {
                if (section) section.hidden = true;
                return;
            }
            section.hidden = false;
            setText(this.elements.detailIntelligenceStatus, "正在载入关联情报…");
            if (typeof loader !== "function") {
                setText(this.elements.detailIntelligenceStatus, "关联情报组件暂不可用。");
                return;
            }
            const Controller = global.AbortController;
            const controller = typeof Controller === "function" ? new Controller() : null;
            this._intelligenceAbort = controller;
            Promise.resolve(loader({
                indexUrl: this.elements.workbench?.dataset.trendsIndexUrl,
                nodeId: node.id,
                baseUrl: global.location?.href,
                fetchFn: global.fetch?.bind(global),
                signal: controller?.signal
            })).then((payload) => {
                if (sequence !== this._intelligenceSequence || controller?.signal.aborted) return;
                this._renderNodeIntelligence(payload);
            }).catch((error) => {
                if (sequence !== this._intelligenceSequence || error?.name === "AbortError") return;
                setText(this.elements.detailIntelligenceStatus, "暂无可核验的关联情报，图谱浏览不受影响。");
            });
        }

        _renderNodeIntelligence(payload) {
            const list = this.elements.detailIntelligenceList;
            clearChildren(list);
            const articles = Array.isArray(payload?.articles) ? payload.articles.slice(0, 6) : [];
            articles.forEach((article) => {
                const item = global.document.createElement("li");
                const link = global.document.createElement("a");
                link.className = "detail-article-link";
                link.href = String(article.article_url || "");
                const title = global.document.createElement("strong");
                title.textContent = String(article.title || "未命名情报");
                const meta = global.document.createElement("span");
                meta.textContent = `${article.source || "来源待核验"} · ${article.associated_observations || 1} 条观测`;
                link.append(title, meta);
                const lineage = global.document.createElement("a");
                lineage.className = "detail-article-lineage";
                lineage.href = String(article.lineage_url || article.article_url || "");
                lineage.textContent = "查看溯源";
                item.append(link, lineage);
                list?.appendChild(item);
            });
            setText(
                this.elements.detailIntelligenceStatus,
                articles.length ? `已载入 ${articles.length} 条关联情报` : "该节点暂无可核验的关联情报。"
            );
            if (this.elements.detailTrendLink && payload?.trend_url) {
                this.elements.detailTrendLink.href = String(payload.trend_url);
            }
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
            this._intelligenceSequence += 1;
            this._intelligenceAbort?.abort?.();
            this._intelligenceAbort = null;
            this._detailNode = null;
            this.elements.workbench?.classList.remove("has-detail");
            const panel = this.elements.detail;
            if (!panel) return;
            panel.classList.remove("animate__fadeInRight", "is-open");
            panel.setAttribute("aria-hidden", "true");
            panel.hidden = true;
        }

        _focusGraphStage() {
            const stage = this.engine?.container;
            if (typeof stage?.focus !== "function") return;
            try {
                stage.focus({ preventScroll: true });
            } catch (_error) {
                stage.focus();
            }
        }

        _setBusy(busy, message = "计算中") {
            if (busy && !this._busy) {
                const active = global.document?.activeElement;
                this._busyFocusOrigin = this.modeButtons.includes(active) ? active : null;
            }
            this._busy = Boolean(busy);
            this.modeButtons.forEach((button) => {
                button.disabled = this._busy;
            });
            if (this.elements.detailFocus) {
                this.elements.detailFocus.disabled = this._busy || !this.engine.selectedNodeId;
            }
            if (this._busy) setText(this.elements.liveState, message);
            else {
                if (this.elements.liveState?.textContent !== "连接失败") setText(this.elements.liveState, "在线");
                const origin = this._busyFocusOrigin;
                this._busyFocusOrigin = null;
                if (origin && !origin.disabled && typeof origin.focus === "function") {
                    origin.focus({ preventScroll: true });
                }
            }
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
            const hasVisibleSnapshot = detail.visibleNodes !== undefined && detail.visibleEdges !== undefined;
            const visible = hasVisibleSnapshot
                ? {}
                : this.engine.getVisibleCounts?.() || {};
            const visibleNodes = detail.visibleNodes ?? visible.nodes ?? this.engine.cy?.nodes(":visible")?.length ?? 0;
            const visibleEdges = detail.visibleEdges ?? visible.edges ?? this.engine.cy?.edges(":visible")?.length ?? 0;
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
            this._intelligenceSequence += 1;
            this._intelligenceAbort?.abort?.();
            this._intelligenceAbort = null;
            this.elements.workbench?.classList.remove("has-detail");
            this.engine = null;
        }
    }

    global.CytoscapeGraphRenderer = CytoscapeGraphRenderer;
})(typeof window !== "undefined" ? window : this);
