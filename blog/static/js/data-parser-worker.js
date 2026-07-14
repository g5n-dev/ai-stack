"use strict";

/*
 * Persistent knowledge-graph data worker.
 *
 * Request:  { id, type: bootstrap|search|community|focus|cancel, payload }
 * Response: { id, type: success|error|cancelled, operation, data? }
 *
 * bootstrap intentionally loads only index.json and core.json. Larger files are
 * fetched lazily by the operation that needs them and then kept in this worker.
 */

const SEARCH_LIMIT = 10;
const COMMUNITY_LIMIT = 24;
const FOCUS_NEIGHBOR_LIMIT = 24;
const FOCUS_EDGE_LIMIT = 80;
const FOCUS_SHARD_COUNT = 128;
const FOCUS_SHARD_ALGORITHM = "fnv1a32";
const SEARCH_TERMS = Symbol("searchTerms");

const state = {
    index: null,
    indexUrl: "",
    baseUrl: "",
    version: 1,
    epoch: 0,
    files: {},
    core: { nodes: [], links: [] },
    cache: new Map(),
    controllers: new Map(),
    cancelled: new Set(),
    searchItems: null,
    searchById: null,
    searchLoadPromise: null,
    focusShards: new Map(),
    communityGraph: null,
    communityHotspots: null,
    hotGraph: null,
    fullGraph: null
};

class CancelledRequestError extends Error {
    constructor() {
        super("Request cancelled");
        this.name = "CancelledRequestError";
    }
}

class HttpRequestError extends Error {
    constructor(status, url) {
        super(`HTTP ${status}: ${url}`);
        this.name = "HttpRequestError";
        this.status = status;
        this.url = url;
    }
}

function asArray(value) {
    return Array.isArray(value) ? value : [];
}

function asNumber(value, fallback = 0) {
    const number = Number(value);
    return Number.isFinite(number) ? number : fallback;
}

function clampLimit(value, maximum, fallback = maximum) {
    const number = Math.floor(asNumber(value, fallback));
    return Math.max(0, Math.min(maximum, number));
}

function endpointId(endpoint) {
    if (endpoint && typeof endpoint === "object") {
        return String(endpoint.id || endpoint.data?.id || "");
    }
    return endpoint == null ? "" : String(endpoint);
}

function normalizeNode(node) {
    if (!node || node.id == null) return null;
    const id = String(node.id);
    return {
        ...node,
        id,
        name: String(node.name || node.label || node.title || node.legacy_id || id),
        degree: asNumber(node.degree ?? node.connections ?? node.related_count, 0),
        weighted_degree: asNumber(node.weighted_degree ?? node.weightedDegree, 0),
        rank: asNumber(node.rank ?? node.pagerank ?? node.score, 0),
        article_count: asNumber(node.article_count ?? node.articleCount, 0)
    };
}

function normalizeLink(link, index = 0) {
    if (!link) return null;
    const source = endpointId(link.source);
    const target = endpointId(link.target);
    if (!source || !target) return null;
    const weight = asNumber(link.weight ?? link.strength ?? link.value, 1);
    return {
        ...link,
        id: String(link.id || `edge:${source}:${target}:${index}`),
        source,
        target,
        weight,
        strength: asNumber(link.strength ?? weight, weight)
    };
}

function normalizeGraph(payload) {
    const source = payload?.graph && typeof payload.graph === "object"
        ? payload.graph
        : (payload || {});
    const rawNodes = asArray(source.nodes).length > 0
        ? source.nodes
        : asArray(source.items);
    const rawLinks = asArray(source.links).length > 0
        ? source.links
        : asArray(source.edges);
    return {
        nodes: rawNodes.map(normalizeNode).filter(Boolean),
        links: rawLinks.map(normalizeLink).filter(Boolean),
        layers: source.layers || payload?.layers || {},
        stats: source.stats || payload?.stats || {}
    };
}

