"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const ROOT = path.resolve(__dirname, "../..");
const WORKER_SOURCE = fs.readFileSync(
  path.join(ROOT, "blog/static/js/data-parser-worker.js"),
  "utf8"
);
const ENGINE_SOURCE = fs.readFileSync(
  path.join(ROOT, "blog/static/js/cytoscape-graph-engine.js"),
  "utf8"
);
const RENDERER_SOURCE = fs.readFileSync(
  path.join(ROOT, "blog/static/js/cytoscape-graph-renderer.js"),
  "utf8"
);

function jsonResponse(value) {
  const bytes = new TextEncoder().encode(JSON.stringify(value));
  let sent = false;
  return {
    ok: true,
    status: 200,
    headers: { get: () => String(bytes.length) },
    body: {
      getReader() {
        return {
          async read() {
            if (sent) return { done: true, value: undefined };
            sent = true;
            return { done: false, value: bytes };
          },
        };
      },
    },
    async json() {
      return value;
    },
  };
}

function focusBucket(nodeId) {
  let hash = 0x811c9dc5;
  for (const byte of new TextEncoder().encode(String(nodeId))) {
    hash ^= byte;
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return hash % 128;
}

function focusShardPaths() {
  return Array.from(
    { length: 128 },
    (_, bucket) => `focus-shards/${String(bucket).padStart(3, "0")}.json`
  );
}

function findFocusBucketCollision(nodeId) {
  const bucket = focusBucket(nodeId);
  for (let index = 0; index < 10000; index += 1) {
    const candidate = `tag:bucket-peer-${index}`;
    if (candidate !== nodeId && focusBucket(candidate) === bucket) return candidate;
  }
  throw new Error(`Unable to find a focus bucket collision for ${nodeId}`);
}

function buildFixture() {
  const agentSearchItems = Array.from({ length: 14 }, (_, index) => ({
    id: `tag:agent-${index}`,
    name: index === 0 ? "Agent" : `AGENT ${index}`,
    layer: "tag",
    rank: index === 0 ? 99 : index,
    community_id: `community:${index % 3}`,
    text: `Agent orchestration result ${index}`,
  }));
  const communityNodes = Array.from({ length: 30 }, (_, index) => ({
    id: `community:${index}`,
    name: `Community ${index}`,
    layer: "community",
    rank: index + 1,
    degree: 50 - index,
  }));
  const focusNodes = [
    {
      id: "tag:center",
      name: "Center",
      layer: "tag",
      rank: 999,
      degree: 30,
    },
    ...Array.from({ length: 30 }, (_, index) => ({
      id: `tag:n-${index}`,
      name: `Neighbor ${index}`,
      layer: "tag",
      rank: index + 1,
      degree: 30 - index,
    })),
  ];
  const focusLinks = [];
  for (let index = 0; index < 30; index += 1) {
    focusLinks.push({
      source: "tag:center",
      target: `tag:n-${index}`,
      weight: 100 - index,
    });
  }
  for (let source = 0; source < 20; source += 1) {
    for (let target = source + 1; target < 20; target += 1) {
      focusLinks.push({
        source: `tag:n-${source}`,
        target: `tag:n-${target}`,
        weight: 1,
      });
    }
  }

  const bucketPeerId = findFocusBucketCollision("tag:center");
  const bucketPeer = {
    id: bucketPeerId,
    legacy_id: bucketPeerId.slice(4),
    name: "Bucket peer",
    layer: "tag",
    category: "testing",
    description: "Shares a deterministic focus bucket with tag:center",
    article_count: 3,
    degree: 1,
    weighted_degree: 7,
    community_id: "community:0",
    rank: 700,
  };
  const conceptNode = {
    id: "concept:vector-search",
    legacy_id: "vector-search",
    name: "Vector Search",
    layer: "concept",
    category: "retrieval",
    description: "Concept metadata comes from the lightweight search index",
    article_count: 8,
    degree: 1,
    weighted_degree: 12,
    community_id: "community:1",
    rank: 80,
  };
  const completeFocusNodes = focusNodes.map((node) => ({
    legacy_id: node.id.slice(4),
    category: "testing",
    description: `Complete metadata for ${node.name}`,
    article_count: node.degree,
    weighted_degree: node.degree * 2,
    community_id: "community:0",
    ...node,
  }));
  const searchItems = [...agentSearchItems, ...completeFocusNodes, bucketPeer, conceptNode];
  const shardFiles = focusShardPaths();
  const shardPayloads = new Map();
  const addShardEntry = (nodeId, relationships) => {
    const bucket = focusBucket(nodeId);
    if (!shardPayloads.has(bucket)) {
      shardPayloads.set(bucket, {
        version: 2,
        bucket,
        algorithm: "fnv1a32",
        entries: {},
      });
    }
    shardPayloads.get(bucket).entries[nodeId] = relationships;
  };
  addShardEntry(
    "tag:center",
    focusLinks
      .filter((link) => link.source === "tag:center" || link.target === "tag:center")
      .map((link) => [
        link.source === "tag:center" ? link.target : link.source,
        link.weight,
        "related",
        link.source === "tag:center" ? 1 : -1,
      ])
  );
  addShardEntry(bucketPeerId, [["tag:n-0", 7, "related", 1]]);
  addShardEntry("concept:vector-search", [["tag:n-0", 12, "concept-tag", -1]]);

  const fixtures = {
    "/graph/index.json": {
      version: 2,
      generated_at: "2026-07-13T00:00:00Z",
      files: {
        core: "core.json",
        tagHot: "tag.hot.json",
        conceptHot: "concept.hot.json",
        tag: "tag.json",
        community: "community.json",
        communityHotspots: "community-hotspots/",
        search: "search.json",
        focusShards: shardFiles,
      },
      layers: {
        tech: { name: "Tech", level: 1, color: "#00ffff" },
        tag: { name: "Tag", level: 2, color: "#ffaa00" },
      },
      defaults: { community_limit: 11 },
      stats: { total_articles: 42 },
    },
    "/graph/core.json": {
      nodes: [
        { id: "tech:python", name: "Python", layer: "tech", rank: 10 },
        { id: "tech:pytorch", name: "PyTorch", layer: "tech", rank: 9 },
      ],
      links: [{ source: "tech:python", target: "tech:pytorch", weight: 2 }],
    },
    "/graph/search.json": { items: searchItems },
    "/graph/community.json": {
      communities: communityNodes.map((node, index) => ({
        ...node,
        hotspot_file:
          index < 2 ? `community-hotspots/${String(index + 1).padStart(2, "0")}.json` : undefined,
      })),
      links: [],
    },
    "/graph/community-hotspots/01.json": {
      version: 2,
      community_id: "community:0",
      hotspot_limit: 24,
      nodes: focusNodes,
      links: focusLinks,
    },
    "/graph/community-hotspots/02.json": {
      version: 2,
      community_id: "community:1",
      hotspot_limit: 24,
      nodes: focusNodes.slice(0, 4),
      links: focusLinks.slice(0, 3),
    },
    "/graph/tag.hot.json": { nodes: focusNodes, links: focusLinks },
    "/graph/concept.hot.json": {
      nodes: [conceptNode],
      links: [{ source: "tag:n-0", target: conceptNode.id, weight: 12, type: "concept-tag" }],
    },
    "/graph/tag.json": { nodes: [...focusNodes, bucketPeer], links: focusLinks },
  };
  for (const [bucket, payload] of shardPayloads) {
    fixtures[`/graph/${shardFiles[bucket]}`] = payload;
  }
  return fixtures;
}

function createWorkerHarness(fixtures = buildFixture()) {
  const posted = [];
  const fetched = [];
  const self = {
    postMessage(message) {
      posted.push(message);
    },
  };
  const context = vm.createContext({
    self,
    URL,
    TextDecoder,
    TextEncoder,
    Uint8Array,
    AbortController,
    DOMException,
    console,
    fetch: async (url) => {
      fetched.push(String(url));
      const value = fixtures[String(url)];
      if (!value) {
        return { ok: false, status: 404, headers: { get: () => null } };
      }
      return jsonResponse(value);
    },
  });
  vm.runInContext(WORKER_SOURCE, context, { filename: "data-parser-worker.js" });

  async function request(type, payload = {}, id = `${type}-request`) {
    const before = posted.length;
    await self.onmessage({ data: { id, type, payload } });
    return posted.slice(before);
  }

  return { fetched, posted, request };
}

function success(messages, operation) {
  return messages.find(
    (message) => message.type === "success" && message.operation === operation
  );
}

test("bootstrap prefers v2 metadata and fetches core only", async () => {
  const worker = createWorkerHarness();

  const messages = await worker.request("bootstrap", {
    indexUrl: "/graph/index.json",
  });

  const response = success(messages, "bootstrap");
  assert.ok(response);
  assert.equal(response.data.version, 2);
  assert.equal(response.data.graph.nodes.length, 2);
  assert.deepEqual(worker.fetched, ["/graph/index.json", "/graph/core.json"]);
});

test("search is case-insensitive, rank ordered, and capped at ten", async () => {
  const worker = createWorkerHarness();
  await worker.request("bootstrap", { indexUrl: "/graph/index.json" });

  const messages = await worker.request("search", {
    query: "aGeNt",
    limit: 99,
  });

  const response = success(messages, "search");
  assert.ok(response);
  assert.equal(response.data.items.length, 10);
  assert.equal(response.data.items[0].name, "Agent");
  assert.deepEqual(
    Array.from(response.data.items.slice(1), (item) => item.rank),
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
  );
  assert.ok(response.data.items.every((item) => /agent/i.test(`${item.name} ${item.text}`)));
  assert.ok(worker.fetched.includes("/graph/search.json"));
});

test("search and focus share one in-flight search-index initialization", async () => {
  const worker = createWorkerHarness();
  await worker.request("bootstrap", { indexUrl: "/graph/index.json" });

  const [searchMessages, focusMessages] = await Promise.all([
    worker.request("search", { query: "agent" }, "concurrent-search"),
    worker.request("focus", { nodeId: "tag:center" }, "concurrent-focus"),
  ]);

  assert.ok(success(searchMessages, "search"));
  assert.ok(success(focusMessages, "focus"));
  assert.equal(
    worker.fetched.filter((url) => url === "/graph/search.json").length,
    1,
    "the first search and focus requests must not download search.json twice"
  );
});

test("worker precomputes folded search terms and releases the raw search payload", () => {
  assert.match(WORKER_SOURCE, /searchLoadPromise/);
  assert.match(WORKER_SOURCE, /SEARCH_TERMS/);
  assert.match(WORKER_SOURCE, /searchTerms\(item\)\.text\.includes\(query\)/);
  assert.match(WORKER_SOURCE, /state\.cache\.delete\(searchUrl\)/);
  assert.doesNotMatch(
    WORKER_SOURCE,
    /\.filter\(\(item\) => searchableText\(item\)\.includes\(query\)\)/,
    "queries must reuse precomputed folded text instead of rebuilding it per item"
  );
});

test("community and focus views enforce hotspot and edge budgets", async () => {
  const worker = createWorkerHarness();
  await worker.request("bootstrap", { indexUrl: "/graph/index.json" });

  const communityMessages = await worker.request("community", { limit: 999 });
  const communities = success(communityMessages, "community").data.graph;
  assert.equal(communities.nodes.length, 11);
  assert.ok(communities.nodes.every((node) => node.graph_role === "community-context"));
  assert.deepEqual(worker.fetched, [
    "/graph/index.json",
    "/graph/core.json",
    "/graph/community.json",
  ]);

  const beforeNodeFocus = worker.fetched.length;
  const focusMessages = await worker.request("focus", {
    nodeId: "tag:center",
    nodeLimit: 999,
    edgeLimit: 999,
  });
  const focus = success(focusMessages, "focus").data.graph;
  assert.equal(focus.nodes.filter((node) => node.id !== "tag:center").length, 24);
  assert.ok(focus.links.length <= 80);
  assert.ok(
    focus.links.every(
      (link) =>
        focus.nodes.some((node) => node.id === link.source) &&
        focus.nodes.some((node) => node.id === link.target)
    )
  );
  assert.deepEqual(worker.fetched.slice(beforeNodeFocus), [
    "/graph/search.json",
    `/graph/${focusShardPaths()[focusBucket("tag:center")]}`,
  ]);
  assert.ok(
    !worker.fetched.some((url) => /\/(?:tag|concept)(?:\.hot)?\.json$/.test(url)),
    "the focus shard fast path must not fetch large tag payloads"
  );

  const fetchedBeforeCommunityFocus = worker.fetched.length;
  const communityFocusMessages = await worker.request("focus", {
    nodeId: "community:0",
    nodeLimit: 999,
    edgeLimit: 999,
  });
  const communityFocus = success(communityFocusMessages, "focus").data.graph;
  assert.equal(
    communityFocus.nodes.filter((node) => node.layer === "community").length,
    11
  );
  assert.equal(
    communityFocus.nodes.filter((node) => node.graph_role === "community-hotspot").length,
    24
  );
  assert.equal(
    communityFocus.nodes.find((node) => node.id === "community:0").graph_role,
    "community-anchor"
  );
  assert.equal(communityFocus.nodes.length, 35);
  assert.ok(communityFocus.links.length <= 80);
  assert.ok(
    communityFocus.links.some(
      (link) => link.source === "community:0" || link.target === "community:0"
    )
  );
  assert.deepEqual(worker.fetched.slice(fetchedBeforeCommunityFocus), [
    "/graph/community-hotspots/01.json",
  ]);
});

test("v2 focus reuses one cached bucket and supports concept nodes", async () => {
  const worker = createWorkerHarness();
  const bucketPeerId = findFocusBucketCollision("tag:center");
  await worker.request("bootstrap", { indexUrl: "/graph/index.json" });

  const centerMessages = await worker.request("focus", { nodeId: "tag:center" });
  const center = success(centerMessages, "focus");
  assert.ok(center);
  assert.equal(center.data.node.id, "tag:center");
  assert.equal(center.data.graph.nodes.length, 25);
  assert.ok(center.data.graph.links.every((link) =>
    link.source === "tag:center" || link.target === "tag:center"
  ));

  const beforeSameBucket = worker.fetched.length;
  const peerMessages = await worker.request("focus", { nodeId: bucketPeerId });
  const peer = success(peerMessages, "focus");
  assert.ok(peer);
  assert.equal(peer.data.node.id, bucketPeerId);
  assert.deepEqual(worker.fetched.slice(beforeSameBucket), []);

  const beforeConcept = worker.fetched.length;
  const conceptMessages = await worker.request("focus", {
    nodeId: "concept:vector-search",
  });
  const concept = success(conceptMessages, "focus");
  assert.ok(concept);
  assert.equal(concept.data.node.layer, "concept");
  assert.equal(concept.data.node.description,
    "Concept metadata comes from the lightweight search index");
  assert.deepEqual(
    Array.from(concept.data.graph.links, (link) => [link.source, link.target, link.type]),
    [["tag:n-0", "concept:vector-search", "concept-tag"]]
  );
  assert.deepEqual(worker.fetched.slice(beforeConcept), [
    `/graph/${focusShardPaths()[focusBucket("concept:vector-search")]}`,
  ]);
  assert.ok(!worker.fetched.includes("/graph/tag.hot.json"));
  assert.ok(!worker.fetched.includes("/graph/concept.hot.json"));
  assert.ok(!worker.fetched.includes("/graph/tag.json"));
});

test("a missing v2 focus shard falls back to the existing graph loader", async () => {
  const fixtures = buildFixture();
  const shardUrl = `/graph/${focusShardPaths()[focusBucket("tag:center")]}`;
  delete fixtures[shardUrl];
  const worker = createWorkerHarness(fixtures);
  await worker.request("bootstrap", { indexUrl: "/graph/index.json" });
  const beforeFocus = worker.fetched.length;

  const messages = await worker.request("focus", { nodeId: "tag:center" });

  assert.ok(success(messages, "focus"));
  assert.deepEqual(worker.fetched.slice(beforeFocus), [
    "/graph/search.json",
    shardUrl,
    "/graph/tag.hot.json",
    "/graph/concept.hot.json",
  ]);
});

test("old v2 and v1 indexes retain the full-graph focus fallback", async (t) => {
  for (const version of [2, 1]) {
    await t.test(`version ${version}`, async () => {
      const fixtures = buildFixture();
      fixtures["/graph/index.json"].version = version;
      delete fixtures["/graph/index.json"].files.focusShards;
      const worker = createWorkerHarness(fixtures);
      await worker.request("bootstrap", { indexUrl: "/graph/index.json" });
      const beforeFocus = worker.fetched.length;

      const messages = await worker.request("focus", { nodeId: "tag:center" });

      assert.ok(success(messages, "focus"));
      assert.deepEqual(worker.fetched.slice(beforeFocus), [
        "/graph/tag.hot.json",
        "/graph/concept.hot.json",
      ]);
    });
  }
});

test("focus shard identity mismatch is rejected without a graph fallback", async () => {
  const fixtures = buildFixture();
  const bucket = focusBucket("tag:center");
  const shardUrl = `/graph/${focusShardPaths()[bucket]}`;
  fixtures[shardUrl].bucket = (bucket + 1) % 128;
  const worker = createWorkerHarness(fixtures);
  await worker.request("bootstrap", { indexUrl: "/graph/index.json" });
  const beforeFocus = worker.fetched.length;

  const messages = await worker.request("focus", { nodeId: "tag:center" });

  const error = messages.find((message) => message.type === "error");
  assert.ok(error);
  assert.match(error.error, /focus shard mismatch/i);
  assert.deepEqual(worker.fetched.slice(beforeFocus), [
    "/graph/search.json",
    shardUrl,
  ]);
});

test("community expansion fetches only the selected deferred shard", async () => {
  const worker = createWorkerHarness();
  await worker.request("bootstrap", { indexUrl: "/graph/index.json" });
  await worker.request("community", { limit: 11 });
  const beforeExpansion = worker.fetched.length;

  const messages = await worker.request("focus", {
    nodeId: "community:0",
    nodeLimit: 24,
    edgeLimit: 80,
  });

  assert.ok(success(messages, "focus"));
  assert.deepEqual(worker.fetched.slice(beforeExpansion), [
    "/graph/community-hotspots/01.json",
  ]);

  const beforeCachedExpansion = worker.fetched.length;
  assert.ok(success(await worker.request("focus", {
    nodeId: "community:0",
    nodeLimit: 24,
    edgeLimit: 80,
  }), "focus"));
  assert.deepEqual(worker.fetched.slice(beforeCachedExpansion), []);

  const beforeSecondCommunity = worker.fetched.length;
  assert.ok(success(await worker.request("focus", {
    nodeId: "community:1",
    nodeLimit: 24,
    edgeLimit: 80,
  }), "focus"));
  assert.deepEqual(worker.fetched.slice(beforeSecondCommunity), [
    "/graph/community-hotspots/02.json",
  ]);
});

test("v2 community without a hotspot mapping never falls back to tag payloads", async () => {
  const fixtures = buildFixture();
  fixtures["/graph/community.json"].communities = fixtures[
    "/graph/community.json"
  ].communities.map(({ hotspot_file: _hotspotFile, ...community }) => community);
  const worker = createWorkerHarness(fixtures);
  await worker.request("bootstrap", { indexUrl: "/graph/index.json" });
  await worker.request("community", { limit: 11 });
  const beforeExpansion = worker.fetched.length;

  const messages = await worker.request("focus", {
    nodeId: "community:0",
    nodeLimit: 24,
    edgeLimit: 80,
  });

  const response = success(messages, "focus");
  assert.ok(response);
  assert.equal(
    response.data.graph.nodes.filter((node) => node.graph_role === "community-hotspot").length,
    0
  );
  assert.deepEqual(worker.fetched.slice(beforeExpansion), []);
});

test("community shard identity mismatch is rejected without a tag fallback", async () => {
  const fixtures = buildFixture();
  fixtures["/graph/community-hotspots/01.json"].community_id = "community:stale";
  const worker = createWorkerHarness(fixtures);
  await worker.request("bootstrap", { indexUrl: "/graph/index.json" });
  await worker.request("community", { limit: 11 });
  const beforeExpansion = worker.fetched.length;

  const messages = await worker.request("focus", {
    nodeId: "community:0",
    nodeLimit: 24,
    edgeLimit: 80,
  });

  const error = messages.find((message) => message.type === "error");
  assert.ok(error);
  assert.match(error.error, /community shard mismatch/i);
  assert.deepEqual(worker.fetched.slice(beforeExpansion), [
    "/graph/community-hotspots/01.json",
  ]);
});

test("renderer does not use innerHTML for runtime text", () => {
  assert.doesNotMatch(RENDERER_SOURCE, /\.innerHTML\s*=/);
  assert.match(RENDERER_SOURCE, /has-detail/);
});

test("focus mode without a selection chooses the highest-ranked non-community node", async () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const graph = {
    nodes: [
      { id: "community:top", layer: "community", rank: 1, weighted_degree: 999 },
      { id: "tag:rank-four", layer: "tag", rank: 4, weighted_degree: 400 },
      { id: "concept:rank-two", layer: "concept", rank: 2, weighted_degree: 5 },
      { id: "tag:unranked", layer: "tag", rank: 0, weighted_degree: 1000 },
    ],
    links: [],
  };
  const focused = [];
  Object.assign(engine, {
    ready: Promise.resolve(),
    isDestroyed: false,
    selectedNodeId: null,
    currentGraph: graph,
    coreGraph: graph,
    focusNode: async (nodeId) => {
      focused.push(nodeId);
      return { id: nodeId };
    },
    _emitError() {},
  });

  const result = await engine.setMode("focus");

  assert.deepEqual(focused, ["concept:rank-two"]);
  assert.equal(result.id, "concept:rank-two");
});

