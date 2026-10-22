from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent.parent


class PublicText(HTMLParser):
    ignored_tags = {"button", "form", "script", "style", "svg"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ignored = []
        self.parts = []
        self.in_body = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "body":
            self.in_body = True
        if (
            tag in self.ignored_tags
            or "hidden" in attributes
            or attributes.get("aria-hidden") == "true"
        ):
            self.ignored.append(tag)

    def handle_endtag(self, tag):
        if self.ignored and tag == self.ignored[-1]:
            self.ignored.pop()
        if tag == "body":
            self.in_body = False

    def handle_data(self, data):
        if self.in_body and not self.ignored:
            self.parts.append(data)


class BuildSiteTest(unittest.TestCase):
    def test_generated_markdown_contains_public_landing_text_and_links(self):
        subprocess.run([sys.executable, "scripts/build-site.py"], cwd=ROOT, check=True)
        parser = PublicText()
        parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        markdown = (ROOT / "dist/llms.txt").read_text(encoding="utf-8")

        for text in parser.parts:
            normalized_text = " ".join(text.split()).casefold()
            if normalized_text:
                self.assertIn(normalized_text, markdown.casefold())
        self.assertIn("https://wa.me/56978505946", markdown)
        self.assertIn("/contacto", markdown)
        self.assertIn("/llms.txt", markdown)
        for text in (
            "Sin instalar nada",
            "se abre desde el celular",
            "Tú defines el beneficio",
            "y cuántas compras pide",
        ):
            self.assertIn(text.casefold(), markdown.casefold())


if __name__ == "__main__":
    unittest.main()
