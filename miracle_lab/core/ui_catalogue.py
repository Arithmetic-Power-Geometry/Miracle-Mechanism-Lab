"""UI-facing catalogue for the frozen 21 generic experiments.

This adapter is the single source of truth for Streamlit selection.  Examples
are nested under experiments and never counted as additional experiments.
"""
from dataclasses import dataclass
from miracle_lab.core.generic_ontology import EXPERIMENT_CATALOGUE
from miracle_lab.core.experiment_specs import SPECS

@dataclass(frozen=True)
class UIExperiment:
 key:str; code:str; title:str; examples:tuple[str,...]; family:str; arena:str
 symbol:str; mathematics:str; measurements:tuple[str,...]; discriminators:tuple[str,...]
 parameters:tuple[str,...]

def _build():
 out={}
 for key,row in EXPERIMENT_CATALOGUE.items():
  s=SPECS[key]
  out[key]=UIExperiment(key,s.code,s.title,tuple(row["examples"]),s.family,s.arena,
                        s.symbol,s.mathematics,s.measurements,s.discriminators,tuple(row["parameters"]))
 return out

UI_EXPERIMENTS=_build()
DISPLAY_TO_KEY={f"{x.code} · {x.title}":k for k,x in UI_EXPERIMENTS.items()}

def examples_for(key): return UI_EXPERIMENTS[key].examples
def audit_ui_catalogue():
 codes=[x.code for x in UI_EXPERIMENTS.values()]
 examples=[e for x in UI_EXPERIMENTS.values() for e in x.examples]
 return {"count":len(UI_EXPERIMENTS),"unique_codes":len(set(codes))==len(codes),
         "unique_examples":len(set(examples))==len(examples),
         "all_have_math":all(bool(x.mathematics) for x in UI_EXPERIMENTS.values()),
         "all_have_measurements":all(bool(x.measurements) for x in UI_EXPERIMENTS.values()),
         "all_have_discriminators":all(bool(x.discriminators) for x in UI_EXPERIMENTS.values())}
