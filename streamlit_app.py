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
from miracle_lab.core.motion_geometry import experiment_svg

st.set_page_config(page_title="ACS Game Zone · 21 Experiment Lab",page_icon="🎮",layout="wide")

st.markdown("""<style>
.block-container{padding-top:1rem;max-width:1500px}.gx-card{border:1px solid #4443;border-radius:18px;padding:1rem 1.2rem;margin:.35rem 0;background:linear-gradient(135deg,#1111,#8881)}
.gx-kpi{font-size:1.35rem;font-weight:800}.gx-small{opacity:.75;font-size:.9rem}.gx-stage{letter-spacing:.16em;font-size:.78rem;font-weight:800}.gx-console{font-family:monospace;border-left:4px solid #888;padding:.8rem 1rem;background:#8881}.gx-ok{font-weight:800}
</style>""",unsafe_allow_html=True)

if "gx_screen" not in st.session_state: st.session_state.gx_screen="briefing"
if "gx_score" not in st.session_state: st.session_state.gx_score=0
if "gx_runs" not in st.session_state: st.session_state.gx_runs=0

def visual(spec,v,stage=1):
 st.markdown(experiment_svg(spec.key,stage),unsafe_allow_html=True)
 st.markdown(f'<div class="gx-card"><div class="gx-stage">{spec.arena}</div><div class="gx-kpi">{spec.symbol} {spec.code} · {spec.title}</div><div class="gx-small">{v.left} → {v.right}</div><p>{v.caption}</p></div>',unsafe_allow_html=True)


