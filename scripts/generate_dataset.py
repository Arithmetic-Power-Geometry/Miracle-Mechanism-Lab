import csv, random, math
from pathlib import Path
from miracle_lab.core.constraints import C

random.seed(20260921)
OUT=Path("data"); OUT.mkdir(exist_ok=True)

CAPS=[
("instant_relocation","locality_m","hidden_transport"),("dual_presence","identity_excess_instances","identity_substitution"),
("unsupported_ascent","unsupported_force_n","hidden_support"),("remote_sensing","information_excess_bits","sensory_leakage"),
("future_sensing","information_excess_bits","selection_or_leakage"),("accelerated_recovery","viability_gain","natural_recovery"),
("local_emergence","mass_energy_j","hidden_source"),("microform","volume_ratio","optical_or_scale_error"),
("macroform","volume_ratio","perspective_or_projection"),("lightform","effective_mass_ratio","hidden_support"),
("remote_acquisition","information_excess_bits","hidden_cue"),("observer_dropout","observer_access","occlusion_or_camouflage"),
("multi_instance","identity_excess_instances","substitute_or_recording"),("gap_travel","locality_m","unobserved_transport"),
]

rows=[]; trial=0
for cap,var,mimic in CAPS:
    for world in ("baseline","mimic","literal_simulation"):
        for rep in range(100):
            trial+=1
            target=max(0.0,random.gauss({"baseline":0.05,"mimic":0.85,"literal_simulation":1.0}[world],0.04))
            alt=max(0.0,random.gauss({"baseline":0.05,"mimic":0.90,"literal_simulation":0.05}[world],0.04))
            distance=1000.0 if cap in ("instant_relocation","gap_travel") else 0.0
            elapsed=0.000001 if cap=="instant_relocation" and world=="literal_simulation" else (60.0 if distance else 0.0)
            mass_delta=1.0 if cap=="local_emergence" and world=="literal_simulation" else 0.0
            energy=mass_delta*C*C
            force=70.0*9.80665 if cap=="unsupported_ascent" and world=="literal_simulation" else 0.0
            info=16.0 if cap in ("remote_sensing","future_sensing","remote_acquisition") and world=="literal_simulation" else 0.0
            identities=2.0 if cap in ("dual_presence","multi_instance") and world=="literal_simulation" else 1.0
            volume_ratio = (1e-6 if cap=="microform" and world=="literal_simulation" else (1e6 if cap=="macroform" and world=="literal_simulation" else 1.0))
            effective_mass_ratio = 1e-6 if cap=="lightform" and world=="literal_simulation" else 1.0
            observer_access = 0.0 if cap=="observer_dropout" and world=="literal_simulation" else 1.0
            viability_gain = 0.5 if cap=="accelerated_recovery" and world=="literal_simulation" else 0.0
            rows.append([trial,cap,var,world,mimic,target,alt,distance,elapsed,mass_delta,energy,force,info,identities,volume_ratio,effective_mass_ratio,observer_access,viability_gain,20260921+rep])

header=["trial_id","capability","primary_residual","world","principal_mimic","target_signal","mimic_signal","distance_m","elapsed_s","delta_mass_kg","mass_energy_j","unsupported_force_n","information_excess_bits","authenticated_instances","volume_ratio","effective_mass_ratio","observer_access","viability_gain","seed"]
with open(OUT/"synthetic_claim_trials.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(header); w.writerows(rows)
print(f"wrote {len(rows)} rows")
