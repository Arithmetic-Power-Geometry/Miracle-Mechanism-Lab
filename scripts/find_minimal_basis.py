import csv, json
from collections import defaultdict
from pathlib import Path
from miracle_lab.core.inversion import minimum_modification
from miracle_lab.core.frontier import mechanism_family
from miracle_lab.core.basis import minimum_basis, singleton_requirements

rows=list(csv.DictReader(Path("data/synthetic_claim_trials.csv").open(encoding="utf-8")))
mapping={}
for r in rows:
    if r["world"]!="literal_simulation" or r["capability"] in mapping: continue
    obs={}
    for k in ("distance_m","elapsed_s","mass_energy_j","unsupported_force_n","information_excess_bits","authenticated_instances","volume_ratio","effective_mass_ratio","observer_access","viability_gain"):
        if k in r and r[k]!="": obs[k]=float(r[k])
    m=minimum_modification(r["capability"],obs)
    if m: mapping[r["capability"]]=mechanism_family(m.name)

req=singleton_requirements(mapping)
result=minimum_basis(req)
family_members=defaultdict(list)
for cap,fam in sorted(mapping.items()): family_members[fam].append(cap)
report={
 "capability_count":len(mapping),
 "basis_size":result.size,
 "basis":list(result.basis),
 "family_members":dict(sorted(family_members.items())),
 "covered":list(result.covered),
 "uncovered":list(result.uncovered),
 "compression_ratio": (len(mapping)/result.size if result.size else None),
 "interpretation":"A structural compression of this stipulated synthetic ontology; not evidence that these mechanisms exist in nature."
}
Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/minimal_miracle_basis.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
