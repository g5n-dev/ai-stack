(function lineageModule(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
    return;
  }
  root.AIStackLineage = Object.freeze(api);
  if (root.document) {
    const start = () => api.initializeArticleLineage(root.document, root);
    if (root.document.readyState === "loading") {
      root.document.addEventListener("DOMContentLoaded", start, { once: true });
    } else {
      start();
    }
  }
}(typeof globalThis !== "undefined" ? globalThis : this, function createLineageApi() {
  "use strict";

  const LINEAGE_ID = /^(?:obs|evt)_[0-9a-f]{64}$/u;
  const SHA256 = /^(?:sha256:)?[0-9a-f]{64}$/u;
  const BUCKET = /^[0-7][0-9a-f]$/u;
  const SAFE_PATH = /^(?:routes|clusters)\/[0-7][0-9a-f]-[0-9a-f]{16}\.json$/u;
  const ISO_TIMESTAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/u;
  const RELATIONS = Object.freeze([
    "original", "exact_copy", "syndicated", "derivative", "same_event", "related_only",
  ]);
  const RELATION_LABELS = Object.freeze({
    original: "最早观测",
    exact_copy: "完全重复",
    syndicated: "关联转载",
    derivative: "衍生解读",
    same_event: "同一事件",
    related_only: "相关报道",
  });
  const CONFIDENCE_LABELS = Object.freeze({
    publisher: "发布方时间",
    feed: "Feed 时间",
    platform: "平台时间",
    git: "首次归档时间",
    observed: "本站观测时间",
    unknown: "时间待核验",
  });
  const MAX_INDEX_BYTES = 64 * 1024;
  const MAX_SHARD_BYTES = 64 * 1024;
  const MAX_OBSERVATIONS = 50;
  const CANONICAL_ORIGIN = "https://ai-stack.site";
  const SENSITIVE_QUERY_TOKENS = Object.freeze(new Set([
    "auth", "authorization", "code", "credential", "jwt", "key", "password", "secret",
    "session", "sig", "signature", "sk", "token",
  ]));
  const SENSITIVE_QUERY_COMPOUNDS = Object.freeze(new Set([
    "accesstoken", "apikey", "authtoken", "awsaccesskeyid", "jwttoken", "sessionid",
    "signedurl",
  ]));

  class LineageDataError extends Error {
    constructor(message = "invalid lineage data") {
      super(message);
      this.name = "LineageDataError";
    }
  }

  function fail(reason) {
    throw new LineageDataError(`invalid lineage data: ${reason}`);
  }

  function plainObject(value) {
    if (value === null || typeof value !== "object" || Array.isArray(value)) return false;
    const prototype = Object.getPrototypeOf(value);
    return prototype === Object.prototype || prototype === null;
  }

  function exactFields(value, fields, context) {
    if (!plainObject(value)) fail(`${context} object`);
    const actual = Object.keys(value).sort();
    const expected = [...fields].sort();
    if (actual.length !== expected.length || actual.some((field, index) => field !== expected[index])) {
      fail(`${context} fields`);
    }
  }

  function safeInteger(value, context, minimum = 0, maximum = Number.MAX_SAFE_INTEGER) {
    if (!Number.isSafeInteger(value) || value < minimum || value > maximum) fail(context);
    return value;
  }

  function safeText(value, context, maximum = 300, allowEmpty = false) {
    if (typeof value !== "string" || Array.from(value).length > maximum) fail(context);
    const normalized = value.normalize("NFKC").trim().replace(/\s+/gu, " ");
    if ((!allowEmpty && !normalized) || /[\u0000-\u001f\u007f]/u.test(normalized)) fail(context);
    return normalized;
  }

  function timestamp(value, context, nullable = false) {
    if (nullable && value === null) return null;
    if (typeof value !== "string" || !ISO_TIMESTAMP.test(value) || !Number.isFinite(Date.parse(value))) {
      fail(context);
    }
    return value;
  }

  function lineageId(value, context) {
    if (typeof value !== "string" || !LINEAGE_ID.test(value)) fail(context);
    return value;
  }

  function normalizeBucket(value, context = "bucket") {
    if (typeof value !== "string" || !BUCKET.test(value)) fail(context);
    return value;
  }

  function bucketForId(value, bucketCount = 128) {
    const id = lineageId(value, "lineage id");
    if (bucketCount !== 128) fail("bucket count");
    return Number.parseInt(id.slice(4, 12), 16) % bucketCount;
  }

  function bucketKeyForId(value, bucketCount = 128) {
    return bucketForId(value, bucketCount).toString(16).padStart(2, "0");
  }

  function safeInternalUrl(value, context) {
    if (typeof value !== "string" || value.length > 2048 || !value.startsWith("/")) fail(context);
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

  function safeSourceUrl(value, context) {
    if (typeof value !== "string" || value.length > 4096) fail(context);
    let parsed;
    try {
      parsed = new URL(value);
    } catch (error) {
      fail(context);
    }
    if (!["http:", "https:"].includes(parsed.protocol) || parsed.username || parsed.password) fail(context);
    for (const key of parsed.searchParams.keys()) {
      const segmented = key.normalize("NFKC")
        .replace(/([A-Z]+)([A-Z][a-z])/gu, "$1_$2")
        .replace(/([a-z0-9])([A-Z])/gu, "$1_$2");
      const normalized = segmented.toLocaleLowerCase("en-US")
        .replace(/[^a-z0-9]+/gu, "_").replace(/^_+|_+$/gu, "");
      const tokens = normalized.split("_");
      const compact = normalized.replace(/_/gu, "");
      if (
        tokens.some((token) => SENSITIVE_QUERY_TOKENS.has(token))
        || SENSITIVE_QUERY_COMPOUNDS.has(compact)
      ) fail(context);
    }
    return parsed.href;
  }

  function deploymentBase(indexUrl) {
    const parsed = new URL(indexUrl, CANONICAL_ORIGIN);
    const suffix = "/data/lineage/index.json";
    if (!parsed.pathname.endsWith(suffix)) fail("index URL");
    const prefix = parsed.pathname.slice(0, -suffix.length);
    return `${prefix || ""}/`;
  }

  function withDeploymentBase(value, indexUrl) {
    if (value === null) return null;
    const path = safeInternalUrl(value, "article url");
    const base = deploymentBase(indexUrl);
    if (base === "/" || path.startsWith(base)) return path;
    return `${base.slice(0, -1)}${path}`;
  }

  function validateReference(value, kind) {
    exactFields(value, ["bucket", "path", "sha256", "bytes"], `${kind} reference`);
    const bucket = normalizeBucket(value.bucket, `${kind} bucket`);
    if (
      typeof value.path !== "string"
      || !SAFE_PATH.test(value.path)
      || !value.path.startsWith(`${kind}/${bucket}-`)
      || value.path.includes("..")
      || value.path.includes("//")
    ) fail(`${kind} path`);
    if (!SHA256.test(value.sha256 || "")) fail(`${kind} sha256`);
    return Object.freeze({
      bucket,
      path: value.path,
      sha256: value.sha256.replace(/^sha256:/u, ""),
      bytes: safeInteger(value.bytes, `${kind} bytes`, 2, MAX_SHARD_BYTES),
    });
  }

  function validateStats(value) {
    exactFields(value, [
      "observations", "events", "exact_copies", "syndicated", "derivatives", "same_event", "related_only",
    ], "stats");
    return Object.freeze(Object.fromEntries(Object.entries(value).map(([key, count]) => [
      key,
      safeInteger(count, `stats ${key}`, 0, 1000000),
    ])));
  }

  function validateIndex(value) {
    exactFields(value, [
      "version", "schema", "generated_at", "bucket_count", "bucket_algorithm", "stats",
      "route_buckets", "cluster_buckets",
    ], "index");
    if (
      value.version !== 1
      || value.schema !== "lineage_index_v1"
      || value.bucket_count !== 128
      || value.bucket_algorithm !== "sha256_prefix32_mod_v1"
    ) fail("index schema");
    if (!Array.isArray(value.route_buckets) || !Array.isArray(value.cluster_buckets)) fail("index buckets");
    const routeBuckets = value.route_buckets.map((item) => validateReference(item, "routes"));
    const clusterBuckets = value.cluster_buckets.map((item) => validateReference(item, "clusters"));
    for (const refs of [routeBuckets, clusterBuckets]) {
      const keys = refs.map((item) => item.bucket);
      if (new Set(keys).size !== keys.length) fail("duplicate bucket");
    }
    return Object.freeze({
      version: 1,
      schema: value.schema,
      generated_at: timestamp(value.generated_at, "index generated_at"),
      bucket_count: 128,
      bucket_algorithm: value.bucket_algorithm,
      stats: validateStats(value.stats),
      route_buckets: Object.freeze(routeBuckets),
      cluster_buckets: Object.freeze(clusterBuckets),
    });
  }

  function validateRouteShard(value, expectedBucket, indexUrl) {
    exactFields(value, ["version", "bucket", "routes"], "route shard");
    if (value.version !== 1 || normalizeBucket(value.bucket) !== expectedBucket || !Array.isArray(value.routes)) {
      fail("route shard identity");
    }
    const seen = new Set();
    const routes = value.routes.map((item) => {
      exactFields(item, ["observation_id", "event_id"], "route");
      const observationId = lineageId(item.observation_id, "route observation id");
      if (seen.has(observationId)) fail("duplicate route");
      seen.add(observationId);
      return Object.freeze({
        observation_id: observationId,
        event_id: lineageId(item.event_id, "route event id"),
      });
    });
    return Object.freeze(routes);
  }

  function validateObservation(value, indexUrl) {
    exactFields(value, [
      "observation_id", "title", "source", "source_url", "article_url", "relation",
      "parent_observation_id", "source_published_at", "first_seen_at", "timestamp_confidence",
    ], "observation");
    if (!RELATIONS.includes(value.relation)) fail("observation relation");
    const parent = value.parent_observation_id === null
      ? null
      : lineageId(value.parent_observation_id, "parent observation id");
    if (!Object.hasOwn(CONFIDENCE_LABELS, value.timestamp_confidence)) fail("timestamp confidence");
    return Object.freeze({
      observation_id: lineageId(value.observation_id, "observation id"),
      title: safeText(value.title, "observation title", 300),
      source: safeText(value.source, "observation source", 160),
      source_url: safeSourceUrl(value.source_url, "source url"),
      article_url: value.article_url === null ? null : withDeploymentBase(value.article_url, indexUrl),
      relation: value.relation,
      parent_observation_id: parent,
      source_published_at: timestamp(value.source_published_at, "source published at", true),
      first_seen_at: timestamp(value.first_seen_at, "first seen at"),
      timestamp_confidence: value.timestamp_confidence,
    });
  }

  function validateClusterShard(value, expectedBucket, indexUrl) {
    exactFields(value, ["version", "bucket", "clusters"], "cluster shard");
    if (value.version !== 1 || normalizeBucket(value.bucket) !== expectedBucket || !Array.isArray(value.clusters)) {
      fail("cluster shard identity");
    }
    return Object.freeze(value.clusters.map((item) => {
      exactFields(item, [
        "event_id", "event_aliases", "earliest_observed_id", "probable_origin_id",
        "representative_article_url", "observations", "lineage_links",
      ], "cluster");
      if (
        !Array.isArray(item.event_aliases)
        || !Array.isArray(item.observations)
        || !item.observations.length
        || !Array.isArray(item.lineage_links)
        || item.lineage_links.length > 6
      ) {
        fail("cluster members");
      }
      const observations = item.observations.map((entry) => (
        validateObservation(entry, indexUrl)
      ));
      const observationIds = new Set(observations.map((entry) => entry.observation_id));
      const earliest = lineageId(item.earliest_observed_id, "earliest observation id");
      const probable = lineageId(item.probable_origin_id, "probable origin id");
      if (!observationIds.has(earliest) || !observationIds.has(probable)) fail("cluster anchors");
      const lineageLinks = item.lineage_links.map((link) => {
        exactFields(link, ["from_observation_id", "relation", "target"], "lineage link");
        const from = lineageId(link.from_observation_id, "lineage link source");
        if (!observationIds.has(from) || !["derivative", "same_event", "related_only"].includes(link.relation)) {
          fail("lineage link relation");
        }
        const target = validateObservation(link.target, indexUrl);
        const source = observations.find((entry) => entry.observation_id === from);
        if (!source || source.parent_observation_id !== target.observation_id) fail("lineage link target");
        return Object.freeze({ from_observation_id: from, relation: link.relation, target });
      });
      return Object.freeze({
        event_id: lineageId(item.event_id, "cluster event id"),
        event_aliases: Object.freeze(item.event_aliases.map((alias) => lineageId(alias, "event alias"))),
        earliest_observed_id: earliest,
        probable_origin_id: probable,
        representative_article_url: item.representative_article_url === null
          ? null
          : withDeploymentBase(item.representative_article_url, indexUrl),
        observations: Object.freeze(observations),
        lineage_links: Object.freeze(lineageLinks),
      });
    }));
  }

  async function sha256Hex(bytes, cryptoObject = globalThis.crypto) {
    if (!cryptoObject?.subtle?.digest) fail("crypto unavailable");
    const digest = await cryptoObject.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  }

  async function fetchBytes(url, fetchFn, maximumBytes) {
    const response = await fetchFn(url, { credentials: "same-origin", cache: "no-cache" });
    if (!response?.ok) fail(`request ${response?.status || "failed"}`);
    const bytes = await response.arrayBuffer();
    if (!(bytes instanceof ArrayBuffer) || bytes.byteLength < 2 || bytes.byteLength > maximumBytes) {
      fail("asset byte budget");
    }
    return bytes;
  }

  function parseJson(bytes, context) {
    try {
      const value = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
      if (!plainObject(value)) fail(`${context} root`);
      return value;
    } catch (error) {
      if (error instanceof LineageDataError) throw error;
      fail(`${context} JSON`);
    }
  }

  async function fetchShard(indexUrl, reference, fetchFn, cryptoObject) {
    const url = new URL(reference.path, new URL(indexUrl, CANONICAL_ORIGIN)).href;
    const bytes = await fetchBytes(url, fetchFn, MAX_SHARD_BYTES);
    if (bytes.byteLength !== reference.bytes || await sha256Hex(bytes, cryptoObject) !== reference.sha256) {
      fail("shard integrity");
    }
    return parseJson(bytes, reference.path);
  }

  function projectCluster(cluster, observationId) {
    const current = cluster.observations.find((item) => item.observation_id === observationId);
    if (!current) fail("current observation missing from cluster");
    const completeTimeline = [...cluster.observations].sort((left, right) => {
      const leftTime = left.source_published_at || left.first_seen_at;
      const rightTime = right.source_published_at || right.first_seen_at;
      return leftTime.localeCompare(rightTime) || left.observation_id.localeCompare(right.observation_id);
    });
    let timeline = completeTimeline.slice(0, MAX_OBSERVATIONS);
    if (!timeline.some((item) => item.observation_id === observationId)) {
      timeline = [...timeline.slice(0, MAX_OBSERVATIONS - 1), current].sort((left, right) => {
        const leftTime = left.source_published_at || left.first_seen_at;
        const rightTime = right.source_published_at || right.first_seen_at;
        return leftTime.localeCompare(rightTime) || left.observation_id.localeCompare(right.observation_id);
      });
    }
    return Object.freeze({
      event_id: cluster.event_id,
      earliest_observed_id: cluster.earliest_observed_id,
      probable_origin_id: cluster.probable_origin_id,
      representative_article_url: cluster.representative_article_url,
      current,
      timeline: Object.freeze(timeline),
      lineage_links: Object.freeze(
        (cluster.lineage_links || [])
          .filter((item) => item.from_observation_id === observationId)
          .slice(0, 6),
      ),
      summary: Object.freeze({
        observation_count: completeTimeline.length,
        source_count: new Set(completeTimeline.map((item) => item.source)).size,
        earliest: completeTimeline.find((item) => item.observation_id === cluster.earliest_observed_id),
        probable_origin: completeTimeline.find((item) => item.observation_id === cluster.probable_origin_id),
      }),
    });
  }

  async function loadLineage({
    indexUrl,
    observationId,
    baseUrl = CANONICAL_ORIGIN,
    fetchFn = globalThis.fetch?.bind(globalThis),
    cryptoObject = globalThis.crypto,
    signal,
  }) {
    lineageId(observationId, "observation id");
    if (typeof fetchFn !== "function") fail("fetch unavailable");
    const absoluteIndexUrl = new URL(indexUrl, baseUrl).href;
    const indexBytes = await fetchBytes(absoluteIndexUrl, (url, options) => (
      fetchFn(url, { ...options, signal })
    ), MAX_INDEX_BYTES);
    const index = validateIndex(parseJson(indexBytes, "index"));
    const routeBucket = bucketKeyForId(observationId, index.bucket_count);
    const routeRef = index.route_buckets.find((item) => item.bucket === routeBucket);
    if (!routeRef) fail("observation route bucket missing");
    const routePayload = await fetchShard(
      absoluteIndexUrl,
      routeRef,
      (url, options) => fetchFn(url, { ...options, signal }),
      cryptoObject,
    );
    const routes = validateRouteShard(routePayload, routeBucket, absoluteIndexUrl);
    const route = routes.find((item) => item.observation_id === observationId);
    if (!route) fail("observation route missing");
    const clusterBucket = bucketKeyForId(route.event_id, index.bucket_count);
    const clusterRef = index.cluster_buckets.find((item) => item.bucket === clusterBucket);
    if (!clusterRef) fail("event cluster bucket missing");
    const clusterPayload = await fetchShard(
      absoluteIndexUrl,
      clusterRef,
      (url, options) => fetchFn(url, { ...options, signal }),
      cryptoObject,
    );
    const clusters = validateClusterShard(clusterPayload, clusterBucket, absoluteIndexUrl);
    const cluster = clusters.find((item) => item.event_id === route.event_id);
    if (!cluster) fail("event cluster missing");
    return projectCluster(cluster, observationId);
  }

  function appendText(document, parent, tagName, className, text) {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    element.textContent = String(text ?? "");
    parent.append(element);
    return element;
  }

  function formatDate(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "时间待核验";
    return new Intl.DateTimeFormat("zh-CN", {
      year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit",
      hour12: false,
    }).format(date);
  }

  function renderLineage(document, card, data) {
    const content = card.querySelector("[data-lineage-content]");
    if (!content) return;
    content.replaceChildren();
    const summary = document.createElement("div");
    summary.className = "lineage-summary";
    const source = data.summary.earliest?.source || "来源待核验";
    [
      ["本站观测", `${data.summary.observation_count} 条`],
      ["独立来源", `${data.summary.source_count} 个`],
      ["最早观测", source],
      ["当前角色", RELATION_LABELS[data.current.relation]],
    ].forEach(([label, value]) => {
      const cell = document.createElement("div");
      appendText(document, cell, "dt", "", label);
      appendText(document, cell, "dd", "", value);
      summary.append(cell);
    });
    content.append(summary);

    const timeline = document.createElement("ol");
    timeline.className = "lineage-timeline";
    data.timeline.forEach((item, position) => {
      const row = document.createElement("li");
      row.className = `lineage-node lineage-node--${item.relation}`;
      if (item.observation_id === data.current.observation_id) {
        row.classList.add("is-current");
        row.setAttribute("aria-current", "true");
      }
      const ordinal = appendText(document, row, "span", "lineage-node__ordinal", String(position + 1).padStart(2, "0"));
      ordinal.setAttribute("aria-hidden", "true");
      const link = document.createElement("a");
      link.className = "lineage-node__article";
      link.href = item.article_url || item.source_url;
      if (!item.article_url) {
        link.target = "_blank";
        link.rel = "noopener noreferrer nofollow";
      }
      appendText(document, link, "strong", "", item.title);
      const meta = document.createElement("span");
      meta.className = "lineage-node__meta";
      appendText(document, meta, "span", "lineage-node__relation", RELATION_LABELS[item.relation]);
      appendText(document, meta, "span", "", item.source);
      const observedAt = item.source_published_at || item.first_seen_at;
      const time = appendText(document, meta, "time", "", formatDate(observedAt));
      time.dateTime = observedAt;
      link.append(meta);
      row.append(link);
      const sourceLink = document.createElement("a");
      sourceLink.className = "lineage-node__source";
      sourceLink.href = item.source_url;
      sourceLink.target = "_blank";
      sourceLink.rel = "noopener noreferrer nofollow";
      sourceLink.textContent = CONFIDENCE_LABELS[item.timestamp_confidence];
      row.append(sourceLink);
      timeline.append(row);
    });
    content.append(timeline);
    if (data.lineage_links.length) {
      appendText(document, content, "h3", "lineage-related__heading", "关联来源");
      const related = document.createElement("ul");
      related.className = "lineage-related";
      data.lineage_links.forEach((item) => {
        const row = document.createElement("li");
        row.className = `lineage-related__item lineage-node--${item.relation}`;
        const link = document.createElement("a");
        link.className = "lineage-related__link";
        link.href = item.target.article_url || item.target.source_url;
        if (!item.target.article_url) {
          link.target = "_blank";
          link.rel = "noopener noreferrer nofollow";
        }
        appendText(document, link, "strong", "", item.target.title);
        appendText(
          document,
          link,
          "span",
          "lineage-related__meta",
          `${RELATION_LABELS[item.relation]} · ${item.target.source}`,
        );
        row.append(link);
        related.append(row);
      });
      content.append(related);
    }
    card.dataset.lineageState = "ready";
  }

  function initializeArticleLineage(document, windowObject = globalThis) {
    const card = document.querySelector?.("[data-lineage-card]");
    if (!card || card.dataset.lineageReady === "true") return null;
    const observationId = card.dataset.observationId || "";
    if (!LINEAGE_ID.test(observationId)) return null;
    card.dataset.lineageReady = "true";
    const status = card.querySelector("[data-lineage-status]");
    const trigger = card.querySelector("[data-lineage-load]");
    let controller = null;
    let promise = null;
    let observer = null;

    function setStatus(message, state = "loading") {
      if (status) status.textContent = message;
      card.dataset.lineageState = state;
    }

    function load() {
      if (promise) return promise;
      setStatus("正在核验来源链…");
      controller = new windowObject.AbortController();
      promise = loadLineage({
        indexUrl: card.dataset.indexUrl,
        observationId,
        baseUrl: windowObject.location?.href || CANONICAL_ORIGIN,
        fetchFn: windowObject.fetch.bind(windowObject),
        cryptoObject: windowObject.crypto,
        signal: controller.signal,
      }).then((data) => {
        setStatus("来源链已核验", "ready");
        renderLineage(document, card, data);
        return data;
      }).catch((error) => {
        if (error?.name === "AbortError") return null;
        setStatus("溯源数据暂不可用，正文阅读不受影响。", "error");
        return null;
      });
      return promise;
    }

    trigger?.addEventListener("click", load);
    if (windowObject.location?.hash === "#intelligence-lineage") {
      load().then(() => card.focus?.({ preventScroll: true }));
    } else if (typeof windowObject.IntersectionObserver === "function") {
      observer = new windowObject.IntersectionObserver((entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          observer.disconnect();
          load();
        }
      }, { rootMargin: "240px 0px" });
      observer.observe(card);
    }

    return Object.freeze({
      load,
      destroy() {
        observer?.disconnect();
        controller?.abort();
        trigger?.removeEventListener("click", load);
        card.removeAttribute("data-lineage-ready");
      },
    });
  }

  return {
    LineageDataError,
    bucketForId,
    bucketKeyForId,
    initializeArticleLineage,
    loadLineage,
    projectCluster,
    relationLabel(value) { return RELATION_LABELS[value] || "关系待核验"; },
    validateIndex,
    withDeploymentBase,
  };
}));
