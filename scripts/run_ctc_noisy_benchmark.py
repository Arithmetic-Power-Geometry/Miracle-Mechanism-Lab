import csv,json
from pathlib import Path
from miracle_lab.core.ctc_probabilistic import probabilistic_resolution_summary
from miracle_lab.core.ctc_probabilistic_benchmark import NOISY_BENCHMARK
out=Path("artifacts"); out.mkdir(exist_ok=True); rows=[]; detail={}
for cap,(mechs,ms) in NOISY_BENCHMARK.items():
 s=probabilistic_resolution_summary(mechs,ms)
 detail[cap]={"target_information":s["target_information"],"unresolved_pairs":[list(x) for x in s["unresolved_pairs"]],
  "pair_best":{" | ".join(k):{"cost":v[0],"samples":v[1],"measurement":v[2]} for k,v in s["pair_best"].items()}}
 rows.append({"capability":cap,"mechanisms":len(mechs),"measurements":len(ms),
  "unresolved_pairs":len(s["unresolved_pairs"]),"max_pair_cost":s["max_pair_cost"]})
with open(out/"ctc_noisy_results.csv","w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
(out/"ctc_noisy_results.json").write_text(json.dumps(detail,indent=2))
print(json.dumps(rows,indent=2))
