(function searchModule(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
    return;
  }

  root.AIStackSearch = Object.freeze(api);
  if (root.document) {
    const start = () => api.initializeSearchPage(root.document);
    if (root.document.readyState === "loading") {
      root.document.addEventListener("DOMContentLoaded", start, { once: true });
    } else {
      start();
    }
  }
}(typeof globalThis !== "undefined" ? globalThis : this, function createSearchApi() {
  "use strict";

  const CANONICAL_ORIGIN = "https://ai-stack.site";
  const FILTER_KEYS = Object.freeze(["source", "date", "entity", "tag", "scenario"]);
  const MAX_FILTER_VALUE_LENGTH = 200;
  const MAX_RESULTS = 20;
  const MAX_SUGGESTIONS = 100;
  const MAX_CATALOG_RECORDS = 20000;
  const CATALOG_SCHEMA_VERSION = "pagefind_result_catalog_v1";
  const FRAGMENT_ID = /^[a-z0-9][a-z0-9-]{0,15}_[0-9a-f]{7}$/u;
  const SHA256 = /^[0-9a-f]{64}$/u;
  const GIT_SHA = /^(?:[0-9a-f]{40}|[0-9a-f]{64})$/u;

  function catalogFailure(kind) {
    const error = new Error(`catalog ${kind}`);
    error.catalogFailure = kind;
    return error;
  }

  function isPlainObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function hasExactFields(value, fields) {
    const keys = Object.keys(value).sort();
    return keys.length === fields.length
      && keys.every((key, index) => key === fields[index]);
  }

  function canonicalCatalogText(value, maxLength) {
    if (
      typeof value !== "string"
      || value.length === 0
      || Array.from(value).length > maxLength
    ) {
      throw catalogFailure("incomplete");
    }
    const canonical = value
      .normalize("NFKC")
      .replace(/[\p{Cc}\p{Cf}\p{Cs}\p{Co}\p{Cn}]/gu, "")
      .trim()
      .replace(/\s+/gu, " ");
    if (!canonical || canonical !== value) {
      throw catalogFailure("incomplete");
    }
    return canonical;
  }

  function normalizeCatalogRecord(value) {
    const fields = ["date", "source", "summary", "title", "url"];
    if (!isPlainObject(value) || !hasExactFields(value, fields)) {
      throw catalogFailure("incomplete");
    }
    const url = safeResultUrl(value.url);
    if (url === "#") {
      throw catalogFailure("incomplete");
    }
    const date = canonicalCatalogText(value.date, 10);
    if (!/^\d{4}-\d{2}-\d{2}$/u.test(date)) {
      throw catalogFailure("incomplete");
    }
    return Object.freeze({
      url,
      title: canonicalCatalogText(value.title, 300),
      source: canonicalCatalogText(value.source, 200),
      date,
      summary: canonicalCatalogText(value.summary, 120),
    });
  }

  function validateCatalogBasis(value) {
    if (!isPlainObject(value) || !GIT_SHA.test(value.code_sha || "")
      || !GIT_SHA.test(value.content_sha || "")) {
      throw catalogFailure("incomplete");
    }
    if (value.basis_schema_version === "repository_build_basis_v1") {
      if (!hasExactFields(value, ["basis_schema_version", "code_sha", "content_sha"])) {
        throw catalogFailure("incomplete");
      }
      return;
    }
    const releaseFields = [
      "basis_schema_version",
      "code_sha",
      "content_sha",
      "generated_at",
      "release_basis_sha256",
      "release_seq",
      "schema_version",
    ];
    if (
      value.basis_schema_version !== "release_basis_v1"
      || !hasExactFields(value, releaseFields)
      || !SHA256.test(value.release_basis_sha256 || "")
      || !Number.isSafeInteger(value.release_seq)
      || value.release_seq <= 0
      || typeof value.schema_version !== "string"
      || !/^[1-9][0-9]*\.[0-9]+$/u.test(value.schema_version)
      || typeof value.generated_at !== "string"
      || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/u.test(value.generated_at)
    ) {
      throw catalogFailure("incomplete");
    }
  }

  function validateCatalog(value) {
    const fields = [
      "basis",
      "record_count",
      "records",
      "schema_version",
      "source_fragment_tree_sha256",
      "summary_codepoints",
    ];
    if (
      !isPlainObject(value)
      || !hasExactFields(value, fields)
      || value.schema_version !== CATALOG_SCHEMA_VERSION
      || value.summary_codepoints !== 120
      || !SHA256.test(value.source_fragment_tree_sha256 || "")
      || !Number.isSafeInteger(value.record_count)
      || value.record_count <= 0
      || value.record_count > MAX_CATALOG_RECORDS
      || !isPlainObject(value.records)
    ) {
      throw catalogFailure("incomplete");
    }
    validateCatalogBasis(value.basis);
    const identifiers = Object.keys(value.records);
    if (identifiers.length !== value.record_count) {
      throw catalogFailure("incomplete");
    }
    const records = Object.create(null);
    for (const identifier of identifiers) {
      if (!FRAGMENT_ID.test(identifier)) {
        throw catalogFailure("incomplete");
      }
      records[identifier] = normalizeCatalogRecord(value.records[identifier]);
    }
    return Object.freeze({
      records: Object.freeze(records),
      recordCount: value.record_count,
      sourceFragmentTreeSha256: value.source_fragment_tree_sha256,
    });
  }

  function catalogResult(catalog, result) {
    const identifier = result?.id;
    if (
      typeof identifier !== "string"
      || !FRAGMENT_ID.test(identifier)
      || !Object.hasOwn(catalog.records, identifier)
    ) {
      throw catalogFailure("incomplete");
    }
    const record = catalog.records[identifier];
    return {
      url: record.url,
      plain_excerpt: record.summary,
      meta: {
        title: record.title,
        source: record.source,
        date: record.date,
      },
    };
  }

  function normalizeFilterValue(value) {
    if (value === undefined || value === null || value === "") {
      return "";
    }
    if (typeof value !== "string") {
      throw new TypeError("unsafe filter value");
    }
    const normalized = value.normalize("NFKC").trim();
    if (
      normalized.length > MAX_FILTER_VALUE_LENGTH
      || /[\u0000-\u001f\u007f]/u.test(normalized)
    ) {
      throw new TypeError("unsafe filter value");
    }
    return normalized;
  }

  function normalizeFilters(values) {
    const filters = {};
    for (const key of FILTER_KEYS) {
      const normalized = normalizeFilterValue(values?.[key]);
      if (normalized) {
        filters[key] = normalized;
      }
    }
    return filters;
  }

  function rankFilterValues(values, limit = MAX_SUGGESTIONS) {
    if (!values || typeof values !== "object" || Array.isArray(values)) {
      return [];
    }
    return Object.entries(values)
      .filter(([label, count]) => (
        typeof label === "string"
        && label.length > 0
        && Number.isFinite(count)
        && count > 0
      ))
      .sort(([leftLabel, leftCount], [rightLabel, rightCount]) => (
        rightCount - leftCount || leftLabel.localeCompare(rightLabel, "zh-CN")
      ))
      .slice(0, Math.max(0, limit))
      .map(([label]) => label);
  }

  function safeResultUrl(value) {
    if (typeof value !== "string" || value.length > 2048) {
      return "#";
    }
    try {
      const url = new URL(value, CANONICAL_ORIGIN);
      if (url.origin !== CANONICAL_ORIGIN || !["http:", "https:"].includes(url.protocol)) {
        return "#";
      }
      return `${url.pathname}${url.search}${url.hash}`;
    } catch (error) {
      return "#";
    }
  }

  function appendTextElement(document, parent, tagName, className, text) {
    const element = document.createElement(tagName);
    element.className = className;
    element.textContent = typeof text === "string" ? text : "";
    parent.append(element);
    return element;
  }

  function renderResults(document, list, results) {
    const items = [];
    for (const result of results) {
      const item = document.createElement("li");
      item.className = "terminal-glass rounded-xl border border-muted-teal/20 p-5";

      const link = document.createElement("a");
      link.className = "text-off-white text-lg hover:text-primary focus:text-primary";
      link.setAttribute("href", safeResultUrl(result?.url));
      link.textContent = result?.meta?.title || "无标题条目";
      item.append(link);

      const metadata = [result?.meta?.source, result?.meta?.date]
        .filter((value) => typeof value === "string" && value)
        .join(" · ");
      appendTextElement(
        document,
        item,
        "p",
        "mt-2 text-xs font-mono text-muted-teal",
        metadata,
      );
      appendTextElement(
        document,
        item,
        "p",
        "mt-3 text-sm leading-relaxed text-off-white/65",
        typeof result?.plain_excerpt === "string" ? result.plain_excerpt.slice(0, 600) : "",
      );
      items.push(item);
    }
    list.replaceChildren(...items);
  }

  async function executeSearch(pagefind, rawQuery, rawFilters) {
    const query = typeof rawQuery === "string" ? rawQuery.normalize("NFKC").trim() : "";
    const filters = normalizeFilters(rawFilters);
    if (!query && Object.keys(filters).length === 0) {
      return { results: [], idle: true };
    }
    return pagefind.search(query || null, { filters });
  }

  function populateSelect(document, select, values) {
    const placeholder = select.children?.[0] || null;
    const options = rankFilterValues(values, Number.MAX_SAFE_INTEGER).map((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      return option;
    });
    select.replaceChildren(...(placeholder ? [placeholder, ...options] : options));
  }

  function populateDataList(document, dataList, values) {
    const options = rankFilterValues(values).map((value) => {
      const option = document.createElement("option");
      option.value = value;
      return option;
    });
    dataList.replaceChildren(...options);
  }

  function getFormValues(form) {
    const values = {};
    for (const key of FILTER_KEYS) {
      values[key] = form.elements.namedItem(key)?.value || "";
    }
    return values;
  }

  function defaultPagefindLoader() {
    return import("/pagefind/pagefind.js");
  }

  async function defaultCatalogLoader() {
    let response;
    try {
      response = await fetch("/pagefind/catalog.json", {
        cache: "force-cache",
        credentials: "same-origin",
      });
      if (!response.ok) {
        throw catalogFailure("load");
      }
      return await response.json();
    } catch (error) {
      if (error?.catalogFailure) {
        throw error;
      }
      throw catalogFailure("load");
    }
  }

  function initializeSearchPage(
    document,
    loadPagefind = defaultPagefindLoader,
    loadCatalog = defaultCatalogLoader,
  ) {
    const form = document.getElementById("search-form");
    if (!form) {
      return null;
    }
    const query = document.getElementById("search-query");
    const status = document.getElementById("search-status");
    const results = document.getElementById("search-results");
    const submit = document.getElementById("search-submit");
    const source = document.getElementById("search-source");
    const suggestionLists = {
      entity: document.getElementById("search-entities"),
      tag: document.getElementById("search-tags"),
      scenario: document.getElementById("search-scenarios"),
    };

    let pagefindPromise;
    let catalogPromise;
    let filtersPromise;
    let filtersLoaded = false;
    let searchSequence = 0;

    async function getPagefind() {
      if (!pagefindPromise) {
        pagefindPromise = Promise.resolve(loadPagefind()).then(async (pagefind) => {
          await pagefind.init();
          return pagefind;
        });
      }
      return pagefindPromise;
    }

    async function getCatalog() {
      if (!catalogPromise) {
        catalogPromise = Promise.resolve(loadCatalog())
          .then(validateCatalog)
          .catch((error) => {
            catalogPromise = undefined;
            if (error?.catalogFailure) {
              throw error;
            }
            throw catalogFailure("load");
          });
      }
      return catalogPromise;
    }

    async function loadFilters() {
      if (filtersLoaded) {
        return;
      }
      if (!filtersPromise) {
        filtersPromise = (async () => {
          const pagefind = await getPagefind();
          const filters = await pagefind.filters();
          if (source) {
            populateSelect(document, source, filters.source);
          }
          for (const [key, dataList] of Object.entries(suggestionLists)) {
            if (dataList) {
              populateDataList(document, dataList, filters[key]);
            }
          }
          filtersLoaded = true;
        })().catch((error) => {
          filtersPromise = undefined;
          throw error;
        });
      }
      try {
        await filtersPromise;
      } finally {
        if (filtersLoaded) {
          filtersPromise = undefined;
        }
      }
    }

    async function runSearch() {
      const sequence = ++searchSequence;
      status.textContent = "正在检索静态索引…";
      form.setAttribute("aria-busy", "true");
      submit.disabled = true;
      try {
        const pagefind = await getPagefind();
        const search = await executeSearch(pagefind, query.value, getFormValues(form));
        if (sequence !== searchSequence) {
          return;
        }
        if (search.idle) {
          results.replaceChildren();
          status.textContent = "输入关键词或至少选择一个过滤条件。";
          return;
        }
        const catalog = search.results.length > 0 ? await getCatalog() : null;
        const visibleResults = search.results
          .slice(0, MAX_RESULTS)
          .map((result) => catalogResult(catalog, result));
        if (sequence !== searchSequence) {
          return;
        }
        renderResults(document, results, visibleResults);
        status.textContent = search.results.length === 0
          ? "没有匹配条目。"
          : `找到 ${search.results.length} 条，当前显示 ${visibleResults.length} 条。`;
      } catch (error) {
        if (sequence === searchSequence) {
          results.replaceChildren();
          if (error?.catalogFailure === "load") {
            status.textContent = "检索结果目录加载失败，请稍后重试。";
          } else if (error?.catalogFailure === "incomplete") {
            status.textContent = "检索结果目录不完整，请稍后重试。";
          } else {
            status.textContent = "检索暂时不可用，请稍后重试。";
          }
        }
      } finally {
        if (sequence === searchSequence) {
          form.removeAttribute("aria-busy");
          submit.disabled = false;
        }
      }
    }

    query.addEventListener("focus", () => {
      loadFilters().catch(() => {
        status.textContent = "过滤条件加载失败，仍可使用关键词检索。";
      });
    }, { once: true });
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      runSearch();
    });
    form.addEventListener("reset", () => {
      searchSequence += 1;
      globalThis.setTimeout(() => {
        results.replaceChildren();
        status.textContent = "输入关键词或至少选择一个过滤条件。";
        query.focus();
      }, 0);
    });

    return Object.freeze({ getCatalog, getPagefind, loadFilters, runSearch });
  }

  return {
    FILTER_KEYS,
    MAX_RESULTS,
    executeSearch,
    initializeSearchPage,
    normalizeFilters,
    rankFilterValues,
    renderResults,
    safeResultUrl,
    validateCatalog,
  };
}));
