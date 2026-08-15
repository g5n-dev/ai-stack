import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

const require = createRequire(import.meta.url);
const Trends = require("../../blog/static/js/trends.js");


function trend(overrides = {}) {
  return {
    id: "tag:llm",
    topic: "LLM",
    score: 82.4,
    state: "rising",
    confidence: "high",
    unique_events: 12,
    observations: 12,
    unique_sources: 3,
    duplicate_rate: 0,
    counts: { current: 12, previous: 7, pre_previous: 4 },
    components: {
      quantity: 1,
      growth: 0.7,
      acceleration: 0.62,
      source_diversity: 0.25,
      novelty: 0.3,
      source_weight: 0.8,
    },
    sparkline: [2, 3, 4, 5, 8, 9, 12],
    sources: [{ name: "arXiv", count: 8 }, { name: "Hacker News", count: 4 }],
    scenarios: [{ name: "模型研发", count: 7 }],
    detail_path: "topics/llm-a1b2c3d4.json",
    ...overrides,
  };
}


test("parses only bounded trend URL state and preserves a valid topic drill-down", () => {
  const state = Trends.parseState(
    "?window=7d&signal=rising&source=arxiv&scenario=%E6%A8%A1%E5%9E%8B%E7%A0%94%E5%8F%91&topic=tag%3Allm&view=list&ignored=boom",
  );

  assert.deepEqual(state, {
    window: "7d",
    signal: "rising",
    source: "arxiv",
    scenario: "模型研发",
    query: "",
    topic: "tag:llm",
    view: "list",
  });
  assert.equal(
    Trends.serializeState(state),
    "?window=7d&signal=rising&source=arxiv&scenario=%E6%A8%A1%E5%9E%8B%E7%A0%94%E5%8F%91&topic=tag%3Allm&view=list",
  );
});


test("rejects unsafe URL state and falls back to the honest 30 day matrix", () => {
  assert.deepEqual(Trends.parseState("?window=year&signal=viral&topic=javascript:boom&query=%00"), {
    window: "30d",
    signal: "all",
    source: "",
    scenario: "",
    query: "",
    topic: "",
    view: "matrix",
  });
});


test("compact view uses the accessible list instead of claiming a hidden matrix", () => {
  const desktop = Trends.adaptStateForViewport(Trends.parseState("?window=30d"), false);
  const compact = Trends.adaptStateForViewport(Trends.parseState("?window=30d"), true);

  assert.equal(desktop.view, "matrix");
  assert.equal(compact.view, "list");
  assert.equal(Trends.serializeState(compact), "?window=30d&view=list");
  assert.equal(Trends.shouldRenderMatrix("list", false), false);
  assert.equal(Trends.shouldRenderMatrix("matrix", true), false);
  assert.equal(Trends.shouldRenderMatrix("matrix", false), true);
});


test("BFCache pagehide preserves the enhanced controls until a real unload", () => {
  assert.equal(Trends.shouldDestroyOnPageHide({ persisted: true }), false);
  assert.equal(Trends.shouldDestroyOnPageHide({ persisted: false }), true);
  assert.equal(Trends.shouldDestroyOnPageHide({}), true);
});


test("topic drill-down never borrows a signal from another observation window", () => {
  const windows = {
    "24h": null,
    "7d": trend({ id: "tag:agent", topic: "Agent" }),
    "30d": trend({ id: "tag:agent", topic: "Agent", score: 91 }),
  };

  assert.equal(Trends.resolveWindowSignal(null, windows, "24h"), null);
  assert.equal(Trends.resolveWindowSignal(null, windows, "7d")?.score, 82.4);
  assert.equal(Trends.resolveWindowSignal(trend({ score: 77 }), windows, "24h")?.score, 77);
});


test("freshness labels static snapshots without realtime claims", () => {
  const cutoff = "2026-07-16T00:00:00Z";

  assert.deepEqual(Trends.freshnessStatus(cutoff, Date.parse("2026-07-16T11:59:59Z")), {
    key: "fresh",
    label: "静态快照",
  });
  assert.deepEqual(Trends.freshnessStatus(cutoff, Date.parse("2026-07-17T12:00:00Z")), {
    key: "delayed",
    label: "数据延迟",
  });
  assert.deepEqual(Trends.freshnessStatus(cutoff, Date.parse("2026-07-18T00:00:01Z")), {
    key: "stale",
    label: "数据过期",
  });
});


