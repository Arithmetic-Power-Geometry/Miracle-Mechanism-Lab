import csv,json,math
from collections import Counter,defaultdict
from pathlib import Path
p=Path("data/synthetic_claim_trials.csv"); rows=list(csv.DictReader(p.open(encoding="utf-8")))
errors=[]; expected=6300
if len(rows)!=expected: errors.append(f"row_count={len(rows)} expected={expected}")
ids=[r["trial_id"] for r in rows]
if len(ids)!=len(set(ids)): errors.append("duplicate trial_id")
counts=Counter((r["experiment"],r["world"]) for r in rows)
if len(counts)!=63: errors.append(f"cell_count={len(counts)} expected=63")
for k,v in counts.items():
 if v!=100: errors.append(f"unbalanced cell {k}={v}")
for i,r in enumerate(rows,2):
 for k in ("target_signal","mimic_signal"):
  try:
   if not math.isfinite(float(r[k])): errors.append(f"nonfinite {k} row {i}")
  except Exception: errors.append(f"nonnumeric {k} row {i}")
for key in sorted(set(r["experiment"] for r in rows)):
 lit=[r for r in rows if r["experiment"]==key and r["world"]=="literal_simulation"]
 mim=[r for r in rows if r["experiment"]==key and r["world"]=="mimic"]
 lt=sum(float(r["target_signal"]) for r in lit)/len(lit); lm=sum(float(r["mimic_signal"]) for r in lit)/len(lit)
 mt=sum(float(r["target_signal"]) for r in mim)/len(mim); mm=sum(float(r["mimic_signal"]) for r in mim)/len(mim)
 if not (lt>.90 and lm<.15): errors.append(f"literal separation failed: {key}")
 if not (mt>.70 and mm>.70): errors.append(f"mimic ambiguity missing: {key}")
report={"rows":len(rows),"cells":len(counts),"experiments":len(set(r["experiment"] for r in rows)),"errors":errors,
 "interpretation":"Synthetic benchmark validation only; not empirical evidence for extraordinary phenomena."}
Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/dataset_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
Path("artifacts/TEST_REPORT.md").write_text(f"# Test report\n\nRows: {len(rows)}\n\nCells: {len(counts)}\n\nExperiments: {report['experiments']}\n\nErrors: {len(errors)}\n\n**Important:** synthetic software benchmark only; not empirical evidence.\n",encoding="utf-8")
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
