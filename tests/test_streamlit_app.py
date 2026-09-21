import unittest
from pathlib import Path
try:
    from streamlit.testing.v1 import AppTest
except Exception:
    AppTest=None

@unittest.skipIf(AppTest is None,"streamlit not installed")
class TestStreamlitApp(unittest.TestCase):
    def app(self):
        p=Path(__file__).resolve().parents[1] / "streamlit_app.py"
        at=AppTest.from_file(str(p)); at.run(timeout=20)
        self.assertFalse(at.exception); return at

    def test_entry(self):
        at=self.app()
        self.assertEqual(at.selectbox[0].label,"What are you curious about?")
        self.assertEqual(at.button[0].label,"ENTER EXPERIMENT →")

    def test_each_scenario_locks_correct_model(self):
        at=self.app()
        expected=[
          ("A 20 g sweet appears in a monitored chamber","ACS-14"),
          ("An object appears in a monitored chamber","ACS-14"),
          ("An object changes position with no observed intermediate path","ACS-09"),
          ("A journey contains a large unobserved segment","ACS-08"),
          ("An object rises without an identified support","ACS-10"),
          ("An object becomes dramatically smaller","ACS-01"),
          ("An object becomes dramatically larger","ACS-02"),
          ("An object behaves as if its effective mass is much lower","ACS-03"),
          ("A present object stops being detected","ACS-05"),
          ("Several matching instances appear at once","ACS-06"),
          ("The same identity appears at separated locations","ACS-07"),
          ("Information appears without an identified ordinary channel","ACS-11"),
          ("Information appears before the later outcome","ACS-12"),
          ("Something is accessed without an observed route","ACS-04"),
          ("Recovery is unusually fast","ACS-13"),
        ]
        for scenario,code in expected:
            at.selectbox[0].select(scenario).run(timeout=20)
            self.assertFalse(at.exception)
            self.assertIn(code,at.markdown[-3].value if len(at.markdown)>=3 else " ".join(x.value for x in at.markdown))

if __name__=="__main__":
    unittest.main()