test("focus mode enters the strongest visible member when a community is selected", async () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const focused = [];
  Object.assign(engine, {
    ready: Promise.resolve(),
    isDestroyed: false,
    selectedNodeId: "community:rag",
    currentGraph: {
      nodes: [
        {
          id: "community:rag",
          name: "RAG 应用",
          layer: "community",
          rank: 1,
          member_ids: ["tag:weak", "tag:strong"],
        },
        {
          id: "tag:weak",
          name: "弱成员",
          layer: "tag",
          community_id: "community:rag",
          graph_role: "community-hotspot",
          weighted_degree: 20,
          rank: 1,
        },
        {
          id: "tag:strong",
          name: "强成员",
          layer: "tag",
          community_id: "community:rag",
          graph_role: "community-hotspot",
          weighted_degree: 90,
          rank: 9,
        },
        {
          id: "tag:outside",
          name: "其他社区节点",
          layer: "tag",
          community_id: "community:other",
          weighted_degree: 999,
          rank: 1,
        },
      ],
      links: [
        { source: "community:rag", target: "tag:weak", type: "community-member" },
        { source: "community:rag", target: "tag:strong", type: "community-member" },
      ],
    },
    focusNode: async (nodeId) => {
      focused.push(nodeId);
      return { id: nodeId };
    },
    _emitError() {},
  });

  const result = await engine.setMode("focus");

  assert.deepEqual(focused, ["tag:strong"]);
  assert.equal(result.id, "tag:strong");
});

