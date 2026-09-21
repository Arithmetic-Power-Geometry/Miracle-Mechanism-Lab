import csv,json
from pathlib import Path
from miracle_lab.core.ctc import minimum_separating_set
from miracle_lab.core.ctc_adaptive import optimal_adaptive_plan,flatten_plan
from miracle_lab.core.ctc_benchmark import BENCHMARK
out=Path("artifacts"); out.mkdir(exist_ok=True); rows=[]; trees={}
for cap,(mechs,ms) in BENCHMARK.items():
 static=minimum_separating_set(mechs,ms); plan=optimal_adaptive_plan(mechs,ms)
 rows.append({"capability":cap,"static_cost":static.total_cost,"adaptive_worst_case_cost":plan.worst_case_cost,
              "worst_case_saving":static.total_cost-plan.worst_case_cost,"root_experiment":plan.experiment})
 trees[cap]=flatten_plan(plan)
with open(out/"ctc_adaptive_results.csv","w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
(out/"ctc_adaptive_trees.json").write_text(json.dumps(trees,indent=2))
print(json.dumps(rows,indent=2))
