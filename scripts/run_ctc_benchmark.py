import csv,json
from pathlib import Path
from miracle_lab.core.ctc import minimum_separating_set,greedy_separating_set,separation_matrix
from miracle_lab.core.ctc_benchmark import BENCHMARK
out=Path("artifacts"); out.mkdir(exist_ok=True); rows=[]; detail={}
for cap,(mechs,measurements) in BENCHMARK.items():
 r=minimum_separating_set(mechs,measurements)
 gsel,gcost,gunresolved=greedy_separating_set(mechs,measurements)
 rows.append({"capability":cap,"mechanisms":len(mechs),"measurements":len(measurements),
  "exact_cost":r.total_cost,"exact_selected":";".join(r.selected),
  "greedy_cost":gcost,"greedy_selected":";".join(gsel),
  "greedy_gap":gcost-r.total_cost,"unresolved_pairs":len(r.unresolved_pairs)})
 detail[cap]={"mechanisms":mechs,"exact_selected":r.selected,"exact_cost":r.total_cost,
  "greedy_selected":gsel,"greedy_cost":gcost,"equivalence_classes":r.equivalence_classes,
  "separation_matrix":separation_matrix(mechs,measurements)}
with open(out/"ctc_exact_results.csv","w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
(out/"ctc_exact_results.json").write_text(json.dumps(detail,indent=2))
print(json.dumps(rows,indent=2))
