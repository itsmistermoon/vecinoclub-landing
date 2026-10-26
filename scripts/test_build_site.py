from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent.parent


class BuildSiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/build-site.py"], cwd=ROOT, check=True)
        cls.markdown = (ROOT / "dist/llms.txt").read_text(encoding="utf-8")

    def test_contains_the_landing_claims_and_complete_contact_links(self):
        for phrase in (
            "Tu propio club de beneficios",
            "Fideliza a tus clientes con sellos y puntos en su celular",
            "Tu comercio vive de los clientes de siempre",
            "Para todo tipo de comercios",
            "Sin instalar nada",
            "se abre desde el celular",
            "Tú defines el beneficio",
            "y cuántas compras pide",
            "Tu cliente escanea",
            "Cada compra suma",
            "Cobra su beneficio",
            "Tú decides qué ofreces y cuántas compras pide",
            "Ejemplos ilustrativos",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.markdown)
        self.assertIn("https://wa.me/56978505946", self.markdown)
        self.assertIn("https://vecinoclub.cl/contacto", self.markdown)

    def test_starts_with_a_branded_description_and_site_address(self):
        self.assertIn(
            "# Tu propio club de beneficios.\n\nVecinoClub es un club de beneficios para comercios. Más información: https://vecinoclub.cl.",
            self.markdown,
        )

    def test_audience_context_joins_the_benefit_heading(self):
        self.assertIn("## Para todo tipo de comercios: Tú defines el beneficio", self.markdown)
        self.assertNotIn("\n\nPara todo tipo de comercios\n", self.markdown)

    def test_contact_links_are_labeled_from_the_html(self):
        self.assertIn("- [WhatsApp](https://wa.me/56978505946)", self.markdown)
        self.assertIn("- [Contacto](https://vecinoclub.cl/contacto)", self.markdown)
        self.assertNotIn("- <https://", self.markdown)

    def test_omits_interface_copy_decorative_numbers_and_hero_demo(self):
        for phrase in (
            "Saltar al contenido",
            "Navegación principal",
            "Cómo funciona",
            "Para quién",
            "01",
            "02",
            "03",
            "Conversemos",
            "Lo quiero en mi negocio",
            "Contáctanos",
            "Pausar",
            "Reanudar",
            "Panadería Central",
            "Te faltan 2 compras para tu café gratis",
            "Mostrar mi código",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.markdown)
        self.assertNotIn("[Cómo funciona](#como-funciona)", self.markdown)
        self.assertNotIn("[Para quién](#para-quien)", self.markdown)
        self.assertNotIn("[Contacto](#contacto)", self.markdown)

    def test_examples_are_labeled_as_illustrative_and_utf8_is_preserved(self):
        label = self.markdown.index("Ejemplos ilustrativos")
        for example in ("Panadería:", "Café:", "Peluquería:", "Librería:", "Almacén:"):
            with self.subTest(example=example):
                self.assertGreater(self.markdown.index(example), label)
        self.assertNotIn("Cuéntanos qué vendes y armamos tu tarjeta juntos", self.markdown)
        self.assertNotIn("**Tu comercio:**", self.markdown)
        for accent in ("beneficios", "beneficio", "cafés", "Tú"):
            with self.subTest(accent=accent):
                self.assertIn(accent, self.markdown)

    def test_robots_allows_normal_crawling_without_claiming_a_sitemap(self):
        robots = (ROOT / "dist/robots.txt").read_text(encoding="utf-8")
        groups = []
        current_group = None
        for line in robots.splitlines():
            line = line.partition("#")[0].strip()
            if not line:
                continue
            directive, separator, value = line.partition(":")
            if not separator:
                continue
            directive = directive.strip().lower()
            value = value.strip()
            if directive == "user-agent":
                if current_group is None or current_group["directives"]:
                    current_group = {"agents": [], "directives": []}
                    groups.append(current_group)
                current_group["agents"].append(value.lower())
            elif current_group is not None:
                current_group["directives"].append((directive, value))

        self.assertTrue(any("*" in group["agents"] for group in groups))
        for group in groups:
            for directive, value in group["directives"]:
                self.assertFalse(directive == "disallow" and value)
        self.assertFalse(any(line.lower().startswith("sitemap:") for line in robots.splitlines()))


if __name__ == "__main__":
    unittest.main()
