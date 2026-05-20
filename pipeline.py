"""The Meta-Analysis Genome: PCA + K-Means clustering of Cochrane reviews.

Each review is characterised by 26 metrics drawn from 8 upstream projects:
  - Fragility Atlas (robustness, frac_significant, frac_reversed, k)
  - PredictionGap (pi_ci_ratio, I2, tau2)
  - ORB (orb_score, excess_significance)
  - Entropy (norm_entropy_index, n_modes, skewness, kurtosis)
  - EvidenceHalfLife (volatility, n_flips, stabilizes)
  - MetaRepair (n_pathologies, correction_pct, pct_sampling/heterogeneity/bias)
  - EvidenceTribunal (adversarial_gap, verdict)
  - ConformalMA (cov_conformal, cov_standard, width_ratio_conf_std)

PCA + K-Means (k=4) then characterises each cluster against an ABCD archetype
(Healthy / Moderate / Mixed / Pathological).

Input CSV locations are resolved in this order for each upstream project:
  1. CLI flag, e.g. --fragility /path/to/fragility_atlas_results.csv
  2. Env var, e.g. METAGENOME_FRAGILITY=/path/to/...csv
  3. Default: <input-root>/<project>/data/output/<file>.csv
     where <input-root> = METAGENOME_INPUT_ROOT (default: ./data/input)

Output directory defaults to ./data/output, overridable with --output / METAGENOME_OUTPUT.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = REPO_ROOT / 'data' / 'output'
DEFAULT_INPUT_ROOT = REPO_ROOT / 'data' / 'input'

# project key -> (default sub-path relative to input root, env var suffix)
PROJECTS = {
    'fragility':  ('FragilityAtlas/data/output/fragility_atlas_results.csv', 'FRAGILITY'),
    'prediction': ('PredictionGap/data/output/prediction_gap_results.csv',   'PREDICTION'),
    'orb':        ('OutcomeReportingBias/data/output/orb_results.csv',       'ORB'),
    'entropy':    ('MetaEntropy/data/output/entropy_results.csv',            'ENTROPY'),
    'halflife':   ('EvidenceHalfLife/data/output/half_life_results.csv',     'HALFLIFE'),
    'repair':     ('MetaRepair/data/output/metarepair_results.csv',          'REPAIR'),
    'tribunal':   ('EvidenceTribunal/data/output/tribunal_results.csv',      'TRIBUNAL'),
    'conformal':  ('ConformalMA/data/output/conformal_results.csv',          'CONFORMAL'),
}

FEATURE_NAMES = [
    'k', 'robustness_score', 'frac_significant', 'frac_reversed',
    'pi_ci_ratio', 'I2', 'tau2',
    'orb_score', 'excess_significance',
    'entropy_nei', 'n_modes', 'skewness', 'kurtosis',
    'volatility', 'n_flips', 'stabilizes',
    'n_pathologies', 'correction_pct', 'pct_sampling', 'pct_heterogeneity', 'pct_bias',
    'adversarial_gap', 'split_verdict',
    'cov_conformal', 'cov_standard', 'width_ratio',
]


def load_dataset(path, key='review_id'):
    data = {}
    with open(path, encoding='utf-8', errors='replace') as f:
        for row in csv.DictReader(f):
            data[row[key]] = row
    return data


def safe_float(val, default=0.0):
    try:
        v = float(val)
        return v if math.isfinite(v) else default
    except (ValueError, TypeError):
        return default


def csv_safe(val):
    """Prepend tick to cells starting with =+@\\t\\r to prevent CSV formula injection."""
    s = str(val) if val is not None else ''
    if s and s[0] in ('=', '+', '@', '\t', '\r'):
        return "'" + s
    return s


def resolve_input_paths(cli_args, env=os.environ):
    """Resolve each upstream project's CSV path: CLI > env > default."""
    input_root = Path(
        getattr(cli_args, 'input_root', None)
        or env.get('METAGENOME_INPUT_ROOT')
        or DEFAULT_INPUT_ROOT
    )
    resolved = {}
    for key, (default_subpath, env_suffix) in PROJECTS.items():
        cli_val = getattr(cli_args, key, None)
        env_val = env.get(f'METAGENOME_{env_suffix}')
        resolved[key] = Path(cli_val or env_val or (input_root / default_subpath))
    return resolved, input_root


