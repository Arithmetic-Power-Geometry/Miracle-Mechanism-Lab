import unittest,tempfile,os,json
from pathlib import Path
import scripts.generate_ctc_artifacts as g
class TestCTCArtifacts(unittest.TestCase):
 def test_artifact_bundle(self):
  old=g.OUT
  with tempfile.TemporaryDirectory() as d:
   g.OUT=Path(d); g.main()
   names={p.name for p in Path(d).iterdir()}
   self.assertEqual(names,{"strategy_benchmark.csv","exact_separating_sets.csv","adaptive_trees.csv","noisy_accuracy_curves.csv","stress_cases.json","manifest.json"})
   m=json.loads((Path(d)/"manifest.json").read_text()); self.assertEqual(m["benchmark_rows"],63); self.assertEqual(m["experiments"],21); self.assertEqual(len(m["files"]),5)
  g.OUT=old
if __name__=="__main__": unittest.main()
