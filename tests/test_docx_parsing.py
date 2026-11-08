import tempfile
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

from word_to_revealjs import (
    clean_soup,
    normalise_text,
    safe_filename,
    split_into_sections,
    parse_docx,
    SourceDoc,
    Section,
)


class TestDocxParsing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_path = Path(__file__).resolve().parent.parent / "Vaccine_Effectiveness_Slide_Test.docx"
        if not cls.fixture_path.is_file():
            raise FileNotFoundError(f"Fixture not found: {cls.fixture_path}")

    def test_safe_filename(self):
        self.assertEqual(safe_filename("Vaccine Effectiveness"), "Vaccine_Effectiveness")
        self.assertEqual(safe_filename("  test @#$ doc  "), "test_doc")
        self.assertEqual(safe_filename(""), "untitled")
        self.assertEqual(safe_filename("___"), "untitled")

    def test_normalise_text(self):
        self.assertEqual(normalise_text("  hello   world  \n\t "), "hello world")
        self.assertEqual(normalise_text(""), "")

    def test_clean_soup_table_and_empty_paragraphs(self):
        html_input = (
            "<body>"
            "<p>   </p>"
            "<p>Valid text</p>"
            "<table><tr><td>Cell 1</td></tr></table>"
            "</body>"
        )
        soup = BeautifulSoup(html_input, "html.parser")
        clean_soup(soup)
        p_tags = soup.find_all("p")
        self.assertEqual(len(p_tags), 1)
        self.assertEqual(p_tags[0].get_text(), "Valid text")

        table = soup.find("table")
        self.assertEqual(table.get("border"), "1")
        self.assertEqual(table.get("cellpadding"), "6")

    def test_split_into_sections(self):
        html_input = (
            "<body>"
            "<h1>My Presentation</h1>"
            "<h2>Slide One</h2>"
            "<p>Paragraph in slide one</p>"
            "<h2>Slide Two</h2>"
            "<p>Paragraph in slide two</p>"
            "</body>"
        )
        soup = BeautifulSoup(html_input, "html.parser")
        title, sections, headings = split_into_sections(soup, slide_heading_level="h2")
        self.assertEqual(title, "My Presentation")
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].title, "Slide One")
        self.assertEqual(len(sections[0].elements), 1)
        self.assertEqual(sections[1].title, "Slide Two")
        self.assertEqual(len(headings), 3)

    def test_parse_docx_reference_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            media_work = Path(td) / "_media_work"
            media_work.mkdir()
            doc = parse_docx(self.fixture_path, media_work, "h2")

            self.assertIsInstance(doc, SourceDoc)
            self.assertEqual(doc.title, "Introduction to Vaccine Effectiveness")
            self.assertEqual(doc.safe_title, "Vaccine_Effectiveness_Slide_Test")
            self.assertEqual(len(doc.sections), 7)
            self.assertEqual(len(doc.image_records), 1)
            self.assertEqual(len(doc.media_files), 1)
            self.assertTrue(doc.media_files[0].is_file())

            # Verify image record attributes
            img = doc.image_records[0]
            self.assertEqual(img.filename, "image_001.png")
            self.assertTrue("vaccine_effectiveness_slide_test" in img.src)


if __name__ == "__main__":
    unittest.main()

