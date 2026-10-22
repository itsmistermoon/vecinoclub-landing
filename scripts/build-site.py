from html.parser import HTMLParser
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"


class LandingMarkdown(HTMLParser):
    ignored_tags = {"a", "article", "button", "form", "script", "style", "svg"}
    block_tags = {"h1", "h2", "h3", "p", "li"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.ignored_depth = 0
        self.block = None
        self.items = []
        self.reward_json = []
        self.capture_rewards = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "script" and attributes.get("id") == "reward-businesses":
            self.capture_rewards = True
            return
        if tag == "main":
            self.depth += 1
        if not self.depth:
            return
        if tag in self.ignored_tags:
            self.ignored_depth += 1
        if not self.ignored_depth and tag in self.block_tags:
            self.block = (tag, [])

    def handle_endtag(self, tag):
        if tag == "script" and self.capture_rewards:
            self.capture_rewards = False
            return
        if self.depth and not self.ignored_depth and tag in self.block_tags and self.block:
            block_tag, parts = self.block
            if block_tag == tag:
                value = " ".join(" ".join(parts).split())
                if value:
                    self.items.append((tag, value))
                self.block = None
        if self.depth and tag in self.ignored_tags and self.ignored_depth:
            self.ignored_depth -= 1
        if tag == "main" and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.capture_rewards:
            self.reward_json.append(data)
            return
        if self.depth and not self.ignored_depth and self.block:
            self.block[1].append(data)


def make_markdown():
    parser = LandingMarkdown()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    lines = [
        "# VecinoClub",
        "",
        "Información de la landing pública de VecinoClub, fidelización para comercios locales de Chile.",
        "",
    ]
    for tag, text in parser.items:
        if tag == "h1":
            lines.extend([f"## {text}", ""])
        elif tag == "h2":
            lines.extend([f"## {text}", ""])
        elif tag == "h3":
            lines.extend([f"### {text}", ""])
        elif tag == "li":
            lines.extend([f"- {text}", ""])
        else:
            lines.extend([text, ""])
    rewards = json.loads("".join(parser.reward_json))
    lines.extend(["## Ejemplos de beneficios", ""])
    for reward in rewards:
        if reward["count"]:
            details = f"{reward['count']} {reward['unit']} para recibir {reward['prizeCount']} {reward['prize']}"
            lines.extend([f"- **{reward['name']}:** {reward['description']} {details}.", ""])
        else:
            lines.extend([f"- **{reward['name']}:** {reward['description']}", ""])
    lines.extend([
        "## Contacto",
        "",
        "[Escríbenos por WhatsApp](https://wa.me/56978505946) o [visita la página de contacto](https://vecinoclub.cl/contacto).",
        "",
    ])
    return "\n".join(lines)


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for name in ("index.html", "contacto.html", "styles.css", "assets", "fonts"):
        source = ROOT / name
        target = OUTPUT / name
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    (OUTPUT / "llms.txt").write_text(make_markdown(), encoding="utf-8")


if __name__ == "__main__":
    main()
