import csv, json, random
from pathlib import Path
from miracle_lab.experiments.sweet import simulate_sweet, observable_signature

random.seed(20260921)
MECH=["ordinary_insertion","unknown_transport","local_materialization","transformation","perceptual_appearance"]
Path("data").mkdir(exist_ok=True); Path("artifacts").mkdir(exist_ok=True)
rows=[]
for mechanism in MECH:
    ideal=simulate_sweet(mechanism)
    sig=observable_signature(ideal)
    for rep in range(200):
        row={"mechanism":mechanism,"rep":rep,"target_mass_kg":0.020}
        for k,v in sig.items():
            noise=random.gauss(0, max(abs(v)*0.005,1e-9)) if k!="implied_energy_j" else random.gauss(0,max(abs(v)*0.005,1.0))
            row[k]=v+noise
        rows.append(row)
fields=list(rows[0])
with Path("data/sweet1_trials.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

# exact ideal signatures and pairwise distinguishability
ideals={m:observable_signature(simulate_sweet(m)) for m in MECH}
pairs=[]
for i,a in enumerate(MECH):
    for b in MECH[i+1:]:
        diff=[k for k in ideals[a] if abs(ideals[a][k]-ideals[b][k])>1e-12]
        pairs.append({"a":a,"b":b,"separating_observables":diff,"separable":bool(diff)})
report={"experiment":"SWEET-1","target":"20 g sweet in initially empty sealed chamber","rows":len(rows),"ideal_signatures":ideals,"pairwise":pairs,
"note":"Synthetic mechanism-discrimination benchmark only; not evidence of materialization or any extraordinary power."}
Path("artifacts/sweet1_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps({"rows":len(rows),"mechanisms":len(MECH),"unseparated_pairs":[p for p in pairs if not p["separable"]]},indent=2))
