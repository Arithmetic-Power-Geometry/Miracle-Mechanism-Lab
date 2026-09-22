"""Experiment-specific procedural SVG scenes for the 21 ACS experiments."""
from html import escape
from miracle_lab.core.experiment_specs import SPECS

MOTIFS={
"scale_decrease":("◎","Radial contraction","r(t) ↓"),
"scale_increase":("◉","Radial expansion","r(t) ↑"),
"mass_response_decrease":("△","Reduced response","F/m ↓"),
"mass_response_increase":("▽","Increased response","F/m ↑"),
"unsupported_motion":("↟","Unsupported trajectory","x(t)"),
"path_discontinuity":("⋯","Path coverage gap","C < 1"),
"barrier_transit":("◇│◇","Barrier transit","x(t) ∩ B"),
"detection_dropout":("◌","Sensor dropout","D⃗(t)"),
"multiple_instances":("◇◇◇","Multiple authenticated instances","N(t)>1"),
"multi_location_identity":("◇↔◇","Separated identity sites","I_A=I_B"),
"remote_information":("⊙···◎","Concealed-target information","I(T;R)"),
"future_information":("R→T","Response before target","t_R<t_T"),
"past_information":("T←R","Concealed past target","T_past→R"),
"remote_acquisition":("□···◇","Remote acquisition","A_local(T)"),
"local_emergence":("∅→◇","Local emergence","Δm"),
"external_influence":("◎)))◇","Remote intervention","ΔY"),
"environmental_influence":("◎)))≋","Environmental intervention","ΔE"),
"accelerated_recovery":("⌁↗","Recovery trajectory","Δr"),
"revival":("0→1","State transition","S₀→S₁"),
"resilience":("◇⟐","Hazard response","R(h,d,t)"),
"form_transformation":("△→○→□","Form change with identity","G₀≠G₁"),
}
STAGE_WORDS={1:("BRIEF","define · parameterize · challenge"),2:("RUN","observe · perturb · measure"),3:("RESOLVE","compare · separate · bound")}

