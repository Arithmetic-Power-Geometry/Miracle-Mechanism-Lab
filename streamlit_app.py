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
.hud {background:#07110d;border:1px solid #1f6f4a;border-radius:10px;color:#9fffc8;padding:12px 15px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;box-shadow:inset 0 0 22px rgba(34,197,94,.07);}
.hudline {display:flex;justify-content:space-between;gap:10px;font-size:.78rem;letter-spacing:.06em;margin:3px 0;}
.objective {border-left:3px solid #22c55e;padding:8px 12px;background:rgba(34,197,94,.06);margin:8px 0;}
.reticle {width:92px;height:92px;border:1px solid rgba(147,197,253,.7);border-radius:50%;margin:12px auto;position:relative;box-shadow:0 0 24px rgba(59,130,246,.25);}
.reticle:before,.reticle:after {content:"";position:absolute;background:rgba(147,197,253,.8);}
.reticle:before {width:120px;height:1px;left:-15px;top:45px;}
.reticle:after {width:1px;height:120px;left:45px;top:-15px;}
.statusdot {display:inline-block;width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;margin-right:6px;}


.stage{min-height:430px;background:radial-gradient(circle at 50% 55%,#18344a 0,#08111c 52%,#03070c 100%);}
.stage-grid{position:absolute;left:0;right:0;bottom:0;height:48%;background-image:linear-gradient(rgba(74,222,128,.12) 1px,transparent 1px),linear-gradient(90deg,rgba(74,222,128,.12) 1px,transparent 1px);background-size:34px 34px;transform:perspective(280px) rotateX(55deg);transform-origin:bottom;}
.actor{position:relative;z-index:3;font-size:88px;text-align:center;margin:92px auto 20px;width:130px;filter:drop-shadow(0 0 18px rgba(125,211,252,.45));}
.origin,.destination{position:absolute;bottom:70px;font:700 12px ui-monospace;color:#86efac;border:1px solid #166534;padding:5px 9px;border-radius:6px}.origin{left:10%}.destination{right:10%}
.emerge{animation:emerge 2.1s ease-in-out infinite}.teleport{animation:teleport 2.8s steps(1,end) infinite}.travel{animation:travel 3.5s ease-in-out infinite}.ascend{animation:ascend 2.6s ease-in-out infinite}.shrink{animation:shrink 2.8s ease-in-out infinite}.grow{animation:grow 2.8s ease-in-out infinite}.float{animation:floaty 2.1s ease-in-out infinite}.fade{animation:fade 2.8s ease-in-out infinite}.duplicate{animation:duplicate 2.8s ease-in-out infinite}.signal{animation:signal 1.7s ease-in-out infinite}.pulse{animation:pulse 1.5s ease-in-out infinite}
@keyframes emerge{0%,25%{opacity:0;transform:scale(.05) rotate(-30deg)}60%,100%{opacity:1;transform:scale(1) rotate(0)}}@keyframes teleport{0%,42%{transform:translateX(-260px);opacity:1}43%,55%{opacity:0}56%,100%{transform:translateX(260px);opacity:1}}@keyframes travel{0%{transform:translateX(-260px)}50%{opacity:.1}100%{transform:translateX(260px)}}@keyframes ascend{0%,100%{transform:translateY(70px)}50%{transform:translateY(-80px)}}@keyframes shrink{0%,100%{transform:scale(1)}50%{transform:scale(.16)}}@keyframes grow{0%,100%{transform:scale(.35)}50%{transform:scale(1.55)}}@keyframes fade{0%,100%{opacity:1}50%{opacity:.05;filter:blur(5px)}}@keyframes duplicate{0%,100%{text-shadow:0 0 transparent}50%{text-shadow:-80px 0 0 rgba(255,255,255,.75),80px 0 0 rgba(255,255,255,.75)}}@keyframes signal{0%,100%{filter:drop-shadow(0 0 5px #38bdf8)}50%{filter:drop-shadow(0 0 40px #38bdf8);transform:scale(1.15)}}@keyframes pulse{0%,100%{transform:scale(.9);opacity:.65}50%{transform:scale(1.15);opacity:1}}
</style>
""", unsafe_allow_html=True)

# Three-screen mission flow -------------------------------------------------
if "screen" not in st.session_state:
    st.session_state.screen="briefing"
if "last_result" not in st.session_state:
    st.session_state.last_result=None

st.markdown('<div class="hero"><h1>ACS // FIELD LAB</h1><p>Interactive anomaly-model investigation console</p></div>', unsafe_allow_html=True)

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
    mission_id=f"ACS-{list(BY_NAME).index(cap)+1:02d}"
    objective={
      "local_emergence":"Secure chamber telemetry. Verify inventory. Exclude hidden source.",
      "instant_relocation":"Lock source and destination. Track continuity. Authenticate object.",
      "gap_travel":"Recover missing path segment from independent checkpoints.",
      "unsupported_ascent":"Map all support forces before classifying the motion.",
      "microform":"Calibrate geometry, mass and identity before and after transition.",
      "macroform":"Calibrate geometry, mass and identity before and after transition.",
      "lightform":"Measure force, acceleration and every candidate support channel.",
      "observer_dropout":"Cross-check optical, thermal and independent sensor channels.",
      "multi_instance":"Synchronize clocks and authenticate every reported instance.",
      "dual_presence":"Authenticate both sites under synchronized continuous recording.",
      "remote_sensing":"Seal information channels, randomize target and preserve blinding.",
      "future_sensing":"Commit prediction before target generation and lock timestamps.",
      "remote_acquisition":"Audit all access channels before testing the unexplained route.",
      "accelerated_recovery":"Define endpoint and reference trajectory before comparison."
    }[cap]
    st.markdown(f"""
    <div class="game-scene">
      <div class="hud">
        <div class="hudline"><span><span class="statusdot"></span>FIELD SYSTEM ONLINE</span><span>{mission_id}</span></div>
        <div class="hudline"><span>ZONE: {arena}</span><span>MODE: INVESTIGATION</span></div>
      </div>
      <div class="game-title" style="margin-top:14px;">MISSION · {arena}</div>
      <div class="scan"></div>
      <div class="reticle"></div>
      <div class="game-object pop">{icon}</div>
      <div class="game-caption">{title}</div>
      <div class="game-sub">{sub}</div>
      <div class="objective"><b>PRIMARY OBJECTIVE</b><br>{objective}</div>
      <div style="margin-top:10px;padding:10px 12px;border-radius:12px;background:rgba(255,255,255,.07);font-size:.86rem;">FIELD REPORT · {scenario}</div>
    </div>
    """,unsafe_allow_html=True)

labels={f"{x.code} · {x.display_name}":x.capability for x in CAPABILITIES}
cap_to_label={v:k for k,v in labels.items()}

if "scenario_text" not in st.session_state:
    st.session_state.scenario_text="A 20 g sweet appears in a monitored chamber"
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

def scene_animation(cap,scenario,phase="experiment"):
    icon,arena,title,sub=VISUALS[cap]
    klass={
      "local_emergence":"emerge","instant_relocation":"teleport","gap_travel":"travel",
      "unsupported_ascent":"ascend","microform":"shrink","macroform":"grow",
      "lightform":"float","observer_dropout":"fade","multi_instance":"duplicate",
      "dual_presence":"duplicate","remote_sensing":"signal","future_sensing":"signal",
      "remote_acquisition":"signal","accelerated_recovery":"pulse"
    }[cap]
    if cap=="local_emergence" and "sweet" in scenario.lower(): icon="🍬"
    st.markdown(f"""
    <div class="game-scene stage">
      <div class="hud"><div class="hudline"><span><span class="statusdot"></span>LIVE SCENE</span><span>{arena}</span></div></div>
      <div class="stage-grid"></div>
      <div class="origin">A</div><div class="destination">B</div>
      <div class="actor {klass}">{icon}</div>
      <div class="game-caption">{title}</div>
      <div class="game-sub">{sub}</div>
      <div class="objective"><b>SCENE:</b> {scenario}</div>
    </div>""",unsafe_allow_html=True)

if st.session_state.screen=="briefing":
    st.markdown("## 01 // MISSION BRIEFING")
    st.markdown('<div class="hud"><div class="hudline"><span>SELECT FIELD EVENT</span><span>INPUT CONSOLE</span></div><div class="objective"><b>OBJECTIVE:</b> Choose what you want to investigate. The next screen becomes a dedicated experimental environment for that choice.</div></div>',unsafe_allow_html=True)
    scenario_choice=st.selectbox("What are you curious about?",list(SCENARIOS),key="scenario_picker",on_change=apply_scenario)
    scenario=st.text_input("Editable mission description",key="scenario_text")
    selected_label=st.selectbox("Suggested model — editable",list(labels),key="capability_label")
    cap=labels[selected_label]; spec=BY_NAME[cap]
    render_game_scene(cap,scenario)
    st.markdown(f"**Mission objective:** {GUIDE[cap][0]}")
    if st.button("ENTER EXPERIMENT →",type="primary",use_container_width=True):
        st.session_state.screen="experiment"; st.rerun()

elif st.session_state.screen=="experiment":
    selected_label=st.session_state.capability_label
    cap=labels[selected_label]; spec=BY_NAME[cap]; scenario=st.session_state.scenario_text
    top1,top2=st.columns([1,4])
    with top1:
        if st.button("← BRIEFING",use_container_width=True):
            st.session_state.screen="briefing"; st.rerun()
    with top2:
        st.markdown(f"## 02 // {VISUALS[cap][1]} · {spec.code}")
    scene_animation(cap,scenario)
    st.markdown("### INSTRUMENT PANEL")
    kwargs={}
    if cap in ("microform","macroform"):
        default=1e-6 if cap=="microform" else 1e6
        kwargs["scale"]=st.number_input("Geometric scale factor",min_value=1e-9,max_value=1e9,value=float(st.session_state.get("param_scale",default)),format="%.6g")
    elif cap=="lightform":
        kwargs["mass_scale"]=st.number_input("Effective-mass scale",min_value=1e-9,max_value=1.0,value=float(st.session_state.get("param_mass_scale",1e-6)),format="%.6g")
    elif cap=="remote_acquisition":
        kwargs["remote_information_gain"]=st.number_input("Information/access gain",min_value=0.0,value=float(st.session_state.get("param_remote_information_gain",1.0)))
    elif cap=="multi_instance":
        kwargs["copies"]=st.slider("Authenticated instances",2,20,int(st.session_state.get("param_copies",2)))
    elif cap in ("gap_travel","instant_relocation"):
        kwargs["dx"]=st.number_input("Displacement A → B (m)",min_value=0.0,value=float(st.session_state.get("param_dx",1000.0)))
    elif cap=="unsupported_ascent":
        kwargs["dz"]=st.number_input("Vertical displacement (m)",min_value=0.0,value=float(st.session_state.get("param_dz",1.0)))
    elif cap=="remote_sensing":
        kwargs["information_gain"]=st.number_input("Information gain",min_value=0.0,value=float(st.session_state.get("param_information_gain",1.0)))
    elif cap=="future_sensing":
        kwargs["horizon"]=st.number_input("Prediction horizon (s)",min_value=0.0,value=float(st.session_state.get("param_horizon",60.0)))
    elif cap=="accelerated_recovery":
        kwargs["viability_gain"]=st.slider("Viability gain",0.0,1.0,float(st.session_state.get("param_viability_gain",0.5)),0.05)
    elif cap=="local_emergence":
        kwargs["delta_mass_kg"]=st.number_input("Object mass / local increase (kg)",min_value=0.0,value=float(st.session_state.get("param_delta_mass_kg",0.020)),format="%.6f")
    st.caption("All mission defaults are editable. The animation follows the model family; the numerical engine uses these values.")
    if st.button("▶ EXECUTE EXPERIMENT",type="primary",use_container_width=True):
        st.session_state.last_kwargs=kwargs
        st.session_state.screen="results"
        st.rerun()

elif st.session_state.screen=="results":
    selected_label=st.session_state.capability_label
    cap=labels[selected_label]; spec=BY_NAME[cap]; scenario=st.session_state.scenario_text
    kwargs=st.session_state.get("last_kwargs",{})
    if st.button("← RUN AGAIN"):
        st.session_state.screen="experiment"; st.rerun()
    st.markdown(f"## 03 // AFTER-ACTION ANALYSIS · {spec.code}")
    scene_animation(cap,scenario,"results")
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
    st.success(f"EXPERIMENT COMPLETE // {spec.display_name}")
    st.progress(100,text="Simulation complete · now inspect the evidence trail")
    # result scene already rendered above
    a,b,c=st.columns(3)
    a.metric("Capability code", spec.code)
    b.metric("Changed state variables", len(delta))
    c.metric("Ordinary mimic", spec.principal_mimic)

    st.markdown("## AFTER-ACTION INTELLIGENCE")
    st.markdown('<div class="hud"><div class="hudline"><span><span class="statusdot"></span>TELEMETRY CAPTURED</span><span>ANALYSIS UNLOCKED</span></div></div>',unsafe_allow_html=True)
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
