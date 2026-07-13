import assert from "node:assert/strict";
import { createRequire } from "node:module";
import test from "node:test";

const require = createRequire(import.meta.url);
const Search = require("../../blog/static/js/search.js");


class FakeElement {
  constructor(tagName = "div") {
    this.tagName = tagName.toUpperCase();
    this.attributes = new Map();
    this.children = [];
    this.dataset = {};
    this.hidden = false;
    this.listeners = new Map();
    this.textContent = "";
    this.value = "";
  }

  append(...children) {
    this.children.push(...children);
  }

  replaceChildren(...children) {
    this.children = [...children];
  }

  setAttribute(name, value) {
    this.attributes.set(name, String(value));
  }

  getAttribute(name) {
    return this.attributes.get(name) ?? null;
  }

  removeAttribute(name) {
    this.attributes.delete(name);
  }

  addEventListener(name, listener) {
    const listeners = this.listeners.get(name) ?? [];
    listeners.push(listener);
    this.listeners.set(name, listeners);
  }

  async dispatch(name, event = {}) {
    for (const listener of this.listeners.get(name) ?? []) {
      await listener(event);
    }
  }

  focus() {
    this.focused = true;
  }
}


function fakeDocument() {
  return {
    createElement(tagName) {
      return new FakeElement(tagName);
    },
    getElementById() {
      return null;
    },
  };
}


function fakeSearchDocument() {
  const ids = Object.fromEntries([
    "search-form",
    "search-query",
    "search-status",
    "search-results",
    "search-submit",
    "search-source",
    "search-date",
    "search-entity",
    "search-tag",
    "search-scenario",
    "search-entities",
    "search-tags",
    "search-scenarios",
  ].map((id) => [id, new FakeElement(id === "search-source" ? "select" : "div")]));
  const fields = {
    source: ids["search-source"],
    date: ids["search-date"],
    entity: ids["search-entity"],
    tag: ids["search-tag"],
    scenario: ids["search-scenario"],
  };
  ids["search-source"].append(new FakeElement("option"));
  ids["search-form"].elements = {
    namedItem(name) {
      return fields[name] ?? null;
    },
  };
  return {
    ...fakeDocument(),
    ids,
    getElementById(id) {
      return ids[id] ?? null;
    },
  };
}


test("normalizes exact Pagefind filters and drops empty values", () => {
  const filters = Search.normalizeFilters({
    source: " arxiv ",
    date: "2026-07-13",
    entity: " entity-openai ",
    tag: " 智能体 ",
    scenario: " RAG应用 ",
    ignored: "must-not-cross-the-boundary",
  });

  assert.deepEqual(filters, {
    source: "arxiv",
    date: "2026-07-13",
    entity: "entity-openai",
    tag: "智能体",
    scenario: "RAG应用",
  });
  assert.deepEqual(Search.normalizeFilters({ source: "  " }), {});
});


test("rejects control characters and overlong filter values", () => {
  assert.throws(
    () => Search.normalizeFilters({ tag: "safe\u0000unsafe" }),
    /unsafe filter value/,
  );
  assert.throws(
    () => Search.normalizeFilters({ tag: "x".repeat(201) }),
    /unsafe filter value/,
  );
  assert.deepEqual(Search.normalizeFilters(null), {});
});


test("orders filter suggestions by count then label without mutating input", () => {
  const values = { Zebra: 2, Alpha: 2, Popular: 9, Empty: 0 };

  assert.deepEqual(Search.rankFilterValues(values, 3), ["Popular", "Alpha", "Zebra"]);
  assert.deepEqual(values, { Zebra: 2, Alpha: 2, Popular: 9, Empty: 0 });
  assert.deepEqual(Search.rankFilterValues(null), []);
  assert.deepEqual(Search.rankFilterValues(["not", "a", "map"]), []);
});


test("renders result fields as text nodes and never trusts raw Pagefind metadata", () => {
  const document = fakeDocument();
  const list = new FakeElement("ol");
  const malicious = {
    url: "javascript:alert(1)",
    plain_excerpt: "<img src=x onerror=alert(1)>",
    meta: {
      title: "<script>alert(1)</script>",
      source: "arxiv",
      date: "2026-07-13",
    },
  };

  Search.renderResults(document, list, [malicious]);

  assert.equal(list.children.length, 1);
  const item = list.children[0];
  const link = item.children[0];
  const excerpt = item.children[2];
  assert.equal(link.textContent, "<script>alert(1)</script>");
  assert.equal(link.getAttribute("href"), "#");
  assert.equal(excerpt.textContent, "<img src=x onerror=alert(1)>");
  assert.equal(item.children.some((child) => child.tagName === "SCRIPT"), false);
});


