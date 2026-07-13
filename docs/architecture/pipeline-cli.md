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
digest is stored as `artifact_digest` with kind `public_tree_manifest_v2` in the
external release descriptor. Readers accept v2 and N-1 v1, but the descriptor
kind must match the tree schema. The transport tar SHA produced later by
`artifact_guard` remains a separate cross-permission transfer check; it is never
used as the release artifact digest.

Manifest v2 also binds the deployable HTML surface. `index.html` becomes `/`,
`path/index.html` becomes `/path/`, and every other `.html` path becomes its
absolute public path. `route_count` and the SHA-256 of the canonical sorted route
array make route loss or addition visible independently of byte totals.

The release guard models the Pages transport because the pinned
[`actions/upload-pages-artifact` action](https://github.com/actions/upload-pages-artifact/blob/56afc609e74202658d3ffba0e8f6dda462b719fa/action.yml)
first creates `artifact.tar` and then uploads that one file. The official pinned
[`actions/upload-artifact` input contract](https://github.com/actions/upload-artifact/blob/ea165f8d65b6e75b540449e92b4886f43607fa02/action.yml)
documents zlib level 6 as the default. The guard therefore creates a temporary,
path-sorted tar (including root and directory entries) with fixed
uid/gid/mode/time metadata and streams it into a
single-member deterministic ZIP using DEFLATE level 6. This is a conservative
pre-upload estimate, not a claim that its bytes are identical to GitHub's
runner-side archive.

All pre-existing limits remain fail-closed: regular non-executable files only,
no symlinks or hardlinks, 16 MiB per file, and 256 MiB raw tree size. The file
fuse is 30,000, with a separate 30,000-directory fuse; even the mandatory
512-byte tar header per file is 14.65 MiB at that count, so the fuses bound
traversal/inode and archive-header pressure. They are not artifact acceptance
targets. The deterministic Pages estimate records
`ok` below 90 MiB and `warning` from 90 MiB, and rejects 100 MiB or more. Every
file is reopened with no-follow semantics and checked against its first-pass
size, digest, inode, timestamps, mode, and link count; temporary tar/ZIP files
are removed on success and failure.

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

Each Hugo-only shadow comparison can append an audit record while retaining the
existing standalone report:

```text
uv run python scripts/shadow_compare.py \
  --baseline legacy-public --candidate ledger-public \
  --report shadow-report.json \
  --code-sha CODE_SHA --content-sha CONTENT_SHA \
  --evidence-root OPS_LEDGER/ops/migrations/shadow \
  --run-id RUN_ID --completed-at 2026-07-13T08:00:00Z \
  --expected-previous-digest PREVIOUS_SHA256
```

`shadow_compare.py` writes the complete report, including all external-link
sets, to `--report` and the content-addressed evidence store. Its stdout is a
bounded `shadow_compare_summary_v1`: counts, tree digests, at most 20 paths per
difference class, the canonical report digest, and the appended record digest.
External-link values are never copied into Actions logs.

The ordinary comparison CLI cannot claim a successful `--full-build`. A
qualifying full build must first produce two byte-identical Hugo trees, run
Pagefind 1.5.2 once against an isolated copy of that common input, and inject
only the resulting regular-file `pagefind/` subtree into both final tree
copies. The full-build attestation is then generated with:

```text
uv run python scripts/shadow_full_build.py \
  --hugo-baseline legacy-hugo-public \
  --hugo-candidate ledger-hugo-public \
  --final-baseline legacy-final-public \
  --final-candidate ledger-final-public \
  --pagefind-bundle shared-pagefind-bundle \
  --package-lock package-lock.json \
  --pagefind-runner node_modules/pagefind/lib/runner/bin.cjs \
  --platform-package @pagefind/linux-x64 \
  --pagefind-command npm run build:search \
  --command-input package_json=package.json \
  --command-input pagefind_config=pagefind.yml \
  --command-input catalog_wrapper=scripts/build_pagefind_catalog.py \
  --command-input catalog_core=ai_stack/pagefind_catalog.py \
  --command-input release_basis=build-handoff/state/release-basis.json \
  --report full-shadow-report.json \
  --code-sha CODE_SHA --content-sha CONTENT_SHA \
  --evidence-root OPS_LEDGER/ops/migrations/shadow \
  --run-id RUN_ID --completed-at 2026-07-13T08:00:00Z \
  --expected-previous-digest PREVIOUS_SHA256
```

`--pagefind-runner` must name the resolved regular runner file, not a symlink.
The command hashes the package lock, runner, command argv, Pagefind config,
package and catalog code, and the exact generated release basis; verifies the
exact Pagefind and platform package versions and npm integrity values; and
rejects duplicate input names or symlinked path components. It never executes
the recorded command: callers
first build the production-format bundle, including catalog generation and
fragment removal when configured, and then attest that exact directory. It
verifies an additive-only injection: no pre-existing
`pagefind/` files, no removed or changed Hugo paths, no additions outside the
allowlisted prefix, and both added subtrees equal the same bundle digest. The
final comparison still covers every path and byte; `compare_trees` has no
ignore or exclusion mode.

The resulting `shadow_full_build_v1` report references the pre-injection and
post-injection `shadow_compare_v1` reports by digest. All three objects are
stored under `reports/<sha256>.json`; the ordered record still uses the
unchanged `shadow_migration_evidence_v1` hash-chain schema. Legacy v1 full-build
records remain readable and preserve their original digest, but do not satisfy
the new three-full-build threshold. The full-build CLI likewise prints only a
bounded `shadow_full_build_summary_v1`, including the report and record digests;
the complete composite remains in `--report` and the evidence store.

Omit `--expected-previous-digest` only for the first record. Reports live under
`reports/<sha256>.json`; ordered records live under
`records/<sequence>-<sha256>.json` and bind the previous record digest. Both are
canonical JSON and append-only. A mismatch is recorded as `FAILED`, resets the
current success window, and can never count toward the gate. Duplicate run IDs,
timestamp reordering, future timestamps, chain gaps, report tampering, and
code/content SHA mismatches fail closed.

`ai-stack migrate dedupe --shadow-evidence-root ... --expected-code-sha
CODE_SHA --expected-source-sha CONTENT_SHA` reports three independently
verified thresholds: 24 consecutive successful runs, three qualifying shared
Pagefind full-build attestations, and seven elapsed days since the start of the
uninterrupted window. Supplying an expected code or content SHA scopes the
entire latest streak, not only its last record: any run with another identity
breaks the window. The CLI requires the current code SHA whenever shadow
evidence is used, so 24 runs produced by an older implementation cannot unlock
a cutover or dedupe under newer code. Passing these checks does **not** mutate
content in this release: the dedupe mutation engine is intentionally absent, so
`--execute` stops after validation with zero changes.

The shared-bundle profile proves “identical Hugo input + one content-addressed
Pagefind bundle injected into both outputs + identical complete final trees.”
It deliberately does **not** claim that two independent Pagefind 1.5.2 runs
produce byte-identical output.

The filesystem hash chain detects mutation relative to its anchored head; it
cannot by itself prove that an untrusted producer actually executed a build.
Production use therefore still requires the protected `ops` writer, Git
fast-forward/CAS, validated cross-job artifacts, and an externally retained head
digest. Removing old records also requires a separately signed archive anchor;
the current verifier expects an unbroken chain beginning at sequence 1.
