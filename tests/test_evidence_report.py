import unittest
from miracle_lab.core.generic_engine import execute
from miracle_lab.core.evidence_report import build_report,report_audit
from miracle_lab.core.experiment_specs import SPECS
class TestEvidenceReport(unittest.TestCase):
 def test_all_21_report(self):
  for k,s in SPECS.items():
   r=build_report(execute(k)); self.assertEqual(r.code,s.code); self.assertEqual(r.resolution_status,"UNRESOLVED"); self.assertTrue(r.unresolved)
 def test_only_declared_measurements_resolve(self):
  s=SPECS["local_emergence"]; r=build_report(execute("local_emergence"),s.measurements)
  self.assertEqual(r.resolution_status,"RESOLVED_FOR_DECLARED_MEASUREMENTS"); self.assertEqual(r.unresolved,())
 def test_partial_measurements_stay_unresolved(self):
  r=build_report(execute("local_emergence"),("mass balance",)); self.assertEqual(r.resolution_status,"UNRESOLVED")
 def test_audit(self): self.assertEqual(report_audit()["count"],21); self.assertTrue(report_audit()["all_have_visual"])
if __name__=="__main__": unittest.main()
