import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { createRequire } from "node:module";
import test from "node:test";

const require = createRequire(import.meta.url);
const Lineage = require("../../blog/static/js/lineage.js");

const OBSERVATION_ID = `obs_${"12345678"}${"a".repeat(56)}`;
const REPRINT_ID = `obs_${"92345678"}${"b".repeat(56)}`;
const EVENT_ID = `evt_${"12345678"}${"c".repeat(56)}`;

function jsonBytes(value) {
  return new TextEncoder().encode(`${JSON.stringify(value)}\n`);
}

function reference(kind, bucket, value) {
  const bytes = jsonBytes(value);
  const sha256 = createHash("sha256").update(bytes).digest("hex");
  return {
    bytes,
    ref: {
      bucket,
      path: `${kind}/${bucket}-${sha256.slice(0, 16)}.json`,
      sha256,
      bytes: bytes.byteLength,
    },
  };
}

function fixture() {
  const routeBucket = Lineage.bucketKeyForId(OBSERVATION_ID);
  const clusterBucket = Lineage.bucketKeyForId(EVENT_ID);
  const routes = {
    version: 1,
    bucket: routeBucket,
    routes: [
      { observation_id: OBSERVATION_ID, event_id: EVENT_ID },
      { observation_id: REPRINT_ID, event_id: EVENT_ID },
    ],
  };
  const clusters = {
    version: 1,
    bucket: clusterBucket,
    clusters: [{
      event_id: EVENT_ID,
      event_aliases: [],
      earliest_observed_id: OBSERVATION_ID,
      lineage_links: [],
      probable_origin_id: OBSERVATION_ID,
      representative_article_url: "/posts/original/",
      observations: [
        {
          observation_id: REPRINT_ID,
          title: "转载报道",
          source: "wire",
          source_url: "https://wire.example/reprint",
          article_url: "/posts/reprint/",
          relation: "syndicated",
          parent_observation_id: OBSERVATION_ID,
          source_published_at: "2026-07-16T09:30:00Z",
          first_seen_at: "2026-07-16T09:31:00Z",
          timestamp_confidence: "feed",
        },
        {
          observation_id: OBSERVATION_ID,
          title: "首发报道",
          source: "publisher",
          source_url: "https://source.example/launch",
          article_url: "/posts/original/",
          relation: "original",
          parent_observation_id: null,
          source_published_at: "2026-07-16T08:00:00Z",
          first_seen_at: "2026-07-16T08:03:00Z",
          timestamp_confidence: "publisher",
        },
      ],
    }],
  };
  const route = reference("routes", routeBucket, routes);
  const cluster = reference("clusters", clusterBucket, clusters);
  const index = {
    version: 1,
    schema: "lineage_index_v1",
    generated_at: "2026-07-16T10:00:00Z",
    bucket_count: 128,
    bucket_algorithm: "sha256_prefix32_mod_v1",
    stats: {
      observations: 2,
      events: 1,
      exact_copies: 0,
      syndicated: 1,
      derivatives: 0,
      same_event: 0,
      related_only: 0,
    },
    route_buckets: [route.ref],
    cluster_buckets: [cluster.ref],
  };
  const root = "https://ai-stack.site/archive/data/lineage/";
  const responses = new Map([
    [`${root}index.json`, jsonBytes(index)],
    [`${root}${route.ref.path}`, route.bytes],
    [`${root}${cluster.ref.path}`, cluster.bytes],
  ]);
  return { index, responses };
}

function response(bytes) {
  return {
    ok: true,
    status: 200,
    async arrayBuffer() {
      return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
    },
  };
}

test("bucket mapping follows the public sha256 prefix contract", () => {
  assert.equal(Lineage.bucketForId(OBSERVATION_ID), 0x12345678 % 128);
  assert.equal(Lineage.bucketForId(EVENT_ID), 0x12345678 % 128);
  assert.throws(() => Lineage.bucketForId("javascript:boom"), /lineage/i);
});

