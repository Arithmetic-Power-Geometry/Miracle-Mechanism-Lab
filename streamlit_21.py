"""ACS 21-experiment interface prototype.

This is intentionally separated from the legacy app until all 21 execution
models are implemented and regression-tested; it prevents a half-migrated
public interface.
"""
import streamlit as st
from miracle_lab.core.ui_catalogue import UI_EXPERIMENTS,DISPLAY_TO_KEY

st.set_page_config(page_title="ACS · 21 Experiment Lab",page_icon="🧪",layout="wide")
st.title("Anomalous Capability Simulator (ACS)")
st.caption("21 generic experiments · examples are nested cases, not extra experiments")

choice=st.selectbox("Generic Experiment",tuple(DISPLAY_TO_KEY))
key=DISPLAY_TO_KEY[choice]; spec=UI_EXPERIMENTS[key]
example=st.selectbox("Example / tradition-neutral report",spec.examples)

st.markdown(f"## {spec.symbol} {spec.code} · {spec.title}")
st.write(f"**Laboratory:** {spec.arena}")
st.write(f"**Selected example:** {example}")
st.write(f"**Mathematical signature:** `{spec.mathematics}`")

st.markdown("### Parameters to operationalize")
for p in spec.parameters: st.text_input(p.replace("_"," ").title(),key=f"gx_{key}_{p}")

st.markdown("### Required measurements")
st.write(" · ".join(spec.measurements))
st.markdown("### Competing explanations to discriminate")
st.write(" · ".join(spec.discriminators))

if st.button("ENTER EXPERIMENT →",type="primary",use_container_width=True):
 st.session_state["gx_mission"]={"experiment":key,"code":spec.code,"example":example,
   "parameters":{p:st.session_state.get(f"gx_{key}_{p}","") for p in spec.parameters}}
 st.success(f"Mission frozen: {spec.code} · {spec.title}")
 st.info("Execution remains locked until the corresponding quantitative simulator passes validation; the interface does not fabricate a result.")
