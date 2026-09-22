"""ACS immersive three-stage game-zone interface for the canonical 21 experiments."""
import json
import streamlit as st
from miracle_lab.core.ui_catalogue import UI_EXPERIMENTS,DISPLAY_TO_KEY
from miracle_lab.core.parameter_specs import PARAMETERS
from miracle_lab.core.mission_config import freeze_mission,execute_mission
from miracle_lab.core.visual_catalogue import V
from miracle_lab.core.evidence_report import build_report
from miracle_lab.core.generic_ctc import solve_experiment
from miracle_lab.core.ctc_adaptive import optimal_adaptive_plan
from miracle_lab.core.noisy_benchmark import noisy_experiment
from miracle_lab.core.ctc_probabilistic import probabilistic_resolution_summary
from miracle_lab.core.noisy_adaptive import choose_next

st.set_page_config(page_title="ACS Game Zone · 21 Experiment Lab",page_icon="🎮",layout="wide")

st.markdown("""<style>
.block-container{padding-top:1rem;max-width:1500px}.gx-card{border:1px solid #4443;border-radius:18px;padding:1rem 1.2rem;margin:.35rem 0;background:linear-gradient(135deg,#1111,#8881)}
.gx-kpi{font-size:1.35rem;font-weight:800}.gx-small{opacity:.75;font-size:.9rem}.gx-stage{letter-spacing:.16em;font-size:.78rem;font-weight:800}.gx-console{font-family:monospace;border-left:4px solid #888;padding:.8rem 1rem;background:#8881}.gx-ok{font-weight:800}
</style>""",unsafe_allow_html=True)

if "gx_screen" not in st.session_state: st.session_state.gx_screen="briefing"
if "gx_score" not in st.session_state: st.session_state.gx_score=0
if "gx_runs" not in st.session_state: st.session_state.gx_runs=0

def visual(spec,v):
 st.markdown(f'<div class="gx-card"><div class="gx-stage">{spec.arena}</div><div class="gx-kpi">{spec.symbol} {spec.code} · {spec.title}</div><div class="gx-small">{v.left} → {v.right}</div><p>{v.caption}</p></div>',unsafe_allow_html=True)

def progress():
 order={"briefing":1,"experiment":2,"results":3}
 n=order.get(st.session_state.gx_screen,1)
 st.progress(n/3,text=f"Mission stage {n}/3")
 a,b=st.columns(2)
 a.metric("Completed runs",st.session_state.gx_runs)
 b.metric("Lab score",st.session_state.gx_score,help="Interface progress score only; not a scientific result.")

st.title("🎮 Anomalous Capability Simulator · Game Zone")
st.caption("21 neutral experiment missions · synthetic computational lab · no extraordinary claim is treated as established")
progress()

if st.session_state.gx_screen=="briefing":
 st.markdown("## 01 // MISSION BRIEFING")
 st.write("Choose a mission, inspect the observable signature, tune the model, then lock the mission before entering the lab.")
 choice=st.selectbox("Choose experiment",tuple(DISPLAY_TO_KEY))
 key=DISPLAY_TO_KEY[choice]; spec=UI_EXPERIMENTS[key]; example=st.selectbox("Scenario",spec.examples)
 visual(spec,V[key])
 c1,c2,c3=st.columns(3)
 c1.metric("Required measurements",len(spec.measurements))
 c2.metric("Alternative explanations",len(spec.discriminators))
 c3.metric("Family",spec.family)
 st.markdown("### Mission objective")
 st.info(f"Test the declared observable relation using {', '.join(spec.measurements)} while checking alternatives such as {', '.join(spec.discriminators)}.")
 st.markdown(f"**Mathematical signature:** `{spec.mathematics}`")
 st.markdown("### Parameter loadout")
 params={}
 for ps in PARAMETERS[key]:
  kwargs={"value":int(ps.default) if ps.integer else float(ps.default),"key":f"gx_{key}_{ps.name}","help":ps.description or None}
  if ps.minimum is not None: kwargs["min_value"]=int(ps.minimum) if ps.integer else float(ps.minimum)
  if ps.maximum is not None: kwargs["max_value"]=int(ps.maximum) if ps.integer else float(ps.maximum)
  if ps.step is not None: kwargs["step"]=int(ps.step) if ps.integer else float(ps.step)
  label=ps.label + (f" [{ps.unit}]" if ps.unit else "")
  params[ps.name]=st.number_input(label,**kwargs)
 with st.expander("Measurement plan",expanded=True):
  for x in spec.measurements: st.write("✅ Required:",x)
  for x in spec.discriminators: st.write("🧩 Alternative to test:",x)
 if st.button("LOCK MISSION & ENTER LAB →",type="primary",use_container_width=True):
  st.session_state.gx_mission=freeze_mission(key,example,params)
  st.session_state.gx_screen="experiment"; st.rerun()