def _scene(key):
    # Every mission uses a different recognizable object and a different motion story.
    scenes={
      "scale_decrease":'<g><rect x="455" y="105" width="90" height="90" rx="10" class="object"/><circle cx="477" cy="128" r="7" class="detail"/><path d="M470 174 L492 148 L515 172 L535 142" class="wave"/><animateTransform attributeName="transform" type="scale" values="1;0.38;1" additive="sum" dur="4s" repeatCount="indefinite"/></g>',
      "scale_increase":'<g><rect x="110" y="105" width="120" height="90" rx="8" class="barrier"/><text x="118" y="88" class="muted">REFERENCE SIZE</text><g transform="translate(170 150)"><rect x="-28" y="-24" width="56" height="48" rx="7" class="object"/><circle cx="-10" cy="-8" r="5" class="detail"/><path d="M-18 14 L-5 0 L8 12 L19 -8" class="wave"/></g><path d="M270 150 H690" class="scan" stroke-dasharray="8 10"/><g transform="translate(735 150)"><rect x="-28" y="-24" width="56" height="48" rx="7" class="object"/><circle cx="-10" cy="-8" r="5" class="detail"/><path d="M-18 14 L-5 0 L8 12 L19 -8" class="wave"/><animateTransform attributeName="transform" type="scale" values=".55;1.65;1.65;.55" dur="4.8s" repeatCount="indefinite"/></g><text x="610" y="72" class="t">MEASURED GEOMETRY INCREASES</text><path d="M690 110 L725 150 L690 190" class="wave"/></g>',
      "mass_response_decrease":'<g><path d="M500 72 C470 105 470 145 500 175 C530 145 530 105 500 72Z" class="object"><animateTransform attributeName="transform" type="translate" values="0 75;0 -20;0 75" dur="3.6s" repeatCount="indefinite"/></path><path d="M500 210 V90 M488 108 L500 90 L512 108" class="wave"/></g>',
      "mass_response_increase":'<g><path d="M455 112 H545 L565 198 H435Z" class="object"><animateTransform attributeName="transform" type="translate" values="0 -35;0 25;0 -35" dur="3.2s" repeatCount="indefinite"/></path><path d="M500 70 V205 M488 187 L500 205 L512 187" class="wave"/></g>',
      "unsupported_motion":'<g><path d="M160 220 Q500 25 835 100" class="scan"/><path d="M-22 8 L18 0 L-22 -8 L-8 0Z" class="object"><animateMotion dur="4s" repeatCount="indefinite" path="M160 220 Q500 25 835 100" rotate="auto"/></path></g>',
      "path_discontinuity":'<g><path d="M140 190 H385 M615 190 H860" class="wave"/><path d="M-18 12 H18 L28 0 L18 -12 H-18Z" class="object"><animateMotion dur="4s" repeatCount="indefinite" path="M140 190 H385 M615 190 H860"/></path><text x="478" y="175" class="t" font-size="54">?</text></g>',
      "barrier_transit":'<g><rect x="470" y="55" width="60" height="190" class="barrier"/><path d="M470 55 L530 85 M470 95 L530 125 M470 135 L530 165 M470 175 L530 205" class="scan"/><circle r="22" class="object"><animateMotion dur="4s" repeatCount="indefinite" path="M150 150 H850"/></circle></g>',
      "detection_dropout":'<g><path d="M465 175 Q500 110 535 175 L525 210 H475Z" class="object"><animate attributeName="opacity" values="1;1;.03;.03;1" dur="4s" repeatCount="indefinite"/></path><path d="M360 150 Q500 55 640 150 Q500 245 360 150Z" class="scan"><animate attributeName="stroke-dasharray" values="2 14;18 4;2 14" dur="3s" repeatCount="indefinite"/></path></g>',
      "multiple_instances":'<g class="object"><path d="M400 115 L430 150 L400 185 L370 150Z"/><path d="M500 115 L530 150 L500 185 L470 150Z"/><path d="M600 115 L630 150 L600 185 L570 150Z"/><animateTransform attributeName="transform" type="translate" values="0 0;0 -14;0 0" dur="2.7s" repeatCount="indefinite"/></g>',
      "multi_location_identity":'<g><path d="M270 175 Q300 95 330 175Z" class="object"/><path d="M670 175 Q700 95 730 175Z" class="object"/><path d="M335 150 H665" class="wave" stroke-dasharray="9 12"><animate attributeName="stroke-dashoffset" values="0;42" dur="2s" repeatCount="indefinite"/></path><text x="475" y="138" class="t">SAME ID</text></g>',
      "remote_information":'<g><rect x="190" y="95" width="125" height="110" rx="8" class="barrier"/><text x="216" y="155" class="t">?</text><path d="M330 150 Q500 55 680 150" class="wave" stroke-dasharray="5 12"><animate attributeName="stroke-dashoffset" values="0;55" dur="2s" repeatCount="indefinite"/></path><path d="M720 110 Q770 150 720 190 Q690 150 720 110Z" class="object"/></g>',
      "future_information":'<g><rect x="205" y="105" width="135" height="90" rx="8" class="object"/><text x="228" y="158" class="t">ANSWER</text><path d="M365 150 H650" class="wave"/><rect x="690" y="92" width="125" height="116" rx="8" class="barrier"/><text x="718" y="158" class="t">FUTURE</text><animate attributeName="opacity" values=".65;1;.65" dur="2.5s" repeatCount="indefinite"/></g>',
      "past_information":'<g><path d="M175 95 H360 V205 H175Z" class="barrier"/><path d="M195 115 L340 185 M195 185 L340 115" class="scan"/><path d="M385 150 H650" class="wave" stroke-dasharray="8 10"><animate attributeName="stroke-dashoffset" values="50;0" dur="2.4s" repeatCount="indefinite"/></path><path d="M705 105 Q760 150 705 195 Q675 150 705 105Z" class="object"/></g>',
      "remote_acquisition":'<g><rect x="185" y="105" width="120" height="90" rx="8" class="barrier"/><path d="M220 135 H270 V170 H220Z" class="object"/><path d="M320 150 H650" class="wave" stroke-dasharray="6 12"/><path d="M690 105 H805 V205 H690Z" class="barrier"/><g class="object"><path d="M720 135 H770 V170 H720Z"/><animate attributeName="opacity" values="0;0;1;1;0" dur="4s" repeatCount="indefinite"/></g></g>',
      "local_emergence":'<g><path d="M390 70 H610 V225 H390Z" class="barrier"/><path d="M410 92 H590 V205 H410Z" class="scan"/><g class="object"><path d="M500 105 C535 140 535 180 500 205 C465 180 465 140 500 105Z"/><animateTransform attributeName="transform" type="scale" values="0;0;1;1;0" additive="sum" dur="4.5s" repeatCount="indefinite"/></g></g>',
      "external_influence":'<g><path d="M245 105 Q300 150 245 195 Q215 150 245 105Z" class="object"/><path d="M315 150 C420 70 550 230 665 150" class="wave"><animate attributeName="stroke-dasharray" values="2 16;20 5;2 16" dur="2.5s" repeatCount="indefinite"/></path><g class="object"><rect x="705" y="112" width="85" height="76" rx="8"/><animateTransform attributeName="transform" type="rotate" values="0 747 150;8 747 150;-8 747 150;0 747 150" dur="2.5s" repeatCount="indefinite"/></g></g>',
      "environmental_influence":'<g><circle cx="500" cy="150" r="92" class="scan"><animate attributeName="r" values="65;118;65" dur="3.5s" repeatCount="indefinite"/></circle><path d="M455 195 Q500 85 545 195Z" class="object"/><path d="M365 105 Q410 75 455 105 M545 105 Q590 75 635 105" class="wave"/></g>',
      "accelerated_recovery":'<g><path d="M190 170 H420 L455 130 L490 205 L525 105 L565 170 H820" class="scan"/><path d="M420 120 L465 165 M465 120 L420 165" class="object"><animate attributeName="opacity" values="1;.15;1" dur="3s" repeatCount="indefinite"/></path><path d="M570 135 Q615 90 660 135 Q615 180 570 135Z" class="object"/></g>',
      "revival":'<g><path d="M250 190 H410" class="axis"/><path d="M410 190 L455 120 L500 220 L545 100 L590 190 H760" class="wave"><animate attributeName="stroke-opacity" values=".08;.08;1;1" dur="4s" repeatCount="indefinite"/></path><circle cx="500" cy="150" r="85" class="scan"><animate attributeName="opacity" values=".05;.05;.7;.05" dur="4s" repeatCount="indefinite"/></circle></g>',
      "resilience":'<g><path d="M500 65 L585 100 L565 205 L500 238 L435 205 L415 100Z" class="object"/><path d="M160 90 L410 125 M160 150 L410 150 M160 210 L425 180" class="ray"><animate attributeName="stroke-width" values="1;7;1" dur="2.8s" repeatCount="indefinite"/></path><circle cx="500" cy="150" r="115" class="scan"><animate attributeName="r" values="105;125;105" dur="2.8s" repeatCount="indefinite"/></circle></g>',
      "form_transformation":'<g class="object"><path d="M500 70 L575 215 L425 215Z"><animate attributeName="d" values="M500 70 L575 215 L425 215Z;M430 85 H570 V215 H430Z;M500 62 L590 150 L500 238 L410 150Z;M500 70 L575 215 L425 215Z" dur="5s" repeatCount="indefinite"/></path></g>'
    }
    return scenes[key]

