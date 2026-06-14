"""
harness.py -- Truth-recovery yardstick for meta-genome.

meta-genome claims to have "discovered 4 species of evidence quality" by PCA +
K-Means clustering of Cochrane reviews. But the pipeline HARDCODES n_clusters=4
("matching the ABCD grading metaphor"), so K-Means ALWAYS partitions the data
into 4 groups -- whether or not 4 real clusters exist. The honest test: on data
with a KNOWN number of true clusters (1 = homogeneous, or 4), does the forced
k=4 clustering reflect real structure, and does a proper cluster-validity model
selection support k=4?

We replicate the pipeline's exact clustering (StandardScaler + KMeans(n_clusters,
random_state=42, n_init=10)) and measure:
  - silhouette of the forced k=4 fit on 1-cluster vs 4-cluster data, and
  - the k chosen by silhouette over k in 2..8 (proper model selection).

Truth-first: every number is produced from seeded simulation here.
Run:  python truth-recovery/harness.py --reps 200
"""
import sys, argparse
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

BASE_SEED = 20260613
N_FEATURES = 8


def gen(rng, n_reviews, true_k, sep=4.0):
    if true_k == 1:
        X = rng.standard_normal((n_reviews, N_FEATURES))
    else:
        centers = rng.standard_normal((true_k, N_FEATURES)) * sep
        assign = rng.integers(0, true_k, n_reviews)
        X = centers[assign] + rng.standard_normal((n_reviews, N_FEATURES))
    return X


def cluster_k(X, k):
    Xs = StandardScaler().fit_transform(X)
    Xs = np.nan_to_num(Xs, nan=0, posinf=3, neginf=-3)
    labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(Xs)
    if len(set(labels)) < 2:
        return labels, -1.0
    return labels, silhouette_score(Xs, labels)


def run_cell(n_reviews, true_k, reps, seed0):
    sil4 = []          # silhouette of the forced k=4 fit
    best_k = []        # k chosen by silhouette over 2..8
    picks4 = 0
    for r in range(reps):
        rng = np.random.default_rng(seed0 + r)
        X = gen(rng, n_reviews, true_k)
        _, s4 = cluster_k(X, 4)
        sil4.append(s4)
        sk = [(k, cluster_k(X, k)[1]) for k in range(2, 9)]
        bk = max(sk, key=lambda z: z[1])[0]
        best_k.append(bk)
        if bk == 4:
            picks4 += 1
    return {"sil4": round(float(np.mean(sil4)), 3),
            "median_bestk": int(np.median(best_k)),
            "pick4_rate": round(picks4 / reps, 3)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--reps", type=int, default=200)
    reps = ap.parse_args().reps
    import time; t0 = time.time()
    print(f"\n# Truth-recovery yardstick -- meta-genome (forced-k=4 'species' clustering)")
    print(f"reps={reps}/cell  n_reviews=307  n_features={N_FEATURES}  seed={BASE_SEED}\n")
    print(f"{'truth':18s} | {'silhouette(k=4)':>15s} | {'median best-k':>13s} | {'P(best-k==4)':>12s}")
    for label, tk in [("1 cluster (homog)", 1), ("4 clusters (real)", 4)]:
        r = run_cell(307, tk, reps, BASE_SEED)
        print(f"{label:18s} | {r['sil4']:>15.3f} | {r['median_bestk']:>13d} | {r['pick4_rate']:>12.3f}")
    print(f"\n(if k=4 were a real discovery, P(best-k==4) should be ~1 for 4-cluster truth")
    print(f" and ~0 for homogeneous truth. {time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
