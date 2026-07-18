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
  const FRAGMENT_ID = /^[a-z0-9][a-z0-9-]{0,15}_[0-9a-f]{7,40}$/u;
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
      item.className = "search-result terminal-glass rounded-xl border border-muted-teal/20 p-5";

      const link = document.createElement("a");
      link.className = "search-result__title text-sm";
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
        "search-result__meta text-xs",
        metadata,
      );
      appendTextElement(
        document,
        item,
        "p",
        "search-result__excerpt text-sm",
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

  function createSearchPicker(document, control, source, windowObject = globalThis) {
    const isSelect = control?.tagName === "SELECT";
    const host = control?.closest?.(isSelect ? "[data-search-select]" : "[data-search-autocomplete]");
    if (!host || host.dataset.enhanced === "true" || !document.body || !source) return null;

    const originalList = isSelect ? "" : control.getAttribute("list") || "";
    const originalAutocomplete = isSelect ? null : control.getAttribute("autocomplete");
    const originalHidden = control.hidden;
    const originalTabIndex = control.getAttribute("tabindex");
    const label = document.querySelector?.(`label[for="${control.id}"]`);
    const trigger = isSelect ? document.createElement("button") : control;
    const valueNode = isSelect ? document.createElement("span") : null;
    const list = document.createElement("div");
    const listId = `${control.id}-listbox`;
    let activeIndex = 0;
    let timer = 0;
    let compositionRefreshTimer = 0;
    let composing = false;
    let destroyed = false;
    let suppressAutoOpen = false;
    const listenerCleanups = [];

    function listen(target, type, handler, options) {
      if (typeof target?.addEventListener !== "function") return;
      target.addEventListener(type, handler, options);
      listenerCleanups.push(() => target.removeEventListener(type, handler, options));
    }

    if (isSelect) {
      trigger.type = "button";
      trigger.className = "search-control search-select__trigger";
      valueNode.className = "search-select__value";
      trigger.append(valueNode);
      host.append(trigger);
      control.hidden = true;
      control.tabIndex = -1;
      control.setAttribute("aria-hidden", "true");
    } else {
      control.removeAttribute("list");
      control.setAttribute("autocomplete", "off");
    }

    trigger.id = isSelect ? `${control.id}-trigger` : control.id;
    trigger.setAttribute("role", "combobox");
    trigger.setAttribute("aria-haspopup", "listbox");
    trigger.setAttribute("aria-expanded", "false");
    trigger.setAttribute("aria-controls", listId);
    trigger.setAttribute("aria-autocomplete", isSelect ? "none" : "list");
    trigger.setAttribute(
      "aria-labelledby",
      label?.id ? (isSelect ? `${label.id} ${trigger.id}` : label.id) : trigger.id,
    );

    list.id = listId;
    list.className = isSelect
      ? "search-picker__list search-select__list"
      : "search-picker__list search-autocomplete__list";
    list.setAttribute("role", "listbox");
    list.setAttribute("aria-labelledby", label?.id || trigger.id);
    list.hidden = true;
    document.body.append(list);
    host.dataset.enhanced = "true";
    host.dataset.open = "false";

    function allItems() {
      if (isSelect) {
        return Array.from(control.options || []).map((option) => ({
          label: String(option.textContent || "").trim(),
          value: option.value,
          selected: option.value === control.value,
        }));
      }
      const query = String(control.value || "").normalize("NFKC").trim().toLocaleLowerCase("zh-CN");
      return Array.from(source.children || [])
        .map((option) => String(option.value || option.textContent || "").trim())
        .filter((value, index, values) => value && values.indexOf(value) === index)
        .filter((value) => !query || value.normalize("NFKC").toLocaleLowerCase("zh-CN").includes(query))
        .slice(0, 20)
        .map((value) => ({ label: value, value, selected: value === control.value }));
    }

    function optionNodes() {
      return Array.from(list.querySelectorAll('[role="option"]'));
    }

    function positionList() {
      if (list.hidden) return;
      const rect = trigger.getBoundingClientRect();
      const visualViewport = windowObject.visualViewport;
      const viewportWidth = Math.max(1, visualViewport?.width || windowObject.innerWidth || document.documentElement.clientWidth || 0);
      const viewportHeight = Math.max(1, visualViewport?.height || windowObject.innerHeight || document.documentElement.clientHeight || 0);
      const viewportLeft = Math.max(0, visualViewport?.offsetLeft || 0);
      const viewportTop = Math.max(0, visualViewport?.offsetTop || 0);
      const width = Math.max(1, Math.min(Math.max(180, rect.width), Math.max(1, viewportWidth - 16)));
      const left = Math.max(viewportLeft + 8, Math.min(viewportLeft + viewportWidth - width - 8, rect.left));
      list.style.width = `${Math.round(width)}px`;
      list.style.left = `${Math.round(left)}px`;
      const menuHeight = Math.min(286, list.scrollHeight || 0, Math.max(1, viewportHeight - 16));
      list.style.maxHeight = `${Math.max(1, Math.round(menuHeight))}px`;
      const viewportBottom = viewportTop + viewportHeight;
      const below = viewportBottom - rect.bottom - 8;
      const above = rect.top - viewportTop - 8;
      const openAbove = below < Math.min(menuHeight, 220) && above > below;
      const top = openAbove ? rect.top - menuHeight - 6 : rect.bottom + 6;
      list.style.top = `${Math.max(viewportTop + 8, Math.min(viewportBottom - menuHeight - 8, Math.round(top)))}px`;
    }

    function setActive(index) {
      const nodes = optionNodes();
      if (!nodes.length) return;
      activeIndex = Math.max(0, Math.min(nodes.length - 1, index));
      nodes.forEach((node, position) => { node.dataset.active = String(position === activeIndex); });
      trigger.setAttribute("aria-activedescendant", nodes[activeIndex].id);
      nodes[activeIndex].scrollIntoView?.({ block: "nearest" });
    }

    function render() {
      if (destroyed) return;
      const items = allItems();
      list.replaceChildren();
      items.forEach((item, index) => {
        const option = document.createElement("button");
        option.id = `${listId}-option-${index}`;
        option.type = "button";
        option.tabIndex = -1;
        option.dataset.value = item.value;
        option.setAttribute("role", "option");
        option.setAttribute("aria-selected", String(item.selected));
        option.textContent = item.label;
        list.append(option);
      });
      if (isSelect) {
        const selected = items.find((item) => item.selected) || items[0];
        valueNode.textContent = selected?.label || "请选择";
        activeIndex = Math.max(0, items.findIndex((item) => item.selected));
      } else {
        activeIndex = Math.min(activeIndex, Math.max(0, items.length - 1));
      }
      if (!list.hidden) {
        if (!items.length) close(false);
        else {
          setActive(activeIndex);
          schedulePosition();
        }
      } else if (!isSelect && !suppressAutoOpen && document.activeElement === control && items.length) {
        open();
      }
    }

    function close(focus = false) {
      if (destroyed || list.hidden) return;
      list.hidden = true;
      host.dataset.open = "false";
      trigger.setAttribute("aria-expanded", "false");
      trigger.removeAttribute("aria-activedescendant");
      if (focus) trigger.focus();
    }

    function open() {
      if (destroyed) return;
      const items = allItems();
      if (!items.length) return;
      if (list.hidden) {
        list.hidden = false;
        host.dataset.open = "true";
        trigger.setAttribute("aria-expanded", "true");
      }
      render();
      positionList();
    }

    function choose(index) {
      const node = optionNodes()[index];
      if (!node) return;
      const changed = control.value !== node.dataset.value;
      control.value = node.dataset.value;
      if (isSelect) render();
      close(true);
      if (changed) {
        const EventConstructor = windowObject.Event || globalThis.Event;
        suppressAutoOpen = true;
        try {
          control.dispatchEvent(new EventConstructor(isSelect ? "change" : "input", { bubbles: true }));
        } finally {
          suppressAutoOpen = false;
        }
      }
    }

    function schedulePosition(event) {
      if (event?.type === "scroll" && list.contains(event.target)) return;
      windowObject.clearTimeout(timer);
      timer = windowObject.setTimeout(positionList, 16);
    }

    function onKeydown(event) {
      if (!isSelect && (composing || event.isComposing || event.keyCode === 229)) return;
      const nodes = optionNodes();
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        const wasHidden = list.hidden;
        if (wasHidden) open();
        const available = optionNodes();
        if (available.length) {
          const next = wasHidden && !isSelect
            ? (event.key === "ArrowDown" ? 0 : available.length - 1)
            : (activeIndex + (event.key === "ArrowDown" ? 1 : -1) + available.length) % available.length;
          setActive(next);
        }
      } else if (event.key === "Home" || event.key === "End") {
        if (list.hidden) return;
        event.preventDefault();
        setActive(event.key === "Home" ? 0 : nodes.length - 1);
      } else if (event.key === "Enter" || (isSelect && event.key === " ")) {
        if (list.hidden) {
          if (isSelect) {
            event.preventDefault();
            open();
          }
          return;
        }
        event.preventDefault();
        choose(activeIndex);
      } else if (event.key === "Escape") {
        if (!list.hidden) {
          event.preventDefault();
          event.stopPropagation();
          close(true);
        }
      } else if (event.key === "Tab") {
        close(false);
      }
    }

    function onListClick(event) {
      const option = event.target.closest?.('[role="option"]');
      if (option && list.contains(option)) choose(optionNodes().indexOf(option));
    }
    function onDocumentPointerDown(event) {
      if (!host.contains(event.target) && !list.contains(event.target)) close(false);
    }

    function onTriggerClick() {
      if (isSelect) {
        if (list.hidden) open();
        else close(false);
        return;
      }
      open();
    }

    function onListPointerDown(event) {
      if (event.pointerType === "mouse") event.preventDefault();
    }

    function onInput(event) {
      if (composing || event.isComposing) {
        close(false);
        return;
      }
      windowObject.clearTimeout(compositionRefreshTimer);
      render();
    }

    function onCompositionStart() {
      windowObject.clearTimeout(compositionRefreshTimer);
      composing = true;
      close(false);
    }

    function onCompositionEnd() {
      composing = false;
      compositionRefreshTimer = windowObject.setTimeout(render, 0);
    }

    function onLabelClick(event) {
      if (!isSelect) return;
      event.preventDefault();
      trigger.focus();
    }

    listen(trigger, "keydown", onKeydown);
    listen(trigger, "click", onTriggerClick);
    if (!isSelect) {
      listen(trigger, "focus", open);
      listen(trigger, "input", onInput);
      listen(trigger, "compositionstart", onCompositionStart);
      listen(trigger, "compositionend", onCompositionEnd);
    } else {
      listen(control, "change", render);
      listen(label, "click", onLabelClick);
    }
    listen(list, "click", onListClick);
    listen(list, "pointerdown", onListPointerDown);
    listen(document, "pointerdown", onDocumentPointerDown);
    listen(windowObject, "resize", schedulePosition);
    listen(windowObject, "scroll", schedulePosition, true);
    listen(windowObject.visualViewport, "resize", schedulePosition);
    listen(windowObject.visualViewport, "scroll", schedulePosition);
    render();

    return Object.freeze({
      trigger,
      close,
      refresh: render,
      destroy() {
        if (destroyed) return;
        destroyed = true;
        windowObject.clearTimeout(timer);
        windowObject.clearTimeout(compositionRefreshTimer);
        listenerCleanups.splice(0).forEach((cleanup) => cleanup());
        list.remove();
        trigger.removeAttribute("role");
        trigger.removeAttribute("aria-haspopup");
        trigger.removeAttribute("aria-expanded");
        trigger.removeAttribute("aria-controls");
        trigger.removeAttribute("aria-autocomplete");
        trigger.removeAttribute("aria-labelledby");
        if (isSelect) {
          trigger.remove();
          control.hidden = originalHidden;
          if (originalTabIndex === null) control.removeAttribute("tabindex");
          else control.setAttribute("tabindex", originalTabIndex);
          control.removeAttribute("aria-hidden");
        } else {
          if (originalList) control.setAttribute("list", originalList);
          if (originalAutocomplete === null) control.removeAttribute("autocomplete");
          else control.setAttribute("autocomplete", originalAutocomplete);
        }
        host.removeAttribute("data-enhanced");
        host.removeAttribute("data-open");
      },
    });
  }

  function createSearchSelect(document, select, windowObject = globalThis) {
    return createSearchPicker(document, select, select, windowObject);
  }

  function createSearchAutocomplete(document, input, windowObject = globalThis) {
    const listId = input?.getAttribute?.("list");
    const dataList = listId ? document.getElementById(listId) : null;
    return createSearchPicker(document, input, dataList, windowObject);
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

  async function defaultCatalogLoader({ refresh = false } = {}) {
    let response;
    try {
      response = await fetch("/pagefind/catalog.json", {
        cache: refresh ? "reload" : "no-cache",
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
    const windowObject = document.defaultView || globalThis;
    const sourceMenu = createSearchSelect(document, source, windowObject);
    const suggestionLists = {
      entity: document.getElementById("search-entities"),
      tag: document.getElementById("search-tags"),
      scenario: document.getElementById("search-scenarios"),
    };
    const autocompleteInputs = ["search-entity", "search-tag", "search-scenario"]
      .map((id) => document.getElementById(id))
      .filter(Boolean);
    const autocompleteMenus = autocompleteInputs
      .map((input) => createSearchAutocomplete(document, input, windowObject))
      .filter(Boolean);
    const listenerCleanups = [];

    let pagefindPromise;
    let catalogPromise;
    let filtersPromise;
    let filtersLoaded = false;
    let searchSequence = 0;
    let resetTimer = 0;
    let destroyed = false;

    function listen(target, type, handler, options) {
      if (typeof target?.addEventListener !== "function") return;
      target.addEventListener(type, handler, options);
      listenerCleanups.push(() => target.removeEventListener(type, handler, options));
    }

    async function getPagefind() {
      if (!pagefindPromise) {
        pagefindPromise = Promise.resolve(loadPagefind()).then(async (pagefind) => {
          await pagefind.init();
          return pagefind;
        });
      }
      return pagefindPromise;
    }

    async function getCatalog({ refresh = false } = {}) {
      if (refresh) {
        catalogPromise = undefined;
      }
      if (!catalogPromise) {
        catalogPromise = Promise.resolve(loadCatalog({ refresh }))
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

    async function mapCatalogResults(searchResults) {
      for (let attempt = 0; attempt < 2; attempt += 1) {
        try {
          const catalog = await getCatalog({ refresh: attempt === 1 });
          return searchResults.map((result) => catalogResult(catalog, result));
        } catch (error) {
          if (attempt === 0 && error?.catalogFailure === "incomplete") {
            continue;
          }
          throw error;
        }
      }
      throw catalogFailure("incomplete");
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
            sourceMenu?.refresh();
          }
          for (const [key, dataList] of Object.entries(suggestionLists)) {
            if (dataList) {
              populateDataList(document, dataList, filters[key]);
            }
          }
          autocompleteMenus.forEach((menu) => menu.refresh());
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
        const visibleResults = search.results.length > 0
          ? await mapCatalogResults(search.results.slice(0, MAX_RESULTS))
          : [];
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

    const preloadFilters = () => (
      loadFilters().catch(() => {
        status.textContent = "过滤条件加载失败，仍可使用关键词检索。";
      })
    );
    const preloadControls = [query, sourceMenu?.trigger || source, ...autocompleteInputs]
      .filter(Boolean);
    preloadControls.forEach((control) => {
      listen(control, "focus", preloadFilters);
      listen(control, "pointerdown", preloadFilters, { passive: true });
    });
    listen(form, "submit", (event) => {
      event.preventDefault();
      runSearch();
    });
    listen(form, "reset", () => {
      searchSequence += 1;
      windowObject.clearTimeout(resetTimer);
      resetTimer = windowObject.setTimeout(() => {
        if (destroyed) return;
        results.replaceChildren();
        status.textContent = "输入关键词或至少选择一个过滤条件。";
        sourceMenu?.refresh();
        autocompleteMenus.forEach((menu) => menu.refresh());
        query.focus();
      }, 0);
    });

    return Object.freeze({
      getCatalog,
      getPagefind,
      loadFilters,
      runSearch,
      destroy() {
        if (destroyed) return;
        destroyed = true;
        searchSequence += 1;
        windowObject.clearTimeout(resetTimer);
        listenerCleanups.splice(0).forEach((cleanup) => cleanup());
        sourceMenu?.destroy();
        autocompleteMenus.forEach((menu) => menu.destroy());
      },
    });
  }

  return {
    FILTER_KEYS,
    MAX_RESULTS,
    createSearchAutocomplete,
    createSearchSelect,
    executeSearch,
    initializeSearchPage,
    normalizeFilters,
    rankFilterValues,
    renderResults,
    safeResultUrl,
    validateCatalog,
  };
}));
