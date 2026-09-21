"""Generate deterministic, auditable ACS benchmark artifacts."""
import csv,json,hashlib
from pathlib import Path
from miracle_lab.core.benchmark_suite import benchmark_rows
from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK,solve_experiment
from miracle_lab.core.ctc_adaptive import optimal_adaptive_plan,flatten_plan
from miracle_lab.core.noisy_benchmark import noisy_experiment,REGIMES
from miracle_lab.core.ctc_probabilistic import probabilistic_resolution_summary
from miracle_lab.core.stress_benchmark import search_strict_greedy_counterexample,stress_audit

OUT=Path("artifacts/ctc"); OUT.mkdir(parents=True,exist_ok=True)
def write_csv(path,rows):
 rows=list(rows)
 with path.open("w",newline="",encoding="utf-8") as f:
  if not rows:return
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def main():
 rows=benchmark_rows(.95); write_csv(OUT/"strategy_benchmark.csv",rows)
 exact=[]; trees=[]
 for key,(m,e) in GENERIC_BENCHMARK.items():
  x=solve_experiment(key)["exact"]
  exact.append({"experiment":key,"selected":";".join(x.selected),"cost":x.total_cost})
  for row in flatten_plan(optimal_adaptive_plan(m,e)): trees.append({"experiment":key,**row})
 write_csv(OUT/"exact_separating_sets.csv",exact); write_csv(OUT/"adaptive_trees.csv",trees)
 curves=[]
 for acc in (.90,.95,.99):
  for regime in REGIMES:
   for key in GENERIC_BENCHMARK:
    m,e=noisy_experiment(key,regime); s=probabilistic_resolution_summary(m,e,acc)
    curves.append({"experiment":key,"regime":regime,"target_accuracy":acc,
      "max_pair_cost":s["max_pair_cost"],"unresolved_pairs":len(s["unresolved_pairs"])})
 write_csv(OUT/"noisy_accuracy_curves.csv",curves)
 found=search_strict_greedy_counterexample()
 stress={"audit":stress_audit()}
 if found:
  m,e,x,g=found; stress["greedy_counterexample"]={"mechanisms":m,
   "measurements":[{"name":z.name,"cost":z.cost,"outcomes":z.outcomes} for z in e],
   "exact":{"selected":x.selected,"cost":x.total_cost},"greedy":{"selected":g[0],"cost":g[1]}}
 (OUT/"stress_cases.json").write_text(json.dumps(stress,indent=2,sort_keys=True),encoding="utf-8")
 files=sorted(p for p in OUT.iterdir() if p.name!="manifest.json")
 manifest={"schema":"acs-ctc-artifacts-v1","generator":"scripts/generate_ctc_artifacts.py",
  "files":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
  "benchmark_rows":len(rows),"experiments":len(GENERIC_BENCHMARK),"accuracy_levels":[.90,.95,.99],
  "noise_regimes":list(REGIMES)}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True),encoding="utf-8")
 print(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
