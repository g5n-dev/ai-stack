import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

const require = createRequire(import.meta.url);
const terminalCommands = require(path.resolve(
  import.meta.dirname,
  "../../blog/static/js/terminal.js",
));
const terminalSource = readFileSync(path.resolve(
  import.meta.dirname,
  "../../blog/static/js/terminal.js",
), "utf8");

test("command parsing is Unicode-normalized and case-insensitive", () => {
  const parsed = terminalCommands.resolveCommand("  ＳＥＡＲＣＨ   AI Agent  ");

  assert.equal(parsed.command, "search");
  assert.equal(parsed.args, "AI Agent");
  assert.equal(parsed.exact, true);
});

test("Chinese IME fragmented Latin commands recover without changing their arguments", () => {
  assert.deepEqual(terminalCommands.resolveCommand("l s"), {
    command: "ls",
    args: "",
    exact: true,
    suggestion: terminalCommands.commands.find((item) => item.id === "ls"),
  });
  assert.deepEqual(terminalCommands.resolveCommand("s e a r c h AI Agent"), {
    command: "search",
    args: "AI Agent",
    exact: true,
    suggestion: terminalCommands.commands.find((item) => item.id === "search"),
  });
});

test("Chinese aliases resolve to the same canonical commands", () => {
  assert.equal(terminalCommands.resolveCommand("帮助").command, "help");
  assert.equal(terminalCommands.resolveCommand("首页").command, "home");
  assert.equal(terminalCommands.resolveCommand("搜索 RAG").command, "search");
  assert.deepEqual(
    terminalCommands.resolveCommand("图谱 聚焦 AI Agent"),
    {
      command: "graph",
      args: "focus AI Agent",
      exact: true,
      suggestion: terminalCommands.commands.find((item) => item.id === "graph focus"),
    },
  );
});

test("fuzzy suggestions rank a transposed command first", () => {
  const suggestions = terminalCommands.rankCommandSuggestions("serach", 4);

  assert.equal(suggestions[0].id, "search");
  assert.equal(suggestions[0].label, "SEARCH");
  assert.ok(suggestions[0].score > suggestions[1].score);
});

test("nested graph commands provide prefix completion", () => {
  const suggestions = terminalCommands.rankCommandSuggestions("GRAPH FOC", 4);

  assert.equal(suggestions[0].id, "graph focus");
  assert.equal(
    terminalCommands.applyCommandCompletion("GRAPH FOC", suggestions[0]),
    "graph focus ",
  );
});

test("empty input returns a compact discoverability set", () => {
  const suggestions = terminalCommands.rankCommandSuggestions("", 4);

  assert.deepEqual(
    suggestions.map((item) => item.id),
    ["help", "ls", "open", "search"],
  );
});

test("unknown commands remain non-executable but include a recommendation", () => {
  const parsed = terminalCommands.resolveCommand("searhc knowledge graph");

  assert.equal(parsed.exact, false);
  assert.equal(parsed.command, "searhc");
  assert.equal(parsed.suggestion.id, "search");
  assert.equal(parsed.args, "knowledge graph");
});

test("command matching caps untrusted input before fuzzy distance allocation", () => {
  const oversized = `serach${"x".repeat(100_000)}`;

  assert.equal(terminalCommands.maxInputLength, 240);
  assert.equal(terminalCommands.normalizeCommandText(oversized).length, 240);
  assert.doesNotThrow(() => terminalCommands.rankCommandSuggestions(oversized, 4));
  assert.match(
    terminalSource,
    /input\.maxLength = commandApi\.maxInputLength;/u,
  );
});

test("completion never traps reverse tab and closes after accepting a suggestion", () => {
  const acceptBlock = terminalSource.slice(
    terminalSource.indexOf("function acceptSuggestion"),
    terminalSource.indexOf("function suggestionQuery"),
  );

  assert.match(terminalSource, /if \(e\.key === "Tab" && e\.shiftKey\) return;/u);
  assert.match(acceptBlock, /closeSuggestions\(\);/u);
  assert.doesNotMatch(acceptBlock, /renderSuggestions\(\);/u);
  assert.match(terminalSource, /option\.tabIndex = -1;/u);
});

test("command suggestions own their active keyboard interaction without leaking to the graph", () => {
  const keydownBlock = terminalSource.slice(
    terminalSource.indexOf('input.addEventListener("keydown"'),
    terminalSource.indexOf('const execBtn = $(".terminal-exec")'),
  );

  assert.doesNotMatch(keydownBlock, /hasTypedValue && suggestionsUi/u);
  assert.match(
    keydownBlock,
    /if \(suggestionsUi && suggestionsUi\.isOpen\(\)\) \{\s*e\.preventDefault\(\);\s*e\.stopPropagation\(\);\s*suggestionsUi\.closeSuggestions\(\);/u,
  );
});

test("IME composition suspends suggestions and failed commands do not accumulate", () => {
  assert.match(terminalSource, /input\.addEventListener\("compositionstart"/u);
  assert.match(terminalSource, /if \(composing \|\| event\.isComposing\)/u);
  assert.match(terminalSource, /isComposing: \(\) => composing/u);

  const keydownBlock = terminalSource.slice(
    terminalSource.indexOf('input.addEventListener("keydown"'),
    terminalSource.indexOf('const execBtn = $(".terminal-exec")'),
  );
  const submitBlock = terminalSource.slice(
    terminalSource.indexOf("async function submitCurrentCommand"),
    terminalSource.indexOf('input.addEventListener("keydown"'),
  );
  assert.match(submitBlock, /input\.value = "";/u);
  assert.match(submitBlock, /await runCommand\(value\);/u);
  assert.match(terminalSource, /input\.inputMode = "latin";/u);
});

test("IME composition cannot submit through the execution button or duplicate initialization", () => {
  const initBlock = terminalSource.slice(
    terminalSource.indexOf("function initTerminal"),
    terminalSource.indexOf("function initRainFog"),
  );
  const execBlock = initBlock.slice(initBlock.indexOf('const execBtn = $(".terminal-exec")'));

  assert.match(initBlock, /input\.dataset\.terminalInitialized === "true"/u);
  assert.match(initBlock, /input\.dataset\.terminalInitialized = "true"/u);
  assert.match(execBlock, /suggestionsUi\?\.isComposing\(\)/u);
  assert.doesNotMatch(
    initBlock.slice(initBlock.indexOf("if (host)"), initBlock.indexOf('input.addEventListener("keydown"')),
    /input\.addEventListener\("compositionend"/u,
  );
});

test("command UI preserves archive routing and touch pointer behavior", () => {
  assert.match(
    terminalSource,
    /case "archive": \{\s*window\.location\.href = "\/archive\/";/u,
  );
  assert.match(
    terminalSource,
    /if \(event\.pointerType === "mouse"\) event\.preventDefault\(\);/u,
  );
  assert.doesNotMatch(terminalSource, /overlay\.setAttribute\("aria-live"/u);
  assert.match(terminalSource, /class="terminal-log" id="terminal-log" role="log"/u);
});
