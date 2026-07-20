import assert from "node:assert/strict";
import { createRequire } from "node:module";
import test from "node:test";

const require = createRequire(import.meta.url);
const Workbench = require("../../blog/static/js/graph-workbench.js");


test("accepts only bounded graph modes and namespaced node ids", () => {
  assert.deepEqual(
    Workbench.parseGraphRequest("?mode=focus&node=tag%3ALLM"),
    { mode: "focus", node: "tag:LLM" },
  );
  assert.deepEqual(
    Workbench.parseGraphRequest("?mode=community&node=tag%3Aignored"),
    { mode: "community", node: "" },
  );
  for (const query of [
    "?mode=focus&node=javascript%3Aalert(1)",
    "?mode=focus&node=tag%3A%3Cscript%3E",
    `?mode=focus&node=tag%3A${"x".repeat(221)}`,
    "?mode=unknown&node=tag%3ALLM",
  ]) {
    assert.deepEqual(Workbench.parseGraphRequest(query), { mode: "overview", node: "" });
  }
});


test("focuses the requested node exactly once after readiness without preloading focus mode", async () => {
  const order = [];
  let focusCalls = 0;
  let resolveReady;
  const ready = new Promise((resolve) => { resolveReady = resolve; });
  const engine = {
    ready,
    mode: "overview",
    selectedNodeId: "",
    async setMode(mode, options) {
      order.push(["setMode", mode, options]);
    },
    async focusNode(node) {
      focusCalls += 1;
      order.push(["focusNode", node]);
      this.selectedNodeId = node;
    },
  };

  const pending = Workbench.applyGraphRequest(engine, { mode: "focus", node: "tag:LLM" });
  await Promise.resolve();
  assert.deepEqual(order, []);
  resolveReady();
  const result = await pending;

  assert.deepEqual(order, [["focusNode", "tag:LLM"]]);
  assert.equal(focusCalls, 1);
  assert.deepEqual(result, { applied: true, mode: "focus", node: "tag:LLM" });
});


test("falls back to overview when a deep-linked focus node cannot load", async () => {
  const calls = [];
  const engine = {
    ready: Promise.resolve(),
    mode: "overview",
    selectedNodeId: "",
    async setMode(mode) {
      calls.push(mode);
      this.mode = mode;
    },
    async focusNode() {
      calls.push("focusNode");
      throw new Error("missing node");
    },
  };

  const result = await Workbench.applyGraphRequest(engine, { mode: "focus", node: "tag:missing" });

  assert.deepEqual(calls, ["focusNode", "overview"]);
  assert.equal(result.applied, false);
  assert.equal(result.mode, "overview");
  assert.match(result.message, /missing node/);
});


test("detail focus uses the captured node id and produces a reproducible deep link", async () => {
  const calls = [];
  const engine = {
    ready: Promise.resolve(),
    mode: "community",
    async focusNode(nodeId) {
      calls.push(nodeId);
      this.mode = "focus";
      return { id: nodeId };
    },
  };

  const result = await Workbench.focusSelectedNode(engine, "tag:AI Agent");
  assert.deepEqual(calls, ["tag:AI Agent"]);
  assert.equal(result.id, "tag:AI Agent");
  assert.equal(engine.mode, "focus");
  assert.equal(
    Workbench.focusRequestUrl("https://ai-stack.site/archive/scenarios/?return_to=%2Ftrends%2F", "tag:AI Agent"),
    "/archive/scenarios/?return_to=%2Ftrends%2F&mode=focus&node=tag%3AAI+Agent",
  );
});


test("mode links clear stale focus state while preserving unrelated navigation state", () => {
  assert.equal(
    Workbench.modeRequestUrl(
      "https://ai-stack.site/archive/scenarios/?return_to=%2Ftrends%2F&mode=focus&node=tag%3ALLM#map",
      "overview",
    ),
    "/archive/scenarios/?return_to=%2Ftrends%2F#map",
  );
  assert.equal(
    Workbench.modeRequestUrl(
      "https://ai-stack.site/archive/scenarios/?return_to=%2Ftrends%2F&mode=focus&node=tag%3ALLM",
      "community",
    ),
    "/archive/scenarios/?return_to=%2Ftrends%2F&mode=community",
  );
});


test("detail focus rejects unsafe or missing node ids before calling the engine", async () => {
  let calls = 0;
  const engine = {
    ready: Promise.resolve(),
    async focusNode() { calls += 1; },
  };
  for (const nodeId of ["", "javascript:alert(1)", "tag:<script>"]) {
    await assert.rejects(Workbench.focusSelectedNode(engine, nodeId), /node/i);
  }
  assert.equal(calls, 0);
});
