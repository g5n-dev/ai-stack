#!/usr/bin/env python3

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = ROOT / "blog" / "themes" / "terminal-theme" / "layouts"
SHARED_HEADER = '{{ partial "site-header.html" . }}'
SHARED_HEAD = '{{ partial "site-head.html"'


class SiteHeaderContractTest(unittest.TestCase):
    @staticmethod
    def _css_rule(source: str, selector: str) -> str:
        matches = re.findall(rf"{re.escape(selector)}\s*\{{([^}}]+)\}}", source)
        if not matches:
            raise AssertionError(f"missing CSS rule: {selector}")
        return "\n".join(matches)

    def test_every_user_facing_document_uses_one_shared_header(self) -> None:
        documents: list[tuple[Path, str]] = []
        for path in sorted(LAYOUTS.rglob("*.html")):
            source = path.read_text(encoding="utf-8")
            if "<!DOCTYPE" in source.upper() and "<body" in source:
                documents.append((path, source))

        self.assertGreaterEqual(len(documents), 12)
        for path, source in documents:
            with self.subTest(template=path.relative_to(LAYOUTS).as_posix()):
                self.assertEqual(source.count(SHARED_HEADER), 1)
                self.assertNotIn('class="site-header"', source)

    def test_taxonomy_wrappers_delegate_to_documents_with_shared_header(self) -> None:
        wrappers = {
            "categories/taxonomy.html": "compact-taxonomy.html",
            "categories/term.html": "compact-term.html",
            "tags/taxonomy.html": "compact-taxonomy.html",
            "tags/term.html": "compact-term.html",
        }
        for relative_path, partial in wrappers.items():
            with self.subTest(template=relative_path):
                source = (LAYOUTS / relative_path).read_text(encoding="utf-8")
                self.assertEqual(source.strip(), f'{{{{ partial "{partial}" . }}}}')

    def test_every_document_loads_the_shared_head_contract(self) -> None:
        """The header must always receive the same reset and canonical stylesheet."""
        for path in sorted(LAYOUTS.rglob("*.html")):
            source = path.read_text(encoding="utf-8")
            if "<!DOCTYPE" not in source.upper() or "<body" not in source:
                continue

            with self.subTest(template=path.relative_to(LAYOUTS).as_posix()):
                self.assertEqual(source.count(SHARED_HEAD), 1)
                self.assertNotIn('href="/css/style.css"', source)
                self.assertNotIn('href="/css/tailwind.css"', source)

    def test_page_specific_styles_cannot_override_the_shared_header(self) -> None:
        """Only style.css owns header geometry and typography."""
        css_root = ROOT / "blog" / "static" / "css"
        for path in sorted(css_root.glob("*.css")):
            if path.name == "style.css":
                continue
            with self.subTest(stylesheet=path.name):
                self.assertNotIn(
                    ".site-header",
                    path.read_text(encoding="utf-8"),
                )

        for path in sorted(LAYOUTS.rglob("*.html")):
            source = path.read_text(encoding="utf-8")
            if "<style" not in source:
                continue
            with self.subTest(template=path.relative_to(LAYOUTS).as_posix()):
                self.assertNotIn(".site-header", source)

    def test_page_effects_do_not_wrap_or_mutate_the_shared_header(self) -> None:
        not_found = (LAYOUTS / "404.html").read_text(encoding="utf-8")
        effect_class = re.search(
            r'class="[^"]*\bcrt-flicker\b[^"]*"',
            not_found,
        )

        self.assertIsNotNone(effect_class)
        self.assertLess(
            not_found.index(SHARED_HEADER),
            effect_class.start(),  # type: ignore[union-attr]
            "404 flicker must begin below the shared header",
        )

    def test_shared_header_has_one_brand_navigation_and_live_telemetry(self) -> None:
        source = (LAYOUTS / "partials" / "site-header.html").read_text(
            encoding="utf-8"
        )
        stats = (LAYOUTS / "partials" / "site-stats.html").read_text(
            encoding="utf-8"
        )

        for contract in (
            "data-site-header",
            "data-site-brand",
            ".Site.Params.description",
            'aria-label="主导航"',
            ".Site.Home.RelPermalink",
            "site-header__telemetry",
            "data-site-clock",
            "条目",
            "延迟",
            "最新内容",
            "当前时间",
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, source)

        self.assertEqual(source.count("<header"), 1)
        self.assertEqual(source.count('aria-label="主导航"'), 1)
        self.assertNotIn("<small", source)
        self.assertNotIn("DATA LIVE", source)
        self.assertNotIn("SYS_STABLE", source)
        self.assertIn('.Date.Format "2006-01-02 15:04"', stats)
        self.assertNotIn('.Date.Format "15:04"', stats)

    def test_telemetry_uses_shared_two_row_baseline_grid(self) -> None:
        css = (ROOT / "blog" / "static" / "css" / "style.css").read_text(
            encoding="utf-8"
        )

        for token in (
            "--site-header-height: 64px",
            "--site-font-sans:",
            "--site-font-mono:",
            "--site-header-telemetry-label-row:",
            "--site-header-telemetry-value-row:",
        ):
            with self.subTest(token=token):
                self.assertIn(token, css)

        telemetry = css[
            css.index(".site-header__telemetry>div") : css.index(
                ".site-header__nav"
            )
        ]
        self.assertIn("grid-template-rows:", telemetry)
        self.assertIn("var(--site-header-telemetry-label-row)", telemetry)
        self.assertIn("var(--site-header-telemetry-value-row)", telemetry)
        self.assertNotIn("telemetry-note-row", telemetry)
        self.assertIn("align-content: center", telemetry)

    def test_header_geometry_and_type_scale_match_on_every_page(self) -> None:
        css = (ROOT / "blog" / "static" / "css" / "style.css").read_text(
            encoding="utf-8"
        )
        expected_declarations = {
            ".site-header": (
                "height: var(--site-header-height)",
                "padding: 0 var(--site-page-gutter)",
                "font-family: var(--site-font-sans)",
            ),
            ".site-header__title": ("font-size: 17px", "line-height: 1"),
            ".site-header__telemetry dt": ("font-size: 10px",),
            ".site-header__telemetry dd": ("font-size: 11px",),
            ".site-header__nav a": ("font-size: var(--site-control-size)", "min-height: 44px"),
            ".site-header__secure": ("font-size: 10px",),
        }

        for selector, declarations in expected_declarations.items():
            rule = self._css_rule(css, selector)
            for declaration in declarations:
                with self.subTest(selector=selector, declaration=declaration):
                    self.assertIn(declaration, rule)

    def test_graph_and_site_share_the_same_font_tokens(self) -> None:
        shared_css = (ROOT / "blog" / "static" / "css" / "style.css").read_text(
            encoding="utf-8"
        )
        graph_css = (ROOT / "blog" / "static" / "css" / "graph.css").read_text(
            encoding="utf-8"
        )

        self.assertIn("font-family: var(--site-font-sans)", shared_css)
        self.assertIn("--graph-sans: var(--site-font-sans)", graph_css)
        self.assertIn("--graph-mono: var(--site-font-mono)", graph_css)
        self.assertNotIn("--graph-sans: Inter", graph_css)

    def test_small_header_copy_keeps_accessible_contrast(self) -> None:
        css = (ROOT / "blog" / "static" / "css" / "style.css").read_text(
            encoding="utf-8"
        )

        self.assertIn("color: rgba(var(--muted-teal), 0.84);", css)
        self.assertIn("color: rgba(var(--off-white), 0.64);", css)
        self.assertNotIn("color: rgba(var(--muted-teal), 0.52);", css)
        self.assertNotIn("color: rgba(var(--off-white), 0.34);", css)

    def test_header_runtime_is_singleton_and_subpath_safe(self) -> None:
        partial = (LAYOUTS / "partials" / "site-header.html").read_text(
            encoding="utf-8"
        )
        runtime = (ROOT / "blog" / "static" / "js" / "site-header.js").read_text(
            encoding="utf-8"
        )

        self.assertIn('"js/site-header.js" | relURL', partial)
        self.assertIn('clock.dataset.siteClockReady === "true"', runtime)
        self.assertIn('menuButton.dataset.siteMenuReady !== "true"', runtime)
        self.assertIn('document.addEventListener("visibilitychange"', runtime)
        self.assertIn("hasPrefix $currentPath $targetPath", partial)

    def test_main_navigation_keeps_the_product_order(self) -> None:
        config = (ROOT / "blog" / "config.toml").read_text(encoding="utf-8")
        positions = [
            config.index(f'name = "{label}"')
            for label in ("首页", "归档", "搜索", "标签", "趋势", "图谱", "关于")
        ]
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
