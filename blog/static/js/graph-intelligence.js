(function graphIntelligenceModule(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
    return;
  }
  root.AIStackGraphIntelligence = Object.freeze(api);
}(typeof globalThis !== "undefined" ? globalThis : this, function createGraphIntelligenceApi() {
  "use strict";

  const INDEX_SCHEMAS = new Set(["stack_trends_index_v1", "stack_trends_index_v2"]);
  const TOPIC_SCHEMAS = new Set(["stack_trends_topic_v1", "stack_trends_topic_v2"]);
  const NODE_ID = /^tag:[^\u0000-\u001f\u007f<>]{1,220}$/u;
  const SHA256 = /^[0-9a-f]{64}$/u;
  const SAFE_TOPIC_PATH = /^topics\/[a-z0-9][a-z0-9._-]{0,180}\.json$/u;
  const LINEAGE_RELATIONS = new Set([
    "original", "exact_copy", "syndicated", "derivative", "same_event", "related_only",
  ]);
  const MAX_INDEX_BYTES = 64 * 1024;
  const MAX_TOPIC_BYTES = 64 * 1024;
  const MAX_ARTICLES = 6;
  const CANONICAL_ORIGIN = "https://ai-stack.site";

  class GraphIntelligenceError extends Error {
    constructor(message) {
      super(message);
      this.name = "GraphIntelligenceError";
    }
  }

  function fail(reason) {
    throw new GraphIntelligenceError(`invalid trend intelligence: ${reason}`);
  }

  function text(value, context, maximum = 320, allowEmpty = false) {
    if (typeof value !== "string" || Array.from(value).length > maximum) fail(context);
    const normalized = value.normalize("NFKC").trim().replace(/\s+/gu, " ");
    if ((!allowEmpty && !normalized) || /[\u0000-\u001f\u007f]/u.test(normalized)) fail(context);
    return normalized;
  }

  function internalUrl(value, context) {
    if (typeof value !== "string" || !value.startsWith("/") || value.length > 2048) fail(context);
    let parsed;
    try {
      parsed = new URL(value, CANONICAL_ORIGIN);
    } catch (error) {
      fail(context);
    }
    if (
      parsed.origin !== CANONICAL_ORIGIN
      || /[\u0000-\u001f\u007f<>\\]/u.test(value)
      || parsed.pathname.split("/").includes("..")
    ) fail(context);
    return `${parsed.pathname}${parsed.search}${parsed.hash}`;
  }

  function deploymentBase(indexUrl) {
    const url = new URL(indexUrl, CANONICAL_ORIGIN);
    const suffix = "/data/stack-trends/index.json";
    if (!url.pathname.endsWith(suffix)) fail("index url");
    return `${url.pathname.slice(0, -suffix.length) || ""}/`;
  }

  function deployedUrl(value, indexUrl) {
    const path = internalUrl(value, "article url");
    const base = deploymentBase(indexUrl);
    if (base === "/" || path.startsWith(base)) return path;
    return `${base.slice(0, -1)}${path}`;
  }

  function safeReference(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) fail("topic reference");
    if (
      typeof value.path !== "string"
      || !SAFE_TOPIC_PATH.test(value.path)
      || value.path.includes("..")
      || !SHA256.test(value.sha256 || "")
      || !Number.isSafeInteger(value.bytes)
      || value.bytes < 2
      || value.bytes > MAX_TOPIC_BYTES
    ) fail("topic reference");
    return value;
  }

  async function sha256(bytes) {
    const cryptoApi = typeof globalThis !== "undefined" ? globalThis.crypto : null;
    if (!cryptoApi?.subtle) throw new GraphIntelligenceError("integrity API unavailable");
    const digest = await cryptoApi.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  }

  async function fetchBytes(url, fetchFn, maximum, expected, signal) {
    const response = await fetchFn(url, { credentials: "same-origin", cache: "no-cache", signal });
    if (!response?.ok) throw new GraphIntelligenceError(`request failed (${response?.status || 0})`);
    const bytes = new Uint8Array(await response.arrayBuffer());
    if (bytes.byteLength < 2 || bytes.byteLength > maximum) fail("asset size");
    if (expected) {
      if (bytes.byteLength !== expected.bytes || await sha256(bytes) !== expected.sha256) {
        throw new GraphIntelligenceError("trend shard integrity mismatch");
      }
    }
    return bytes;
  }

  function parseJson(bytes, context) {
    try {
      return JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
    } catch (error) {
      fail(`${context} json`);
    }
  }

  function validateIndex(value, nodeId) {
    if (!value || typeof value !== "object" || !INDEX_SCHEMAS.has(value.schema_version)) fail("index schema");
    if (!value.topics || typeof value.topics !== "object" || Array.isArray(value.topics)) fail("topics index");
    return safeReference(value.topics[nodeId]);
  }

  function article(value, indexUrl, v2) {
    if (!value || typeof value !== "object" || Array.isArray(value)) fail("evidence");
    const relation = v2 ? value.relation : "original";
    if (!LINEAGE_RELATIONS.has(relation)) fail("evidence relation");
    const articleUrl = deployedUrl(value.internal_url, indexUrl);
    return Object.freeze({
      title: text(value.title, "evidence title"),
      source: text(value.source, "evidence source", 160),
      published_at: text(value.published_at, "evidence time", 40),
      role: relation,
      associated_observations: v2 && Number.isSafeInteger(value.associated_observations)
        ? Math.max(1, value.associated_observations)
        : 1,
      article_url: articleUrl,
      lineage_url: `${articleUrl.split("#", 1)[0]}#intelligence-lineage`,
    });
  }

  function validateTopic(value, nodeId, indexUrl) {
    if (!value || typeof value !== "object" || !TOPIC_SCHEMAS.has(value.schema_version)) fail("topic schema");
    if (value.id !== nodeId || value.graph_node_id !== nodeId || !Array.isArray(value.evidence)) fail("topic identity");
    const v2 = value.schema_version === "stack_trends_topic_v2";
    return Object.freeze(value.evidence.slice(0, MAX_ARTICLES).map((item) => article(item, indexUrl, v2)));
  }

  async function loadNodeIntelligence(options = {}) {
    const nodeId = typeof options.nodeId === "string" ? options.nodeId : "";
    if (!NODE_ID.test(nodeId) || nodeId !== nodeId.trim()) fail("node id");
    const fetchFn = options.fetchFn || globalThis.fetch?.bind(globalThis);
    if (typeof fetchFn !== "function") throw new GraphIntelligenceError("fetch is unavailable");
    const indexUrl = new URL(options.indexUrl, options.baseUrl || globalThis.location?.href || CANONICAL_ORIGIN).href;
    const index = parseJson(await fetchBytes(indexUrl, fetchFn, MAX_INDEX_BYTES, null, options.signal), "index");
    const reference = validateIndex(index, nodeId);
    const topicUrl = new URL(reference.path, indexUrl).href;
    const topic = parseJson(await fetchBytes(topicUrl, fetchFn, MAX_TOPIC_BYTES, reference, options.signal), "topic");
    const articles = validateTopic(topic, nodeId, indexUrl);
    const trend = new URL("trends/", new URL(deploymentBase(indexUrl), new URL(indexUrl).origin));
    trend.searchParams.set("window", "30d");
    trend.searchParams.set("topic", nodeId);
    return Object.freeze({
      node_id: nodeId,
      articles,
      trend_url: `${trend.pathname}${trend.search}`,
    });
  }

  return {
    GraphIntelligenceError,
    loadNodeIntelligence,
  };
}));