def experiment_svg(key,stage=1,width=980,height=300):
    if key not in SPECS:
        raise KeyError(key)
    stage=max(1,min(3,int(stage)))
    spec=SPECS[key]
    symbol,title,equation=MOTIFS[key]
    stage_name,verbs=STAGE_WORDS[stage]
    palettes={
      "scale_decrease":("#68e8ff","#8b5cff"),"scale_increase":("#7fffc8","#49a7ff"),
      "mass_response_decrease":("#ffe66d","#57d9ff"),"mass_response_increase":("#ff9f68","#ff5f7a"),
      "unsupported_motion":("#6ef2ff","#a56cff"),"path_discontinuity":("#ffdf6e","#ff6fae"),
      "barrier_transit":("#7afcff","#6c7dff"),"detection_dropout":("#ff78d7","#63dfff"),
      "multiple_instances":("#82ffb4","#56c8ff"),"multi_location_identity":("#63eaff","#c77dff"),
      "remote_information":("#ffd76a","#67e8ff"),"future_information":("#ff9ee8","#77d8ff"),
      "past_information":("#a7a0ff","#62f0d2"),"remote_acquisition":("#ffcf70","#7ee7ff"),
      "local_emergence":("#8affd1","#b37cff"),"external_influence":("#ff8fa3","#6ee7ff"),
      "environmental_influence":("#77f4c7","#5ca9ff"),"accelerated_recovery":("#8dff8a","#61d9ff"),
      "revival":("#ff7676","#ffe875"),"resilience":("#ffc85c","#6fffd8"),
      "form_transformation":("#d38cff","#65e7ff")}
    accent,accent2=palettes[key]
    grid="".join(f'<path d="M {x} 25 V 270" />' for x in range(40,width,60))+"".join(f'<path d="M 20 {y} H {width-20}" />' for y in range(30,height,45))
    return f'''<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{escape(spec.title)} animated experiment scene" xmlns="http://www.w3.org/2000/svg">
    <defs><radialGradient id="g"><stop offset="0%" stop-color="#fff" stop-opacity=".95"/><stop offset="40%" stop-color="{accent}" stop-opacity=".72"/><stop offset="100%" stop-color="{accent2}" stop-opacity=".06"/></radialGradient><filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
    <style>.bg{{fill:#050713}}.grid path{{stroke:#8ef;stroke-opacity:.07;stroke-width:1}}.core{{fill:url(#g);stroke:{accent};stroke-width:2;filter:url(#glow)}}.object{{fill:url(#g);stroke:{accent};stroke-width:3;filter:url(#glow)}}.detail{{fill:{accent2};filter:url(#glow)}}.wave{{fill:none;stroke:{accent};stroke-width:3;filter:url(#glow)}}.scan{{fill:none;stroke:{accent2};stroke-width:2;stroke-opacity:.7}}.axis{{stroke:#789;stroke-width:2}}.barrier{{fill:#4453;stroke:{accent2};stroke-width:2}}.particle{{fill:#fff;filter:url(#glow)}}.ray{{stroke:{accent2};stroke-width:2}}.t{{fill:#eef;font-family:monospace}}.muted{{fill:#9ab;font-family:monospace}}</style>
    <rect width="100%" height="100%" rx="20" class="bg"/><g class="grid">{grid}</g>{_scene(key)}
    <text x="34" y="48" class="t" font-size="22">{escape(spec.code)} · {escape(spec.title)}</text>
    <text x="34" y="78" class="muted" font-size="15">{escape(stage_name)} // {escape(verbs)}</text>
    <text x="34" y="252" class="t" font-size="20">{escape(symbol)}  {escape(title)}</text>
    <text x="34" y="278" class="muted" font-size="15">{escape(equation)} · {escape(spec.mathematics[:70])}</text>
    </svg>'''

def audit_motion_system():
    return {"count":len(MOTIFS),"aligned":set(MOTIFS)==set(SPECS),"stages":3,
            "all_have_symbol":all(v[0] for v in MOTIFS.values()),
            "all_have_science_line":all(v[2] for v in MOTIFS.values()),
            "distinct_scene_count":len(SPECS)}
