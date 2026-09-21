"""Knowledge Synthesis Agent (KSA).

A tradition-neutral reasoning layer for extraordinary-capability descriptions.
Historical/religious labels are treated as descriptions to be compiled, never
as evidence that a claimed phenomenon occurs.
"""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class KnowledgeClaim:
    label: str
    capability: str
    observables: tuple[str,...]
    ordinary_mechanisms: tuple[str,...]
    decisive_measurements: tuple[str,...]

CLAIM_ONTOLOGY=(
 KnowledgeClaim("size decrease","microform",("geometry","mass","identity"),("perspective","substitution","measurement error"),("calibrated 3D geometry","mass","continuous identity")),
 KnowledgeClaim("size increase","macroform",("geometry","mass","identity"),("perspective","substitution","measurement error"),("calibrated 3D geometry","mass","continuous identity")),
 KnowledgeClaim("unusual lightness","lightform",("force","acceleration","support"),("hidden support","buoyancy","airflow"),("force platform","airflow","field audit")),
 KnowledgeClaim("remote acquisition","remote_acquisition",("target access","channel","timing"),("hidden channel","ordinary delivery","cueing"),("randomized target","channel audit","access log")),
 KnowledgeClaim("disappearance from observation","observer_dropout",("optical","thermal","range"),("occlusion","camouflage","sensor failure"),("multimodal synchronized sensing",)),
 KnowledgeClaim("multiple instances","multi_instance",("identity","simultaneity","provenance"),("substitution","recording","timing error"),("independent authentication","synchronized clocks")),
 KnowledgeClaim("presence at separated sites","dual_presence",("identity","location","time"),("substitution","relay","clock error"),("two-site authentication","trusted time")),
 KnowledgeClaim("unobserved path","gap_travel",("trajectory","identity","time"),("ordinary hidden route","tracking dropout"),("continuous path coverage","independent checkpoints")),
 KnowledgeClaim("discontinuous relocation","instant_relocation",("source","destination","path","time"),("hidden transport","substitution"),("continuous path coverage","identity authentication")),
 KnowledgeClaim("unsupported ascent","unsupported_ascent",("position","force","environment"),("hidden support","airflow","electromagnetic force"),("load-path audit","airflow","field sensing")),
 KnowledgeClaim("remote knowing","remote_sensing",("target","response","channel"),("leakage","cueing","chance"),("randomized concealed target","double blind","predeclared scoring")),
 KnowledgeClaim("future knowing","future_sensing",("prediction","target","time"),("timestamp error","postselection","leakage"),("precommitment","later RNG target","trusted timestamps")),
 KnowledgeClaim("accelerated recovery","accelerated_recovery",("endpoint","trajectory","time"),("baseline variation","confounding","measurement bias"),("controls","blinded endpoint","time course")),
 KnowledgeClaim("local appearance","local_emergence",("mass","boundary","provenance","energy"),("hidden transfer","transformation","measurement error"),("sealed boundary","mass balance","provenance audit")),
)

# Cross-cultural vocabulary is only a navigation aid into the neutral ontology.
ALIASES={
 "anima":"microform","mahima":"macroform","laghima":"lightform","prapti":"remote_acquisition",
 "antardhana":"observer_dropout","kayavyuha":"multi_instance","bilocation":"dual_presence",
 "flying":"unsupported_ascent","levitation":"unsupported_ascent","clairvoyance":"remote_sensing",
 "telepathy":"remote_sensing","precognition":"future_sensing","healing":"accelerated_recovery",
 "materialization":"local_emergence","teleportation":"instant_relocation","iddhi":"unclassified",
 "abhijna":"unclassified","siddhi":"unclassified",
}

def claims_for_capability(capability):
    return tuple(c for c in CLAIM_ONTOLOGY if c.capability==capability)

def classify_description(text:str):
    t=text.lower()
    hits=[]
    for term,cap in ALIASES.items():
        if term in t and cap!="unclassified": hits.append((term,cap))
    for c in CLAIM_ONTOLOGY:
        if c.label in t: hits.append((c.label,c.capability))
    # preserve ambiguity rather than forcing a single interpretation
    return tuple(dict.fromkeys(hits))

def audit_claim(capability):
    matches=claims_for_capability(capability)
    if not matches: raise KeyError(capability)
    c=matches[0]
    return {"capability":c.capability,"observables":c.observables,
            "ordinary_mechanisms":c.ordinary_mechanisms,
            "decisive_measurements":c.decisive_measurements,
            "epistemic_status":"description compiled; phenomenon not established"}

def infer_testable_consequences(capability):
    a=audit_claim(capability)
    return tuple(f"measure {x}" for x in a["observables"])+tuple(
        f"exclude/test {x}" for x in a["ordinary_mechanisms"])