test("keeps same-origin and site-relative result URLs", () => {
  assert.equal(Search.safeResultUrl("/2026/07/post/"), "/2026/07/post/");
  assert.equal(Search.safeResultUrl("https://ai-stack.site/2026/07/post/"), "/2026/07/post/");
  assert.equal(Search.safeResultUrl("https://evil.example/post/"), "#");
  assert.equal(Search.safeResultUrl("data:text/html,boom"), "#");
  assert.equal(Search.safeResultUrl(null), "#");
  assert.equal(Search.safeResultUrl("https://[invalid"), "#");
});


test("builds filter-only searches with null query and deterministic filter options", async () => {
  const calls = [];
  const pagefind = {
    async init() {},
    async search(query, options) {
      calls.push({ query, options });
      return { results: [] };
    },
  };

  const outcome = await Search.executeSearch(pagefind, "   ", { source: "arxiv" });

  assert.deepEqual(calls, [{ query: null, options: { filters: { source: "arxiv" } } }]);
  assert.deepEqual(outcome, { results: [] });
});


test("skips an unfiltered empty search so the browser does not load thousands of records", async () => {
  let called = false;
  const pagefind = {
    async search() {
      called = true;
      return { results: [] };
    },
  };

  const outcome = await Search.executeSearch(pagefind, "", {});

  assert.equal(called, false);
  assert.deepEqual(outcome, { results: [], idle: true });
});


test("initializes Pagefind once, populates safe facets and renders a bounded result page", async () => {
  const document = fakeSearchDocument();
  document.ids["search-query"].value = "VideoGPA";
  document.ids["search-source"].value = "arxiv";
  let initializeCalls = 0;
  let filterCalls = 0;
  const pagefind = {
    async init() {
      initializeCalls += 1;
    },
    async filters() {
      filterCalls += 1;
      return {
        source: { arxiv: 20, github: 10 },
        entity: { "entity-openai": 5 },
        tag: { 智能体: 8 },
        scenario: { RAG应用: 3 },
      };
    },
    async search(query, options) {
      assert.equal(query, "VideoGPA");
      assert.deepEqual(options, { filters: { source: "arxiv" } });
      return {
        results: Array.from({ length: 25 }, (_, index) => ({
          async data() {
            return {
              url: `/result-${index}/`,
              plain_excerpt: `excerpt ${index}`,
              meta: { title: `Result ${index}`, source: "arxiv", date: "2026-07-13" },
            };
          },
        })),
      };
    },
  };

  const controller = Search.initializeSearchPage(document, async () => pagefind);
  await Promise.all([controller.loadFilters(), controller.loadFilters()]);
  await controller.runSearch();

  assert.equal(initializeCalls, 1);
  assert.equal(filterCalls, 1);
  assert.equal(document.ids["search-source"].children.length, 3);
  assert.equal(document.ids["search-entities"].children[0].value, "entity-openai");
  assert.equal(document.ids["search-tags"].children[0].value, "智能体");
  assert.equal(document.ids["search-scenarios"].children[0].value, "RAG应用");
  assert.equal(document.ids["search-results"].children.length, Search.MAX_RESULTS);
  assert.equal(document.ids["search-status"].textContent, "找到 25 条，当前显示 20 条。");
  assert.equal(document.ids["search-form"].getAttribute("aria-busy"), null);
  assert.equal(document.ids["search-submit"].disabled, false);
});


test("fails closed with an accessible status when the index cannot initialize", async () => {
  const document = fakeSearchDocument();
  document.ids["search-query"].value = "unavailable";
  const controller = Search.initializeSearchPage(document, async () => {
    throw new Error("index unavailable");
  });

  await controller.runSearch();

  assert.equal(document.ids["search-results"].children.length, 0);
  assert.equal(document.ids["search-status"].textContent, "检索暂时不可用，请稍后重试。");
  assert.equal(document.ids["search-submit"].disabled, false);
});


test("returns null off the search page and keeps an idle page empty", async () => {
  assert.equal(Search.initializeSearchPage(fakeDocument()), null);
  const document = fakeSearchDocument();
  const pagefind = {
    async init() {},
    async search() {
      throw new Error("an idle search must not reach Pagefind");
    },
  };
  const controller = Search.initializeSearchPage(document, async () => pagefind);

  await controller.runSearch();

  assert.equal(document.ids["search-results"].children.length, 0);
  assert.equal(
    document.ids["search-status"].textContent,
    "输入关键词或至少选择一个过滤条件。",
  );
});


test("allows a failed facet preload to be retried without poisoning keyword search", async () => {
  const document = fakeSearchDocument();
  let filterCalls = 0;
  const pagefind = {
    async init() {},
    async filters() {
      filterCalls += 1;
      if (filterCalls === 1) {
        throw new Error("transient facet failure");
      }
      return {};
    },
    async search() {
      return { results: [] };
    },
  };
  const controller = Search.initializeSearchPage(document, async () => pagefind);

  await assert.rejects(controller.loadFilters(), /transient facet failure/);
  await controller.loadFilters();
  document.ids["search-query"].value = "missing";
  await controller.runSearch();

  assert.equal(filterCalls, 2);
  assert.equal(document.ids["search-status"].textContent, "没有匹配条目。");
});