test("heat tiers use stable cross-window thresholds with monotonic visual emphasis", () => {
  const boundaries = [
    [0, "cold"],
    [49.999, "cold"],
    [50, "watch"],
    [59.999, "watch"],
    [60, "active"],
    [66.999, "active"],
    [67, "hot"],
    [69.999, "hot"],
    [70, "signal"],
    [100, "signal"],
  ];

  assert.deepEqual(
    boundaries.map(([score]) => Trends.heatTier(score)),
    boundaries.map(([, expected]) => expected),
  );

  const visuals = [0, 50, 60, 67, 70].map((score) => Trends.heatVisual(score));
  assert.deepEqual(visuals.map((item) => item.key), ["cold", "watch", "active", "hot", "signal"]);
  assert.deepEqual(visuals.map((item) => item.label), ["低热", "观察", "活跃", "高热", "强信号"]);
  for (let index = 1; index < visuals.length; index += 1) {
    assert.ok(visuals[index].rings > visuals[index - 1].rings);
    assert.ok(visuals[index].glow > visuals[index - 1].glow);
  }
});


test("topology badges keep only topic and direction while hover owns score details", () => {
  const [point] = Trends.layoutMatrix([
    trend({ topic: "Amazon Bedrock", score: 73, state: "rising", unique_sources: 4,
      counts: { current: 16, previous: 9, pre_previous: 5 } }),
  ], 900, 480);

  assert.deepEqual(Trends.matrixBadgeCopy(point), {
    title: "01  Amazon Bedrock",
    status: "↑ 上升",
  });
  assert.deepEqual(Trends.matrixTooltipCopy(point), {
    topic: "Amazon Bedrock",
    rank: "01",
    status: "↑ 上升",
    heat: "强信号",
    score: "73",
    evidence: "16",
    sources: "4",
  });

  assert.equal(Trends.matrixBadgeCopy({ ...point, state: "steady" }).status, "• 稳定");
  assert.equal(Trends.matrixBadgeCopy({ ...point, state: "cooling" }).status, "↓ 降温");
  assert.equal(Trends.matrixBadgeCopy({ ...point, state: "new" }).status, "✦ 新出现");
});


test("keyboard trend cards expose the same score detail as topology hover", () => {
  const value = trend({
    topic: "Amazon Bedrock",
    score: 73,
    state: "steady",
    unique_events: 16,
    unique_sources: 4,
    counts: { current: 16, previous: 16, pre_previous: 12 },
  });
  const [point] = Trends.layoutMatrix([value], 900, 480);

  assert.deepEqual(Trends.trendCardScoreCopy(value), {
    status: "• 稳定",
    heat: "强信号",
    score: "73",
    evidence: "16",
    sources: "4",
  });
  assert.deepEqual(
    Trends.trendCardScoreCopy(value),
    (({ status, heat, score, evidence, sources }) => ({ status, heat, score, evidence, sources }))(
      Trends.matrixTooltipCopy(point),
    ),
  );
});


test("score explanation makes formula, window buckets and duplicate penalty auditable", () => {
  const formula = "100 × weighted_components × (1 − 0.5×duplicate_rate)";
  const explanation = Trends.scoreExplanation(trend({
    score: 58.23125,
    observations: 16,
    duplicate_rate: 0.25,
  }), "7d", formula);

  assert.equal(explanation.formula, formula);
  assert.equal(explanation.windowLabel, "7 天");
  assert.deepEqual(explanation.ranges, [
    "当前：[截止−7 天, 截止]",
    "上一周期：[截止−14 天, 截止−7 天)",
    "前两周期：[截止−21 天, 截止−14 天)",
  ]);
  assert.match(explanation.growthDefinition, /current−previous/u);
  assert.match(explanation.accelerationDefinition, /previous−pre_previous/u);
  assert.equal(explanation.duplicateCount, 4);
  assert.equal(explanation.duplicateRate, 0.25);
  assert.equal(explanation.duplicateMultiplier, 0.875);
  assert.equal(explanation.weightedSubtotal, 0.6655);
  assert.equal(explanation.recomputedScore, 58.23125);
});


test("every topology node receives a visible heat-scaled glow budget", () => {
  const cold = Trends.nodeGlowVisual({ score: 30 }, false, false);
  const hot = Trends.nodeGlowVisual({ score: 73 }, false, false);
  const selected = Trends.nodeGlowVisual({ score: 73 }, true, false);
  const hovered = Trends.nodeGlowVisual({ score: 73 }, false, true);

  assert.ok(cold.blur >= 16);
  assert.ok(cold.facetBlur >= 8);
  assert.ok(cold.haloAlpha >= 0.26);
  assert.ok(cold.auraAlpha >= 0.1);
  assert.ok(hot.blur > cold.blur);
  assert.ok(hot.haloAlpha > cold.haloAlpha);
  assert.ok(hot.auraAlpha > cold.auraAlpha);
  assert.ok(selected.blur > hot.blur);
  assert.ok(hovered.blur > hot.blur);
});


