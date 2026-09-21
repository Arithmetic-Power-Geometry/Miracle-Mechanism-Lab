"""One-step adaptive noisy CTC policy.

At each posterior state, choose the admissible measurement with maximum
expected entropy reduction per unit cost. This is a transparent baseline,
not claimed globally optimal.
"""
from math import log2
from miracle_lab.core.noisy_benchmark import noisy_experiment

def entropy(p):
 return -sum(x*log2(x) for x in p.values() if x>0)

def posterior(prior,e,y):
 weights={m:prior[m]*(e.p_success[m] if y else 1-e.p_success[m]) for m in prior}
 z=sum(weights.values())
 return prior.copy() if z==0 else {m:w/z for m,w in weights.items()}

def expected_information_gain(prior,e):
 h0=entropy(prior)
 py=sum(prior[m]*e.p_success[m] for m in prior)
 h1=entropy(posterior(prior,e,1)); h0y=entropy(posterior(prior,e,0))
 return h0-(py*h1+(1-py)*h0y)

def choose_next(prior,measurements):
 ranked=[]
 for e in measurements:
  if not e.admissible or e.cost_per_sample<=0: continue
  gain=expected_information_gain(prior,e)
  ranked.append((-(gain/e.cost_per_sample),-gain,e.cost_per_sample,e.name))
 return None if not ranked else min(ranked)[3]

def adaptive_trace(key,regime,outcomes):
 mechanisms,measurements=noisy_experiment(key,regime)
 prior={m:1/len(mechanisms) for m in mechanisms}; by={e.name:e for e in measurements}; rows=[]
 for y in outcomes:
  name=choose_next(prior,measurements)
  if name is None: break
  e=by[name]; gain=expected_information_gain(prior,e)
  rows.append({"measurement":name,"outcome":int(bool(y)),"expected_information_gain_bits":gain,
               "posterior_before":dict(prior)})
  prior=posterior(prior,e,bool(y)); rows[-1]["posterior_after"]=dict(prior)
 return prior,tuple(rows)
