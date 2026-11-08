import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from word_to_revealjs import render_quarto, write_quarto_yml


class TestQuartoIntegration(unittest.TestCase):
    def test_missing_quarto_diagnostic(self):
        with tempfile.TemporaryDirectory() as td:
            qmd_path = Path(td) / "test_slides.qmd"
            qmd_path.write_text("---\ntitle: Test\nformat: revealjs\n---\n## S1\nText\n", encoding="utf-8")

            with patch("shutil.which", return_value=None):
                with self.assertRaises(RuntimeError) as ctx:
                    render_quarto(qmd_path)
                self.assertIn("Quarto is required for HTML rendering", str(ctx.exception))

    def test_render_quarto_success(self):
        if not shutil.which("quarto"):
            self.skipTest("Quarto CLI is not installed on system PATH")

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            write_quarto_yml(out_dir)
            qmd_path = out_dir / "sample_slides.qmd"
            qmd_path.write_text(
                "---\ntitle: Sample Presentation\nformat: revealjs\n---\n\n## Slide One\nHello world\n",
                encoding="utf-8",
            )
            render_quarto(qmd_path)

            site_dir = out_dir / "_site"
            self.assertTrue(site_dir.is_dir(), "_site directory must be created")
            html_file = site_dir / "sample_slides.html"
            self.assertTrue(html_file.is_file(), "Compiled Reveal.js HTML file must exist")
            content = html_file.read_text(encoding="utf-8")
            self.assertIn("Sample Presentation", content)
            self.assertIn("Slide One", content)


if __name__ == "__main__":
    unittest.main()

