import unittest
try:
    from streamlit.testing.v1 import AppTest
except Exception:
    AppTest=None

@unittest.skipIf(AppTest is None,"streamlit not installed")
class TestStreamlitApp(unittest.TestCase):
    def test_app_starts(self):
        at=AppTest.from_file("streamlit_app.py")
        at.run(timeout=20)
        self.assertFalse(at.exception)
        self.assertGreaterEqual(len(at.selectbox),1)
        self.assertGreaterEqual(len(at.button),1)

if __name__=="__main__":
    unittest.main()
