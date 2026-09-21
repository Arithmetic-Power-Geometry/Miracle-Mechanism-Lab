import csv, json
from collections import defaultdict
from pathlib import Path
from miracle_lab.core.inversion import minimum_modification
from miracle_lab.core.frontier import mechanism_family

rows=list(csv.DictReader(Path("data/synthetic_claim_trials.csv").open(encoding="utf-8")))
literal=[r for r in rows if r["world"]=="literal_simulation"]
by_cap=defaultdict(list)
for r in literal:
    obs={}
    for k in ("distance_m","elapsed_s","mass_energy_j","unsupported_force_n","information_excess_bits","authenticated_instances","volume_ratio","effective_mass_ratio","observer_access","viability_gain"):
        if k in r and r[k]!="": obs[k]=float(r[k])
    m=minimum_modification(r["capability"],obs)
    if m: by_cap[r["capability"]].append(m)

capability_summary=[]
families=defaultdict(list)
for cap,mods in sorted(by_cap.items()):
    mechanism=mods[0].name
    fam=mechanism_family(mechanism)
    cost=sum(m.normalized_cost for m in mods)/len(mods)
    capability_summary.append({"capability":cap,"mechanism":mechanism,"family":fam,"mean_cost":cost,"n":len(mods)})
    families[fam].append(cap)

report={"capabilities":capability_summary,"shared_mechanism_families":dict(sorted(families.items())),
"note":"Clusters are consequences of the stipulated synthetic model, not discoveries of physical mechanisms."}
Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/mechanism_clusters.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