test("topology keeps every outer node luminous teal and reserves amber for focus", () => {
  const coldOuter = Trends.topologyNodeVisual({ score: 30 }, false);
  const hotOuter = Trends.topologyNodeVisual({ score: 73 }, false);
  const focused = Trends.topologyNodeVisual({ score: 30 }, true);

  assert.equal(coldOuter.color, "#5adacf");
  assert.equal(hotOuter.color, "#5adacf");
  assert.ok(hotOuter.glow > coldOuter.glow);
  assert.equal(focused.color, "#f3a948");
});


test("filters trends by signal, source, scenario and case-insensitive topic query", () => {
  const values = [
    trend(),
    trend({
      id: "tag:agent",
      topic: "智能体 Agent",
      state: "new",
      sources: [{ name: "GitHub", count: 3 }],
      scenarios: [{ name: "智能体工具", count: 3 }],
    }),
  ];

  assert.deepEqual(
    Trends.filterTrends(values, {
      signal: "new",
      source: "github",
      scenario: "智能体工具",
      query: "AGENT",
    }).map((item) => item.id),
    ["tag:agent"],
  );
  assert.equal(Trends.filterTrends(values, { query: "不存在" }).length, 0);
});


test("facet filters rank the strongest matching evidence before global heat", () => {
  const values = [
    trend({
      id: "tag:global-hot",
      topic: "Global Hot",
      score: 95,
      sources: [{ name: "GitHub", count: 2 }],
      scenarios: [{ name: "大语言模型", count: 3 }],
    }),
    trend({
      id: "tag:facet-strong",
      topic: "Facet Strong",
      score: 61,
      sources: [{ name: "GitHub", count: 9 }],
      scenarios: [{ name: "大语言模型", count: 14 }],
    }),
  ];

  assert.deepEqual(
    Trends.filterTrends(values, { scenario: "大语言模型" }).map((item) => item.id),
    ["tag:facet-strong", "tag:global-hot"],
  );
  assert.deepEqual(
    Trends.filterTrends(values, { source: "github" }).map((item) => item.id),
    ["tag:facet-strong", "tag:global-hot"],
  );
});


test("facet summaries distinguish matching topics from evidence and reconcile stale URL state", () => {
  const values = [
    trend({ sources: [{ name: "GitHub", count: 9 }], scenarios: [{ name: "大语言模型", count: 14 }] }),
    trend({ id: "tag:agent", sources: [{ name: "GitHub", count: 2 }], scenarios: [{ name: "大语言模型", count: 3 }] }),
  ];

  assert.equal(Trends.countFacetTopics(values, "scenarios", "大语言模型"), 2);
  assert.equal(Trends.countFacetTopics(values, "sources", "github"), 2);
  assert.deepEqual(
    Trends.reconcileFacetState(
      { source: "GitHub", scenario: "RAG应用", query: "LLM" },
      { sources: [{ name: "GitHub", count: 11 }], scenarios: [{ name: "大语言模型", count: 17 }] },
    ),
    {
      state: { source: "GitHub", scenario: "", query: "LLM" },
      changed: true,
    },
  );
});


test("committed trend data drills a selective scenario into its strongest matching topic", () => {
  const dataRoot = path.resolve(import.meta.dirname, "../../blog/static/data/stack-trends");
  const index = JSON.parse(readFileSync(path.join(dataRoot, "index.json"), "utf8"));
  const validatedIndex = Trends.validateIndex(index);
  const windowData = JSON.parse(readFileSync(path.join(dataRoot, index.windows["30d"].path), "utf8"));
  const validatedWindow = Trends.validateWindow(windowData, "30d", validatedIndex);
  const selectedScenario = validatedWindow.facets.scenarios.find((facet) => {
    const matches = Trends.countFacetTopics(validatedWindow.trends, "scenarios", facet.name);
    return matches > 0 && matches < validatedWindow.trends.length;
  });

  assert.ok(selectedScenario, "committed data needs at least one selective scenario");
  const filtered = Trends.filterTrends(validatedWindow.trends, { scenario: selectedScenario.name });
  const evidenceCounts = filtered.map((item) => (
    item.scenarios.find((facet) => facet.name === selectedScenario.name)?.count || 0
  ));

  assert.ok(filtered.length > 0 && filtered.length < windowData.trends.length);
  assert.ok(filtered.every((item) => item.scenarios.some((facet) => facet.name === selectedScenario.name)));
  assert.equal(evidenceCounts[0], Math.max(...evidenceCounts));
});


