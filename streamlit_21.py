"""ACS three-stage interface for the frozen 21 generic experiments."""
import streamlit as st
from miracle_lab.core.ui_catalogue import UI_EXPERIMENTS,DISPLAY_TO_KEY
from miracle_lab.core.generic_engine import DEFAULTS
from miracle_lab.core.mission_config import freeze_mission,execute_mission
from miracle_lab.core.visual_catalogue import V
from miracle_lab.core.evidence_report import build_report

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
 for p in spec.parameters:
  default=DEFAULTS[key][p]
  params[p]=st.number_input(p.replace("_"," ").title(),value=float(default),key=f"gx_{key}_{p}")
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
 st.markdown("### Resolution boundary")
 if report.resolution_status=="UNRESOLVED":
  st.warning("UNRESOLVED — missing required measurements: "+", ".join(report.unresolved))
 else:
  st.success("Resolved for the declared measurement set. This does not establish the extraordinary interpretation.")
 st.write(report.interpretation); st.caption(report.boundary)
 if st.button("← RUN / REVIEW AGAIN"):
  st.session_state.gx_screen="experiment"; st.rerun()
