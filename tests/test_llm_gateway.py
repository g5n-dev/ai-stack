import unittest


from processor.llm_gateway import (
    BudgetExceeded,
    BudgetPolicy,
    InMemoryBudgetStore,
    InMemoryResponseCache,
    LLMGateway,
    ProviderResponse,
)


class FakeProvider:
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, *, purpose: str, payload: str, max_tokens: int) -> ProviderResponse:
        self.calls += 1
        return ProviderResponse(
            text=f"generated:{purpose}:{payload}",
            model="fake-model",
            input_tokens=10,
            output_tokens=5,
        )


class LLMGatewayTest(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = FakeProvider()
        self.store = InMemoryBudgetStore()
        self.cache = InMemoryResponseCache()
        self.gateway = LLMGateway(
            provider=self.provider,
            budget_store=self.store,
            cache=self.cache,
            policy=BudgetPolicy(
                max_calls_per_item=2,
                max_calls_per_run=3,
                max_calls_per_day=4,
                max_tokens_per_item=100,
                max_tokens_per_run=200,
                max_tokens_per_day=300,
            ),
        )

    def test_reserves_budget_before_provider_call(self) -> None:
        response = self.gateway.generate(
            run_id="run-1",
            item_id="item-1",
            purpose="draft",
            payload="input",
            model="fake-model",
            prompt_version="p1",
            policy_version="policy1",
            max_tokens=20,
        )

        self.assertEqual(response.text, "generated:draft:input")
        reservations = self.store.reservations()
        self.assertEqual(len(reservations), 1)
        self.assertEqual(reservations[0].status, "reconciled")
        self.assertEqual(reservations[0].actual_tokens, 15)

    def test_cache_hit_uses_no_budget_and_no_provider_call(self) -> None:
        kwargs = {
            "run_id": "run-1",
            "item_id": "item-1",
            "purpose": "draft",
            "payload": "input",
            "model": "fake-model",
            "prompt_version": "p1",
            "policy_version": "policy1",
            "max_tokens": 20,
        }
        first = self.gateway.generate(**kwargs)
        second = self.gateway.generate(**kwargs)

        self.assertEqual(first.text, second.text)
        self.assertEqual(self.provider.calls, 1)
        self.assertEqual(len(self.store.reservations()), 1)
        self.assertTrue(second.cache_hit)

    def test_budget_is_rejected_before_provider_call(self) -> None:
        for purpose in ("one", "two"):
            self.gateway.generate(
                run_id="run-1",
                item_id="item-1",
                purpose=purpose,
                payload=purpose,
                model="fake-model",
                prompt_version="p1",
                policy_version="policy1",
                max_tokens=20,
            )

        with self.assertRaises(BudgetExceeded):
            self.gateway.generate(
                run_id="run-1",
                item_id="item-1",
                purpose="three",
                payload="three",
                model="fake-model",
                prompt_version="p1",
                policy_version="policy1",
                max_tokens=20,
            )

        self.assertEqual(self.provider.calls, 2)

    def test_provider_failure_keeps_reservation_consumed(self) -> None:
        class FailingProvider:
            def generate(self, *, purpose: str, payload: str, max_tokens: int) -> ProviderResponse:
                raise TimeoutError("unknown provider outcome")

        gateway = LLMGateway(
            provider=FailingProvider(),
            budget_store=self.store,
            cache=self.cache,
            policy=self.gateway.policy,
        )

        with self.assertRaises(TimeoutError):
            gateway.generate(
                run_id="run-2",
                item_id="item-2",
                purpose="draft",
                payload="input",
                model="fake-model",
                prompt_version="p1",
                policy_version="policy1",
                max_tokens=20,
            )

        self.assertEqual(self.store.reservations()[-1].status, "unknown")


if __name__ == "__main__":
    unittest.main()