PUBLIC_EXPLANATIONS = {
"scale_decrease": {"plain":"Tests whether an object's measured geometry becomes smaller rather than merely appearing smaller.","why":"Useful when perspective, substitution or calibration could mimic a size change.","measure":["Calibrated 3-D dimensions before and after","Mass under the same weighing conditions","Continuous identity or provenance record"],"alts":{"perspective":"A camera angle or viewing distance can make the object look smaller without changing its geometry.","substitution":"A different smaller object can replace the original unless identity is continuously authenticated.","measurement error":"Calibration, segmentation or scale-reference errors can create a false size change."},"takeaway":"A smaller image is not enough; geometry and identity must change consistently."},
"scale_increase": {"plain":"Tests whether an object's measured geometry becomes larger rather than merely appearing larger.","why":"Useful when perspective, substitution or calibration could mimic enlargement.","measure":["Calibrated 3-D dimensions before and after","Mass under the same weighing conditions","Continuous identity or provenance record"],"alts":{"perspective":"Camera geometry can make an unchanged object appear larger.","substitution":"A larger replacement can imitate enlargement unless identity is tracked.","measurement error":"Calibration or scale-reference error can create false growth."},"takeaway":"Apparent enlargement is resolved only when calibrated geometry and identity agree."},
"mass_response_decrease": {"plain":"Tests whether the measured force response becomes lower under controlled conditions.","why":"Useful for claims of unusual lightness where support, buoyancy or airflow may explain the effect.","measure":["Applied force","Acceleration or load response","Support and environmental forces"],"alts":{"hidden support":"An unseen support can reduce the measured load.","buoyancy":"Fluid or air buoyancy can reduce apparent weight.","airflow":"Air currents can provide lift or alter a force measurement."},"takeaway":"Low measured response does not by itself identify a new mechanism."},
"mass_response_increase": {"plain":"Tests whether the measured force response becomes higher under controlled conditions.","why":"Useful for claims of unusual heaviness where anchoring, fields or instrument error may explain the effect.","measure":["Applied force","Acceleration or load response","Support and environmental conditions"],"alts":{"anchoring":"Mechanical attachment can increase the force needed to move the object.","field force":"An ordinary external field or force can add to the measured response.","instrument error":"Sensor offset or overload can imitate increased response."},"takeaway":"A larger force reading must be separated from ordinary extra forces and sensor error."},
"unsupported_motion": {"plain":"Tests motion when no supporting force has yet been identified.","why":"Useful for separating an unusual trajectory from hidden support, airflow or electromagnetic forces.","measure":["Position over time","Forces acting on the object","Environmental conditions"],"alts":{"support":"A hidden mechanical support can produce the trajectory.","airflow":"Airflow can accelerate or lift an object.","electromagnetic force":"Magnetic or electric forces can move an object without visible contact."},"takeaway":"Motion is not evidence of unsupported motion until known force channels are audited."},
"path_discontinuity": {"plain":"Tests whether an authenticated object has an unobserved break in its path between two locations.","why":"Useful when endpoints are known but continuous travel is not.","measure":["Continuous trajectory coverage","Trusted timing","Authenticated identity"],"alts":{"hidden route":"The object may follow an ordinary route outside observation.","tracking dropout":"Sensors may temporarily lose the object.","substitution":"A different object can appear at the destination."},"takeaway":"Endpoints alone do not prove a discontinuous path."},
"barrier_transit": {"plain":"Tests whether the same authenticated object crosses an intact barrier.","why":"Useful when before-and-after observations could be explained by openings, occlusion or substitution.","measure":["Barrier integrity","Trajectory through the boundary region","Identity continuity"],"alts":{"opening":"An ordinary opening or access path may exist.","occlusion":"The crossing may occur while the relevant region is not observed.","substitution":"A second object can appear on the opposite side."},"takeaway":"Barrier crossing requires simultaneous evidence about the barrier, path and identity."},
"detection_dropout": {"plain":"Tests whether an object disappears across independent sensing channels rather than only from one sensor.","why":"Useful for separating broad detection loss from camouflage, occlusion or sensor failure.","measure":["Optical/IR/range/audio detection","Position estimate","Synchronized timing"],"alts":{"camouflage":"The object may remain present but become hard to detect in one modality.","occlusion":"Another object or geometry may block the sensor.","sensor failure":"A sensor can fail without the object disappearing."},"takeaway":"Single-camera disappearance is weak evidence; independent sensors matter."},
"multiple_instances": {"plain":"Tests whether more than one simultaneously present object can be authenticated as the same source identity.","why":"Useful when recordings or substitutes could create an apparent duplicate.","measure":["Identity authentication","Simultaneity","Provenance of each instance"],"alts":{"substitution":"A look-alike or duplicate object can be mistaken for the original.","recording":"Replay or display artifacts can look like another live instance.","timing error":"Non-simultaneous events can be mistaken for simultaneous ones."},"takeaway":"Counting appearances is not enough; each instance must be authenticated at the same time."},
"multi_location_identity": {"plain":"Tests whether one authenticated identity is independently present at separated sites at the same time.","why":"Useful when relay, substitution or clock error could imitate simultaneous presence.","measure":["Independent identity authentication at both sites","Trusted synchronized clocks","Measured site separation"],"alts":{"relay":"Information from one site can be relayed to another without physical co-presence.","substitution":"A second person or object can imitate the identity.","clock error":"Timing mismatch can create false simultaneity."},"takeaway":"The key evidence is independent authentication plus trustworthy simultaneity."},
"remote_information": {"plain":"Tests whether responses contain information about a concealed target beyond chance.","why":"Useful when leakage, cueing or random success could explain apparent remote knowledge.","measure":["Randomized concealed targets","Predefined responses","Channel and leakage audit"],"alts":{"leakage":"Target information may reach the respondent through an ordinary channel.","cueing":"Experimenter or environmental cues can influence responses.","chance":"A small number of correct responses can occur randomly."},"takeaway":"A striking answer is not enough; concealment, scoring and leakage control are essential."},
"future_information": {"plain":"Tests whether a response committed before target generation predicts a later random target.","why":"Useful when postselection, leakage or timestamp problems could create hindsight effects.","measure":["Irrevocable response commitment","Later independently generated target","Trusted timestamps"],"alts":{"postselection":"Only successful predictions may be retained after the target is known.","leakage":"Future target information may become available through an ordinary process.","timestamp error":"Incorrect timing can make a later response appear earlier."},"takeaway":"Prediction requires verifiable commitment before the target exists."},
"past_information": {"plain":"Tests whether a concealed historical target can be inferred without ordinary access.","why":"Useful when memory, cueing or selective sampling could explain success.","measure":["Concealed historical target sample","Recorded response","Target provenance and access audit"],"alts":{"ordinary memory":"The respondent may already know the historical information.","cueing":"Context or experimenter behavior may reveal clues.","selection bias":"Targets or successful trials may be selected after the fact."},"takeaway":"Retrospective accuracy is informative only when prior access and selection are controlled."},
"remote_acquisition": {"plain":"Tests whether local access to a target occurs without a documented ordinary transfer channel.","why":"Useful when hidden delivery, access or cueing could explain the result.","measure":["Target access record","Transfer-channel audit","Timing and distance"],"alts":{"ordinary delivery":"The target may have been moved by a normal route.","hidden channel":"An unmonitored transfer path may exist.","cueing":"Information about the target may guide an ordinary acquisition."},"takeaway":"Appearance of access is not enough; provenance and transfer channels must be audited."},
"local_emergence": {"plain":"Tests whether inventory appears within an audited boundary and whether mass/provenance accounting changes.","why":"Useful for sealed-chamber or local-appearance reports where hidden transfer, transformation or measurement error are alternatives.","measure":["Mass balance before and after","Boundary integrity","Provenance of the appearing inventory"],"alts":{"hidden transfer":"The object or material may enter through an unnoticed route.","transformation":"Existing material may change form rather than appear from nowhere.","measurement error":"Inventory or mass may be recorded incorrectly."},"takeaway":"Seeing an object appear does not identify its mechanism; mass balance, boundary integrity and provenance are decisive."},
"external_influence": {"plain":"Tests whether an intervention changes a remote target relative to controls.","why":"Useful when ordinary channels, bias or confounding could explain the difference.","measure":["Target outcome","Randomized intervention assignment","Control condition"],"alts":{"ordinary force/channel":"A conventional signal or force may connect intervention and target.","bias":"Expectations or analysis choices may shift the reported effect.","confounding":"Another variable may differ between intervention and control."},"takeaway":"A causal claim requires controlled comparison, not just a before-and-after change."},
"environmental_influence": {"plain":"Tests whether an intervention is associated with a controlled change in an environmental variable.","why":"Useful when natural variation, local forcing or selection bias could explain the observation.","measure":["Environmental field or variable","Matched controls","Synchronized timing"],"alts":{"natural variation":"The environment may change on its own.","local forcing":"An ordinary local process may produce the change.","selection bias":"Only favorable time windows or locations may be reported."},"takeaway":"Environmental change becomes informative only against an appropriate control and baseline."},
"accelerated_recovery": {"plain":"Tests whether a recovery trajectory differs from an appropriate comparison trajectory.","why":"Useful when regression to the mean, treatment effects or measurement bias could explain rapid improvement.","measure":["Baseline state","Repeated time-course measurements","Comparison/control trajectory"],"alts":{"regression to mean":"Extreme initial measurements often move toward typical values on repeat testing.","treatment":"Ordinary treatment or care may explain improvement.","measurement bias":"Changes in measurement conditions can imitate recovery."},"takeaway":"Before-and-after improvement is weaker than a controlled recovery trajectory."},
"revival": {"plain":"Tests an operational transition from a declared state 0 to state 1 under predefined criteria.","why":"Useful when misclassification, ordinary resuscitation or record error could explain the transition.","measure":["Predeclared state criterion","Independent confirmation","Trusted timing"],"alts":{"misclassification":"The initial state may have been classified incorrectly.","resuscitation":"An ordinary intervention may restore the state.","record error":"Documentation or timing errors may create a false transition."},"takeaway":"The state definition must be fixed before interpreting a state transition."},
"resilience": {"plain":"Tests response to a verified hazard, dose and exposure duration.","why":"Useful when insufficient exposure, protection or measurement error could explain apparent resistance.","measure":["Hazard dose","Verified exposure","Measured response"],"alts":{"insufficient exposure":"The actual dose may be lower than assumed.","protection":"Ordinary shielding or protective factors may reduce the effect.","measurement error":"Dose or response may be measured incorrectly."},"takeaway":"Resilience cannot be judged without verified exposure and dose."},
"form_transformation": {"plain":"Tests whether geometry changes while authenticated identity remains continuous.","why":"Useful when costume, substitution or perspective could imitate transformation.","measure":["Geometry before and after","Identity continuity","Continuous observation"],"alts":{"costume":"External covering can alter appearance without changing the underlying object.","substitution":"A different object can replace the original.","perspective":"Viewing geometry can make form appear to change."},"takeaway":"Transformation requires both geometric change and continuous identity evidence."}
}
def public_explanation(key):
    return PUBLIC_EXPLANATIONS[key]

