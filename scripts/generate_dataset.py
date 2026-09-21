import csv, random
from pathlib import Path

random.seed(20260921)
OUT=Path("data")
OUT.mkdir(exist_ok=True)

CAPS=[
("teleportation","path_continuity","hidden_transport"),
("bilocation","authenticated_instances","identity_substitution"),
("levitation","unsupported_vertical_force","hidden_support"),
("clairvoyance","remote_information","sensory_leakage"),
("precognition","future_information","selection_or_leakage"),
("healing","recovery_rate","natural_recovery"),
("materialization","local_mass_energy","hidden_source"),
("anima","volume","optical_or_scale_error"),
("mahima","volume","perspective_or_projection"),
("laghima","effective_mass","hidden_support"),
("prapti","remote_information","hidden_cue"),
("disappearance","observer_access","occlusion_or_camouflage"),
("multiplication","authenticated_instances","substitute_or_recording"),
("extraordinary_travel","path_continuity","unobserved_transport"),
]

rows=[]
trial=0
for cap,var,mimic in CAPS:
    for world in ("baseline","mimic","literal_simulation"):
        for rep in range(100):
            trial+=1
            if world=="baseline":
                signal=random.gauss(0,0.05); alt=random.gauss(0,0.05)
            elif world=="mimic":
                signal=random.gauss(0.85,0.08); alt=random.gauss(0.90,0.06)
            else:
                signal=random.gauss(1.0,0.04); alt=random.gauss(0.05,0.04)
            rows.append([trial,cap,var,world,mimic,signal,alt,20260921+rep])

with open(OUT/"synthetic_claim_trials.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["trial_id","capability","primary_variable","world","principal_mimic","target_signal","mimic_signal","seed"])
    w.writerows(rows)
print(f"wrote {len(rows)} rows")
