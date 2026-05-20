# The Meta-Analysis Genome

Unsupervised phenotyping of 307 Cochrane reviews along 26 quality metrics
drawn from 8 upstream evidence-quality projects (Fragility Atlas,
PredictionGap, ORB, MetaEntropy, EvidenceHalfLife, MetaRepair,
EvidenceTribunal, ConformalMA). PCA + K-Means (k=4) recovers four
evidence archetypes: **Healthy**, **Moderate**, **Mixed**, **Pathological**.

This repository hosts the E156 micro-paper, the analysis script, the
clustered output, and the GitHub Pages reader.

- Project page: <https://mahmood726-cyber.github.io/meta-genome/>
- Micro-paper:  <https://mahmood726-cyber.github.io/meta-genome/e156-submission/>
- Dashboard:    <https://mahmood726-cyber.github.io/meta-genome/e156-submission/assets/dashboard.html>

## Repository layout

```
.
├── pipeline.py            # PCA + K-Means clustering pipeline
├── tests/                 # pytest smoke tests
├── data/output/           # genome_results.csv + genome_summary.json (committed)
├── docs/                  # protocol notes
├── paper/                 # full manuscripts (PLOS Med + draft)
├── e156-submission/       # 156-word micro-paper + Pages assets
├── index.html             # Pages landing page
└── E156-PROTOCOL.md       # pre-registered protocol
```

## Running the pipeline

The pipeline reads CSV outputs from 8 upstream projects, normalises 26
features, runs PCA + K-Means, and writes `genome_results.csv` and
`genome_summary.json`.

```bash
pip install -r requirements.txt

# Option A: point at a single root containing all 8 project folders
export METAGENOME_INPUT_ROOT=/path/to/projects
python pipeline.py

# Option B: pass individual CSV paths
python pipeline.py \
  --fragility  /path/to/fragility_atlas_results.csv \
  --prediction /path/to/prediction_gap_results.csv \
  --orb        /path/to/orb_results.csv \
  --entropy    /path/to/entropy_results.csv \
  --halflife   /path/to/half_life_results.csv \
  --repair     /path/to/metarepair_results.csv \
  --tribunal   /path/to/tribunal_results.csv \
  --conformal  /path/to/conformal_results.csv

# See all options
python pipeline.py --help
```

Resolution order for each input path: CLI flag &gt; `METAGENOME_<PROJECT>`
env var &gt; `<input-root>/<project>/data/output/<file>.csv`.

Output directory defaults to `./data/output/`. Override with `--output`
or `METAGENOME_OUTPUT`.

## Testing

```bash
pip install pytest
pytest
```

## Citation

If you use this work, please cite the E156 micro-paper. See
[`e156-submission/paper.md`](e156-submission/paper.md) and
[`E156-PROTOCOL.md`](E156-PROTOCOL.md).

## License

MIT — see [LICENSE](LICENSE).