test("renderer keeps the 03 focus mode button enabled unless the workbench is busy", () => {
  const window = {};
  vm.runInNewContext(RENDERER_SOURCE, { window }, {
    filename: "cytoscape-graph-renderer.js",
  });
  const Renderer = window.CytoscapeGraphRenderer;
  const renderer = Object.create(Renderer.prototype);
  const focusButton = {
    dataset: { graphMode: "focus" },
    disabled: false,
  };
  Object.assign(renderer, {
    _busy: false,
    engine: { selectedNodeId: null },
    modeButtons: [focusButton],
    elements: {
      detailFocus: { disabled: false },
      liveState: { textContent: "" },
    },
  });

  renderer._setBusy(false);
  assert.equal(focusButton.disabled, false, "no selection must not disable mode 03");

  renderer._syncFocusControls(false);
  assert.equal(focusButton.disabled, false, "selection events must not disable mode 03");

  renderer._setBusy(true);
  assert.equal(focusButton.disabled, true, "busy workbench must disable mode 03");
});

test("engine exposes the workbench API and semantic mode layouts", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const prototype = Engine.prototype;

  for (const method of [
    "setMode",
    "expandCommunity",
    "focusNode",
    "getCommunityInsights",
    "getCommunityVisualState",
    "clearSelection",
    "pause",
    "resume",
    "destroy",
  ]) {
    assert.equal(typeof prototype[method], "function", `${method} must be public`);
  }

  const engine = Object.create(prototype);
  engine.options = {};
  engine.reducedMotion = false;
  assert.equal(engine._getLayoutOptions("overview").name, "dagre");
  assert.equal(engine._getLayoutOptions("community").name, "preset");
  const focusLayout = engine._getLayoutOptions("focus");
  assert.equal(focusLayout.name, "preset");
  assert.equal(
    focusLayout.animate,
    false,
    "focus layout must settle before the camera centers the selected node"
  );
  assert.equal(engine._shouldDeferLabel({ layer: "tag", rank: 200 }), true);
  assert.equal(engine._shouldDeferLabel({ layer: "tag", rank: 2 }), false);
  assert.equal(engine._shouldDeferLabel({ layer: "framework", rank: 200 }), false);
  engine.cy = { zoom: () => 1.24 };
  assert.equal(engine._labelsShouldBeExpanded(), false);
  engine.cy = { zoom: () => 1.25 };
  assert.equal(engine._labelsShouldBeExpanded(), true);

  const packedNodes = [
    {
      id: () => "tech:python",
      data: (key) => ({ layer: "language" })[key],
      position(value) {
        if (value) this.value = value;
        return this.value || { x: 0, y: 0 };
      },
    },
    ...Array.from({ length: 31 }, (_, index) => ({
      id: () => `tech:scenario-${index}`,
      data: (key) => ({ layer: "scenario" })[key],
      position(value) {
        if (value) this.value = value;
        return this.value || { x: 500, y: index * 10 };
      },
    })),
  ];
  engine.data = {
    layers: {
      language: { level: 1 },
      scenario: { level: 5 },
    },
  };
  engine.mode = "overview";
  engine.cy = {
    nodes: () => packedNodes,
    batch: (callback) => callback(),
  };
  engine._packOverviewLayers();
  const scenarioPositions = packedNodes.slice(1).map((node) => node.position());
  assert.equal(new Set(scenarioPositions.map((position) => position.x)).size, 3);
  for (const x of new Set(scenarioPositions.map((position) => position.x))) {
    assert.ok(scenarioPositions.filter((position) => position.x === x).length <= 11);
  }
  assert.ok(
    Math.min(...scenarioPositions.map((position) => position.x)) - packedNodes[0].position().x >= 200
  );
  assert.doesNotMatch(ENGINE_SOURCE, /container\.querySelector\(['"]canvas['"]\)/);
  assert.doesNotMatch(ENGINE_SOURCE, /cose-bilkent/);
});

test("a late Cytoscape ready callback cannot refit a semantic scene", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const calls = [];
  Object.assign(engine, {
    isDestroyed: false,
    cy: {},
    mode: "community",
    _packOverviewLayers: () => calls.push("pack"),
    _fitCurrentGraph: () => calls.push("fit"),
  });

  assert.equal(engine._settleInitialViewport(), false);
  assert.deepEqual(calls, []);
  engine.mode = "overview";
  assert.equal(engine._settleInitialViewport(), true);
  assert.deepEqual(calls, ["pack", "fit"]);
});

test("overlay canvases cap their backing pixels on high-DPR displays", () => {
  const window = { devicePixelRatio: 2 };
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const pixelBudget = 8 * 1024 * 1024;

  const fullHdRatio = engine._resolveOverlayPixelRatio(1920, 1080);
  const fourKRatio = engine._resolveOverlayPixelRatio(3840, 2160);
  const eightKRatio = engine._resolveOverlayPixelRatio(7680, 4320);

  assert.equal(fullHdRatio, 2, "1080p should retain a crisp 2x backing store");
  assert.ok(fourKRatio < 2, "4K must reduce DPR instead of allocating 4x pixels");
  assert.ok(eightKRatio < 1, "8K must be allowed to render below CSS-pixel density");
  for (const [width, height, ratio] of [
    [3840, 2160, fourKRatio],
    [7680, 4320, eightKRatio],
  ]) {
    assert.ok(
      width * height * ratio * ratio <= pixelBudget + 2,
      `${width}x${height}@${ratio} exceeds the overlay pixel budget`
    );
  }
});

test("pause and resume restore an interrupted layout exactly once", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const classChanges = [];
  const layouts = [];
  let stops = 0;
  Object.assign(engine, {
    isDestroyed: false,
    _paused: false,
    _layoutRunning: true,
    _layoutInterrupted: false,
    mode: "overview",
    cy: {},
    container: {
      closest: () => ({
        classList: {
          add: (name) => classChanges.push(`add:${name}`),
          remove: (name) => classChanges.push(`remove:${name}`),
        },
      }),
    },
    _activeLayout: { stop: () => { stops += 1; } },
    _stopParticleLoop() {},
    _stopCommunityFieldLoop() {},
    _resizeOverlay() {},
    _syncParticles() {},
    _scheduleCommunityFieldDraw() {},
    _runLayout: (mode) => layouts.push(mode),
  });

  engine.pause();
  assert.equal(engine._paused, true);
  assert.equal(engine._layoutInterrupted, true);
  assert.equal(stops, 1);
  assert.deepEqual(classChanges, ["add:is-paused"]);

  engine.resume();
  assert.equal(engine._paused, false);
  assert.equal(engine._layoutInterrupted, false);
  assert.deepEqual(layouts, ["overview"]);
  assert.deepEqual(classChanges, ["add:is-paused", "remove:is-paused"]);

  engine.resume();
  assert.deepEqual(layouts, ["overview"], "duplicate resume must not create another layout");
});

