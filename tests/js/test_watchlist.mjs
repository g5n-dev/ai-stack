import assert from "node:assert/strict";
import { createRequire } from "node:module";
import test from "node:test";

const require = createRequire(import.meta.url);
const Watchlist = require("../../blog/static/js/watchlist.js");


class MemoryStorage {
  constructor() {
    this.values = new Map();
  }

  getItem(key) {
    return this.values.has(key) ? this.values.get(key) : null;
  }

  setItem(key, value) {
    this.values.set(key, String(value));
  }

  removeItem(key) {
    this.values.delete(key);
  }
}


test("normalizes, deduplicates and byte-stably exports schema v1", () => {
  const first = Watchlist.exportWatchlist({
    schema_version: 1,
    last_visited_at: "2026-07-13T12:00:00Z",
    rules: {
      tags: [" Agent ", "agent", "协议"],
      entities: ["entity-openai"],
      sources: ["github"],
      keywords: ["Context Protocol"],
    },
  });
  const second = Watchlist.exportWatchlist({
    rules: {
      keywords: ["context protocol"],
      sources: ["github"],
      entities: ["entity-openai"],
      tags: ["协议", "AGENT"],
    },
    last_visited_at: "2026-07-13T12:00:00+00:00",
    schema_version: 1,
  });

  assert.equal(first, second);
  assert.deepEqual(JSON.parse(first), {
    schema_version: 1,
    last_visited_at: "2026-07-13T12:00:00.000Z",
    rules: {
      entities: ["entity-openai"],
      tags: ["agent", "协议"],
      sources: ["github"],
      keywords: ["context protocol"],
    },
  });
});


test("rejects imports larger than one MiB before parsing", () => {
  const oversized = `{"schema_version":1,"padding":"${"x".repeat(1024 * 1024)}"}`;

  assert.throws(
    () => Watchlist.importWatchlist(oversized),
    /1 MiB/,
  );
});


test("rejects prototype pollution, unknown fields and markup-like values", () => {
  const attacks = [
    '{"schema_version":1,"rules":{"entities":[],"tags":[],"sources":[],"keywords":[],"__proto__":{"polluted":true}}}',
    '{"schema_version":1,"rules":{"entities":[],"tags":[],"sources":[],"keywords":[]},"constructor":{}}',
    '{"schema_version":1,"rules":{"entities":[],"tags":["<img src=x onerror=alert(1)>"],"sources":[],"keywords":[]}}',
    '{"schema_version":1,"rules":{"entities":[],"tags":[],"sources":["javascript:alert(1)"],"keywords":[]}}',
  ];

  for (const attack of attacks) {
    assert.throws(() => Watchlist.importWatchlist(attack), Watchlist.WatchlistValidationError);
  }
  assert.equal({}.polluted, undefined);
});


test("rejects invalid versions, invalid dates, excessive rules and non-objects", () => {
  const invalidPayloads = [
    "null",
    "[]",
    '{"schema_version":2,"rules":{"entities":[],"tags":[],"sources":[],"keywords":[]}}',
    '{"schema_version":1,"last_visited_at":"yesterday","rules":{"entities":[],"tags":[],"sources":[],"keywords":[]}}',
    '{"schema_version":1,"last_visited_at":"2026-07-13","rules":{"entities":[],"tags":[],"sources":[],"keywords":[]}}',
    JSON.stringify({
      schema_version: 1,
      rules: {
        entities: Array.from({ length: 1001 }, (_, index) => `entity-${index}`),
        tags: [],
        sources: [],
        keywords: [],
      },
    }),
  ];

  for (const payload of invalidPayloads) {
    assert.throws(() => Watchlist.importWatchlist(payload), Watchlist.WatchlistValidationError);
  }
});


test("local store persists, visits, exports and safely imports", () => {
  const storage = new MemoryStorage();
  const store = Watchlist.createStore(storage);
  const saved = store.save({
    schema_version: 1,
    last_visited_at: null,
    rules: {
      entities: ["entity-openai"],
      tags: ["agents"],
      sources: ["github"],
      keywords: ["context"],
    },
  });

  assert.deepEqual(store.load(), saved);
  const visited = store.markVisited("2026-07-13T12:00:00Z");
  assert.equal(visited.last_visited_at, "2026-07-13T12:00:00.000Z");
  assert.deepEqual(store.import(store.export()), visited);
  store.clear();
  assert.deepEqual(store.load(), Watchlist.emptyWatchlist());
});


test("matches entity, tag, source or keyword without rendering input", () => {
  const watchlist = Watchlist.importWatchlist(JSON.stringify({
    schema_version: 1,
    last_visited_at: "2026-07-13T00:00:00Z",
    rules: {
      entities: ["entity-openai"],
      tags: ["agent"],
      sources: ["arxiv"],
      keywords: ["context protocol"],
    },
  }));

  assert.equal(Watchlist.matches(watchlist, { entities: ["entity-openai"] }), true);
  assert.equal(Watchlist.matches(watchlist, { tags: ["Agent"] }), true);
  assert.equal(Watchlist.matches(watchlist, { source: "arxiv" }), true);
  assert.equal(Watchlist.matches(watchlist, { title: "A Context Protocol guide" }), true);
  assert.equal(Watchlist.matches(watchlist, { title: "Unrelated item" }), false);
});


test("documents local-only and data-cutoff semantics without realtime claims", () => {
  assert.match(Watchlist.SCOPE_NOTICE, /当前浏览器/);
  assert.match(Watchlist.SCOPE_NOTICE, /不会跨设备同步/);
  assert.doesNotMatch(Watchlist.SCOPE_NOTICE, /实时/);
});