function mergeGraphs(graphs) {
    const nodes = new Map();
    const links = new Map();
    const layers = {};
    const stats = {};

    for (const graph of graphs.filter(Boolean)) {
        for (const node of asArray(graph.nodes)) {
            const normalized = normalizeNode(node);
            if (!normalized) continue;
            nodes.set(normalized.id, { ...(nodes.get(normalized.id) || {}), ...normalized });
        }
        asArray(graph.links).forEach((link, index) => {
            const normalized = normalizeLink(link, index);
            if (!normalized) return;
            const canonicalKey = normalized.id || `${normalized.source}:${normalized.target}`;
            links.set(canonicalKey, normalized);
        });
        Object.assign(layers, graph.layers || {});
        Object.assign(stats, graph.stats || {});
    }

    return {
        nodes: Array.from(nodes.values()),
        links: Array.from(links.values()),
        layers,
        stats
    };
}

function compareNodes(left, right) {
    const leftRank = asNumber(left.rank, 0) > 0 ? asNumber(left.rank) : Number.POSITIVE_INFINITY;
    const rightRank = asNumber(right.rank, 0) > 0 ? asNumber(right.rank) : Number.POSITIVE_INFINITY;
    if (leftRank !== rightRank) return leftRank - rightRank;
    const weightedDifference = asNumber(right.weighted_degree) - asNumber(left.weighted_degree);
    if (weightedDifference !== 0) return weightedDifference;
    const articleDifference = asNumber(right.article_count) - asNumber(left.article_count);
    if (articleDifference !== 0) return articleDifference;
    const degreeDifference = asNumber(right.degree ?? right.size ?? right.member_count) -
        asNumber(left.degree ?? left.size ?? left.member_count);
    if (degreeDifference !== 0) return degreeDifference;
    return String(left.name || left.id).localeCompare(String(right.name || right.id));
}

function compareLinks(left, right) {
    return asNumber(right.weight ?? right.strength, 1) - asNumber(left.weight ?? left.strength, 1);
}

