"""Typed invariant signatures for the canonical 21-GX ontology.

The basis describes challenged observable relations; it does not assert that
any phenomenon occurs.
"""
from miracle_lab.core.generic_ontology import GENERIC_PHENOMENA
INVARIANTS=tuple(sorted({x for sig in GENERIC_PHENOMENA.values() for x in sig}))
CAPABILITY_BASIS={k:tuple(v) for k,v in GENERIC_PHENOMENA.items()}
def signature(capability):
 active=set(CAPABILITY_BASIS[capability]); return tuple(int(x in active) for x in INVARIANTS)
def compression_summary():
 sigs={cap:signature(cap) for cap in CAPABILITY_BASIS}
 return {"capabilities":len(sigs),"basis_size":len(INVARIANTS),
         "unique_signatures":len(set(sigs.values())),"signatures":sigs}
