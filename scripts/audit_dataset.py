import csv, json
from collections import Counter, defaultdict
from pathlib import Path

p=Path("data/synthetic_claim_trials.csv")
rows=list(csv.DictReader(p.open(encoding="utf-8")))
errors=[]
if len(rows)!=4200: errors.append(f"row_count={len(rows)} expected=4200")
ids=[r["trial_id"] for r in rows]
if len(ids)!=len(set(ids)): errors.append("duplicate trial_id")
required={"trial_id","capability","primary_variable","world","principal_mimic","target_signal","mimic_signal","seed"}
if rows and set(rows[0])!=required: errors.append("schema mismatch")
counts=Counter((r["capability"],r["world"]) for r in rows)
for k,v in counts.items():
    if v!=100: errors.append(f"unbalanced cell {k}={v}")
summary=defaultdict(lambda:{"n":0,"target":0.0,"mimic":0.0})
for r in rows:
    k=(r["capability"],r["world"]); d=summary[k]
    d["n"]+=1; d["target"]+=float(r["target_signal"]); d["mimic"]+=float(r["mimic_signal"])
report={"rows":len(rows),"errors":errors,"cells":{f"{k[0]}::{k[1]}":{"n":v["n"],"mean_target":v["target"]/v["n"],"mean_mimic":v["mimic"]/v["n"]} for k,v in summary.items()}}
Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/dataset_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps({"rows":len(rows),"errors":errors},indent=2))
