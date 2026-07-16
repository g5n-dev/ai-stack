(function trendsModule(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
    return;
  }

  root.AIStackTrends = Object.freeze(api);
  if (root.document) {
    const start = () => api.initializeTrendsPage(root.document, root);
    if (root.document.readyState === "loading") {
      root.document.addEventListener("DOMContentLoaded", start, { once: true });
    } else {
      start();
    }
  }
}(typeof globalThis !== "undefined" ? globalThis : this, function createTrendsApi() {
  "use strict";

  const INDEX_SCHEMA = "stack_trends_index_v1";
  const WINDOW_SCHEMA = "stack_trends_window_v1";
  const TOPIC_SCHEMA = "stack_trends_topic_v1";
  const WINDOWS = Object.freeze(["24h", "7d", "30d"]);
  const SIGNALS = Object.freeze(["all", "new", "rising", "steady", "cooling"]);
  const VIEWS = Object.freeze(["matrix", "list"]);
  const COMPONENTS = Object.freeze([
    "quantity",
    "growth",
    "acceleration",
    "source_diversity",
    "novelty",
    "source_weight",
  ]);
  const COMPONENT_LABELS = Object.freeze({
    quantity: "证据数量",
    growth: "增长幅度",
    acceleration: "增长加速度",
    source_diversity: "来源多样性",
    novelty: "主题新颖度",
    source_weight: "来源权重",
  });
  const STATE_LABELS = Object.freeze({
    new: "新出现",
    rising: "上升",
    steady: "稳定",
    cooling: "降温",
  });
  const CONFIDENCE_LABELS = Object.freeze({ high: "高置信", medium: "中等置信" });
  const WINDOW_LABELS = Object.freeze({ "24h": "24 小时", "7d": "7 天", "30d": "30 天" });
  const SOURCE_LABELS = Object.freeze({
    blogs_podcasts: "博客与播客",
    hacker_news: "Hacker News",
    juejin: "掘金",
    arxiv: "arXiv",
    github_trending: "GitHub Trending",
  });
  const MAX_INDEX_BYTES = 64 * 1024;
  const MAX_WINDOW_BYTES = 128 * 1024;
  const MAX_TOPIC_BYTES = 96 * 1024;
  const MAX_TOPICS = 100;
  const MAX_TRENDS = 24;
  const MAX_EVIDENCE = 30;
  const MAX_FACETS = 100;
  const MAX_TEXT = 400;
  const SHA256 = /^[0-9a-f]{64}$/u;
  const ISO_TIMESTAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/u;
  const TOPIC_ID = /^tag:[^\u0000-\u001f\u007f<>]{1,200}$/u;
  const SAFE_PATH = /^(?:windows|topics)\/[a-z0-9][a-z0-9._/-]{0,220}\.json$/u;
  const CANONICAL_ORIGIN = "https://ai-stack.site";
  const GRAPH_ROUTE = "/scenarios/";

  class TrendDataError extends Error {
    constructor(message = "invalid trend data") {
      super(message);
      this.name = "TrendDataError";
    }
  }

  function fail(reason) {
    throw new TrendDataError(`invalid trend data: ${reason}`);
  }

  function isPlainObject(value) {
    if (value === null || typeof value !== "object" || Array.isArray(value)) return false;
    const prototype = Object.getPrototypeOf(value);
    return prototype === Object.prototype || prototype === null;
  }

  function hasExactFields(value, fields) {
    if (!isPlainObject(value)) return false;
    const actual = Object.keys(value).sort();
    const expected = [...fields].sort();
    return actual.length === expected.length
      && actual.every((field, index) => field === expected[index]);
  }

  function assertExactFields(value, fields, context) {
    if (!hasExactFields(value, fields)) fail(`${context} fields`);
  }

  function finiteNumber(value, context, minimum = 0, maximum = Number.MAX_SAFE_INTEGER) {
    if (
      typeof value !== "number"
      || !Number.isFinite(value)
      || value < minimum
      || value > maximum
    ) fail(context);
    return value;
  }

  function safeInteger(value, context, minimum = 0, maximum = Number.MAX_SAFE_INTEGER) {
    if (!Number.isSafeInteger(value) || value < minimum || value > maximum) fail(context);
    return value;
  }

  function canonicalText(value, context, maximum = MAX_TEXT, allowEmpty = false) {
    if (typeof value !== "string" || Array.from(value).length > maximum) fail(context);
    const normalized = value.normalize("NFKC").trim().replace(/\s+/gu, " ");
    if ((!allowEmpty && !normalized) || /[\u0000-\u001f\u007f<>]/u.test(normalized)) fail(context);
    return normalized;
  }

  function timestamp(value, context) {
    if (typeof value !== "string" || !ISO_TIMESTAMP.test(value) || !Number.isFinite(Date.parse(value))) {
      fail(context);
    }
    return value;
  }

  function topicId(value, context = "topic id") {
    if (typeof value !== "string" || !TOPIC_ID.test(value) || value !== value.trim()) fail(context);
    return value;
  }

  function safeAssetPath(value, context = "asset path") {
    if (
      typeof value !== "string"
      || !SAFE_PATH.test(value)
      || value.includes("..")
      || value.includes("//")
      || value.includes("\\")
    ) fail(context);
    return value;
  }

  function validateRef(value, context, maximumBytes) {
    assertExactFields(value, ["path", "sha256", "bytes"], context);
    const path = safeAssetPath(value.path, `${context} path`);
    if (!SHA256.test(value.sha256 || "")) fail(`${context} sha256`);
    const bytes = safeInteger(value.bytes, `${context} bytes`, 2, maximumBytes);
    return Object.freeze({ path, sha256: value.sha256, bytes });
  }

  function validateWindowRef(value, context) {
    assertExactFields(value, ["path", "sha256", "bytes", "trend_count"], context);
    const ref = validateRef(
      { path: value.path, sha256: value.sha256, bytes: value.bytes },
      context,
      MAX_WINDOW_BYTES,
    );
    const trendCount = safeInteger(value.trend_count, `${context} trend_count`, 0, MAX_TRENDS);
    return Object.freeze({ ...ref, trend_count: trendCount });
  }

  function validateNormalization(value) {
    assertExactFields(value, [
      "quantity_target_unique_events",
      "growth_neutral",
      "acceleration_neutral",
      "component_range",
      "score_range",
    ], "normalization");
    safeInteger(value.quantity_target_unique_events, "normalization quantity target", 1, 1000);
    finiteNumber(value.growth_neutral, "normalization growth neutral", 0, 1);
    finiteNumber(value.acceleration_neutral, "normalization acceleration neutral", 0, 1);
    if (
      !Array.isArray(value.component_range)
      || value.component_range.length !== 2
      || value.component_range[0] !== 0
      || value.component_range[1] !== 1
      || !Array.isArray(value.score_range)
      || value.score_range.length !== 2
      || value.score_range[0] !== 0
      || value.score_range[1] !== 100
    ) fail("normalization ranges");
    return Object.freeze({
      quantity_target_unique_events: value.quantity_target_unique_events,
      growth_neutral: value.growth_neutral,
      acceleration_neutral: value.acceleration_neutral,
      component_range: Object.freeze([0, 1]),
      score_range: Object.freeze([0, 100]),
    });
  }

  function validateStatsWindow(value, context) {
    assertExactFields(value, ["trend_count", "evidence_articles", "source_count"], context);
    return Object.freeze({
      trend_count: safeInteger(value.trend_count, `${context} trend_count`, 0, MAX_TRENDS),
      evidence_articles: safeInteger(value.evidence_articles, `${context} evidence_articles`, 0, 100000),
      source_count: safeInteger(value.source_count, `${context} source_count`, 0, 10000),
    });
  }

  function validateStats(value) {
    assertExactFields(value, ["eligible_articles", "topic_count", "source_count", "windows"], "stats");
    assertExactFields(value.windows, WINDOWS, "stats windows");
    return Object.freeze({
      eligible_articles: safeInteger(value.eligible_articles, "stats eligible_articles", 0, 100000),
      topic_count: safeInteger(value.topic_count, "stats topic_count", 0, MAX_TOPICS),
      source_count: safeInteger(value.source_count, "stats source_count", 0, 10000),
      windows: Object.freeze(Object.fromEntries(
        WINDOWS.map((name) => [name, validateStatsWindow(value.windows[name], `stats ${name}`)]),
      )),
    });
  }

  function validateIndex(value) {
    assertExactFields(value, [
      "schema_version",
      "generated_at",
      "data_as_of",
      "realtime",
      "timezone",
      "default_window",
      "disclaimer",
      "formula",
      "normalization",
      "stats",
      "windows",
      "topics",
    ], "index");
    if (value.schema_version !== INDEX_SCHEMA) fail("index schema");
    const generatedAt = timestamp(value.generated_at, "index generated_at");
    const dataAsOf = timestamp(value.data_as_of, "index data_as_of");
    if (generatedAt !== dataAsOf || value.realtime !== false) fail("index cutoff");
    if (value.timezone !== "Asia/Shanghai" || value.default_window !== "30d") fail("index defaults");
    const disclaimer = canonicalText(value.disclaimer, "index disclaimer", 240);
    const formula = canonicalText(value.formula, "index formula", 500);
    const normalization = validateNormalization(value.normalization);
    const stats = validateStats(value.stats);
    assertExactFields(value.windows, WINDOWS, "index windows");
    const windows = Object.freeze(Object.fromEntries(
      WINDOWS.map((name) => [name, validateWindowRef(value.windows[name], `index ${name}`)]),
    ));
    if (!isPlainObject(value.topics)) fail("index topics");
    const topicEntries = Object.entries(value.topics);
    if (topicEntries.length === 0 || topicEntries.length > MAX_TOPICS) fail("index topics count");
    const topics = Object.create(null);
    for (const [id, ref] of topicEntries) {
      topicId(id, "index topic id");
      topics[id] = validateRef(ref, `index topic ${id}`, MAX_TOPIC_BYTES);
    }
    if (topicEntries.length !== stats.topic_count) fail("index topic count mismatch");
    return Object.freeze({
      schema_version: INDEX_SCHEMA,
      generated_at: generatedAt,
      data_as_of: dataAsOf,
      realtime: false,
      timezone: value.timezone,
      default_window: value.default_window,
      disclaimer,
      formula,
      normalization,
      stats,
      windows,
      topics: Object.freeze(topics),
    });
  }

  function validateFacet(value, context) {
    assertExactFields(value, ["name", "count"], context);
    return Object.freeze({
      name: canonicalText(value.name, `${context} name`, 160),
      count: safeInteger(value.count, `${context} count`, 1, 100000),
    });
  }

  function validateFacetArray(value, context, maximum = MAX_FACETS) {
    if (!Array.isArray(value) || value.length > maximum) fail(context);
    const seen = new Set();
    const result = value.map((item, index) => {
      const facet = validateFacet(item, `${context}[${index}]`);
      const key = facet.name.normalize("NFKC").toLocaleLowerCase("zh-CN");
      if (seen.has(key)) fail(`${context} duplicate`);
      seen.add(key);
      return facet;
    });
    return Object.freeze(result);
  }

  function validateCounts(value, context) {
    assertExactFields(value, ["current", "previous", "pre_previous"], context);
    return Object.freeze({
      current: safeInteger(value.current, `${context} current`, 0, 100000),
      previous: safeInteger(value.previous, `${context} previous`, 0, 100000),
      pre_previous: safeInteger(value.pre_previous, `${context} pre_previous`, 0, 100000),
    });
  }

  function validateComponents(value, context) {
    assertExactFields(value, COMPONENTS, context);
    return Object.freeze(Object.fromEntries(
      COMPONENTS.map((name) => [name, finiteNumber(value[name], `${context} ${name}`, 0, 1)]),
    ));
  }

  function validateSparkline(value, context) {
    if (!Array.isArray(value) || value.length !== 12) fail(context);
    return Object.freeze(value.map((count, index) => (
      safeInteger(count, `${context}[${index}]`, 0, 100000)
    )));
  }

  function validateSignal(value, context) {
    if (!SIGNALS.slice(1).includes(value)) fail(context);
    return value;
  }

  function validateConfidence(value, context) {
    if (!["high", "medium"].includes(value)) fail(context);
    return value;
  }

  function validateTrend(value, context) {
    assertExactFields(value, [
      "id",
      "topic",
      "graph_node_id",
      "score",
      "state",
      "confidence",
      "unique_events",
      "observations",
      "unique_sources",
      "duplicate_rate",
      "counts",
      "components",
      "sparkline",
      "sources",
      "scenarios",
      "detail_path",
    ], context);
    const id = topicId(value.id, `${context} id`);
    if (value.graph_node_id !== id) fail(`${context} graph node`);
    return Object.freeze({
      id,
      topic: canonicalText(value.topic, `${context} topic`, 200),
      graph_node_id: id,
      score: finiteNumber(value.score, `${context} score`, 0, 100),
      state: validateSignal(value.state, `${context} state`),
      confidence: validateConfidence(value.confidence, `${context} confidence`),
      unique_events: safeInteger(value.unique_events, `${context} unique_events`, 3, 100000),
      observations: safeInteger(value.observations, `${context} observations`, 3, 1000000),
      unique_sources: safeInteger(value.unique_sources, `${context} unique_sources`, 1, 10000),
      duplicate_rate: finiteNumber(value.duplicate_rate, `${context} duplicate_rate`, 0, 1),
      counts: validateCounts(value.counts, `${context} counts`),
      components: validateComponents(value.components, `${context} components`),
      sparkline: validateSparkline(value.sparkline, `${context} sparkline`),
      sources: validateFacetArray(value.sources, `${context} sources`),
      scenarios: validateFacetArray(value.scenarios, `${context} scenarios`),
      detail_path: safeAssetPath(value.detail_path, `${context} detail_path`),
    });
  }

  function validateWindow(value, expectedWindow, index) {
    assertExactFields(value, [
      "schema_version",
      "window",
      "data_as_of",
      "minimum_unique_events",
      "formula",
      "sample_notice",
      "facets",
      "trends",
    ], "window");
    if (value.schema_version !== WINDOW_SCHEMA || value.window !== expectedWindow || !WINDOWS.includes(value.window)) {
      fail("window schema");
    }
    const dataAsOf = timestamp(value.data_as_of, "window data_as_of");
    if (index && (dataAsOf !== index.data_as_of || value.formula !== index.formula)) fail("window basis");
    const formula = canonicalText(value.formula, "window formula", 500);
    if (value.sample_notice !== null && typeof value.sample_notice !== "string") fail("window sample_notice");
    const sampleNotice = value.sample_notice === null
      ? null
      : canonicalText(value.sample_notice, "window sample_notice", 240);
    assertExactFields(value.facets, ["sources", "scenarios"], "window facets");
    if (!Array.isArray(value.trends) || value.trends.length > MAX_TRENDS) fail("window trends");
    const trends = value.trends.map((item, position) => validateTrend(item, `trend[${position}]`));
    const seen = new Set();
    let previousScore = Number.POSITIVE_INFINITY;
    for (const item of trends) {
      if (seen.has(item.id) || item.score > previousScore) fail("window trend order");
      seen.add(item.id);
      previousScore = item.score;
      if (index) {
        const ref = index.topics[item.id];
        if (!ref || ref.path !== item.detail_path) fail("window detail reference");
      }
    }
    if (index && trends.length !== index.windows[expectedWindow].trend_count) fail("window trend count");
    return Object.freeze({
      schema_version: WINDOW_SCHEMA,
      window: value.window,
      data_as_of: dataAsOf,
      minimum_unique_events: safeInteger(value.minimum_unique_events, "window minimum", 1, 100),
      formula,
      sample_notice: sampleNotice,
      facets: Object.freeze({
        sources: validateFacetArray(value.facets.sources, "window source facets"),
        scenarios: validateFacetArray(value.facets.scenarios, "window scenario facets"),
      }),
      trends: Object.freeze(trends),
    });
  }

  function validateTopicWindow(value, context) {
    if (value === null) return null;
    assertExactFields(value, [
      "score",
      "state",
      "confidence",
      "unique_events",
      "unique_sources",
      "counts",
      "sparkline",
    ], context);
    return Object.freeze({
      score: finiteNumber(value.score, `${context} score`, 0, 100),
      state: validateSignal(value.state, `${context} state`),
      confidence: validateConfidence(value.confidence, `${context} confidence`),
      unique_events: safeInteger(value.unique_events, `${context} events`, 3, 100000),
      unique_sources: safeInteger(value.unique_sources, `${context} sources`, 1, 10000),
      counts: validateCounts(value.counts, `${context} counts`),
      sparkline: validateSparkline(value.sparkline, `${context} sparkline`),
    });
  }

  function validateRelatedTopic(value, context) {
    assertExactFields(value, [
      "id",
      "topic",
      "graph_node_id",
      "cooccurrence",
      "jaccard",
    ], context);
    const id = topicId(value.id, `${context} id`);
    if (value.graph_node_id !== id) fail(`${context} graph node`);
    return Object.freeze({
      id,
      topic: canonicalText(value.topic, `${context} topic`, 200),
      graph_node_id: id,
      cooccurrence: safeInteger(value.cooccurrence, `${context} cooccurrence`, 2, 100000),
      jaccard: finiteNumber(value.jaccard, `${context} jaccard`, 0, 1),
    });
  }

  function safeInternalUrl(value) {
    if (typeof value !== "string" || value.length > 2048 || /[\u0000-\u001f\u007f<>]/u.test(value)) return "#";
    try {
      const parsed = new URL(value, CANONICAL_ORIGIN);
      if (parsed.origin !== CANONICAL_ORIGIN || !["http:", "https:"].includes(parsed.protocol)) return "#";
      return `${parsed.pathname}${parsed.search}${parsed.hash}`;
    } catch (error) {
      return "#";
    }
  }

  function withBasePath(value, basePath = "/") {
    const path = safeInternalUrl(value);
    if (path === "#") return "#";
    const normalizedBase = typeof basePath === "string" && basePath.startsWith("/")
      ? `${basePath.replace(/\/+$/u, "")}/`
      : "/";
    if (normalizedBase === "/" || path.startsWith(normalizedBase)) return path;
    return `${normalizedBase.slice(0, -1)}${path}`;
  }

  function validateEvidence(value, context) {
    assertExactFields(value, ["id", "title", "summary", "source", "published_at", "internal_url"], context);
    const internalUrl = safeInternalUrl(value.internal_url);
    if (internalUrl === "#") fail(`${context} internal url`);
    return Object.freeze({
      id: canonicalText(value.id, `${context} id`, 200),
      title: canonicalText(value.title, `${context} title`, 300),
      summary: canonicalText(value.summary, `${context} summary`, 500, true),
      source: canonicalText(value.source, `${context} source`, 160),
      published_at: timestamp(value.published_at, `${context} published_at`),
      internal_url: internalUrl,
    });
  }

  function validateTopic(value, expectedId, index) {
    assertExactFields(value, [
      "schema_version",
      "id",
      "topic",
      "graph_node_id",
      "data_as_of",
      "description",
      "windows",
      "related_topics",
      "sources",
      "scenarios",
      "categories",
      "evidence",
    ], "topic");
    if (value.schema_version !== TOPIC_SCHEMA) fail("topic schema");
    const id = topicId(value.id, "topic id");
    if (id !== expectedId || value.graph_node_id !== id) fail("topic identity");
    const dataAsOf = timestamp(value.data_as_of, "topic data_as_of");
    if (index && dataAsOf !== index.data_as_of) fail("topic cutoff");
    assertExactFields(value.windows, WINDOWS, "topic windows");
    if (!Array.isArray(value.related_topics) || value.related_topics.length > 12) fail("related topics");
    if (!Array.isArray(value.evidence) || value.evidence.length > MAX_EVIDENCE) fail("topic evidence");
    const relatedTopics = value.related_topics.map((item, position) => (
      validateRelatedTopic(item, `related_topics[${position}]`)
    ));
    return Object.freeze({
      schema_version: TOPIC_SCHEMA,
      id,
      topic: canonicalText(value.topic, "topic label", 200),
      graph_node_id: id,
      data_as_of: dataAsOf,
      description: canonicalText(value.description, "topic description", 600, true),
      windows: Object.freeze(Object.fromEntries(
        WINDOWS.map((name) => [name, validateTopicWindow(value.windows[name], `topic ${name}`)]),
      )),
      related_topics: Object.freeze(relatedTopics),
      sources: validateFacetArray(value.sources, "topic sources"),
      scenarios: validateFacetArray(value.scenarios, "topic scenarios"),
      categories: validateFacetArray(value.categories, "topic categories"),
      evidence: Object.freeze(value.evidence.map((item, position) => (
        validateEvidence(item, `evidence[${position}]`)
      ))),
    });
  }

  function normalizeStateText(value, maximum = 100) {
    if (typeof value !== "string") return "";
    const normalized = value.normalize("NFKC").trim().replace(/\s+/gu, " ");
    if (!normalized || Array.from(normalized).length > maximum || /[\u0000-\u001f\u007f<>]/u.test(normalized)) {
      return "";
    }
    return normalized;
  }

  function parseState(search = "") {
    const params = new URLSearchParams(typeof search === "string" ? search : "");
    const windowName = params.get("window");
    const signal = params.get("signal");
    const view = params.get("view");
    const rawTopic = params.get("topic") || "";
    return {
      window: WINDOWS.includes(windowName) ? windowName : "30d",
      signal: SIGNALS.includes(signal) ? signal : "all",
      source: normalizeStateText(params.get("source") || "", 160),
      scenario: normalizeStateText(params.get("scenario") || "", 160),
      query: normalizeStateText(params.get("query") || "", 100),
      topic: TOPIC_ID.test(rawTopic) && rawTopic === rawTopic.trim() ? rawTopic : "",
      view: VIEWS.includes(view) ? view : "matrix",
    };
  }

  function serializeState(input) {
    const state = { ...parseState(""), ...input };
    const params = new URLSearchParams();
    params.set("window", WINDOWS.includes(state.window) ? state.window : "30d");
    if (SIGNALS.includes(state.signal) && state.signal !== "all") params.set("signal", state.signal);
    if (normalizeStateText(state.source, 160)) params.set("source", normalizeStateText(state.source, 160));
    if (normalizeStateText(state.scenario, 160)) params.set("scenario", normalizeStateText(state.scenario, 160));
    if (normalizeStateText(state.query, 100)) params.set("query", normalizeStateText(state.query, 100));
    if (TOPIC_ID.test(state.topic || "")) params.set("topic", state.topic);
    if (state.view === "list") params.set("view", "list");
    return `?${params.toString()}`;
  }

  function adaptStateForViewport(state, compact) {
    return compact ? { ...state, view: "list" } : { ...state };
  }

  function shouldRenderMatrix(view, compact) {
    return view === "matrix" && !compact;
  }

  function resolveWindowSignal(current, topicWindows, windowName) {
    if (current && typeof current === "object") return current;
    if (!WINDOWS.includes(windowName) || !topicWindows || typeof topicWindows !== "object") return null;
    const signal = topicWindows[windowName];
    return signal && typeof signal === "object" ? signal : null;
  }

  function freshnessStatus(dataAsOf, now = Date.now()) {
    const cutoff = Date.parse(dataAsOf);
    if (!Number.isFinite(cutoff) || !Number.isFinite(now)) {
      return Object.freeze({ key: "stale", label: "数据过期" });
    }
    const ageHours = Math.max(0, now - cutoff) / 3600000;
    if (ageHours <= 12) return Object.freeze({ key: "fresh", label: "静态快照" });
    if (ageHours <= 48) return Object.freeze({ key: "delayed", label: "数据延迟" });
    return Object.freeze({ key: "stale", label: "数据过期" });
  }

  function normalizeCompare(value) {
    return String(value || "").normalize("NFKC").trim().toLocaleLowerCase("zh-CN");
  }

  function filterTrends(trends, state = {}) {
    if (!Array.isArray(trends)) return [];
    const query = normalizeCompare(state.query);
    const source = normalizeCompare(state.source);
    const scenario = normalizeCompare(state.scenario);
    const signal = SIGNALS.includes(state.signal) ? state.signal : "all";
    return trends.filter((trend) => {
      if (!trend || typeof trend !== "object") return false;
      if (signal !== "all" && trend.state !== signal) return false;
      if (query && !normalizeCompare(trend.topic).includes(query)) return false;
      if (source && !(trend.sources || []).some((item) => normalizeCompare(item.name) === source)) return false;
      if (scenario && !(trend.scenarios || []).some((item) => normalizeCompare(item.name) === scenario)) return false;
      return true;
    });
  }

  function stableHash(value) {
    let hash = 2166136261;
    for (const character of String(value)) {
      hash ^= character.codePointAt(0);
      hash = Math.imul(hash, 16777619) >>> 0;
    }
    return hash;
  }

  function layoutMatrix(trends, width, height) {
    const safeWidth = Math.max(240, Number(width) || 0);
    const safeHeight = Math.max(220, Number(height) || 0);
    const left = 48;
    const right = safeWidth - 48;
    const top = 40;
    const bottom = safeHeight - 48;
    const maxEvents = Math.max(1, ...trends.map((item) => Number(item.counts?.current) || 0));
    const maxLog = Math.log1p(maxEvents);
    const maximumOffset = 28;
    const points = trends.map((item) => {
      const current = Number(item.counts?.current) || 0;
      const previous = Number(item.counts?.previous) || 0;
      const prePrevious = Number(item.counts?.pre_previous) || 0;
      const direction = (current - previous) / Math.max(current, previous, 1);
      const previousDirection = (previous - prePrevious) / Math.max(previous, prePrevious, 1);
      const normalizedX = Math.max(0, Math.min(1, 0.5 + (direction * 0.43)));
      const previousNormalizedX = Math.max(0, Math.min(1, 0.5 + (previousDirection * 0.43)));
      const normalizedY = maxLog === 0 ? 0 : Math.log1p(current) / maxLog;
      const previousNormalizedY = maxLog === 0 ? 0 : Math.log1p(previous) / maxLog;
      const sourceCount = Math.max(1, Number(item.unique_sources) || 1);
      const anchorX = left + ((right - left) * normalizedX);
      const anchorY = Math.max(top, Math.min(bottom, bottom - ((bottom - top) * normalizedY)));
      return {
        id: item.id,
        topic: item.topic,
        state: item.state,
        score: Number(item.score) || 0,
        x: anchorX,
        y: anchorY,
        anchorX,
        anchorY,
        baseX: anchorX,
        baseY: anchorY,
        previousX: left + ((right - left) * previousNormalizedX),
        previousY: bottom - ((bottom - top) * previousNormalizedY),
        radius: Math.max(8, Math.min(19, 7 + (Math.sqrt(sourceCount) * 3.7))),
      };
    });

    const clampOffset = (point) => {
      const offsetX = point.x - point.anchorX;
      const offsetY = point.y - point.anchorY;
      const distance = Math.hypot(offsetX, offsetY);
      if (distance <= maximumOffset) return;
      const scale = maximumOffset / distance;
      point.x = point.anchorX + (offsetX * scale);
      point.y = point.anchorY + (offsetY * scale);
    };

    for (let pass = 0; pass < 36; pass += 1) {
      for (let leftIndex = 0; leftIndex < points.length; leftIndex += 1) {
        for (let rightIndex = leftIndex + 1; rightIndex < points.length; rightIndex += 1) {
          const first = points[leftIndex];
          const second = points[rightIndex];
          let dx = second.x - first.x;
          let dy = second.y - first.y;
          let distance = Math.hypot(dx, dy);
          if (distance < 0.01) {
            const angle = ((stableHash(`${first.id}|${second.id}`) % 360) * Math.PI) / 180;
            dx = Math.cos(angle);
            dy = Math.sin(angle);
            distance = 1;
          }
          const minimum = first.radius + second.radius + 7;
          if (distance >= minimum) continue;
          const push = (minimum - distance) / 2;
          const unitX = dx / distance;
          const unitY = dy / distance;
          first.x = Math.max(left, Math.min(right, first.x - (unitX * push)));
          first.y = Math.max(top, Math.min(bottom, first.y - (unitY * push)));
          second.x = Math.max(left, Math.min(right, second.x + (unitX * push)));
          second.y = Math.max(top, Math.min(bottom, second.y + (unitY * push)));
          clampOffset(first);
          clampOffset(second);
        }
      }
    }
    return points.map((point) => Object.freeze({
      ...point,
      x: Math.round(point.x * 1000) / 1000,
      y: Math.round(point.y * 1000) / 1000,
      anchorX: Math.round(point.anchorX * 1000) / 1000,
      anchorY: Math.round(point.anchorY * 1000) / 1000,
      baseX: Math.round(point.baseX * 1000) / 1000,
      baseY: Math.round(point.baseY * 1000) / 1000,
      previousX: Math.round(point.previousX * 1000) / 1000,
      previousY: Math.round(point.previousY * 1000) / 1000,
      radius: Math.round(point.radius * 1000) / 1000,
    }));
  }

  function labeledPointIds(points, selectedId = "", hoveredId = "", limit = 8) {
    const ranked = [...(points || [])]
      .sort((left, right) => right.score - left.score || String(left.id).localeCompare(String(right.id)))
      .slice(0, Math.max(0, limit));
    const ids = new Set(ranked.map((point) => point.id));
    if (selectedId) ids.add(selectedId);
    if (hoveredId) ids.add(hoveredId);
    return ids;
  }

  function layoutPointLabels(points, selectedId = "", hoveredId = "", width = 900, height = 430, limit = 8) {
    const labels = labeledPointIds(points, selectedId, hoveredId, limit);
    const candidates = (points || [])
      .filter((point) => labels.has(point.id))
      .sort((left, right) => left.y - right.y || right.score - left.score || String(left.id).localeCompare(String(right.id)));
    const lanes = { left: [], right: [] };
    candidates.forEach((point, index) => {
      const side = index % 2 === 0 ? "right" : "left";
      lanes[side].push({ point, side });
    });
    const minimumY = 18;
    const maximumY = Math.max(minimumY, height - 18);
    const gap = 18;
    const result = [];
    for (const side of ["left", "right"]) {
      let nextY = minimumY;
      const lane = lanes[side].map(({ point }) => {
        const y = Math.max(nextY, Math.min(maximumY, point.y));
        nextY = y + gap;
        return {
          id: point.id,
          topic: point.topic,
          pointX: point.x,
          pointY: point.y,
          radius: point.radius,
          side,
          x: side === "right"
            ? (width < 680
              ? Math.min(width - 96, Math.max(width * 0.74, point.x + point.radius + 15))
              : Math.min(width - 8, point.x + point.radius + 15))
            : (width < 680
              ? Math.max(96, Math.min(width * 0.66, point.x - point.radius - 15))
              : Math.max(8, point.x - point.radius - 15)),
          y,
          align: side === "right" ? "left" : "right",
        };
      });
      const overflow = lane.length ? Math.max(0, lane[lane.length - 1].y - maximumY) : 0;
      lane.forEach((annotation) => {
        annotation.y = Math.max(minimumY, annotation.y - overflow);
        result.push(Object.freeze(annotation));
      });
    }
    return result.sort((left, right) => left.pointY - right.pointY || left.id.localeCompare(right.id));
  }

  function formatSourceName(value) {
    const name = String(value || "");
    return SOURCE_LABELS[name.toLocaleLowerCase("en-US")] || name;
  }

  function hitTestMatrix(points, x, y) {
    return [...(points || [])]
      .reverse()
      .find((point) => Math.hypot(point.x - x, point.y - y) <= point.radius + 5) || null;
  }

  function matrixColor(state) {
    if (state === "new") return { solid: "#f3a948", glow: "rgba(243,169,72,0.28)" };
    if (state === "steady") return { solid: "#7fb0c9", glow: "rgba(127,176,201,0.25)" };
    if (state === "cooling") return { solid: "#75818d", glow: "rgba(117,129,141,0.2)" };
    return { solid: "#4db6ac", glow: "rgba(77,182,172,0.28)" };
  }

  function drawMatrix(canvas, points, selectedId = "", hoveredId = "") {
    if (!canvas || typeof canvas.getContext !== "function") return;
    const width = Math.max(240, Math.round(canvas.clientWidth || canvas.width || 900));
    const height = Math.max(220, Math.round(canvas.clientHeight || canvas.height || 430));
    const ratio = Math.min(2, Math.max(1, Number(globalThis.devicePixelRatio) || 1));
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    const context = canvas.getContext("2d");
    if (!context) return;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    context.clearRect(0, 0, width, height);

    context.strokeStyle = "rgba(77,182,172,0.11)";
    context.lineWidth = 1;
    for (let step = 1; step < 5; step += 1) {
      const x = Math.round((width / 5) * step) + 0.5;
      const y = Math.round((height / 5) * step) + 0.5;
      context.beginPath();
      context.moveTo(x, 30);
      context.lineTo(x, height - 34);
      context.stroke();
      context.beginPath();
      context.moveTo(38, y);
      context.lineTo(width - 30, y);
      context.stroke();
    }
    context.strokeStyle = "rgba(77,182,172,0.26)";
    context.beginPath();
    context.moveTo(width / 2, 28);
    context.lineTo(width / 2, height - 34);
    context.stroke();

    for (const point of points) {
      const palette = matrixColor(point.state);
      const anchorX = Number.isFinite(point.anchorX) ? point.anchorX : point.x;
      const anchorY = Number.isFinite(point.anchorY) ? point.anchorY : point.y;
      context.strokeStyle = point.state === "cooling"
        ? "rgba(127,176,201,0.18)"
        : "rgba(77,182,172,0.18)";
      context.lineWidth = 1;
      context.setLineDash([3, 4]);
      context.beginPath();
      context.moveTo(point.previousX, point.previousY);
      context.lineTo(anchorX, anchorY);
      context.stroke();
      context.setLineDash([]);
      context.fillStyle = "rgba(209,213,219,0.32)";
      context.beginPath();
      context.arc(point.previousX, point.previousY, 2.2, 0, Math.PI * 2);
      context.fill();

      context.strokeStyle = "rgba(77,182,172,0.07)";
      context.beginPath();
      context.moveTo(anchorX, anchorY);
      context.lineTo(anchorX, height - 36);
      context.stroke();

      if (Math.hypot(point.x - anchorX, point.y - anchorY) > 1) {
        context.strokeStyle = "rgba(209,213,219,0.42)";
        context.setLineDash([2, 3]);
        context.beginPath();
        context.moveTo(anchorX, anchorY);
        context.lineTo(point.x, point.y);
        context.stroke();
        context.setLineDash([]);
        context.fillStyle = "rgba(209,213,219,0.72)";
        context.beginPath();
        context.arc(anchorX, anchorY, 2.4, 0, Math.PI * 2);
        context.fill();
      }

      context.fillStyle = palette.glow;
      context.beginPath();
      context.arc(point.x, point.y, point.radius + 9, 0, Math.PI * 2);
      context.fill();

      context.fillStyle = "rgba(6,10,20,0.94)";
      context.strokeStyle = palette.solid;
      context.lineWidth = point.id === selectedId ? 3 : 1.5;
      context.beginPath();
      context.arc(point.x, point.y, point.radius, 0, Math.PI * 2);
      context.fill();
      context.stroke();

      context.fillStyle = palette.solid;
      context.beginPath();
      context.arc(point.x, point.y, Math.max(3, point.radius * 0.24), 0, Math.PI * 2);
      context.fill();

      if (point.id === selectedId) {
        context.strokeStyle = "rgba(243,169,72,0.9)";
        context.lineWidth = 1.4;
        context.beginPath();
        context.arc(point.x, point.y, point.radius + 5, 0, Math.PI * 2);
        context.stroke();
        context.strokeStyle = "rgba(243,169,72,0.32)";
        context.beginPath();
        context.arc(point.x, point.y, point.radius + 10, 0, Math.PI * 2);
        context.stroke();
      }

      context.fillStyle = "rgba(77,182,172,0.72)";
      context.font = "11px ui-monospace, SFMono-Regular, Menlo, monospace";
      context.textAlign = "center";
      context.fillText(String(Math.round(point.score)), point.x, point.y + 3);
    }

    const annotations = layoutPointLabels(
      points,
      selectedId,
      hoveredId,
      width,
      height,
      height < 280 ? 4 : (width < 680 ? 6 : 8),
    );
    for (const annotation of annotations) {
      const label = Array.from(annotation.topic).slice(0, width < 680 ? 10 : 14).join("");
      context.font = "600 12px ui-monospace, SFMono-Regular, Menlo, monospace";
      context.textAlign = annotation.align;
      const textWidth = Math.ceil(context.measureText(label).width);
      const labelX = annotation.align === "left"
        ? Math.min(annotation.x, width - textWidth - 5)
        : Math.max(annotation.x, textWidth + 5);
      const lineStartX = annotation.side === "right"
        ? annotation.pointX + annotation.radius
        : annotation.pointX - annotation.radius;
      const lineEndX = annotation.side === "right" ? labelX - 5 : labelX + 5;
      context.strokeStyle = "rgba(77,182,172,0.34)";
      context.lineWidth = 1;
      context.beginPath();
      context.moveTo(lineStartX, annotation.pointY);
      context.lineTo(lineEndX, annotation.y);
      context.stroke();
      const backgroundX = annotation.align === "left"
        ? labelX - 3
        : labelX - textWidth - 3;
      context.fillStyle = "rgba(6,10,20,0.88)";
      context.fillRect(backgroundX, annotation.y - 12, textWidth + 6, 17);
      context.strokeStyle = "rgba(77,182,172,0.14)";
      context.strokeRect(backgroundX + 0.5, annotation.y - 11.5, textWidth + 5, 16);
      context.fillStyle = "rgba(209,213,219,0.94)";
      context.fillText(label, labelX, annotation.y);
    }
  }

  function drawSparkline(canvas, values, state) {
    if (!canvas || typeof canvas.getContext !== "function" || !Array.isArray(values)) return;
    const width = Math.max(220, Math.round(canvas.clientWidth || 280));
    const height = Math.max(68, Math.round(canvas.clientHeight || 74));
    const ratio = Math.min(2, Math.max(1, Number(globalThis.devicePixelRatio) || 1));
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    const context = canvas.getContext("2d");
    if (!context) return;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    context.clearRect(0, 0, width, height);
    context.strokeStyle = "rgba(77,182,172,0.12)";
    context.beginPath();
    context.moveTo(0, height - 12.5);
    context.lineTo(width, height - 12.5);
    context.stroke();
    const maximum = Math.max(1, ...values);
    const palette = matrixColor(state);
    context.strokeStyle = palette.solid;
    context.lineWidth = 2;
    context.beginPath();
    values.forEach((value, index) => {
      const x = 4 + ((width - 8) * (index / Math.max(1, values.length - 1)));
      const y = height - 13 - (((height - 24) * value) / maximum);
      if (index === 0) context.moveTo(x, y);
      else context.lineTo(x, y);
    });
    context.stroke();
    context.fillStyle = palette.solid;
    values.forEach((value, index) => {
      const x = 4 + ((width - 8) * (index / Math.max(1, values.length - 1)));
      const y = height - 13 - (((height - 24) * value) / maximum);
      context.beginPath();
      context.arc(x, y, 2.2, 0, Math.PI * 2);
      context.fill();
    });
  }

  function buildGraphUrl(id, basePath = "/") {
    if (typeof id !== "string" || !TOPIC_ID.test(id)) return "#";
    const normalizedBase = typeof basePath === "string" && basePath.startsWith("/")
      ? `${basePath.replace(/\/+$/u, "")}/`
      : "/";
    const path = `${normalizedBase === "//" ? "/" : normalizedBase}${GRAPH_ROUTE.slice(1)}`.replace(/\/+/gu, "/");
    const params = new URLSearchParams({ mode: "focus", node: id });
    return `${path}?${params.toString()}`;
  }

  function toggleWatchlistTopic(store, topic) {
    if (!store || typeof store.load !== "function" || typeof store.save !== "function") {
      throw new TypeError("watchlist store is required");
    }
    const normalized = normalizeStateText(topic, 200);
    if (!normalized) throw new TypeError("topic is required");
    const current = store.load();
    const match = normalizeCompare(normalized);
    const tags = current.rules.tags.filter((tag) => normalizeCompare(tag) !== match);
    const active = tags.length === current.rules.tags.length;
    if (active) tags.push(normalized);
    const saved = store.save({
      ...current,
      rules: { ...current.rules, tags },
    });
    return Object.freeze({ active, watchlist: saved });
  }

  function appendText(document, parent, tagName, className, value) {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    element.textContent = value === undefined || value === null ? "" : String(value);
    parent.append(element);
    return element;
  }

  function formatNumber(value) {
    return new Intl.NumberFormat("zh-CN").format(Number(value) || 0);
  }

  function formatTimestamp(value) {
    try {
      return new Intl.DateTimeFormat("zh-CN", {
        timeZone: "Asia/Shanghai",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      }).format(new Date(value));
    } catch (error) {
      return value;
    }
  }

  function formatDate(value) {
    try {
      return new Intl.DateTimeFormat("zh-CN", {
        timeZone: "Asia/Shanghai",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      }).format(new Date(value));
    } catch (error) {
      return value.slice(0, 10);
    }
  }

  function resolveAssetUrl(indexUrl, path, windowObject) {
    safeAssetPath(path);
    const base = new URL(indexUrl, windowObject.location.href);
    const resolved = new URL(path, base);
    if (resolved.origin !== base.origin || !resolved.pathname.startsWith(base.pathname.replace(/\/[^/]*$/u, "/"))) {
      fail("asset origin");
    }
    return resolved.href;
  }

  async function sha256Hex(bytes, windowObject) {
    if (!windowObject.crypto?.subtle) throw new TrendDataError("趋势数据完整性检查不可用。");
    const digest = await windowObject.crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  }

  async function fetchJson(url, options, windowObject) {
    const response = await windowObject.fetch(url, {
      signal: options.signal,
      cache: options.cache || "force-cache",
      credentials: "same-origin",
    });
    if (!response.ok) throw new TrendDataError(`趋势数据请求失败（${response.status}）。`);
    const declared = Number(response.headers.get("content-length"));
    if (Number.isFinite(declared) && declared > options.maximumBytes) {
      throw new TrendDataError("趋势数据超过安全体积限制。");
    }
    const bytes = await response.arrayBuffer();
    if (bytes.byteLength > options.maximumBytes) throw new TrendDataError("趋势数据超过安全体积限制。");
    if (options.expectedBytes && bytes.byteLength !== options.expectedBytes) {
      throw new TrendDataError("趋势数据体积校验失败。");
    }
    if (options.expectedSha256) {
      const actual = await sha256Hex(bytes, windowObject);
      if (actual !== options.expectedSha256) throw new TrendDataError("趋势数据摘要校验失败。");
    }
    let value;
    try {
      value = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
    } catch (error) {
      throw new TrendDataError("趋势数据格式无效。");
    }
    return value;
  }

  class LruCache {
    constructor(limit = 8) {
      this.limit = limit;
      this.values = new Map();
    }

    get(key) {
      if (!this.values.has(key)) return undefined;
      const value = this.values.get(key);
      this.values.delete(key);
      this.values.set(key, value);
      return value;
    }

    set(key, value) {
      if (this.values.has(key)) this.values.delete(key);
      this.values.set(key, value);
      while (this.values.size > this.limit) this.values.delete(this.values.keys().next().value);
    }
  }

  function initializeTrendsPage(document, windowObject = globalThis) {
    const root = document.getElementById("trend-workbench");
    if (!root || root.dataset.trendsReady === "true") return null;
    root.dataset.trendsReady = "true";
    const elements = {
      query: document.getElementById("trend-query"),
      filterToggle: document.getElementById("trend-mobile-filter-toggle"),
      filterBody: document.getElementById("trend-filter-body"),
      signal: document.getElementById("trend-signal"),
      source: document.getElementById("trend-source"),
      scenario: document.getElementById("trend-scenario"),
      clear: document.getElementById("trend-clear"),
      status: document.getElementById("trend-status"),
      dataState: document.getElementById("trend-data-state"),
      dataAsOf: document.getElementById("trend-data-as-of"),
      disclaimer: document.getElementById("trend-disclaimer"),
      statArticles: document.getElementById("trend-stat-articles"),
      statTopics: document.getElementById("trend-stat-topics"),
      statSources: document.getElementById("trend-stat-sources"),
      statWindow: document.getElementById("trend-stat-window"),
      resultCount: document.getElementById("trend-result-count"),
      sampleNotice: document.getElementById("trend-sample-notice"),
      matrixPanel: document.getElementById("trend-matrix-panel"),
      matrix: document.getElementById("trend-matrix"),
      list: document.getElementById("trend-list"),
      empty: document.getElementById("trend-empty"),
      detail: document.getElementById("trend-detail"),
    };
    if (Object.values(elements).some((element) => !element)) return null;

    const model = {
      index: null,
      windowData: null,
      state: adaptStateForViewport(
        parseState(windowObject.location.search),
        Boolean(windowObject.matchMedia?.("(max-width: 420px)").matches),
      ),
      points: [],
      windowController: null,
      topicController: null,
      windowSequence: 0,
      topicSequence: 0,
      topicCache: new LruCache(8),
      visibleEvidence: 8,
      hoveredId: "",
      returnTopicId: "",
      returnToStage: false,
      resizeObserver: null,
      watchlistStore: null,
    };
    const filterMedia = windowObject.matchMedia?.("(max-width: 760px)");

    try {
      if (windowObject.AIStackWatchlist && windowObject.localStorage) {
        model.watchlistStore = windowObject.AIStackWatchlist.createStore(windowObject.localStorage);
      }
    } catch (error) {
      model.watchlistStore = null;
    }

    function setStatus(message, error = false) {
      elements.status.textContent = message;
      elements.status.classList.toggle("is-error", error);
    }

    function setFilterPanel(expanded) {
      const isExpanded = Boolean(expanded);
      elements.filterBody.hidden = !isExpanded;
      elements.filterToggle.setAttribute("aria-expanded", String(isExpanded));
      elements.filterToggle.textContent = isExpanded ? "收起筛选" : "展开筛选";
    }

    function handleFilterViewportChange(event) {
      setFilterPanel(!event.matches);
    }

    setFilterPanel(!filterMedia?.matches);
    filterMedia?.addEventListener?.("change", handleFilterViewportChange);

    function updateHistory(push = false) {
      const url = `${windowObject.location.pathname}${serializeState(model.state)}`;
      if (push) windowObject.history.pushState({ trends: true }, "", url);
      else windowObject.history.replaceState({ trends: true }, "", url);
    }

    function setButtonStates() {
      root.dataset.view = model.state.view;
      document.querySelectorAll("[data-trend-window]").forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.trendWindow === model.state.window));
      });
      document.querySelectorAll("[data-trend-view]").forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.trendView === model.state.view));
      });
      elements.query.value = model.state.query;
      elements.signal.value = model.state.signal;
      elements.source.value = model.state.source;
      elements.scenario.value = model.state.scenario;
    }

    function appendOption(select, value, label) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      select.append(option);
    }

    function populateFacets() {
      const facets = model.windowData?.facets;
      if (!facets) return;
      const sourceValue = model.state.source;
      const scenarioValue = model.state.scenario;
      elements.source.replaceChildren();
      elements.scenario.replaceChildren();
      appendOption(elements.source, "", "全部来源");
      appendOption(elements.scenario, "", "全部场景");
      facets.sources.forEach((facet) => appendOption(
        elements.source,
        facet.name,
        `${formatSourceName(facet.name)} · ${formatNumber(facet.count)}`,
      ));
      facets.scenarios.forEach((facet) => appendOption(
        elements.scenario,
        facet.name,
        `${facet.name} · ${formatNumber(facet.count)}`,
      ));
      elements.source.value = [...elements.source.options].some((option) => option.value === sourceValue)
        ? sourceValue
        : "";
      elements.scenario.value = [...elements.scenario.options].some((option) => option.value === scenarioValue)
        ? scenarioValue
        : "";
      model.state.source = elements.source.value;
      model.state.scenario = elements.scenario.value;
    }

    function currentTrend(id = model.state.topic) {
      return model.windowData?.trends.find((item) => item.id === id) || null;
    }

    function renderList(trends) {
      elements.list.replaceChildren();
      trends.forEach((item) => {
        const rank = model.windowData.trends.findIndex((candidate) => candidate.id === item.id) + 1;
        const row = document.createElement("li");
        row.className = "trend-card";
        const button = document.createElement("button");
        button.type = "button";
        button.className = "trend-card__button";
        button.dataset.topicId = item.id;
        button.setAttribute("aria-pressed", String(model.state.topic === item.id));
        button.setAttribute("aria-label", `查看 ${item.topic} 趋势详情，得分 ${Math.round(item.score)}`);
        appendText(document, button, "span", "trend-card__rank", String(rank).padStart(2, "0"));
        const copy = document.createElement("span");
        copy.className = "trend-card__copy";
        appendText(document, copy, "strong", "trend-card__title", item.topic);
        appendText(
          document,
          copy,
          "small",
          "trend-card__meta",
          `${STATE_LABELS[item.state]} · ${formatNumber(item.unique_events)} 篇证据 · ${formatNumber(item.unique_sources)} 来源`,
        );
        button.append(copy);
        appendText(document, button, "span", "trend-card__score", Math.round(item.score));
        row.append(button);
        elements.list.append(row);
      });
    }

    function renderMatrix(trends) {
      const compact = Boolean(windowObject.matchMedia?.("(max-width: 420px)").matches);
      if (!trends.length || !shouldRenderMatrix(model.state.view, compact)) {
        model.points = [];
        return;
      }
      const rect = elements.matrix.getBoundingClientRect();
      model.points = layoutMatrix(trends, rect.width || 900, rect.height || 430);
      drawMatrix(elements.matrix, model.points, model.state.topic, model.hoveredId);
    }

    function renderResults() {
      if (!model.windowData) return;
      const trends = filterTrends(model.windowData.trends, model.state);
      elements.resultCount.textContent = `${formatNumber(trends.length)} 个主题`;
      elements.empty.hidden = trends.length !== 0;
      elements.matrixPanel.hidden = trends.length === 0;
      renderList(trends);
      renderMatrix(trends);
      elements.statTopics.textContent = formatNumber(model.index.stats.windows[model.state.window].trend_count);
      elements.statSources.textContent = formatNumber(model.index.stats.windows[model.state.window].source_count);
      elements.statWindow.textContent = WINDOW_LABELS[model.state.window];
      setButtonStates();
      setStatus(
        trends.length
          ? `已显示 ${trends.length} 个可解释趋势；选择主题可查看证据。`
          : "当前筛选没有趋势信号。",
      );
    }

    function renderDetailPlaceholder() {
      elements.detail.replaceChildren();
      const placeholder = document.createElement("div");
      placeholder.className = "trend-detail__placeholder";
      appendText(document, placeholder, "p", "trend-panel-index", "03 / EVIDENCE DRILLDOWN");
      const heading = appendText(document, placeholder, "h2", "", "主题详情");
      heading.id = "trend-detail-title";
      appendText(document, placeholder, "p", "", "选择趋势气泡或排名条目，查看评分依据、关联主题和证据文章。");
      appendText(document, placeholder, "small", "", "站内文章在当前标签页打开；使用浏览器返回可恢复当前趋势状态。");
      elements.detail.append(placeholder);
    }

    function appendMetricGrid(parent, signal) {
      const metrics = document.createElement("dl");
      metrics.className = "trend-metric-grid";
      [
        ["当前证据", formatNumber(signal.unique_events)],
        ["来源覆盖", formatNumber(signal.unique_sources)],
        ["上一周期", formatNumber(signal.counts.previous)],
        ["前两周期", formatNumber(signal.counts.pre_previous)],
      ].forEach(([label, value]) => {
        const cell = document.createElement("div");
        appendText(document, cell, "dt", "", label);
        appendText(document, cell, "dd", "", value);
        metrics.append(cell);
      });
      parent.append(metrics);
    }

    function appendComponents(parent, components) {
      if (!components) return;
      const section = document.createElement("section");
      section.className = "trend-detail-section";
      appendText(document, section, "h3", "", "为什么形成趋势");
      const list = document.createElement("ul");
      list.className = "trend-component-list";
      COMPONENTS.forEach((name) => {
        const row = document.createElement("li");
        row.className = "trend-component-row";
        appendText(document, row, "span", "", COMPONENT_LABELS[name]);
        const bar = document.createElement("span");
        bar.className = "trend-component-bar";
        const fill = document.createElement("span");
        fill.style.width = `${Math.round(components[name] * 100)}%`;
        bar.append(fill);
        row.append(bar);
        const output = document.createElement("output");
        output.textContent = `${Math.round(components[name] * 100)}%`;
        row.append(output);
        list.append(row);
      });
      section.append(list);
      parent.append(section);
    }

    function appendTagSection(parent, title, facets, className, labelFormatter = (value) => value) {
      if (!facets.length) return;
      const section = document.createElement("section");
      section.className = "trend-detail-section";
      appendText(document, section, "h3", "", title);
      const tags = document.createElement("div");
      tags.className = "trend-tag-list";
      facets.slice(0, 12).forEach((facet) => {
        appendText(document, tags, "span", className, `${labelFormatter(facet.name)} · ${facet.count}`);
      });
      section.append(tags);
      parent.append(section);
    }

    function appendRelatedTopics(parent, relatedTopics) {
      const available = relatedTopics.filter((item) => model.index.topics[item.id]);
      if (!available.length) return;
      const section = document.createElement("section");
      section.className = "trend-detail-section";
      appendText(document, section, "h3", "", `关联主题（${available.length}）`);
      const list = document.createElement("ul");
      list.className = "trend-related-list";
      available.forEach((item) => {
        const row = document.createElement("li");
        const button = document.createElement("button");
        button.type = "button";
        button.className = "trend-related-button";
        button.dataset.relatedTopicId = item.id;
        appendText(document, button, "span", "", item.topic);
        appendText(document, button, "small", "", `共现 ${item.cooccurrence} · J ${item.jaccard.toFixed(2)}`);
        row.append(button);
        list.append(row);
      });
      section.append(list);
      parent.append(section);
    }

    function appendEvidence(parent, evidence) {
      if (!evidence.length) return;
      const section = document.createElement("section");
      section.className = "trend-detail-section";
      appendText(document, section, "h3", "", `30 天证据文章（${evidence.length}）`);
      const list = document.createElement("ol");
      list.className = "trend-evidence-list";
      evidence.slice(0, model.visibleEvidence).forEach((item) => {
        const row = document.createElement("li");
        row.className = "trend-evidence-item";
        const link = document.createElement("a");
        link.className = "trend-evidence-link";
        link.href = withBasePath(item.internal_url, root.dataset.basePath || "/");
        link.dataset.articleId = item.id;
        appendText(document, link, "strong", "trend-evidence-title", item.title);
        if (item.summary) appendText(document, link, "p", "", item.summary);
        const meta = document.createElement("div");
        meta.className = "trend-evidence-meta";
        appendText(document, meta, "span", "", formatSourceName(item.source));
        const time = appendText(document, meta, "time", "", formatDate(item.published_at));
        time.dateTime = item.published_at;
        link.append(meta);
        row.append(link);
        list.append(row);
      });
      section.append(list);
      if (evidence.length > model.visibleEvidence) {
        const more = document.createElement("button");
        more.type = "button";
        more.className = "trend-button trend-button--quiet trend-load-more";
        more.dataset.loadMoreEvidence = "true";
        more.textContent = `继续查看 ${Math.min(8, evidence.length - model.visibleEvidence)} 篇`;
        section.append(more);
      }
      parent.append(section);
    }

    function isWatchlisted(topic) {
      if (!model.watchlistStore) return false;
      try {
        const match = normalizeCompare(topic);
        return model.watchlistStore.load().rules.tags.some((tag) => normalizeCompare(tag) === match);
      } catch (error) {
        return false;
      }
    }

    function renderDetail(topic) {
      elements.detail.replaceChildren();
      const trend = currentTrend(topic.id);
      const signal = resolveWindowSignal(trend, topic.windows, model.state.window);
      const heading = document.createElement("div");
      heading.className = "trend-detail__heading";
      const copy = document.createElement("div");
      appendText(document, copy, "p", "trend-panel-index", "03 / EVIDENCE DRILLDOWN");
      const title = appendText(document, copy, "h2", "", topic.topic);
      title.id = "trend-detail-title";
      title.tabIndex = -1;
      heading.append(copy);
      const close = document.createElement("button");
      close.type = "button";
      close.className = "trend-button trend-button--quiet";
      close.dataset.closeTrendDetail = "true";
      close.setAttribute("aria-label", "关闭主题详情");
      close.textContent = "关闭";
      heading.append(close);
      elements.detail.append(heading);

      if (!signal) {
        const notice = document.createElement("div");
        notice.className = "trend-window-empty";
        appendText(
          document,
          notice,
          "strong",
          "",
          `${WINDOW_LABELS[model.state.window]}窗口无有效信号`,
        );
        appendText(
          document,
          notice,
          "p",
          "",
          `该主题在当前${WINDOW_LABELS[model.state.window]}未达到趋势阈值；下方来源、场景、分类与证据为 30 天主题档案，不借用其他窗口评分。`,
        );
        elements.detail.append(notice);
      }

      if (signal) {
        const topline = document.createElement("div");
        topline.className = "trend-detail__topline";
        appendText(document, topline, "strong", "trend-detail__score", Math.round(signal.score));
        const chips = document.createElement("div");
        chips.className = "trend-detail__chips";
        appendText(document, chips, "span", "trend-signal-chip", STATE_LABELS[signal.state]);
        appendText(document, chips, "span", "trend-confidence-chip", CONFIDENCE_LABELS[signal.confidence]);
        topline.append(chips);
        elements.detail.append(topline);
      }

      if (topic.description) appendText(document, elements.detail, "p", "trend-detail__description", topic.description);

      const actions = document.createElement("div");
      actions.className = "trend-detail__actions";
      const graph = document.createElement("a");
      graph.className = "trend-link trend-link--graph";
      graph.href = buildGraphUrl(topic.graph_node_id, root.dataset.basePath || "/");
      graph.textContent = "进入知识图谱聚焦";
      actions.append(graph);
      if (model.watchlistStore) {
        const watchlist = document.createElement("button");
        watchlist.type = "button";
        watchlist.className = "trend-button";
        watchlist.dataset.watchlistTopic = topic.topic;
        const active = isWatchlisted(topic.topic);
        watchlist.setAttribute("aria-pressed", String(active));
        watchlist.textContent = active ? "已关注主题" : "关注此主题";
        actions.append(watchlist);
      }
      elements.detail.append(actions);

      if (signal) {
        appendMetricGrid(elements.detail, signal);
        const seriesSection = document.createElement("section");
        seriesSection.className = "trend-detail-section";
        appendText(document, seriesSection, "h3", "", `${WINDOW_LABELS[model.state.window]}证据走势`);
        const canvas = document.createElement("canvas");
        canvas.className = "trend-series";
        canvas.setAttribute("role", "img");
        canvas.setAttribute("aria-label", `${topic.topic} 最近 12 个采样区间的证据走势`);
        seriesSection.append(canvas);
        elements.detail.append(seriesSection);
        drawSparkline(canvas, signal.sparkline, signal.state);
      }

      appendComponents(elements.detail, trend?.components);
      appendTagSection(elements.detail, "30 天来源分布", topic.sources, "trend-source-tag", formatSourceName);
      appendTagSection(elements.detail, "30 天场景", topic.scenarios, "trend-category-tag");
      appendTagSection(elements.detail, "30 天内容分类", topic.categories, "trend-category-tag");
      appendRelatedTopics(elements.detail, topic.related_topics);
      appendEvidence(elements.detail, topic.evidence);
    }

    function showDetailLoading() {
      elements.detail.replaceChildren();
      const state = document.createElement("div");
      state.className = "trend-detail__placeholder";
      appendText(document, state, "p", "trend-panel-index", "03 / EVIDENCE DRILLDOWN");
      const title = appendText(document, state, "h2", "", "正在装载主题证据");
      title.id = "trend-detail-title";
      title.tabIndex = -1;
      appendText(document, state, "p", "", "仅请求当前主题的静态详情分片。其他主题保持未加载。 ");
      elements.detail.append(state);
    }

    async function loadTopic(id, options = {}) {
      if (!model.index || !TOPIC_ID.test(id) || !model.index.topics[id]) {
        model.state.topic = "";
        updateHistory(Boolean(options.push));
        renderResults();
        renderDetailPlaceholder();
        return;
      }
      if (TOPIC_ID.test(options.returnTopicId || "")) {
        model.returnTopicId = options.returnTopicId;
        model.returnToStage = false;
      } else if (options.returnToStage) {
        model.returnTopicId = "";
        model.returnToStage = true;
      }
      model.visibleEvidence = 8;
      model.state.topic = id;
      updateHistory(Boolean(options.push));
      renderResults();
      const cached = model.topicCache.get(id);
      if (cached) {
        renderDetail(cached);
        completeDetailTransition(options);
        return;
      }
      model.topicController?.abort();
      model.topicController = new AbortController();
      const sequence = ++model.topicSequence;
      showDetailLoading();
      try {
        const ref = model.index.topics[id];
        const url = resolveAssetUrl(root.dataset.indexUrl, ref.path, windowObject);
        const raw = await fetchJson(url, {
          signal: model.topicController.signal,
          maximumBytes: MAX_TOPIC_BYTES,
          expectedBytes: ref.bytes,
          expectedSha256: ref.sha256,
        }, windowObject);
        if (sequence !== model.topicSequence) return;
        const topic = validateTopic(raw, id, model.index);
        model.topicCache.set(id, topic);
        renderDetail(topic);
        completeDetailTransition(options);
      } catch (error) {
        if (error?.name === "AbortError") return;
        if (sequence !== model.topicSequence) return;
        elements.detail.replaceChildren();
        const state = document.createElement("div");
        state.className = "trend-detail__placeholder";
        const title = appendText(document, state, "h2", "", "主题详情暂不可用");
        title.id = "trend-detail-title";
        title.tabIndex = -1;
        appendText(document, state, "p", "", error?.message || "主题分片校验失败。");
        elements.detail.append(state);
        completeDetailTransition(options);
        setStatus("主题详情加载失败，趋势总览仍可使用。", true);
      }
    }

    function scrollDetailIntoView() {
      if (!windowObject.matchMedia?.("(max-width: 1020px)").matches) return;
      const reduced = windowObject.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
      elements.detail.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
    }

    function completeDetailTransition(options = {}) {
      if (options.scroll) scrollDetailIntoView();
      if (!options.focus) return;
      const title = document.getElementById("trend-detail-title");
      if (title && typeof title.focus === "function") title.focus({ preventScroll: true });
    }

    function restoreTrendOrigin(topicId, fallbackToStage = false) {
      const topicButton = Array.from(elements.list.querySelectorAll?.("[data-topic-id]") || [])
        .find((button) => button.dataset.topicId === topicId);
      if (topicButton && typeof topicButton.focus === "function") {
        topicButton.focus();
        return;
      }
      if (!fallbackToStage) return;
      const stageTitle = document.getElementById("trend-stage-title");
      if (stageTitle && typeof stageTitle.focus === "function") {
        stageTitle.tabIndex = -1;
        stageTitle.focus();
      }
    }

    function closeTopicDetail(restoreFocus = false) {
      const returnTopicId = model.returnTopicId;
      const returnToStage = model.returnToStage;
      model.topicController?.abort();
      model.state.topic = "";
      model.returnTopicId = "";
      model.returnToStage = false;
      updateHistory(true);
      renderResults();
      renderDetailPlaceholder();
      if (!restoreFocus) return;
      restoreTrendOrigin(returnTopicId, returnToStage);
    }

    async function loadWindow(windowName, options = {}) {
      if (!model.index || !WINDOWS.includes(windowName)) return;
      model.windowController?.abort();
      model.topicController?.abort();
      model.windowController = new AbortController();
      const sequence = ++model.windowSequence;
      model.state.window = windowName;
      if (options.push !== undefined) updateHistory(Boolean(options.push));
      setButtonStates();
      setStatus(`正在加载${WINDOW_LABELS[windowName]}趋势分片…`);
      try {
        const ref = model.index.windows[windowName];
        const url = resolveAssetUrl(root.dataset.indexUrl, ref.path, windowObject);
        const raw = await fetchJson(url, {
          signal: model.windowController.signal,
          maximumBytes: MAX_WINDOW_BYTES,
          expectedBytes: ref.bytes,
          expectedSha256: ref.sha256,
        }, windowObject);
        if (sequence !== model.windowSequence) return;
        model.windowData = validateWindow(raw, windowName, model.index);
        elements.sampleNotice.hidden = !model.windowData.sample_notice;
        elements.sampleNotice.textContent = model.windowData.sample_notice || "";
        populateFacets();
        renderResults();
        if (model.state.topic) await loadTopic(model.state.topic, { push: false });
        else renderDetailPlaceholder();
      } catch (error) {
        if (error?.name === "AbortError") return;
        if (sequence !== model.windowSequence) return;
        model.windowData = null;
        elements.list.replaceChildren();
        elements.matrixPanel.hidden = true;
        elements.empty.hidden = false;
        setStatus(error?.message || "趋势窗口加载失败。", true);
      }
    }

    async function initialise() {
      setButtonStates();
      try {
        const raw = await fetchJson(root.dataset.indexUrl, {
          maximumBytes: MAX_INDEX_BYTES,
          cache: "no-cache",
        }, windowObject);
        model.index = validateIndex(raw);
        const freshness = freshnessStatus(model.index.data_as_of, Date.now());
        elements.dataState.textContent = freshness.label;
        elements.dataState.dataset.freshness = freshness.key;
        elements.disclaimer.textContent = model.index.disclaimer;
        elements.dataAsOf.dateTime = model.index.data_as_of;
        elements.dataAsOf.textContent = `数据截止 ${formatTimestamp(model.index.data_as_of)}`;
        elements.statArticles.textContent = formatNumber(model.index.stats.eligible_articles);
        await loadWindow(model.state.window, { push: false });
      } catch (error) {
        elements.dataState.textContent = "数据异常";
        elements.dataState.dataset.freshness = "error";
        elements.matrixPanel.hidden = true;
        elements.empty.hidden = false;
        setStatus(error?.message || "趋势索引加载失败。", true);
      }
    }

    function changeFilters(push = false) {
      model.state = {
        ...model.state,
        query: normalizeStateText(elements.query.value, 100),
        signal: SIGNALS.includes(elements.signal.value) ? elements.signal.value : "all",
        source: normalizeStateText(elements.source.value, 160),
        scenario: normalizeStateText(elements.scenario.value, 160),
      };
      updateHistory(push);
      renderResults();
    }

    document.querySelectorAll("[data-trend-window]").forEach((button) => {
      button.addEventListener("click", () => {
        const windowName = button.dataset.trendWindow;
        if (windowName !== model.state.window) loadWindow(windowName, { push: true });
      });
    });
    document.querySelectorAll("[data-trend-view]").forEach((button) => {
      button.addEventListener("click", () => {
        const view = button.dataset.trendView;
        if (!VIEWS.includes(view) || view === model.state.view) return;
        model.state.view = view;
        updateHistory(true);
        renderResults();
      });
    });
    elements.query.addEventListener("input", () => changeFilters(false));
    elements.signal.addEventListener("change", () => changeFilters(true));
    elements.source.addEventListener("change", () => changeFilters(true));
    elements.scenario.addEventListener("change", () => changeFilters(true));
    elements.clear.addEventListener("click", () => {
      model.state = { ...model.state, signal: "all", source: "", scenario: "", query: "" };
      setButtonStates();
      updateHistory(true);
      renderResults();
      elements.query.focus();
    });
    elements.filterToggle.addEventListener("click", () => {
      setFilterPanel(elements.filterToggle.getAttribute("aria-expanded") !== "true");
    });

    elements.list.addEventListener("click", (event) => {
      const button = event.target.closest?.("[data-topic-id]");
      if (button) loadTopic(button.dataset.topicId, {
        push: true,
        scroll: true,
        focus: true,
        returnTopicId: button.dataset.topicId,
      });
    });
    elements.matrix.addEventListener("click", (event) => {
      const rect = elements.matrix.getBoundingClientRect();
      const point = hitTestMatrix(model.points, event.clientX - rect.left, event.clientY - rect.top);
      if (point) loadTopic(point.id, { push: true, scroll: true, focus: true, returnToStage: true });
    });
    elements.matrix.addEventListener("mousemove", (event) => {
      const rect = elements.matrix.getBoundingClientRect();
      const point = hitTestMatrix(model.points, event.clientX - rect.left, event.clientY - rect.top);
      const nextHoveredId = point?.id || "";
      if (nextHoveredId !== model.hoveredId) {
        model.hoveredId = nextHoveredId;
        drawMatrix(elements.matrix, model.points, model.state.topic, model.hoveredId);
      }
      elements.matrix.style.cursor = point ? "pointer" : "crosshair";
      elements.matrix.title = point ? `${point.topic} · 得分 ${Math.round(point.score)}` : "";
    });
    elements.matrix.addEventListener("mouseleave", () => {
      if (!model.hoveredId) return;
      model.hoveredId = "";
      drawMatrix(elements.matrix, model.points, model.state.topic, "");
      elements.matrix.title = "";
    });
    elements.detail.addEventListener("click", (event) => {
      const related = event.target.closest?.("[data-related-topic-id]");
      if (related) {
        loadTopic(related.dataset.relatedTopicId, { push: true, scroll: false, focus: true });
        return;
      }
      if (event.target.closest?.("[data-close-trend-detail]")) {
        closeTopicDetail(true);
        return;
      }
      const watchlist = event.target.closest?.("[data-watchlist-topic]");
      if (watchlist && model.watchlistStore) {
        try {
          const result = toggleWatchlistTopic(model.watchlistStore, watchlist.dataset.watchlistTopic);
          watchlist.setAttribute("aria-pressed", String(result.active));
          watchlist.textContent = result.active ? "已关注主题" : "关注此主题";
          setStatus(result.active ? "已加入当前浏览器的关注列表。" : "已从当前浏览器的关注列表移除。");
        } catch (error) {
          setStatus("当前浏览器无法更新关注列表。", true);
        }
        return;
      }
      if (event.target.closest?.("[data-load-more-evidence]")) {
        const topic = model.topicCache.get(model.state.topic);
        if (topic) {
          model.visibleEvidence = Math.min(topic.evidence.length, model.visibleEvidence + 8);
          renderDetail(topic);
        }
      }
    });

    windowObject.addEventListener("popstate", async () => {
      const previousTopic = model.state.topic;
      const next = adaptStateForViewport(
        parseState(windowObject.location.search),
        Boolean(windowObject.matchMedia?.("(max-width: 420px)").matches),
      );
      const changedWindow = next.window !== model.state.window;
      model.state = next;
      model.returnTopicId = next.topic || "";
      model.returnToStage = false;
      setButtonStates();
      if (changedWindow) {
        await loadWindow(next.window);
        if (next.topic) completeDetailTransition({ focus: true, scroll: true });
        else restoreTrendOrigin(previousTopic, Boolean(previousTopic));
      } else {
        renderResults();
        if (next.topic) await loadTopic(next.topic, { push: false, focus: true, scroll: true });
        else {
          renderDetailPlaceholder();
          restoreTrendOrigin(previousTopic, Boolean(previousTopic));
        }
      }
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && model.state.topic) {
        closeTopicDetail(true);
      }
    });
    windowObject.addEventListener("pagehide", () => {
      model.windowController?.abort();
      model.topicController?.abort();
      model.resizeObserver?.disconnect();
      filterMedia?.removeEventListener?.("change", handleFilterViewportChange);
    }, { once: true });

    if (typeof windowObject.ResizeObserver === "function") {
      model.resizeObserver = new windowObject.ResizeObserver(() => {
        if (model.windowData) renderMatrix(filterTrends(model.windowData.trends, model.state));
      });
      model.resizeObserver.observe(elements.matrix);
    } else {
      windowObject.addEventListener("resize", () => {
        if (model.windowData) renderMatrix(filterTrends(model.windowData.trends, model.state));
      });
    }

    initialise();
    return Object.freeze({ model, loadWindow, loadTopic, destroy() {
      model.windowController?.abort();
      model.topicController?.abort();
      model.resizeObserver?.disconnect();
      filterMedia?.removeEventListener?.("change", handleFilterViewportChange);
    } });
  }

  return {
    TrendDataError,
    adaptStateForViewport,
    buildGraphUrl,
    drawMatrix,
    drawSparkline,
    filterTrends,
    formatSourceName,
    freshnessStatus,
    hitTestMatrix,
    initializeTrendsPage,
    layoutMatrix,
    layoutPointLabels,
    labeledPointIds,
    parseState,
    resolveWindowSignal,
    safeAssetPath,
    safeInternalUrl,
    serializeState,
    shouldRenderMatrix,
    toggleWatchlistTopic,
    validateIndex,
    validateTopic,
    validateWindow,
    withBasePath,
  };
}));
