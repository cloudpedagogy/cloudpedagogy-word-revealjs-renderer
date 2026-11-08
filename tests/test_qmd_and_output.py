import tempfile
import unittest
from pathlib import Path

from word_to_revealjs import (
    reveal_yaml,
    write_quarto_yml,
    write_qa_report,
    write_reveal_output,
    SourceDoc,
    Section,
    ImageRecord,
)


class TestQmdAndOutput(unittest.TestCase):
    def test_reveal_yaml(self):
        yaml_str = reveal_yaml("My Title", theme="solarized")
        self.assertIn('title: "My Title"', yaml_str)
        self.assertIn("theme: solarized", yaml_str)
        self.assertIn("format:\n  revealjs:", yaml_str)

    def test_write_quarto_yml(self):
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            write_quarto_yml(out_dir)
            yml_file = out_dir / "_quarto.yml"
            self.assertTrue(yml_file.is_file())
            content = yml_file.read_text(encoding="utf-8")
            self.assertIn("type: website", content)
            self.assertIn("- media/**", content)

    def test_write_qa_report(self):
        doc = SourceDoc(
            source_path=Path("Test.docx"),
            source_name="Test.docx",
            source_stem="Test",
            title="Test Doc",
            safe_title="Test",
            output_folder="Test",
            media_subdir="media/test",
            media_files=[],
            sections=[Section(title="Intro", elements=["<p>Hello</p>"])],
            detected_headings=["H1: Test Doc", "H2: Intro"],
            image_records=[ImageRecord(filename="img1.png", src="media/test/img1.png", alt="Alt text")],
            messages=["Conversion message"],
            qa_findings=["Minor finding"],
        )
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            qmd_path = out_dir / "Test_slides.qmd"
            write_qa_report(doc, out_dir, qmd_path)

            qa_file = out_dir / "qa_report_revealjs.md"
            self.assertTrue(qa_file.is_file())
            content = qa_file.read_text(encoding="utf-8")
            self.assertIn("Test.docx", content)
            self.assertIn("Slides generated: 1", content)
            self.assertIn("Images extracted: 1", content)
            self.assertIn("Minor finding", content)
            self.assertIn("Conversion message", content)


if __name__ == "__main__":
    unittest.main()

