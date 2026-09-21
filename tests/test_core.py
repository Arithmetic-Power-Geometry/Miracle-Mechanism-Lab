import unittest
from miracle_lab.core.state import WorldState
from miracle_lab.agents.extraordinary import SiddhiAgent, IddhiAgent, KaramatAgent, MiracleAgent
from miracle_lab.core.evidence import score_evidence

class TestAgents(unittest.TestCase):
    def setUp(self):
        self.s=WorldState()

    def test_anima_changes_volume_only(self):
        r=SiddhiAgent().simulate("anima",self.s,scale=0.5)
        changed={k:v for k,v in r.required_delta.items() if v != 0}
        self.assertEqual(set(changed),{"volume"})
        self.assertAlmostEqual(r.after.volume,0.035)

    def test_bilocation_changes_identity(self):
        r=KaramatAgent().simulate("bilocation",self.s)
        self.assertEqual(r.after.identity_state,2.0)

    def test_teleportation_changes_position(self):
        r=MiracleAgent().simulate("teleportation",self.s,dx=1000)
        self.assertEqual(r.required_delta["position_x"],1000)

    def test_evidence_rejects_unseparated_case(self):
        r=score_evidence("teleportation",{"path":0.0},{"path":0.0},[{"path":0.0}])
        self.assertFalse(r.resolved)
        self.assertIn("ordinary alternative not separated",r.errors)

    def test_evidence_accepts_separated_case(self):
        r=score_evidence("remote_information",{"accuracy":1.0,"leakage":0.0},{"accuracy":1.0,"leakage":0.0},[{"accuracy":0.5,"leakage":1.0}])
        self.assertTrue(r.resolved)

if __name__ == "__main__":
    unittest.main()
