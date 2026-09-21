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
.block-container {max-width: 980px; padding-top: 1rem; padding-bottom:2rem;}
[data-testid="stAppViewContainer"] {background:radial-gradient(circle at 50% 0%,#122235 0,#070d15 44%,#03070b 100%);}
[data-testid="stHeader"] {background:transparent;}
[data-testid="stMainBlockContainer"] {min-height:100vh;}
html,body,[class*="css"] {color:#e5eef7;}
h1,h2,h3,h4,p,span,label {color:inherit;}
[data-testid="stMarkdownContainer"] p {color:#d7e2ee;}
[data-testid="stMarkdownContainer"] h1,[data-testid="stMarkdownContainer"] h2,[data-testid="stMarkdownContainer"] h3 {color:#f4f8fc;}
[data-testid="stDataFrame"] {background:#0b1520;border-radius:10px;}
[data-testid="stExpander"] {background:#0b1520;border:1px solid #26384a;border-radius:10px;}


.hero {padding: 1.2rem 1.4rem; border-radius: 18px; background: linear-gradient(135deg,#111827,#1f2937); color:white; margin-bottom:1rem;}
.hero h1 {margin:0; font-size:2.1rem;}
.hero p {opacity:.88; margin:.35rem 0 0 0;}
.card {border:1px solid #e5e7eb; border-radius:14px; padding:1rem; background:white;}
.small {font-size:.9rem; opacity:.8;}
.flowbox {border:1px solid #d1d5db; border-radius:16px; padding:1rem; text-align:center; font-weight:600; min-height:82px;}
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
.toolbelt{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:10px 0 18px}.toolchip{background:#07110d;border:1px solid #244b39;border-radius:8px;padding:9px;text-align:center;color:#9fffc8;font:700 11px ui-monospace}.missionbar{height:7px;background:#10241a;border-radius:9px;overflow:hidden}.missionbar>div{height:100%;background:linear-gradient(90deg,#22c55e,#86efac);box-shadow:0 0 12px #22c55e}.coord{position:absolute;color:#86efac;font:10px ui-monospace;opacity:.75}.c1{left:18px;top:88px}.c2{right:18px;top:88px}

</style>
""", unsafe_allow_html=True)

# Three-screen mission flow -------------------------------------------------
if "screen" not in st.session_state:
    st.session_state.screen="briefing"
if "last_result" not in st.session_state:
    st.session_state.last_result=None

# Keep the full project masthead on the entry page; later stages use a compact HUD.
if st.session_state.screen=="briefing":
    st.markdown('<div class="hero"><h1>Anomalous Capability Simulator (ACS)</h1><p>A research-oriented interactive laboratory for turning unusual-event descriptions into explicit state-transition models, animated experiments, competing explanations, and discriminating tests.</p></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="hud"><div class="hudline"><span>ANOMALOUS CAPABILITY SIMULATOR · ACS</span><span>FIELD LAB</span></div></div>',unsafe_allow_html=True)

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

def scene_animation(cap,scenario,phase="briefing"):
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
        st.session_state.active_preview_cap=cap_name
        st.session_state.scenario_text=text
        for key,value in defaults.items():
            st.session_state[f"param_{key}"]=value
    else:
        st.session_state.scenario_text=text

def scene_animation(cap,scenario,phase="experiment"):
    icon,arena,title,sub=VISUALS[cap]
    if cap=="local_emergence": icon="🍬" if "sweet" in scenario.lower() else "📦"
    cfg={
      "local_emergence":("emerge","EMPTY CHAMBER","LOCAL INVENTORY EVENT","Object appears at monitored center; no A→B travel is modeled."),
      "instant_relocation":("teleport","SOURCE A","DESTINATION B","Object state switches from A to B with no modeled intermediate path."),
      "gap_travel":("travel","TRACKED START A","TRACKED END B","Object traverses A→B while the middle path becomes observationally unavailable."),
      "unsupported_ascent":("ascend","GROUND","VERTICAL Z","Object changes vertical position; support/force audit is the central question."),
      "microform":("shrink","INITIAL SCALE","REDUCED SCALE","Object geometry contracts around a fixed center; this is a scale transformation, not travel."),
      "macroform":("grow","INITIAL SCALE","EXPANDED SCALE","Object geometry expands around a fixed center; this is a scale transformation, not travel."),
      "lightform":("float","REFERENCE MASS","REDUCED RESPONSE","Visual motion represents reduced effective response; force measurement is required."),
      "observer_dropout":("fade","DETECTED","SENSOR DROPOUT","Object remains in the model while observer-access coupling falls."),
      "multi_instance":("duplicate","INSTANCE 1","MULTIPLE INSTANCES","Additional authenticated appearances are represented; provenance is the key test."),
      "dual_presence":("duplicate","SITE A","SITE B","The same identity is represented at separated sites simultaneously."),
      "remote_sensing":("signal","CONCEALED TARGET","OBSERVER","Information-state gain is shown as a signal relation, not object motion."),
      "future_sensing":("signal","FUTURE TARGET","EARLIER RECORD","Prediction horizon is represented as information preceding the target event."),
      "remote_acquisition":("signal","REMOTE TARGET","LOCAL ACCESS","Access/information changes without an observed ordinary route."),
      "accelerated_recovery":("pulse","BASELINE STATE","LATER STATE","A bounded state variable follows a faster modeled recovery trajectory.")
    }[cap]
    klass,leftlab,rightlab,meaning=cfg
    endpoint_html=""
    if cap in ("instant_relocation","gap_travel","dual_presence"):
        endpoint_html=f'<div class="origin">{leftlab}</div><div class="destination">{rightlab}</div>'
    elif cap=="local_emergence":
        endpoint_html='<div class="origin">CHAMBER SEALED</div><div class="destination">INVENTORY +</div>'
    elif cap=="unsupported_ascent":
        endpoint_html='<div class="origin">z₀</div><div class="destination">z₁ ↑</div>'
    elif cap in ("microform","macroform","lightform","observer_dropout","multi_instance","accelerated_recovery"):
        endpoint_html=f'<div class="origin">{leftlab}</div><div class="destination">{rightlab}</div>'
    else:
        endpoint_html=f'<div class="origin">{leftlab}</div><div class="destination">{rightlab}</div>'
    phase_label={"results":"EXPERIMENT REPLAY","briefing":"MISSION PREVIEW"}.get(phase,"LIVE EXPERIMENT")
    values={
      "local_emergence":f"Δm = {float(st.session_state.get('param_delta_mass_kg',0.020)):.6g} kg",
      "instant_relocation":f"Δx = {float(st.session_state.get('param_dx',1000.0)):.6g} m",
      "gap_travel":f"Δx = {float(st.session_state.get('param_dx',1000.0)):.6g} m",
      "unsupported_ascent":f"Δz = {float(st.session_state.get('param_dz',1.0)):.6g} m",
      "microform":f"scale = {float(st.session_state.get('param_scale',1e-6)):.6g}",
      "macroform":f"scale = {float(st.session_state.get('param_scale',1e6)):.6g}",
      "lightform":f"mass scale = {float(st.session_state.get('param_mass_scale',1e-6)):.6g}",
      "observer_dropout":"observer access: 1 → 0",
      "multi_instance":f"instances = {int(st.session_state.get('param_copies',2))}",
      "dual_presence":"authenticated sites = 2",
      "remote_sensing":f"information gain = {float(st.session_state.get('param_information_gain',1.0)):.6g} model-unit",
      "future_sensing":f"horizon = {float(st.session_state.get('param_horizon',60.0)):.6g} s",
      "remote_acquisition":f"access gain = {float(st.session_state.get('param_remote_information_gain',1.0)):.6g} model-unit",
      "accelerated_recovery":f"viability gain = {float(st.session_state.get('param_viability_gain',0.5)):.3g}",
    }[cap]
    st.markdown(f"""
    <div class="game-scene stage">
      <div class="hud"><div class="hudline"><span><span class="statusdot"></span>{phase_label} · {BY_NAME[cap].code}</span><span>{arena}</span></div></div>
      <div class="stage-grid"></div><div class="coord c1">CAM-01 · LOCK</div><div class="coord c2">SENSOR BUS · LIVE</div>
      {endpoint_html}
      <div class="actor {klass}">{icon}</div>
      <div class="game-caption">{title}</div>
      <div class="game-sub">{sub}</div>
      <div class="objective"><b>VISUAL MODEL:</b> {meaning}<br><b>SCENARIO:</b> {scenario}<br><b>MISSION DATA:</b> {values}</div>
    </div>""",unsafe_allow_html=True)

TOOLS={
"local_emergence":["⚖️ MASS","📷 CAMERA","🌡️ THERMAL","🔒 SEAL","🧾 INVENTORY"],
"instant_relocation":["📍 TRACK","⏱️ CLOCK","📷 CAMERA","🪪 ID","📡 RANGE"],
"gap_travel":["🗺️ MAP","📍 TRACK","⏱️ CLOCK","📷 CAMERA","🪪 ID"],
"unsupported_ascent":["⚖️ FORCE","🌬️ AIR","🧲 FIELD","📷 CAMERA","📏 RANGE"],
"microform":["📏 SCALE","⚖️ MASS","📷 CAMERA","🪪 ID","🔬 OPTICS"],
"macroform":["📏 SCALE","⚖️ MASS","📷 CAMERA","🪪 ID","🔬 OPTICS"],
"lightform":["⚖️ FORCE","📏 RANGE","📷 CAMERA","🌬️ AIR","🧲 FIELD"],
"observer_dropout":["📷 OPTICAL","🌡️ THERMAL","📡 RANGE","🎙️ AUDIO","⏱️ SYNC"],
"multi_instance":["🪪 ID","⏱️ SYNC","📍 TRACK","📷 CAMERA","🧾 PROVENANCE"],
"dual_presence":["🪪 ID","⏱️ SYNC","📍 SITE A","📍 SITE B","🧾 PROVENANCE"],
"remote_sensing":["🎲 TARGET","🔒 BLIND","📡 CHANNEL","⏱️ CLOCK","🧾 LOG"],
"future_sensing":["🎲 RNG","🔒 COMMIT","⏱️ CLOCK","🧾 LOG","📡 AUDIT"],
"remote_acquisition":["🎯 TARGET","🔒 BLIND","📡 AUDIT","⏱️ CLOCK","🧾 LOG"],
"accelerated_recovery":["📈 ENDPOINT","⏱️ TIME","👥 CONTROL","🧾 LOG","📊 CURVE"],
}
def toolbelt(cap):
    st.markdown('<div class="toolbelt">'+''.join(f'<div class="toolchip">{x}</div>' for x in TOOLS[cap])+'</div>',unsafe_allow_html=True)

if st.session_state.screen=="briefing":
    st.markdown("## 01 // MISSION BRIEFING")
    st.markdown('<div class="hud"><div class="hudline"><span>SELECT FIELD EVENT</span><span>INPUT CONSOLE</span></div><div class="objective"><b>OBJECTIVE:</b> Choose what you want to investigate. The next screen becomes a dedicated experimental environment for that choice.</div></div>',unsafe_allow_html=True)
    st.markdown("### SELECT MISSION")
    scenario_choice=st.selectbox("What are you curious about?",list(SCENARIOS),key="scenario_picker",on_change=apply_scenario,label_visibility="collapsed")
    # Synchronize immediately on every rerun, not only through a widget callback.
    cap,defaults=SCENARIOS[scenario_choice]
    st.session_state.capability_label=cap_to_label[cap]
    st.session_state.scenario_text=scenario_choice
    for key,value in defaults.items():
        if st.session_state.get("active_scenario") != scenario_choice:
            st.session_state[f"param_{key}"]=value
    st.session_state.active_scenario=scenario_choice
    scenario=scenario_choice
    spec=BY_NAME[cap]
    st.markdown(f"**Automatically selected model:** {spec.code} · {spec.display_name}")
    st.caption("The model is locked to the chosen mission so Stage 1, Stage 2 and Stage 3 cannot drift to a different experiment.")
    st.markdown(f'<div class="hud"><div class="hudline"><span>MISSION {spec.code}</span><span>{VISUALS[cap][1]}</span></div><div class="objective"><b>OBJECTIVE:</b> {GUIDE[cap][0]}</div></div>',unsafe_allow_html=True)
    scene_animation(cap,scenario,phase="briefing")
    if st.button("ENTER EXPERIMENT →",type="primary",use_container_width=True):
        st.session_state.active_cap=cap
        st.session_state.active_scenario=scenario
        st.session_state.active_spec_code=spec.code
        st.session_state.screen="experiment"; st.rerun()

elif st.session_state.screen=="experiment":
    cap=st.session_state.active_cap
    spec=BY_NAME[cap]
    scenario=st.session_state.active_scenario
    top1,top2=st.columns([1,4])
    with top1:
        if st.button("← BRIEFING",use_container_width=True):
            st.session_state.screen="briefing"
            st.session_state.pop("active_cap",None)
            st.session_state.pop("executed_cap",None)
            st.rerun()
    with top2:
        st.markdown(f"## 02 // {VISUALS[cap][1]} · {spec.code}")
    scene_animation(cap,scenario)
    toolbelt(cap)
    st.markdown("### EXPERIMENT CONTROLS")
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
        st.session_state.last_kwargs=dict(kwargs)
        st.session_state.executed_cap=cap
        st.session_state.executed_scenario=scenario
        st.session_state.screen="results"
        st.rerun()

elif st.session_state.screen=="results":
    cap=st.session_state.executed_cap
    spec=BY_NAME[cap]
    scenario=st.session_state.executed_scenario
    kwargs=dict(st.session_state.get("last_kwargs",{}))
    if st.button("← RUN AGAIN"):
        st.session_state.screen="experiment"; st.rerun()

    st.markdown(f"## 03 // EXPERIMENT REPORT · {spec.code}")
    st.caption(f"{spec.display_name} · experiment-specific after-action report")
    st.markdown(f'<div class="hud"><div class="hudline"><span>REPORT LOCKED TO {spec.code}</span><span>{VISUALS[cap][1]}</span></div><div class="objective"><b>ANALYZED EVENT:</b> {scenario}<br><b>MODEL:</b> {spec.display_name}<br><b>VISUAL USED IN EXPERIMENT:</b> {VISUALS[cap][2]} — {VISUALS[cap][3]}</div></div>',unsafe_allow_html=True)
    state=WorldState()
    if cap=="accelerated_recovery":
        state=WorldState(biological_viability=0.4)
    result=AGENTS[spec.family].simulate(cap,state,**kwargs)
    delta={k:v for k,v in result.required_delta.items() if abs(v)>1e-15}

    # Build observation from the experiment itself, never from a generic constant.
    obs={}
    derived=[]
    if cap in ("gap_travel","instant_relocation"):
        d=abs(kwargs.get("dx",1000.0)); elapsed=60.0 if cap=="gap_travel" else 1e-6
        speed=d/elapsed if elapsed>0 else math.inf
        obs={"distance_m":d,"elapsed_s":elapsed}
        derived=[("Displacement",f"{d:.6g} m"),("Modeled interval",f"{elapsed:.6g} s"),("Required average speed",f"{speed:.6g} m/s")]
    elif cap in ("dual_presence","multi_instance"):
        n=2.0 if cap=="dual_presence" else float(kwargs.get("copies",2))
        obs={"authenticated_instances":n}
        derived=[("Authenticated instances",f"{n:g}"),("Identity-locality excess",f"{max(0,n-1):g} instance(s)")]
    elif cap=="unsupported_ascent":
        dz=kwargs.get("dz",1.0); force=state.mass*9.80665
        obs={"unsupported_force_n":force}
        derived=[("Vertical displacement",f"{dz:.6g} m"),("Reference mass",f"{state.mass:.6g} kg"),("Reference weight mg",f"{force:.6g} N")]
    elif cap=="local_emergence":
        dm=kwargs.get("delta_mass_kg",0.020); energy=dm*(299792458.0**2)
        obs={"mass_energy_j":energy}
        derived=[("Local mass increase",f"{dm:.6g} kg"),("Rest-mass energy equivalent",f"{energy:.6g} J"),("Final tracked mass",f"{result.after.mass:.6g} kg")]
    elif cap=="remote_sensing":
        gain=kwargs.get("information_gain",1.0); obs={"information_excess_bits":gain}
        derived=[("Declared information gain",f"{gain:.6g} model-unit"),("Ordinary causal access after",f"{result.after.causal_access:.6g}")]
    elif cap=="remote_acquisition":
        gain=kwargs.get("remote_information_gain",1.0); obs={"information_excess_bits":gain}
        derived=[("Declared remote access gain",f"{gain:.6g} model-unit"),("Information state after",f"{result.after.information_state:.6g}")]
    elif cap=="future_sensing":
        h=kwargs.get("horizon",60.0); obs={"information_excess_bits":h}
        derived=[("Prediction horizon",f"{h:.6g} s"),("Future-information coordinate",f"{result.after.prediction_horizon:.6g} s")]
    elif cap in ("microform","macroform"):
        r=kwargs.get("scale",1.0); obs={"volume_ratio":r}
        linear=r**(1/3) if r>=0 else math.nan
        derived=[("Volume ratio V1/V0",f"{r:.6g}"),("Equivalent isotropic linear ratio",f"{linear:.6g}"),("Final modeled volume",f"{result.after.volume:.6g} m³")]
    elif cap=="lightform":
        r=kwargs.get("mass_scale",1.0); obs={"effective_mass_ratio":r}
        derived=[("Effective-mass ratio",f"{r:.6g}"),("Initial mass",f"{state.mass:.6g} kg"),("Final effective mass",f"{result.after.mass:.6g} kg")]
    elif cap=="observer_dropout":
        obs={"observer_access":result.after.observer_access}
        derived=[("Observer access before",f"{state.observer_access:.6g}"),("Observer access after",f"{result.after.observer_access:.6g}")]
    elif cap=="accelerated_recovery":
        gain=result.after.biological_viability-state.biological_viability
        obs={"viability_gain":gain}
        derived=[("Baseline viability",f"{state.biological_viability:.6g}"),("Final viability",f"{result.after.biological_viability:.6g}"),("Realized gain",f"{gain:.6g}")]

    mod=minimum_modification(cap,obs)

    st.markdown("### MISSION SUMMARY")
    st.markdown(f"""
**Scenario:** {scenario}

**Selected model:** {spec.display_name} ({spec.code})  
**Model family:** {spec.family.replace("_"," ").title()}  
**Primary modeled quantity:** {spec.primary_variable.replace("_"," ")}  
**Expected direction:** {spec.expected_direction}

**Simulation action:** {result.notes.get("claim_model","State transition model")}.

**Research question:** What measurable state change would represent this scenario, what ordinary process could imitate it, and what observation would distinguish the two?

**Interpretation boundary:** This is a synthetic state-transition experiment. It does not report a physical event and does not establish that the modeled mechanism exists.
""")

    st.markdown("### INPUTS ACTUALLY USED")
    input_rows=[{"parameter":k,"value":v} for k,v in kwargs.items()]
    if input_rows: st.dataframe(pd.DataFrame(input_rows),use_container_width=True,hide_index=True)
    else: st.write("This model uses its declared baseline state and has no additional numeric input.")

    st.markdown("### BEFORE → AFTER STATE")
    rows=[]
    for name in result.before.__dataclass_fields__:
        b=getattr(result.before,name); a=getattr(result.after,name)
        rows.append({"state variable":name,"before":b,"after":a,"delta":a-b,"changed":"YES" if abs(a-b)>1e-15 else "—"})
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    st.markdown("### EXPERIMENT-SPECIFIC DERIVED QUANTITIES")
    st.dataframe(pd.DataFrame([{"quantity":k,"value":v} for k,v in derived]),use_container_width=True,hide_index=True)

    st.markdown("### HOW THIS EXPERIMENT WAS CALCULATED")
    st.latex(r"X_1=T_{model}(X_0;\theta),\qquad \Delta X=X_1-X_0")
    if cap=="local_emergence":
        dm=kwargs.get("delta_mass_kg",0.020); energy=dm*(299792458.0**2)
        st.write(f"The selected object contributes Δm = {dm:.6g} kg to the tracked local mass inventory. The simulator therefore sets m₁ = m₀ + Δm = {result.after.mass:.6g} kg.")
        st.latex(r"E_{eq}=\Delta m c^2")
        st.write(f"With c = 299,792,458 m/s, E_eq = {energy:.6g} J. This is the rest-mass energy equivalent used for accounting; the simulation did not measure or release that energy.")
    elif cap in ("instant_relocation","gap_travel"):
        d=abs(kwargs.get("dx",1000.0)); t=1e-6 if cap=="instant_relocation" else 60.0
        st.write(f"The model changes x by {d:.6g} m. Its benchmark interval is {t:.6g} s, so the implied average traversal rate is {d/t:.6g} m/s.")
        st.latex(r"v_{req}=|x_1-x_0|/\Delta t")
        st.write("The key issue is not merely speed: the selected model stipulates missing or discontinuous path information, so continuous authenticated tracking is the critical separator.")
    elif cap in ("microform","macroform"):
        r=kwargs.get("scale",1.0)
        st.latex(r"V_1=V_0r")
        st.write(f"V₀ = {state.volume:.6g} m³, r = {r:.6g}, giving V₁ = {result.after.volume:.6g} m³. Under isotropic scaling the corresponding linear ratio is r^(1/3) = {r**(1/3):.6g}.")
    elif cap=="lightform":
        r=kwargs.get("mass_scale",1.0)
        st.latex(r"m_1=m_0r")
        st.write(f"m₀ = {state.mass:.6g} kg and r = {r:.6g}, giving modeled effective mass m₁ = {result.after.mass:.6g} kg.")
    elif cap=="unsupported_ascent":
        dz=kwargs.get("dz",1.0)
        st.write(f"The state is displaced vertically by Δz = {dz:.6g} m. For the {state.mass:.6g} kg baseline, mg = {state.mass*9.80665:.6g} N is shown as the reference gravitational force that an experimental support/force audit would need to account for.")
    elif cap in ("dual_presence","multi_instance"):
        n=2 if cap=="dual_presence" else kwargs.get("copies",2)
        st.latex(r"R_{identity}=\max(0,n-1)")
        st.write(f"n = {n}; therefore the modeled excess beyond one localized authenticated instance is {max(0,n-1)}.")
    elif cap=="observer_dropout":
        st.write(f"Observer access changes from {state.observer_access:.6g} to {result.after.observer_access:.6g}. The model does not equate this with physical disappearance; independent sensing is required to distinguish detection failure from object absence.")
    elif cap=="future_sensing":
        h=kwargs.get("horizon",60.0)
        st.write(f"The future-information coordinate is assigned a horizon of {h:.6g} s. A real test would require a prediction commitment timestamp preceding randomized target generation.")
    elif cap in ("remote_sensing","remote_acquisition"):
        gain=kwargs.get("information_gain",kwargs.get("remote_information_gain",1.0))
        st.write(f"The declared information/access coordinate increases by {gain:.6g} model-unit(s). This is a synthetic coordinate, not a measured bit count. A real protocol must operationalize scoring before data collection.")
    elif cap=="accelerated_recovery":
        st.write(f"For visualization the baseline viability is 0.4 rather than the default ceiling of 1.0, allowing the requested change to be represented. The realized transition is {state.biological_viability:.3f} → {result.after.biological_viability:.3f}. A real study would require a defined endpoint, time axis and matched controls.")

    st.markdown("### INVERSION / MINIMUM MODEL EXTENSION")
    if mod:
        st.write(f"The inversion layer maps the synthetic observation to **{mod.name}** with magnitude **{mod.magnitude:.6g} {mod.unit}** and normalized deviation **{mod.normalized_cost:.6g}**.")
        st.caption("Normalized deviation is an internal model-comparison coordinate. It is not probability, confidence, evidence strength, likelihood of the event, or a score of a real capability.")
    else:
        st.write("No inversion residual is defined for this configuration.")

    st.markdown("### COMPETING EXPLANATION AND DECISIVE TEST")
    st.write(f"**Primary ordinary competitor:** {spec.principal_mimic}.")
    st.write(f"**Why it matters:** a conventional process can reproduce part or all of the observed appearance without requiring the selected model.")
    st.write(f"**Discriminating measurement:** {spec.separator}.")
    st.write(f"**Primary quantity to measure:** {spec.primary_variable}; expected modeled direction: **{spec.expected_direction}**.")
    st.write(f"**Constraint being challenged or audited:** {spec.known_constraint}.")

    st.markdown("### WHAT A REAL PROTOCOL WOULD NEED")
    protocol={
      "local_emergence":"Pre/post calibrated chamber mass; continuous chamber-boundary recording; independent object provenance; environmental monitoring; inventory reconciliation; predeclared exclusion criteria.",
      "instant_relocation":"Synchronized source/destination recording; continuous path coverage; object authentication before and after; calibrated clocks; exclusion of substitution and hidden transport.",
      "gap_travel":"Continuous authenticated tracking across the claimed gap; independent checkpoints; synchronized timestamps; route coverage and identity continuity.",
      "unsupported_ascent":"Force platform or load path; airflow measurement; magnetic/electric field monitoring; synchronized motion capture; complete support audit.",
      "microform":"Calibrated 3D geometry, mass and identity before/after; perspective controls; instrument calibration and uncertainty.",
      "macroform":"Calibrated 3D geometry, mass and identity before/after; perspective controls; instrument calibration and uncertainty.",
      "lightform":"Independent mass/inertia/force measurements; support, buoyancy and airflow audit; calibrated acceleration measurement.",
      "observer_dropout":"Independent optical, thermal, range and other sensors with synchronized logs; occlusion and camouflage controls.",
      "multi_instance":"Simultaneous independent authentication of each instance; synchronized clocks; continuous provenance and anti-substitution controls.",
      "dual_presence":"Two-site synchronized recording; independent authentication at both sites; continuous provenance; timing uncertainty bounds.",
      "remote_sensing":"Predefined scoring; randomized concealed targets; double blinding; leakage audit; enough trials for uncertainty estimation.",
      "future_sensing":"Prediction committed before cryptographically or physically randomized target generation; synchronized timing; predefined scoring and stopping rule.",
      "remote_acquisition":"Randomized concealed target; channel audit; blinding; access logs; predefined success criterion.",
      "accelerated_recovery":"Operational clinical/biological endpoint; baseline trajectory; matched or randomized controls; blinded assessment where possible; time-course and uncertainty analysis."
    }[cap]
    st.write(protocol)

    st.markdown("### ASSUMPTIONS AND SCOPE")
    st.write("The transition is stipulated by the selected model. Values not changed by that model remain at baseline. The visualization is explanatory and does not generate additional measurements. Derived quantities are computed only from the selected parameters and declared benchmark assumptions.")
    st.write(f"**Model family:** {spec.family}. **Tracked primary variable:** {spec.primary_variable}. **Expected direction:** {spec.expected_direction}.")

    st.markdown("### MEASUREMENT / EVIDENCE CHECKLIST")
    checklist={
      "local_emergence":["Calibrated pre/post chamber mass","Continuous boundary surveillance","Object composition and provenance","Thermal/environmental record","Complete inventory reconciliation"],
      "instant_relocation":["Authenticated object at source","Authenticated object at destination","Continuous path coverage","Synchronized clocks","Substitution controls"],
      "gap_travel":["Continuous route coverage","Independent checkpoints","Identity continuity","Clock synchronization","Missing-data audit"],
      "unsupported_ascent":["Force/load path","Airflow","Magnetic/electric fields","Motion capture","Environmental disturbances"],
      "microform":["3D geometry","Mass","Identity","Camera calibration","Perspective control"],
      "macroform":["3D geometry","Mass","Identity","Camera calibration","Perspective control"],
      "lightform":["Mass/inertia","Force","Acceleration","Support/buoyancy","Airflow"],
      "observer_dropout":["Optical sensor","Thermal sensor","Range sensor","Occlusion map","Synchronized logs"],
      "multi_instance":["Independent identity tests","Simultaneous timestamps","Continuous provenance","Anti-substitution control","Independent cameras"],
      "dual_presence":["Site-A authentication","Site-B authentication","Synchronized clocks","Continuous provenance","Independent observers/sensors"],
      "remote_sensing":["Randomized target","Double blinding","Leakage audit","Predefined scoring","Trial uncertainty"],
      "future_sensing":["Precommitted prediction","Later randomized target","Trusted timestamps","Predefined scoring","Stopping rule"],
      "remote_acquisition":["Concealed randomized target","Access-channel audit","Blinding","Predefined criterion","Complete logs"],
      "accelerated_recovery":["Defined endpoint","Baseline trajectory","Control group","Time course","Uncertainty analysis"]
    }[cap]
    for i,item in enumerate(checklist,1):
        st.write(f"**{i}.** {item}")

    st.markdown("### WHAT THIS RESULT CAN AND CANNOT SAY")
    st.write("**Can say:** the selected computational model produced the requested state transition; the report identifies its mathematical consequences, a conventional competitor, and measurements capable of testing the distinction.")
    st.write("**Cannot say:** that the animated event occurred physically, that the selected mechanism is true, or that a numerical residual is empirical evidence.")

    st.markdown("### REPORT CONCLUSION")
    changed=", ".join(delta) if delta else "no tracked state variables"
    st.write(f"Under the selected parameters, the software successfully instantiated the **{spec.display_name}** model by changing **{changed}**. This establishes only internal simulation consistency. The next empirical question is whether the discriminating measurement — **{spec.separator}** — can separate the selected model from **{spec.principal_mimic}** in real observations.")
    st.warning("SIMULATION ≠ OBSERVATION ≠ EVIDENCE. The report explains what was modeled, what was calculated, what alternative explanation matters, and what would have to be measured next.")

    with st.expander("Full calculation audit"):
        st.write("Baseline state X₀")
        st.json(result.before.__dict__)
        st.write("Final state X₁")
        st.json(result.after.__dict__)
        st.write("ΔX")
        st.json(result.required_delta)
        st.write("Observation supplied to inversion")
        st.json(obs)
        st.write("Model notes")
        st.json(result.notes)

    st.markdown("---")
    st.caption("Anomalous Capability Simulator · synthetic modeling environment · Copyright (C) 2026 Mohammad Amir Khusru Akhtar · Apache License 2.0")
