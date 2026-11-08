import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestCli(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script_path = Path(__file__).resolve().parent.parent / "word_to_revealjs.py"
        cls.fixture_path = Path(__file__).resolve().parent.parent / "Vaccine_Effectiveness_Slide_Test.docx"

    def test_cli_missing_input_returns_nonzero(self):
        result = subprocess.run(
            [sys.executable, str(self.script_path), "--input-glob", "non_existent_path/**/*.docx"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("No DOCX files found.", result.stderr)

    def test_cli_corrupt_docx_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as td:
            bad_docx = Path(td) / "corrupt.docx"
            bad_docx.write_text("This is not a zip or docx file", encoding="utf-8")
            out_dir = Path(td) / "out"

            result = subprocess.run(
                [
                    sys.executable,
                    str(self.script_path),
                    "--input-glob",
                    str(bad_docx),
                    "--output-dir",
                    str(out_dir),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Error:", result.stderr)

    def test_cli_successful_run_without_render(self):
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            result = subprocess.run(
                [
                    sys.executable,
                    str(self.script_path),
                    "--input-glob",
                    str(self.fixture_path),
                    "--output-dir",
                    str(out_dir),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Done.", result.stdout)
            self.assertIn("Slides: 7", result.stdout)
            self.assertIn("Images: 1", result.stdout)

            expected_qmd = out_dir / "Vaccine_Effectiveness_Slide_Test" / "Vaccine_Effectiveness_Slide_Test_slides.qmd"
            self.assertTrue(expected_qmd.is_file())


if __name__ == "__main__":
    unittest.main()

