# Unified pipeline CLI contract

The CLI preserves the existing GitHub Actions trigger contract while making each
trust boundary explicit. Every cross-job directory contains only `content/`,
`ops/`, and/or `state/` paths and must be repackaged by `artifact_guard`.

## Trusted DAG commands

```text
ai-stack crawl --run-id RUN --output handoff
ai-stack validate --kind discovery --input handoff --output validated
ai-stack process --phase persist-discovery --run-id RUN \
  --input validated --state-root CONTENT_LEDGER
ai-stack process --phase reserve-budget --run-id RUN \
  --input CONTENT_LEDGER --state-root OPS_LEDGER
ai-stack process --phase generate --run-id RUN \
  --input CONTENT_LEDGER --ops-root OPS_LEDGER --output generated
ai-stack validate --kind generated --input generated --output validated-result
ai-stack process --phase persist-result --run-id RUN \
  --input validated-result --state-root CONTENT_LEDGER
ai-stack render --run-id RUN --code-sha CODE_SHA --content-sha CONTENT_SHA \
  --ops-sha OPS_SHA --content-root CONTENT_LEDGER --ops-root OPS_LEDGER \
  --output build-handoff
```

`render` writes the static API source into `blog/static/api/v1`, copies the
release outbox to `build-handoff/content/outbox`, and writes only
`build-handoff/state/release-basis.json`. The basis has no artifact digest.

After Hugo, Pagefind, and final DOM validation complete, the workflow must run:

```text
python scripts/release_guard.py create \
  --public-root blog/public \
  --basis build-handoff/state/release-basis.json \
  --output build-handoff/state/release.json
```

This command hashes a canonical manifest of the completed `blog/public` tree.
The manifest is path-sorted and records each path, byte length, and SHA-256. Its
digest is stored as `artifact_digest` with kind `public_tree_manifest_v1` in the
external release descriptor. The transport tar SHA produced later by
`artifact_guard` remains a separate cross-permission transfer check; it is never
used as the release artifact digest.

The release ID is independently derived from:

```text
hash(schema_version, release_seq, code_sha, content_sha)
```

It intentionally excludes the public-tree digest because public API files embed
the release ID. This removes any self-referential hashing cycle.

Deploy first validates the candidate against the previous
`ops/releases/current-healthy.json`. After production health succeeds, the
secret-free ops writer persists the exact descriptor both as an append-only
record and as the current healthy pointer:

```text
ai-stack process --phase persist-release --run-id RUN \
  --input release --state-root OPS_LEDGER \
  --expected-release-id RELEASE_ID \
  --expected-code-sha CODE_SHA --expected-content-sha CONTENT_SHA \
  --expected-artifact-digest PUBLIC_TREE_DIGEST
```

The publisher checks `release/state/release.json` for exact equality with that
healthy pointer and recomputes the digest of
`release/state/public-tree-manifest.json` before channel credentials enter its
step. Publishing and receipt persistence then use:

```text
ai-stack publish --run-id RUN --input release/content/outbox --output receipts
ai-stack process --phase persist-receipt --run-id RUN \
  --input receipts --state-root OPS_LEDGER
```

Configured channels remain disabled by default. A timeout or exception after a
send attempt becomes `UNKNOWN`; it is persisted and not blindly retried.

## Migration safety

The supported migration commands are:

```text
ai-stack migrate inventory [CONTENT_ROOT]
ai-stack migrate seed-content SOURCE_ROOT --target-root TARGET_ROOT
ai-stack migrate dedupe [CONTENT_ROOT]
ai-stack migrate restore SOURCE_ROOT --target-root TARGET_ROOT
```

All default to dry-run. `--execute` requires `--expected-source-sha`,
`--backup-id`, and `--max-changes`. Seed and restore never overwrite or delete a
file. Dedupe additionally caps `--max-changes` at 100 and requires an exact
`--shadow-evidence-root` from the `ops` ledger.

Each shadow comparison can append an audit record while retaining the existing
standalone report:

```text
uv run python scripts/shadow_compare.py \
  --baseline legacy-public --candidate ledger-public \
  --report shadow-report.json \
  --code-sha CODE_SHA --content-sha CONTENT_SHA \
  --evidence-root OPS_LEDGER/ops/migrations/shadow \
  --run-id RUN_ID --completed-at 2026-07-13T08:00:00Z \
  --full-build --expected-previous-digest PREVIOUS_SHA256
```

Omit `--expected-previous-digest` only for the first record. Reports live under
`reports/<sha256>.json`; ordered records live under
`records/<sequence>-<sha256>.json` and bind the previous record digest. Both are
canonical JSON and append-only. A mismatch is recorded as `FAILED`, resets the
current success window, and can never count toward the gate. Duplicate run IDs,
timestamp reordering, future timestamps, chain gaps, report tampering, and
code/content SHA mismatches fail closed.

`ai-stack migrate dedupe --shadow-evidence-root ...` reports three independently
verified thresholds: 24 consecutive successful runs, three successful full-tree
build comparisons, and seven elapsed days since the start of the uninterrupted
window. The latest evidence must bind the requested source SHA. Passing these
checks does **not** mutate content in this release: the dedupe mutation engine is
intentionally absent, so `--execute` stops after validation with zero changes.

The filesystem hash chain detects mutation relative to its anchored head; it
cannot by itself prove that an untrusted producer actually executed a build.
Production use therefore still requires the protected `ops` writer, Git
fast-forward/CAS, validated cross-job artifacts, and an externally retained head
digest. Removing old records also requires a separately signed archive anchor;
the current verifier expects an unbroken chain beginning at sequence 1.
