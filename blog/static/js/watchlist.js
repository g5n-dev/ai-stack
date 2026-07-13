(function watchlistModule(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.AIStackWatchlist = Object.freeze(api);
  }
}(typeof globalThis !== "undefined" ? globalThis : this, function createWatchlistApi() {
  "use strict";

  const SCHEMA_VERSION = 1;
  const STORAGE_KEY = "ai-stack.watchlist.v1";
  const MAX_IMPORT_BYTES = 1024 * 1024;
  const MAX_RULES_PER_KIND = 1000;
  const MAX_RULE_LENGTH = 200;
  const RULE_KINDS = Object.freeze(["entities", "tags", "sources", "keywords"]);
  const TOP_LEVEL_FIELDS = new Set(["schema_version", "last_visited_at", "rules"]);
  const RULE_FIELDS = new Set(RULE_KINDS);
  const FORBIDDEN_OBJECT_KEYS = new Set(["__proto__", "constructor", "prototype"]);
  const SOURCE_PATTERN = /^[a-z0-9][a-z0-9._-]{0,127}$/;
  const ISO_TIMESTAMP_PATTERN = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[+-]\d{2}:\d{2})$/iu;
  const SCOPE_NOTICE = "关注规则与上次访问时间只保存在当前浏览器，不会跨设备同步；内容按页面标注的数据截止时间更新。";

  class WatchlistValidationError extends Error {
    constructor(message) {
      super(message);
      this.name = "WatchlistValidationError";
    }
  }

  function isPlainObject(value) {
    if (value === null || typeof value !== "object" || Array.isArray(value)) {
      return false;
    }
    const prototype = Object.getPrototypeOf(value);
    return prototype === Object.prototype || prototype === null;
  }

  function assertAllowedFields(value, allowedFields, context) {
    for (const key of Object.keys(value)) {
      if (FORBIDDEN_OBJECT_KEYS.has(key) || !allowedFields.has(key)) {
        throw new WatchlistValidationError(`${context} contains an unsupported field`);
      }
    }
  }

  function normalizeRule(value, kind) {
    if (typeof value !== "string") {
      throw new WatchlistValidationError(`${kind} entries must be strings`);
    }
    const normalized = value.normalize("NFKC").trim().toLowerCase();
    if (!normalized || normalized.length > MAX_RULE_LENGTH) {
      throw new WatchlistValidationError(`${kind} entries must contain 1-${MAX_RULE_LENGTH} characters`);
    }
    if (/[\u0000-\u001f\u007f<>]/u.test(normalized)) {
      throw new WatchlistValidationError(`${kind} entries contain unsafe characters`);
    }
    if (kind === "sources" && !SOURCE_PATTERN.test(normalized)) {
      throw new WatchlistValidationError("source entries must be safe source identifiers");
    }
    return normalized;
  }

  function normalizeRules(value) {
    if (!isPlainObject(value)) {
      throw new WatchlistValidationError("rules must be an object");
    }
    assertAllowedFields(value, RULE_FIELDS, "rules");

    const result = {};
    for (const kind of RULE_KINDS) {
      const entries = value[kind];
      if (!Array.isArray(entries)) {
        throw new WatchlistValidationError(`${kind} must be an array`);
      }
      if (entries.length > MAX_RULES_PER_KIND) {
        throw new WatchlistValidationError(`${kind} exceeds ${MAX_RULES_PER_KIND} rules`);
      }
      const unique = new Set(entries.map((entry) => normalizeRule(entry, kind)));
      result[kind] = Array.from(unique).sort();
    }
    return result;
  }

  function normalizeLastVisited(value) {
    if (value === undefined || value === null) {
      return null;
    }
    if (
      typeof value !== "string"
      || value.length > 64
      || !ISO_TIMESTAMP_PATTERN.test(value)
    ) {
      throw new WatchlistValidationError("last_visited_at must be an ISO-8601 string or null");
    }
    const timestamp = Date.parse(value);
    if (!Number.isFinite(timestamp)) {
      throw new WatchlistValidationError("last_visited_at must be a valid ISO-8601 timestamp");
    }
    return new Date(timestamp).toISOString();
  }

  function normalizeWatchlist(value) {
    if (!isPlainObject(value)) {
      throw new WatchlistValidationError("watchlist must be an object");
    }
    assertAllowedFields(value, TOP_LEVEL_FIELDS, "watchlist");
    if (value.schema_version !== SCHEMA_VERSION) {
      throw new WatchlistValidationError(`schema_version must be ${SCHEMA_VERSION}`);
    }
    return {
      schema_version: SCHEMA_VERSION,
      last_visited_at: normalizeLastVisited(value.last_visited_at),
      rules: normalizeRules(value.rules),
    };
  }

  function emptyWatchlist() {
    return {
      schema_version: SCHEMA_VERSION,
      last_visited_at: null,
      rules: {
        entities: [],
        tags: [],
        sources: [],
        keywords: [],
      },
    };
  }

  function byteLength(value) {
    if (typeof TextEncoder === "function") {
      return new TextEncoder().encode(value).byteLength;
    }
    return unescape(encodeURIComponent(value)).length;
  }

  function importWatchlist(serialized) {
    if (typeof serialized !== "string") {
      throw new WatchlistValidationError("import must be a JSON string");
    }
    if (byteLength(serialized) > MAX_IMPORT_BYTES) {
      throw new WatchlistValidationError("watchlist import exceeds 1 MiB");
    }

    let parsed;
    try {
      parsed = JSON.parse(serialized);
    } catch (error) {
      throw new WatchlistValidationError("watchlist import is not valid JSON");
    }
    return normalizeWatchlist(parsed);
  }

  function exportWatchlist(value) {
    return JSON.stringify(normalizeWatchlist(value));
  }

  function assertStorage(storage) {
    if (
      !storage
      || typeof storage.getItem !== "function"
      || typeof storage.setItem !== "function"
      || typeof storage.removeItem !== "function"
    ) {
      throw new WatchlistValidationError("a localStorage-compatible object is required");
    }
  }

  function createStore(storage, storageKey = STORAGE_KEY) {
    assertStorage(storage);
    if (typeof storageKey !== "string" || !storageKey || storageKey.length > 128) {
      throw new WatchlistValidationError("storage key is invalid");
    }

    function load() {
      const serialized = storage.getItem(storageKey);
      if (serialized === null) {
        return emptyWatchlist();
      }
      try {
        return importWatchlist(serialized);
      } catch (error) {
        if (!(error instanceof WatchlistValidationError)) {
          throw error;
        }
        return emptyWatchlist();
      }
    }

    function save(value) {
      const normalized = normalizeWatchlist(value);
      storage.setItem(storageKey, JSON.stringify(normalized));
      return normalized;
    }

    return Object.freeze({
      load,
      save,
      clear() {
        storage.removeItem(storageKey);
      },
      export() {
        return exportWatchlist(load());
      },
      import(serialized) {
        return save(importWatchlist(serialized));
      },
      markVisited(timestamp = new Date().toISOString()) {
        return save({
          ...load(),
          last_visited_at: timestamp,
        });
      },
    });
  }

  function normalizedEventValues(value, kind) {
    if (!Array.isArray(value)) {
      return [];
    }
    const result = [];
    for (const item of value) {
      try {
        result.push(normalizeRule(item, kind));
      } catch (error) {
        if (!(error instanceof WatchlistValidationError)) {
          throw error;
        }
      }
    }
    return result;
  }

  function matches(value, event) {
    const watchlist = normalizeWatchlist(value);
    if (!isPlainObject(event)) {
      return false;
    }

    const eventEntities = new Set(normalizedEventValues(event.entities, "entities"));
    if (watchlist.rules.entities.some((entity) => eventEntities.has(entity))) {
      return true;
    }
    const eventTags = new Set(normalizedEventValues(event.tags, "tags"));
    if (watchlist.rules.tags.some((tag) => eventTags.has(tag))) {
      return true;
    }
    if (typeof event.source === "string") {
      try {
        const source = normalizeRule(event.source, "sources");
        if (watchlist.rules.sources.includes(source)) {
          return true;
        }
      } catch (error) {
        if (!(error instanceof WatchlistValidationError)) {
          throw error;
        }
      }
    }

    const searchableFields = [event.title, event.summary, event.text]
      .filter((field) => typeof field === "string")
      .join(" ")
      .normalize("NFKC")
      .toLowerCase();
    return watchlist.rules.keywords.some((keyword) => searchableFields.includes(keyword));
  }

  return {
    MAX_IMPORT_BYTES,
    SCHEMA_VERSION,
    SCOPE_NOTICE,
    STORAGE_KEY,
    WatchlistValidationError,
    createStore,
    emptyWatchlist,
    exportWatchlist,
    importWatchlist,
    matches,
    normalizeWatchlist,
  };
}));
