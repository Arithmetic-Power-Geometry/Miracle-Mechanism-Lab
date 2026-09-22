import csv,json
from collections import defaultdict
from pathlib import Path
from miracle_lab.core.inversion import minimum_modification
from miracle_lab.core.frontier import mechanism_family
rows=list(csv.DictReader(Path("data/synthetic_claim_trials.csv").open(encoding="utf-8")))
by=defaultdict(list)
for r in rows:
 if r["world"]!="literal_simulation": continue
 obs=json.loads(r["model_outputs"])
 m=minimum_modification(r["experiment"],obs)
 if m: by[r["experiment"]].append(m)
summary=[]; families=defaultdict(list)
for gx,mods in sorted(by.items()):
 mechanism=mods[0].name; fam=mechanism_family(mechanism)
 summary.append({"experiment":gx,"mechanism":mechanism,"family":fam,"mean_cost":sum(x.normalized_cost for x in mods)/len(mods),"n":len(mods)})
 families[fam].append(gx)
report={"experiments":summary,"shared_mechanism_families":dict(sorted(families.items())),
 "note":"Structural consequences of a stipulated synthetic model; not discoveries of physical mechanisms."}
Path("artifacts").mkdir(exist_ok=True); Path("artifacts/mechanism_clusters.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
