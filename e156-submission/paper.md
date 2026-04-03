Mahmood Ahmad
Tahir Heart Institute
author@example.com

The Meta-Analysis Genome: Unsupervised Phenotyping of 307 Cochrane Reviews

Can unsupervised clustering of multi-dimensional quality metrics from eight independent projects reveal natural archetypes among Cochrane systematic reviews? We assembled a 26-feature matrix for 307 reviews common across Fragility Atlas, PredictionGap, outcome reporting bias, entropy, evidence half-life, MetaRepair, EvidenceTribunal, and conformal meta-analysis projects, standardized with z-score normalization. Principal component analysis provided dimensionality reduction, followed by K-means clustering into four groups matching quality archetypes with ANOVA F-tests identifying the most discriminating features. Four clusters emerged with median prevalence of pathological reviews at 24 percent with 95% CI 19 to 30: Healthy, Moderate, Pathological requiring over 60 percent correction, and Mixed. Robustness score and adversarial gap were the two most discriminating features with F-statistics exceeding 50 across all four identified clusters. This genome approach provides a data-driven taxonomy beyond single-metric quality assessment toward multidimensional evidence phenotyping. The limitation is that the taxonomy depends on specific input projects, and adding or removing a data source would alter cluster boundaries.

Outside Notes

Type: empirical
Primary estimand: Cluster archetype (4 types)
App: MetaGenome Pipeline v1.0
Data: 307 Cochrane reviews from 8 cross-project datasets
Code: https://github.com/mahmood726-cyber/meta-genome
Version: 1.0
Validation: DRAFT

References

1. Walsh M, Srinathan SK, McAuley DF, et al. The statistical significance of randomized controlled trial results is frequently fragile: a case for a Fragility Index. J Clin Epidemiol. 2014;67(6):622-628.
2. Atal I, Porcher R, Boutron I, Ravaud P. The statistical significance of meta-analyses is frequently fragile: definition of a fragility index for meta-analyses. J Clin Epidemiol. 2019;111:32-40.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI (Claude, Anthropic) was used as a constrained synthesis engine operating on structured inputs and predefined rules for infrastructure generation, not as an autonomous author. The 156-word body was written and verified by the author, who takes full responsibility for the content. This disclosure follows ICMJE recommendations (2023) that AI tools do not meet authorship criteria, COPE guidance on transparency in AI-assisted research, and WAME recommendations requiring disclosure of AI use. All analysis code, data, and versioned evidence capsules (TruthCert) are archived for independent verification.
