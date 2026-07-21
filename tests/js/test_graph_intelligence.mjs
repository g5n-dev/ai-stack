import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { createRequire } from "node:module";
import test from "node:test";

const require = createRequire(import.meta.url);
const Intelligence = require("../../blog/static/js/graph-intelligence.js");

function bytes(value) {
  return new TextEncoder().encode(`${JSON.stringify(value)}\n`);
}

function response(body) {
  return {
    ok: true,
    status: 200,
    async arrayBuffer() {
      return body.buffer.slice(body.byteOffset, body.byteOffset + body.byteLength);
    },
  };
}

test("graph detail loads at most six safe article links from a v2 topic shard", async () => {
  const evidence = Array.from({ length: 8 }, (_, index) => ({
    id: `evt_${String(index).padStart(64, "0")}`,
    observation_id: `obs_${String(index).padStart(64, "0")}`,
    title: `Evidence ${index}`,
    summary: "Verified summary",
    source: "publisher",
    published_at: "2026-07-20T00:00:00Z",
    internal_url: `/posts/evidence-${index}/`,
    relation: index ? "syndicated" : "original",
    associated_observations: index ? 2 : 1,
    related_reports: index ? [{
      observation_id: `obs_${String(index + 20).padStart(64, "0")}`,
      title: "Related",
      source: "wire",
      internal_url: "/posts/related/",
      relation: "syndicated",
      published_at: "2026-07-20T00:01:00Z",
    }] : [],
  }));
  const topic = {
    schema_version: "stack_trends_topic_v2",
    id: "tag:LLM",
    topic: "LLM",
    graph_node_id: "tag:LLM",
    data_as_of: "2026-07-20T00:00:00Z",
    description: "LLM evidence",
    windows: { "24h": null, "7d": null, "30d": null },
    related_topics: [], sources: [], scenarios: [], categories: [], evidence,
  };
  const topicBytes = bytes(topic);
  const digest = createHash("sha256").update(topicBytes).digest("hex");
  const index = {
    schema_version: "stack_trends_index_v2",
    topics: {
      "tag:LLM": {
        path: `topics/llm-${digest.slice(0, 12)}.json`,
        sha256: digest,
        bytes: topicBytes.byteLength,
      },
    },
  };
  const indexBytes = bytes(index);
  const root = "https://ai-stack.site/archive/data/stack-trends/";
  const requests = [];
  const result = await Intelligence.loadNodeIntelligence({
    indexUrl: `${root}index.json`,
    nodeId: "tag:LLM",
    baseUrl: "https://ai-stack.site/archive/scenarios/",
    fetchFn: async (url) => {
      requests.push(String(url));
      return response(String(url).endsWith("index.json") ? indexBytes : topicBytes);
    },
  });

  assert.equal(requests.length, 2);
  assert.equal(result.articles.length, 6);
  assert.equal(result.articles[0].article_url, "/archive/posts/evidence-0/");
  assert.equal(result.articles[1].lineage_url, "/archive/posts/evidence-1/#intelligence-lineage");
  assert.equal(result.trend_url, "/archive/trends/?window=30d&topic=tag%3ALLM");
});

test("graph intelligence accepts v1 fallback and fails closed on tampering", async () => {
  const topic = {
    schema_version: "stack_trends_topic_v1",
    id: "tag:LLM",
    topic: "LLM",
    graph_node_id: "tag:LLM",
    evidence: [{
      id: "evt-legacy", title: "Legacy", summary: "", source: "feed",
      published_at: "2026-07-20T00:00:00Z", internal_url: "/posts/legacy/",
    }],
  };
  const topicBytes = bytes(topic);
  const digest = createHash("sha256").update(topicBytes).digest("hex");
  const indexBytes = bytes({
    schema_version: "stack_trends_index_v1",
    topics: { "tag:LLM": { path: "topics/llm.json", sha256: digest, bytes: topicBytes.byteLength } },
  });
  const fetchFn = async (url) => response(String(url).endsWith("index.json") ? indexBytes : topicBytes);
  const result = await Intelligence.loadNodeIntelligence({
    indexUrl: "/data/stack-trends/index.json", nodeId: "tag:LLM",
    baseUrl: "https://ai-stack.site/scenarios/", fetchFn,
  });
  assert.equal(result.articles[0].role, "original");

  const corrupted = new Uint8Array(topicBytes);
  corrupted[0] ^= 1;
  await assert.rejects(Intelligence.loadNodeIntelligence({
    indexUrl: "/data/stack-trends/index.json", nodeId: "tag:LLM",
    baseUrl: "https://ai-stack.site/scenarios/",
    fetchFn: async (url) => response(String(url).endsWith("index.json") ? indexBytes : corrupted),
  }), /integrity/i);
});
