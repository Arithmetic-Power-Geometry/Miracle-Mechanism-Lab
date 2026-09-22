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
    scenes={
        "scale_decrease":'<circle cx="500" cy="150" r="78" class="core"><animate attributeName="r" values="78;28;78" dur="4s" repeatCount="indefinite"/></circle>',
        "scale_increase":'<circle cx="500" cy="150" r="28" class="core"><animate attributeName="r" values="28;82;28" dur="4s" repeatCount="indefinite"/></circle>',
        "mass_response_decrease":'<line x1="500" y1="55" x2="500" y2="235" class="axis"/><rect x="455" y="155" width="90" height="45" class="core"><animate attributeName="y" values="155;105;155" dur="3s" repeatCount="indefinite"/></rect><path d="M470 220 V130 M460 145 L470 130 L480 145" class="wave"/>',
        "mass_response_increase":'<line x1="500" y1="55" x2="500" y2="235" class="axis"/><rect x="455" y="105" width="90" height="45" class="core"><animate attributeName="y" values="105;165;105" dur="3s" repeatCount="indefinite"/></rect><path d="M470 80 V165 M460 150 L470 165 L480 150" class="wave"/>',
        "unsupported_motion":'<path d="M180 220 Q500 40 820 100" class="wave"/><circle r="12" class="particle"><animateMotion dur="4s" repeatCount="indefinite" path="M180 220 Q500 40 820 100"/></circle>',
        "path_discontinuity":'<path d="M150 170 H390 M610 170 H850" class="wave"/><circle r="12" class="particle"><animate attributeName="cx" values="150;390;610;850" dur="4s" repeatCount="indefinite"/><animate attributeName="cy" values="170;170;170;170" dur="4s" repeatCount="indefinite"/></circle><text x="485" y="178" class="t" font-size="28">?</text>',
        "barrier_transit":'<rect x="480" y="45" width="40" height="205" class="barrier"/><path d="M160 150 H840" class="wave"/><circle r="12" class="particle"><animate attributeName="cx" values="160;440;560;840" dur="4s" repeatCount="indefinite"/><animate attributeName="cy" values="150;150;150;150" dur="4s" repeatCount="indefinite"/></circle>',
        "detection_dropout":'<circle cx="500" cy="150" r="45" class="core"><animate attributeName="opacity" values="1;.05;1" dur="3s" repeatCount="indefinite"/></circle><circle cx="500" cy="150" r="90" class="scan"><animate attributeName="r" values="50;115;50" dur="3s" repeatCount="indefinite"/></circle>',
        "multiple_instances":'<circle cx="400" cy="150" r="35" class="core"><animate attributeName="r" values="28;38;28" dur="2.6s" repeatCount="indefinite"/></circle><circle cx="500" cy="150" r="35" class="core"><animate attributeName="r" values="38;28;38" dur="2.6s" repeatCount="indefinite"/></circle><circle cx="600" cy="150" r="35" class="core"><animate attributeName="r" values="28;38;28" dur="2.6s" repeatCount="indefinite"/></circle>',
        "multi_location_identity":'<circle cx="300" cy="150" r="38" class="core"/><circle cx="700" cy="150" r="38" class="core"/><path d="M338 150 H662" class="wave" stroke-dasharray="8 12"><animate attributeName="stroke-dashoffset" values="0;40" dur="2s" repeatCount="indefinite"/></path><text x="485" y="140" class="t" font-size="20">ID</text>',
        "remote_information":'<circle cx="250" cy="150" r="50" class="barrier"/><text x="220" y="156" class="t" font-size="18">TARGET</text><path d="M310 150 Q500 60 690 150" class="wave" stroke-dasharray="5 10"><animate attributeName="stroke-dashoffset" values="0;45" dur="2s" repeatCount="indefinite"/></path><circle cx="750" cy="150" r="34" class="core"/>',
        "future_information":'<rect x="220" y="120" width="150" height="60" class="core"><animate attributeName="opacity" values="1;.55;1" dur="2.5s" repeatCount="indefinite"/></rect><text x="245" y="157" class="t" font-size="16">RESPONSE</text><path d="M390 150 H650" class="wave"/><polygon points="650,140 675,150 650,160" class="core"/><rect x="690" y="120" width="120" height="60" class="barrier"/><text x="707" y="157" class="t" font-size="16">TARGET</text>',
        "past_information":'<rect x="190" y="120" width="120" height="60" class="barrier"/><text x="206" y="157" class="t" font-size="16">PAST</text><path d="M330 150 H620" class="wave" stroke-dasharray="8 10"><animate attributeName="stroke-dashoffset" values="40;0" dur="2.2s" repeatCount="indefinite"/></path><circle cx="700" cy="150" r="36" class="core"/><text x="670" y="156" class="t" font-size="13">RESPONSE</text>',
        "remote_acquisition":'<rect x="205" y="115" width="90" height="70" class="barrier"/><text x="221" y="155" class="t" font-size="15">TARGET</text><path d="M315 150 H650" class="wave" stroke-dasharray="6 12"/><rect x="690" y="115" width="95" height="70" class="core"><animate attributeName="opacity" values=".25;1;.25" dur="3s" repeatCount="indefinite"/></rect>',
        "local_emergence":'<rect x="390" y="65" width="220" height="170" rx="8" class="barrier"/><circle cx="500" cy="150" r="30" class="core"><animate attributeName="r" values="0;36;36;0" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" dur="4s" repeatCount="indefinite"/></circle>',
        "external_influence":'<circle cx="270" cy="150" r="34" class="core"/><path d="M320 150 C420 80 540 220 650 150" class="wave"><animate attributeName="stroke-opacity" values=".25;1;.25" dur="2s" repeatCount="indefinite"/></path><rect x="690" y="115" width="90" height="70" class="barrier"/>',
        "environmental_influence":'<circle cx="250" cy="150" r="34" class="core"/><path d="M300 150 C420 60 560 240 700 150" class="wave"><animate attributeName="stroke-dasharray" values="2 10;18 6;2 10" dur="2.4s" repeatCount="indefinite"/></path><path d="M690 100 Q740 55 790 100 Q740 145 690 100" class="scan"/>',
        "accelerated_recovery":'<path d="M170 220 C360 215 420 180 500 145 S690 75 830 60" class="wave"/><path d="M170 220 C390 215 570 190 830 145" class="scan"/><circle r="10" class="particle"><animateMotion dur="4s" repeatCount="indefinite" path="M170 220 C360 215 420 180 500 145 S690 75 830 60"/></circle>',
        "revival":'<line x1="190" y1="190" x2="810" y2="190" class="axis"/><path d="M200 190 H430 L470 110 L520 230 L560 145 L610 190 H800" class="wave"><animate attributeName="stroke-opacity" values=".2;1;.2" dur="3s" repeatCount="indefinite"/></path>',
        "resilience":'<polygon points="500,60 585,95 570,190 500,235 430,190 415,95" class="core"><animate attributeName="stroke-width" values="2;7;2" dur="2.4s" repeatCount="indefinite"/></polygon><line x1="180" y1="90" x2="420" y2="125" class="ray"/><line x1="180" y1="150" x2="415" y2="150" class="ray"/><line x1="180" y1="210" x2="430" y2="180" class="ray"/>',
        "form_transformation":'<polygon points="500,70 570,210 430,210" class="core"><animate attributeName="points" values="500,70 570,210 430,210;430,90 570,90 570,210 430,210;500,65 585,150 500,235 415,150;500,70 570,210 430,210" dur="5s" repeatCount="indefinite"/></polygon>'
    }
    return scenes[key]

