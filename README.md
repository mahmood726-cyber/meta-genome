# meta-genome

The Meta-Analysis Genome: Multi-Dimensional Profiling of 307 Cochrane Reviews under an Imposed ABCD Grading

PCA + K-Means profiling of 26 quality metrics across 307 Cochrane reviews into
four evidence archetypes. **Important honesty note:** the four-way split is an
**imposed ABCD grading scheme** (`KMeans` is run with `n_clusters=4` hardcoded),
**not "4 species discovered via clustering."** Because k=4 is fixed, K-Means
always returns four groups whether or not four real clusters exist. The pipeline
therefore reports cluster-validity diagnostics (silhouette at k=4, a
silhouette-vs-k curve over k in 2..8, and the model-selection best-k) and warns
when the 4-way structure is not data-supported.

A seeded truth-recovery check (`truth-recovery/`) quantifies why hardcoded k=4
cannot stand in for discovery: on truly homogeneous data the silhouette at k=4
is ~0.095 and proper model selection picks k=4 only ~0.5% of the time, vs
silhouette ~0.617 and ~90% on genuine 4-cluster data. The silhouette cleanly
discriminates real structure from noise; the hardcoded k does not.

_Status: Active (portfolio registry)._
