import csv,json,ast
from collections import defaultdict
from pathlib import Path
from miracle_lab.core.inversion import minimum_modification
from miracle_lab.core.frontier import mechanism_family
from miracle_lab.core.basis import minimum_basis,singleton_requirements
rows=list(csv.DictReader(Path("data/synthetic_claim_trials.csv").open(encoding="utf-8"))); mapping={}
for r in rows:
 if r["world"]!="literal_simulation" or r["experiment"] in mapping: continue
 obs=dict(ast.literal_eval(r["model_outputs"])); m=minimum_modification(r["experiment"],obs)
 if m: mapping[r["experiment"]]=mechanism_family(m.name)
result=minimum_basis(singleton_requirements(mapping)); members=defaultdict(list)
for gx,fam in sorted(mapping.items()): members[fam].append(gx)
report={"experiment_count":len(mapping),"basis_size":result.size,"basis":list(result.basis),
 "family_members":dict(sorted(members.items())),"covered":list(result.covered),"uncovered":list(result.uncovered),
 "compression_ratio":len(mapping)/result.size if result.size else None,
 "interpretation":"Structural compression of the stipulated synthetic ontology; not evidence that these mechanisms exist in nature."}
Path("artifacts").mkdir(exist_ok=True); Path("artifacts/minimal_miracle_basis.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
