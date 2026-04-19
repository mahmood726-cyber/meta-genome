# E156 Protocol — `meta-genome`

This repository is the source code and dashboard backing an E156 micro-paper on the [E156 Student Board](https://mahmood726-cyber.github.io/e156/students.html).

---

## `[95]` The Meta-Analysis Genome: Unsupervised Phenotyping of 307 Cochrane Reviews

**Type:** empirical  |  ESTIMAND: Cluster archetype (4 types)  
**Data:** 307 Cochrane reviews from 8 cross-project datasets

### 156-word body

Can unsupervised clustering of multi-dimensional quality metrics from eight independent projects reveal natural archetypes among Cochrane systematic reviews? We assembled a 26-feature matrix for 307 reviews common across Fragility Atlas, PredictionGap, outcome reporting bias, entropy, evidence half-life, MetaRepair, EvidenceTribunal, and conformal meta-analysis projects, standardized with z-score normalization. Principal component analysis provided dimensionality reduction, followed by K-means clustering into four groups matching quality archetypes with ANOVA F-tests identifying the most discriminating features. Four clusters emerged with median prevalence of pathological reviews at 24 percent with 95% CI 19 to 30: Healthy, Moderate, Pathological requiring over 60 percent correction, and Mixed. Robustness score and adversarial gap were the two most discriminating features with F-statistics exceeding 50 across all four identified clusters. This genome approach provides a data-driven taxonomy beyond single-metric quality assessment toward multidimensional evidence phenotyping. The limitation is that the taxonomy depends on specific input projects, and adding or removing a data source would alter cluster boundaries.

### Submission metadata

```
Corresponding author: Mahmood Ahmad <mahmood.ahmad2@nhs.net>
ORCID: 0000-0001-9107-3704
Affiliation: Tahir Heart Institute, Rabwah, Pakistan

Links:
  Code:      https://github.com/mahmood726-cyber/meta-genome
  Protocol:  https://github.com/mahmood726-cyber/meta-genome/blob/main/E156-PROTOCOL.md
  Dashboard: https://mahmood726-cyber.github.io/meta-genome/

References (topic pack: multilevel / three-level meta-analysis):
  1. Cheung MW-L. 2014. Modeling dependent effect sizes with three-level meta-analyses: a structural equation modeling approach. Psychol Methods. 19(2):211-229. doi:10.1037/a0032968
  2. Van den Noortgate W, López-López JA, Marín-Martínez F, Sánchez-Meca J. 2013. Three-level meta-analysis of dependent effect sizes. Behav Res Methods. 45(2):576-594. doi:10.3758/s13428-012-0261-6

Data availability: No patient-level data used. Analysis derived exclusively
  from publicly available aggregate records. All source identifiers are in
  the protocol document linked above.

Ethics: Not required. Study uses only publicly available aggregate data; no
  human participants; no patient-identifiable information; no individual-
  participant data. No institutional review board approval sought or required
  under standard research-ethics guidelines for secondary methodological
  research on published literature.

Funding: None.

Competing interests: MA serves on the editorial board of Synthēsis (the
  target journal); MA had no role in editorial decisions on this
  manuscript, which was handled by an independent editor of the journal.

Author contributions (CRediT):
  [STUDENT REWRITER, first author] — Writing – original draft, Writing –
    review & editing, Validation.
  [SUPERVISING FACULTY, last/senior author] — Supervision, Validation,
    Writing – review & editing.
  Mahmood Ahmad (middle author, NOT first or last) — Conceptualization,
    Methodology, Software, Data curation, Formal analysis, Resources.

AI disclosure: Computational tooling (including AI-assisted coding via
  Claude Code [Anthropic]) was used to develop analysis scripts and assist
  with data extraction. The final manuscript was human-written, reviewed,
  and approved by the author; the submitted text is not AI-generated. All
  quantitative claims were verified against source data; cross-validation
  was performed where applicable. The author retains full responsibility for
  the final content.

Preprint: Not preprinted.

Reporting checklist: PRISMA 2020.

Target journal: ◆ Synthēsis (https://www.synthesis-medicine.org/index.php/journal)
  Section: Methods Note — submit the 156-word E156 body verbatim as the main text.
  The journal caps main text at ≤400 words; E156's 156-word, 7-sentence
  contract sits well inside that ceiling. Do NOT pad to 400 — the
  micro-paper length is the point of the format.

Manuscript license: CC-BY-4.0.
Code license: MIT.

SUBMITTED: [ ]
```


---

_Auto-generated from the workbook by `C:/E156/scripts/create_missing_protocols.py`. If something is wrong, edit `rewrite-workbook.txt` and re-run the script — it will overwrite this file via the GitHub API._