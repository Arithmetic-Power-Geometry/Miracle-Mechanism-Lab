"""ACS three-stage interface for the frozen 21 generic experiments."""
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

st.set_page_config(page_title="ACS · 21 Experiment Lab",page_icon="🧪",layout="wide")
if "gx_screen" not in st.session_state: st.session_state.gx_screen="briefing"

def visual(spec,v):
 st.markdown(f"### {spec.symbol} {spec.code} · {spec.title}")
 st.caption(f"{spec.arena} · {v.left} → {v.right}")
 st.info(v.caption)

st.title("Anomalous Capability Simulator (ACS)")
st.caption("21 generic experiments · examples are nested cases, not additional experiments")

if st.session_state.gx_screen=="briefing":
 st.markdown("## 01 // MISSION BRIEFING")
 choice=st.selectbox("Generic Experiment",tuple(DISPLAY_TO_KEY))
 key=DISPLAY_TO_KEY[choice]; spec=UI_EXPERIMENTS[key]; example=st.selectbox("Example / tradition-neutral report",spec.examples)
 visual(spec,V[key])
 st.markdown(f"**Mathematical signature:** `{spec.mathematics}`")
 st.markdown("### Parameters")
 params={}
 for ps in PARAMETERS[key]:
  kwargs={"value":int(ps.default) if ps.integer else float(ps.default),"key":f"gx_{key}_{ps.name}","help":ps.description or None}
  if ps.minimum is not None: kwargs["min_value"]=int(ps.minimum) if ps.integer else float(ps.minimum)
  if ps.maximum is not None: kwargs["max_value"]=int(ps.maximum) if ps.integer else float(ps.maximum)
  if ps.step is not None: kwargs["step"]=int(ps.step) if ps.integer else float(ps.step)
  label=ps.label + (f" [{ps.unit}]" if ps.unit else "")
  params[ps.name]=st.number_input(label,**kwargs)
 st.markdown("**Required measurements:** "+ " · ".join(spec.measurements))
 if st.button("ENTER EXPERIMENT →",type="primary",use_container_width=True):
  st.session_state.gx_mission=freeze_mission(key,example,params)
  st.session_state.gx_screen="experiment"; st.rerun()

elif st.session_state.gx_screen=="experiment":
 m=st.session_state.gx_mission; spec=UI_EXPERIMENTS[m.experiment]; v=V[m.experiment]
 st.markdown("## 02 // EXPERIMENT")
 visual(spec,v)
 st.write(f"**Frozen example:** {m.example}")
 st.json(dict(m.parameters))
 st.markdown("### Measurement console")
 observed=[]
 for x in spec.measurements:
  if st.checkbox(x,key=f"obs_{m.code}_{x}"): observed.append(x)
 st.caption("Unchecked required measurements remain epistemically unresolved; the simulator never silently treats them as observed.")
 if st.button("▶ EXECUTE FROZEN EXPERIMENT",type="primary",use_container_width=True):
  st.session_state.gx_result=execute_mission(m); st.session_state.gx_observed=tuple(observed)
  st.session_state.gx_screen="results"; st.rerun()
 if st.button("← EDIT MISSION"):
  st.session_state.gx_screen="briefing"; st.rerun()

else:
 m=st.session_state.gx_mission; result=st.session_state.gx_result
 spec=UI_EXPERIMENTS[m.experiment]; report=build_report(result,st.session_state.get("gx_observed",()))
 st.markdown("## 03 // EVIDENCE REPORT")
 visual(spec,V[m.experiment])
 st.write(f"**Example:** {m.example}")
 st.markdown("### Mathematics")
 st.code(report.mathematics)
 for e in report.equations: st.code(e)
 st.markdown("### Quantitative outputs"); st.json(report.outputs)
 st.markdown("### Competing explanations")
 for x in report.alternatives: st.write("• "+x)
 st.markdown("### CTC experimental design")
 ctc=solve_experiment(m.experiment)
 st.write("**Minimum separating set:** "+(" · ".join(ctc["exact"].selected) or "none"))
 st.write(f'**Exact fixed cost:** {ctc["exact"].total_cost:g} · **Greedy fixed cost:** {ctc["greedy"][1]:g}')
 mechanisms,measurements=ctc["mechanisms"],ctc["measurements"]
 adaptive=optimal_adaptive_plan(mechanisms,measurements)
 st.write(f'**Deterministic adaptive worst-case cost:** {adaptive.worst_case_cost:g}')
 nm,ne=noisy_experiment(m.experiment,"moderate")
 cols=st.columns(3)
 for col,acc in zip(cols,(.90,.95,.99)):
  ns=probabilistic_resolution_summary(nm,ne,acc)
  col.metric(f"Noisy {int(acc*100)}% max pair cost",f'{ns["max_pair_cost"]:g}')
 prior={x:1/len(nm) for x in nm}
 nxt=choose_next(prior,ne)
 st.write(f"**Adaptive noisy first measurement:** {nxt or 'no admissible measurement'}")
 st.caption("Noisy values use the synthetic moderate benchmark regime; they are not empirical effect estimates.")
 st.markdown("### Resolution boundary")
 if report.resolution_status=="UNRESOLVED":
  st.warning("UNRESOLVED — missing required measurements: "+", ".join(report.unresolved))
 else:
  st.success("Resolved for the declared measurement set. This does not establish the extraordinary interpretation.")
 st.write(report.interpretation); st.caption(report.boundary)
 if st.button("← RUN / REVIEW AGAIN"):
  st.session_state.gx_screen="experiment"; st.rerun()