test("every committed 30 day filter independently changes the visible result set", () => {
  const dataRoot = path.resolve(import.meta.dirname, "../../blog/static/data/stack-trends");
  const index = JSON.parse(readFileSync(path.join(dataRoot, "index.json"), "utf8"));
  const windowData = JSON.parse(readFileSync(path.join(dataRoot, index.windows["30d"].path), "utf8"));
  const total = windowData.trends.length;
  const partialState = [...new Set(windowData.trends.map((item) => item.state))]
    .find((state) => {
      const count = windowData.trends.filter((item) => item.state === state).length;
      return count > 0 && count < total;
    });
  const partialSource = windowData.facets.sources.find((facet) => {
    const count = Trends.countFacetTopics(windowData.trends, "sources", facet.name);
    return count > 0 && count < total;
  });
  const partialScenario = windowData.facets.scenarios.find((facet) => {
    const count = Trends.countFacetTopics(windowData.trends, "scenarios", facet.name);
    return count > 0 && count < total;
  });
  assert.ok(partialState, "committed data needs at least one selective signal state");
  assert.ok(partialSource, "committed data needs at least one selective source");
  assert.ok(partialScenario, "committed data needs at least one selective scenario");

  const byState = Trends.filterTrends(windowData.trends, { signal: partialState });
  assert.ok(byState.length > 0 && byState.length < total);
  assert.ok(byState.every((item) => item.state === partialState));

  const bySource = Trends.filterTrends(windowData.trends, { source: partialSource.name });
  assert.ok(bySource.length > 0 && bySource.length < total);
  assert.ok(bySource.every((item) => item.sources.some((facet) => facet.name === partialSource.name)));

  const byScenario = Trends.filterTrends(windowData.trends, { scenario: partialScenario.name });
  assert.ok(byScenario.length > 0 && byScenario.length < total);
  assert.ok(byScenario.every((item) => item.scenarios.some((facet) => facet.name === partialScenario.name)));

  const query = windowData.trends.at(-1).topic;
  const byQuery = Trends.filterTrends(windowData.trends, { query });
  assert.ok(byQuery.length > 0 && byQuery.length < total);
  assert.ok(byQuery.every((item) => item.topic.toLocaleLowerCase("zh-CN").includes(query.toLocaleLowerCase("zh-CN"))));
});


test("committed observation windows select distinct snapshots", () => {
  const dataRoot = path.resolve(import.meta.dirname, "../../blog/static/data/stack-trends");
  const index = JSON.parse(readFileSync(path.join(dataRoot, "index.json"), "utf8"));
  const loadWindow = (name) => JSON.parse(
    readFileSync(path.join(dataRoot, index.windows[name].path), "utf8"),
  );
  const day = loadWindow("24h");
  const month = loadWindow("30d");

  assert.notDeepEqual(day.trends.map((item) => item.id), month.trends.map((item) => item.id));
  assert.notEqual(day.trends.length, month.trends.length);
});


test("builds safe, distinct article and graph drill-down destinations", () => {
  assert.equal(Trends.safeInternalUrl("/2026/07/an-article/?ref=trend"), "/2026/07/an-article/?ref=trend");
  assert.equal(Trends.safeInternalUrl("https://ai-stack.site/2026/07/post/"), "/2026/07/post/");
  assert.equal(Trends.safeInternalUrl("https://evil.example/post/"), "#");
  assert.equal(Trends.safeInternalUrl("javascript:alert(1)"), "#");
  assert.equal(Trends.withBasePath("/2026/07/post/", "/archive/"), "/archive/2026/07/post/");
  assert.equal(Trends.withBasePath("/archive/2026/07/post/", "/archive/"), "/archive/2026/07/post/");
  assert.equal(
    Trends.buildGraphUrl("tag:LLM"),
    "/scenarios/?mode=focus&node=tag%3ALLM",
  );
  assert.equal(Trends.buildGraphUrl("javascript:boom"), "#");
});


test("reload, popstate and drill-down links preserve the complete trend context", () => {
  const state = {
    window: "7d",
    signal: "rising",
    source: "arxiv",
    scenario: "模型研发",
    query: "Agent",
    topic: "tag:LLM",
    view: "list",
  };
  const returnTo = Trends.buildTrendReturnUrl("/trends/", state);

  assert.equal(
    returnTo,
    "/trends/?window=7d&signal=rising&source=arxiv&scenario=%E6%A8%A1%E5%9E%8B%E7%A0%94%E5%8F%91&query=Agent&topic=tag%3ALLM&view=list",
  );
  assert.deepEqual(Trends.parseState(new URL(returnTo, "https://ai-stack.site").search), state);
  assert.equal(
    Trends.buildGraphUrl("tag:LLM", "/", returnTo),
    "/scenarios/?mode=focus&node=tag%3ALLM&return_to=%2Ftrends%2F%3Fwindow%3D7d%26signal%3Drising%26source%3Darxiv%26scenario%3D%25E6%25A8%25A1%25E5%259E%258B%25E7%25A0%2594%25E5%258F%2591%26query%3DAgent%26topic%3Dtag%253ALLM%26view%3Dlist",
  );
  assert.equal(
    Trends.appendReturnContext("/posts/example/?ref=evidence#proof", returnTo),
    "/posts/example/?ref=evidence&return_to=%2Ftrends%2F%3Fwindow%3D7d%26signal%3Drising%26source%3Darxiv%26scenario%3D%25E6%25A8%25A1%25E5%259E%258B%25E7%25A0%2594%25E5%258F%2591%26query%3DAgent%26topic%3Dtag%253ALLM%26view%3Dlist#proof",
  );
  assert.equal(Trends.appendReturnContext("/posts/example/", "https://evil.example/"), "/posts/example/");
});


