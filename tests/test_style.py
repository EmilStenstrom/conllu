import unittest

from flake8.api.legacy import get_style_guide

class TestFlake8Compliance(unittest.TestCase):
    def test_flake8(self):
        style_guide = get_style_guide()
        report = style_guide.check_files()
        self.assertEqual(report.get_statistics('E'), [])
