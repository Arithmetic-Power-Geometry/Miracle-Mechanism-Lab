import streamlit as st
import pandas as pd
from dataclasses import asdict
from miracle_lab.core.state import WorldState
from miracle_lab.core.capabilities import CAPABILITIES, BY_NAME
from miracle_lab.agents.extraordinary import AGENTS
from miracle_lab.core.inversion import minimum_modification

st.set_page_config(page_title="Anomalous Capability Simulator", page_icon="🧪", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 1.5rem;}
.hero {padding: 1.2rem 1.4rem; border-radius: 18px; background: linear-gradient(135deg,#111827,#1f2937); color:white; margin-bottom:1rem;}
.hero h1 {margin:0; font-size:2.1rem;}
.hero p {opacity:.88; margin:.35rem 0 0 0;}
.card {border:1px solid #e5e7eb; border-radius:14px; padding:1rem; background:white;}
.small {font-size:.9rem; opacity:.8;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🧪 Anomalous Capability Simulator</h1><p>Explore hypothetical state transitions, ordinary mimics, and measurable consequences — without asserting that extraordinary phenomena are real.</p></div>', unsafe_allow_html=True)

st.info("Research simulator only. Outputs are synthetic model results, not empirical evidence, religious interpretation, medical advice, or proof of extraordinary powers.")

labels={f"{c.code} · {c.display_name}":c.capability for c in CAPABILITIES}
left,right=st.columns([1,1])
with left:
    selected_label=st.selectbox("Select a capability", list(labels))
    cap=labels[selected_label]
    spec=BY_NAME[cap]
    scenario=st.text_area("Describe any hypothetical outcome", "A surprising event occurs under controlled observation.")
with right:
    st.markdown("### Parameters")
    kwargs={}
    if cap in ("microform","macroform"):
        kwargs["scale"]=st.number_input("Scale factor", min_value=1e-9, max_value=1e9, value=(1e-6 if cap=="microform" else 1e6), format="%.6g")
    elif cap=="lightform":
        kwargs["mass_scale"]=st.number_input("Effective-mass scale", min_value=1e-9, max_value=1.0, value=1e-6, format="%.6g")
    elif cap=="remote_acquisition":
        kwargs["remote_information_gain"]=st.number_input("Information/access gain", min_value=0.0, value=1.0)
    elif cap=="multi_instance":
        kwargs["copies"]=st.slider("Authenticated instances",2,20,2)
    elif cap in ("gap_travel","instant_relocation"):
        kwargs["dx"]=st.number_input("Displacement (m)", min_value=0.0, value=1000.0)
    elif cap=="unsupported_ascent":
        kwargs["dz"]=st.number_input("Vertical displacement (m)", min_value=0.0, value=1.0)
    elif cap=="remote_sensing":
        kwargs["information_gain"]=st.number_input("Information gain", min_value=0.0, value=1.0)
    elif cap=="future_sensing":
        kwargs["horizon"]=st.number_input("Prediction horizon (s)", min_value=0.0, value=60.0)
    elif cap=="accelerated_recovery":
        kwargs["viability_gain"]=st.slider("Viability gain",0.0,1.0,0.5,0.05)
    elif cap=="local_emergence":
        kwargs["delta_mass_kg"]=st.number_input("Local mass increase (kg)", min_value=0.0, value=0.020, format="%.6f")

if st.button("✨ Run simulation", type="primary", use_container_width=True):
    state=WorldState()
    result=AGENTS[spec.family].simulate(cap,state,**kwargs)
    delta={k:v for k,v in result.required_delta.items() if abs(v)>0}
    obs={}
    if cap in ("gap_travel","instant_relocation"):
        obs={"distance_m":abs(kwargs.get("dx",1000.0)),"elapsed_s":1e-6 if cap=="instant_relocation" else 60.0}
    elif cap in ("dual_presence","multi_instance"):
        obs={"authenticated_instances":2.0 if cap=="dual_presence" else float(kwargs.get("copies",2))}
    elif cap=="unsupported_ascent":
        obs={"unsupported_force_n":70.0*9.80665}
    elif cap=="local_emergence":
        dm=kwargs.get("delta_mass_kg",0.020); obs={"mass_energy_j":dm*(299792458.0**2)}
    elif cap in ("remote_sensing","future_sensing","remote_acquisition"):
        obs={"information_excess_bits":16.0}
    elif cap=="microform":
        obs={"volume_ratio":kwargs.get("scale",1e-6)}
    elif cap=="macroform":
        obs={"volume_ratio":kwargs.get("scale",1e6)}
    elif cap=="lightform":
        obs={"effective_mass_ratio":kwargs.get("mass_scale",1e-6)}
    elif cap=="observer_dropout":
        obs={"observer_access":0.0}
    elif cap=="accelerated_recovery":
        obs={"viability_gain":kwargs.get("viability_gain",0.5)}

    mod=minimum_modification(cap,obs)
    st.success(f"Simulation complete: {spec.display_name}")
    a,b,c=st.columns(3)
    a.metric("Capability code", spec.code)
    b.metric("Changed state variables", len(delta))
    c.metric("Ordinary mimic", spec.principal_mimic)

    st.markdown("### What changed?")
    if delta:
        st.dataframe(pd.DataFrame([{"variable":k,"delta":v} for k,v in delta.items()]), use_container_width=True, hide_index=True)
    else:
        st.write("No state variable changed under this parameterization.")

    st.markdown("### How the model realizes the outcome")
    st.write(result.notes.get("claim_model","State transition model"))
    st.write(f"**Known constraint:** {spec.known_constraint}")
    st.write(f"**Best ordinary mimic to exclude:** {spec.principal_mimic}")
    st.write(f"**Discriminating observation:** {spec.separator}")
    if mod:
        st.write(f"**Smallest modeled extension under current normalization:** {mod.name} — magnitude {mod.magnitude:.6g} {mod.unit}; normalized deviation {mod.normalized_cost:.6g}.")
    st.caption("Normalized deviations are model-dependent comparison values, not probabilities and not measurements of supernatural strength.")
    st.markdown("### Your scenario")
    st.write(scenario)
    st.warning("Interpretation: the software can simulate the requested hypothetical transition. It does not physically realize the event and does not establish that such a capability exists in nature.")

with st.expander("About this project"):
    st.write("The simulator uses neutral project-created labels and studies hypothetical capability patterns as computational models. It does not evaluate religions, scriptures, traditions, or practitioners.")
    st.write("Copyright (C) 2026 Mohammad Amir Khusru Akhtar · Apache License 2.0")