def progress():
 order={"briefing":1,"experiment":2,"results":3}
 n=order.get(st.session_state.gx_screen,1)
 st.progress(n/3,text=f"Mission stage {n}/3")
 a,b=st.columns(2)
 a.metric("Completed runs",st.session_state.gx_runs)
 b.metric("Lab score",st.session_state.gx_score,help="Interface progress score only; not a scientific result.")

st.title("🎮 Anomalous Capability Simulator · Game Zone")
st.markdown("""
### What is ACS?
ACS is a public research simulator for turning an unusual report into a **clear measurement plan**. It does not ask you to believe or reject a claim. Instead, it asks what must be measured, which ordinary alternatives remain possible, what the model computes, and what evidence is still missing.

**How to use it:** **Claim → Measure → Compare explanations → Find missing evidence → Conclude only what the evidence permits.**

*Example:* if an object is reported to appear inside a sealed chamber, ACS asks whether the boundary was intact, whether mass changed, whether the object's provenance is known, and whether hidden transfer or measurement error still fit the observations.
""")
st.caption("21 neutral experiment missions · synthetic computational lab · no extraordinary claim is treated as established")
progress()

if st.session_state.gx_screen=="briefing":
 st.markdown("## 01 // MISSION BRIEFING")
 st.write("Choose a mission, inspect the observable signature, tune the model, then lock the mission before entering the lab.")
 choice=st.selectbox("Choose experiment",tuple(DISPLAY_TO_KEY))
 key=DISPLAY_TO_KEY[choice]; spec=UI_EXPERIMENTS[key]; explain=public_explanation(key); example=st.selectbox("Scenario",spec.examples)
 visual(spec,V[key],1)
 st.markdown("### In plain language")
 st.write(explain["plain"])
 st.write("**Why this experiment matters:** "+explain["why"])
 st.info("Key idea: "+explain["takeaway"])
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
  for x,desc in zip(spec.measurements,explain["measure"]):
   st.write(f"✅ **{x}** — {desc}")
  st.markdown("**What the competing explanations mean**")
  for x in spec.discriminators:
   st.write(f"🧩 **{x}** — {explain['alts'].get(x,'A declared competing explanation that remains possible until discriminating evidence excludes it.')}")
 if st.button("LOCK MISSION & ENTER LAB →",type="primary",use_container_width=True):
  st.session_state.gx_mission=freeze_mission(key,example,params)
  st.session_state.gx_screen="experiment"; st.rerun()

