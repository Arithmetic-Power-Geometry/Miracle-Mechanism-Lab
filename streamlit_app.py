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

st.info("Research simulator only. Outputs are synthetic model results, not empirical evidence, medical advice, or proof that an unusual capability exists.")

with st.expander("👋 New here? Start in 60 seconds", expanded=True):
    st.markdown("""
**You do not need to know any capability name. Start with an event you are curious about.**

1. Ask **what changed?** — size, mass, position, visibility, identity, information, recovery, or object inventory.
2. Pick the closest capability below. The name is only a modeling shortcut.
3. Change one parameter and run the simulation.
4. Read **ordinary mimic** first. A surprising outcome is not automatically an unusual mechanism.
5. Read **discriminating observation** to see what a real test would need to measure.

**Example questions:** “What would have to change for a 20 g object to appear in a closed chamber?” · “What measurements distinguish hidden transport from instant relocation?” · “What would count as information arriving without an ordinary channel?”
""")

GUIDE = {
"microform":("Something becomes dramatically smaller","What variables must change if an object's effective size falls by a million-fold?"),
"macroform":("Something becomes dramatically larger","What must change if effective spatial extent increases enormously?"),
"lightform":("Something behaves as if much lighter","What measurements distinguish reduced effective mass from hidden support?"),
"remote_acquisition":("Something is accessed without an observed route","What would separate remote access from hidden cues or ordinary delivery?"),
"observer_dropout":("Something present stops being detected","What sensors distinguish observer dropout from camouflage or occlusion?"),
"multi_instance":("Several matching instances appear","What evidence distinguishes multiple instances from substitutes or recordings?"),
"dual_presence":("The same identity appears at separated places","What continuous provenance measurements would be required?"),
"gap_travel":("A large journey has an unobserved segment","What observations distinguish an unseen ordinary route from a path gap?"),
"instant_relocation":("Position changes with no observed intermediate path","How do distance and elapsed time change the modeled constraint residual?"),
"unsupported_ascent":("Something rises without an identified support","What force measurements could exclude hidden support?"),
"remote_sensing":("Information seems available without an identified channel","What blinded test would distinguish information gain from leakage?"),
"future_sensing":("Information seems available before the outcome","What timing and randomization separate prediction from selection effects?"),
"accelerated_recovery":("Recovery is unusually fast","How should an unusual recovery trajectory be compared with controls?"),
"local_emergence":("An object or mass appears locally without an identified source","What mass, energy, provenance, and chamber measurements would be needed?")
}

SCENARIOS = {
"An object appears in a monitored chamber":("local_emergence",{"delta_mass_kg":0.020}),
"An object changes position with no observed intermediate path":("instant_relocation",{"dx":1000.0}),
"A journey contains a large unobserved segment":("gap_travel",{"dx":1000.0}),
"An object rises without an identified support":("unsupported_ascent",{"dz":1.0}),
"An object becomes dramatically smaller":("microform",{"scale":1e-6}),
"An object becomes dramatically larger":("macroform",{"scale":1e6}),
"An object behaves as if its effective mass is much lower":("lightform",{"mass_scale":1e-6}),
"A present object stops being detected":("observer_dropout",{}),
"Several matching instances appear at once":("multi_instance",{"copies":2}),
"The same identity appears at separated locations":("dual_presence",{}),
"Information appears without an identified ordinary channel":("remote_sensing",{"information_gain":1.0}),
"Information appears before the later outcome":("future_sensing",{"horizon":60.0}),
"Something is accessed without an observed route":("remote_acquisition",{"remote_information_gain":1.0}),
"Recovery is unusually fast":("accelerated_recovery",{"viability_gain":0.5}),
}

labels={f"{x.code} · {x.display_name}":x.capability for x in CAPABILITIES}
cap_to_label={v:k for k,v in labels.items()}

if "scenario_text" not in st.session_state:
    st.session_state.scenario_text="An object appears in a monitored chamber"
if "capability_label" not in st.session_state:
    st.session_state.capability_label=cap_to_label["local_emergence"]

def apply_scenario():
    text=st.session_state.scenario_picker
    if text in SCENARIOS:
        cap_name,defaults=SCENARIOS[text]
        st.session_state.capability_label=cap_to_label[cap_name]
        st.session_state.scenario_text=text
        for key,value in defaults.items():
            st.session_state[f"param_{key}"]=value
    else:
        st.session_state.scenario_text=text

