"""Probabilistic separation for noisy Claim-to-Test experiments.

KL quantities remain diagnostics. Reliability is operationalized separately
through exact finite-sample Bayes accuracy for repeated Bernoulli observations.
"""
from dataclasses import dataclass
from itertools import combinations
from math import log, ceil, inf, lgamma, exp

_EPS=1e-12
@dataclass(frozen=True)
class NoisyMeasurement:
 name:str; cost_per_sample:float; p_success:dict; admissible:bool=True

def bernoulli_kl(p,q):
 p=min(max(float(p),_EPS),1-_EPS); q=min(max(float(q),_EPS),1-_EPS)
 return p*log(p/q)+(1-p)*log((1-p)/(1-q))
def symmetric_kl(p,q): return .5*(bernoulli_kl(p,q)+bernoulli_kl(q,p))
def pair_information(e,a,b): return symmetric_kl(e.p_success[a],e.p_success[b])
def required_samples(e,a,b,target_information=4.0):
 d=pair_information(e,a,b); return inf if d<=0 else max(1,ceil(target_information/d))
def pair_cost(e,a,b,target_information=4.0):
 n=required_samples(e,a,b,target_information); return inf if n==inf else n*e.cost_per_sample

def _binom_pmf(k,n,p):
 if p==0: return 1.0 if k==0 else 0.0
 if p==1: return 1.0 if k==n else 0.0
 return exp(lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)+k*log(p)+(n-k)*log(1-p))

def binomial_total_variation(p,q,n):
 if n<1: raise ValueError("n must be >=1")
 p=float(p); q=float(q)
 if not (0<=p<=1 and 0<=q<=1): raise ValueError("probabilities must be in [0,1]")
 return .5*sum(abs(_binom_pmf(k,n,p)-_binom_pmf(k,n,q)) for k in range(n+1))

def bayes_accuracy_equal_prior(p,q,n):
 """Optimal equal-prior classification accuracy from n iid Bernoulli samples."""
 return .5*(1.0+binomial_total_variation(p,q,n))

def minimum_samples_for_accuracy(p,q,target_accuracy=.95,max_n=100000):
 if not (.5<target_accuracy<1): raise ValueError("target_accuracy must be between .5 and 1")
 if p==q: return inf
 lo,hi=1,1
 while hi<=max_n and bayes_accuracy_equal_prior(p,q,hi)<target_accuracy: hi*=2
 if hi>max_n:
  hi=max_n
  if bayes_accuracy_equal_prior(p,q,hi)<target_accuracy: return inf
 while lo<hi:
  mid=(lo+hi)//2
  if bayes_accuracy_equal_prior(p,q,mid)>=target_accuracy: hi=mid
  else: lo=mid+1
 return lo

def best_pair_measurement_for_accuracy(mechanisms,measurements,target_accuracy=.95,max_n=100000):
 out={}
 for a,b in combinations(sorted(mechanisms),2):
  candidates=[]
  for e in measurements:
   if not e.admissible: continue
   n=minimum_samples_for_accuracy(e.p_success[a],e.p_success[b],target_accuracy,max_n)
   if n!=inf: candidates.append((n*e.cost_per_sample,n,e.name))
  out[(a,b)]=min(candidates) if candidates else (inf,inf,None)
 return out

def probabilistic_resolution_summary(mechanisms,measurements,target_accuracy=.95,max_n=100000):
 best=best_pair_measurement_for_accuracy(mechanisms,measurements,target_accuracy,max_n)
 unresolved=tuple(pair for pair,(cost,n,name) in best.items() if name is None)
 finite=[cost for cost,n,name in best.values() if name is not None]
 return {"target_accuracy":target_accuracy,"pair_best":best,"unresolved_pairs":unresolved,
         "max_pair_cost":max(finite) if finite else inf}