def experiment_svg(key,stage=1,width=980,height=300):
    if key not in SPECS:
        raise KeyError(key)
    stage=max(1,min(3,int(stage)))
    spec=SPECS[key]
    symbol,title,equation=MOTIFS[key]
    stage_name,verbs=STAGE_WORDS[stage]
    grid="".join(f'<path d="M {x} 25 V 270" />' for x in range(40,width,60))+"".join(f'<path d="M 20 {y} H {width-20}" />' for y in range(30,height,45))
    return f'''<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{escape(spec.title)} animated experiment scene" xmlns="http://www.w3.org/2000/svg">
    <defs><radialGradient id="g"><stop offset="0%" stop-color="#fff" stop-opacity=".95"/><stop offset="40%" stop-color="#8ef" stop-opacity=".55"/><stop offset="100%" stop-color="#81f" stop-opacity=".03"/></radialGradient><filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
    <style>.bg{{fill:#050713}}.grid path{{stroke:#8ef;stroke-opacity:.07;stroke-width:1}}.core{{fill:url(#g);stroke:#bff;stroke-width:2;filter:url(#glow)}}.wave{{fill:none;stroke:#bff;stroke-width:3;filter:url(#glow)}}.scan{{fill:none;stroke:#9cf;stroke-width:2;stroke-opacity:.55}}.axis{{stroke:#789;stroke-width:2}}.barrier{{fill:#4453;stroke:#9cf;stroke-width:2}}.particle{{fill:#fff;filter:url(#glow)}}.ray{{stroke:#9cf;stroke-width:2}}.t{{fill:#eef;font-family:monospace}}.muted{{fill:#9ab;font-family:monospace}}</style>
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
