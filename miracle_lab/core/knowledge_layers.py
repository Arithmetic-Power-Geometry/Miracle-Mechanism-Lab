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
 LayeredClaim("Yoga/Samkhya","siddhi","extraordinary attainment",("altered embodiment","extraordinary knowing"),("prakriti transformation","samadhi/samyama"),("scale_decrease","scale_increase","mass_response_decrease","remote_information","future_information")),
 LayeredClaim("Buddhist","iddhi/rddhi","extraordinary ability",("multiplicity","unusual locomotion","unusual perception"),("meditative accomplishment",),("multiple_instances","unsupported_motion","remote_information")),
 LayeredClaim("Buddhist","abhijna","higher knowledge",("remote perception","mind-related knowing","retrocognitive report"),("concentration/insight",),("remote_information",)),
 LayeredClaim("Tantric","siddhi","ritual/contemplative accomplishment",("extraordinary efficacy","altered agency"),("mantra/deity/ritual frameworks",),("remote_information","future_information","local_emergence","remote_acquisition")),
 LayeredClaim("Islamic devotional/hagiographic","karama/karamat","saintly marvel report",("unusual knowledge","unusual locomotion","unexpected provision or material event","unusual recovery"),("divine gift; not an independently controlled power",),("remote_information","future_information","path_discontinuity","path_discontinuity","local_emergence","accelerated_recovery")),
 LayeredClaim("Jain contemplative","labdhi/rddhi","extraordinary attainment report",("unusual perception","altered embodiment","unusual locomotion"),("ascetic/contemplative accomplishment",),("remote_information","scale_decrease","scale_increase","unsupported_motion")),
 LayeredClaim("Christian hagiographic","charism/miracle report","saintly or charismatic marvel report",("unusual healing","unusual knowledge","multiple-location report","material event"),("divine action/grace",),("accelerated_recovery","remote_information","multi_location_identity","local_emergence")),
 LayeredClaim("Jewish scriptural/rabbinic","miracle/wonder report","scriptural or hagiographic marvel report",("unusual material event","unusual locomotion","unusual recovery"),("divine action",),("local_emergence","path_discontinuity","accelerated_recovery")),
 LayeredClaim("Comparative mysticism","mystical/noetic experience","transformative experience",("unity","noetic seeming","ineffability"),("theistic","nondual","naturalistic"),()),
 LayeredClaim("Anomalous reports","anomalous capability","reported anomaly",("unexpected information","unexpected motion","unexpected material change","unexpected detection loss"),("underdetermined",),("remote_information","future_information","path_discontinuity","local_emergence","detection_dropout")),
)

def by_capability(cap):
    return tuple(x for x in KNOWLEDGE_LAYERS if cap in x.observable_capabilities)

def cross_tradition_convergence(cap):
    rows=by_capability(cap)
    return {"capability":cap,"source_families":tuple(sorted({x.source_family for x in rows})),
            "terms":tuple(sorted({x.term for x in rows})),
            "convergence_count":len({x.source_family for x in rows}),
            "interpretation":"descriptive convergence only; truth and mechanism remain open"}