test("community stylesheet keeps hotspot labels readable without invalid style keys", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const stylesheet = engine._getStylesheet();
  const baseNode = stylesheet.find((entry) => entry.selector === "node").style;
  const hotspot = stylesheet.find(
    (entry) => entry.selector === "node.community-hotspot"
  ).style;
  const anchor = stylesheet.find(
    (entry) => entry.selector === "node.community-node.community-anchor"
  ).style;

  const effectiveMinimum = hotspot["min-zoomed-font-size"] ??
    baseNode["min-zoomed-font-size"];
  assert.ok(
    hotspot["font-size"] >= effectiveMinimum,
    `hotspot labels are hidden at 100% zoom: ${hotspot["font-size"]} < ${effectiveMinimum}`
  );
  assert.ok(
    anchor["text-margin-y"] >= -155 && anchor["text-margin-y"] <= -130,
    `selected community label misses the target field edge: ${anchor["text-margin-y"]}`
  );
  stylesheet.forEach((entry) => {
    Object.keys(entry.style).forEach((property) => {
      assert.ok(!property.startsWith("shadow-"), `${entry.selector}: ${property}`);
    });
  });
});

test("focus nodes use compact stellar tiers and reserve amber for the selected core", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  engine.mode = "focus";
  engine.selectedNodeId = "tag:center";
  engine.data = {
    layers: {
      tag: { name: "标签层", color: "#f59e0b" },
    },
  };

  const formatted = engine._formatElements({
    nodes: [
      {
        id: "tag:center",
        name: "AI Agent",
        layer: "tag",
        rank: 27,
        degree: 1153,
        weighted_degree: 2849,
        article_count: 407,
      },
      {
        id: "tag:neighbor",
        name: "OpenAI",
        layer: "tag",
        rank: 2,
        degree: 500,
        weighted_degree: 900,
        article_count: 200,
      },
    ],
    links: [{ source: "tag:center", target: "tag:neighbor", weight: 80 }],
  });
  const core = formatted.nodes.find((entry) => entry.data.id === "tag:center");
  const neighbor = formatted.nodes.find((entry) => entry.data.id === "tag:neighbor");

  assert.match(core.classes, /\bfocus-core\b/);
  assert.match(neighbor.classes, /\bfocus-neighbor\b/);
  assert.ok(core.data.visualSize <= 34, `focus core is oversized: ${core.data.visualSize}`);
  assert.ok(
    neighbor.data.visualSize <= 24,
    `focus neighbor is oversized: ${neighbor.data.visualSize}`
  );

  const stylesheet = engine._getStylesheet();
  const neighborStyle = stylesheet.find(
    (entry) => entry.selector === "node.focus-neighbor"
  ).style;
  const coreStyle = stylesheet.find(
    (entry) => entry.selector === "node.focus-core"
  ).style;

  assert.ok(neighborStyle["background-opacity"] <= 0.45);
  assert.doesNotMatch(
    neighborStyle["background-color"].toLowerCase(),
    /#(?:d97706|f59e0b|a96820)/
  );
  assert.equal(coreStyle["border-color"], "#f2a53a");
  assert.ok(coreStyle["border-width"] >= 2);
  assert.ok(coreStyle["underlay-padding"] >= 5);
  assert.ok(coreStyle["underlay-opacity"] > 0);
});