test("watchlist toggles a normalized topic without changing the existing schema", () => {
  let value = {
    schema_version: 1,
    last_visited_at: null,
    rules: { entities: [], tags: [], sources: [], keywords: [] },
  };
  const store = {
    load: () => structuredClone(value),
    save(next) {
      value = structuredClone(next);
      return structuredClone(value);
    },
  };

  assert.equal(Trends.toggleWatchlistTopic(store, " LLM ").active, true);
  assert.deepEqual(value.rules.tags, ["LLM"]);
  assert.equal(Trends.toggleWatchlistTopic(store, "llm").active, false);
  assert.deepEqual(value.rules.tags, []);
});


test("topic load invalidation aborts and advances the sequence before a cache hit can render", () => {
  let aborts = 0;
  const model = {
    topicController: { abort() { aborts += 1; } },
    topicSequence: 7,
  };

  assert.equal(Trends.invalidateTopicLoad(model), 8);
  assert.equal(aborts, 1);
  assert.equal(model.topicController, null);
  assert.equal(Trends.invalidateTopicLoad(model), 9);
  assert.equal(aborts, 1);
});


test("canvas backing stores reuse unchanged allocations and obey the eight megapixel budget", () => {
  const pixelBudget = 8 * 1024 * 1024;
  const fourKRatio = Trends.resolveCanvasPixelRatio(3840, 2160, 2);
  const eightKRatio = Trends.resolveCanvasPixelRatio(7680, 4320, 2);
  assert.ok(fourKRatio < 2);
  assert.ok(eightKRatio < 1);
  for (const [width, height, ratio] of [
    [3840, 2160, fourKRatio],
    [7680, 4320, eightKRatio],
  ]) {
    assert.ok(width * height * ratio * ratio <= pixelBudget + 2);
  }

  let width = 0;
  let height = 0;
  let allocations = 0;
  const canvas = {};
  Object.defineProperties(canvas, {
    width: { get: () => width, set: (value) => { width = value; allocations += 1; } },
    height: { get: () => height, set: (value) => { height = value; allocations += 1; } },
  });
  const transforms = [];
  const context = { setTransform: (...values) => transforms.push(values) };
  const first = Trends.resizeCanvasBackingStore(canvas, context, 1200, 800, 2);
  const second = Trends.resizeCanvasBackingStore(canvas, context, 1200, 800, 2);

  assert.equal(first.resized, true);
  assert.equal(second.resized, false);
  assert.equal(allocations, 2, "hover redraw must not reallocate an unchanged backing store");
  assert.equal(transforms.length, 2);
});


test("topology matrix is deterministic, bounded and needs no animation frame", () => {
  const values = [
    trend(),
    trend({ id: "tag:agent", topic: "Agent", score: 60, counts: { current: 4, previous: 0, pre_previous: 0 } }),
  ];
  const first = Trends.layoutMatrix(values, 900, 480);
  const second = Trends.layoutMatrix(values, 900, 480);

  assert.deepEqual(first, second);
  assert.equal(first.length, 2);
  assert.equal(first[0].isCenter, true);
  assert.equal(first[0].id, "tag:llm");
  for (const point of first) {
    assert.ok(point.x >= 0 && point.x <= 900);
    assert.ok(point.y >= 0 && point.y <= 480);
    assert.ok(point.anchorX >= 28 && point.anchorX <= 872);
    assert.ok(point.anchorY >= 24 && point.anchorY <= 456);
    assert.ok(point.radius >= 12 && point.radius <= 20);
    assert.ok(point.cellRadiusX >= 43);
    assert.ok(point.cellRadiusY >= 39);
    assert.ok(point.previousX >= 28 && point.previousX <= 872);
    assert.ok(point.previousY >= 24 && point.previousY <= 456);
    assert.ok(Array.isArray(point.facets));
    assert.equal(point.heat.key, Trends.heatTier(point.score));
  }
  assert.equal(Trends.hitTestMatrix(first, first[0].x, first[0].y)?.id, first[0].id);
});