test("article lineage loads exactly index, route and cluster with verified hashes", async () => {
  const { responses } = fixture();
  const requests = [];
  const result = await Lineage.loadLineage({
    indexUrl: "/archive/data/lineage/index.json",
    observationId: OBSERVATION_ID,
    baseUrl: "https://ai-stack.site/posts/current/",
    fetchFn: async (url) => {
      requests.push(String(url));
      const bytes = responses.get(String(url));
      return bytes ? response(bytes) : { ok: false, status: 404 };
    },
  });

  assert.equal(requests.length, 3);
  assert.deepEqual(requests, [
    "https://ai-stack.site/archive/data/lineage/index.json",
    requests[1],
    requests[2],
  ]);
  assert.match(requests[1], /\/routes\//u);
  assert.match(requests[2], /\/clusters\//u);
  assert.equal(result.event_id, EVENT_ID);
  assert.equal(result.current.observation_id, OBSERVATION_ID);
  assert.equal(result.timeline[0].relation, "original");
  assert.equal(result.timeline[1].relation, "syndicated");
  assert.equal(result.summary.source_count, 2);
  assert.equal(result.summary.observation_count, 2);
  assert.equal(result.timeline[0].article_url, "/archive/posts/original/");
});

test("lineage loader fails closed on tampered shards and unsafe public URLs", async () => {
  const tampered = fixture();
  const routeUrl = [...tampered.responses.keys()].find((url) => url.includes("/routes/"));
  tampered.responses.set(routeUrl, jsonBytes({ version: 1, bucket: "00", routes: [] }));
  await assert.rejects(
    Lineage.loadLineage({
      indexUrl: "/archive/data/lineage/index.json",
      observationId: OBSERVATION_ID,
      baseUrl: "https://ai-stack.site/posts/current/",
      fetchFn: async (url) => response(tampered.responses.get(String(url))),
    }),
    /integrity/i,
  );

  const unsafe = fixture();
  const clusterUrl = [...unsafe.responses.keys()].find((url) => url.includes("/clusters/"));
  const payload = JSON.parse(new TextDecoder().decode(unsafe.responses.get(clusterUrl)));
  payload.clusters[0].observations[0].source_url = "javascript:alert(1)";
  const bytes = jsonBytes(payload);
  unsafe.responses.set(clusterUrl, bytes);
  const indexUrl = "https://ai-stack.site/archive/data/lineage/index.json";
  const index = JSON.parse(new TextDecoder().decode(unsafe.responses.get(indexUrl)));
  index.cluster_buckets[0].sha256 = createHash("sha256").update(bytes).digest("hex");
  index.cluster_buckets[0].bytes = bytes.byteLength;
  unsafe.responses.set(indexUrl, jsonBytes(index));
  await assert.rejects(
    Lineage.loadLineage({
      indexUrl,
      observationId: OBSERVATION_ID,
      baseUrl: "https://ai-stack.site/posts/current/",
      fetchFn: async (url) => response(unsafe.responses.get(String(url))),
    }),
    /source url/i,
  );
});

test("lineage loader rejects secret-bearing source URL query keys", async () => {
  for (const query of [
    "token=secret",
    "sk=secret",
    "session=secret",
    "X-Amz-Credential=secret",
    "X-Amz-Signature=secret",
    "jwtToken=secret",
    "sessionId=secret",
    "accessToken=secret",
    "authToken=secret",
    "AWSAccessKeyId=secret",
    "signedUrl=secret",
    "jwt-Token=secret",
    "signed.URL=secret",
  ]) {
    const unsafe = fixture();
    const clusterUrl = [...unsafe.responses.keys()].find((url) => url.includes("/clusters/"));
    const payload = JSON.parse(new TextDecoder().decode(unsafe.responses.get(clusterUrl)));
    payload.clusters[0].observations[0].source_url = `https://source.example/story?${query}`;
    const bytes = jsonBytes(payload);
    unsafe.responses.set(clusterUrl, bytes);
    const indexUrl = "https://ai-stack.site/archive/data/lineage/index.json";
    const index = JSON.parse(new TextDecoder().decode(unsafe.responses.get(indexUrl)));
    index.cluster_buckets[0].sha256 = createHash("sha256").update(bytes).digest("hex");
    index.cluster_buckets[0].bytes = bytes.byteLength;
    unsafe.responses.set(indexUrl, jsonBytes(index));

    await assert.rejects(
      Lineage.loadLineage({
        indexUrl,
        observationId: OBSERVATION_ID,
        baseUrl: "https://ai-stack.site/posts/current/",
        fetchFn: async (url) => response(unsafe.responses.get(String(url))),
      }),
      /source url/i,
    );
  }
});

test("lineage loader preserves ordinary source URL query keys", async () => {
  const safe = fixture();
  const clusterUrl = [...safe.responses.keys()].find((url) => url.includes("/clusters/"));
  const payload = JSON.parse(new TextDecoder().decode(safe.responses.get(clusterUrl)));
  const sourceUrl = "https://source.example/story?id=42&post=agent&v=3&langVersion=zh-CN";
  payload.clusters[0].observations.find(
    (item) => item.observation_id === OBSERVATION_ID,
  ).source_url = sourceUrl;
  const bytes = jsonBytes(payload);
  safe.responses.set(clusterUrl, bytes);
  const indexUrl = "https://ai-stack.site/archive/data/lineage/index.json";
  const index = JSON.parse(new TextDecoder().decode(safe.responses.get(indexUrl)));
  index.cluster_buckets[0].sha256 = createHash("sha256").update(bytes).digest("hex");
  index.cluster_buckets[0].bytes = bytes.byteLength;
  safe.responses.set(indexUrl, jsonBytes(index));

  const result = await Lineage.loadLineage({
    indexUrl,
    observationId: OBSERVATION_ID,
    baseUrl: "https://ai-stack.site/posts/current/",
    fetchFn: async (url) => response(safe.responses.get(String(url))),
  });
  assert.equal(result.current.source_url, sourceUrl);
});

test("derivative projection exposes a bounded cross-event parent preview", () => {
  const current = {
    observation_id: OBSERVATION_ID,
    title: "衍生解读",
    source: "analysis",
    source_url: "https://analysis.example/story",
    article_url: "/posts/analysis/",
    relation: "derivative",
    parent_observation_id: REPRINT_ID,
    source_published_at: "2026-07-16T10:00:00Z",
    first_seen_at: "2026-07-16T10:01:00Z",
    timestamp_confidence: "publisher",
  };
  const parent = {
    ...current,
    observation_id: REPRINT_ID,
    title: "首发来源",
    source: "publisher",
    source_url: "https://publisher.example/story",
    article_url: "/posts/original/",
    relation: "original",
    parent_observation_id: null,
    source_published_at: "2026-07-16T08:00:00Z",
    first_seen_at: "2026-07-16T08:01:00Z",
  };
  const projected = Lineage.projectCluster({
    event_id: EVENT_ID,
    event_aliases: [],
    earliest_observed_id: OBSERVATION_ID,
    probable_origin_id: OBSERVATION_ID,
    representative_article_url: "/posts/analysis/",
    observations: [current],
    lineage_links: [{
      from_observation_id: OBSERVATION_ID,
      relation: "derivative",
      target: parent,
    }],
  }, OBSERVATION_ID);

  assert.equal(projected.timeline.length, 1);
  assert.equal(projected.lineage_links.length, 1);
  assert.equal(projected.lineage_links[0].target.observation_id, REPRINT_ID);
});
