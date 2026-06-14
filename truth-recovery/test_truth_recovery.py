"""
test_truth_recovery.py -- measured invariants for the meta-genome yardstick.
Seeded. Exit 0 = all pass.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from harness import run_cell, BASE_SEED

ok = True


def check(name, cond, detail):
    global ok
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")
    if not cond:
        ok = False


homog = run_cell(307, 1, 120, BASE_SEED)
real = run_cell(307, 4, 120, BASE_SEED)

check("forced k=4 produces only weak clusters on truly HOMOGENEOUS data (low silhouette)",
      homog["sil4"] < 0.2, f"(silhouette {homog['sil4']})")
check("real 4-cluster data clusters cleanly (high silhouette)",
      real["sil4"] > 0.4, f"(silhouette {real['sil4']})")
check("the silhouette DISCRIMINATES real structure from noise (so it should be the validity gate)",
      real["sil4"] > homog["sil4"] + 0.3, f"(real {real['sil4']} vs homog {homog['sil4']})")
check("proper model selection supports k=4 only when 4 clusters TRULY exist, not on homogeneous data",
      real["pick4_rate"] > 0.7 and homog["pick4_rate"] < 0.1,
      f"(P(best-k==4): real {real['pick4_rate']} vs homog {homog['pick4_rate']})")

print("\nAll measured invariants hold." if ok else "\nSOME INVARIANTS FAILED.")
sys.exit(0 if ok else 1)
