import json
from pathlib import Path
from miracle_lab.experiments.sweet import simulate_sweet, observable_signature
from miracle_lab.core.separation import separating_observables, minimum_measurement_set

MECH=["ordinary_insertion","unknown_transport","local_materialization","transformation","perceptual_appearance"]
signatures={m:observable_signature(simulate_sweet(m)) for m in MECH}
pairs=separating_observables(signatures)
minimum=minimum_measurement_set(signatures)
report={
 "experiment":"SWEET-1",
 "mechanisms":MECH,
 "minimum_measurement_set":minimum,
 "measurement_count":len(minimum),
 "pairwise_separation":{f"{a} vs {b}":sorted(v) for (a,b),v in pairs.items()},
 "all_pairs_separable":all(bool(v) for v in pairs.values()),
 "interpretation":"Minimum set for the current idealized synthetic signatures only; real experiments require measurement error, provenance controls and independent validation."
}
Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/sweet1_minimum_measurements.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
