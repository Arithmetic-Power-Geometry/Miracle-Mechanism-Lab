"""Experiment-specific mathematics and discrimination report for ACS 21."""
from dataclasses import dataclass
from miracle_lab.core.experiment_specs import SPECS
from miracle_lab.core.generic_engine import ExecutionResult
from miracle_lab.core.visual_catalogue import V

@dataclass(frozen=True)
class EvidenceReport:
 code:str; title:str; mathematics:str; equations:tuple[str,...]
 measurements:tuple[str,...]; alternatives:tuple[str,...]; outputs:dict
 resolution_status:str; unresolved:tuple[str,...]; interpretation:str; boundary:str

def build_report(result:ExecutionResult, observed=None):
 spec=SPECS[result.key]; observed=set(observed or ())
 required=set(spec.measurements)
 missing=tuple(sorted(required-observed))
 status="RESOLVED_FOR_DECLARED_MEASUREMENTS" if not missing else "UNRESOLVED"
 return EvidenceReport(result.code,spec.title,spec.mathematics,result.equations,
   spec.measurements,spec.discriminators,result.outputs,status,missing,
   result.interpretation,result.boundary)

def report_audit():
 return {"count":len(SPECS),"all_have_visual":set(SPECS)==set(V),
  "all_have_measurements":all(len(s.measurements)>=3 for s in SPECS.values()),
  "all_have_alternatives":all(len(s.discriminators)>=3 for s in SPECS.values())}
