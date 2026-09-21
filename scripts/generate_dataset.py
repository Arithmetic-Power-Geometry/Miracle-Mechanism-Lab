"""Generate the canonical 21-GX synthetic benchmark dataset."""
import csv,random
from pathlib import Path
from miracle_lab.core.experiment_specs import SPECS
from miracle_lab.core.generic_engine import execute,DEFAULTS
random.seed(20260921); OUT=Path("data"); OUT.mkdir(exist_ok=True)
rows=[]; trial=0
for key,spec in SPECS.items():
 for world in ("baseline","mimic","literal_simulation"):
  for rep in range(100):
   trial+=1
   target=max(0.0,random.gauss({"baseline":.05,"mimic":.85,"literal_simulation":1.0}[world],.04))
   alt=max(0.0,random.gauss({"baseline":.05,"mimic":.90,"literal_simulation":.05}[world],.04))
   result=execute(key,DEFAULTS[key])
   rows.append({"trial_id":trial,"experiment":key,"code":spec.code,"world":world,
    "target_signal":target,"mimic_signal":alt,"seed":20260921+rep,
    "model_outputs":repr(sorted(result.outputs.items())),
    "interpretation_boundary":result.boundary})
header=("trial_id","experiment","code","world","target_signal","mimic_signal","seed","model_outputs","interpretation_boundary")
with (OUT/"synthetic_claim_trials.csv").open("w",newline="",encoding="utf-8") as f:
 w=csv.DictWriter(f,fieldnames=header); w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows across {len(SPECS)} experiments")
