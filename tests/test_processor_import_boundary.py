from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run_isolated(source: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(ROOT), existing_pythonpath) if part
    )
    return subprocess.run(
        [sys.executable, "-c", textwrap.dedent(source)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        check=False,
        text=True,
    )


def test_deterministic_submodule_import_does_not_load_llm_runtime() -> None:
    result = _run_isolated(
        """
        import importlib.abc
        import sys

        class BlockAnthropic(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                if fullname == "anthropic" or fullname.startswith("anthropic."):
                    raise ModuleNotFoundError(
                        "anthropic blocked by import-boundary test",
                        name=fullname,
                    )
                return None

        sys.meta_path.insert(0, BlockAnthropic())

        from processor.stack_trends import verify_stack_trends

        assert callable(verify_stack_trends)
        for module_name in (
            "processor.anthropic_client",
            "processor.generator",
            "processor.main",
            "processor.summarizer",
            "processor.tagger",
            "processor.translator",
        ):
            assert module_name not in sys.modules, module_name
        """
    )

    assert result.returncode == 0, result.stderr


def test_public_processor_exports_remain_lazy_and_compatible() -> None:
    result = _run_isolated(
        """
        import importlib
        import sys

        import processor

        assert "processor.anthropic_client" not in sys.modules
        expected_exports = {
            "AnthropicClient": "processor.anthropic_client",
            "ContentSummarizer": "processor.summarizer",
            "ContentTranslator": "processor.translator",
            "ContentGenerator": "processor.generator",
            "ContentTagger": "processor.tagger",
            "ProcessorOrchestrator": "processor.main",
        }
        assert set(processor.__all__) == set(expected_exports)

        for export_name, module_name in expected_exports.items():
            exported = getattr(processor, export_name)
            module = importlib.import_module(module_name)
            assert exported is getattr(module, export_name)
        """
    )

    assert result.returncode == 0, result.stderr
