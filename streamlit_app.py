import streamlit as st
import pandas as pd
import math
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
.small {font-size:.9rem; opacity:.8;}\n.flowbox {border:1px solid #d1d5db; border-radius:16px; padding:1rem; text-align:center; font-weight:600; min-height:82px;}
.game-scene {position:relative; overflow:hidden; min-height:270px; border-radius:24px; padding:24px; background:linear-gradient(160deg,#0f172a,#1e293b); color:white; border:1px solid #334155; box-shadow:0 14px 38px rgba(15,23,42,.22);}
.game-title {font-size:1rem; opacity:.72; letter-spacing:.12em; font-weight:700;}
.game-object {font-size:76px; text-align:center; margin:20px 0 6px 0; animation:floaty 2.4s ease-in-out infinite;}
.game-caption {text-align:center; font-size:1.08rem; font-weight:700;}
.game-sub {text-align:center; opacity:.72; font-size:.88rem;}
.scan {height:2px;background:#93c5fd;box-shadow:0 0 14px #93c5fd;animation:scan 2.2s linear infinite;}
@keyframes floaty {0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-12px) scale(1.04)}}
@keyframes scan {0%{transform:translateY(0);opacity:.2}50%{transform:translateY(160px);opacity:1}100%{transform:translateY(0);opacity:.2}}
@keyframes popin {0%{transform:scale(.2);opacity:0}65%{transform:scale(1.18);opacity:1}100%{transform:scale(1);opacity:1}}
.pop {animation:popin 1s ease-out;}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🧪 Anomalous Capability Simulator</h1><p>Explore hypothetical state transitions, ordinary mimics, and measurable consequences — without asserting that extraordinary phenomena are real.</p></div>', unsafe_allow_html=True)

st.info("Research simulator only. Outputs are synthetic model results, not empirical evidence, medical advice, or proof that an unusual capability exists.")

st.markdown("### How the simulator thinks")
f1,f2,f3,f4=st.columns(4)
f1.markdown('<div class="flowbox">① OBSERVATION<br><span class="small">What is reported?</span></div>',unsafe_allow_html=True)
f2.markdown('<div class="flowbox">② STATE CHANGE<br><span class="small">What variables must move?</span></div>',unsafe_allow_html=True)
f3.markdown('<div class="flowbox">③ COMPETING MODEL<br><span class="small">What ordinary route can imitate it?</span></div>',unsafe_allow_html=True)
f4.markdown('<div class="flowbox">④ SEPARATION TEST<br><span class="small">What measurement tells them apart?</span></div>',unsafe_allow_html=True)

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
"A 20 g sweet appears in a monitored chamber":("local_emergence",{"delta_mass_kg":0.020}),
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

VISUALS={
"local_emergence":("🍬","CHAMBER LAB","Object inventory changed","Mass · provenance · energy accounting"),
"instant_relocation":("📦","RELOCATION ARENA","Source → destination","Path continuity · timing · identity"),
"gap_travel":("🚗","TRACKING COURSE","A path segment is missing","Continuous tracking · checkpoints"),
"unsupported_ascent":("🎈","FORCE LAB","Upward motion under test","Force · acceleration · environment"),
"microform":("🔬","SCALE LAB","Effective extent decreases","Geometry · mass · identity"),
"macroform":("🔭","SCALE LAB","Effective extent increases","Geometry · mass · identity"),
"lightform":("🪶","MASS LAB","Effective response decreases","Force · acceleration · support"),
"observer_dropout":("👁️","SENSOR ROOM","Detection channel changes","Camera · thermal · range sensors"),
"multi_instance":("👥","IDENTITY LAB","Multiple instances","Authentication · provenance · timing"),
"dual_presence":("📍","TWIN-SITE LAB","One identity, two sites","Authentication · synchronized clocks"),
"remote_sensing":("📡","INFORMATION LAB","Unknown information route","Blinding · randomization · leakage control"),
"future_sensing":("⏱️","TIMING LAB","Information precedes target","Commitment · RNG · timestamps"),
"remote_acquisition":("🛰️","ACCESS LAB","Access without observed route","Channel audit · randomized target"),
"accelerated_recovery":("📈","TRAJECTORY LAB","Rate differs from reference","Endpoint · time course · controls"),
}

def render_game_scene(cap,scenario):
    icon,arena,title,sub=VISUALS[cap]
    st.markdown(f"""
    <div class="game-scene">
      <div class="game-title">MISSION · {arena}</div>
      <div class="scan"></div>
      <div class="game-object pop">{icon}</div>
      <div class="game-caption">{title}</div>
      <div class="game-sub">{sub}</div>
      <div style="margin-top:18px;padding:10px 12px;border-radius:12px;background:rgba(255,255,255,.07);font-size:.86rem;">🎯 {scenario}</div>
    </div>
    """,unsafe_allow_html=True)

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
    render_game_scene(cap,scenario)
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

st.markdown("### 🎮 Mission controls")
mc1,mc2,mc3=st.columns(3)
mc1.markdown("**1 · Choose**\n\nPick a scenario.")
mc2.markdown("**2 · Tune**\n\nEdit the model and parameters.")
mc3.markdown("**3 · Investigate**\n\nRun it, then challenge the explanation.")

if st.button("🚀 Launch investigation", type="primary", use_container_width=True):
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
    st.success(f"Mission simulated: {spec.display_name}")
    st.progress(100,text="Simulation complete · now inspect the evidence trail")
    render_game_scene(cap,scenario)
    a,b,c=st.columns(3)
    a.metric("Capability code", spec.code)
    b.metric("Changed state variables", len(delta))
    c.metric("Ordinary mimic", spec.principal_mimic)

    st.markdown("### 🧭 Investigation board")
    q1,q2,q3=st.columns(3)
    q1.markdown("**CLUE 1 — State**\n\nWhat changed in the modeled world?")
    q2.markdown(f"**CLUE 2 — Rival**\n\n{spec.principal_mimic}")
    q3.markdown(f"**CLUE 3 — Test**\n\n{spec.separator}")
    st.markdown("### Simulation map")
    st.caption("This is a conceptual map of the calculation, not a photograph of a physical event.")
    st.graphviz_chart(f"""
    digraph G {{
      rankdir=LR;
      node [shape=box, style="rounded"];
      A [label="Observed scenario"];
      B [label="{spec.display_name}\\n({spec.code})"];
      C [label="State transition\\n{spec.primary_variable}: {spec.expected_direction}"];
      D [label="Constraint check"];
      E [label="Ordinary mimic"];
      F [label="Discriminating test"];
      A -> B -> C -> D;
      D -> E [label="compare"];
      E -> F;
    }}
    """)

    st.markdown("### Calculation summary")
    calc_rows=[]
    for name,value in delta.items():
        before=getattr(result.before,name)
        after=getattr(result.after,name)
        calc_rows.append({"variable":name,"before":before,"after":after,"delta = after - before":value})
    if calc_rows:
        st.dataframe(pd.DataFrame(calc_rows),use_container_width=True,hide_index=True)

    with st.expander("🧮 Show exactly how this result was calculated", expanded=True):
        st.markdown("**Step 1 — Start from the baseline world state.** The simulator creates a declared baseline vector \\(X_0\\) containing position, mass, volume, viability, information access and other tracked quantities.")
        st.markdown("**Step 2 — Apply the selected transition.** The selected model changes only its declared variables, producing \\(X_1\\).")
        st.latex(r"\\Delta X = X_1 - X_0")
        if cap=="local_emergence":
            dm=kwargs.get("delta_mass_kg",0.020)
            energy=dm*(299792458.0**2)
            st.markdown(f"Here the requested local mass increase is **{dm:.6g} kg**. For accounting, the simulator computes its rest-mass energy equivalent:")
            st.latex(r"E_{eq}=\\Delta m c^2")
            st.write(f"Using c = 299,792,458 m/s gives **{energy:.6g} J**. This is an accounting equivalent, not a claim that this energy was physically observed or released.")
        elif cap in ("gap_travel","instant_relocation"):
            d=abs(kwargs.get("dx",1000.0)); elapsed=1e-6 if cap=="instant_relocation" else 60.0
            speed=d/elapsed if elapsed else math.inf
            st.latex(r"v_{required}=d/\\Delta t")
            st.write(f"With d = {d:.6g} m and modeled Δt = {elapsed:.6g} s, required average speed = **{speed:.6g} m/s**.")
        elif cap in ("microform","macroform"):
            r=kwargs.get("scale",1.0)
            st.latex(r"V_1=V_0 r")
            st.write(f"The selected volume ratio is **r = {r:.6g}**. The inversion layer uses |ln(r)| as the declared geometry-deviation coordinate.")
        elif cap=="lightform":
            r=kwargs.get("mass_scale",1.0)
            st.latex(r"m_1=m_0 r")
            st.write(f"The selected effective-mass ratio is **{r:.6g}**; the model deviation is |1-r|.")
        elif cap in ("dual_presence","multi_instance"):
            n=2 if cap=="dual_presence" else kwargs.get("copies",2)
            st.latex(r"R_{identity}=\\max(0,n-1)")
            st.write(f"For **n = {n}** authenticated instances, the identity-locality residual is **{max(0,n-1):.6g} instance(s)**.")
        elif cap=="unsupported_ascent":
            st.latex(r"F_{reference}=mg")
            st.write("The current benchmark uses a 70 kg reference state and standard gravitational acceleration 9.80665 m/s² when constructing the unsupported-force observable.")
        elif cap in ("remote_sensing","future_sensing","remote_acquisition"):
            st.write("The current synthetic benchmark assigns a declared information-excess observable and asks what ordinary signal/leakage route would have to be excluded. It is a model variable, not measured information from a real experiment.")
        elif cap=="observer_dropout":
            st.write("Observer access is changed from its baseline value to zero in the stipulated simulation. Independent sensing is then the proposed separator from occlusion or attention effects.")
        elif cap=="accelerated_recovery":
            st.write("The model changes the bounded viability state by the selected gain. A real study would require an operational endpoint, time course and matched controls; this simulator does not diagnose recovery.")
        st.markdown("**Step 3 — Invert the observation.** The inversion engine asks for the smallest declared model extension that reproduces the synthetic observation.")
        if mod:
            st.code(f"mechanism = {mod.name}\nmagnitude = {mod.magnitude:.8g} {mod.unit}\nnormalized deviation = {mod.normalized_cost:.8g}",language="text")
        st.markdown("**Step 4 — Challenge the result.** The simulator reports an ordinary mimic and a separating measurement. A model is scientifically interesting only if competing explanations can be tested rather than assumed away.")

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
    st.caption("Normalized deviations are model-dependent comparison values, not probabilities, confidence scores, evidence strength, or measurements of a real-world capability.")
    with st.expander("What does normalized deviation mean?"):
        st.write("Different residuals use different units (metres, joules, bits, instances, fractions). The inversion module divides some residual magnitudes by declared reference scales so they can be handled consistently inside the software. These scales are modeling choices. Comparing two normalized values does not establish which physical scenario is more plausible.")
    with st.expander("What would a real experiment need?"):
        st.markdown(f"""
**Measure:** {spec.primary_variable} and the variables required by the separator.  
**Exclude first:** {spec.principal_mimic}.  
**Key test:** {spec.separator}.  
**Record:** calibration, uncertainty, timing, provenance, exclusions, and the complete protocol before interpreting an unusual observation.

The simulator supplies a test architecture; it does not substitute for real measurements.
""")
    st.markdown("### Your scenario")
    st.write(scenario)
    st.warning("Interpretation: the software can simulate the requested hypothetical transition. It does not physically realize the event and does not establish that such a capability exists in nature.")

st.markdown("---")
st.markdown("## Project reference")
r1,r2,r3=st.columns(3)
r1.metric("Neutral capability models",len(CAPABILITIES))
r2.metric("Model families",len(set(x.family for x in CAPABILITIES)))
r3.metric("Benchmark design","4,200 synthetic rows")
st.markdown("""
The project separates four layers that are easy to confuse: **observation**, **model**, **constraint residual**, and **evidence**. A simulation can successfully reproduce an observation while providing zero evidence that the simulated mechanism occurs in nature.
""")

with st.expander("How to read a result"):
    st.markdown("""
**Changed state variables** = what the software altered.  
**Known constraint** = an ordinary rule/accounting condition the scenario presses against.  
**Ordinary mimic** = a conventional explanation capable of producing a similar observation.  
**Discriminating observation** = a measurement intended to separate those explanations.  
**Normalized deviation** = a model-dependent comparison number, not a probability or a power score.
""")

with st.expander("🎮 Why the game-like interface?"):
    st.write("The visual missions are an educational interface over the same deterministic research model. Animation, icons and mission language do not add evidence or change the calculations. The purpose is to make model comparison, controls and falsification easier to explore.")

with st.expander("About this project"):
    st.write("The simulator uses project-created neutral labels and studies hypothetical capability patterns as computational models.")
    st.write("Copyright (C) 2026 Mohammad Amir Khusru Akhtar · Apache License 2.0")