left,right=st.columns([1,1])
with left:
    scenario_choice=st.selectbox(
        "What are you curious about?",
        list(SCENARIOS),
        key="scenario_picker",
        on_change=apply_scenario,
        help="Pick a ready-made scenario. It automatically selects a matching model and sensible editable defaults."
    )
    st.caption("Select a starting scenario, then edit the description below if you want something more specific.")
    scenario=st.text_input(
        "Your editable question / scenario",
        key="scenario_text",
        help="You can rewrite this freely. The selected model and parameters remain editable."
    )
    selected_label=st.selectbox(
        "Suggested capability model — editable",
        list(labels),
        key="capability_label",
        help="Automatically aligned to the selected scenario. Change it if you want to compare another explanation."
    )
    cap=labels[selected_label]
    spec=BY_NAME[cap]
    st.markdown(f"**Best for:** {GUIDE[cap][0]}")
    st.caption(f"Suggested question: {GUIDE[cap][1]}")
    with st.expander("Why this model? / Choose another"):
        st.write("The scenario sets only a starting model. Nothing is locked. You can choose another capability and compare the results.")
        st.markdown("""
- **Size/shape:** Microform or Macroform
- **Effective weight/support:** Lightform or Unsupported Ascent
- **Movement/location:** Gap Travel or Instant Relocation
- **Detection:** Observer Dropout
- **Instances/identity:** Multi-Instance or Dual Presence
- **Information:** Remote Sensing, Future Sensing, or Remote Acquisition
- **Recovery:** Accelerated Recovery
- **Object/mass appearance:** Local Emergence
""")

with right:
    st.markdown("### Parameters — defaults are editable")
    kwargs={}
    if cap in ("microform","macroform"):
        default=1e-6 if cap=="microform" else 1e6
        kwargs["scale"]=st.number_input("Scale factor",min_value=1e-9,max_value=1e9,value=float(st.session_state.get("param_scale",default)),format="%.6g",key=f"input_scale_{cap}")
    elif cap=="lightform":
        kwargs["mass_scale"]=st.number_input("Effective-mass scale",min_value=1e-9,max_value=1.0,value=float(st.session_state.get("param_mass_scale",1e-6)),format="%.6g")
    elif cap=="remote_acquisition":
        kwargs["remote_information_gain"]=st.number_input("Information/access gain",min_value=0.0,value=float(st.session_state.get("param_remote_information_gain",1.0)))
    elif cap=="multi_instance":
        kwargs["copies"]=st.slider("Authenticated instances",2,20,int(st.session_state.get("param_copies",2)))
    elif cap in ("gap_travel","instant_relocation"):
        kwargs["dx"]=st.number_input("Displacement (m)",min_value=0.0,value=float(st.session_state.get("param_dx",1000.0)),key=f"input_dx_{cap}")
    elif cap=="unsupported_ascent":
        kwargs["dz"]=st.number_input("Vertical displacement (m)",min_value=0.0,value=float(st.session_state.get("param_dz",1.0)))
    elif cap=="remote_sensing":
        kwargs["information_gain"]=st.number_input("Information gain",min_value=0.0,value=float(st.session_state.get("param_information_gain",1.0)))
    elif cap=="future_sensing":
        kwargs["horizon"]=st.number_input("Prediction horizon (s)",min_value=0.0,value=float(st.session_state.get("param_horizon",60.0)))
    elif cap=="accelerated_recovery":
        kwargs["viability_gain"]=st.slider("Viability gain",0.0,1.0,float(st.session_state.get("param_viability_gain",0.5)),0.05)
    elif cap=="local_emergence":
        kwargs["delta_mass_kg"]=st.number_input("Local mass increase (kg)",min_value=0.0,value=float(st.session_state.get("param_delta_mass_kg",0.020)),format="%.6f")
    st.caption("Defaults come from the selected scenario. Every displayed value can be changed before running the simulation.")

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

    st.markdown("### Result in plain language")
    st.write(f"The simulator changed **{', '.join(delta) if delta else 'no tracked state variable'}** to represent the selected hypothetical outcome.")
    st.write("This tells you what the model had to change; it does **not** tell you that this is what happened in the physical world.")
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

with st.expander("How to read a result"):
    st.markdown("""
**Changed state variables** = what the software altered.  
**Known constraint** = an ordinary rule/accounting condition the scenario presses against.  
**Ordinary mimic** = a conventional explanation capable of producing a similar observation.  
**Discriminating observation** = a measurement intended to separate those explanations.  
**Normalized deviation** = a model-dependent comparison number, not a probability or a power score.
""")

with st.expander("About this project"):
    st.write("The simulator uses project-created neutral labels and studies hypothetical capability patterns as computational models.")
    st.write("Copyright (C) 2026 Mohammad Amir Khusru Akhtar · Apache License 2.0")
