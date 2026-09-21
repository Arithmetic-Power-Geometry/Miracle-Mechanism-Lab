import json
from pathlib import Path
from miracle_lab.experiments.sweet import simulate_sweet, observable_signature
from miracle_lab.core.anomaly import anomaly_profile, minimum_anomaly

MECH=["ordinary_insertion","unknown_transport","local_materialization","transformation","perceptual_appearance"]
profiles=[anomaly_profile(m,observable_signature(simulate_sweet(m))) for m in MECH]
ordinary=[p.mechanism for p in profiles if p.ordinary_compatible]
extra=[p.mechanism for p in profiles if not p.ordinary_compatible]
minimum=[p.mechanism for p in minimum_anomaly(profiles)]
report={
 "experiment":"SWEET-1",
 "ordinary_compatible_mechanisms":ordinary,
 "anomalous_mechanisms":extra,
 "minimum_residual_count_for_physical_outcome":min(p.residual_count for p in profiles if p.mechanism!="perceptual_appearance"),
 "minimum_anomaly_mechanisms":minimum,
 "profiles":[{"mechanism":p.mechanism,"violated_constraints":list(p.violated_constraints),"residual_count":p.residual_count,"residual_l1":p.residual_l1,"ordinary_compatible":p.ordinary_compatible} for p in profiles],
 "conclusion":"The visible outcome alone does not require an anomaly because ordinary insertion/transformation remain compatible. Extraordinary mechanism claims require additional observations excluding ordinary paths.",
 "scope":"Synthetic closed-chamber ontology only; not empirical evidence."
}
Path("artifacts/sweet1_anomaly_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
