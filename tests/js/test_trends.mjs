import assert from "node:assert/strict";
import { createRequire } from "node:module";
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
    unique_sources: 3,
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
    "?window=7d&signal=rising&source=arXiv&scenario=%E6%A8%A1%E5%9E%8B%E7%A0%94%E5%8F%91&topic=tag%3Allm&view=list&ignored=boom",
  );

  assert.deepEqual(state, {
    window: "7d",
    signal: "rising",
    source: "arXiv",
    scenario: "模型研发",
    query: "",
    topic: "tag:llm",
    view: "list",
  });
  assert.equal(
    Trends.serializeState(state),
    "?window=7d&signal=rising&source=arXiv&scenario=%E6%A8%A1%E5%9E%8B%E7%A0%94%E5%8F%91&topic=tag%3Allm&view=list",
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
  }
  assert.equal(Trends.hitTestMatrix(first, first[0].x, first[0].y)?.id, first[0].id);
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
