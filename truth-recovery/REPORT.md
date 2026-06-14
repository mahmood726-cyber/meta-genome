# Truth-recovery yardstick — meta-genome

**Verdict: the "4 species of evidence quality discovered via clustering" is a
FORCED partition, not a data-driven discovery. The pipeline hardcodes
`n_clusters=4` and never gates on cluster validity, so it reports 4 "species"
whether or not 4 real clusters exist. The good news: the silhouette score DOES
discriminate real structure from noise — so the fix is to report and act on it.**

## The issue
`pipeline.py` clusters reviews with `KMeans(n_clusters=4, ... "matching the ABCD
grading metaphor")`. K-Means with k=4 always returns a 4-way partition of any
point cloud, so "4 species" follows from the *choice of k=4*, not from the data.
The pipeline reports the four clusters without ever checking whether 4 (or any
k>1) is supported.

## Method
Replicate the pipeline's exact clustering (`StandardScaler` + `KMeans(k,
random_state=42, n_init=10)`) on data with a KNOWN number of true clusters
(1 = homogeneous, or 4), and measure (a) the silhouette of the forced k=4 fit and
(b) the k chosen by silhouette over k∈{2..8} (proper model selection). 200
reps/cell, 307 reviews, 8 features.

## Results

| truth              | silhouette(k=4) | median best-k | P(best-k == 4) |
|--------------------|----------------:|--------------:|---------------:|
| 1 cluster (homog)  | 0.095 | 7 | **0.005** |
| 4 clusters (real)  | 0.617 | 4 | **0.900** |

## Findings (all measured)
1. **The "4 species" is forced, not discovered.** On truly homogeneous data
   (no real subgroups), K-Means k=4 still returns four clusters, but proper model
   selection picks k=4 only **0.5%** of the time — the data do not support a 4-way
   structure. On genuinely 4-cluster data, model selection picks k=4 **90%** of the
   time. So a hardcoded k=4 cannot tell the two apart; the published "4 species"
   claim is unjustified by the clustering alone.
2. **But the silhouette is a working validity gate.** It is 0.095 on homogeneous
   data vs 0.617 on real 4-cluster data — a clean separation. The pipeline already
   computes the clustering; it simply never reports or acts on the silhouette. → The
   fix is cheap: report the silhouette (and the gap statistic / silhouette-vs-k
   curve), and either (a) select k by validity rather than hardcoding 4, or (b)
   keep the ABCD 4-way partition but re-frame it honestly as an *imposed grading
   scheme*, not "4 species discovered via clustering."
3. This is the forced-structure cousin of the over-detection findings elsewhere
   (meta-entropy, tda-ma): a structure/number-of-groups claim presented as a
   discovery when the method cannot distinguish it from noise.

## Recommendation
Add a cluster-validity report (silhouette over k, gap statistic) and gate the
"species" claim on it; if the real Cochrane feature matrix has a low silhouette at
k=4, the "4 species" framing must be withdrawn or relabelled as an imposed
4-way grading.

## What did NOT transfer
The clustering IS standard sklearn (no bespoke engine to extract); the truth-
recovery test is the known-#-of-clusters validity check. NPE/conformal not needed.

## Reproduce
```
python truth-recovery/harness.py --reps 200
python truth-recovery/test_truth_recovery.py
```