function resolveUrl(file) {
    if (!file) return "";
    const value = String(file);
    if (/^(?:https?:)?\/\//i.test(value) || value.startsWith("/")) return value;
    if (state.baseUrl) {
        const base = state.baseUrl.endsWith("/") ? state.baseUrl : `${state.baseUrl}/`;
        return `${base}${value}`;
    }
    const slash = state.indexUrl.lastIndexOf("/");
    return slash >= 0 ? `${state.indexUrl.slice(0, slash + 1)}${value}` : value;
}

function fileFor(role) {
    const files = state.files || {};
    const v2Files = files.v2 || state.index?.v2?.files || {};
    const candidates = {
        core: [v2Files.core, files.coreV2, files.core_v2, files.core],
        search: [v2Files.search, files.searchV2, files.search_v2, files.search],
        community: [v2Files.community, v2Files.communities, files.communityV2,
            files.community_v2, files.community, files.communities],
        communityHotspots: [v2Files.communityHotspots, v2Files.community_hotspots,
            files.communityHotspotsV2, files.community_hotspots_v2,
            files.communityHotspots, files.community_hotspots],
        tagHot: [v2Files.tagHot, files.tagHot, files.tag_hot],
        conceptHot: [v2Files.conceptHot, files.conceptHot, files.concept_hot],
        tag: [v2Files.tag, files.tag]
    };
    return (candidates[role] || []).find(Boolean) || "";
}

function focusShardManifest() {
    const files = state.files || {};
    const v2Files = files.v2 || state.index?.v2?.files || {};
    const manifest = v2Files.focusShards ?? v2Files.focus_shards ??
        files.focusShards ?? files.focus_shards;
    return manifest == null ? null : manifest;
}

function fnv1a32(value) {
    let hash = 0x811c9dc5;
    const bytes = new TextEncoder().encode(String(value));
    for (const byte of bytes) {
        hash ^= byte;
        hash = Math.imul(hash, 0x01000193) >>> 0;
    }
    return hash >>> 0;
}

function focusBucket(nodeId) {
    return fnv1a32(nodeId) % FOCUS_SHARD_COUNT;
}

function post(id, type, operation, extra = {}) {
    self.postMessage({ id, type, operation, ...extra });
}

function assertActive(id) {
    if (state.cancelled.has(id)) throw new CancelledRequestError();
}

async function fetchJson(url, id, operation) {
    if (!url) throw new Error(`Missing data file for ${operation}`);
    if (state.cache.has(url)) return state.cache.get(url);

    assertActive(id);
    const controller = state.controllers.get(id);
    const response = await fetch(url, controller ? { signal: controller.signal } : undefined);
    if (!response.ok) throw new HttpRequestError(response.status, url);

    const contentLength = asNumber(response.headers?.get?.("Content-Length"), 0);
    let data;

    if (response.body?.getReader) {
        const reader = response.body.getReader();
        const chunks = [];
        let receivedLength = 0;

        while (true) {
            assertActive(id);
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            receivedLength += value.length;
            if (contentLength > 0) {
                post(id, "progress", operation, {
                    progress: Math.min(100, Math.round(receivedLength / contentLength * 100)),
                    url
                });
            }
        }

        const merged = new Uint8Array(receivedLength);
        let offset = 0;
        for (const chunk of chunks) {
            merged.set(chunk, offset);
            offset += chunk.length;
        }
        post(id, "parsing", operation, { url });
        data = JSON.parse(new TextDecoder("utf-8").decode(merged));
    } else {
        data = await response.json();
    }

    assertActive(id);
    state.cache.set(url, data);
    return data;
}

async function loadGraphFile(role, id, operation) {
    const file = fileFor(role);
    if (!file) return { nodes: [], links: [], layers: {}, stats: {} };
    return normalizeGraph(await fetchJson(resolveUrl(file), id, operation));
}

function communityPayloadToGraph(payload) {
    if (asArray(payload?.communities).length === 0) return normalizeGraph(payload);

    const nodes = payload.communities.map((community, index) => normalizeNode({
        ...community,
        id: community.id || community.community_id || `community:${index}`,
        name: community.name || community.label || community.title ||
            asArray(community.top_terms || community.tags).slice(0, 3).join(" · ") ||
            `Community ${index + 1}`,
        layer: community.layer || "community",
        degree: community.degree ?? community.node_count ?? community.size ?? community.member_count,
        rank: community.rank ?? community.score ?? community.weighted_degree,
        member_ids: community.member_ids || community.members || community.node_ids || community.nodes || [],
        graph_role: community.graph_role || "community-context"
    })).filter(Boolean);
    const links = asArray(payload.links).length > 0 ? payload.links : payload.edges;
    return normalizeGraph({ nodes, links, layers: payload.layers, stats: payload.stats });
}

function visibleCommunityLimit() {
    return Math.max(1, Math.min(
        COMMUNITY_LIMIT,
        asNumber(state.index?.defaults?.community_limit, 11)
    ));
}

function visibleCommunityGraph() {
    const source = state.communityGraph || { nodes: [], links: [], layers: {}, stats: {} };
    const nodes = [...asArray(source.nodes)]
        .filter((node) => node.id !== "community:other")
        .sort(compareNodes)
        .slice(0, visibleCommunityLimit())
        .map((node) => ({ ...node, graph_role: "community-context" }));
    const nodeIds = new Set(nodes.map((node) => node.id));
    const links = asArray(source.links)
        .filter((link) => nodeIds.has(endpointId(link.source)) && nodeIds.has(endpointId(link.target)))
        .sort(compareLinks)
        .map((link) => ({ ...link, type: "community", graph_role: "community-route" }));
    return { ...source, nodes, links };
}

async function bootstrap(id, payload) {
    const epoch = ++state.epoch;
    for (const [requestId, controller] of state.controllers) {
        if (requestId === id) continue;
        state.cancelled.add(requestId);
        controller.abort();
    }
    state.indexUrl = String(payload.indexUrl || payload.url || "/data/tag-graph/index.json");
    state.baseUrl = String(payload.baseUrl || "");
    state.cache.clear();
    state.searchItems = null;
    state.searchById = null;
    state.searchLoadPromise = null;
    state.focusShards = new Map();
    state.communityGraph = null;
    state.communityHotspots = null;
    state.hotGraph = null;
    state.fullGraph = null;

    const index = await fetchJson(state.indexUrl, id, "bootstrap");
    if (epoch !== state.epoch) throw new CancelledRequestError();
    state.index = index || {};
    state.version = Math.max(1, asNumber(index?.version ?? index?.schema_version, 1));
    state.files = index?.files || {};

    const core = await loadGraphFile("core", id, "bootstrap");
    if (epoch !== state.epoch) throw new CancelledRequestError();
    state.core = core;

    return {
        version: state.version,
        generated_at: index?.generated_at || core?.stats?.generated_at || null,
        defaults: index?.defaults || {},
        layers: { ...(index?.layers || {}), ...(core.layers || {}) },
        stats: { ...(core.stats || {}), ...(index?.stats || {}) },
        graph: core,
        capabilities: {
            searchIndex: state.version >= 2 && Boolean(fileFor("search")),
            communitySummary: state.version >= 2 && Boolean(fileFor("community")),
            communityHotspots: state.version >= 2 && Boolean(fileFor("communityHotspots")),
            focusShards: state.version >= 2 &&
                Array.isArray(focusShardManifest()) &&
                focusShardManifest().length === FOCUS_SHARD_COUNT
        }
    };
}

function foldSearchText(value) {
    return String(value ?? "").normalize("NFKC").toLocaleLowerCase();
}

function searchableText(item) {
    return foldSearchText([
        item.id,
        item.legacy_id,
        item.name,
        item.label,
        item.layer,
        item.category,
        item.description,
        item.text
    ].filter(Boolean).join(" "));
}

function precomputeSearchTerms(item) {
    if (!item || item[SEARCH_TERMS]) return item;
    Object.defineProperty(item, SEARCH_TERMS, {
        configurable: false,
        enumerable: false,
        value: {
            text: searchableText(item),
            name: foldSearchText(item.name || item.label),
            identity: foldSearchText(item.id),
            legacyId: foldSearchText(item.legacy_id)
        }
    });
    return item;
}

function searchTerms(item) {
    precomputeSearchTerms(item);
    return item[SEARCH_TERMS];
}

function startSearchItemsLoad() {
    const epoch = state.epoch;
    const loadId = `search-index:${epoch}`;
    const searchUrl = state.version >= 2 && fileFor("search")
        ? resolveUrl(fileFor("search"))
        : "";
    state.controllers.set(loadId, new AbortController());

    let loadPromise;
    loadPromise = (async () => {
        try {
            let items;

            if (searchUrl) {
                let payload;
                try {
                    payload = await fetchJson(searchUrl, loadId, "search");
                    if (epoch !== state.epoch) throw new CancelledRequestError();
                    const rawItems = asArray(payload?.items).length > 0
                        ? payload.items
                        : asArray(payload?.nodes);
                    items = rawItems.map(normalizeNode).filter(Boolean);
                } finally {
                    // The normalized index is authoritative after initialization. Keeping the
                    // decoded payload in the generic cache would retain a second full copy.
                    state.cache.delete(searchUrl);
                }
            } else {
                const full = await ensureFullGraph(loadId, "search");
                if (epoch !== state.epoch) throw new CancelledRequestError();
                items = full.nodes;
            }

            items.forEach(precomputeSearchTerms);
            const byId = new Map(items.map((node) => [node.id, node]));
            if (epoch !== state.epoch) throw new CancelledRequestError();
            state.searchItems = items;
            state.searchById = byId;
            return items;
        } finally {
            state.controllers.delete(loadId);
            state.cancelled.delete(loadId);
            if (state.searchLoadPromise === loadPromise) {
                state.searchLoadPromise = null;
            }
        }
    })();

    return loadPromise;
}

async function ensureSearchItems(id) {
    if (state.searchItems) return state.searchItems;

    if (!state.searchLoadPromise) {
        state.searchLoadPromise = startSearchItemsLoad();
    }

    const items = await state.searchLoadPromise;
    assertActive(id);
    return items;
}

async function search(id, payload) {
    const query = foldSearchText(String(payload.query || "").trim());
    if (!query) return { items: [], query: "" };
    const limit = clampLimit(payload.limit, SEARCH_LIMIT, SEARCH_LIMIT);
    const items = await ensureSearchItems(id);
    assertActive(id);

    const matchQuality = (item) => {
        const { name, identity, legacyId } = searchTerms(item);
        if (name === query || identity === query || legacyId === query) return 0;
        if (name.startsWith(query)) return 1;
        if (name.includes(query)) return 2;
        return 3;
    };
    const matches = items
        .filter((item) => searchTerms(item).text.includes(query))
        .sort((left, right) => matchQuality(left) - matchQuality(right) || compareNodes(left, right))
        .slice(0, limit);
    return { items: matches, query };
}

function trimGraph(graph, nodeLimit, edgeLimit = FOCUS_EDGE_LIMIT) {
    const nodes = [...asArray(graph.nodes)].sort(compareNodes).slice(0, nodeLimit);
    const nodeIds = new Set(nodes.map((node) => node.id));
    const links = asArray(graph.links)
        .filter((link) => nodeIds.has(endpointId(link.source)) && nodeIds.has(endpointId(link.target)))
        .sort(compareLinks)
        .slice(0, edgeLimit);
    return { ...graph, nodes, links };
}

function withLabelRanks(graph) {
    return {
        ...graph,
        nodes: asArray(graph.nodes).map((node, index) =>
            asNumber(node.rank, 0) > 0 ? node : { ...node, label_rank: index + 1 }
        )
    };
}

async function community(id, payload) {
    const limit = clampLimit(payload.limit, visibleCommunityLimit(), visibleCommunityLimit());

    if (state.version >= 2 && fileFor("community")) {
        await ensureCommunityGraph(id, "community");
        return { graph: trimGraph(visibleCommunityGraph(), limit, FOCUS_EDGE_LIMIT) };
    }

    const hot = await ensureHotGraph(id, "community");
    return { graph: withLabelRanks(trimGraph(hot, limit)) };
}

async function ensureCommunityGraph(id, operation) {
    if (state.communityGraph) return state.communityGraph;
    if (!fileFor("community")) return null;
    const raw = await fetchJson(resolveUrl(fileFor("community")), id, operation);
    state.communityGraph = communityPayloadToGraph(raw);
    return state.communityGraph;
}

async function ensureCommunityHotspots(id, selected, operation) {
    if (!state.communityHotspots) state.communityHotspots = new Map();
    if (state.communityHotspots.has(selected.id)) {
        return state.communityHotspots.get(selected.id);
    }

    let file = String(selected.hotspot_file || selected.hotspotFile || "");
    if (!file) return null;

    const raw = await fetchJson(resolveUrl(file), id, operation);
    const payloadCommunityId = String(raw?.community_id || "");
    if (asNumber(raw?.version, 0) !== 2 || payloadCommunityId !== selected.id) {
        throw new Error(
            `Community shard mismatch: expected ${selected.id}, received ${payloadCommunityId || "unknown"}`
        );
    }
    const graph = normalizeGraph(raw);
    state.communityHotspots.set(selected.id, graph);
    return graph;
}

async function ensureHotGraph(id, operation) {
    if (state.hotGraph) return state.hotGraph;
    const [tagHot, conceptHot] = await Promise.all([
        loadGraphFile("tagHot", id, operation),
        loadGraphFile("conceptHot", id, operation)
    ]);
    assertActive(id);
    state.hotGraph = mergeGraphs([state.core, tagHot, conceptHot]);
    return state.hotGraph;
}

async function ensureFullGraph(id, operation) {
    if (state.fullGraph) return state.fullGraph;
    const hot = await ensureHotGraph(id, operation);
    const fullTag = await loadGraphFile("tag", id, operation);
    assertActive(id);
    state.fullGraph = mergeGraphs([hot, fullTag]);
    return state.fullGraph;
}

function findNode(graph, nodeId) {
    const wanted = String(nodeId || "");
    return graph.nodes.find((node) =>
        node.id === wanted ||
        String(node.legacy_id || "") === wanted ||
        String(node.name || "") === wanted
    );
}

function findLoadedNode(nodeId) {
    for (const graph of [state.fullGraph, state.hotGraph, state.core]) {
        if (!graph) continue;
        const found = findNode(graph, nodeId);
        if (found) return found;
    }
    return null;
}

function findSearchNode(nodeId) {
    const wanted = String(nodeId || "");
    const exact = state.searchById?.get(wanted);
    if (exact) return exact;
    return asArray(state.searchItems).find((node) =>
        String(node.legacy_id || "") === wanted || String(node.name || "") === wanted
    ) || null;
}

function assertFocusShardIdentity(raw, bucket, nodeId) {
    const receivedVersion = asNumber(raw?.version, 0);
    const receivedBucket = asNumber(raw?.bucket, -1);
    const receivedAlgorithm = String(raw?.algorithm || "");
    const entries = raw?.entries;
    if (receivedVersion !== 2 || receivedBucket !== bucket ||
        receivedAlgorithm !== FOCUS_SHARD_ALGORITHM ||
        !entries || typeof entries !== "object" || Array.isArray(entries)) {
        throw new Error(
            `Focus shard mismatch: expected v2/${FOCUS_SHARD_ALGORITHM}/${bucket}, ` +
            `received v${receivedVersion}/${receivedAlgorithm || "unknown"}/${receivedBucket}`
        );
    }
    if (!Object.prototype.hasOwnProperty.call(entries, nodeId) ||
        !Array.isArray(entries[nodeId])) {
        throw new Error(`Focus shard mismatch: missing entry for ${nodeId} in bucket ${bucket}`);
    }
}

async function loadFocusShard(id, nodeId) {
    const manifest = focusShardManifest();
    if (manifest == null) return null;
    if (!Array.isArray(manifest) || manifest.length !== FOCUS_SHARD_COUNT) {
        throw new Error(
            `Focus shard mismatch: expected ${FOCUS_SHARD_COUNT} manifest entries`
        );
    }

    const bucket = focusBucket(nodeId);
    const file = manifest[bucket];
    if (typeof file !== "string" || !file.trim()) return null;
    if (state.focusShards.has(bucket)) {
        const cached = state.focusShards.get(bucket);
        assertFocusShardIdentity(cached, bucket, nodeId);
        return cached;
    }

    let raw;
    try {
        raw = await fetchJson(resolveUrl(file), id, "focus");
    } catch (error) {
        if (error?.status === 404) return null;
        throw error;
    }
    assertFocusShardIdentity(raw, bucket, nodeId);
    state.focusShards.set(bucket, raw);
    return raw;
}

function buildShardFocusGraph(shard, selected, neighborLimit, edgeLimit) {
    const relationships = shard.entries[selected.id];
    const candidates = new Map();

    for (const relationship of relationships) {
        if (!Array.isArray(relationship) || relationship.length < 4) {
            throw new Error(`Focus shard mismatch: malformed relationship for ${selected.id}`);
        }
        const [rawNeighborId, rawWeight, rawType, rawDirection] = relationship;
        const neighborId = String(rawNeighborId || "");
        const direction = asNumber(rawDirection, 0);
        const weight = asNumber(rawWeight, Number.NaN);
        if (!neighborId || neighborId === selected.id || !Number.isFinite(weight) ||
            (direction !== 1 && direction !== -1)) {
            throw new Error(`Focus shard mismatch: malformed relationship for ${selected.id}`);
        }
        const neighbor = state.searchById?.get(neighborId);
        if (!neighbor) {
            throw new Error(
                `Focus shard mismatch: neighbor ${neighborId} is absent from search index`
            );
        }
        const current = candidates.get(neighborId);
        if (!current || weight > current.weight) {
            candidates.set(neighborId, {
                neighbor,
                weight,
                type: String(rawType || "related"),
                direction
            });
        }
    }

    const selectedCandidates = Array.from(candidates.values())
        .sort((left, right) => right.weight - left.weight ||
            compareNodes(left.neighbor, right.neighbor))
        .slice(0, neighborLimit);
    const nodes = [selected, ...selectedCandidates.map((candidate) => candidate.neighbor)];
    const links = selectedCandidates.slice(0, edgeLimit).map((candidate, index) => {
        const source = candidate.direction === 1 ? selected.id : candidate.neighbor.id;
        const target = candidate.direction === 1 ? candidate.neighbor.id : selected.id;
        return normalizeLink({
            id: `focus:${selected.id}:${candidate.neighbor.id}:${index}`,
            source,
            target,
            type: candidate.type,
            weight: candidate.weight,
            strength: candidate.weight
        }, index);
    });
    return withLabelRanks({
        nodes,
        links,
        layers: { ...(state.index?.layers || {}), ...(state.core.layers || {}) },
        stats: { ...(state.core.stats || {}), ...(state.index?.stats || {}) }
    });
}

function buildFocusGraph(graph, selected, neighborLimit, edgeLimit) {
    const incident = graph.links
        .filter((link) => link.source === selected.id || link.target === selected.id)
        .sort(compareLinks);
    const nodeById = new Map(graph.nodes.map((node) => [node.id, node]));
    const neighborScores = new Map();

    for (const link of incident) {
        const neighborId = link.source === selected.id ? link.target : link.source;
        if (!nodeById.has(neighborId)) continue;
        const previous = neighborScores.get(neighborId) || 0;
        neighborScores.set(neighborId, Math.max(previous, asNumber(link.weight, 1)));
    }

    const neighbors = Array.from(neighborScores.keys())
        .map((neighborId) => nodeById.get(neighborId))
        .sort((left, right) => {
            const edgeDifference = neighborScores.get(right.id) - neighborScores.get(left.id);
            return edgeDifference !== 0 ? edgeDifference : compareNodes(left, right);
        })
        .slice(0, neighborLimit);
    const nodes = [selected, ...neighbors];
    const nodeIds = new Set(nodes.map((node) => node.id));
    const links = graph.links
        .filter((link) => nodeIds.has(link.source) && nodeIds.has(link.target))
        .sort((left, right) => {
            const leftIncident = left.source === selected.id || left.target === selected.id ? 1 : 0;
            const rightIncident = right.source === selected.id || right.target === selected.id ? 1 : 0;
            return rightIncident - leftIncident || compareLinks(left, right);
        })
        .slice(0, edgeLimit);
    return withLabelRanks({ nodes, links, layers: graph.layers, stats: graph.stats });
}

async function buildCommunityFocus(id, selected, neighborLimit, edgeLimit) {
    const sourceGraph = await ensureCommunityHotspots(id, selected, "focus") || {
        nodes: [], links: [], layers: {}, stats: {}
    };
    const memberCandidates = sourceGraph.nodes;

    const members = memberCandidates
        .sort(compareNodes)
        .slice(0, neighborLimit)
        .map((member) => ({
            ...member,
            community_id: selected.id,
            graph_role: "community-hotspot"
        }));
    const memberSet = new Set(members.map((node) => node.id));
    const syntheticLinks = members.map((member, index) => normalizeLink({
        id: `edge:${selected.id}:${member.id}`,
        source: selected.id,
        target: member.id,
        type: "community-member",
        weight: Math.max(1, asNumber(member.weighted_degree ?? member.degree ?? member.article_count, 1)),
        strength: 1
    }, index));
    const memberLinks = sourceGraph.links
        .filter((link) => memberSet.has(link.source) && memberSet.has(link.target))
        .sort(compareLinks);
    const communityContext = visibleCommunityGraph();
    const contextNodes = communityContext.nodes.map((node) => ({
        ...node,
        graph_role: node.id === selected.id ? "community-anchor" : "community-context"
    }));
    const contextIds = new Set(contextNodes.map((node) => node.id));
    const communityLinks = communityContext.links
        .filter((link) => contextIds.has(link.source) && contextIds.has(link.target));
    const links = [...communityLinks, ...syntheticLinks, ...memberLinks].slice(0, edgeLimit);
    return {
        node: {
            ...selected,
            graph_role: "community-anchor"
        },
        graph: {
            nodes: [...contextNodes, ...members],
            links,
            layers: {
                ...(sourceGraph.layers || {}),
                community: { name: "Community", level: 0, color: "#33e6d2" }
            },
            stats: sourceGraph.stats
        }
    };
}

async function focus(id, payload) {
    const nodeId = String(payload.nodeId || payload.id || "");
    if (!nodeId) throw new Error("focus requires nodeId");
    const neighborLimit = clampLimit(payload.nodeLimit ?? payload.neighborLimit,
        FOCUS_NEIGHBOR_LIMIT, FOCUS_NEIGHBOR_LIMIT);
    const edgeLimit = clampLimit(payload.edgeLimit, FOCUS_EDGE_LIMIT, FOCUS_EDGE_LIMIT);

    if (state.version >= 2 && fileFor("community")) {
        let communities = state.communityGraph;
        let selectedCommunity = communities ? findNode(communities, nodeId) : null;
        if (!selectedCommunity && nodeId.startsWith("community:")) {
            communities = await ensureCommunityGraph(id, "focus");
            selectedCommunity = communities ? findNode(communities, nodeId) : null;
        }
        if (selectedCommunity) {
            return buildCommunityFocus(id, selectedCommunity, neighborLimit, edgeLimit);
        }
    }

    const manifest = focusShardManifest();
    if (state.version >= 2 && manifest != null && fileFor("search")) {
        await ensureSearchItems(id);
        assertActive(id);
        const indexed = findSearchNode(nodeId);
        const loaded = findLoadedNode(indexed?.id || nodeId);
        const selected = indexed || loaded
            ? normalizeNode({ ...(loaded || {}), ...(indexed || {}) })
            : null;
        if (!selected) {
            throw new Error(`Focus shard mismatch: ${nodeId} is absent from search index`);
        }
        const shard = await loadFocusShard(id, selected.id);
        if (shard) {
            return {
                node: selected,
                graph: buildShardFocusGraph(shard, selected, neighborLimit, edgeLimit)
            };
        }
    }

    let graph = state.core;
    let selected = findNode(graph, nodeId);
    if (!selected) {
        graph = await ensureHotGraph(id, "focus");
        selected = findNode(graph, nodeId);
    }
    if (!selected && fileFor("tag")) {
        graph = await ensureFullGraph(id, "focus");
        selected = findNode(graph, nodeId);
    }
    if (!selected) throw new Error(`Node not found: ${nodeId}`);

    return {
        node: selected,
        graph: buildFocusGraph(graph, selected, neighborLimit, edgeLimit)
    };
}

function cancel(id, payload) {
    const requestId = String(payload.requestId || payload.targetId || "");
    if (requestId && state.controllers.has(requestId)) {
        state.cancelled.add(requestId);
        state.controllers.get(requestId)?.abort();
    }
    return { requestId };
}

const operations = { bootstrap, search, community, focus };

async function handleProtocolMessage(message) {
    const id = String(message.id || `${message.type || "request"}:${Date.now()}`);
    const operation = String(message.type || "");
    const payload = message.payload || {};

    if (operation === "cancel") {
        const data = cancel(id, payload);
        post(id, "cancelled", "cancel", { data });
        return;
    }
    if (!operations[operation]) {
        post(id, "error", operation || "unknown", { error: `Unsupported operation: ${operation}` });
        return;
    }

    state.cancelled.delete(id);
    state.controllers.set(id, new AbortController());
    try {
        const data = await operations[operation](id, payload);
        assertActive(id);
        post(id, "success", operation, { data });
    } catch (error) {
        const cancelled = state.cancelled.has(id) ||
            error?.name === "AbortError" || error?.name === "CancelledRequestError";
        if (cancelled) {
            post(id, "cancelled", operation);
        } else {
            post(id, "error", operation, { error: error?.message || String(error) });
        }
    } finally {
        state.controllers.delete(id);
        state.cancelled.delete(id);
    }
}

async function handleLegacyMessage(message) {
    const id = String(message.id || `legacy:${Date.now()}`);
    const url = String(message.url || "");
    state.controllers.set(id, new AbortController());
    try {
        const data = await fetchJson(url, id, "load");
        self.postMessage({ type: "success", data, url });
    } catch (error) {
        self.postMessage({ type: "error", error: error?.message || String(error), url });
    } finally {
        state.controllers.delete(id);
    }
}

self.onmessage = function onMessage(event) {
    const message = event?.data || {};
    if (!message.type && message.url) return handleLegacyMessage(message);
    return handleProtocolMessage(message);
};
