import csv,json
from pathlib import Path
from miracle_lab.core.noisy_benchmark import noisy_experiment,REGIMES
from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK
from miracle_lab.core.ctc_probabilistic import probabilistic_resolution_summary
out=Path("artifacts"); out.mkdir(exist_ok=True); rows=[]; detail={}
for regime in REGIMES:
 for gx in GENERIC_BENCHMARK:
  mechs,ms=noisy_experiment(gx,regime); s=probabilistic_resolution_summary(mechs,ms,.95)
  key=f"{gx}::{regime}"
  detail[key]={"target_accuracy":s["target_accuracy"],"unresolved_pairs":[list(x) for x in s["unresolved_pairs"]],
   "pair_best":{" | ".join(k):{"cost":v[0],"samples":v[1],"measurement":v[2]} for k,v in s["pair_best"].items()}}
  rows.append({"experiment":gx,"regime":regime,"mechanisms":len(mechs),"measurements":len(ms),
   "target_accuracy":s["target_accuracy"],"unresolved_pairs":len(s["unresolved_pairs"]),"max_pair_cost":s["max_pair_cost"]})
with open(out/"ctc_noisy_results.csv","w",newline="",encoding="utf-8") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
(out/"ctc_noisy_results.json").write_text(json.dumps(detail,indent=2),encoding="utf-8")
print(json.dumps(rows,indent=2))
