import csv,json
from pathlib import Path
from miracle_lab.core.ctc import minimum_separating_set
from miracle_lab.core.ctc_benchmark import BENCHMARK
out=Path("artifacts"); out.mkdir(exist_ok=True); rows=[]; detail={}
for cap,(mechs,measurements) in BENCHMARK.items():
 r=minimum_separating_set(mechs,measurements)
 rows.append({"capability":cap,"mechanisms":len(mechs),"measurements":len(measurements),"minimum_cost":r.total_cost,"selected":";".join(r.selected),"unresolved_pairs":len(r.unresolved_pairs)})
 detail[cap]={"selected":r.selected,"minimum_cost":r.total_cost,"equivalence_classes":r.equivalence_classes}
with open(out/"ctc_exact_results.csv","w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
(out/"ctc_exact_results.json").write_text(json.dumps(detail,indent=2))
print(json.dumps(rows,indent=2))