def build_feature_row(rid, datasets):
    f = datasets['fragility'][rid]
    p = datasets['prediction'][rid]
    o = datasets['orb'][rid]
    e = datasets['entropy'][rid]
    h = datasets['halflife'][rid]
    r = datasets['repair'][rid]
    t = datasets['tribunal'][rid]
    c = datasets['conformal'][rid]
    return [
        safe_float(f.get('k')),
        safe_float(f.get('robustness_score')),
        safe_float(f.get('frac_significant')),
        safe_float(f.get('frac_reversed')),
        safe_float(p.get('pi_ci_ratio')),
        safe_float(p.get('I2')),
        safe_float(p.get('tau2')),
        safe_float(o.get('orb_score')),
        safe_float(o.get('excess_significance')),
        safe_float(e.get('norm_entropy_index')),
        safe_float(e.get('n_modes')),
        safe_float(e.get('skewness')),
        safe_float(e.get('kurtosis')),
        safe_float(h.get('volatility')),
        safe_float(h.get('n_flips')),
        1.0 if h.get('stabilizes') == 'Yes' else 0.0,
        safe_float(r.get('n_pathologies')),
        safe_float(r.get('correction_pct')),
        safe_float(r.get('pct_sampling')),
        safe_float(r.get('pct_heterogeneity')),
        safe_float(r.get('pct_bias')),
        safe_float(t.get('adversarial_gap')),
        1.0 if t.get('verdict') == 'SPLIT' else 0.0,
        safe_float(c.get('cov_conformal')),
        safe_float(c.get('cov_standard')),
        safe_float(c.get('width_ratio_conf_std')),
    ]


def classify_archetype(robustness, adversarial_gap, correction_pct):
    if robustness > 70 and correction_pct < 30:
        return 'Healthy'
    if robustness > 50 and adversarial_gap < 0.3:
        return 'Moderate'
    if correction_pct > 60 or adversarial_gap > 0.5:
        return 'Pathological'
    return 'Mixed'


