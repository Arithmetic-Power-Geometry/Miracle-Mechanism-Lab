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
 LayeredClaim("Tantric","siddhi","ritual/contemplative accomplishment",("extraordinary efficacy","altered agency"),("mantra/deity/ritual frameworks",),("remote_sensing","future_sensing","local_emergence","remote_acquisition")),
 LayeredClaim("Islamic devotional/hagiographic","karama/karamat","saintly marvel report",("unusual knowledge","unusual locomotion","unexpected provision or material event","unusual recovery"),("divine gift; not an independently controlled power",),("remote_sensing","future_sensing","gap_travel","instant_relocation","local_emergence","accelerated_recovery")),
 LayeredClaim("Jain contemplative","labdhi/rddhi","extraordinary attainment report",("unusual perception","altered embodiment","unusual locomotion"),("ascetic/contemplative accomplishment",),("remote_sensing","microform","macroform","unsupported_ascent")),
 LayeredClaim("Christian hagiographic","charism/miracle report","saintly or charismatic marvel report",("unusual healing","unusual knowledge","multiple-location report","material event"),("divine action/grace",),("accelerated_recovery","remote_sensing","dual_presence","local_emergence")),
 LayeredClaim("Jewish scriptural/rabbinic","miracle/wonder report","scriptural or hagiographic marvel report",("unusual material event","unusual locomotion","unusual recovery"),("divine action",),("local_emergence","gap_travel","accelerated_recovery")),
 LayeredClaim("Comparative mysticism","mystical/noetic experience","transformative experience",("unity","noetic seeming","ineffability"),("theistic","nondual","naturalistic"),()),
 LayeredClaim("Anomalous reports","anomalous capability","reported anomaly",("unexpected information","unexpected motion","unexpected material change","unexpected detection loss"),("underdetermined",),("remote_sensing","future_sensing","instant_relocation","local_emergence","observer_dropout")),
)

def by_capability(cap):
    return tuple(x for x in KNOWLEDGE_LAYERS if cap in x.observable_capabilities)

def cross_tradition_convergence(cap):
    rows=by_capability(cap)
    return {"capability":cap,"source_families":tuple(sorted({x.source_family for x in rows})),
            "terms":tuple(sorted({x.term for x in rows})),
            "convergence_count":len({x.source_family for x in rows}),
            "interpretation":"descriptive convergence only; truth and mechanism remain open"}
