"""Cross-tradition analytical layers for KSA.

The layer separates textual report, phenomenology, metaphysical interpretation,
physical consequence, and empirical test. Similar descriptions may therefore
map to the same observable class without asserting equivalent doctrines.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class LayeredClaim:
    source_family:str
    term:str
    report_type:str
    phenomenology:tuple[str,...]
    metaphysical_frame:tuple[str,...]
    observable_capabilities:tuple[str,...]
    epistemic_note:str="historical/doctrinal description; not empirical confirmation"

KNOWLEDGE_LAYERS=(
 LayeredClaim("Yoga/Samkhya","siddhi","extraordinary attainment",("altered embodiment","extraordinary knowing"),("prakriti transformation","samadhi/samyama"),("microform","macroform","lightform","remote_sensing","future_sensing")),
 LayeredClaim("Buddhist","iddhi/rddhi","extraordinary ability",("multiplicity","unusual locomotion","unusual perception"),("meditative accomplishment",),("multi_instance","unsupported_ascent","remote_sensing")),
 LayeredClaim("Buddhist","abhijna","higher knowledge",("remote perception","mind-related knowing","retrocognitive report"),("concentration/insight",),("remote_sensing",)),
 LayeredClaim("Tantric","siddhi","ritual/contemplative accomplishment",("extraordinary efficacy","altered agency"),("mantra/deity/ritual frameworks",),("remote_sensing","local_emergence")),
 LayeredClaim("Comparative mysticism","mystical/noetic experience","transformative experience",("unity","noetic seeming","ineffability"),("theistic","nondual","naturalistic"),()),
 LayeredClaim("Anomalous reports","anomalous capability","reported anomaly",("unexpected information","unexpected motion","unexpected material change"),("underdetermined",),("remote_sensing","future_sensing","instant_relocation","local_emergence")),
)

def by_capability(cap):
    return tuple(x for x in KNOWLEDGE_LAYERS if cap in x.observable_capabilities)

def cross_tradition_convergence(cap):
    rows=by_capability(cap)
    return {"capability":cap,"source_families":tuple(sorted({x.source_family for x in rows})),
            "terms":tuple(sorted({x.term for x in rows})),
            "convergence_count":len({x.source_family for x in rows}),
            "interpretation":"descriptive convergence only; truth and mechanism remain open"}
