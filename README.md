# AI Stack operations ledger

This orphan branch stores non-rewindable operational facts only. Application
code, canonical articles, and generated site artifacts do not belong here.

- `state/ops/` is the content-addressed ledger for budget reservations,
  outbox entries, release sequence records, publisher receipts, and
  reconciliation state.
- `backups/` contains verified immutable-backup records used only by the
  separately approved break-glass deletion workflow.
- Normal writers use expected-parent compare-and-swap and fast-forward commits.
- Normal writers cannot delete records or rewrite branch history.
- Rolling content back never rolls this branch or its budget/notification facts
  backward.
