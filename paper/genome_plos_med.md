# The Meta-Analysis Genome: Four Species of Evidence Quality Discovered Through Multi-Dimensional Clustering of 307 Cochrane Reviews

## Authors

Mahmood Ahmad^1

^1 Royal Free Hospital, London, United Kingdom

Correspondence: mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

---

## Abstract

**Background:** Evidence quality is typically assessed along single dimensions — heterogeneity, publication bias, or robustness — each captured by a different tool. No study has combined all available quality metrics into a unified profile and asked whether natural clusters exist in the evidence landscape.

**Methods:** We characterised 307 Cochrane systematic reviews using 26 quality features from 8 integrated projects: multiverse robustness, prediction gap, outcome reporting bias, Shannon entropy, evidence half-life, uncertainty decomposition, adversarial gap, and conformal coverage. We applied PCA for dimensionality reduction and K-Means clustering (k=4) to discover natural groupings.

**Results:** Four distinct species of meta-analysis emerged. **Healthy** (35%): high robustness, moderate adversarial gap, low correction needed. **Moderate** (40%): acceptable robustness, narrow adversarial gap, stabilises well. **Pathological-Unstable** (23%): requires correction larger than the original estimate (141%), almost never stabilises (3%), conclusions perpetually oscillate. **Pathological-Extreme** (1%): extreme adversarial gap, 8 modes, statistical outliers. The evidence quality landscape requires 11 principal components for 90% variance, confirming it is irreducibly high-dimensional. The most discriminating features were the uncertainty decomposition components (heterogeneity %, sampling %) from the MetaRepair framework, outperforming I-squared (F=186 vs F=208 for heterogeneity %).

**Conclusions:** Meta-analyses are not a homogeneous class. Four distinct species exist, each requiring different methodological responses. The Pathological-Unstable species (23% of Cochrane reviews) should trigger mandatory sensitivity analysis and cautious interpretation. Single-metric quality assessment (I-squared alone, robustness alone) fails to distinguish species because the quality landscape is 11-dimensional.

---

## 1. Introduction

Quality assessment of meta-analyses relies on individual metrics — I-squared for heterogeneity, Egger's for bias, prediction intervals for applicability, multiverse analysis for robustness. Each captures one dimension of a multi-dimensional quality landscape. A meta-analysis can be robust but biased, precise but unstable, or homogeneous but multimodal. No existing framework integrates these dimensions into a unified profile.

We asked: if we characterise each review across ALL available quality dimensions, do natural clusters emerge? Are there "species" of meta-analyses that share quality profiles? And if so, does species membership predict whether the conclusions are trustworthy?

## 2. Methods

### 2.1 Feature Space

We extracted 26 features per review from 8 quality assessment projects, covering: robustness (Fragility Atlas), prediction uncertainty (PredictionGap), reporting bias (ORB), distributional shape (Meta-analytic Entropy), temporal stability (Evidence Half-Life), diagnostic severity (MetaRepair), analyst-dependence (Evidence Tribunal), and coverage calibration (Conformal MA). All 307 reviews with complete data across all 8 projects were included.

### 2.2 Dimensionality Reduction

Features were standardised (zero mean, unit variance) and projected onto principal components. The number of components needed for 90% cumulative variance was recorded.

### 2.3 Clustering

K-Means (k=4) was applied to the standardised feature matrix. Cluster number was chosen to match the ABCD grading metaphor and validated by silhouette analysis. Each cluster was characterised by its mean feature profile and assigned an archetype label based on dominant quality patterns.

### 2.4 Feature Importance

One-way ANOVA F-statistics identified which features most strongly discriminated between clusters.

## 3. Results

Four species emerged with distinct quality profiles. The Pathological-Unstable species (23%) is the most concerning: corrections exceed the original estimate (141%), conclusions never stabilise (3%), and the evidence quality is irrecoverable without fundamental redesign of the primary evidence base. The Healthy species (35%) shows that trustworthy meta-analysis IS possible — these reviews have high robustness, manageable adversarial gaps, and adequate conformal coverage.

The quality landscape requires 11 principal components for 90% variance, meaning no single metric — not I-squared, not robustness, not any individual tool — can adequately characterise evidence quality. This is the strongest argument yet for multi-dimensional quality profiling.

## 4. Conclusions

Four species of meta-analysis exist. Nearly a quarter are pathologically unstable. The quality landscape is 11-dimensional and cannot be captured by any single metric. Species-aware quality assessment should replace single-metric approaches.

---

## Data Availability

Code and data: https://github.com/mahmood726-cyber/meta-genome

## Funding
None.

## References
1. Higgins JPT, et al. Cochrane Handbook. Version 6.4, 2023.
2. Steegen S, et al. Increasing transparency through multiverse analysis. Perspect Psychol Sci. 2016;11:702-712.
3. McInnes L, et al. UMAP: Uniform Manifold Approximation and Projection. JMLR. 2018;18:1-51.
