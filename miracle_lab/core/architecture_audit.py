"""V1 architecture audit: canonical 21-GX path versus isolated compatibility modules."""
from miracle_lab.core.generic_ontology import EXPERIMENT_CATALOGUE
from miracle_lab.core.experiment_specs import SPECS
from miracle_lab.core.ui_catalogue import UI_EXPERIMENTS
from miracle_lab.core.visual_catalogue import V
from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK
from miracle_lab.core.parameter_specs import PARAMETERS,audit_parameter_specs

CANONICAL=("generic_ontology","experiment_specs","parameter_specs","ui_catalogue","mission_config",
 "generic_engine","visual_catalogue","evidence_report","generic_ctc","ctc","ctc_adaptive",
 "ctc_probabilistic","noisy_benchmark","noisy_adaptive","benchmark_suite")
LEGACY_COMPATIBILITY=("state","capabilities","agents/extraordinary","ctc_benchmark","ctc_probabilistic_benchmark")
LEGACY_TOKENS=("microform","macroform","lightform","remote_sensing","future_sensing","dual_presence",
 "multi_instance","instant_relocation","gap_travel","unsupported_ascent","observer_dropout")

def architecture_audit():
 keys=set(EXPERIMENT_CATALOGUE)
 aligned=keys==set(SPECS)==set(PARAMETERS)==set(UI_EXPERIMENTS)==set(V)==set(GENERIC_BENCHMARK)
 return {"canonical_experiments":len(keys),"aligned":aligned,
  "parameter_registry_valid":audit_parameter_specs()["valid"],
  "legacy_compatibility_modules":LEGACY_COMPATIBILITY,"legacy_is_canonical":False}