elif st.session_state.gx_screen=="experiment":
 m=st.session_state.gx_mission; spec=UI_EXPERIMENTS[m.experiment]; v=V[m.experiment]; explain=public_explanation(m.experiment)
 st.markdown("## 02 // EXPERIMENT ZONE")
 visual(spec,v,2)
 st.write(f"**Scenario locked:** {m.example}")
 st.info(explain["plain"])
 st.markdown("### What you are checking now")
 st.write("Tick a measurement only if that evidence is actually available. Leaving a box unchecked is scientifically valid: it means the claim remains unresolved on that dimension.")
 c1,c2=st.columns([1,1])
 with c1:
  st.markdown("### Frozen configuration")
  st.json(dict(m.parameters))
 with c2:
  st.markdown("### Mission checklist")
  observed=[]
  for x,desc in zip(spec.measurements,explain["measure"]):
   if st.checkbox(f"Observe · {x}",key=f"obs_{m.code}_{x}",help=desc): observed.append(x)
   st.caption(desc)
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
 spec=UI_EXPERIMENTS[m.experiment]; explain=public_explanation(m.experiment); observed=st.session_state.get("gx_observed",())
 report=build_report(result,observed)
 st.markdown("## 03 // ANALYSIS & OUTPUT ZONE")
 visual(spec,V[m.experiment],3)
 c1,c2,c3=st.columns(3)
 c1.metric("Observed required",f"{len(observed)}/{len(spec.measurements)}")
 c2.metric("Output fields",len(report.outputs))
 c3.metric("Resolution","Resolved*" if report.resolution_status!="UNRESOLVED" else "Unresolved")
 st.markdown("### What this result means")
 st.info(report.interpretation)
 st.write("**Plain-language reading:** "+explain["takeaway"])
 if report.resolution_status=="UNRESOLVED":
  st.write("The current evidence is not enough to separate all declared explanations. That is a valid scientific result, not a failure.")
 else:
  st.write("The declared synthetic alternatives are separated by the selected measurements. This is still a model-level result, not proof of an extraordinary real-world mechanism.")
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
 st.write("These are concrete competing explanations. Each remains possible until the relevant evidence excludes it.")
 for i,x in enumerate(report.alternatives,1):
  st.write(f"**{i}. {x}** — {explain['alts'].get(x,'This declared alternative remains possible until discriminating evidence excludes it.')}")
 st.markdown("### What evidence is still needed?")
 missing=[x for x in spec.measurements if x not in observed]
 if missing:
  for x in missing:
   idx=list(spec.measurements).index(x)
   st.write(f"• **{x}** — {explain['measure'][idx]}")
 else:
  st.write("All required measurement dimensions were declared observed for this run.")
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
 st.caption("Interpretation: lower synthetic cost means fewer weighted benchmark observations are needed in the declared model; it is not a currency, probability of truth, or real laboratory price.")
 st.caption("CTC/noisy values are synthetic benchmark quantities used to test discrimination algorithms, not empirical effect estimates.")
 st.markdown("### Resolution boundary")
 if report.resolution_status=="UNRESOLVED":
  st.warning("UNRESOLVED — missing required measurements: "+", ".join(report.unresolved))
  reward=5
 else:
  st.success("Resolved relative to the declared synthetic measurement set. This does not establish an extraordinary interpretation.")
  reward=20
 st.caption(report.boundary)
 st.markdown("### Research takeaway")
 st.info(explain["takeaway"])
 st.markdown("### How to use this outside the simulator")
 st.write("Use the listed measurements as a checklist for designing or reviewing a real study. Replace the synthetic parameters with calibrated domain-specific measurements, predefine the protocol, document provenance and controls, and keep any unresolved alternatives explicit.")
 if "gx_last_rewarded" not in st.session_state or st.session_state.gx_last_rewarded!=st.session_state.gx_runs:
  st.session_state.gx_score+=reward; st.session_state.gx_last_rewarded=st.session_state.gx_runs
 st.success(f"Game-zone progress +{reward} points. This score measures interface completion only.")
 b1,b2=st.columns(2)
 if b1.button("↻ REVIEW / RE-RUN",use_container_width=True):
  st.session_state.gx_screen="experiment"; st.rerun()
 if b2.button("🎮 NEW MISSION",type="primary",use_container_width=True):
  st.session_state.gx_screen="briefing"; st.rerun()
