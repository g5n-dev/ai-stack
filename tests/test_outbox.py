import unittest

from publisher.outbox import (
    InMemoryOutboxStore,
    OutboxDispatcher,
    OutboxRecord,
    PublishResult,
)


class OutboxTest(unittest.TestCase):
    def test_successful_message_is_not_sent_twice(self) -> None:
        calls: list[str] = []

        def sender(payload: str, idempotency_key: str) -> PublishResult:
            calls.append(payload)
            return PublishResult.sent(provider_message_id="message-1")

        store = InMemoryOutboxStore()
        dispatcher = OutboxDispatcher(store=store, sender=sender)
        key = dispatcher.enqueue(
            event_revision="event-1:rev-1",
            platform="telegram",
            template_version="v1",
            payload="hello",
        )

        first = dispatcher.dispatch(key)
        second = dispatcher.dispatch(key)

        self.assertEqual(first.status, "sent")
        self.assertEqual(second.status, "sent")
        self.assertEqual(calls, ["hello"])
        self.assertEqual(second.provider_message_id, "message-1")

    def test_unknown_outcome_is_not_blindly_retried(self) -> None:
        calls = 0

        def sender(payload: str, idempotency_key: str) -> PublishResult:
            nonlocal calls
            calls += 1
            return PublishResult.unknown("timeout_after_send")

        store = InMemoryOutboxStore()
        dispatcher = OutboxDispatcher(store=store, sender=sender)
        key = dispatcher.enqueue(
            event_revision="event-1:rev-1",
            platform="twitter",
            template_version="v1",
            payload="hello",
        )

        first = dispatcher.dispatch(key)
        second = dispatcher.dispatch(key)

        self.assertEqual(first.status, "unknown")
        self.assertEqual(second.status, "unknown")
        self.assertEqual(calls, 1)

    def test_idempotency_key_covers_revision_platform_and_template(self) -> None:
        store = InMemoryOutboxStore()
        dispatcher = OutboxDispatcher(
            store=store,
            sender=lambda payload, idempotency_key: PublishResult.sent("id"),
        )

        first = dispatcher.enqueue("event:rev1", "telegram", "v1", "one")
        same = dispatcher.enqueue("event:rev1", "telegram", "v1", "one")
        changed = dispatcher.enqueue("event:rev2", "telegram", "v1", "two")

        self.assertEqual(first, same)
        self.assertNotEqual(first, changed)
        self.assertEqual(len(store.records()), 2)

    def test_retryable_failure_can_retry_then_succeed(self) -> None:
        calls = 0

        def sender(payload: str, idempotency_key: str) -> PublishResult:
            nonlocal calls
            calls += 1
            if calls == 1:
                return PublishResult.failed("temporary", retryable=True)
            return PublishResult.sent("message-2")

        dispatcher = OutboxDispatcher(store=InMemoryOutboxStore(), sender=sender)
        key = dispatcher.enqueue("event:rev", "telegram", "v1", "hello")

        self.assertEqual(dispatcher.dispatch(key).status, "failed")
        self.assertEqual(dispatcher.dispatch(key).status, "sent")
        self.assertEqual(calls, 2)

    def test_nonretryable_failure_moves_to_dead_letter_without_resend(self) -> None:
        calls = 0

        def sender(payload: str, idempotency_key: str) -> PublishResult:
            nonlocal calls
            calls += 1
            return PublishResult.failed("rejected", retryable=False)

        dispatcher = OutboxDispatcher(store=InMemoryOutboxStore(), sender=sender)
        key = dispatcher.enqueue("event:rev", "twitter", "v1", "hello")

        self.assertEqual(dispatcher.dispatch(key).status, "failed")
        self.assertEqual(dispatcher.dispatch(key).status, "dead_letter")
        self.assertEqual(calls, 1)

    def test_retry_limit_moves_to_dead_letter(self) -> None:
        dispatcher = OutboxDispatcher(
            store=InMemoryOutboxStore(),
            sender=lambda payload, key: PublishResult.failed("temporary", retryable=True),
            max_attempts=1,
        )
        key = dispatcher.enqueue("event:rev", "telegram", "v1", "hello")

        self.assertEqual(dispatcher.dispatch(key).status, "failed")
        self.assertEqual(dispatcher.dispatch(key).status, "dead_letter")

    def test_sender_exception_is_unknown_and_not_retried(self) -> None:
        calls = 0

        def sender(payload: str, idempotency_key: str) -> PublishResult:
            nonlocal calls
            calls += 1
            raise TimeoutError("outcome unknown")

        dispatcher = OutboxDispatcher(store=InMemoryOutboxStore(), sender=sender)
        key = dispatcher.enqueue("event:rev", "telegram", "v1", "hello")

        record = dispatcher.dispatch(key)
        self.assertEqual(record.status, "unknown")
        self.assertEqual(record.detail, "TimeoutError")
        dispatcher.dispatch(key)
        self.assertEqual(calls, 1)

    def test_store_rejects_collision_and_unknown_save(self) -> None:
        store = InMemoryOutboxStore()
        first = OutboxRecord("same-key", "event:rev", "telegram", "v1", "one")
        store.put_if_absent(first)

        with self.assertRaises(ValueError):
            store.put_if_absent(
                OutboxRecord("same-key", "event:rev", "telegram", "v1", "changed")
            )
        with self.assertRaises(KeyError):
            store.save(OutboxRecord("missing", "event:rev", "telegram", "v1", "one"))

    def test_publish_result_refuses_invalid_state(self) -> None:
        with self.assertRaises(ValueError):
            PublishResult(status="success")
        with self.assertRaises(ValueError):
            PublishResult(status="sent")


if __name__ == "__main__":
    unittest.main()
