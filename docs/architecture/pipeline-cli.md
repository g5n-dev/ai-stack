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

Publishing and receipt persistence then use:

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
file. Dedupe execution remains blocked until 24 shadow runs and the seven-day
soak gate have actually completed.