test("focus scene deterministically groups a bounded neighborhood into contour cells", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  Object.assign(engine, {
    mode: "focus",
    selectedNodeId: "tag:center",
    data: { layers: { tag: { name: "标签层", color: "#4db6ac" } } },
  });
  const nodes = [
    { id: "tag:center", name: "API", layer: "tag", rank: 1 },
    ...Array.from({ length: 24 }, (_, index) => ({
      id: `tag:neighbor-${index + 1}`,
      name: `Neighbor ${index + 1}`,
      layer: "tag",
      category: "article_tag",
      community_id: "community:other",
      rank: index + 2,
    })),
  ];
  const links = nodes.slice(1).map((node, index) => ({
    id: `edge:${index}`,
    source: "tag:center",
    target: node.id,
    weight: 100 - index,
  }));
  const formatted = engine._formatElements({ nodes, links });
  const inner = formatted.nodes.filter((node) => node.data.focusSceneRole === "inner");
  const context = formatted.nodes.filter((node) => node.data.focusSceneRole === "context");
  const groupAnchors = formatted.nodes.filter((node) =>
    node.classes.includes("focus-group-anchor")
  );

  assert.equal(inner.length, 8);
  assert.equal(context.length, 16);
  assert.equal(new Set(context.map((node) => node.data.focusGroupIndex)).size, 6);
  assert.equal(groupAnchors.length, 6);
  assert.ok(formatted.edges.filter((edge) =>
    edge.classes.includes("focus-context-link")
  ).length <= 16);

  const dataNodes = formatted.nodes.map((node) => node.data);
  const bounds = { width: 1269, height: 894 };
  const positions = engine._focusPresetPositions(dataNodes, bounds);
  const repeated = engine._focusPresetPositions(dataNodes, bounds);
  assert.deepEqual(positions, repeated, "focus topology must be deterministic");
  assert.equal(new Set(Object.values(positions).map(({ x, y }) => `${x}:${y}`)).size, 25);
  const center = positions["tag:center"];
  inner.forEach((node) => {
    assert.ok(
      Math.hypot(positions[node.data.id].x - center.x, positions[node.data.id].y - center.y) < 130,
      `${node.data.id} escaped the selected focus cell`
    );
  });
  groupAnchors.forEach((node) => {
    assert.ok(
      Math.hypot(positions[node.data.id].x - center.x, positions[node.data.id].y - center.y) > 190,
      `${node.data.id} did not form an outer context cell`
    );
  });

  const mobilePositions = engine._focusPresetPositions(
    dataNodes,
    { width: 390, height: 844 }
  );
  assert.equal(new Set(Object.values(mobilePositions).map(({ x, y }) => `${x}:${y}`)).size, 25);
  assert.equal(new Set(groupAnchors.map((node) => {
    const position = mobilePositions[node.data.id];
    return `${position.x}:${position.y}`;
  })).size, 6, "mobile focus groups must retain six independent cells");
  Object.values(mobilePositions).forEach((position) => {
    assert.ok(position.x >= 20 && position.x <= 370, `mobile focus x overflow: ${position.x}`);
    assert.ok(position.y >= 24 && position.y <= 820, `mobile focus y overflow: ${position.y}`);
  });
});

test("community mode chooses the fifth ranked cell as its bounded default expansion", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const communities = Array.from({ length: 11 }, (_, index) => ({
    id: `community:${11 - index}`,
    name: `Community ${11 - index}`,
    layer: "community",
    rank: 11 - index,
  }));

  assert.equal(
    engine._defaultCommunityAnchorId({ nodes: communities, links: [] }),
    "community:5"
  );
  assert.equal(
    engine._defaultCommunityAnchorId({ nodes: communities.slice(0, 3), links: [] }),
    "community:9"
  );
});

test("community mode progressively loads one bounded default hotspot shard", async () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const communities = Array.from({ length: 11 }, (_, index) => ({
    id: `community:${index + 1}`,
    name: `Community ${index + 1}`,
    layer: "community",
    rank: index + 1,
  }));
  const requests = [];
  const renders = [];
  let resolveExpansion;
  const expansionPromise = new Promise((resolve) => {
    resolveExpansion = resolve;
  });
  const expandedResponse = {
    node: { ...communities[4], graph_role: "community-anchor" },
    graph: {
      nodes: [
        ...communities.map((node) => ({
          ...node,
          graph_role: node.id === "community:5"
            ? "community-anchor"
            : "community-context",
        })),
        { id: "tag:hot", name: "Hot", layer: "tag", graph_role: "community-hotspot" },
      ],
      links: [{
        source: "community:5",
        target: "tag:hot",
        type: "community-member",
      }],
    },
  };
  Object.assign(engine, {
    ready: Promise.resolve(),
    isDestroyed: false,
    mode: "overview",
    layoutMode: "overview",
    worker: {},
    _modeSequence: 0,
    _request: async (type, payload) => {
      requests.push({ type, payload });
      if (type === "community") {
        return { graph: { nodes: communities, links: [] } };
      }
      return expansionPromise;
    },
    clearSelection() {},
    _replaceGraph: (graph, mode) => {
      renders.push({ graph, mode });
      engine.currentGraph = graph;
    },
    _emit() {},
    _emitError() {},
  });

  assert.equal(await engine.setMode("community"), "community");
  assert.deepEqual(requests.map((request) => request.type), ["community", "focus"]);
  assert.equal(requests[1].payload.nodeId, "community:5");
  assert.equal(requests[1].payload.nodeLimit, 24);
  assert.equal(requests[1].payload.edgeLimit, 80);
  assert.equal(engine.expandedCommunityId, null);
  assert.equal(renders.length, 1, "summary skeleton must render before hotspot I/O resolves");
  assert.equal(renders[0].mode, "community");
  assert.equal(renders[0].graph.nodes.length, 11);

  const progressiveTask = engine._defaultCommunityExpansion;
  assert.ok(progressiveTask, "default hotspot load should continue in the background");
  resolveExpansion(expandedResponse);
  assert.equal(await progressiveTask, true);
  assert.equal(engine.expandedCommunityId, "community:5");
  assert.equal(renders.length, 2);
  assert.equal(renders[1].graph.nodes.length, 12);
});

test("a stale progressive community expansion cannot replace a newer view", async () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  let resolveExpansion;
  const expansionPromise = new Promise((resolve) => {
    resolveExpansion = resolve;
  });
  let replacements = 0;
  Object.assign(engine, {
    isDestroyed: false,
    mode: "community",
    _modeSequence: 7,
    _request: async () => expansionPromise,
    _replaceGraph: () => { replacements += 1; },
    _emit() {},
  });

  const task = engine._queueDefaultCommunityExpansion("community:5", 7);
  engine._modeSequence = 8;
  engine.mode = "overview";
  resolveExpansion({
    node: { id: "community:5", layer: "community" },
    graph: { nodes: [], links: [] },
  });

  assert.equal(await task, false);
  assert.equal(replacements, 0);
  assert.equal(engine.expandedCommunityId, undefined);
});

test("an explicit community drawer reserves its side channel before the only layout run", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const communities = Array.from({ length: 11 }, (_, index) => ({
    id: `community:${index + 1}`,
    name: `Community ${index + 1}`,
    layer: "community",
    rank: index + 1,
  }));
  const response = {
    node: communities[4],
    graph: { nodes: communities, links: [] },
  };
  const fakeNode = { length: 1 };
  const layouts = [];
  Object.assign(engine, {
    mode: "community",
    selectedNode: null,
    _detailCommunityId: null,
    currentGraph: response.graph,
    cy: {
      getElementById: () => fakeNode,
      nodes: () => ({ length: 11 }),
      edges: () => ({ length: 0 }),
    },
    _replaceGraph(graph) {
      engine.currentGraph = graph;
      const positions = engine._communityPresetPositions(
        graph.nodes,
        { width: 1269, height: 894 },
        "community:5"
      );
      layouts.push({
        detailId: engine._detailCommunityId,
        selectedAtLayout: engine.selectedNode,
        center: positions["community:5"],
      });
    },
    _selectNode(node) {
      engine.selectedNode = node;
      return { id: "community:5", layer: "community" };
    },
    _emit() {},
    _scheduleCommunityFieldDraw() {},
  });

  engine._applyCommunityExpansion(response, "community");
  assert.equal(layouts.length, 1);
  assert.equal(layouts[0].detailId, "community:5");
  assert.equal(layouts[0].selectedAtLayout, null, "test must preserve real call order");
  assert.ok(layouts[0].center.x >= 450 && layouts[0].center.x <= 470);
});

test("tapping the already expanded center reserves the drawer and reflows exactly once", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const handlers = [];
  const order = [];
  Object.assign(engine, {
    mode: "community",
    expandedCommunityId: "community:5",
    _detailCommunityId: null,
    cy: {
      on(...args) { handlers.push(args); },
    },
    _selectNode() {
      order.push("select");
      return { id: "community:5", layer: "community" };
    },
    _runLayout(mode) { order.push(`layout:${mode}`); },
    expandCommunity() {
      throw new Error("the expanded center must not request its shard again");
    },
  });
  engine._bindCytoscapeEvents();
  const tapNode = handlers.find(([eventName, selector]) =>
    eventName === "tap" && selector === "node"
  )?.[2];
  assert.equal(typeof tapNode, "function");

  tapNode({ target: {} });
  assert.deepEqual(order, ["select", "layout:community"]);
  assert.equal(engine._detailCommunityId, "community:5");

  tapNode({ target: {} });
  assert.deepEqual(
    order,
    ["select", "layout:community", "select"],
    "an already-reserved drawer must not trigger a second layout"
  );
});

