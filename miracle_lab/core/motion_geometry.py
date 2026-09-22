"""Procedural SVG motion system for the canonical 21 ACS experiments.

The renderer is deterministic, dependency-free and experiment-specific. It
creates scientific geometric motion from the experiment key and stage; the
visualization is explanatory UI, not experimental evidence.
"""
from html import escape
from miracle_lab.core.experiment_specs import SPECS

MOTIFS={
"scale_decrease":("◎","Radial contraction","r(t) ↓"),
"scale_increase":("◉","Radial expansion","r(t) ↑"),
"mass_response_decrease":("△","Response lift","F/m ↓"),
"mass_response_increase":("▽","Response anchor","F/m ↑"),
"unsupported_motion":("↟","Free trajectory","x(t)"),
"path_discontinuity":("⋯","Broken geodesic","C < 1"),
"barrier_transit":("◇│◇","Boundary transit","x(t) ∩ B"),
"detection_dropout":("◌","Sensor phase-out","D⃗(t)"),
"multiple_instances":("◇◇◇","Instance branching","N(t) > 1"),
"multi_location_identity":("◇↔◇","Identity bridge","I_A = I_B"),
"remote_information":("⊙···◎","Hidden-channel probe","I(T;R)"),
"future_information":("◇→⌁","Temporal inversion test","t_R < t_T"),
"past_information":("⌁→◇","Retrospective probe","T_past → R"),
"remote_acquisition":("◎⇢□","Acquisition channel","A_local(T)"),
"local_emergence":("∅→◇","Inventory emergence","Δm"),
"external_influence":("◎)))◇","Remote perturbation","ΔY"),
"environmental_influence":("◎)))≋","Field perturbation","ΔE"),
"accelerated_recovery":("⌁↗","Recovery trajectory","Δr"),
"revival":("0→1","State transition","S₀ → S₁"),
"resilience":("◇⟐","Hazard envelope","R(h,d,t)"),
"form_transformation":("△→○→□","Identity-preserving morph","G₀ ≠ G₁"),
}
STAGE_WORDS={1:("BRIEF","define · parameterize · challenge"),2:("RUN","observe · perturb · measure"),3:("RESOLVE","compare · separate · bound")}

def _shape(key):
 if key in ("scale_decrease","scale_increase","detection_dropout","local_emergence"): return "circle"
 if key in ("multiple_instances","multi_location_identity","barrier_transit","form_transformation"): return "polygon"
 return "path"

def experiment_svg(key,stage=1,width=980,height=300):
 if key not in SPECS: raise KeyError(key)
 stage=max(1,min(3,int(stage))); spec=SPECS[key]; symbol,title,equation=MOTIFS[key]
 mode=_shape(key); phase=(stage-1)*1.7
 grid="".join(f'<path d="M {x} 25 V 270" />' for x in range(40,width,60))+"".join(f'<path d="M 20 {y} H {width-20}" />' for y in range(30,height,45))
 if mode=="circle":
  core=f'<circle cx="490" cy="150" r="58" class="core"><animate attributeName="r" values="28;72;28" dur="{4-stage*.5}s" repeatCount="indefinite"/></circle><circle cx="490" cy="150" r="100" class="orbit"/>'
 elif mode=="polygon":
  core='<polygon points="490,70 560,150 490,230 420,150" class="core"><animateTransform attributeName="transform" type="rotate" from="0 490 150" to="360 490 150" dur="8s" repeatCount="indefinite"/></polygon><polygon points="490,45 595,150 490,255 385,150" class="orbit"/>'
 else:
  core='<path d="M120 190 C250 20 360 280 490 140 S730 40 860 155" class="wave"/><circle r="11" class="particle"><animateMotion dur="4s" repeatCount="indefinite" path="M120 190 C250 20 360 280 490 140 S730 40 860 155"/></circle>'
 rays="".join(f'<line x1="490" y1="150" x2="{100+i*98}" y2="{55+(i%3)*92}" class="ray"><animate attributeName="stroke-opacity" values=".1;.9;.1" dur="{2.2+i*.13}s" repeatCount="indefinite"/></line>' for i in range(9))
 stage_name,verbs=STAGE_WORDS[stage]
 return f'''<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{escape(spec.title)} animated experiment geometry" xmlns="http://www.w3.org/2000/svg">
 <defs><radialGradient id="g"><stop offset="0%" stop-color="#fff" stop-opacity=".95"/><stop offset="35%" stop-color="#8ef" stop-opacity=".55"/><stop offset="100%" stop-color="#81f" stop-opacity=".03"/></radialGradient><filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
 <style>.bg{{fill:#050713}}.grid path{{stroke:#8ef;stroke-opacity:.07;stroke-width:1}}.core{{fill:url(#g);stroke:#bff;stroke-width:2;filter:url(#glow)}}.orbit{{fill:none;stroke:#9cf;stroke-opacity:.35;stroke-width:1.5;stroke-dasharray:5 12}}.wave{{fill:none;stroke:#bff;stroke-width:3;filter:url(#glow)}}.particle{{fill:#fff;filter:url(#glow)}}.ray{{stroke:#9cf;stroke-width:1}}.t{{fill:#eef;font-family:monospace}}.muted{{fill:#9ab;font-family:monospace}}</style>
 <rect width="100%" height="100%" rx="20" class="bg"/><g class="grid">{grid}</g><g opacity=".8">{rays}</g>{core}
 <text x="34" y="48" class="t" font-size="22">{escape(spec.code)} · {escape(spec.title)}</text><text x="34" y="78" class="muted" font-size="15">{escape(stage_name)} // {escape(verbs)}</text>
 <text x="34" y="252" class="t" font-size="20">{escape(symbol)}  {escape(title)}</text><text x="34" y="278" class="muted" font-size="15">{escape(equation)} · {escape(spec.mathematics[:70])}</text>
 </svg>'''

def audit_motion_system():
 return {"count":len(MOTIFS),"aligned":set(MOTIFS)==set(SPECS),"stages":3,
         "all_have_symbol":all(v[0] for v in MOTIFS.values()),
         "all_have_science_line":all(v[2] for v in MOTIFS.values())}
