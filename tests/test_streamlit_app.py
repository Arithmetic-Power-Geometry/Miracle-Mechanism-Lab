import unittest
from pathlib import Path
try:
    from streamlit.testing.v1 import AppTest
except Exception:
    AppTest=None

@unittest.skipIf(AppTest is None,"streamlit not installed")
class TestStreamlitApp(unittest.TestCase):
    def test_three_screen_flow_starts(self):
        app_path=Path(__file__).resolve().parents[1] / "streamlit_app.py"
        at=AppTest.from_file(str(app_path))
        at.run(timeout=20)
        self.assertFalse(at.exception)
        self.assertGreaterEqual(len(at.selectbox),2)
        self.assertEqual(at.selectbox[0].label,"What are you curious about?")
        self.assertGreaterEqual(len(at.button),1)
        self.assertEqual(at.button[0].label,"ENTER EXPERIMENT →")

if __name__=="__main__":
    unittest.main()
