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


function resultCatalog(records) {
  return {
    schema_version: "pagefind_result_catalog_v1",
    summary_codepoints: 120,
    record_count: Object.keys(records).length,
    source_fragment_tree_sha256: "a".repeat(64),
    basis: {
      basis_schema_version: "repository_build_basis_v1",
      code_sha: "b".repeat(40),
      content_sha: "c".repeat(40),
    },
    records,
  };
}


function catalogRecord(index) {
  return {
    url: `/result-${index}/`,
    summary: `excerpt ${index}`,
    title: `Result ${index}`,
    source: "arxiv",
    date: "2026-07-13",
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
  let catalogCalls = 0;
  let fragmentDataCalls = 0;
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
          id: `zh-cn_${index.toString(16).padStart(7, "0")}`,
          async data() {
            fragmentDataCalls += 1;
            throw new Error("the compact catalog must replace fragment downloads");
          },
        })),
      };
    },
  };
  const records = Object.fromEntries(
    Array.from({ length: 25 }, (_, index) => [
      `zh-cn_${index.toString(16).padStart(7, "0")}`,
      catalogRecord(index),
    ]),
  );

  const controller = Search.initializeSearchPage(
    document,
    async () => pagefind,
    async () => {
      catalogCalls += 1;
      return resultCatalog(records);
    },
  );
  await Promise.all([controller.loadFilters(), controller.loadFilters()]);
  await controller.runSearch();

  assert.equal(initializeCalls, 1);
  assert.equal(filterCalls, 1);
  assert.equal(catalogCalls, 1);
  assert.equal(fragmentDataCalls, 0);
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


test("fails closed when the result catalog is unavailable and retries on the next search", async () => {
  const document = fakeSearchDocument();
  document.ids["search-query"].value = "retry";
  const pagefind = {
    async init() {},
    async search() {
      return { results: [{ id: "zh-cn_123abcd" }] };
    },
  };
  let catalogCalls = 0;
  const controller = Search.initializeSearchPage(
    document,
    async () => pagefind,
    async () => {
      catalogCalls += 1;
      if (catalogCalls === 1) {
        throw new Error("catalog unavailable");
      }
      return resultCatalog({ "zh-cn_123abcd": catalogRecord(1) });
    },
  );

  await controller.runSearch();
  assert.equal(document.ids["search-results"].children.length, 0);
  assert.equal(document.ids["search-status"].textContent, "检索结果目录加载失败，请稍后重试。");

  await controller.runSearch();
  assert.equal(catalogCalls, 2);
  assert.equal(document.ids["search-results"].children.length, 1);
  assert.equal(document.ids["search-results"].children[0].children[0].textContent, "Result 1");
});


test("rejects incomplete or malformed catalog records instead of downloading fragments", async () => {
  const document = fakeSearchDocument();
  document.ids["search-query"].value = "missing";
  let fragmentDataCalls = 0;
  const pagefind = {
    async init() {},
    async search() {
      return {
        results: [{
          id: "zh-cn_123abcd",
          async data() {
            fragmentDataCalls += 1;
          },
        }],
      };
    },
  };
  const controller = Search.initializeSearchPage(
    document,
    async () => pagefind,
    async () => resultCatalog({}),
  );

  await controller.runSearch();

  assert.equal(fragmentDataCalls, 0);
  assert.equal(document.ids["search-results"].children.length, 0);
  assert.equal(document.ids["search-status"].textContent, "检索结果目录不完整，请稍后重试。");
});


test("validates catalog text limits by Unicode code point rather than UTF-16 unit", () => {
  const summary = "🚀".repeat(120);
  const value = resultCatalog({
    "zh-cn_123abcd": { ...catalogRecord(1), summary },
  });

  const catalog = Search.validateCatalog(value);

  assert.equal(catalog.records["zh-cn_123abcd"].summary, summary);
  assert.equal(Array.from(summary).length, 120);
  assert.equal(summary.length, 240);
});


test("normalizes a same-origin Unicode catalog URL without rejecting it", () => {
  const value = resultCatalog({
    "zh-cn_123abcd": { ...catalogRecord(1), url: "/posts/中文路径/" },
  });

  const catalog = Search.validateCatalog(value);

  assert.equal(
    catalog.records["zh-cn_123abcd"].url,
    "/posts/%E4%B8%AD%E6%96%87%E8%B7%AF%E5%BE%84/",
  );
});


test("a late search cannot overwrite the newest catalog-backed result", async () => {
  const document = fakeSearchDocument();
  let releaseFirst;
  let markFirstStarted;
  const firstStarted = new Promise((resolve) => {
    markFirstStarted = resolve;
  });
  const firstResponse = new Promise((resolve) => {
    releaseFirst = resolve;
  });
  let catalogCalls = 0;
  const pagefind = {
    async init() {},
    async search(query) {
      if (query === "first") {
        markFirstStarted();
        return firstResponse;
      }
      return { results: [{ id: "zh-cn_2222222" }] };
    },
  };
  const controller = Search.initializeSearchPage(
    document,
    async () => pagefind,
    async () => {
      catalogCalls += 1;
      return resultCatalog({
        "zh-cn_1111111": { ...catalogRecord(1), title: "Old result" },
        "zh-cn_2222222": { ...catalogRecord(2), title: "Newest result" },
      });
    },
  );

  document.ids["search-query"].value = "first";
  const oldSearch = controller.runSearch();
  await firstStarted;
  document.ids["search-query"].value = "second";
  await controller.runSearch();
  releaseFirst({ results: [{ id: "zh-cn_1111111" }] });
  await oldSearch;

  assert.equal(catalogCalls, 1);
  assert.equal(document.ids["search-results"].children.length, 1);
  assert.equal(
    document.ids["search-results"].children[0].children[0].textContent,
    "Newest result",
  );
  assert.equal(document.ids["search-status"].textContent, "找到 1 条，当前显示 1 条。");
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
