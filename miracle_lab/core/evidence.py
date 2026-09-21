from dataclasses import dataclass
from typing import Dict, List

@dataclass
class EvidenceResult:
    capability: str
    literal_score: float
    best_mimic_score: float
    separation_margin: float
    resolved: bool
    errors: List[str]

def score_evidence(capability: str, observations: Dict[str, float], required: Dict[str, float], mimics: List[Dict[str, float]], tolerance: float = 0.10) -> EvidenceResult:
    errors = []
    if not required:
        return EvidenceResult(capability, 0.0, 0.0, 0.0, False, ["no required signature"])
    def fit(model):
        vals=[]
        for k,v in model.items():
            if k not in observations:
                continue
            scale=max(abs(v),1.0)
            vals.append(max(0.0,1.0-abs(observations[k]-v)/scale))
        return sum(vals)/len(vals) if vals else 0.0
    literal=fit(required)
    mimic_scores=[fit(m) for m in mimics] or [0.0]
    best=max(mimic_scores)
    margin=literal-best
    resolved=literal >= 1.0-tolerance and margin > tolerance
    if literal < 1.0-tolerance: errors.append("literal signature not sufficiently matched")
    if margin <= tolerance: errors.append("ordinary alternative not separated")
    return EvidenceResult(capability,literal,best,margin,resolved,errors)
