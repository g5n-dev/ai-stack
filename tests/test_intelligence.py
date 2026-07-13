#!/usr/bin/env python3

import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from processor.intelligence import (
    IntelligenceValidationError,
    TREND_FORMULA,
    build_static_intelligence,
    canonical_events,
    calculate_trends,
)


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "intelligence_events.json"
AS_OF = datetime(2026, 7, 13, 12, 0, tzinfo=timezone.utc)


def load_fixture():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def tree_bytes(root: Path):
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class CanonicalEventTest(unittest.TestCase):
    def test_aliases_orphans_and_quarantined_events_are_not_public(self):
        result = canonical_events(load_fixture()["events"])

        self.assertEqual(
            [event["event_id"] for event in result],
            [
                "evt-agent-1",
                "evt-agent-2",
                "evt-agent-3",
                "evt-agent-4",
                "evt-agent-5",
            ],
        )
        self.assertNotIn("untrusted-topic", {topic for event in result for topic in event["topics"]})

    def test_latest_revision_wins_without_mutating_input(self):
        events = [
            {
                "event_id": "evt-1",
                "canonical_event_id": "evt-1",
                "occurred_at": "2026-07-13T10:00:00Z",
                "updated_at": "2026-07-13T10:01:00Z",
                "title": "old",
            },
            {
                "event_id": "evt-1",
                "canonical_event_id": "evt-1",
                "occurred_at": "2026-07-13T10:00:00Z",
                "updated_at": "2026-07-13T10:02:00Z",
                "title": "new",
            },
        ]
        original = json.loads(json.dumps(events))

        result = canonical_events(events)

        self.assertEqual(result[0]["title"], "new")
        self.assertEqual(events, original)


class TrendV1Test(unittest.TestCase):
    def test_emits_three_fixed_windows_and_honest_cutoff(self):
        payload = calculate_trends(load_fixture()["events"], as_of=AS_OF)

        self.assertEqual(payload["schema_version"], "trend_v1")
        self.assertEqual(payload["as_of"], "2026-07-13T12:00:00Z")
        self.assertEqual(payload["windows"].keys(), {"24h", "7d", "30d"})
        self.assertEqual(payload["formula"], TREND_FORMULA)
        self.assertNotIn("实时", json.dumps(payload, ensure_ascii=False))

    def test_requires_three_unique_canonical_events_per_topic(self):
        payload = calculate_trends(load_fixture()["events"], as_of=AS_OF)

        trends_24h = payload["windows"]["24h"]["trends"]

        self.assertEqual([trend["topic"] for trend in trends_24h], ["agents"])
        self.assertEqual(trends_24h[0]["unique_events"], 3)
        self.assertNotIn("llm", [trend["topic"] for trend in trends_24h])

    def test_score_exposes_every_component_and_exact_formula(self):
        payload = calculate_trends(load_fixture()["events"], as_of=AS_OF)
        trend = payload["windows"]["24h"]["trends"][0]
        components = trend["components"]

        weighted = (
            0.25 * components["quantity"]
            + 0.25 * components["growth"]
            + 0.15 * components["acceleration"]
            + 0.15 * components["source_diversity"]
            + 0.10 * components["novelty"]
            + 0.10 * components["source_weight"]
        )
        expected = round(100 * weighted * (1 - 0.5 * trend["duplicate_rate"]), 6)

        self.assertEqual(trend["score"], expected)
        self.assertEqual(trend["observations"], 5)
        self.assertEqual(trend["duplicate_rate"], 0.4)
        self.assertEqual(set(components), {
            "quantity",
            "growth",
            "acceleration",
            "source_diversity",
            "novelty",
            "source_weight",
        })

    def test_duplicate_observations_only_reduce_the_penalty(self):
        events = load_fixture()["events"]
        without_aliases = [
            event for event in events if event["event_id"] == event["canonical_event_id"]
        ]

        with_duplicates = calculate_trends(events, as_of=AS_OF)["windows"]["24h"]["trends"][0]
        without_duplicates = calculate_trends(without_aliases, as_of=AS_OF)["windows"]["24h"]["trends"][0]

        self.assertEqual(with_duplicates["components"], without_duplicates["components"])
        self.assertLess(with_duplicates["score"], without_duplicates["score"])

    def test_future_events_do_not_leak_into_the_cutoff(self):
        events = load_fixture()["events"] + [
            {
                "event_id": "evt-future",
                "canonical_event_id": "evt-future",
                "occurred_at": "2026-07-13T12:01:00Z",
                "source": "github",
                "source_weight": 1.0,
                "topics": ["agents"],
            }
        ]

        trend = calculate_trends(events, as_of=AS_OF)["windows"]["24h"]["trends"][0]

        self.assertEqual(trend["unique_events"], 3)


