"""Neutral analytical layer for ACS claim descriptions.

The canonical software separates a report description, a modeled interpretation,
observable capabilities, and empirical tests. It does not encode religious,
scriptural, doctrinal, or practitioner-specific classifications.
"""
from dataclasses import dataclass
from miracle_lab.core.experiment_specs import SPECS

@dataclass(frozen=True)
class LayeredClaim:
 source_family:str
 term:str
 report_type:str
 phenomenology:tuple[str,...]
 metaphysical_frame:tuple[str,...]
 observable_capabilities:tuple[str,...]
 epistemic_note:str="descriptive scenario only; not empirical confirmation"

KNOWLEDGE_LAYERS=tuple(
 LayeredClaim(
  source_family="neutral scenario catalogue",
  term=spec.title.lower(),
  report_type="modeled unusual-capability report",
  phenomenology=spec.measurements,
  metaphysical_frame=("underdetermined",),
  observable_capabilities=(key,),
 ) for key,spec in SPECS.items()
)

def by_capability(cap):
 return tuple(x for x in KNOWLEDGE_LAYERS if cap in x.observable_capabilities)

def cross_scenario_convergence(cap):
 rows=by_capability(cap)
 return {"capability":cap,"source_families":tuple(sorted({x.source_family for x in rows})),
         "terms":tuple(sorted({x.term for x in rows})),
         "convergence_count":len(rows),
         "interpretation":"descriptive grouping only; truth and mechanism remain open"}

def cross_tradition_convergence(cap):
 """Backward-compatible name; returns the neutral scenario grouping."""
 return cross_scenario_convergence(cap)
