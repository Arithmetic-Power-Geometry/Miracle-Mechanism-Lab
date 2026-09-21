"""Run one validated default simulation for every canonical GX experiment."""
from miracle_lab.core.experiment_specs import SPECS
from miracle_lab.core.generic_engine import execute

def main():
 for key,spec in SPECS.items():
  result=execute(key)
  print(f"\n[{spec.code}] {spec.title}")
  print("inputs:",result.inputs)
  print("outputs:",result.outputs)
  print("interpretation:",result.interpretation)
  print("boundary:",result.boundary)

if __name__=="__main__":
 main()
