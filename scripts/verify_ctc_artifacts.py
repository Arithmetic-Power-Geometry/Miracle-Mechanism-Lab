"""Verify generated CTC artifact hashes and cardinalities."""
import json,hashlib
from pathlib import Path
def main():
 root=Path("artifacts/ctc"); m=json.loads((root/"manifest.json").read_text(encoding="utf-8"))
 assert m["benchmark_rows"]==63 and m["experiments"]==21
 for name,digest in m["files"].items():
  assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
 print("CTC artifact manifest verified")
if __name__=="__main__": main()
