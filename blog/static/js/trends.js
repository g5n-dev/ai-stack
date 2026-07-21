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

  const INDEX_SCHEMA_V1 = "stack_trends_index_v1";
  const WINDOW_SCHEMA_V1 = "stack_trends_window_v1";
  const TOPIC_SCHEMA_V1 = "stack_trends_topic_v1";
  const INDEX_SCHEMA_V2 = "stack_trends_index_v2";
  const WINDOW_SCHEMA_V2 = "stack_trends_window_v2";
  const TOPIC_SCHEMA_V2 = "stack_trends_topic_v2";
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
  const COMPONENT_WEIGHTS = Object.freeze({
    quantity: 0.25,
    growth: 0.25,
    acceleration: 0.15,
    source_diversity: 0.15,
    novelty: 0.10,
    source_weight: 0.10,
  });
  const STATE_LABELS = Object.freeze({
    new: "新出现",
    rising: "上升",
    steady: "稳定",
    cooling: "降温",
  });
  const STATE_GLYPHS = Object.freeze({ new: "✦", rising: "↑", steady: "•", cooling: "↓" });
  const HEAT_VISUALS = Object.freeze([
    Object.freeze({ key: "cold", label: "低热", minimum: 0, color: "#75818d", rgb: "117,129,141", rings: 2, glow: 0.08 }),
    Object.freeze({ key: "watch", label: "观察", minimum: 50, color: "#7fb0c9", rgb: "127,176,201", rings: 3, glow: 0.14 }),
    Object.freeze({ key: "active", label: "活跃", minimum: 60, color: "#4db6ac", rgb: "77,182,172", rings: 4, glow: 0.2 }),
    Object.freeze({ key: "hot", label: "高热", minimum: 67, color: "#5adacf", rgb: "90,218,207", rings: 5, glow: 0.3 }),
    Object.freeze({ key: "signal", label: "强信号", minimum: 70, color: "#f3a948", rgb: "243,169,72", rings: 7, glow: 0.42 }),
  ]);
  const CONFIDENCE_LABELS = Object.freeze({ high: "高置信", medium: "中等置信" });
  const WINDOW_LABELS = Object.freeze({ "24h": "24 小时", "7d": "7 天", "30d": "30 天" });
  const WINDOW_BUCKETS = Object.freeze({
    "24h": Object.freeze({ span: 24, unit: "小时" }),
    "7d": Object.freeze({ span: 7, unit: "天" }),
    "30d": Object.freeze({ span: 30, unit: "天" }),
  });
  const SOURCE_LABELS = Object.freeze({
    blogs_podcasts: "博客与播客",
    hacker_news: "Hacker News",
    juejin: "掘金",
    arxiv: "arXiv",
    github_trending: "GitHub Trending",
  });
  const MAX_TOPOLOGY_CELLS = 11;
  const TOPOLOGY_SLOTS = Object.freeze([
    Object.freeze([0.2, 0.18]),
    Object.freeze([0.5, 0.15]),
    Object.freeze([0.8, 0.18]),
    Object.freeze([0.91, 0.39]),
    Object.freeze([0.88, 0.68]),
    Object.freeze([0.69, 0.85]),
    Object.freeze([0.46, 0.88]),
    Object.freeze([0.24, 0.84]),
    Object.freeze([0.09, 0.66]),
    Object.freeze([0.1, 0.38]),
  ]);
  const MAX_INDEX_BYTES = 64 * 1024;
  const MAX_WINDOW_BYTES = 128 * 1024;
  const MAX_TOPIC_BYTES = 96 * 1024;
  const MAX_MATRIX_PIXELS = 8 * 1024 * 1024;
  const MAX_TOPICS = 100;
  const MAX_TRENDS = 24;
  const MAX_EVIDENCE = 30;
  const MAX_FACETS = 100;
  const MAX_TEXT = 400;
  const SHA256 = /^[0-9a-f]{64}$/u;
  const ISO_TIMESTAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/u;
  const TOPIC_ID = /^tag:[^\u0000-\u001f\u007f<>]{1,200}$/u;
  const LINEAGE_ID = /^(?:obs|evt)_[0-9a-f]{64}$/u;
  const LINEAGE_RELATIONS = Object.freeze([
    "original", "exact_copy", "syndicated", "derivative", "same_event", "related_only",
  ]);
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

  function validateStatsWindow(value, context, v2 = false) {
    assertExactFields(value, v2
      ? ["trend_count", "evidence_articles", "unique_events", "redundant_observations", "source_count"]
      : ["trend_count", "evidence_articles", "source_count"], context);
    const result = {
      trend_count: safeInteger(value.trend_count, `${context} trend_count`, 0, MAX_TRENDS),
      evidence_articles: safeInteger(value.evidence_articles, `${context} evidence_articles`, 0, 100000),
      source_count: safeInteger(value.source_count, `${context} source_count`, 0, 10000),
    };
    if (v2) {
      result.unique_events = safeInteger(value.unique_events, `${context} unique_events`, 0, 100000);
      result.redundant_observations = safeInteger(
        value.redundant_observations,
        `${context} redundant_observations`,
        0,
        100000,
      );
      if (result.evidence_articles !== result.unique_events + result.redundant_observations) {
        fail(`${context} observation accounting`);
      }
    }
    return Object.freeze(result);
  }

  function validateStats(value, v2 = false) {
    assertExactFields(value, v2
      ? ["eligible_articles", "unique_events", "redundant_observations", "topic_count", "source_count", "windows"]
      : ["eligible_articles", "topic_count", "source_count", "windows"], "stats");
    assertExactFields(value.windows, WINDOWS, "stats windows");
    const result = {
      eligible_articles: safeInteger(value.eligible_articles, "stats eligible_articles", 0, 100000),
      topic_count: safeInteger(value.topic_count, "stats topic_count", 0, MAX_TOPICS),
      source_count: safeInteger(value.source_count, "stats source_count", 0, 10000),
      windows: Object.freeze(Object.fromEntries(
        WINDOWS.map((name) => [name, validateStatsWindow(value.windows[name], `stats ${name}`, v2)]),
      )),
    };
    if (v2) {
      result.unique_events = safeInteger(value.unique_events, "stats unique_events", 0, 100000);
      result.redundant_observations = safeInteger(
        value.redundant_observations,
        "stats redundant_observations",
        0,
        100000,
      );
      if (result.eligible_articles !== result.unique_events + result.redundant_observations) {
        fail("stats observation accounting");
      }
    }
    return Object.freeze(result);
  }

  function validateIndex(value) {
    const v2 = value?.schema_version === INDEX_SCHEMA_V2;
    if (!v2 && value?.schema_version !== INDEX_SCHEMA_V1) fail("index schema");
    const fields = [
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
    ];
    if (v2) fields.push("lineage_mode");
    assertExactFields(value, fields, "index");
    const generatedAt = timestamp(value.generated_at, "index generated_at");
    const dataAsOf = timestamp(value.data_as_of, "index data_as_of");
    if (generatedAt !== dataAsOf || value.realtime !== false) fail("index cutoff");
    if (value.timezone !== "Asia/Shanghai" || value.default_window !== "30d") fail("index defaults");
    const disclaimer = canonicalText(value.disclaimer, "index disclaimer", 240);
    const formula = canonicalText(value.formula, "index formula", 500);
    const normalization = validateNormalization(value.normalization);
    const stats = validateStats(value.stats, v2);
    const lineageMode = v2
      ? canonicalText(value.lineage_mode, "index lineage mode", 40)
      : "url_fallback";
    if (v2 && !["lineage_index_v1", "url_fallback"].includes(lineageMode)) fail("index lineage mode");
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
      schema_version: value.schema_version,
      generated_at: generatedAt,
      data_as_of: dataAsOf,
      realtime: false,
      lineage_mode: lineageMode,
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

  function validateTrend(value, context, v2 = false) {
    const fields = [
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
    ];
    if (v2) fields.push("redundant_observations", "source_diversity");
    assertExactFields(value, fields, context);
    const id = topicId(value.id, `${context} id`);
    if (value.graph_node_id !== id) fail(`${context} graph node`);
    const uniqueEvents = safeInteger(value.unique_events, `${context} unique_events`, 3, 100000);
    const observations = safeInteger(value.observations, `${context} observations`, 3, 1000000);
    const redundant = v2
      ? safeInteger(value.redundant_observations, `${context} redundant_observations`, 0, 1000000)
      : Math.max(0, observations - uniqueEvents);
    if (observations < uniqueEvents || redundant !== observations - uniqueEvents) {
      fail(`${context} observation accounting`);
    }
    return Object.freeze({
      id,
      topic: canonicalText(value.topic, `${context} topic`, 200),
      graph_node_id: id,
      score: finiteNumber(value.score, `${context} score`, 0, 100),
      state: validateSignal(value.state, `${context} state`),
      confidence: validateConfidence(value.confidence, `${context} confidence`),
      unique_events: uniqueEvents,
      observations,
      redundant_observations: redundant,
      source_diversity: v2
        ? safeInteger(value.source_diversity, `${context} source_diversity`, 1, 10000)
        : safeInteger(value.unique_sources, `${context} unique_sources`, 1, 10000),
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
    const v2 = value.schema_version === WINDOW_SCHEMA_V2;
    if (
      (!v2 && value.schema_version !== WINDOW_SCHEMA_V1)
      || value.window !== expectedWindow
      || !WINDOWS.includes(value.window)
      || (index && v2 !== (index.schema_version === INDEX_SCHEMA_V2))
    ) {
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
    const trends = value.trends.map((item, position) => validateTrend(item, `trend[${position}]`, v2));
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
      schema_version: value.schema_version,
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

  function validateTopicWindow(value, context, v2 = false) {
    if (value === null) return null;
    const fields = [
      "score",
      "state",
      "confidence",
      "unique_events",
      "unique_sources",
      "counts",
      "sparkline",
    ];
    if (v2) fields.push("observations", "redundant_observations", "source_diversity");
    assertExactFields(value, fields, context);
    const uniqueEvents = safeInteger(value.unique_events, `${context} events`, 3, 100000);
    const observations = v2
      ? safeInteger(value.observations, `${context} observations`, 3, 1000000)
      : uniqueEvents;
    const redundant = v2
      ? safeInteger(value.redundant_observations, `${context} redundant`, 0, 1000000)
      : 0;
    if (observations < uniqueEvents || redundant !== observations - uniqueEvents) {
      fail(`${context} observation accounting`);
    }
    return Object.freeze({
      score: finiteNumber(value.score, `${context} score`, 0, 100),
      state: validateSignal(value.state, `${context} state`),
      confidence: validateConfidence(value.confidence, `${context} confidence`),
      unique_events: uniqueEvents,
      observations,
      redundant_observations: redundant,
      unique_sources: safeInteger(value.unique_sources, `${context} sources`, 1, 10000),
      source_diversity: v2
        ? safeInteger(value.source_diversity, `${context} source diversity`, 1, 10000)
        : safeInteger(value.unique_sources, `${context} sources`, 1, 10000),
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

  function evidenceAssociationCopy(value, basePath = "/") {
    const associated = Number(value?.associated_observations);
    const count = Number.isSafeInteger(associated) ? associated - 1 : 0;
    if (count <= 0) return null;
    const target = withBasePath(value?.internal_url, basePath);
    if (target === "#") return null;
    const parsed = new URL(target, CANONICAL_ORIGIN);
    parsed.hash = "intelligence-lineage";
    return Object.freeze({
      count,
      label: `另有 ${count} 条关联报道`,
      href: `${parsed.pathname}${parsed.search}${parsed.hash}`,
    });
  }

  function validateEvidenceReport(value, context) {
    assertExactFields(value, [
      "observation_id", "title", "source", "published_at", "internal_url", "relation",
    ], context);
    if (!LINEAGE_ID.test(value.observation_id || "") || !LINEAGE_RELATIONS.includes(value.relation)) {
      fail(`${context} lineage identity`);
    }
    const internalUrl = safeInternalUrl(value.internal_url);
    if (internalUrl === "#") fail(`${context} internal url`);
    return Object.freeze({
      observation_id: value.observation_id,
      title: canonicalText(value.title, `${context} title`, 300),
      source: canonicalText(value.source, `${context} source`, 160),
      published_at: timestamp(value.published_at, `${context} published_at`),
      internal_url: internalUrl,
      relation: value.relation,
    });
  }

  function validateEvidence(value, context, v2 = false) {
    const fields = ["id", "title", "summary", "source", "published_at", "internal_url"];
    if (v2) fields.push(
      "observation_id", "relation", "associated_observations", "related_reports",
    );
    assertExactFields(value, fields, context);
    const internalUrl = safeInternalUrl(value.internal_url);
    if (internalUrl === "#") fail(`${context} internal url`);
    const relatedReports = v2
      ? (() => {
        if (!Array.isArray(value.related_reports) || value.related_reports.length > 5) {
          fail(`${context} related reports`);
        }
        return Object.freeze(value.related_reports.map((item, position) => (
          validateEvidenceReport(item, `${context} related_reports[${position}]`)
        )));
      })()
      : Object.freeze([]);
    const associated = v2
      ? safeInteger(value.associated_observations, `${context} associated observations`, 1, 100000)
      : 1;
    if (associated < relatedReports.length + 1) fail(`${context} associated observations`);
    if (v2 && (!LINEAGE_ID.test(value.observation_id || "") || !LINEAGE_RELATIONS.includes(value.relation))) {
      fail(`${context} lineage identity`);
    }
    return Object.freeze({
      id: canonicalText(value.id, `${context} id`, 200),
      observation_id: v2 ? value.observation_id : "",
      title: canonicalText(value.title, `${context} title`, 300),
      summary: canonicalText(value.summary, `${context} summary`, 500, true),
      source: canonicalText(value.source, `${context} source`, 160),
      published_at: timestamp(value.published_at, `${context} published_at`),
      internal_url: internalUrl,
      relation: v2 ? value.relation : "original",
      associated_observations: associated,
      related_reports: relatedReports,
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
    const v2 = value.schema_version === TOPIC_SCHEMA_V2;
    if (
      (!v2 && value.schema_version !== TOPIC_SCHEMA_V1)
      || (index && v2 !== (index.schema_version === INDEX_SCHEMA_V2))
    ) fail("topic schema");
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
      schema_version: value.schema_version,
      id,
      topic: canonicalText(value.topic, "topic label", 200),
      graph_node_id: id,
      data_as_of: dataAsOf,
      description: canonicalText(value.description, "topic description", 600, true),
      windows: Object.freeze(Object.fromEntries(
        WINDOWS.map((name) => [name, validateTopicWindow(value.windows[name], `topic ${name}`, v2)]),
      )),
      related_topics: Object.freeze(relatedTopics),
      sources: validateFacetArray(value.sources, "topic sources"),
      scenarios: validateFacetArray(value.scenarios, "topic scenarios"),
      categories: validateFacetArray(value.categories, "topic categories"),
      evidence: Object.freeze(value.evidence.map((item, position) => (
        validateEvidence(item, `evidence[${position}]`, v2)
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

  function buildTrendReturnUrl(pathname = "/trends/", state = {}) {
    const safePath = safeInternalUrl(pathname);
    if (safePath === "#") return "#";
    const parsed = new URL(safePath, CANONICAL_ORIGIN);
    return `${parsed.pathname}${serializeState(state)}`;
  }

  function appendReturnContext(value, returnTo = "") {
    const target = safeInternalUrl(value);
    if (target === "#") return "#";
    const safeReturn = safeInternalUrl(returnTo);
    if (safeReturn === "#" || !returnTo) return target;
    const parsed = new URL(target, CANONICAL_ORIGIN);
    parsed.searchParams.set("return_to", safeReturn);
    return `${parsed.pathname}${parsed.search}${parsed.hash}`;
  }

  function adaptStateForViewport(state, compact) {
    return compact ? { ...state, view: "list" } : { ...state };
  }

  function shouldRenderMatrix(view, compact) {
    return view === "matrix" && !compact;
  }

  function shouldDestroyOnPageHide(event) {
    return event?.persisted !== true;
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
    const filtered = trends.filter((trend) => {
      if (!trend || typeof trend !== "object") return false;
      if (signal !== "all" && trend.state !== signal) return false;
      if (query && !normalizeCompare(trend.topic).includes(query)) return false;
      if (source && !(trend.sources || []).some((item) => normalizeCompare(item.name) === source)) return false;
      if (scenario && !(trend.scenarios || []).some((item) => normalizeCompare(item.name) === scenario)) return false;
      return true;
    });
    if (!source && !scenario) return filtered;

    function facetCount(items, target) {
      if (!target) return 0;
      return (items || []).find((item) => normalizeCompare(item.name) === target)?.count || 0;
    }

    return filtered.sort((left, right) => {
      const scenarioDelta = facetCount(right.scenarios, scenario) - facetCount(left.scenarios, scenario);
      if (scenarioDelta) return scenarioDelta;
      const sourceDelta = facetCount(right.sources, source) - facetCount(left.sources, source);
      if (sourceDelta) return sourceDelta;
      return right.score - left.score || normalizeCompare(left.topic).localeCompare(normalizeCompare(right.topic));
    });
  }

  function countFacetTopics(trends, key, name) {
    if (!Array.isArray(trends) || !["sources", "scenarios"].includes(key)) return 0;
    const target = normalizeCompare(name);
    if (!target) return 0;
    return trends.reduce((total, trend) => (
      (trend?.[key] || []).some((facet) => normalizeCompare(facet.name) === target)
        ? total + 1
        : total
    ), 0);
  }

  function reconcileFacetState(state = {}, facets = {}) {
    function canonicalFacet(items, value) {
      const target = normalizeCompare(value);
      if (!target) return "";
      return (Array.isArray(items) ? items : [])
        .find((facet) => normalizeCompare(facet?.name) === target)?.name || "";
    }

    const source = canonicalFacet(facets.sources, state.source);
    const scenario = canonicalFacet(facets.scenarios, state.scenario);
    return Object.freeze({
      state: { ...state, source, scenario },
      changed: source !== (state.source || "") || scenario !== (state.scenario || ""),
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

  function resolveCanvasPixelRatio(width, height, requestedRatio = 1) {
    const safeWidth = Math.max(1, Number(width) || 1);
    const safeHeight = Math.max(1, Number(height) || 1);
    const requested = Math.min(2, Math.max(1, Number(requestedRatio) || 1));
    const budgetRatio = Math.sqrt(MAX_MATRIX_PIXELS / (safeWidth * safeHeight));
    return Math.max(0.25, Math.min(requested, budgetRatio));
  }

  function resizeCanvasBackingStore(canvas, context, width, height, requestedRatio = 1) {
    const pixelRatio = resolveCanvasPixelRatio(width, height, requestedRatio);
    const targetWidth = Math.max(1, Math.round(width * pixelRatio));
    const targetHeight = Math.max(1, Math.round(height * pixelRatio));
    let resized = false;
    if (canvas.width !== targetWidth) {
      canvas.width = targetWidth;
      resized = true;
    }
    if (canvas.height !== targetHeight) {
      canvas.height = targetHeight;
      resized = true;
    }
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    return Object.freeze({ pixelRatio, targetWidth, targetHeight, resized });
  }

  function invalidateTopicLoad(model) {
    model.topicController?.abort?.();
    model.topicController = null;
    model.topicSequence = (Number.isSafeInteger(model.topicSequence) ? model.topicSequence : 0) + 1;
    return model.topicSequence;
  }

  function heatVisual(score) {
    const value = Math.max(0, Math.min(100, Number(score) || 0));
    for (let index = HEAT_VISUALS.length - 1; index >= 0; index -= 1) {
      if (value >= HEAT_VISUALS[index].minimum) return HEAT_VISUALS[index];
    }
    return HEAT_VISUALS[0];
  }

  function heatTier(score) {
    return heatVisual(score).key;
  }

  function trendCardScoreCopy(value) {
    const state = STATE_LABELS[value?.state] || String(value?.state || "");
    const glyph = STATE_GLYPHS[value?.state] || "•";
    const visual = value?.heat || heatVisual(value?.score);
    const evidence = Number.isFinite(Number(value?.current))
      ? Number(value.current)
      : Number(value?.counts?.current ?? value?.unique_events);
    const sources = Number.isFinite(Number(value?.sourceCount))
      ? Number(value.sourceCount)
      : Number(value?.unique_sources);
    return Object.freeze({
      status: `${glyph} ${state}`.trim(),
      heat: visual.label,
      score: String(Math.round(Number(value?.score) || 0)),
      evidence: String(Math.max(0, evidence || 0)),
      sources: String(Math.max(0, sources || 0)),
    });
  }

  function scoreExplanation(signal, windowName = "30d", formula = "") {
    const resolvedWindow = WINDOWS.includes(windowName) ? windowName : "30d";
    const bucket = WINDOW_BUCKETS[resolvedWindow];
    const formatOffset = (multiple) => `${bucket.span * multiple} ${bucket.unit}`;
    const components = signal?.components || {};
    const weightedSubtotal = COMPONENTS.reduce((total, name) => (
      total + ((Number(components[name]) || 0) * COMPONENT_WEIGHTS[name])
    ), 0);
    const uniqueEvents = Math.max(0, Number(signal?.unique_events) || 0);
    const observations = Math.max(uniqueEvents, Number(signal?.observations) || uniqueEvents);
    const inferredRate = observations > 0 ? (observations - uniqueEvents) / observations : 0;
    const duplicateRate = Math.max(0, Math.min(
      1,
      Number.isFinite(Number(signal?.duplicate_rate)) ? Number(signal.duplicate_rate) : inferredRate,
    ));
    const duplicateMultiplier = 1 - (0.5 * duplicateRate);
    const round = (value) => Math.round(value * 1000000) / 1000000;
    return Object.freeze({
      formula: String(formula || ""),
      windowLabel: WINDOW_LABELS[resolvedWindow],
      ranges: Object.freeze([
        `当前：[截止−${formatOffset(1)}, 截止]`,
        `上一周期：[截止−${formatOffset(2)}, 截止−${formatOffset(1)})`,
        `前两周期：[截止−${formatOffset(3)}, 截止−${formatOffset(2)})`,
      ]),
      growthDefinition: "growth = clamp(0.5 + 0.5 × (current−previous) / max(current, previous, 1), 0, 1)",
      accelerationDefinition: "acceleration = clamp(0.5 + 0.5 × ((current−previous)−(previous−pre_previous)) / max(current, previous, pre_previous, 1), 0, 1)",
      uniqueEvents,
      observations,
      duplicateCount: Math.max(0, Math.round(observations - uniqueEvents)),
      duplicateRate: round(duplicateRate),
      duplicateMultiplier: round(duplicateMultiplier),
      weightedSubtotal: round(weightedSubtotal),
      recomputedScore: round(100 * weightedSubtotal * duplicateMultiplier),
    });
  }

  function topologyNodeVisual(point, active = false) {
    const visual = point?.heat || heatVisual(point?.score);
    return Object.freeze({
      ...visual,
      color: active ? "#f3a948" : "#5adacf",
      rgb: active ? "243,169,72" : "90,218,207",
    });
  }

  function matrixBadgeCopy(point, active = Boolean(point?.isCenter)) {
    const rank = String(Number(point?.rank) || 0).padStart(2, "0");
    const topic = truncateLabel(point?.topic, active ? 18 : 14);
    const state = STATE_LABELS[point?.state] || String(point?.state || "");
    const glyph = STATE_GLYPHS[point?.state] || "•";
    return Object.freeze({
      title: `${rank}  ${topic}`,
      status: `${glyph} ${state}`.trim(),
    });
  }

  function matrixTooltipCopy(point) {
    const badge = matrixBadgeCopy(point);
    const scoreCopy = trendCardScoreCopy(point);
    return Object.freeze({
      topic: String(point?.topic || ""),
      rank: String(Number(point?.rank) || 0).padStart(2, "0"),
      status: badge.status,
      heat: scoreCopy.heat,
      score: scoreCopy.score,
      evidence: scoreCopy.evidence,
      sources: scoreCopy.sources,
    });
  }

  function nodeGlowVisual(point, active = false, hovered = false) {
    const visual = point?.heat || heatVisual(point?.score);
    const activeBoost = active ? 8 : 0;
    const hoverBoost = hovered ? 6 : 0;
    return Object.freeze({
      blur: 16 + (visual.glow * 32) + activeBoost + hoverBoost,
      facetBlur: Math.min(18, 8 + (visual.glow * 16) + (hovered ? 4 : 0)),
      haloAlpha: Math.min(0.86, 0.26 + (visual.glow * 0.9) + (active ? 0.08 : 0) + (hovered ? 0.1 : 0)),
      haloRadius: 5 + (visual.glow * 8) + (active ? 2 : 0),
      haloWidth: 2.2 + (visual.glow * 2.8) + (active ? 0.8 : 0),
      auraAlpha: Math.min(0.38, 0.1 + (visual.glow * 0.42) + (active ? 0.04 : 0) + (hovered ? 0.04 : 0)),
      coreAlpha: Math.min(0.82, 0.34 + (visual.glow * 0.76) + (active ? 0.06 : 0)),
    });
  }

  function heatRgba(visual, alpha) {
    return `rgba(${visual.rgb},${Math.max(0, Math.min(1, alpha))})`;
  }

  function layoutMatrix(trends, width, height, selectedId = "", rankById = null) {
    const safeWidth = Math.max(240, Number(width) || 0);
    const safeHeight = Math.max(220, Number(height) || 0);
    const source = Array.isArray(trends) ? trends : [];
    const resolvedRanks = new Map(source.map((item, index) => {
      const supplied = Number(rankById?.get?.(item?.id));
      const embedded = Number(item?.rank);
      const rank = Number.isSafeInteger(supplied) && supplied > 0
        ? supplied
        : (Number.isSafeInteger(embedded) && embedded > 0 ? embedded : index + 1);
      return [item?.id, rank];
    }));
    const ranked = [...source]
      .sort((left, right) => (
        (resolvedRanks.get(left?.id) || Number.MAX_SAFE_INTEGER)
        - (resolvedRanks.get(right?.id) || Number.MAX_SAFE_INTEGER)
        || (Number(right?.score) || 0) - (Number(left?.score) || 0)
        || String(left?.id || "").localeCompare(String(right?.id || ""))
      ));
    if (!ranked.length) return [];

    const selected = ranked.find((item) => item.id === selectedId) || ranked[0];
    const visible = [selected, ...ranked.filter((item) => item.id !== selected.id)]
      .slice(0, MAX_TOPOLOGY_CELLS);
    const maxEvents = Math.max(1, ...visible.map((item) => Number(item.counts?.current) || 0));
    const maxLog = Math.log1p(maxEvents);
    const quantitativeLeft = 28;
    const quantitativeRight = safeWidth - 28;
    const quantitativeTop = 24;
    const quantitativeBottom = safeHeight - 24;
    const outerCount = Math.max(0, visible.length - 1);
    const slotFor = (index) => {
      if (outerCount >= 8) return TOPOLOGY_SLOTS[index] || TOPOLOGY_SLOTS[TOPOLOGY_SLOTS.length - 1];
      const angle = (-Math.PI / 2) + ((Math.PI * 2 * index) / Math.max(1, outerCount));
      return [0.5 + (Math.cos(angle) * 0.4), 0.5 + (Math.sin(angle) * 0.35)];
    };

    return visible.map((item, index) => {
      const current = Number(item.counts?.current) || 0;
      const previous = Number(item.counts?.previous) || 0;
      const prePrevious = Number(item.counts?.pre_previous) || 0;
      const direction = (current - previous) / Math.max(current, previous, 1);
      const previousDirection = (previous - prePrevious) / Math.max(previous, prePrevious, 1);
      const normalizedEvidence = maxLog === 0 ? 0 : Math.log1p(current) / maxLog;
      const previousEvidence = maxLog === 0 ? 0 : Math.log1p(previous) / maxLog;
      const sourceCount = Math.max(1, Number(item.unique_sources) || 1);
      const isCenter = index === 0;
      const slot = isCenter ? [0.5, 0.51] : slotFor(index - 1);
      const cellRadiusX = isCenter
        ? Math.max(78, Math.min(safeWidth * 0.19, safeHeight * 0.25))
        : Math.max(43, Math.min(
          safeWidth * (0.066 + (normalizedEvidence * 0.018)),
          safeHeight * 0.14,
        ));
      const cellRadiusY = isCenter
        ? Math.max(72, Math.min(safeHeight * 0.2, safeWidth * 0.18))
        : Math.max(39, Math.min(
          safeHeight * (0.062 + (normalizedEvidence * 0.016)),
          safeWidth * 0.105,
        ));
      const facets = [
        ...(Array.isArray(item.sources) ? item.sources : []).map((facet) => ({
          role: "source",
          name: String(facet.name || ""),
          count: Number(facet.count) || 0,
        })),
        ...(Array.isArray(item.scenarios) ? item.scenarios : []).map((facet) => ({
          role: "scenario",
          name: String(facet.name || ""),
          count: Number(facet.count) || 0,
        })),
      ]
        .filter((facet) => facet.name)
        .sort((left, right) => right.count - left.count || left.name.localeCompare(right.name))
        .slice(0, isCenter ? 10 : 7)
        .map((facet) => Object.freeze(facet));
      const normalizedX = Math.max(0, Math.min(1, 0.5 + (direction * 0.43)));
      const previousNormalizedX = Math.max(0, Math.min(1, 0.5 + (previousDirection * 0.43)));
      const rank = resolvedRanks.get(item.id) || (ranked.findIndex((candidate) => candidate.id === item.id) + 1);
      return Object.freeze({
        id: item.id,
        topic: item.topic,
        state: item.state,
        score: Number(item.score) || 0,
        heat: heatVisual(item.score),
        rank,
        x: Math.round(safeWidth * slot[0] * 1000) / 1000,
        y: Math.round(safeHeight * slot[1] * 1000) / 1000,
        radius: Math.round((isCenter ? 20 : 12 + (Math.sqrt(sourceCount) * 1.5)) * 1000) / 1000,
        cellRadiusX: Math.round(cellRadiusX * 1000) / 1000,
        cellRadiusY: Math.round(cellRadiusY * 1000) / 1000,
        anchorX: Math.round((quantitativeLeft + ((quantitativeRight - quantitativeLeft) * normalizedX)) * 1000) / 1000,
        anchorY: Math.round((quantitativeBottom - ((quantitativeBottom - quantitativeTop) * normalizedEvidence)) * 1000) / 1000,
        previousX: Math.round((quantitativeLeft + ((quantitativeRight - quantitativeLeft) * previousNormalizedX)) * 1000) / 1000,
        previousY: Math.round((quantitativeBottom - ((quantitativeBottom - quantitativeTop) * previousEvidence)) * 1000) / 1000,
        current,
        previous,
        prePrevious,
        growth: Math.round(direction * 1000000) / 1000000,
        sourceCount,
        isCenter,
        isSelected: item.id === selectedId,
        facets: Object.freeze(facets),
        visibleCount: visible.length,
        totalCount: ranked.length,
      });
    });
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
      .find((point) => {
        const radiusX = Math.max(point.radius + 5, Number(point.cellRadiusX) || 0);
        const radiusY = Math.max(point.radius + 5, Number(point.cellRadiusY) || 0);
        const normalizedX = (point.x - x) / radiusX;
        const normalizedY = (point.y - y) / radiusY;
        return ((normalizedX * normalizedX) + (normalizedY * normalizedY)) <= 1;
      }) || null;
  }

  function matrixColor(state) {
    if (state === "new") return { solid: "#f3a948", glow: "rgba(243,169,72,0.28)" };
    if (state === "steady") return { solid: "#7fb0c9", glow: "rgba(127,176,201,0.25)" };
    if (state === "cooling") return { solid: "#75818d", glow: "rgba(117,129,141,0.2)" };
    return { solid: "#4db6ac", glow: "rgba(77,182,172,0.28)" };
  }

  function hashUnit(seed, index) {
    return (stableHash(`${seed}:${index}`) % 10000) / 9999;
  }

  function traceOrganicContour(context, point, scale, seedOffset = 0) {
    const segments = 22;
    const coordinates = [];
    for (let index = 0; index < segments; index += 1) {
      const angle = (Math.PI * 2 * index) / segments;
      const perturbation = 0.94 + (hashUnit(point.id, (seedOffset * 31) + index) * 0.12);
      coordinates.push({
        x: point.x + (Math.cos(angle) * point.cellRadiusX * scale * perturbation),
        y: point.y + (Math.sin(angle) * point.cellRadiusY * scale * perturbation),
      });
    }
    const first = coordinates[0];
    const last = coordinates[coordinates.length - 1];
    context.beginPath();
    context.moveTo((last.x + first.x) / 2, (last.y + first.y) / 2);
    coordinates.forEach((current, index) => {
      const next = coordinates[(index + 1) % coordinates.length];
      context.quadraticCurveTo(current.x, current.y, (current.x + next.x) / 2, (current.y + next.y) / 2);
    });
    context.closePath();
  }

  function drawStarfield(context, width, height) {
    const count = Math.max(84, Math.min(190, Math.round((width * height) / 4200)));
    context.save();
    for (let index = 0; index < count; index += 1) {
      const x = hashUnit("trend-star-x", index) * width;
      const y = hashUnit("trend-star-y", index) * height;
      const bright = hashUnit("trend-star-a", index);
      const radius = 0.45 + (hashUnit("trend-star-r", index) * 1.15);
      context.fillStyle = bright > 0.9
        ? `rgba(127,176,201,${0.18 + (bright * 0.32)})`
        : `rgba(209,213,219,${0.055 + (bright * 0.13)})`;
      context.beginPath();
      context.arc(x, y, radius, 0, Math.PI * 2);
      context.fill();
    }
    context.restore();
  }

  function ellipseBoundary(point, towardX, towardY, padding = 0) {
    const dx = towardX - point.x;
    const dy = towardY - point.y;
    const denominator = Math.sqrt(
      ((dx * dx) / Math.max(1, point.cellRadiusX * point.cellRadiusX))
      + ((dy * dy) / Math.max(1, point.cellRadiusY * point.cellRadiusY)),
    ) || 1;
    const scale = Math.max(0, (1 / denominator) - (padding / Math.max(point.cellRadiusX, point.cellRadiusY)));
    return { x: point.x + (dx * scale), y: point.y + (dy * scale) };
  }

  function drawTopologyRoute(context, center, point, index) {
    const visual = topologyNodeVisual(point, false);
    const start = ellipseBoundary(center, point.x, point.y, 7);
    const end = ellipseBoundary(point, center.x, center.y, -5);
    const dx = end.x - start.x;
    const dy = end.y - start.y;
    const bend = ((index % 2 === 0 ? 1 : -1) * Math.min(42, Math.hypot(dx, dy) * 0.12));
    const length = Math.hypot(dx, dy) || 1;
    const normalX = -dy / length;
    const normalY = dx / length;
    const firstControl = {
      x: start.x + (dx * 0.34) + (normalX * bend),
      y: start.y + (dy * 0.34) + (normalY * bend),
    };
    const secondControl = {
      x: start.x + (dx * 0.7) + (normalX * bend * 0.55),
      y: start.y + (dy * 0.7) + (normalY * bend * 0.55),
    };
    context.save();
    context.strokeStyle = heatRgba(visual, 0.2 + (visual.glow * 0.55));
    context.lineWidth = 1 + (visual.glow * 0.55);
    context.setLineDash([8, 9]);
    context.beginPath();
    context.moveTo(start.x, start.y);
    context.bezierCurveTo(
      firstControl.x,
      firstControl.y,
      secondControl.x,
      secondControl.y,
      end.x,
      end.y,
    );
    context.stroke();
    context.setLineDash([]);
    const angle = Math.atan2(end.y - secondControl.y, end.x - secondControl.x);
    const arrow = 7;
    context.fillStyle = heatRgba(visual, 0.58 + (visual.glow * 0.48));
    context.beginPath();
    context.moveTo(end.x, end.y);
    context.lineTo(
      end.x - (Math.cos(angle - 0.52) * arrow),
      end.y - (Math.sin(angle - 0.52) * arrow),
    );
    context.lineTo(
      end.x - (Math.cos(angle + 0.52) * arrow),
      end.y - (Math.sin(angle + 0.52) * arrow),
    );
    context.closePath();
    context.fill();
    context.restore();
  }

  function drawCellContours(context, point, active = false, hovered = false) {
    const visual = topologyNodeVisual(point, active);
    context.save();
    context.fillStyle = heatRgba(visual, 0.018 + (visual.glow * (active ? 0.13 : 0.08)));
    context.beginPath();
    context.ellipse(point.x, point.y, point.cellRadiusX * 0.82, point.cellRadiusY * 0.8, 0, 0, Math.PI * 2);
    context.fill();
    const rings = visual.rings;
    for (let ring = 0; ring < rings; ring += 1) {
      const scale = 0.7 + (ring * (rings > 5 ? 0.065 : 0.078));
      traceOrganicContour(context, point, scale, ring);
      const alpha = Math.max(0.055, 0.12 + visual.glow + (hovered ? 0.09 : 0) - (ring * 0.026));
      context.strokeStyle = heatRgba(visual, alpha);
      context.lineWidth = ring === 0 ? 1.2 + (visual.glow * 0.8) : 1;
      context.stroke();
    }
    context.restore();
  }

  function drawHub(context, point, active = false, hovered = false) {
    const visual = topologyNodeVisual(point, active);
    const glow = nodeGlowVisual(point, active, hovered);
    const radius = point.radius + (hovered ? 2 : 0);
    context.save();
    const auraRadius = Math.min(55, radius + glow.haloRadius + (glow.blur * 0.56));
    const aura = context.createRadialGradient(
      point.x,
      point.y,
      Math.max(1, radius * 0.38),
      point.x,
      point.y,
      auraRadius,
    );
    aura.addColorStop(0, heatRgba(visual, glow.auraAlpha));
    aura.addColorStop(0.38, heatRgba(visual, glow.auraAlpha * 0.68));
    aura.addColorStop(0.72, heatRgba(visual, glow.auraAlpha * 0.18));
    aura.addColorStop(1, heatRgba(visual, 0));
    context.fillStyle = aura;
    context.beginPath();
    context.arc(point.x, point.y, auraRadius, 0, Math.PI * 2);
    context.fill();
    context.shadowColor = heatRgba(visual, 0.56 + (visual.glow * 0.72));
    context.shadowBlur = glow.blur;
    context.fillStyle = "rgba(6,15,24,0.96)";
    context.strokeStyle = visual.color;
    context.lineWidth = 1.8 + (visual.glow * 1.8) + (active ? 0.8 : 0);
    context.beginPath();
    context.arc(point.x, point.y, radius, 0, Math.PI * 2);
    context.fill();
    context.stroke();
    context.strokeStyle = heatRgba(visual, glow.haloAlpha);
    context.lineWidth = glow.haloWidth;
    context.beginPath();
    context.arc(point.x, point.y, radius + glow.haloRadius, 0, Math.PI * 2);
    context.stroke();
    context.shadowBlur = 0;
    context.strokeStyle = heatRgba(visual, 0.3 + (visual.glow * 0.36));
    context.lineWidth = 1;
    context.beginPath();
    context.arc(point.x, point.y, Math.max(5, radius * 0.56), 0, Math.PI * 2);
    context.stroke();
    context.beginPath();
    context.moveTo(point.x - radius + 3, point.y);
    context.lineTo(point.x + radius - 3, point.y);
    context.moveTo(point.x, point.y - radius + 3);
    context.lineTo(point.x, point.y + radius - 3);
    context.stroke();
    if (active) {
      context.strokeStyle = heatRgba(visual, 0.42 + (visual.glow * 0.55));
      context.lineWidth = 1;
      context.beginPath();
      context.arc(point.x, point.y, radius + 6, 0, Math.PI * 2);
      context.stroke();
    }
    context.restore();
  }

  function facetLabel(facet) {
    return facet.role === "source" ? formatSourceName(facet.name) : facet.name;
  }

  function truncateLabel(value, maximum) {
    const characters = Array.from(String(value || ""));
    return characters.length <= maximum ? characters.join("") : `${characters.slice(0, maximum).join("")}…`;
  }

  function drawOuterNetwork(context, point, hovered = false) {
    const visual = topologyNodeVisual(point, false);
    drawCellContours(context, point, false, hovered);
    const facets = point.facets || [];
    facets.forEach((facet, index) => {
      const angle = ((Math.PI * 2 * index) / Math.max(1, facets.length))
        + ((stableHash(point.id) % 31) / 90);
      const radial = 0.48 + (hashUnit(point.id, index + 70) * 0.18);
      const nodeX = point.x + (Math.cos(angle) * point.cellRadiusX * radial);
      const nodeY = point.y + (Math.sin(angle) * point.cellRadiusY * radial);
      context.strokeStyle = heatRgba(visual, 0.2 + (visual.glow * 0.45));
      context.lineWidth = 1;
      context.beginPath();
      context.moveTo(point.x, point.y);
      context.lineTo(nodeX, nodeY);
      context.stroke();
      context.fillStyle = "rgba(6,15,24,0.96)";
      context.strokeStyle = heatRgba(visual, hovered ? 0.96 : 0.72 + (visual.glow * 0.4));
      context.lineWidth = 1.2;
      const glow = nodeGlowVisual(point, false, hovered);
      context.save();
      context.fillStyle = heatRgba(visual, 0.12 + (visual.glow * 0.34));
      context.strokeStyle = heatRgba(visual, Math.min(0.98, 0.78 + (visual.glow * 0.42)));
      context.shadowColor = heatRgba(visual, 0.9);
      context.shadowBlur = glow.facetBlur;
      context.beginPath();
      const nodeRadius = 3 + Math.min(2.2, Math.sqrt(Math.max(0, facet.count)) * 0.62);
      context.arc(nodeX, nodeY, nodeRadius, 0, Math.PI * 2);
      context.fill();
      context.stroke();
      context.shadowBlur = 0;
      context.fillStyle = heatRgba(visual, glow.coreAlpha);
      context.beginPath();
      context.arc(nodeX, nodeY, Math.max(1.1, nodeRadius * 0.28), 0, Math.PI * 2);
      context.fill();
      context.restore();
    });
    drawHub(context, point, false, hovered);
  }

  function drawCentralNetwork(context, point, hovered = false) {
    const visual = topologyNodeVisual(point, true);
    drawCellContours(context, point, true, hovered);
    const slots = [
      [0, -0.59], [0.36, -0.48], [0.61, -0.24], [0.65, 0.1], [0.47, 0.41],
      [0.13, 0.58], [-0.27, 0.54], [-0.54, 0.33], [-0.64, -0.03], [-0.43, -0.4],
    ];
    const nodes = (point.facets || []).map((facet, index) => ({
      facet,
      x: point.x + (slots[index][0] * point.cellRadiusX),
      y: point.y + (slots[index][1] * point.cellRadiusY),
    }));
    nodes.forEach((node, index) => {
      context.strokeStyle = heatRgba(visual, 0.3 + (visual.glow * 0.42));
      context.lineWidth = 1;
      context.beginPath();
      context.moveTo(point.x, point.y);
      context.lineTo(node.x, node.y);
      context.stroke();
      const next = nodes[index + 1];
      if (next && stableHash(`${point.id}:${index}`) % 3 !== 0) {
        context.strokeStyle = heatRgba(visual, 0.15 + (visual.glow * 0.28));
        context.beginPath();
        context.moveTo(node.x, node.y);
        context.lineTo(next.x, next.y);
        context.stroke();
      }
    });
    nodes.forEach((node) => {
      const radius = 4 + Math.min(3, Math.sqrt(Math.max(0, node.facet.count)) * 0.7);
      const glow = nodeGlowVisual(point, true, hovered);
      context.fillStyle = heatRgba(visual, glow.coreAlpha * 0.74);
      context.strokeStyle = heatRgba(visual, 0.9);
      context.lineWidth = 1.1;
      context.save();
      context.shadowColor = heatRgba(visual, 0.94);
      context.shadowBlur = glow.facetBlur;
      context.beginPath();
      context.arc(node.x, node.y, radius, 0, Math.PI * 2);
      context.fill();
      context.stroke();
      context.shadowBlur = 0;
      context.fillStyle = heatRgba(visual, glow.coreAlpha);
      context.beginPath();
      context.arc(node.x, node.y, Math.max(1.2, radius * 0.26), 0, Math.PI * 2);
      context.fill();
      context.restore();
      const label = truncateLabel(facetLabel(node.facet), 10);
      const deltaX = node.x - point.x;
      const centered = Math.abs(deltaX) < point.cellRadiusX * 0.14;
      const alignRight = deltaX < 0;
      context.font = "600 12px ui-monospace, SFMono-Regular, Menlo, monospace";
      context.textAlign = centered ? "center" : (alignRight ? "right" : "left");
      context.textBaseline = "middle";
      context.fillStyle = "rgba(222,237,238,0.92)";
      context.fillText(
        label,
        centered ? node.x : node.x + (alignRight ? -9 : 9),
        centered ? node.y + (node.y < point.y ? -13 : 13) : node.y,
      );
    });
    drawHub(context, point, true, hovered);
  }

  function drawTerminalBadge(context, point, width, height, active = false, hovered = false) {
    const visual = topologyNodeVisual(point, active);
    const copy = matrixBadgeCopy(point, active);
    const title = copy.title;
    const detail = copy.status;
    const titleSize = width >= 900 ? 13 : 12;
    const detailSize = width >= 900 ? 12 : 11;
    context.save();
    context.font = `700 ${titleSize}px ui-monospace, SFMono-Regular, Menlo, monospace`;
    const titleWidth = context.measureText(title).width;
    context.font = `${detailSize}px ui-monospace, SFMono-Regular, Menlo, monospace`;
    const detailWidth = context.measureText(detail).width;
    const badgeWidth = Math.min(width - 16, Math.ceil(Math.max(titleWidth, detailWidth)) + 18);
    const badgeHeight = width >= 900 ? 42 : 38;
    const rawTop = point.y - point.cellRadiusY - badgeHeight - 4;
    const left = Math.max(8, Math.min(width - badgeWidth - 8, point.x - (badgeWidth / 2)));
    const top = Math.max(8, Math.min(height - badgeHeight - 8, rawTop));
    context.fillStyle = "rgba(3,9,18,0.94)";
    context.strokeStyle = heatRgba(visual, active || hovered ? 0.78 : 0.28 + (visual.glow * 0.72));
    context.lineWidth = hovered || active ? 1.35 : 1;
    context.fillRect(left, top, badgeWidth, badgeHeight);
    context.strokeRect(left + 0.5, top + 0.5, badgeWidth - 1, badgeHeight - 1);
    context.textAlign = "left";
    context.textBaseline = "alphabetic";
    context.font = `700 ${titleSize}px ui-monospace, SFMono-Regular, Menlo, monospace`;
    context.fillStyle = active ? visual.color : "rgba(222,237,238,0.96)";
    context.fillText(title, left + 9, top + (width >= 900 ? 17 : 15));
    context.font = `${detailSize}px ui-monospace, SFMono-Regular, Menlo, monospace`;
    context.fillStyle = heatRgba(visual, 0.88 + (visual.glow * 0.25));
    context.fillText(detail, left + 9, top + (width >= 900 ? 34 : 30));
    context.restore();
  }

  function renderMatrixTooltip(document, tooltip, point) {
    if (!tooltip) return;
    tooltip.replaceChildren();
    if (!point) {
      tooltip.hidden = true;
      tooltip.setAttribute("aria-hidden", "true");
      delete tooltip.dataset.heat;
      return;
    }
    const copy = matrixTooltipCopy(point);
    tooltip.dataset.heat = point.heat?.key || heatTier(point.score);
    const header = document.createElement("div");
    header.className = "trend-matrix-tooltip__header";
    appendText(document, header, "span", "trend-matrix-tooltip__rank", copy.rank);
    appendText(document, header, "strong", "trend-matrix-tooltip__topic", copy.topic);
    appendText(document, header, "span", "trend-matrix-tooltip__state", copy.status);
    const metrics = document.createElement("dl");
    metrics.className = "trend-matrix-tooltip__metrics";
    [
      ["综合得分", copy.score],
      ["证据", copy.evidence],
      ["来源", copy.sources],
    ].forEach(([label, value]) => {
      const cell = document.createElement("div");
      appendText(document, cell, "dt", "", label);
      appendText(document, cell, "dd", "", value);
      metrics.append(cell);
    });
    tooltip.append(header);
    appendText(document, tooltip, "small", "trend-matrix-tooltip__heat", copy.heat);
    tooltip.append(metrics);
    tooltip.hidden = false;
    tooltip.setAttribute("aria-hidden", "false");
  }

  function positionMatrixTooltip(tooltip, panel, clientX, clientY) {
    if (!tooltip || tooltip.hidden || !panel) return;
    const rect = panel.getBoundingClientRect();
    const gap = 14;
    const inset = 8;
    const tooltipWidth = tooltip.offsetWidth || 216;
    const tooltipHeight = tooltip.offsetHeight || 98;
    const pointerX = clientX - rect.left;
    const pointerY = clientY - rect.top;
    let left = pointerX + gap;
    let top = pointerY + gap;
    if (left + tooltipWidth > rect.width - inset) left = pointerX - tooltipWidth - gap;
    if (top + tooltipHeight > rect.height - inset) top = pointerY - tooltipHeight - gap;
    tooltip.style.left = `${Math.max(inset, Math.min(rect.width - tooltipWidth - inset, left))}px`;
    tooltip.style.top = `${Math.max(inset, Math.min(rect.height - tooltipHeight - inset, top))}px`;
  }

  function drawMatrix(canvas, points, selectedId = "", hoveredId = "") {
    if (!canvas || typeof canvas.getContext !== "function") return;
    const width = Math.max(240, Math.round(canvas.clientWidth || canvas.width || 900));
    const height = Math.max(220, Math.round(canvas.clientHeight || canvas.height || 430));
    const context = canvas.getContext("2d");
    if (!context) return;
    resizeCanvasBackingStore(
      canvas,
      context,
      width,
      height,
      Number(globalThis.devicePixelRatio) || 1,
    );
    context.clearRect(0, 0, width, height);
    context.fillStyle = "rgb(3,9,18)";
    context.fillRect(0, 0, width, height);
    drawStarfield(context, width, height);

    const center = (points || []).find((point) => point.isCenter) || points?.[0];
    if (!center) return;
    const outer = points.filter((point) => point !== center);
    outer.forEach((point, index) => drawTopologyRoute(context, center, point, index));
    outer.forEach((point) => drawOuterNetwork(context, point, point.id === hoveredId));
    drawCentralNetwork(context, center, center.id === hoveredId);
    outer.forEach((point) => drawTerminalBadge(
      context,
      point,
      width,
      height,
      false,
      point.id === hoveredId,
    ));
    drawTerminalBadge(context, center, width, height, true, center.id === hoveredId);

    context.save();
    context.fillStyle = "rgba(209,213,219,0.74)";
    context.strokeStyle = "rgba(77,182,172,0.34)";
    context.lineWidth = 1;
    context.fillRect(14, 14, 94, 32);
    context.fillStyle = "rgba(3,9,18,0.96)";
    context.fillRect(15, 15, 92, 30);
    context.strokeRect(14.5, 14.5, 93, 31);
    context.font = "600 11px ui-monospace, SFMono-Regular, Menlo, monospace";
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillStyle = "rgba(209,213,219,0.86)";
    context.fillText("趋势总览", 61, 30);
    const facetTotal = points.reduce((total, point) => total + (point.facets?.length || 0), 0);
    const hidden = Math.max(0, (center.totalCount || points.length) - points.length);
    const budget = `可见 ${points.length} 主题 / ${facetTotal} 维度${hidden ? ` / ${hidden} 待下钻` : ""}`;
    context.font = "11px ui-monospace, SFMono-Regular, Menlo, monospace";
    context.textAlign = "left";
    context.fillStyle = "rgba(127,176,201,0.64)";
    context.fillText(budget, 14, height - 15);
    context.restore();
  }

  function drawSparkline(canvas, values, state) {
    if (!canvas || typeof canvas.getContext !== "function" || !Array.isArray(values)) return;
    const width = Math.max(220, Math.round(canvas.clientWidth || 280));
    const height = Math.max(68, Math.round(canvas.clientHeight || 74));
    const context = canvas.getContext("2d");
    if (!context) return;
    resizeCanvasBackingStore(
      canvas,
      context,
      width,
      height,
      Number(globalThis.devicePixelRatio) || 1,
    );
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

  function buildGraphUrl(id, basePath = "/", returnTo = "") {
    if (typeof id !== "string" || !TOPIC_ID.test(id)) return "#";
    const normalizedBase = typeof basePath === "string" && basePath.startsWith("/")
      ? `${basePath.replace(/\/+$/u, "")}/`
      : "/";
    const path = `${normalizedBase === "//" ? "/" : normalizedBase}${GRAPH_ROUTE.slice(1)}`.replace(/\/+/gu, "/");
    const params = new URLSearchParams({ mode: "focus", node: id });
    const safeReturn = safeInternalUrl(returnTo);
    if (returnTo && safeReturn !== "#") params.set("return_to", safeReturn);
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

  function createTrendSelect(document, select, windowObject = globalThis) {
    const host = select?.closest?.("[data-trend-select]");
    if (!host || host.dataset.enhanced === "true" || !document.body) return null;

    const listId = `${select.id}-listbox`;
    const triggerId = `${select.id}-trigger`;
    const label = document.querySelector(`label[for="${select.id}"]`);
    const previousTabIndex = select.getAttribute("tabindex");
    const previousHidden = select.hidden;
    const trigger = document.createElement("button");
    const value = document.createElement("span");
    const list = document.createElement("div");
    let activeIndex = Math.max(0, select.selectedIndex);
    let typeahead = "";
    let typeaheadTimer = 0;
    let positionFrame = 0;
    let positionScheduled = false;
    let destroyed = false;

    trigger.id = triggerId;
    trigger.type = "button";
    trigger.className = "trend-select__trigger";
    trigger.setAttribute("role", "combobox");
    trigger.setAttribute("aria-haspopup", "listbox");
    trigger.setAttribute("aria-expanded", "false");
    trigger.setAttribute("aria-controls", listId);
    trigger.setAttribute("aria-autocomplete", "none");
    trigger.setAttribute("aria-labelledby", label?.id ? `${label.id} ${triggerId}` : triggerId);

    value.className = "trend-select__value";
    trigger.append(value);

    list.id = listId;
    list.className = "trend-select__list";
    list.setAttribute("role", "listbox");
    list.setAttribute("aria-labelledby", label?.id || triggerId);
    list.hidden = true;

    host.append(trigger);
    document.body.append(list);
    select.tabIndex = -1;
    select.setAttribute("aria-hidden", "true");
    select.hidden = true;
    host.dataset.enhanced = "true";
    host.dataset.open = "false";

    function optionParts(option) {
      const text = String(option?.textContent || "").trim();
      const match = text.match(/^(.*?)(?:\s+·\s+(.+))$/u);
      return match ? { label: match[1], meta: match[2] } : { label: text, meta: "" };
    }

    function optionNodes() {
      return Array.from(list.querySelectorAll('[role="option"]'));
    }

    function syncSelection() {
      const options = Array.from(select.options || []);
      const selectedIndex = Math.max(0, options.findIndex((option) => option.value === select.value));
      activeIndex = Math.min(Math.max(0, activeIndex), Math.max(0, options.length - 1));
      optionNodes().forEach((node, index) => {
        node.setAttribute("aria-selected", String(index === selectedIndex));
        node.dataset.active = String(index === activeIndex);
      });
      value.textContent = optionParts(options[selectedIndex] || options[0]).label || "请选择";
    }

    function setActive(index, scroll = true) {
      const nodes = optionNodes();
      if (!nodes.length) return;
      activeIndex = Math.max(0, Math.min(nodes.length - 1, index));
      nodes.forEach((node, position) => {
        node.dataset.active = String(position === activeIndex);
      });
      trigger.setAttribute("aria-activedescendant", nodes[activeIndex].id);
      if (scroll) nodes[activeIndex].scrollIntoView?.({ block: "nearest" });
    }

    function refresh() {
      if (destroyed) return;
      const options = Array.from(select.options || []);
      list.replaceChildren();
      options.forEach((option, index) => {
        const item = document.createElement("button");
        const copy = optionParts(option);
        const itemLabel = document.createElement("span");
        item.id = `${listId}-option-${index}`;
        item.type = "button";
        item.setAttribute("role", "option");
        item.tabIndex = -1;
        item.dataset.value = option.value;
        itemLabel.className = "trend-select__option-label";
        itemLabel.textContent = copy.label;
        item.append(itemLabel);
        if (copy.meta) {
          const meta = document.createElement("span");
          meta.className = "trend-select__option-meta";
          meta.textContent = copy.meta;
          item.append(meta);
        }
        list.append(item);
      });
      activeIndex = Math.max(0, select.selectedIndex);
      syncSelection();
      if (!list.hidden) schedulePosition();
    }

    function positionList() {
      if (list.hidden) return;
      const rect = trigger.getBoundingClientRect();
      const viewportWidth = Math.max(320, windowObject.innerWidth || document.documentElement.clientWidth || 0);
      const viewportHeight = Math.max(320, windowObject.innerHeight || document.documentElement.clientHeight || 0);
      const width = Math.max(180, Math.min(rect.width, viewportWidth - 16));
      const left = Math.max(8, Math.min(viewportWidth - width - 8, rect.left));
      list.style.width = `${Math.round(width)}px`;
      list.style.left = `${Math.round(left)}px`;
      const menuHeight = Math.min(286, list.scrollHeight || 0);
      const below = viewportHeight - rect.bottom - 8;
      const above = rect.top - 8;
      const openAbove = below < Math.min(menuHeight, 220) && above > below;
      const top = openAbove
        ? Math.max(8, rect.top - menuHeight - 6)
        : Math.min(viewportHeight - menuHeight - 8, rect.bottom + 6);
      list.style.top = `${Math.max(8, Math.round(top))}px`;
      list.dataset.placement = openAbove ? "top" : "bottom";
    }

    function close(focus = false) {
      if (destroyed || list.hidden) return;
      list.hidden = true;
      host.dataset.open = "false";
      trigger.setAttribute("aria-expanded", "false");
      trigger.removeAttribute("aria-activedescendant");
      typeahead = "";
      if (focus) trigger.focus();
    }

    function cancelScheduledPosition() {
      if (!positionScheduled) return;
      windowObject.clearTimeout(positionFrame);
      positionFrame = 0;
      positionScheduled = false;
    }

    function schedulePosition() {
      if (destroyed || list.hidden || positionScheduled) return;
      positionScheduled = true;
      const update = () => {
        positionScheduled = false;
        positionFrame = 0;
        if (!destroyed && !list.hidden) positionList();
      };
      positionFrame = windowObject.setTimeout(update, 16);
    }

    function open() {
      if (destroyed || !list.hidden) return;
      refresh();
      list.hidden = false;
      host.dataset.open = "true";
      trigger.setAttribute("aria-expanded", "true");
      activeIndex = Math.max(0, select.selectedIndex);
      setActive(activeIndex, false);
      positionList();
      optionNodes()[activeIndex]?.scrollIntoView?.({ block: "nearest" });
    }

    function choose(index) {
      const options = Array.from(select.options || []);
      const option = options[index];
      if (!option) return;
      const changed = select.value !== option.value;
      select.value = option.value;
      activeIndex = index;
      syncSelection();
      close(true);
      if (changed) {
        const EventConstructor = windowObject.Event || globalThis.Event;
        select.dispatchEvent(new EventConstructor("change", { bubbles: true }));
      }
    }

    function move(delta) {
      const length = select.options?.length || 0;
      if (!length) return;
      if (list.hidden) open();
      setActive((activeIndex + delta + length) % length);
    }

    function onTriggerClick() {
      if (list.hidden) open();
      else close(false);
    }

    function onTriggerKeydown(event) {
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        move(event.key === "ArrowDown" ? 1 : -1);
        return;
      }
      if (event.key === "Home" || event.key === "End") {
        event.preventDefault();
        if (list.hidden) open();
        setActive(event.key === "Home" ? 0 : Math.max(0, select.options.length - 1));
        return;
      }
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        if (list.hidden) open();
        else choose(activeIndex);
        return;
      }
      if (event.key === "Escape") {
        if (!list.hidden) {
          event.preventDefault();
          event.stopPropagation();
          close(true);
        }
        return;
      }
      if (event.key === "Tab") {
        close(false);
        return;
      }
      if (event.key.length !== 1 || event.ctrlKey || event.metaKey || event.altKey) return;
      typeahead += event.key.toLocaleLowerCase("zh-CN");
      windowObject.clearTimeout(typeaheadTimer);
      typeaheadTimer = windowObject.setTimeout(() => { typeahead = ""; }, 560);
      const options = Array.from(select.options || []);
      const index = options.findIndex((option) => (
        optionParts(option).label.toLocaleLowerCase("zh-CN").startsWith(typeahead)
      ));
      if (index >= 0) {
        event.preventDefault();
        if (list.hidden) open();
        setActive(index);
      }
    }

    function onListClick(event) {
      const option = event.target.closest?.('[role="option"]');
      if (!option || !list.contains(option)) return;
      choose(optionNodes().indexOf(option));
    }

    function onListPointerDown(event) {
      if (event.pointerType === "mouse") event.preventDefault();
    }

    function onPointerDown(event) {
      if (host.contains(event.target) || list.contains(event.target)) return;
      close(false);
    }

    function onLabelClick(event) {
      event.preventDefault();
      trigger.focus();
    }

    function onViewportChange(event) {
      if (event?.type === "scroll" && list.contains(event.target)) return;
      schedulePosition();
    }

    trigger.addEventListener("click", onTriggerClick);
    trigger.addEventListener("keydown", onTriggerKeydown);
    list.addEventListener("click", onListClick);
    list.addEventListener("pointerdown", onListPointerDown);
    select.addEventListener("change", syncSelection);
    label?.addEventListener("click", onLabelClick);
    document.addEventListener("pointerdown", onPointerDown);
    windowObject.addEventListener?.("resize", onViewportChange);
    windowObject.addEventListener?.("scroll", onViewportChange, true);
    refresh();

    return Object.freeze({
      close,
      refresh,
      trigger,
      destroy() {
        if (destroyed) return;
        destroyed = true;
        windowObject.clearTimeout(typeaheadTimer);
        cancelScheduledPosition();
        trigger.removeEventListener("click", onTriggerClick);
        trigger.removeEventListener("keydown", onTriggerKeydown);
        list.removeEventListener("click", onListClick);
        list.removeEventListener("pointerdown", onListPointerDown);
        select.removeEventListener("change", syncSelection);
        label?.removeEventListener("click", onLabelClick);
        document.removeEventListener("pointerdown", onPointerDown);
        windowObject.removeEventListener?.("resize", onViewportChange);
        windowObject.removeEventListener?.("scroll", onViewportChange, true);
        list.remove();
        trigger.remove();
        host.removeAttribute("data-enhanced");
        host.removeAttribute("data-open");
        select.removeAttribute("aria-hidden");
        select.hidden = previousHidden;
        if (previousTabIndex === null) select.removeAttribute("tabindex");
        else select.setAttribute("tabindex", previousTabIndex);
      },
    });
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
      filterSummary: document.getElementById("trend-filter-summary"),
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
      matrixTooltip: document.getElementById("trend-matrix-tooltip"),
      list: document.getElementById("trend-list"),
      empty: document.getElementById("trend-empty"),
      detail: document.getElementById("trend-detail"),
    };
    if (Object.values(elements).some((element) => !element)) return null;
    const listenerCleanups = [];
    let destroyed = false;
    function listen(target, type, handler, options) {
      if (typeof target?.addEventListener !== "function") return;
      target.addEventListener(type, handler, options);
      listenerCleanups.push(() => target.removeEventListener(type, handler, options));
    }
    const selectMenus = [elements.signal, elements.source, elements.scenario]
      .map((select) => createTrendSelect(document, select, windowObject))
      .filter(Boolean);

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
    listen(filterMedia, "change", handleFilterViewportChange);

    function updateHistory(push = false) {
      const url = buildTrendReturnUrl(windowObject.location.pathname, model.state);
      if (push) windowObject.history.pushState({ trends: true }, "", url);
      else windowObject.history.replaceState({ trends: true }, "", url);
    }

    function setButtonStates() {
      root.dataset.view = model.state.view;
      root.dataset.detail = model.state.topic ? "open" : "closed";
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
      selectMenus.forEach((menu) => menu.refresh());
    }

    function appendOption(select, value, label) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      select.append(option);
    }

    function populateFacets() {
      const facets = model.windowData?.facets;
      if (!facets) return false;
      const reconciled = reconcileFacetState(model.state, facets);
      model.state = reconciled.state;
      const sourceValue = model.state.source;
      const scenarioValue = model.state.scenario;
      elements.source.replaceChildren();
      elements.scenario.replaceChildren();
      appendOption(elements.source, "", "全部来源");
      appendOption(elements.scenario, "", "全部场景");
      facets.sources.forEach((facet) => appendOption(
        elements.source,
        facet.name,
        `${formatSourceName(facet.name)} · ${formatNumber(countFacetTopics(model.windowData.trends, "sources", facet.name))} 主题 / ${formatNumber(facet.count)} 条证据`,
      ));
      facets.scenarios.forEach((facet) => appendOption(
        elements.scenario,
        facet.name,
        `${facet.name} · ${formatNumber(countFacetTopics(model.windowData.trends, "scenarios", facet.name))} 主题 / ${formatNumber(facet.count)} 条证据`,
      ));
      elements.source.value = [...elements.source.options].some((option) => option.value === sourceValue)
        ? sourceValue
        : "";
      elements.scenario.value = [...elements.scenario.options].some((option) => option.value === scenarioValue)
        ? scenarioValue
        : "";
      model.state.source = elements.source.value;
      model.state.scenario = elements.scenario.value;
      selectMenus.forEach((menu) => menu.refresh());
      return reconciled.changed;
    }

    function clearTopicOutsideResults(trends) {
      if (!model.state.topic || trends.some((trend) => trend.id === model.state.topic)) return false;
      invalidateTopicLoad(model);
      model.state.topic = "";
      model.returnTopicId = "";
      model.returnToStage = false;
      renderDetailPlaceholder();
      return true;
    }

    function currentTrend(id = model.state.topic) {
      return model.windowData?.trends.find((item) => item.id === id) || null;
    }

    function renderList(trends) {
      elements.list.replaceChildren();
      trends.forEach((item) => {
        const rank = model.windowData.trends.findIndex((candidate) => candidate.id === item.id) + 1;
        const visual = heatVisual(item.score);
        const scoreCopy = trendCardScoreCopy(item);
        const row = document.createElement("li");
        row.className = "trend-card";
        row.dataset.heat = visual.key;
        const button = document.createElement("button");
        button.type = "button";
        button.className = "trend-card__button";
        button.dataset.topicId = item.id;
        button.setAttribute("aria-pressed", String(model.state.topic === item.id));
        button.setAttribute(
          "aria-label",
          `查看 ${item.topic} 趋势详情，${scoreCopy.status}，${scoreCopy.heat}，综合得分 ${scoreCopy.score}，${scoreCopy.evidence} 篇证据，${scoreCopy.sources} 个来源`,
        );
        appendText(document, button, "span", "trend-card__rank", String(rank).padStart(2, "0"));
        const copy = document.createElement("span");
        copy.className = "trend-card__copy";
        appendText(document, copy, "strong", "trend-card__title", item.topic);
        appendText(
          document,
          copy,
          "small",
          "trend-card__meta",
          scoreCopy.status,
        );
        button.append(copy);
        const details = document.createElement("span");
        details.className = "trend-card__focus-details";
        details.setAttribute("aria-hidden", "true");
        appendText(document, details, "strong", "", `${scoreCopy.heat} · ${scoreCopy.score} 分`);
        appendText(
          document,
          details,
          "small",
          "",
          `${scoreCopy.evidence} 篇证据 · ${scoreCopy.sources} 个来源`,
        );
        button.append(details);
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
      const rankById = new Map(model.windowData.trends.map((item, index) => [item.id, index + 1]));
      model.points = layoutMatrix(
        trends,
        rect.width || 900,
        rect.height || 620,
        model.state.topic,
        rankById,
      );
      drawMatrix(elements.matrix, model.points, model.state.topic, model.hoveredId);
    }

    function renderResults() {
      if (!model.windowData) return;
      model.hoveredId = "";
      renderMatrixTooltip(document, elements.matrixTooltip, null);
      const trends = filterTrends(model.windowData.trends, model.state);
      elements.resultCount.textContent = `${formatNumber(trends.length)} 个主题`;
      elements.empty.hidden = trends.length !== 0;
      elements.matrixPanel.hidden = trends.length === 0;
      renderList(trends);
      renderMatrix(trends);
      elements.statTopics.textContent = formatNumber(model.index.stats.windows[model.state.window].trend_count);
      elements.statSources.textContent = formatNumber(model.index.stats.windows[model.state.window].source_count);
      elements.statWindow.textContent = WINDOW_LABELS[model.state.window];
      const activeFilters = [];
      if (model.state.signal !== "all") activeFilters.push(`状态 ${STATE_LABELS[model.state.signal]}`);
      if (model.state.source) activeFilters.push(`来源 ${formatSourceName(model.state.source)}`);
      if (model.state.scenario) activeFilters.push(`场景 ${model.state.scenario}`);
      if (model.state.query) activeFilters.push(`主题 “${model.state.query}”`);
      elements.filterSummary.dataset.active = String(activeFilters.length > 0);
      elements.filterSummary.textContent = activeFilters.length
        ? `当前筛选：${activeFilters.join(" / ")} · 命中 ${trends.length} 个主题；场景与来源按匹配证据强度排序。`
        : `当前未启用附加筛选 · 共 ${trends.length} 个主题。`;
      setButtonStates();
      setStatus(
        trends.length
          ? `已发现 ${trends.length} 个可解释趋势；拓扑首屏显示至多 ${MAX_TOPOLOGY_CELLS} 个主题细胞域，选择即可下钻证据。`
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

    function appendScoreExplanation(parent, signal) {
      if (!signal) return;
      const explanation = scoreExplanation(signal, model.state.window, model.index.formula);
      const section = document.createElement("section");
      section.className = "trend-detail-section trend-score-method";
      appendText(document, section, "h3", "", "评分公式与窗口语义");
      appendText(
        document,
        section,
        "p",
        "trend-score-method__window",
        `窗口采用互斥时间切片：${explanation.ranges.join("；")}。当前窗口包含起止边界，前序窗口不含右边界。`,
      );
      const formula = appendText(
        document,
        section,
        "code",
        "trend-score-method__formula",
        explanation.formula,
      );
      formula.setAttribute("aria-label", "趋势综合评分公式");
      const audit = document.createElement("dl");
      audit.className = "trend-score-method__audit";
      [
        ["加权子项", `${(explanation.weightedSubtotal * 100).toFixed(1)}%`],
        ["去重结果", `${formatNumber(explanation.uniqueEvents)} / ${formatNumber(explanation.observations)} 条观测`],
        ["重复惩罚", `${(explanation.duplicateRate * 100).toFixed(1)}% → × ${(explanation.duplicateMultiplier * 100).toFixed(1)}%`],
        ["公式复算", `${explanation.recomputedScore.toFixed(1)} 分`],
      ].forEach(([label, value]) => {
        const cell = document.createElement("div");
        appendText(document, cell, "dt", "", label);
        appendText(document, cell, "dd", "", value);
        audit.append(cell);
      });
      section.append(audit);
      appendText(
        document,
        section,
        "p",
        "trend-score-method__definition",
        `增长：${explanation.growthDefinition}；加速度：${explanation.accelerationDefinition}。两者 0.5 表示持平或无加速，所有子项限制在 0–1。`,
      );
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
        link.href = appendReturnContext(
          withBasePath(item.internal_url, root.dataset.basePath || "/"),
          buildTrendReturnUrl(windowObject.location.pathname, model.state),
        );
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
        const association = evidenceAssociationCopy(
          item,
          root.dataset.basePath || "/",
        );
        if (association) {
          const lineage = document.createElement("a");
          lineage.className = "trend-evidence-lineage";
          lineage.href = appendReturnContext(
            association.href,
            buildTrendReturnUrl(windowObject.location.pathname, model.state),
          );
          lineage.textContent = `${association.label} · 查看溯源`;
          lineage.setAttribute("aria-label", `${item.title}，${association.label}，查看情报溯源`);
          row.append(lineage);
        }
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
      graph.href = buildGraphUrl(
        topic.graph_node_id,
        root.dataset.basePath || "/",
        buildTrendReturnUrl(windowObject.location.pathname, model.state),
      );
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
        appendScoreExplanation(elements.detail, signal);
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

      if (signal) appendComponents(elements.detail, signal.components);
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
      const sequence = invalidateTopicLoad(model);
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
      const controller = new AbortController();
      model.topicController = controller;
      showDetailLoading();
      try {
        const ref = model.index.topics[id];
        const url = resolveAssetUrl(root.dataset.indexUrl, ref.path, windowObject);
        const raw = await fetchJson(url, {
          signal: controller.signal,
          maximumBytes: MAX_TOPIC_BYTES,
          expectedBytes: ref.bytes,
          expectedSha256: ref.sha256,
        }, windowObject);
        if (sequence !== model.topicSequence) return;
        if (model.topicController === controller) model.topicController = null;
        const topic = validateTopic(raw, id, model.index);
        model.topicCache.set(id, topic);
        renderDetail(topic);
        completeDetailTransition(options);
      } catch (error) {
        if (sequence !== model.topicSequence) return;
        if (model.topicController === controller) model.topicController = null;
        if (error?.name === "AbortError") return;
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
      if (!windowObject.matchMedia?.("(max-width: 1439px)").matches) return;
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
      invalidateTopicLoad(model);
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
      invalidateTopicLoad(model);
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
        const facetsChanged = populateFacets();
        const topicChanged = clearTopicOutsideResults(filterTrends(model.windowData.trends, model.state));
        if (facetsChanged || topicChanged) updateHistory(false);
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
      clearTopicOutsideResults(filterTrends(model.windowData?.trends || [], model.state));
      updateHistory(push);
      renderResults();
    }

    document.querySelectorAll("[data-trend-window]").forEach((button) => {
      listen(button, "click", () => {
        const windowName = button.dataset.trendWindow;
        if (windowName !== model.state.window) loadWindow(windowName, { push: true });
      });
    });
    document.querySelectorAll("[data-trend-view]").forEach((button) => {
      listen(button, "click", () => {
        const view = button.dataset.trendView;
        if (!VIEWS.includes(view) || view === model.state.view) return;
        model.state.view = view;
        updateHistory(true);
        renderResults();
      });
    });
    listen(elements.query, "input", () => changeFilters(false));
    listen(elements.signal, "change", () => changeFilters(true));
    listen(elements.source, "change", () => changeFilters(true));
    listen(elements.scenario, "change", () => changeFilters(true));
    listen(elements.clear, "click", () => {
      model.state = { ...model.state, signal: "all", source: "", scenario: "", query: "" };
      setButtonStates();
      updateHistory(true);
      renderResults();
      elements.query.focus();
    });
    listen(elements.filterToggle, "click", () => {
      setFilterPanel(elements.filterToggle.getAttribute("aria-expanded") !== "true");
    });

    listen(elements.list, "click", (event) => {
      const button = event.target.closest?.("[data-topic-id]");
      if (button) loadTopic(button.dataset.topicId, {
        push: true,
        scroll: true,
        focus: true,
        returnTopicId: button.dataset.topicId,
      });
    });
    listen(elements.matrix, "click", (event) => {
      const rect = elements.matrix.getBoundingClientRect();
      const point = hitTestMatrix(model.points, event.clientX - rect.left, event.clientY - rect.top);
      if (point) loadTopic(point.id, { push: true, scroll: true, focus: true, returnToStage: true });
    });
    listen(elements.matrix, "mousemove", (event) => {
      const rect = elements.matrix.getBoundingClientRect();
      const point = hitTestMatrix(model.points, event.clientX - rect.left, event.clientY - rect.top);
      const nextHoveredId = point?.id || "";
      if (nextHoveredId !== model.hoveredId || (point && elements.matrixTooltip?.hidden)) {
        model.hoveredId = nextHoveredId;
        drawMatrix(elements.matrix, model.points, model.state.topic, model.hoveredId);
        renderMatrixTooltip(document, elements.matrixTooltip, point);
      }
      elements.matrix.style.cursor = point ? "pointer" : "default";
      positionMatrixTooltip(elements.matrixTooltip, elements.matrixPanel, event.clientX, event.clientY);
    });
    listen(elements.matrix, "mouseleave", () => {
      renderMatrixTooltip(document, elements.matrixTooltip, null);
      if (!model.hoveredId) return;
      model.hoveredId = "";
      drawMatrix(elements.matrix, model.points, model.state.topic, "");
    });
    listen(elements.detail, "click", (event) => {
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

    listen(windowObject, "popstate", async () => {
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
        if (model.state.topic) completeDetailTransition({ focus: true, scroll: true });
        else restoreTrendOrigin(previousTopic, Boolean(previousTopic));
      } else {
        const reconciled = reconcileFacetState(model.state, model.windowData?.facets || {});
        if (reconciled.changed) {
          model.state = reconciled.state;
          setButtonStates();
          updateHistory(false);
        }
        renderResults();
        if (model.state.topic) await loadTopic(model.state.topic, { push: false, focus: true, scroll: true });
        else {
          renderDetailPlaceholder();
          restoreTrendOrigin(previousTopic, Boolean(previousTopic));
        }
      }
    });
    listen(document, "keydown", (event) => {
      if (event.key === "Escape" && model.state.topic) {
        closeTopicDetail(true);
      }
    });
    function destroy() {
      if (destroyed) return;
      destroyed = true;
      model.windowController?.abort();
      invalidateTopicLoad(model);
      model.resizeObserver?.disconnect();
      selectMenus.forEach((menu) => menu.destroy());
      listenerCleanups.splice(0).forEach((cleanup) => cleanup());
      root.removeAttribute("data-trends-ready");
    }
    function handlePageHide(event) {
      if (!shouldDestroyOnPageHide(event)) {
        selectMenus.forEach((menu) => menu.close(false));
        return;
      }
      destroy();
    }
    listen(windowObject, "pagehide", handlePageHide);

    if (typeof windowObject.ResizeObserver === "function") {
      model.resizeObserver = new windowObject.ResizeObserver(() => {
        if (model.windowData) renderMatrix(filterTrends(model.windowData.trends, model.state));
      });
      model.resizeObserver.observe(elements.matrix);
    } else {
      listen(windowObject, "resize", () => {
        if (model.windowData) renderMatrix(filterTrends(model.windowData.trends, model.state));
      });
    }

    initialise();
    return Object.freeze({ model, loadWindow, loadTopic, destroy });
  }

  return {
    TrendDataError,
    adaptStateForViewport,
    appendReturnContext,
    buildGraphUrl,
    buildTrendReturnUrl,
    countFacetTopics,
    drawMatrix,
    drawSparkline,
    filterTrends,
    evidenceAssociationCopy,
    formatSourceName,
    freshnessStatus,
    heatTier,
    heatVisual,
    hitTestMatrix,
    initializeTrendsPage,
    invalidateTopicLoad,
    layoutMatrix,
    layoutPointLabels,
    labeledPointIds,
    matrixBadgeCopy,
    matrixTooltipCopy,
    nodeGlowVisual,
    topologyNodeVisual,
    parseState,
    resizeCanvasBackingStore,
    reconcileFacetState,
    resolveCanvasPixelRatio,
    resolveWindowSignal,
    safeAssetPath,
    safeInternalUrl,
    scoreExplanation,
    serializeState,
    shouldDestroyOnPageHide,
    shouldRenderMatrix,
    toggleWatchlistTopic,
    trendCardScoreCopy,
    validateIndex,
    validateTopic,
    validateWindow,
    withBasePath,
  };
}));