def parse_args(argv=None):
    p = argparse.ArgumentParser(description='Meta-Analysis Genome: cluster Cochrane reviews.')
    p.add_argument('--input-root', help='Root directory containing the 8 upstream project folders.')
    p.add_argument('--output', help='Output directory (defaults to ./data/output).')
    p.add_argument('--n-clusters', type=int, default=4, help='K for K-Means (default: 4).')
    p.add_argument('--seed', type=int, default=42, help='Random seed (default: 42).')
    for key in PROJECTS:
        p.add_argument(f'--{key}', help=f'Path to {key} results CSV.')
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    output_dir = Path(args.output or os.environ.get('METAGENOME_OUTPUT') or DEFAULT_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_paths, input_root = resolve_input_paths(args)

    print("The Meta-Analysis Genome")
    print("=" * 40)
    print(f"  Input root:  {input_root}")
    print(f"  Output dir:  {output_dir}")

    t0 = time.time()

    missing = [str(path) for path in input_paths.values() if not path.exists()]
    if missing:
        print("\nERROR: missing required input files:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        print(
            "\nSet METAGENOME_INPUT_ROOT, pass --input-root, or pass per-project flags.",
            file=sys.stderr,
        )
        return 2

    datasets = {key: load_dataset(path) for key, path in input_paths.items()}

    common = set(datasets['fragility'])
    for key in ('prediction', 'orb', 'halflife', 'repair', 'tribunal', 'conformal', 'entropy'):
        common &= set(datasets[key])
    print(f"  Common reviews across all 8 projects: {len(common)}")

    if not common:
        print("ERROR: no review IDs in common across all 8 projects.", file=sys.stderr)
        return 3

    review_ids = sorted(common)
    X = np.zeros((len(review_ids), len(FEATURE_NAMES)))
    for i, rid in enumerate(review_ids):
        X[i] = build_feature_row(rid, datasets)

    print(f"  Feature matrix: {X.shape[0]} reviews x {X.shape[1]} features")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = np.nan_to_num(X_scaled, nan=0, posinf=3, neginf=-3)

    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X_scaled)
    var_explained = pca.explained_variance_ratio_
    print(f"  PCA: {var_explained[0]*100:.1f}% + {var_explained[1]*100:.1f}% = {sum(var_explained)*100:.1f}% variance")

    pca_full = PCA(n_components=min(10, X.shape[1]))
    pca_full.fit(X_scaled)
    cumvar = np.cumsum(pca_full.explained_variance_ratio_)
    n_components_90 = int(np.searchsorted(cumvar, 0.90) + 1)
    print(f"  Components for 90% variance: {n_components_90}")

    k = args.n_clusters
    kmeans = KMeans(n_clusters=k, random_state=args.seed, n_init=10)
    labels_km = kmeans.fit_predict(X_scaled)

    print(f"\n{'='*60}")
    print(f"GENOME CLUSTERS (K-Means, k={k})")
    print(f"{'='*60}")

    cluster_profiles = {}
    for c in range(k):
        mask = labels_km == c
        n_c = int(np.sum(mask))
        profile = {fname: {'mean': float(np.mean(X[mask, j])), 'std': float(np.std(X[mask, j]))}
                   for j, fname in enumerate(FEATURE_NAMES)}

        rob = profile['robustness_score']['mean']
        gap = profile['adversarial_gap']['mean']
        corr = profile['correction_pct']['mean']
        stab = profile['stabilizes']['mean']
        archetype = classify_archetype(rob, gap, corr)

        cluster_profiles[c] = {
            'n': n_c,
            'archetype': archetype,
            'robustness': round(rob, 1),
            'adversarial_gap': round(gap, 3),
            'correction_pct': round(corr, 1),
            'stabilizes_pct': round(stab * 100, 1),
            'n_modes_mean': round(profile['n_modes']['mean'], 1),
            'conformal_coverage': round(profile['cov_conformal']['mean'], 3),
            'standard_coverage': round(profile['cov_standard']['mean'], 3),
        }

        print(f"\n  Cluster {c} — {archetype} (n={n_c})")
        print(f"    Robustness: {rob:.1f}%")
        print(f"    Adversarial gap: {gap:.3f}")
        print(f"    Correction: {corr:.1f}%")
        print(f"    Stabilizes: {stab*100:.1f}%")
        print(f"    Modes: {profile['n_modes']['mean']:.1f}")
        print(f"    Conformal cov: {profile['cov_conformal']['mean']:.3f}")
        print(f"    Standard cov: {profile['cov_standard']['mean']:.3f}")

    from scipy.stats import f_oneway
    f_scores = []
    for j, fname in enumerate(FEATURE_NAMES):
        groups = [X_scaled[labels_km == c, j] for c in range(k)]
        groups = [g for g in groups if len(g) > 1]
        if len(groups) >= 2:
            f_stat, p_val = f_oneway(*groups)
            f_scores.append((fname, float(f_stat), float(p_val)))
        else:
            f_scores.append((fname, 0.0, 1.0))

    f_scores.sort(key=lambda x: -x[1])
    print(f"\n{'='*60}")
    print("TOP GENOME FEATURES (most discriminating)")
    print(f"{'='*60}")
    for fname, f_stat, p_val in f_scores[:10]:
        print(f"  {fname:25s}  F={f_stat:8.1f}  p={p_val:.4f}")

    rows = []
    for i, rid in enumerate(review_ids):
        row = {
            'review_id': rid,
            'pc1': round(float(X_2d[i, 0]), 4),
            'pc2': round(float(X_2d[i, 1]), 4),
            'cluster': int(labels_km[i]),
            'archetype': cluster_profiles[labels_km[i]]['archetype'],
        }
        for j, fname in enumerate(FEATURE_NAMES):
            row[fname] = round(float(X[i, j]), 4)
        rows.append(row)

    fields = list(rows[0].keys())
    safe_rows = [{k: csv_safe(v) for k, v in row.items()} for row in rows]
    with open(output_dir / 'genome_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(safe_rows)

    summary = {
        'n_reviews': len(review_ids),
        'n_features': len(FEATURE_NAMES),
        'pca_variance_explained': [round(float(v), 3) for v in var_explained],
        'n_components_90pct': n_components_90,
        'clusters': cluster_profiles,
        'top_features': [{'name': n, 'f_stat': round(f, 1)} for n, f, _ in f_scores[:10]],
        'elapsed': round(time.time() - t0, 1),
    }
    with open(output_dir / 'genome_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Saved to {output_dir}/ in {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
