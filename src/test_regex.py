import unittest
import regex

class TestRegex(unittest.TestCase):

    def test_eq(self):
            text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
            expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
            self.assertEqual(regex.extract_markdown_images(text), expected)

    def test_eq2(self):
            text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
            self.assertEqual(regex.extract_markdown_links(text), expected)
    