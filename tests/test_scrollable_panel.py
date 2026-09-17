import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scrollable_panel import ScrollablePanel


class FakeCanvas:
    def __init__(self, first=0.5, last=0.7, region_height=2000, viewport_height=400):
        self.first = first
        self.last = last
        self.region_height = region_height
        self.viewport_height = viewport_height
        self.moveto_calls = []

    def yview(self):
        return self.first, self.last

    def cget(self, key):
        self.assert_key = key
        return f"0 0 100 {self.region_height}"

    def winfo_height(self):
        return self.viewport_height

    def yview_moveto(self, fraction):
        self.moveto_calls.append(fraction)


class ScrollablePanelBehaviorTests(unittest.TestCase):
    def test_wheel_scroll_uses_bounded_fractional_repaint(self):
        panel = ScrollablePanel.__new__(ScrollablePanel)
        panel.canvas = FakeCanvas(first=0.5, last=0.7)

        panel._scroll_by_wheel(120)

        self.assertEqual(len(panel.canvas.moveto_calls), 1)
        self.assertLess(panel.canvas.moveto_calls[0], 0.5)
        self.assertGreaterEqual(panel.canvas.moveto_calls[0], 0.0)

    def test_wheel_scroll_clamps_at_the_bottom(self):
        panel = ScrollablePanel.__new__(ScrollablePanel)
        panel.canvas = FakeCanvas(first=0.98, last=1.0)

        panel._scroll_by_wheel(-120)

        self.assertEqual(panel.canvas.moveto_calls, [1.0])


if __name__ == "__main__":
    unittest.main()
