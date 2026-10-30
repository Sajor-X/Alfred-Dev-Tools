import json
import os
from pathlib import Path
import plistlib
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zlib

from alfred_dev_tools.features.rgb import build_results, parse_color, swatch_path, swatch_png


ROOT = Path(__file__).resolve().parents[1]


class ColorParsingTests(unittest.TestCase):
    def test_supported_formats(self):
        cases = {
            "#CC73E1FF": (204, 115, 225, 1),
            " cc73e1 ": (204, 115, 225, 1),
            "#C7E": (204, 119, 238, 1),
            "#C7E8": (204, 119, 238, 136 / 255),
            "#CC73E180": (204, 115, 225, 128 / 255),
            "RGB(204, 115, 225)": (204, 115, 225, 1),
            "rgba(204,115,225,.5)": (204, 115, 225, .5),
            "204, 115, 225, 0.5": (204, 115, 225, .5),
            "204 115 225": (204, 115, 225, 1),
            "rgb(80% 45% 88% / 50%)": (204, 115, 224, .5),
            "rgba(0, 0, 0, 0)": (0, 0, 0, 0),
            "rgb(255 255 255 / 100%)": (255, 255, 255, 1),
            "rgb(1e2, 0.5, 1.5)": (100, 1, 2, 1),
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(parse_color(query), expected)

    def test_invalid_inputs(self):
        for query in ("#12", "#12345", "#1234567", "#GG0000", "red", "",
                      "rgb(256,0,0)", "rgb(-1,0,0)", "rgb(101%,0,0)",
                      "rgba(1,2,3,255)", "rgba(1,2,3,-.1)", "rgba(1,2,3,101%)",
                      "rgb(1,,2,3)", "rgb(1,2,3,)", "rgb(1 2 / .5)",
                      "rgb(1 2 3 / .5 / .2)", "rgb(1,2,3", "rgb(NaN,0,0)",
                      "rgb(1e999,0,0)", "rgba(0,0,0,inf)", "1 2 3 4 5"):
            with self.subTest(query=query), self.assertRaises(ValueError):
                parse_color(query)


class ColorPreviewTests(unittest.TestCase):
    def test_png_pixels_and_dimensions(self):
        for alpha, expected in ((1, ((204, 115, 225), (204, 115, 225))),
                                (.5, ((230, 185, 240), (210, 166, 221))),
                                (0, ((255, 255, 255), (216, 216, 216)))):
            with self.subTest(alpha=alpha):
                png = swatch_png((204, 115, 225, alpha))
                self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
                position, compressed = 8, b""
                while position < len(png):
                    size = struct.unpack(">I", png[position:position + 4])[0]
                    kind = png[position + 4:position + 8]
                    data = png[position + 8:position + 8 + size]
                    crc = struct.unpack(">I", png[position + 8 + size:position + 12 + size])[0]
                    self.assertEqual(crc, zlib.crc32(kind + data))
                    if kind == b"IHDR":
                        self.assertEqual(struct.unpack(">IIBBBBB", data), (1200, 800, 8, 2, 0, 0, 0))
                    if kind == b"IDAT":
                        compressed += data
                    position += size + 12
                pixels = zlib.decompress(compressed)
                self.assertEqual(len(pixels), (1200 * 3 + 1) * 800)
                self.assertEqual(tuple(pixels[1:4]), expected[0])
                self.assertEqual(tuple(pixels[97:100]), expected[1])
                row32 = (1200 * 3 + 1) * 32
                self.assertEqual(tuple(pixels[row32 + 1:row32 + 4]), expected[1])

    def test_result_copy_preview_and_cache(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"alfred_workflow_cache": directory}):
            results = build_results("rgba(204,115,225,.5)")["items"]
            self.assertEqual([r["arg"] for r in results], ["#CC73E180", "rgba(204, 115, 225, 0.5)", "#CC73E1", "rgb(204, 115, 225)"])
            preview = Path(results[0]["quicklookurl"])
            self.assertTrue(preview.is_file())
            timestamp = preview.stat().st_mtime_ns
            self.assertEqual(swatch_path(parse_color("rgba(204,115,225,.5)")), str(preview))
            self.assertEqual(timestamp, preview.stat().st_mtime_ns)
            for result in results:
                self.assertTrue(result["valid"])
                self.assertEqual(result["text"]["copy"], result["arg"])
                self.assertEqual(result["icon"]["path"], str(preview))

    def test_cache_failure_keeps_copyable_values(self):
        with patch("alfred_dev_tools.features.rgb.swatch_path", side_effect=OSError("read only")):
            result = build_results("#CC73E1FF")["items"][0]
        self.assertEqual(result["arg"], "#CC73E1")
        self.assertNotIn("quicklookurl", result)
        self.assertIn("色卡生成失败", result["subtitle"])

    def test_help_and_errors_do_not_generate_images(self):
        with patch("alfred_dev_tools.features.rgb.swatch_path") as preview:
            for query in ("", "help", "?", "invalid"):
                self.assertFalse(build_results(query)["items"][0]["valid"])
            preview.assert_not_called()

    def test_dispatcher_and_workflow_wiring(self):
        with tempfile.TemporaryDirectory() as directory:
            output = subprocess.check_output(
                [sys.executable, "workflow.py", "rgb", "#CC73E1FF"], cwd=ROOT,
                env={**os.environ, "alfred_workflow_cache": directory}, text=True,
            )
            self.assertIn("rgba(204, 115, 225, 1)", [r["arg"] for r in json.loads(output)["items"]])
        workflow = plistlib.loads((ROOT / "info.plist").read_bytes())
        rgb = next(o for o in workflow["objects"] if o["uid"] == "rgb-input")
        self.assertEqual(rgb["config"]["keyword"], "{var:keyword_prefix}rgb")
        self.assertEqual(workflow["connections"]["rgb-input"][0]["destinationuid"], "clipboard-output")


if __name__ == "__main__":
    unittest.main()