test("topology badge rectangle is part of the node hit target", () => {
  const width = 900;
  const height = 480;
  const [point] = Trends.layoutMatrix([
    trend({ topic: "Amazon Bedrock", score: 73, state: "rising" }),
  ], width, height);
  const badgeHeight = width >= 900 ? 42 : 38;
  const badgeCenterX = point.x;
  const badgeCenterY = Math.max(
    8 + (badgeHeight / 2),
    point.y - point.cellRadiusY - 4 - (badgeHeight / 2),
  );

  const normalizedY = (point.y - badgeCenterY) / point.cellRadiusY;
  assert.ok(
    normalizedY > 1,
    "the probe must be outside the existing organic cell so this specifically covers the badge",
  );
  assert.equal(
    Trends.hitTestMatrix([point], badgeCenterX, badgeCenterY)?.id,
    point.id,
    "hovering or clicking the visible badge must resolve to the same trend node",
  );
});


test("topology normalizes viewport geometry and gives the visually topmost center priority", () => {
  const points = Trends.layoutMatrix([
    trend(),
    trend({ id: "tag:agent", topic: "Agent", score: 60 }),
  ], 899.6, 479.6);
  assert.equal(points[0].viewportWidth, 900);
  assert.equal(points[0].viewportHeight, 480);

  const center = { ...points[0], x: 450, y: 240, cellRadiusX: 90, cellRadiusY: 80 };
  const coveredOuter = { ...points[1], x: 450, y: 240, cellRadiusX: 70, cellRadiusY: 60 };
  assert.equal(
    Trends.hitTestMatrix([center, coveredOuter], 450, 240)?.id,
    center.id,
    "the center is drawn last and must win overlapping node hit tests",
  );
});


test("topology matrix caps the first paint and moves the selected topic into the expanded center", () => {
  const values = Array.from({ length: 18 }, (_, index) => trend({
    id: `tag:t-${index}`,
    topic: `Topic ${index}`,
    score: 100 - index,
  }));
  const points = Trends.layoutMatrix(values, 900, 620, "tag:t-15");

  assert.equal(points.length, 11);
  assert.equal(points[0].id, "tag:t-15");
  assert.equal(points[0].isCenter, true);
  assert.equal(points[0].isSelected, true);
  assert.equal(points[0].totalCount, 18);
  assert.equal(points.filter((point) => point.isCenter).length, 1);
});


test("filtered topology badges retain the full-window rank instead of renumbering", () => {
  const filtered = [trend({ id: "tag:third", topic: "Third", score: 72 })];
  const points = Trends.layoutMatrix(
    filtered,
    900,
    620,
    "",
    new Map([["tag:third", 3]]),
  );

  assert.equal(points.length, 1);
  assert.equal(points[0].rank, 3);
});


test("matrix labels only the strongest eight plus selected and hovered evidence points", () => {
  const points = Array.from({ length: 12 }, (_, index) => ({
    id: `tag:t-${index}`,
    score: 100 - index,
  }));

  assert.deepEqual(
    Trends.labeledPointIds(points, "tag:t-10", "tag:t-11"),
    new Set([
      "tag:t-0", "tag:t-1", "tag:t-2", "tag:t-3",
      "tag:t-4", "tag:t-5", "tag:t-6", "tag:t-7",
      "tag:t-10", "tag:t-11",
    ]),
  );
});


test("topology orbit keeps explicit evidence and growth anchors without pretending they are positions", () => {
  const points = Trends.layoutMatrix([
    trend({ id: "tag:first", topic: "First" }),
    trend({ id: "tag:second", topic: "Second" }),
  ], 700, 360);

  assert.equal(points[0].anchorX, points[1].anchorX);
  assert.equal(points[0].anchorY, points[1].anchorY);
  assert.notDeepEqual(
    [points[0].x, points[0].y],
    [points[1].x, points[1].y],
  );
  assert.equal(points[0].current, 12);
  assert.equal(points[0].previous, 7);
  assert.equal(points[0].growth, points[1].growth);
});


test("annotation lanes keep labels separated without moving data points", () => {
  const points = Array.from({ length: 10 }, (_, index) => ({
    id: `tag:t-${index}`,
    topic: `Topic ${index}`,
    score: 100 - index,
    x: 500 + index,
    y: 120 + index,
    radius: 12,
  }));
  const annotations = Trends.layoutPointLabels(points, "", "", 900, 430);
  const compactAnnotations = Trends.layoutPointLabels(points, "", "", 600, 430, 6);

  assert.equal(annotations.length, 8);
  assert.equal(compactAnnotations.length, 6);
  for (const side of ["left", "right"]) {
    const lane = annotations.filter((item) => item.side === side).sort((a, b) => a.y - b.y);
    for (let index = 1; index < lane.length; index += 1) {
      assert.ok(lane[index].y - lane[index - 1].y >= 18);
    }
  }
  points.forEach((point, index) => {
    assert.equal(point.x, 500 + index);
    assert.equal(point.y, 120 + index);
  });
});


