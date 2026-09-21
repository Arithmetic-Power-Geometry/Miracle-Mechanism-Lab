import unittest
from pathlib import Path
try:
    from streamlit.testing.v1 import AppTest
except Exception:
    AppTest=None

@unittest.skipIf(AppTest is None,"streamlit not installed")
class TestStreamlitApp(unittest.TestCase):
    def test_app_starts(self):
        app_path=Path(__file__).resolve().parents[1] / "streamlit_app.py"
        at=AppTest.from_file(str(app_path))
        at.run(timeout=20)
        self.assertFalse(at.exception)
        self.assertGreaterEqual(len(at.selectbox),1)
        self.assertGreaterEqual(len(at.button),1)

if __name__=="__main__":
    unittest.main()
