import csv, json, math
from collections import Counter, defaultdict
from pathlib import Path

p=Path("data/synthetic_claim_trials.csv")
rows=list(csv.DictReader(p.open(encoding="utf-8")))
errors=[]; warnings=[]
expected=4200
if len(rows)!=expected: errors.append(f"row_count={len(rows)} expected={expected}")
ids=[r["trial_id"] for r in rows]
if len(ids)!=len(set(ids)): errors.append("duplicate trial_id")
counts=Counter((r["capability"],r["world"]) for r in rows)
if len(counts)!=42: errors.append(f"cell_count={len(counts)} expected=42")
for k,v in counts.items():
    if v!=100: errors.append(f"unbalanced cell {k}={v}")

numeric=["target_signal","mimic_signal","distance_m","elapsed_s","delta_mass_kg","mass_energy_j","unsupported_force_n","information_excess_bits","authenticated_instances"]
for i,r in enumerate(rows,2):
    for k in numeric:
        try:
            x=float(r[k])
            if not math.isfinite(x): errors.append(f"nonfinite {k} row {i}")
        except Exception: errors.append(f"nonnumeric {k} row {i}")

summary=defaultdict(lambda:{"n":0,"target":0.0,"mimic":0.0})
for r in rows:
    k=(r["capability"],r["world"]); d=summary[k]; d["n"]+=1
    d["target"]+=float(r["target_signal"]); d["mimic"]+=float(r["mimic_signal"])

# Designed benchmark invariants
for cap in sorted(set(r["capability"] for r in rows)):
    lit=[r for r in rows if r["capability"]==cap and r["world"]=="literal_simulation"]
    mim=[r for r in rows if r["capability"]==cap and r["world"]=="mimic"]
    lt=sum(float(r["target_signal"]) for r in lit)/len(lit)
    lm=sum(float(r["mimic_signal"]) for r in lit)/len(lit)
    mt=sum(float(r["target_signal"]) for r in mim)/len(mim)
    mm=sum(float(r["mimic_signal"]) for r in mim)/len(mim)
    if not (lt>0.90 and lm<0.15): errors.append(f"literal separation failed: {cap}")
    if not (mt>0.70 and mm>0.70): errors.append(f"mimic ambiguity missing: {cap}")

report={"rows":len(rows),"cells":len(counts),"errors":errors,"warnings":warnings,
"interpretation":"Synthetic benchmark validation only; not empirical evidence for extraordinary phenomena.",
"summary":{f"{k[0]}::{k[1]}":{"n":v["n"],"mean_target":v["target"]/v["n"],"mean_mimic":v["mimic"]/v["n"]} for k,v in summary.items()}}
Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/dataset_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
Path("artifacts/TEST_REPORT.md").write_text("# Test report\n\nRows: %d\n\nCells: %d\n\nErrors: %d\n\n%s\n\n**Important:** this is a synthetic software benchmark, not evidence for any extraordinary phenomenon.\n" % (len(rows),len(counts),len(errors), "\n".join("- "+e for e in errors) if errors else "No dataset audit errors."),encoding="utf-8")
print(json.dumps({"rows":len(rows),"cells":len(counts),"errors":errors},indent=2))
if errors: raise SystemExit(1)