test("maps source machine identifiers to stable user-facing names", () => {
  assert.equal(Trends.formatSourceName("blogs_podcasts"), "博客与播客");
  assert.equal(Trends.formatSourceName("hacker_news"), "Hacker News");
  assert.equal(Trends.formatSourceName("juejin"), "掘金");
  assert.equal(Trends.formatSourceName("arxiv"), "arXiv");
  assert.equal(Trends.formatSourceName("github_trending"), "GitHub Trending");
  assert.equal(Trends.formatSourceName("Custom Source"), "Custom Source");
});


test("strict shard validators reject unknown schemas, unsafe paths and oversized assets", () => {
  const validIndex = {
    schema_version: "stack_trends_index_v1",
    generated_at: "2026-07-16T03:39:14Z",
    data_as_of: "2026-07-16T03:39:14Z",
    realtime: false,
    timezone: "Asia/Shanghai",
    default_window: "30d",
    disclaimer: "基于本站收录证据，不代表全网热度。",
    formula: "transparent formula",
    normalization: {
      quantity_target_unique_events: 10,
      growth_neutral: 0.5,
      acceleration_neutral: 0.5,
      component_range: [0, 1],
      score_range: [0, 100],
    },
    stats: {
      eligible_articles: 1936,
      topic_count: 1,
      source_count: 5,
      windows: {
        "24h": { trend_count: 1, evidence_articles: 3, source_count: 2 },
        "7d": { trend_count: 8, evidence_articles: 24, source_count: 4 },
        "30d": { trend_count: 24, evidence_articles: 153, source_count: 5 },
      },
    },
    windows: {
      "24h": { path: "windows/24h-a.json", bytes: 1200, sha256: "a".repeat(64), trend_count: 1 },
      "7d": { path: "windows/7d-b.json", bytes: 4200, sha256: "b".repeat(64), trend_count: 8 },
      "30d": { path: "windows/30d-c.json", bytes: 8800, sha256: "c".repeat(64), trend_count: 24 },
    },
    topics: {
      "tag:llm": { path: "topics/llm-a1b2c3d4.json", bytes: 4096, sha256: "d".repeat(64) },
    },
  };

  assert.equal(Trends.validateIndex(validIndex).default_window, "30d");
  assert.throws(
    () => Trends.validateIndex({ ...validIndex, windows: { ...validIndex.windows, "30d": { ...validIndex.windows["30d"], path: "../secret.json" } } }),
    /invalid trend data/i,
  );
  assert.throws(
    () => Trends.validateIndex({ ...validIndex, schema_version: "trend_v1" }),
    /invalid trend data/i,
  );
  assert.throws(
    () => Trends.validateIndex({ ...validIndex, topics: {} }),
    /invalid trend data/i,
  );
});


