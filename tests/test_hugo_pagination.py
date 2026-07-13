#!/usr/bin/env python3

import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).parents[1]
THEMES_DIR = PROJECT_ROOT / "blog" / "themes"
PAGE_SIZE = 50
POST_COUNT = 121
FIXTURE_START = datetime(2025, 8, 31, 23, 0, tzinfo=timezone.utc)


class HugoPaginationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if shutil.which("hugo") is None:
            raise unittest.SkipTest("Hugo is not installed")

    def test_posts_and_archive_render_stable_fifty_item_pages(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            site = Path(tmp_dir)
            self._create_fixture_site(site)
            result = subprocess.run(
                [
                    "hugo",
                    "--source",
                    str(site),
                    "--destination",
                    str(site / "public"),
                    "--quiet",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            expected_counts = [50, 50, 21]
            expected_first_routes = [
                "/posts/post-120/",
                "/posts/post-070/",
                "/posts/post-020/",
            ]
            observed_routes = {}
            for section, marker in (
                ("posts", "data-entry-link"),
                ("archive", "data-archive-entry"),
            ):
                for page_number, (expected_count, expected_first) in enumerate(
                    zip(expected_counts, expected_first_routes),
                    start=1,
                ):
                    html_path = self._page_path(site / "public", section, page_number)
                    self.assertTrue(html_path.is_file(), html_path)
                    html = html_path.read_text(encoding="utf-8")
                    routes = re.findall(rf'{marker}="([^"]+)"', html)

                    self.assertEqual(len(routes), expected_count)
                    self.assertEqual(routes[0], expected_first)
                    self.assertEqual(len(routes), len(set(routes)))
                    self.assertIn(f'data-current-page="{page_number}"', html)
                    self.assertIn('data-total-pages="3"', html)
                    self.assertIn(
                        f'<link rel="canonical" href="https://fixture.example/{section}/'
                        + (f'page/{page_number}/' if page_number > 1 else "")
                        + '" />',
                        html,
                    )
                    observed_routes[(section, page_number)] = routes

            self.assertFalse((site / "public/posts/page/4/index.html").exists())
            self.assertFalse((site / "public/archive/page/4/index.html").exists())

            repeat = subprocess.run(
                [
                    "hugo",
                    "--source",
                    str(site),
                    "--destination",
                    str(site / "public-repeat"),
                    "--quiet",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(repeat.returncode, 0, repeat.stderr)
            for (section, page_number), expected_routes in observed_routes.items():
                html = self._page_path(
                    site / "public-repeat", section, page_number
                ).read_text(encoding="utf-8")
                marker = "data-entry-link" if section == "posts" else "data-archive-entry"
                self.assertEqual(
                    re.findall(rf'{marker}="([^"]+)"', html),
                    expected_routes,
                )

    @staticmethod
    def _page_path(public: Path, section: str, page_number: int) -> Path:
        if page_number == 1:
            return public / section / "index.html"
        return public / section / "page" / str(page_number) / "index.html"

    @staticmethod
    def _create_fixture_site(site: Path) -> None:
        (site / "content/posts").mkdir(parents=True)
        (site / "content/archive").mkdir(parents=True)
        (site / "layouts/_default").mkdir(parents=True)
        config = textwrap.dedent(
            f"""\
            baseURL = "https://fixture.example/"
            languageCode = "zh-CN"
            title = "Pagination Fixture"
            theme = "terminal-theme"
            themesDir = "{THEMES_DIR.as_posix()}"
            disableKinds = ["home", "taxonomy", "term", "RSS", "sitemap", "robotsTXT", "404"]

            [params]
            description = "pagination fixture"
            profile_image = "/img/profile-holo.png"

            [taxonomies]
            tag = "tags"
            category = "categories"
            scenario = "scenarios"
            """
        )
        (site / "hugo.toml").write_text(config, encoding="utf-8")
        (site / "content/archive/_index.md").write_text(
            textwrap.dedent(
                """\
                ---
                title: "Archive"
                layout: "archive"
                ---
                """
            ),
            encoding="utf-8",
        )
        (site / "layouts/_default/single.html").write_text(
            "<!doctype html><title>{{ .Title }}</title>",
            encoding="utf-8",
        )

        for index in range(POST_COUNT):
            published = FIXTURE_START + timedelta(minutes=index)
            body = textwrap.dedent(
                f"""\
                ---
                title: "Fixture Post {index:03d}"
                date: {published.isoformat()}
                draft: false
                source: fixture
                tags: ["fixture", "page-{index // PAGE_SIZE}"]
                ---

                Fixed pagination fixture {index:03d}.
                """
            )
            (site / f"content/posts/post-{index:03d}.md").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
