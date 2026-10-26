from html.parser import HTMLParser
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"
IGNORED_TAGS = {"button", "footer", "form", "header", "nav", "script", "style", "svg"}
IGNORED_CLASSES = {"btn", "cta-row", "hero-visual", "reward-accordion", "sr-only"}
BLOCK_TAGS = {"b", "h1", "h2", "h3", "p", "span"}


class LandingContent(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.content_depth = 0
        self.ignored_stack = []
        self.current_tag = None
        self.current_parts = []
        self.facts_depth = 0
        self.blocks = []
        self.links = []
        self.reward_json = []
        self.capture_rewards = False
        self.site_url = ""
        self.intro = ""

    def flush(self):
        text = " ".join(" ".join(self.current_parts).split()).replace(" .", ".")
        if text and not (text.isdecimal() and len(text) == 2):
            self.blocks.append((self.current_tag, text))
        self.current_tag = None
        self.current_parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())

        if tag == "meta" and attributes.get("property") == "og:url":
            self.site_url = attributes.get("content", "").rstrip("/")

        if tag == "script" and attributes.get("id") == "reward-businesses":
            self.capture_rewards = True
            return
        if self.capture_rewards:
            return

        if self.content_depth == 0 and "data-llms-content" in attributes:
            self.content_depth = 1
            self.intro = attributes.get("data-llms-intro", "")
            return
        if not self.content_depth:
            return
        if self.ignored_stack:
            self.ignored_stack.append(tag)
            return

        if tag == "a":
            href = attributes.get("href", "")
            label = attributes.get("data-llms-label", "")
            if href.startswith("https://"):
                if label:
                    self.links.append((label, href))
            elif href.startswith("/"):
                if label:
                    self.links.append((label, f"{self.site_url}{href}"))

        if (
            tag in IGNORED_TAGS
            or classes.intersection(IGNORED_CLASSES)
            or "hidden" in attributes
            or attributes.get("aria-hidden") == "true"
            or attributes.get("role") == "tablist"
        ):
            self.flush()
            self.ignored_stack.append(tag)
            return

        if tag == "div" and self.facts_depth:
            self.facts_depth += 1
            return
        if tag == "div" and "facts" in classes:
            self.flush()
            self.current_tag = "fact"
            self.facts_depth = 1
            return

        if tag in BLOCK_TAGS and not self.facts_depth:
            self.flush()
            self.current_tag = tag

    def handle_endtag(self, tag):
        if tag == "script" and self.capture_rewards:
            self.capture_rewards = False
            return
        if self.ignored_stack:
            if tag in self.ignored_stack:
                del self.ignored_stack[len(self.ignored_stack) - 1 - self.ignored_stack[::-1].index(tag):]
            return
        if tag == "div" and self.facts_depth:
            self.facts_depth -= 1
            if self.facts_depth:
                self.current_parts.append(". ")
            else:
                self.flush()
        elif tag in BLOCK_TAGS and not self.facts_depth:
            self.flush()
        if tag == "main" and self.content_depth:
            self.content_depth = 0

    def handle_data(self, data):
        if self.capture_rewards:
            self.reward_json.append(data)
            return
        if self.content_depth and not self.ignored_stack and self.current_tag:
            self.current_parts.append(data)


def make_markdown():
    parser = LandingContent()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    lines = []
    rewards = json.loads("".join(parser.reward_json))
    has_illustrative_label = any("Ejemplos ilustrativos" in text for _, text in parser.blocks)

    def add_examples():
        if not rewards or not has_illustrative_label:
            return
        for reward in rewards:
            if not reward["count"]:
                continue
            detail = f"{reward['count']} {reward['unit']} para recibir {reward['prizeCount']} {reward['prize']}"
            lines.extend([f"- **{reward['name']}:** {reward['description']} {detail}.", ""])

    skip_next_heading = False
    for index, (tag, text) in enumerate(parser.blocks):
        if skip_next_heading:
            skip_next_heading = False
            continue
        if tag == "span" and index + 1 < len(parser.blocks) and parser.blocks[index + 1][0] == "h2":
            lines.extend([f"## {text}: {parser.blocks[index + 1][1]}", ""])
            skip_next_heading = True
            continue
        if tag == "h1":
            lines.extend([f"# {text}", ""])
            if parser.intro:
                lines.extend([parser.intro, ""])
        elif tag in {"h2", "h3"}:
            lines.extend([f"## {text}", ""])
        elif tag == "fact":
            lines.extend([f"{text.rstrip('.')}.", ""])
        else:
            lines.extend([text, ""])
        if tag == "p" and "Ejemplos ilustrativos" in text:
            add_examples()

    if parser.links:
        lines.extend(f"- [{label}]({href})" for label, href in dict.fromkeys(parser.links))
    return "\n".join(lines).strip() + "\n"


def build():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for name in ("index.html", "contacto.html", "styles.css", "assets", "fonts", "robots.txt"):
        source = ROOT / name
        target = OUTPUT / name
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    (OUTPUT / "llms.txt").write_text(make_markdown(), encoding="utf-8")


if __name__ == "__main__":
    build()