test("closing a community drawer restores the full stage exactly once", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const communities = Array.from({ length: 11 }, (_, index) => ({
    id: `community:${index + 1}`,
    layer: "community",
    rank: index + 1,
  }));
  const bounds = { width: 1269, height: 894 };
  const centers = [];
  Object.assign(engine, {
    isDestroyed: false,
    mode: "community",
    expandedCommunityId: "community:5",
    _detailCommunityId: "community:5",
    selectedNode: { length: 1 },
    selectedNodeId: "community:5",
    hoveredNode: null,
    _modeSequence: 0,
    cy: {
      elements: () => ({ unselect() {} }),
      nodes: () => ({ removeClass() {} }),
    },
    _cancelOperation() {},
    _updateSemanticLabels() {},
    _clearHighlights() {},
    _emit() {},
    _runLayout(mode) {
      assert.equal(mode, "community");
      const positions = engine._communityPresetPositions(
        communities,
        bounds,
        "community:5"
      );
      centers.push(positions["community:5"]);
    },
  });
  const reservedCenter = engine._communityPresetPositions(
    communities,
    bounds,
    "community:5"
  )["community:5"];

  engine.clearSelection();
  assert.equal(engine._detailCommunityId, null);
  assert.equal(centers.length, 1);
  assert.ok(reservedCenter.x >= 450 && reservedCenter.x <= 470);
  assert.ok(centers[0].x >= 595 && centers[0].x <= 615);

  engine.clearSelection();
  assert.equal(centers.length, 1, "an already-closed drawer must not reflow again");
});

test("v1 community payloads fall back to a bounded non-preset layout", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const ordinaryNodes = Array.from({ length: 24 }, (_, index) => ({
    id: `tag:${index}`,
    layer: "tag",
    rank: index + 1,
  }));
  Object.assign(engine, {
    reducedMotion: false,
    container: { getBoundingClientRect: () => ({ width: 800, height: 640 }) },
    cy: {
      nodes: () => ({
        map: (callback) => ordinaryNodes.map((node) => callback({ data: () => node })),
      }),
    },
  });

  const layout = engine._getLayoutOptions("community");
  assert.equal(layout.name, "concentric");
  assert.equal(layout.fit, true);
  assert.equal(layout.animate, false);
  assert.ok(layout.minNodeSpacing >= 42);
});

test("focus resize restores its complete scene instead of re-centering one node", () => {
  const scheduled = [];
  const window = {
    setTimeout(callback) {
      scheduled.push(callback);
      return scheduled.length;
    },
    clearTimeout() {},
  };
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const selected = { length: 1, id: () => "tag:center" };
  let zoom = 1.54;
  const centered = [];
  const layouts = [];
  Object.assign(engine, {
    isDestroyed: false,
    mode: "focus",
    selectedNodeId: "tag:center",
    _resizeFitTimer: null,
    _resizeOverlay() {},
    _runLayout(mode) {
      layouts.push(mode);
    },
    container: { getBoundingClientRect: () => ({ width: 1269, height: 904 }) },
    cy: {
      resize() {},
      zoom(value) {
        if (value !== undefined) zoom = value;
        return zoom;
      },
      center(node) {
        centered.push(node.id());
      },
      getElementById: () => selected,
    },
  });

  engine._handleViewportResize();
  assert.equal(scheduled.length, 1);
  scheduled[0]();

  assert.deepEqual(layouts, ["focus"]);
  assert.equal(zoom, 1);
  assert.deepEqual(centered, []);
});

test("community preset keeps one selected field centered with ten separated satellites", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const communities = Array.from({ length: 11 }, (_, index) => ({
    id: `community:${index + 1}`,
    layer: "community",
    graph_role: index === 4 ? "community-anchor" : "community-context",
    rank: index + 1,
  }));
  const hotspots = Array.from({ length: 24 }, (_, index) => ({
    id: `tag:hotspot-${index + 1}`,
    layer: "tag",
    graph_role: "community-hotspot",
    rank: index + 1,
  }));
  const nodes = [...communities, ...hotspots];
  // 1625x968 acceptance viewport minus the 356px console and 74px header.
  const bounds = { width: 1269, height: 894 };
  engine.selectedNode = { length: 1 };

  const positions = engine._communityPresetPositions(
    nodes,
    bounds,
    "community:5"
  );
  const repeated = engine._communityPresetPositions(
    nodes,
    bounds,
    "community:5"
  );
  assert.deepEqual(positions, repeated, "community layout must be deterministic");

  const readmeViewportPositions = engine._communityPresetPositions(
    communities,
    { width: 968, height: 736 },
    null
  );
  assert.ok(
    readmeViewportPositions["community:1"].y >= 145,
    `top community label lacks safe headroom: ${readmeViewportPositions["community:1"].y}`
  );

  const center = positions["community:5"];
  assert.ok(center.x >= 410 && center.x <= 500, `unexpected center x: ${center.x}`);
  assert.ok(center.y >= 360 && center.y <= 450, `unexpected center y: ${center.y}`);
  assert.ok(
    Math.abs(356 + center.x - 815) <= 3,
    `selected field must align with the target x anchor: ${356 + center.x}`
  );
  assert.ok(
    Math.abs(74 + center.y - 484) <= 3,
    `selected field must align with the target y anchor: ${74 + center.y}`
  );

  const contextPositions = communities
    .filter((node) => node.id !== "community:5")
    .map((node) => positions[node.id]);
  assert.equal(contextPositions.length, 10);
  assert.ok(contextPositions.every((position) => position.x < bounds.width - 300));
  contextPositions.forEach((position) => {
    assert.ok(Math.hypot(position.x - center.x, position.y - center.y) >= 210);
  });
  for (let left = 0; left < contextPositions.length; left += 1) {
    for (let right = left + 1; right < contextPositions.length; right += 1) {
      assert.ok(
        Math.hypot(
          contextPositions[left].x - contextPositions[right].x,
          contextPositions[left].y - contextPositions[right].y
        ) >= 145,
        `community satellites ${left} and ${right} overlap`
      );
    }
  }

  const hotspotPositions = hotspots.map((node) => positions[node.id]);
  assert.equal(new Set(hotspotPositions.map(({ x, y }) => `${x}:${y}`)).size, 24);
  hotspotPositions.forEach((position) => {
    const radius = Math.hypot(position.x - center.x, position.y - center.y);
    assert.ok(radius >= 38 && radius <= 170, `unexpected hotspot radius: ${radius}`);
  });
  for (let left = 0; left < hotspotPositions.length; left += 1) {
    for (let right = left + 1; right < hotspotPositions.length; right += 1) {
      assert.ok(
        Math.hypot(
          hotspotPositions[left].x - hotspotPositions[right].x,
          hotspotPositions[left].y - hotspotPositions[right].y
        ) >= 24,
        `hotspots ${left} and ${right} overlap`
      );
    }
  }

  const overviewPositions = engine._communityPresetPositions(nodes, bounds, null);
  const overviewCommunityPositions = communities.map((node) => overviewPositions[node.id]);
  assert.equal(
    new Set(overviewCommunityPositions.map(({ x, y }) => `${x}:${y}`)).size,
    11,
    "unexpanded communities must occupy eleven unique fields"
  );
  const overviewCenter = overviewPositions["community:5"];
  assert.ok(
    overviewCommunityPositions.every((position, index) =>
      index === 4 || `${position.x}:${position.y}` !== `${overviewCenter.x}:${overviewCenter.y}`
    ),
    "rank five is the unique default center"
  );

  const rankTwoSelected = engine._communityPresetPositions(
    nodes,
    bounds,
    "community:2"
  );
  assert.deepEqual(rankTwoSelected["community:2"], center);
  assert.deepEqual(
    rankTwoSelected["community:5"],
    positions["community:2"],
    "selecting another community swaps it with the default center instead of reflowing every field"
  );
  for (const node of communities.filter((item) => !["community:2", "community:5"].includes(item.id))) {
    assert.deepEqual(
      rankTwoSelected[node.id],
      positions[node.id],
      `${node.id} must retain its spatial home`
    );
  }

  const mobilePositions = engine._communityPresetPositions(
    nodes,
    { width: 390, height: 467 },
    "community:5"
  );
  const mobileCenter = mobilePositions["community:5"];
  const mobileHotspotRadius = Math.max(...hotspots.map((node) => {
    const position = mobilePositions[node.id];
    return Math.hypot(position.x - mobileCenter.x, position.y - mobileCenter.y);
  }));
  assert.ok(
    mobileHotspotRadius <= 82,
    `mobile hotspot field must scale down instead of overflowing: ${mobileHotspotRadius}`
  );
});