class StaticIntelligenceBuildTest(unittest.TestCase):
    def test_build_is_byte_stable_and_release_is_content_addressed(self):
        fixture = load_fixture()
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_result = build_static_intelligence(
                output_dir=first,
                events=fixture["events"],
                entities=fixture["entities"],
                graph=fixture["graph"],
                as_of=AS_OF,
                base_url="https://ai-stack.example",
                max_items_per_shard=2,
                max_shard_bytes=2_048,
            )
            second_result = build_static_intelligence(
                output_dir=second,
                events=list(reversed(fixture["events"])),
                entities=list(reversed(fixture["entities"])),
                graph=list(reversed(fixture["graph"])),
                as_of=AS_OF,
                base_url="https://ai-stack.example",
                max_items_per_shard=2,
                max_shard_bytes=2_048,
            )

            self.assertEqual(first_result["release_id"], second_result["release_id"])
            self.assertRegex(first_result["release_id"], r"^r-[0-9a-f]{20}$")
            self.assertEqual(tree_bytes(Path(first)), tree_bytes(Path(second)))

    def test_manifest_checksums_sizes_and_shard_limits_match_files(self):
        fixture = load_fixture()
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = build_static_intelligence(
                output_dir=tmp_dir,
                events=fixture["events"],
                entities=fixture["entities"],
                graph=fixture["graph"],
                as_of=AS_OF,
                max_items_per_shard=2,
                max_shard_bytes=2_048,
            )
            root = Path(tmp_dir)
            release_manifest = json.loads(
                (root / result["release_manifest_path"]).read_text(encoding="utf-8")
            )

            for collection in release_manifest["collections"].values():
                for shard in collection["shards"]:
                    body = (root / shard["path"].lstrip("/")).read_bytes()
                    self.assertEqual(hashlib.sha256(body).hexdigest(), shard["sha256"])
                    self.assertEqual(len(body), shard["bytes"])
                    self.assertLessEqual(shard["count"], 2)
                    self.assertLessEqual(shard["bytes"], 2_048)
                    self.assertRegex(Path(shard["path"]).name, r"^[0-9a-f]{20}\.json$")

    def test_shard_policy_is_part_of_the_content_addressed_release(self):
        fixture = load_fixture()
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_result = build_static_intelligence(
                output_dir=first,
                events=fixture["events"],
                entities=fixture["entities"],
                graph=fixture["graph"],
                as_of=AS_OF,
                max_items_per_shard=1,
            )
            second_result = build_static_intelligence(
                output_dir=second,
                events=fixture["events"],
                entities=fixture["entities"],
                graph=fixture["graph"],
                as_of=AS_OF,
                max_items_per_shard=2,
            )

            self.assertNotEqual(first_result["release_id"], second_result["release_id"])

    def test_reusing_an_explicit_release_id_cannot_mutate_existing_release(self):
        fixture = load_fixture()
        with tempfile.TemporaryDirectory() as tmp_dir:
            first_result = build_static_intelligence(
                output_dir=tmp_dir,
                events=fixture["events"],
                entities=fixture["entities"],
                graph=fixture["graph"],
                as_of=AS_OF,
                release_id="fixed-release",
            )
            root_manifest = Path(tmp_dir) / first_result["root_manifest_path"]
            original_root = root_manifest.read_bytes()
            original_tree = tree_bytes(Path(tmp_dir))

            changed_events = [dict(event) for event in fixture["events"]]
            changed_events[0]["title"] = "不同内容"
            with self.assertRaises(IntelligenceValidationError):
                build_static_intelligence(
                    output_dir=tmp_dir,
                    events=changed_events,
                    entities=fixture["entities"],
                    graph=fixture["graph"],
                    as_of=AS_OF,
                    release_id="fixed-release",
                )

            self.assertEqual(root_manifest.read_bytes(), original_root)
            self.assertEqual(tree_bytes(Path(tmp_dir)), original_tree)

    def test_only_canonical_public_events_are_emitted(self):
        fixture = load_fixture()
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = build_static_intelligence(
                output_dir=tmp_dir,
                events=fixture["events"],
                entities=[],
                graph=[],
                as_of=AS_OF,
            )
            manifest = json.loads(
                (Path(tmp_dir) / result["release_manifest_path"]).read_text(encoding="utf-8")
            )
            emitted = []
            for shard in manifest["collections"]["events"]["shards"]:
                payload = json.loads(
                    (Path(tmp_dir) / shard["path"].lstrip("/")).read_text(encoding="utf-8")
                )
                emitted.extend(payload["items"])

            self.assertEqual(len(emitted), 5)
            self.assertTrue(all(event["event_id"] == event["canonical_event_id"] for event in emitted))

    def test_feed_metadata_is_static_local_and_format_explicit(self):
        fixture = load_fixture()
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = build_static_intelligence(
                output_dir=tmp_dir,
                events=fixture["events"],
                entities=fixture["entities"],
                graph=[],
                as_of=AS_OF,
                base_url="https://ai-stack.example/",
            )
            metadata = json.loads(
                (Path(tmp_dir) / result["feeds_path"]).read_text(encoding="utf-8")
            )

            self.assertEqual(
                {feed["format"] for feed in metadata["feeds"]},
                {"rss", "json_feed", "opml"},
            )
            self.assertEqual(metadata["data_as_of"], "2026-07-13T12:00:00Z")
            self.assertFalse(metadata["realtime"])
            self.assertEqual(metadata["watchlist_scope"], "local_browser_only")
            self.assertNotIn("跨设备同步", json.dumps(metadata, ensure_ascii=False))

    def test_rejects_path_traversal_and_an_oversized_single_item(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(IntelligenceValidationError):
                build_static_intelligence(
                    output_dir=tmp_dir,
                    events=[],
                    as_of=AS_OF,
                    release_id="../../escape",
                )

            with self.assertRaises(IntelligenceValidationError):
                build_static_intelligence(
                    output_dir=tmp_dir,
                    events=[
                        {
                            "event_id": "evt-large",
                            "canonical_event_id": "evt-large",
                            "occurred_at": "2026-07-13T11:00:00Z",
                            "title": "x" * 5_000,
                            "topics": ["large"],
                        }
                    ],
                    as_of=AS_OF,
                    max_shard_bytes=512,
                )


if __name__ == "__main__":
    unittest.main()
