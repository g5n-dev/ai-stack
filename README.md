# AI Stack content ledger

This orphan branch stores canonical content data only. Code and generated site
artifacts do not belong here.

- The initial seed is a byte-exact, append-only copy from Git commit
  `b71a275de15c8ee27f6f0428b4bac901d63001f6`.
- The seed does not deduplicate, rename, delete, or rewrite any Markdown file.
- `content/seed-manifest.json` binds every seeded path to its SHA-256 digest.
- New writes are limited to `content/` and `state/`, use expected-parent CAS,
  and must be normal fast-forward commits.
- Deletion and history rewriting are not part of the normal writer path.