test("v2 validators expose event accounting while retaining the v1 rollout fallback", () => {
  const baseStats = {
    eligible_articles: 4,
    unique_events: 3,
    redundant_observations: 1,
    promoted_same_event_pairs: 1,
    topic_count: 1,
    source_count: 3,
    windows: {
      "24h": { trend_count: 1, evidence_articles: 4, unique_events: 3, redundant_observations: 1, source_count: 3 },
      "7d": { trend_count: 1, evidence_articles: 4, unique_events: 3, redundant_observations: 1, source_count: 3 },
      "30d": { trend_count: 1, evidence_articles: 4, unique_events: 3, redundant_observations: 1, source_count: 3 },
    },
  };
  const index = Trends.validateIndex({
    schema_version: "stack_trends_index_v2",
    generated_at: "2026-07-16T10:00:00Z",
    data_as_of: "2026-07-16T10:00:00Z",
    realtime: false,
    lineage_mode: "lineage_index_v1",
    timezone: "Asia/Shanghai",
    default_window: "30d",
    disclaimer: "基于本站收录证据，不代表全网热度。",
    formula: "transparent formula",
    normalization: {
      quantity_target_unique_events: 10,
      growth_neutral: 0.5,
      acceleration_neutral: 0.5,
      component_range: [0, 1],
      score_range: [0, 100],
    },
    stats: baseStats,
    windows: {
      "24h": { path: "windows/24h-a.json", bytes: 1200, sha256: "a".repeat(64), trend_count: 1 },
      "7d": { path: "windows/7d-b.json", bytes: 1200, sha256: "b".repeat(64), trend_count: 1 },
      "30d": { path: "windows/30d-c.json", bytes: 1200, sha256: "c".repeat(64), trend_count: 1 },
    },
    topics: {
      "tag:llm": { path: "topics/llm-a.json", bytes: 1200, sha256: "d".repeat(64) },
    },
  });
  const value = trend({
    graph_node_id: "tag:llm",
    sparkline: Array(12).fill(1),
    unique_events: 3,
    observations: 4,
    redundant_observations: 1,
    source_diversity: 3,
    detail_path: "topics/llm-a.json",
  });
  const windowData = Trends.validateWindow({
    schema_version: "stack_trends_window_v2",
    window: "30d",
    data_as_of: index.data_as_of,
    minimum_unique_events: 3,
    formula: index.formula,
    sample_notice: null,
    facets: { sources: value.sources, scenarios: value.scenarios },
    trends: [value],
  }, "30d", index);
  const topic = Trends.validateTopic({
    schema_version: "stack_trends_topic_v2",
    id: "tag:llm",
    topic: "LLM",
    graph_node_id: "tag:llm",
    data_as_of: index.data_as_of,
    description: "可审计主题",
    windows: {
      "24h": null,
      "7d": null,
      "30d": {
        score: 82.4,
        state: "rising",
        confidence: "high",
        unique_events: 3,
        observations: 4,
        redundant_observations: 1,
        unique_sources: 3,
        source_diversity: 3,
        counts: { current: 3, previous: 2, pre_previous: 1 },
        sparkline: Array(12).fill(1),
      },
    },
    related_topics: [],
    sources: value.sources,
    scenarios: value.scenarios,
    categories: [{ name: "模型", count: 3 }],
    evidence: [{
      id: `evt_${"1".repeat(64)}`,
      observation_id: `obs_${"1".repeat(64)}`,
      title: "代表报道",
      summary: "代表摘要",
      source: "arxiv",
      published_at: "2026-07-16T09:00:00Z",
      internal_url: "/posts/original/",
      relation: "original",
      associated_observations: 2,
      related_reports: [{
        observation_id: `obs_${"2".repeat(64)}`,
        title: "转载报道",
        source: "wire",
        published_at: "2026-07-16T09:30:00Z",
        internal_url: "/posts/reprint/",
        relation: "syndicated",
      }],
    }],
  }, "tag:llm", index);

  assert.equal(index.schema_version, "stack_trends_index_v2");
  assert.equal(index.stats.promoted_same_event_pairs, 1);
  assert.equal(windowData.trends[0].redundant_observations, 1);
  assert.equal(topic.evidence[0].associated_observations, 2);
  assert.equal(topic.evidence[0].related_reports[0].relation, "syndicated");
  assert.throws(
    () => Trends.validateWindow({
      ...windowData,
      trends: [{ ...value, redundant_observations: 0 }],
    }, "30d", index),
    /invalid trend data/i,
  );

  const legacyV2Stats = { ...baseStats };
  delete legacyV2Stats.promoted_same_event_pairs;
  const legacyV2Index = Trends.validateIndex({
    schema_version: "stack_trends_index_v2",
    generated_at: "2026-07-16T10:00:00Z",
    data_as_of: "2026-07-16T10:00:00Z",
    realtime: false,
    lineage_mode: "lineage_index_v1",
    timezone: "Asia/Shanghai",
    default_window: "30d",
    disclaimer: "基于本站收录证据，不代表全网热度。",
    formula: "transparent formula",
    normalization: {
      quantity_target_unique_events: 10,
      growth_neutral: 0.5,
      acceleration_neutral: 0.5,
      component_range: [0, 1],
      score_range: [0, 100],
    },
    stats: legacyV2Stats,
    windows: {
      "24h": { path: "windows/24h-a.json", bytes: 1200, sha256: "a".repeat(64), trend_count: 1 },
      "7d": { path: "windows/7d-b.json", bytes: 1200, sha256: "b".repeat(64), trend_count: 1 },
      "30d": { path: "windows/30d-c.json", bytes: 1200, sha256: "c".repeat(64), trend_count: 1 },
    },
    topics: {
      "tag:llm": { path: "topics/llm-a.json", bytes: 1200, sha256: "d".repeat(64) },
    },
  });
  assert.equal(legacyV2Index.stats.promoted_same_event_pairs, 0);
  assert.throws(
    () => Trends.validateIndex({
      ...legacyV2Index,
      stats: { ...baseStats, unknown_counter: 1 },
    }),
    /invalid trend data: stats fields/i,
  );
  assert.throws(
    () => Trends.validateIndex({
      ...legacyV2Index,
      stats: { ...baseStats, promoted_same_event_pairs: 2 },
    }),
    /invalid trend data: stats promoted same event accounting/i,
  );
});


test("trend evidence links disclose associated reports and drill into article lineage", () => {
  assert.deepEqual(
    Trends.evidenceAssociationCopy({
      associated_observations: 4,
      internal_url: "/posts/original/",
    }, "/archive/"),
    {
      count: 3,
      label: "另有 3 条关联报道",
      href: "/archive/posts/original/#intelligence-lineage",
    },
  );
  assert.equal(
    Trends.evidenceAssociationCopy({ associated_observations: 1, internal_url: "/posts/one/" }),
    null,
  );
});
