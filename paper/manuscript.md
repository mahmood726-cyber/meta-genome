# The Meta-Analysis Genome: Unsupervised Phenotyping of 307 Cochrane Reviews via Multi-Project Quality Metrics

**Mahmood Ahmad**^1

1. Royal Free Hospital, London, United Kingdom

**Correspondence:** Mahmood Ahmad, mahmood.ahmad2@nhs.net | **ORCID:** 0009-0003-7781-4478

---

## Abstract

**Background:** Individual quality metrics (I-squared, fragility index, Egger's p) each capture one dimension of meta-analytic reliability. No study has combined metrics from multiple independent quality assessment projects to create a multidimensional phenotype of evidence quality.

**Methods:** We assembled a 26-feature quality matrix for 307 Cochrane reviews common across eight independent projects: Fragility Atlas (multiverse robustness), PredictionGap (PI-CI discordance), outcome reporting bias (excess significance), MetaEntropy (information-theoretic heterogeneity), EvidenceHalfLife (analytical stability), MetaRepair (pathology correction), EvidenceTribunal (adversarial specification search), and ConformalMA (distribution-free coverage). Features were z-score normalised. Principal component analysis provided dimensionality reduction, followed by K-means clustering into four archetype groups.

**Results:** Four clusters emerged: Healthy (n=87, 28.3%), Moderate (n=112, 36.5%), Pathological (n=74, 24.1%, requiring >60% correction), and Mixed (n=34, 11.1%). The two most discriminating features were robustness score (F=62.3) and adversarial gap (F=54.1). Pathological reviews had mean I-squared of 71.4%, median fragility index of 2, and 89% showed bimodal Dirichlet process distributions. Healthy reviews had mean I-squared of 18.2%, median fragility index of 12, and 94% concordant multiverse specifications.

**Conclusions:** Multidimensional phenotyping reveals four natural archetypes of evidence quality, providing a data-driven taxonomy that goes beyond any single metric. One in four Cochrane reviews falls into the Pathological archetype.

**Keywords:** evidence quality, unsupervised learning, meta-epidemiology, phenotyping, K-means, PCA, Cochrane reviews

---

## 1. Introduction

Meta-analytic quality is inherently multidimensional. A review may have low heterogeneity but high fragility, or strong statistical significance but a prediction interval crossing the null. Existing quality frameworks (AMSTAR-2, GRADE) assess dimensions qualitatively; quantitative metrics assess them one at a time.^1

We propose an alternative: treat each review as a point in a high-dimensional quality space and use unsupervised machine learning to discover natural groupings. This approach — analogous to genomic phenotyping in precision medicine — reveals which combinations of quality features co-occur and identifies distinct "archetypes" of meta-analytic evidence.

The key enabling factor is that our ecosystem of eight independent quality assessment projects produces overlapping metrics for the same 307 Cochrane reviews, creating a rich feature matrix without additional data collection.

## 2. Methods

### 2.1 Feature Matrix Construction

For each of 307 reviews (Pairwise70, k >= 5), we extracted 26 features from eight projects:

| Project | Features |
|---------|----------|
| Fragility Atlas | Robustness score, significance concordance, specification I-squared |
| PredictionGap | PI width, PI-CI ratio, false reassurance flag |
| Outcome Reporting Bias | Excess significance ratio, composite ORB score |
| MetaEntropy | Normalised entropy, mutual information, multimodality flag |
| EvidenceHalfLife | Studies to stabilise, never-stabilised flag, volatility |
| MetaRepair | Pathology count, correction magnitude, heterogeneity fraction |
| EvidenceTribunal | Adversarial gap, split verdict flag, defence specification |
| ConformalMA | Conformal coverage, standard coverage, coverage gap |

### 2.2 Analysis

Features were z-score normalised. PCA reduced dimensionality; the first 5 components explained 78% of variance. K-means clustering (k=4, determined by elbow method and silhouette score) partitioned reviews into archetypes. ANOVA F-tests identified the most discriminating features.

## 3. Results

### 3.1 Four Archetypes

| Archetype | n (%) | Key Profile |
|-----------|-------|-------------|
| **Healthy** | 87 (28.3%) | Low I², high fragility index, concordant multiverse, narrow PI |
| **Moderate** | 112 (36.5%) | Moderate I², some PI-CI discordance, stable under most specs |
| **Pathological** | 74 (24.1%) | High I², fragile, bimodal, excess significance, >60% correction needed |
| **Mixed** | 34 (11.1%) | Discordant signals: robust on some metrics, fragile on others |

### 3.2 Discriminating Features

Robustness score (F=62.3) and adversarial gap (F=54.1) were the strongest discriminators. Normalised entropy (F=41.7) and PI-CI ratio (F=38.9) followed. Standard I-squared ranked only 8th (F=22.1), confirming that single metrics miss the multidimensional structure.

### 3.3 Archetype Profiles

Pathological reviews: mean I²=71.4%, median MAFI=2, 89% bimodal (Dirichlet process), mean adversarial gap 1.24, 91% split verdicts (Tribunal), mean correction magnitude 0.34 (MetaRepair).

Healthy reviews: mean I²=18.2%, median MAFI=12, 6% bimodal, mean adversarial gap 0.08, 2% split verdicts, mean correction magnitude 0.03.

## 4. Discussion

The Meta-Analysis Genome demonstrates that evidence quality has a natural four-cluster structure that no single metric captures. The Pathological archetype (24.1%) represents reviews where multiple independent quality signals simultaneously flag concern — these are the reviews most likely to mislead guidelines.

The Mixed archetype (11.1%) is clinically the most challenging: these reviews appear robust on some metrics but fragile on others, requiring careful per-dimension assessment rather than a single quality label.

Limitations: the taxonomy depends on the specific input projects; adding or removing a data source would alter cluster boundaries. The K=4 choice, while supported by silhouette analysis, is not unique.

## References

1. Shea BJ, et al. AMSTAR 2. *BMJ*. 2017;358:j4008.
2. Guyatt G, et al. GRADE guidelines. *J Clin Epidemiol*. 2011;64:383-394.

## Data Availability

Code at https://github.com/mahmood726-cyber/meta-genome (MIT licence).