test("automatic community expansion uses the full stage until a detail drawer is opened", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  engine.selectedNode = null;
  const communities = Array.from({ length: 11 }, (_, index) => ({
    id: `community:${index + 1}`,
    layer: "community",
    rank: index + 1,
  }));
  const bounds = { width: 968, height: 656 };
  const positions = engine._communityPresetPositions(
    communities,
    bounds,
    "community:5"
  );
  const center = positions["community:5"];
  const contexts = communities
    .filter((node) => node.id !== "community:5")
    .map((node) => positions[node.id]);

  assert.ok(center.x >= 450 && center.x <= 470, `unexpected automatic center x: ${center.x}`);
  assert.ok(center.y >= 292 && center.y <= 312, `unexpected automatic center y: ${center.y}`);
  assert.ok(Math.min(...contexts.map((position) => position.x)) <= 125);
  assert.ok(Math.max(...contexts.map((position) => position.x)) >= 875);
  assert.ok(Math.min(...contexts.map((position) => position.y)) <= 145);
  assert.ok(Math.max(...contexts.map((position) => position.y)) >= 555);
});

test("compact community density keeps a small progressive context set", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const nodes = Array.from({ length: 11 }, (_, index) => {
    const classes = new Set();
    return {
      id: () => `community:${index + 1}`,
      data: (key) => ({ layer: "community", rank: index + 1 })[key],
      toggleClass(name, enabled) {
        if (enabled) classes.add(name);
        else classes.delete(name);
      },
      hasClass: (name) => classes.has(name),
    };
  });
  engine.cy = { nodes: () => ({ forEach: (callback) => nodes.forEach(callback) }) };
  engine.expandedCommunityId = "community:10";

  engine._syncCommunityDensity("community", { width: 390 });
  const compactVisible = nodes.filter((node) => !node.hasClass("community-compact-hidden"));
  assert.equal(compactVisible.length, 5);
  assert.ok(compactVisible.some((node) => node.id() === "community:10"));
  assert.ok(compactVisible.every((node) => node.hasClass("community-compact")));

  engine._syncCommunityDensity("community", { width: 968 });
  assert.equal(nodes.filter((node) => node.hasClass("community-compact-hidden")).length, 0);
  assert.equal(nodes.filter((node) => node.hasClass("community-compact")).length, 0);
});

test("compact community density keeps only six hotspot labels", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const communities = Array.from({ length: 11 }, (_, index) => ({
    id: () => `community:${index + 1}`,
    data: (key) => ({ layer: "community", rank: index + 1 })[key],
    toggleClass() {},
  }));
  const hotspots = Array.from({ length: 10 }, (_, index) => {
    const classes = new Set();
    return {
      id: () => `tag:${index + 1}`,
      data: (key) => ({
        layer: "tag",
        graph_role: "community-hotspot",
        rank: index + 1,
      })[key],
      toggleClass(name, enabled) {
        if (enabled) classes.add(name);
        else classes.delete(name);
      },
      hasClass: (name) => classes.has(name),
    };
  });
  const nodes = [...communities, ...hotspots];
  engine.cy = { nodes: () => ({ forEach: (callback) => nodes.forEach(callback) }) };
  engine.expandedCommunityId = "community:5";

  engine._syncCommunityDensity("community", { width: 390, height: 290 });
  assert.equal(
    hotspots.filter((node) => !node.hasClass("community-compact-label-hidden")).length,
    6
  );

  engine._syncCommunityDensity("community", { width: 968, height: 640 });
  assert.equal(
    hotspots.filter((node) => node.hasClass("community-compact-label-hidden")).length,
    0
  );
});

test("the 720px bottom-sheet breakpoint keeps the selected community centered", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const communities = Array.from({ length: 11 }, (_, index) => ({
    id: `community:${index + 1}`,
    layer: "community",
    graph_role: index === 4 ? "community-anchor" : "community-context",
    rank: index + 1,
  }));
  const bounds = { width: 720, height: 640 };

  const positions = engine._communityPresetPositions(
    communities,
    bounds,
    "community:5"
  );
  const anchor = positions["community:5"];

  // graph.css uses @media (max-width: 720px), where the detail panel becomes a
  // bottom sheet. The graph must therefore not reserve a desktop drawer on the right.
  assert.ok(
    anchor.x >= bounds.width * 0.42 && anchor.x <= bounds.width * 0.58,
    `bottom-sheet detail must not pin the selected field left: ${anchor.x}`
  );
});

test("a narrow selected scene exposes only independent radius-bounded community fields", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const bounds = { width: 720, height: 640 };
  const rawNodes = Array.from({ length: 11 }, (_, index) => ({
    id: `community:${index + 1}`,
    layer: "community",
    graph_role: index === 4 ? "community-anchor" : "community-context",
    rank: index + 1,
    node_count: 72 - index * 3,
  }));
  const positions = engine._communityPresetPositions(
    rawNodes,
    bounds,
    "community:5"
  );
  const nodes = rawNodes.map((rawNode) => {
    const classes = new Set();
    return {
      id: () => rawNode.id,
      data: (key) => key === undefined ? rawNode : rawNode[key],
      renderedPosition: () => positions[rawNode.id],
      connectedEdges: () => ({ forEach() {} }),
      toggleClass(name, enabled) {
        if (enabled) classes.add(name);
        else classes.delete(name);
      },
      hasClass: (name) => classes.has(name),
    };
  });
  engine.cy = {
    nodes(selector) {
      const selectedNodes = selector === ":visible"
        ? nodes.filter((node) => !node.hasClass("community-compact-hidden"))
        : nodes;
      return { forEach: (callback) => selectedNodes.forEach(callback) };
    },
  };
  Object.assign(engine, {
    mode: "community",
    expandedCommunityId: "community:5",
    _fieldWidth: bounds.width,
    _fieldHeight: bounds.height,
  });

  engine._syncCommunityDensity("community", bounds);
  const descriptors = engine._fieldDescriptors();

  assert.equal(
    descriptors.length,
    5,
    "a selected compact scene should draw one anchor and four context fields"
  );
  assert.equal(
    new Set(descriptors.map(({ x, y }) => `${x}:${y}`)).size,
    descriptors.length,
    "community fields must have independent centers"
  );
  assert.ok(
    descriptors.every((descriptor) => descriptor.radius <= bounds.width * 0.16),
    `community field radius escaped the compact budget: ${descriptors.map((field) => field.radius)}`
  );
  for (let left = 0; left < descriptors.length; left += 1) {
    for (let right = left + 1; right < descriptors.length; right += 1) {
      const first = descriptors[left];
      const second = descriptors[right];
      const distance = Math.hypot(first.x - second.x, first.y - second.y);
      assert.ok(
        distance >= (first.radius + second.radius) * 0.82,
        `community fields ${first.id} and ${second.id} collapse into one contour mass`
      );
    }
  }
});

test("a 732px side-detail scene keeps four cluster fields around a visible anchor", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const bounds = { width: 732, height: 564 };
  const rawNodes = Array.from({ length: 11 }, (_, index) => ({
    id: `community:${index + 1}`,
    layer: "community",
    graph_role: index === 9 ? "community-anchor" : "community-context",
    rank: index + 1,
    node_count: 72 - index * 3,
  }));
  const positions = engine._communityPresetPositions(
    rawNodes,
    bounds,
    "community:10"
  );
  const nodes = rawNodes.map((rawNode) => {
    const classes = new Set();
    return {
      id: () => rawNode.id,
      data: (key) => key === undefined ? rawNode : rawNode[key],
      renderedPosition: () => positions[rawNode.id],
      connectedEdges: () => ({ forEach() {} }),
      toggleClass(name, enabled) {
        if (enabled) classes.add(name);
        else classes.delete(name);
      },
      hasClass: (name) => classes.has(name),
    };
  });
  engine.cy = {
    nodes(selector) {
      const selectedNodes = selector === ":visible"
        ? nodes.filter((node) => !node.hasClass("community-compact-hidden"))
        : nodes;
      return { forEach: (callback) => selectedNodes.forEach(callback) };
    },
  };
  Object.assign(engine, {
    mode: "community",
    expandedCommunityId: "community:10",
    _fieldWidth: bounds.width,
    _fieldHeight: bounds.height,
  });

  engine._syncCommunityDensity("community", bounds);
  const descriptors = engine._fieldDescriptors();
  const anchor = descriptors.find((descriptor) => descriptor.anchor);
  const contexts = descriptors.filter((descriptor) => !descriptor.anchor);

  assert.equal(descriptors.length, 5);
  assert.ok(anchor.x < bounds.width - 292, `anchor is hidden under detail panel: ${anchor.x}`);
  assert.ok(contexts.some((field) => field.x < anchor.x));
  assert.ok(contexts.some((field) => field.x > anchor.x));
  assert.ok(contexts.some((field) => field.y < anchor.y));
  assert.ok(contexts.some((field) => field.y > anchor.y));
  assert.equal(
    new Set(contexts.map((field) =>
      `${field.x < anchor.x ? "L" : "R"}${field.y < anchor.y ? "T" : "B"}`
    )).size,
    4,
    "compact context fields must occupy all four quadrants around the anchor"
  );
});

