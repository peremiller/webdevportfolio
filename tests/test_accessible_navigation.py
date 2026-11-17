"""Accessible navigation regression tests for the original static portfolio."""
import re
import unittest
from pathlib import Path

HTML = (Path(__file__).resolve().parents[1] / "index.html").read_text(encoding="utf-8")


class PortfolioNavigationTests(unittest.TestCase):
    def test_skip_link_targets_focusable_main_landmark(self):
        self.assertRegex(HTML, r'<a class="skip-link" href="#main-content">Skip to main content</a>')
        self.assertRegex(HTML, r'<main id="main-content" tabindex="-1">')
        self.assertLess(HTML.index('href="#main-content"'), HTML.index("<nav>"))
        self.assertLess(HTML.index("<main id="), HTML.index('<header class="hero"'))
        self.assertGreater(HTML.index("</main>"), HTML.index('<section id="contact">'))

    def test_skip_link_only_visible_on_focus(self):
        self.assertIn('.skip-link:focus{transform:none', HTML)
        self.assertIn('z-index:200', HTML)

    def test_typewriter_does_not_start_if_reduced_motion(self):
        self.assertRegex(
            HTML,
            r'if \(window\.matchMedia\("\(prefers-reduced-motion: reduce\)"\)\.matches\)\s*\{'
            r'\s*tw\.textContent = WORDS\[0\];\s*\}\s*else\s*\{\s*tick\(\);'
        )

    def test_navigation_has_stable_hash_targets(self):
        ids = set(re.findall(r'\bid="([^"]+)"', HTML))
        for href in re.findall(r'<a\b[^>]*\bhref="#([^"]+)"', HTML):
            self.assertIn(href, ids, f"Missing hash target {href}")


if __name__ == "__main__":
    unittest.main()
