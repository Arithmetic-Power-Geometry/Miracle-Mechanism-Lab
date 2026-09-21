import csv,json
from pathlib import Path
from miracle_lab.core.ctc import minimum_separating_set
from miracle_lab.core.ctc_adaptive import optimal_adaptive_plan,flatten_plan
from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK
out=Path("artifacts"); out.mkdir(exist_ok=True); rows=[]; trees={}
for gx,(mechs,ms) in GENERIC_BENCHMARK.items():
 static=minimum_separating_set(mechs,ms); plan=optimal_adaptive_plan(mechs,ms)
 rows.append({"experiment":gx,"static_cost":static.total_cost,"adaptive_worst_case_cost":plan.worst_case_cost,
              "worst_case_saving":static.total_cost-plan.worst_case_cost,"root_experiment":plan.experiment})
 trees[gx]=flatten_plan(plan)
with open(out/"ctc_adaptive_results.csv","w",newline="",encoding="utf-8") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
(out/"ctc_adaptive_trees.json").write_text(json.dumps(trees,indent=2),encoding="utf-8")
print(json.dumps(rows,indent=2))