test("particle loop retains timestamps so highlighted-path particles advance", () => {
  const callbacks = [];
  const window = {
    document: { hidden: false },
    requestAnimationFrame(callback) {
      callbacks.push(callback);
      return callbacks.length;
    },
    cancelAnimationFrame() {},
  };
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const particle = {
    edgeId: "edge:flow",
    progress: 0.2,
    speed: 0.25,
    size: 2,
    reverse: false,
  };
  const context = {
    clearRect() {},
    save() {},
    restore() {},
    beginPath() {},
    arc() {},
    fill() {},
  };
  const edge = {
    length: 1,
    visible: () => true,
    renderedSourceEndpoint: () => ({ x: 0, y: 0 }),
    renderedTargetEndpoint: () => ({ x: 100, y: 0 }),
    renderedMidpoint: () => ({ x: 50, y: 0 }),
  };
  Object.assign(engine, {
    _particleFrame: null,
    _particleTimestamp: 0,
    _particleDirtyRects: [],
    _particles: [particle],
    _paused: false,
    reducedMotion: false,
    isDestroyed: false,
    _overlayContext: context,
    _overlayWidth: 200,
    _overlayHeight: 100,
    cy: { getElementById: () => edge },
  });

  engine._startParticleLoop();
  callbacks.shift()(1000);
  callbacks.shift()(1016);
  callbacks.shift()(1040);

  assert.ok(particle.progress > 0.2, `particle did not advance: ${particle.progress}`);
  assert.equal(engine._particleTimestamp, 1040);
});

test("community field coalesces high-frequency viewport events to its paint budget", () => {
  const callbacks = [];
  const window = {
    requestAnimationFrame(callback) {
      callbacks.push(callback);
      return callbacks.length;
    },
    cancelAnimationFrame() {},
  };
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  let paints = 0;
  Object.assign(engine, {
    _fieldContext: {},
    _fieldFrame: null,
    _fieldTimestamp: 0,
    _fieldDirty: false,
    _communityFields: [],
    _paused: false,
    isDestroyed: false,
    mode: "community",
    _drawCommunityField: () => { paints += 1; },
  });

  for (let timestamp = 16; timestamp <= 976; timestamp += 16) {
    engine._scheduleCommunityFieldDraw();
    const callback = callbacks.shift();
    if (callback) callback(timestamp);
  }

  assert.ok(paints > 0);
  assert.ok(paints <= 24, `paint budget exceeded: ${paints}`);
});

test("focus field remains demand-driven with reduced motion", () => {
  const callbacks = [];
  const window = {
    requestAnimationFrame(callback) {
      callbacks.push(callback);
      return callbacks.length;
    },
    cancelAnimationFrame() {},
  };
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  let paints = 0;
  Object.assign(engine, {
    _fieldContext: {},
    _fieldFrame: null,
    _fieldTimestamp: 0,
    _fieldDirty: false,
    _communityFields: [],
    _paused: false,
    reducedMotion: true,
    isDestroyed: false,
    mode: "focus",
    _drawCommunityField: () => { paints += 1; },
  });

  engine._scheduleCommunityFieldDraw();
  assert.equal(callbacks.length, 1);
  callbacks.shift()(16);
  assert.equal(paints, 1);
  assert.equal(callbacks.length, 0, "focus field must not create a continuous RAF loop");
  assert.equal(engine._fieldFrame, null);
  assert.equal(engine._fieldDirty, false);
});

test("clearSelection invalidates an in-flight view request", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  let cancelledOperation = null;
  Object.assign(engine, {
    isDestroyed: false,
    _modeSequence: 7,
    selectedNode: {},
    selectedNodeId: "community:5",
    hoveredNode: {},
    cy: {
      elements: () => ({ unselect() {} }),
      nodes: () => ({ removeClass() {} }),
    },
    _cancelOperation: (operation) => { cancelledOperation = operation; },
    _updateSemanticLabels() {},
    _clearHighlights() {},
    _emit() {},
  });

  engine.clearSelection();

  assert.equal(engine._modeSequence, 8);
  assert.equal(cancelledOperation, "view");
  assert.equal(engine.selectedNodeId, null);
});

test("engine cancels a stale view request before starting its replacement", async () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const messages = [];
  engine.isDestroyed = false;
  engine._requestSequence = 0;
  engine._pendingRequests = new Map();
  engine._operationRequests = new Map();
  engine.worker = { postMessage: (message) => messages.push(message) };

  const first = engine._request("focus", { nodeId: "community:1" }, {
    operationKey: "view",
    cancelPrevious: true,
  });
  const firstRejected = assert.rejects(first, (error) => error.name === "AbortError");
  const second = engine._request("focus", { nodeId: "community:2" }, {
    operationKey: "view",
    cancelPrevious: true,
  });

  assert.deepEqual(
    messages.map((message) => message.type),
    ["focus", "cancel", "focus"]
  );
  assert.equal(messages[1].payload.requestId, messages[0].id);
  engine._handleWorkerMessage({ id: messages[0].id, type: "cancelled" });
  engine._handleWorkerMessage({
    id: messages[2].id,
    type: "success",
    data: { node: { id: "community:2" } },
  });

  await firstRejected;
  assert.equal((await second).node.id, "community:2");
});

test("community insights expose real members and related communities", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  engine.currentGraph = {
    nodes: [
      {
        id: "community:rag",
        name: "RAG 应用",
        layer: "community",
        node_count: 20,
        member_ids: ["tag:vector", "tag:retrieval"],
      },
      {
        id: "community:model",
        name: "语言模型",
        layer: "community",
        node_count: 18,
      },
      {
        id: "tag:vector",
        name: "向量检索",
        layer: "tag",
        rank: 2,
        degree: 18,
        weighted_degree: 42,
        article_count: 9,
      },
      {
        id: "tag:retrieval",
        name: "重排序",
        layer: "tag",
        rank: 4,
        degree: 12,
        weighted_degree: 30,
        article_count: 7,
      },
    ],
    links: [
      {
        id: "edge:community",
        source: "community:rag",
        target: "community:model",
        type: "community",
        weight: 88,
      },
      {
        id: "edge:member:1",
        source: "community:rag",
        target: "tag:vector",
        type: "community-member",
        weight: 42,
      },
      {
        id: "edge:member:2",
        source: "community:rag",
        target: "tag:retrieval",
        type: "community-member",
        weight: 30,
      },
    ],
  };

  const insight = engine.getCommunityInsights("community:rag");
  assert.equal(insight.memberCount, 20);
  assert.equal(insight.visibleMembers, 2);
  assert.deepEqual(
    Array.from(insight.topMembers, (item) => item.name),
    ["向量检索", "重排序"]
  );
  assert.deepEqual(
    Array.from(insight.relatedCommunities, (item) => item.name),
    ["语言模型"]
  );
  assert.equal(insight.connectionStrength, 88);
});

test("community animation follows curved edges and respects the paint budget", () => {
  const window = {};
  vm.runInNewContext(ENGINE_SOURCE, { window }, {
    filename: "cytoscape-graph-engine.js",
  });
  const Engine = window.CytoscapeGraphEngine;
  const engine = Object.create(Engine.prototype);
  const edge = {
    renderedSourceEndpoint: () => ({ x: 0, y: 0 }),
    renderedMidpoint: () => ({ x: 50, y: 50 }),
    renderedTargetEndpoint: () => ({ x: 100, y: 0 }),
  };

  const midpoint = engine._pointOnRenderedEdge(edge, 0.5);
  assert.equal(midpoint.x, 50);
  assert.equal(midpoint.y, 50);
  engine._fieldTimestamp = 100;
  assert.equal(engine._shouldPaintCommunityFrame(120), false);
  assert.equal(engine._shouldPaintCommunityFrame(141), false);
  assert.equal(engine._shouldPaintCommunityFrame(142), true);
});
