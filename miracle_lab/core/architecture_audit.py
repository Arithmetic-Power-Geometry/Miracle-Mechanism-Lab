"""V1 architecture audit: canonical 21-GX path versus isolated legacy modules."""
from miracle_lab.core.generic_ontology import EXPERIMENT_CATALOGUE
from miracle_lab.core.experiment_specs import SPECS
from miracle_lab.core.ui_catalogue import UI_EXPERIMENTS
from miracle_lab.core.visual_catalogue import V
from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK
CANONICAL=("generic_ontology","experiment_specs","ui_catalogue","mission_config","generic_engine",
           "visual_catalogue","evidence_report","generic_ctc","ctc","ctc_adaptive",
           "ctc_probabilistic","noisy_benchmark","noisy_adaptive","benchmark_suite")
LEGACY_COMPATIBILITY=("state","capabilities","agents/extraordinary","ctc_benchmark")
def architecture_audit():
 keys=set(EXPERIMENT_CATALOGUE)
 aligned=keys==set(SPECS)==set(UI_EXPERIMENTS)==set(V)==set(GENERIC_BENCHMARK)
 return {"canonical_experiments":len(keys),"aligned":aligned,
         "legacy_compatibility_modules":LEGACY_COMPATIBILITY,
         "legacy_is_canonical":False}
