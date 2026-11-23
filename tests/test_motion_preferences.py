"""Source-level reduced-motion guardrails; these do not replace browser tests."""
import unittest
from pathlib import Path

HTML = (Path(__file__).resolve().parents[1] / "index.html").read_text(encoding="utf-8")


class MotionPreferenceSourceTests(unittest.TestCase):
    def test_reduced_motion_disables_blink_and_pulse(self):
        css = HTML.split('@media (prefers-reduced-motion:reduce){', 1)[1].split('/* ---------- responsive', 1)[0]
        self.assertIn('.hero-kicker .dot,.typeline .cursor{animation:none}', css)
        self.assertIn('.typeline .cursor{display:none}', css)

    def test_typewriter_has_static_reduced_motion_fallback(self):
        self.assertIn('const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)")', HTML)
        self.assertIn('if (reducedMotion.matches) { tw.textContent = WORDS[0]; return; }', HTML)
        self.assertIn('typeTimer = setTimeout(tick, delay)', HTML)

    def test_motion_preference_change_cancels_old_timer(self):
        self.assertIn('reducedMotion.addEventListener?.("change"', HTML)
        self.assertIn('clearTimeout(typeTimer)', HTML)
        self.assertIn('if (reducedMotion.matches) tw.textContent = WORDS[0]', HTML)

    def test_project_cards_allow_320px_mobile_width(self):
        self.assertIn('minmax(min(100%,310px),1fr)', HTML)


    def test_mobile_navigation_stays_accessible_without_scripts(self):
        # Mobile links stay visible by default; only enhanced navigation hides them.
        self.assertIn('.nav-links{width:100%;flex-wrap:wrap;gap:0}', HTML)
        self.assertIn('.nav-enhanced .nav-links{', HTML)
        self.assertIn('.nav-enhanced .nav-links.open{display:flex}', HTML)
        self.assertIn('.nav-enhanced .nav-toggle{display:block}', HTML)
        self.assertIn('document.documentElement.classList.add("nav-enhanced");', HTML)
        self.assertIn('if (restoreFocus) toggle.focus()', HTML)

    def test_existing_nav_and_sections_are_preserved(self):
        self.assertIn('aria-controls="site-navigation"', HTML)
        self.assertIn('<main id="main-content" tabindex="-1">', HTML)
        self.assertIn('href="#main-content">Skip to main content</a>', HTML)
        self.assertIn('window.addEventListener("resize"', HTML)


if __name__ == "__main__":
    unittest.main()
