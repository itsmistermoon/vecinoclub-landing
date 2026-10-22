from html.parser import HTMLParser
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"


class LandingMarkdown(HTMLParser):
    ignored_tags = {"button", "form", "script", "style", "svg"}
    block_tags = {
        "article",
        "div",
        "footer",
        "h1",
        "h2",
        "h3",
        "header",
        "li",
        "main",
        "p",
        "section",
    }
    content_tags = {"body", "footer", "header", "main"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.content_depth = 0
        self.ignored_stack = []
        self.blocks = []
        self.current_tag = None
        self.current_parts = []
        self.items = []
        self.links = []
        self.link_stack = []
        self.reward_json = []
        self.capture_rewards = False

    def flush(self):
        value = " ".join(" ".join(self.current_parts).split())
        if value:
            self.items.append((self.current_tag, value))
        self.current_parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "script" and attributes.get("id") == "reward-businesses":
            self.capture_rewards = True
            return
        if tag in self.content_tags:
            self.content_depth += 1
        if not self.content_depth:
            return
        if self.ignored_stack:
            if tag in self.ignored_tags:
                self.ignored_stack.append(tag)
            return
        if (
            tag in self.ignored_tags
            or "hidden" in attributes
            or attributes.get("aria-hidden") == "true"
        ):
            self.ignored_stack.append(tag)
            return
        if tag == "a":
            self.link_stack.append({"href": attributes.get("href", ""), "parts": []})
        if tag in self.block_tags:
            self.flush()
            self.blocks.append(tag)
            self.current_tag = tag

    def handle_endtag(self, tag):
        if tag == "script" and self.capture_rewards:
            self.capture_rewards = False
            return
        if self.ignored_stack:
            if tag == self.ignored_stack[-1]:
                self.ignored_stack.pop()
            return
        if tag == "a" and self.link_stack:
            link = self.link_stack.pop()
            text = " ".join(" ".join(link["parts"]).split())
            if text and link["href"]:
                self.links.append((text, link["href"]))
        if tag in self.block_tags and self.blocks:
            self.flush()
            if tag in self.blocks:
                self.blocks.remove(tag)
            self.current_tag = self.blocks[-1] if self.blocks else None
        if tag in self.content_tags and self.content_depth:
            self.content_depth -= 1

    def handle_data(self, data):
        if self.capture_rewards:
            self.reward_json.append(data)
            return
        if self.content_depth and not self.ignored_stack:
            self.current_parts.append(data)
            for link in self.link_stack:
                link["parts"].append(data)


def make_markdown():
    parser = LandingMarkdown()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    lines = []
    for tag, text in parser.items:
        if tag == "h1":
            lines.extend([f"# {text}", ""])
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
            lines.extend(
                [f"- **{reward['name']}:** {reward['description']} {details}.", ""]
            )
        else:
            lines.extend([f"- **{reward['name']}:** {reward['description']}", ""])
    if parser.links:
        lines.extend(["## Enlaces", ""])
        for text, href in parser.links:
            lines.extend([f"- [{text}]({href})", ""])
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
