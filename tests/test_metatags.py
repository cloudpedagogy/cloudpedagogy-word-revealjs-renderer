import unittest

from word_to_revealjs import (
    youtube_embed_url,
    extract_panopto_id,
    panopto_embed_url,
    process_metatags,
    iframe_block,
)


class TestMetatags(unittest.TestCase):
    def test_youtube_embed_url(self):
        # Standard watch URL
        self.assertEqual(
            youtube_embed_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
        )
        # Short URL
        self.assertEqual(
            youtube_embed_url("https://youtu.be/dQw4w9WgXcQ"),
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
        )
        # Embed URL
        self.assertEqual(
            youtube_embed_url("https://www.youtube.com/embed/dQw4w9WgXcQ"),
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
        )
        # Query parameters preceding 'v='
        self.assertEqual(
            youtube_embed_url("https://www.youtube.com/watch?feature=shared&v=dQw4w9WgXcQ"),
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
        )
        # Query parameters after 'v='
        self.assertEqual(
            youtube_embed_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s"),
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
        )
        # Invalid URL
        self.assertIsNone(youtube_embed_url("https://notyoutube.com/video/123"))

    def test_panopto_embed_url(self):
        viewer_url = "https://example.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=d19ba573-9ad1-480b-95db-b3ed01014aab"
        expected_embed = "https://example.cloud.panopto.eu/Panopto/Pages/Embed.aspx?id=d19ba573-9ad1-480b-95db-b3ed01014aab"
        self.assertEqual(panopto_embed_url(viewer_url), expected_embed)

        embed_url = "https://example.cloud.panopto.eu/Panopto/Pages/Embed.aspx?id=d19ba573-9ad1-480b-95db-b3ed01014aab"
        self.assertEqual(panopto_embed_url(embed_url), embed_url)

        # Invalid URL without ID
        self.assertIsNone(panopto_embed_url("https://example.com/no_id"))
        # Non-http scheme
        self.assertIsNone(panopto_embed_url("javascript:alert(1)?id=123"))

    def test_iframe_block_security(self):
        # Valid URL
        res = iframe_block("https://example.com/embed")
        self.assertIn("https://example.com/embed", res)
        self.assertIn("<iframe", res)

        # Malicious javascript: URL blocked
        blocked = iframe_block("javascript:alert('xss')")
        self.assertIn("Invalid iframe URL", blocked)
        self.assertNotIn("<iframe", blocked)

    def test_process_metatags_youtube(self):
        # Simple text form
        text1 = "<p>YouTubeEmbed :: https://www.youtube.com/watch?v=abc123xyz</p>"
        res1 = process_metatags(text1)
        self.assertIn("https://www.youtube.com/embed/abc123xyz", res1)
        self.assertIn("```{=html}", res1)

        # Hyperlinked text form
        text2 = '<p>YouTubeEmbed :: <a href="https://www.youtube.com/watch?v=abc123xyz">https://www.youtube.com/watch?v=abc123xyz</a></p>'
        res2 = process_metatags(text2)
        self.assertIn("https://www.youtube.com/embed/abc123xyz", res2)

        # Bracket-style plain text (split paragraph)
        text3 = "<p>[YOUTUBE]</p>\n<p>https://youtu.be/abc123xyz</p>"
        res3 = process_metatags(text3)
        self.assertIn("https://www.youtube.com/embed/abc123xyz", res3)

        # Bracket-style plain text (single paragraph)
        text4 = "<p>[YOUTUBE] https://youtu.be/abc123xyz</p>"
        res4 = process_metatags(text4)
        self.assertIn("https://www.youtube.com/embed/abc123xyz", res4)

        # Bracket-style hyperlink (split paragraph)
        text5 = '<p>[YOUTUBE]</p>\n<p><a href="https://youtu.be/abc123xyz">https://youtu.be/abc123xyz</a></p>'
        res5 = process_metatags(text5)
        self.assertIn("https://www.youtube.com/embed/abc123xyz", res5)

        # Bracket-style hyperlink (single paragraph)
        text6 = '<p>[YOUTUBE] <a href="https://youtu.be/abc123xyz">https://youtu.be/abc123xyz</a></p>'
        res6 = process_metatags(text6)
        self.assertIn("https://www.youtube.com/embed/abc123xyz", res6)

    def test_process_metatags_iframe(self):
        # IFrame plain text
        text1 = "<p>IFrameEmbed :: https://example.com/interactive</p>"
        res1 = process_metatags(text1)
        self.assertIn("https://example.com/interactive", res1)

        # IFrame bracket plain text
        text2 = "<p>[IFRAME]</p>\n<p>https://example.com/interactive</p>"
        res2 = process_metatags(text2)
        self.assertIn("https://example.com/interactive", res2)

        # IFrame bracket hyperlinked
        text3 = '<p>[IFRAME]</p>\n<p><a href="https://example.com/interactive">Click here</a></p>'
        res3 = process_metatags(text3)
        self.assertIn("https://example.com/interactive", res3)

    def test_process_metatags_panopto(self):
        url = "https://lshtm.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=d19ba573-9ad1-480b-95db-b3ed01014aab"
        # PanoptoEmbed :: plain text
        text1 = f"<p>PanoptoEmbed :: {url}</p>"
        res1 = process_metatags(text1)
        self.assertIn("Embed.aspx?id=d19ba573-9ad1-480b-95db-b3ed01014aab", res1)

        # Panopto bracket form
        text2 = f"<p>[PANOPTO]</p>\n<p>{url}</p>"
        res2 = process_metatags(text2)
        self.assertIn("Embed.aspx?id=d19ba573-9ad1-480b-95db-b3ed01014aab", res2)


if __name__ == "__main__":
    unittest.main()