elif st.session_state.gx_screen=="experiment":
 m=st.session_state.gx_mission; spec=UI_EXPERIMENTS[m.experiment]; v=V[m.experiment]
 st.markdown("## 02 // EXPERIMENT ZONE")
 visual(spec,v)
 st.write(f"**Scenario locked:** {m.example}")
 c1,c2=st.columns([1,1])
 with c1:
  st.markdown("### Frozen configuration")
  st.json(dict(m.parameters))
 with c2:
  st.markdown("### Mission checklist")
  observed=[]
  for x in spec.measurements:
   if st.checkbox(f"Observe · {x}",key=f"obs_{m.code}_{x}"): observed.append(x)
  st.caption(f"{len(observed)}/{len(spec.measurements)} required measurements declared observed.")
 st.markdown("### Live lab console")
 st.markdown(f'<div class="gx-console">MODEL: {m.code}<br>SCENARIO: {m.example}<br>OBSERVED: {", ".join(observed) if observed else "none"}<br>STATUS: READY</div>',unsafe_allow_html=True)
 st.warning("Unchecked measurements remain unresolved. The simulator never silently marks a measurement as observed.")
 b1,b2=st.columns([3,1])
 if b1.button("▶ EXECUTE FROZEN EXPERIMENT",type="primary",use_container_width=True):
  st.session_state.gx_result=execute_mission(m); st.session_state.gx_observed=tuple(observed)
  st.session_state.gx_screen="results"; st.session_state.gx_runs+=1; st.rerun()
 if b2.button("← EDIT MISSION",use_container_width=True):
  st.session_state.gx_screen="briefing"; st.rerun()

else:
 m=st.session_state.gx_mission; result=st.session_state.gx_result
 spec=UI_EXPERIMENTS[m.experiment]; observed=st.session_state.get("gx_observed",())
 report=build_report(result,observed)
 st.markdown("## 03 // ANALYSIS & OUTPUT ZONE")
 visual(spec,V[m.experiment])
 c1,c2,c3=st.columns(3)
 c1.metric("Observed required",f"{len(observed)}/{len(spec.measurements)}")
 c2.metric("Output fields",len(report.outputs))
 c3.metric("Resolution","Resolved*" if report.resolution_status!="UNRESOLVED" else "Unresolved")
 st.markdown("### Mission result")
 st.info(report.interpretation)
 st.markdown("### Mathematics")
 st.code(report.mathematics)
 for e in report.equations: st.code(e)
 st.markdown("### Quantitative output console")
 st.json(report.outputs)
 st.download_button("⬇ Download this result JSON",json.dumps({
  "experiment":m.experiment,"code":m.code,"scenario":m.example,"parameters":dict(m.parameters),
  "observed":list(observed),"outputs":report.outputs,"resolution_status":report.resolution_status,
  "boundary":report.boundary
 },indent=2,default=str),file_name=f"{m.code.lower()}_result.json",mime="application/json")
 st.markdown("### Alternative-explanation challenge")
 for i,x in enumerate(report.alternatives,1): st.write(f"**{i}. {x}** — the current output does not remove this explanation unless the required discriminating measurements support doing so.")
 st.markdown("### CTC strategy console")
 ctc=solve_experiment(m.experiment)
 mechanisms,measurements=ctc["mechanisms"],ctc["measurements"]
 adaptive=optimal_adaptive_plan(mechanisms,measurements)
 a,b,c=st.columns(3)
 a.metric("Exact fixed cost",f'{ctc["exact"].total_cost:g}')
 b.metric("Greedy fixed cost",f'{ctc["greedy"][1]:g}')
 c.metric("Adaptive worst-case",f'{adaptive.worst_case_cost:g}')
 st.write("**Minimum separating set:** "+(" · ".join(ctc["exact"].selected) or "none"))
 nm,ne=noisy_experiment(m.experiment,"moderate")
 cols=st.columns(3)
 for col,acc in zip(cols,(.90,.95,.99)):
  ns=probabilistic_resolution_summary(nm,ne,acc)
  col.metric(f"Synthetic {int(acc*100)}% pair cost",f'{ns["max_pair_cost"]:g}')
 prior={x:1/len(nm) for x in nm}; nxt=choose_next(prior,ne)
 st.write(f"**Suggested first noisy measurement:** {nxt or 'no admissible measurement'}")
 st.caption("CTC/noisy values are synthetic benchmark quantities used to test discrimination algorithms, not empirical effect estimates.")
 st.markdown("### Resolution boundary")
 if report.resolution_status=="UNRESOLVED":
  st.warning("UNRESOLVED — missing required measurements: "+", ".join(report.unresolved))
  reward=5
 else:
  st.success("Resolved relative to the declared synthetic measurement set. This does not establish an extraordinary interpretation.")
  reward=20
 st.caption(report.boundary)
 if "gx_last_rewarded" not in st.session_state or st.session_state.gx_last_rewarded!=st.session_state.gx_runs:
  st.session_state.gx_score+=reward; st.session_state.gx_last_rewarded=st.session_state.gx_runs
 st.success(f"Game-zone progress +{reward} points. This score measures interface completion only.")
 b1,b2=st.columns(2)
 if b1.button("↻ REVIEW / RE-RUN",use_container_width=True):
  st.session_state.gx_screen="experiment"; st.rerun()
 if b2.button("🎮 NEW MISSION",type="primary",use_container_width=True):
  st.session_state.gx_screen="briefing"; st.rerun()
