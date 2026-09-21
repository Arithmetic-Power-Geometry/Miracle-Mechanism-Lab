import csv, json
from collections import defaultdict
from pathlib import Path
from miracle_lab.core.inversion import minimum_modification

rows=list(csv.DictReader(Path("data/synthetic_claim_trials.csv").open(encoding="utf-8")))
literal=[r for r in rows if r["world"]=="literal_simulation"]
out=[]
for r in literal:
    obs={k:float(v) for k,v in r.items() if k in {
        "distance_m","elapsed_s","mass_energy_j","unsupported_force_n",
        "information_excess_bits","authenticated_instances","volume_ratio",
        "effective_mass_ratio","observer_access","viability_gain"} and v!=""}
    m=minimum_modification(r["capability"],obs)
    if m:
        out.append({"capability":r["capability"],"mechanism":m.name,"magnitude":m.magnitude,"unit":m.unit,"normalized_cost":m.normalized_cost})

agg=defaultdict(lambda:{"n":0,"cost":0.0})
for r in out:
    d=agg[(r["capability"],r["mechanism"])]; d["n"]+=1; d["cost"]+=r["normalized_cost"]
report=[{"capability":k[0],"minimum_extension":k[1],"n":v["n"],"mean_normalized_cost":v["cost"]/v["n"]} for k,v in sorted(agg.items())]
Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/constraint_inversion.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
