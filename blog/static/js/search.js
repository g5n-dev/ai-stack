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

  function initializeSearchPage(document, loadPagefind = defaultPagefindLoader) {
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
        const visibleResults = await Promise.all(
          search.results.slice(0, MAX_RESULTS).map((result) => result.data()),
        );
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
          status.textContent = "检索暂时不可用，请稍后重试。";
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

    return Object.freeze({ getPagefind, loadFilters, runSearch });
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
  };
}));
