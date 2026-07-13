from hashlib import sha256
import unittest


from processor.evidence_pipeline import EvidenceGate, PublicationTier


class EvidenceGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.gate = EvidenceGate(minimum_coverage=0.9)
        self.snapshots = {
            "snap-1": "Project Atlas released version 2.0 on 2026-07-13. It adds a local cache.",
            "snap-2": "The maintainers describe the release as experimental.",
        }

    def evidence(self, evidence_id: str, snapshot_id: str, snippet: str, **changes: object) -> dict[str, object]:
        snapshot = self.snapshots[snapshot_id]
        start_character = snapshot.index(snippet)
        start_byte = len(snapshot[:start_character].encode("utf-8"))
        record: dict[str, object] = {
            "id": evidence_id,
            "url": f"https://example.test/{snapshot_id}",
            "snapshot_id": snapshot_id,
            "snapshot_sha256": sha256(snapshot.encode("utf-8")).hexdigest(),
            "start_byte": start_byte,
            "end_byte": start_byte + len(snippet.encode("utf-8")),
            "snippet": snippet,
        }
        record.update(changes)
        return record

    def test_rejects_long_article_with_no_factual_claims(self) -> None:
        decision = self.gate.evaluate(
            {
                "body": "A" * 201,
                "claims": [],
                "evidence": [],
                "content_mode": "article",
            },
            self.snapshots,
        )

        self.assertFalse(decision.publishable)
        self.assertEqual(decision.tier, PublicationTier.QUARANTINED)
        self.assertIn("no_factual_claims", decision.reasons)

    def test_requires_evidence_snippet_to_exist_in_snapshot(self) -> None:
        decision = self.gate.evaluate(
            {
                "body": "Project Atlas released version 2.0.",
                "claims": [
                    {
                        "id": "claim-1",
                        "text": "Project Atlas released version 2.0.",
                        "kind": "fact",
                        "evidence_ids": ["ev-1"],
                    }
                ],
                "evidence": [
                    {
                        "id": "ev-1",
                        "url": "https://example.test/snap-1",
                        "snapshot_id": "snap-1",
                        "snapshot_sha256": sha256(self.snapshots["snap-1"].encode()).hexdigest(),
                        "start_byte": 0,
                        "end_byte": 34,
                        "snippet": "Project Atlas released version 9.9",
                    }
                ],
                "content_mode": "article",
            },
            self.snapshots,
        )

        self.assertFalse(decision.publishable)
        self.assertIn("unlocatable_evidence:ev-1", decision.reasons)

    def test_numeric_and_security_claims_require_full_support(self) -> None:
        article = {
            "body": "Project Atlas released version 2.0 and is secure.",
            "claims": [
                {
                    "id": "claim-1",
                    "text": "Project Atlas released version 2.0.",
                    "kind": "numeric",
                    "evidence_ids": ["ev-1"],
                },
                {
                    "id": "claim-2",
                    "text": "Project Atlas is secure.",
                    "kind": "security",
                    "evidence_ids": [],
                },
            ],
            "evidence": [
                self.evidence(
                    "ev-1",
                    "snap-1",
                    "Project Atlas released version 2.0 on 2026-07-13",
                )
            ],
            "content_mode": "article",
        }

        decision = self.gate.evaluate(article, self.snapshots)

        self.assertFalse(decision.publishable)
        self.assertEqual(decision.coverage, 0.5)
        self.assertIn("mandatory_claim_unsupported:claim-2", decision.reasons)

    def test_publishes_supported_article_as_tier_a(self) -> None:
        decision = self.gate.evaluate(
            {
                "body": "Project Atlas released version 2.0. The release is experimental.",
                "claims": [
                    {
                        "id": "claim-1",
                        "text": "Project Atlas released version 2.0.",
                        "kind": "numeric",
                        "evidence_ids": ["ev-1"],
                    },
                    {
                        "id": "claim-2",
                        "text": "The release is experimental.",
                        "kind": "source_claim",
                        "evidence_ids": ["ev-2"],
                    },
                ],
                "evidence": [
                    self.evidence(
                        "ev-1",
                        "snap-1",
                        "Project Atlas released version 2.0 on 2026-07-13",
                    ),
                    self.evidence("ev-2", "snap-2", "describe the release as experimental"),
                ],
                "content_mode": "article",
            },
            self.snapshots,
        )

        self.assertTrue(decision.publishable)
        self.assertEqual(decision.tier, PublicationTier.A)
        self.assertEqual(decision.coverage, 1.0)

    def test_typed_inference_can_publish_as_tier_b(self) -> None:
        decision = self.gate.evaluate(
            {
                "body": "Project Atlas released version 2.0. This may accelerate adoption.",
                "claims": [
                    {
                        "id": "claim-1",
                        "text": "Project Atlas released version 2.0.",
                        "kind": "numeric",
                        "evidence_ids": ["ev-1"],
                    },
                    {
                        "id": "claim-2",
                        "text": "This may accelerate adoption.",
                        "kind": "inference",
                        "evidence_ids": ["ev-1"],
                    },
                ],
                "evidence": [
                    self.evidence(
                        "ev-1",
                        "snap-1",
                        "Project Atlas released version 2.0 on 2026-07-13",
                    )
                ],
                "content_mode": "article",
            },
            self.snapshots,
        )

        self.assertTrue(decision.publishable)
        self.assertEqual(decision.tier, PublicationTier.B)

    def test_high_risk_domain_never_auto_publishes(self) -> None:
        decision = self.gate.evaluate(
            {
                "body": "Use this dosage for medical treatment.",
                "claims": [
                    {
                        "id": "claim-1",
                        "text": "Use this dosage for medical treatment.",
                        "kind": "numeric",
                        "evidence_ids": ["ev-1"],
                    }
                ],
                "evidence": [
                    self.evidence("ev-1", "snap-1", "Project Atlas released version 2.0")
                ],
                "risk_domain": "medical",
                "content_mode": "article",
            },
            self.snapshots,
        )

        self.assertFalse(decision.publishable)
        self.assertIn("high_risk_domain:medical", decision.reasons)

    def test_rejects_tampered_snapshot_hash(self) -> None:
        evidence = self.evidence("ev-1", "snap-1", "Project Atlas released version 2.0")
        evidence["snapshot_sha256"] = "0" * 64

        decision = self.gate.evaluate(
            {
                "body": "Project Atlas released version 2.0.",
                "claims": [
                    {
                        "id": "claim-1",
                        "kind": "numeric",
                        "evidence_ids": ["ev-1"],
                    }
                ],
                "evidence": [evidence],
            },
            self.snapshots,
        )

        self.assertFalse(decision.publishable)
        self.assertIn("snapshot_hash_mismatch:ev-1", decision.reasons)

    def test_rejects_imprecise_byte_locator(self) -> None:
        evidence = self.evidence("ev-1", "snap-1", "Project Atlas released version 2.0")
        evidence["start_byte"] = 1

        decision = self.gate.evaluate(
            {
                "body": "Project Atlas released version 2.0.",
                "claims": [
                    {
                        "id": "claim-1",
                        "kind": "numeric",
                        "evidence_ids": ["ev-1"],
                    }
                ],
                "evidence": [evidence],
            },
            self.snapshots,
        )

        self.assertFalse(decision.publishable)
        self.assertIn("unlocatable_evidence:ev-1", decision.reasons)

    def test_source_brief_is_the_only_claimless_publishable_mode(self) -> None:
        decision = self.gate.evaluate(
            {
                "body": "来源发布了一个实验版本。",
                "claims": [],
                "evidence": [
                    self.evidence(
                        "ev-1",
                        "snap-2",
                        "The maintainers describe the release as experimental.",
                    )
                ],
                "content_mode": "source_brief",
            },
            self.snapshots,
        )

        self.assertTrue(decision.publishable)
        self.assertEqual(decision.tier, PublicationTier.C)

    def test_rejects_malformed_duplicate_and_dangerous_records(self) -> None:
        valid = self.evidence("ev-1", "snap-1", "Project Atlas released version 2.0")
        duplicate = dict(valid)
        bad_url = self.evidence("ev-2", "snap-1", "It adds a local cache.")
        bad_url["url"] = "javascript:alert(1)"
        decision = self.gate.evaluate(
            {
                "body": "conflicting",
                "contradictory_evidence": True,
                "claims": ["not-a-claim"],
                "evidence": ["not-evidence", valid, duplicate, bad_url],
            },
            self.snapshots,
        )

        self.assertFalse(decision.publishable)
        self.assertIn("contradictory_evidence", decision.reasons)
        self.assertIn("invalid_evidence_record", decision.reasons)
        self.assertIn("invalid_or_duplicate_evidence_id", decision.reasons)
        self.assertIn("invalid_evidence_url:ev-2", decision.reasons)
        self.assertIn("invalid_claim_record", decision.reasons)

    def test_accepts_hashed_snapshot_record(self) -> None:
        evidence = self.evidence("ev-1", "snap-1", "Project Atlas released version 2.0")
        decision = self.gate.evaluate(
            {
                "body": "Project Atlas released version 2.0.",
                "claims": [
                    {"id": "claim-1", "kind": "numeric", "evidence_ids": ["ev-1"]}
                ],
                "evidence": [evidence],
            },
            {"snap-1": {"content": self.snapshots["snap-1"]}},
        )

        self.assertTrue(decision.publishable)

    def test_rejects_duplicate_claim_and_unsupported_inference(self) -> None:
        evidence = self.evidence("ev-1", "snap-1", "Project Atlas released version 2.0")
        decision = self.gate.evaluate(
            {
                "body": "Project Atlas released version 2.0, which may change adoption.",
                "claims": [
                    {"id": "claim-1", "kind": "fact", "evidence_ids": ["ev-1"]},
                    {"id": "claim-1", "kind": "fact", "evidence_ids": ["ev-1"]},
                    {"id": "claim-2", "kind": "inference", "evidence_ids": []},
                ],
                "evidence": [evidence],
            },
            self.snapshots,
        )

        self.assertFalse(decision.publishable)
        self.assertIn("invalid_or_duplicate_claim_id", decision.reasons)
        self.assertIn("inference_without_supported_premise:claim-2", decision.reasons)

    def test_rejects_invalid_gate_limits(self) -> None:
        with self.assertRaises(ValueError):
            EvidenceGate(minimum_coverage=0)
        with self.assertRaises(ValueError):
            EvidenceGate(long_body_threshold=0)


if __name__ == "__main__":
    unittest.main()
