import shutil
import tempfile
import unittest
from pathlib import Path

from word_to_revealjs import parse_docx, write_reveal_output


class TestReferenceParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent
        cls.fixture_path = cls.repo_root / "Vaccine_Effectiveness_Slide_Test.docx"
        cls.reference_dir = cls.repo_root / "output" / "presentations" / "Vaccine_Effectiveness_Slide_Test"

    def test_seven_slide_qmd_and_qa_parity(self):
        with tempfile.TemporaryDirectory() as td:
            output_root = Path(td)
            media_work = output_root / "_media_work"
            media_work.mkdir()

            doc = parse_docx(self.fixture_path, media_work, "h2")
            self.assertEqual(len(doc.sections), 7, "Reference docx must yield exactly 7 slides")

            qmd_path = write_reveal_output(doc, output_root, media_work, "simple", render=False)

            # Compare generated QMD against tracked reference
            gen_qmd = qmd_path.read_text(encoding="utf-8")
            ref_qmd = (self.reference_dir / "Vaccine_Effectiveness_Slide_Test_slides.qmd").read_text(encoding="utf-8")
            self.assertEqual(gen_qmd, ref_qmd, "Generated QMD must match reference QMD byte-for-byte")

            # Compare generated QA report against tracked reference
            gen_qa = (qmd_path.parent / "qa_report_revealjs.md").read_text(encoding="utf-8")
            ref_qa = (self.reference_dir / "qa_report_revealjs.md").read_text(encoding="utf-8")
            self.assertEqual(gen_qa, ref_qa, "Generated QA report must match reference QA report byte-for-byte")

            # Compare _quarto.yml
            gen_yml = (qmd_path.parent / "_quarto.yml").read_text(encoding="utf-8")
            ref_yml = (self.reference_dir / "_quarto.yml").read_text(encoding="utf-8")
            self.assertEqual(gen_yml, ref_yml, "Generated _quarto.yml must match reference _quarto.yml byte-for-byte")

            # Compare extracted media
            gen_media = qmd_path.parent / "media" / "vaccine_effectiveness_slide_test" / "image_001.png"
            ref_media = self.reference_dir / "media" / "vaccine_effectiveness_slide_test" / "image_001.png"
            self.assertTrue(gen_media.is_file())
            self.assertEqual(gen_media.read_bytes(), ref_media.read_bytes(), "Extracted image must match reference image byte-for-byte")

    def test_quarto_html_render_parity(self):
        if not shutil.which("quarto"):
            self.skipTest("Quarto CLI is not installed on system PATH")

        with tempfile.TemporaryDirectory() as td:
            output_root = Path(td)
            media_work = output_root / "_media_work"
            media_work.mkdir()

            doc = parse_docx(self.fixture_path, media_work, "h2")
            qmd_path = write_reveal_output(doc, output_root, media_work, "simple", render=True)

            gen_html = (qmd_path.parent / "_site" / "Vaccine_Effectiveness_Slide_Test_slides.html").read_text(encoding="utf-8")
            ref_html = (self.reference_dir / "_site" / "Vaccine_Effectiveness_Slide_Test_slides.html").read_text(encoding="utf-8")

            self.assertEqual(gen_html, ref_html, "Quarto rendered HTML must match reference HTML byte-for-byte")


if __name__ == "__main__":
    unittest.main()

