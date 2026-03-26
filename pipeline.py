"""The Meta-Analysis Genome: UMAP clustering of 307 Cochrane reviews.

Each review is characterised by 30+ metrics from 8 projects:
  - Fragility Atlas (robustness, eta2, frac_sig)
  - PredictionGap (pi_ci_ratio, discordance, I2)
  - ORB (orb_score, excess_sig)
  - BiasForensics (n_detect, concordance, egger_p)
  - MetaReproducer (oa_coverage, match_rate)
  - EvidenceHalfLife (half_life_k, volatility, n_flips)
  - MetaRepair (grade, n_pathologies, correction_pct, uncertainty decomposition)
  - EvidenceTribunal (verdict, adversarial_gap)
  - ConformalMA (coverage gap, width ratio)
  - Entropy (NEI, n_modes, skewness, kurtosis)

Apply UMAP to find natural clusters. Then characterise each cluster.
"""

import csv
import json
import math
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from collections import Counter
import time

OUTPUT_DIR = Path(r'C:\Models\MetaGenome\data\output')


def load_dataset(path, key='review_id'):
    data = {}
    with open(path, encoding='utf-8', errors='replace') as f:
        for row in csv.DictReader(f):
            data[row[key]] = row
    return data


def safe_float(val, default=0):
    try:
        v = float(val)
        return v if math.isfinite(v) else default
    except (ValueError, TypeError):
        return default


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("The Meta-Analysis Genome")
    print("=" * 40)

    t0 = time.time()

    # Load all datasets
    fragility = load_dataset(r'C:\FragilityAtlas\data\output\fragility_atlas_results.csv')
    prediction = load_dataset(r'C:\PredictionGap\data\output\prediction_gap_results.csv')
    orb = load_dataset(r'C:\OutcomeReportingBias\data\output\orb_results.csv')
    entropy = load_dataset(r'C:\Models\MetaEntropy\data\output\entropy_results.csv')
    halflife = load_dataset(r'C:\EvidenceHalfLife\data\output\half_life_results.csv')
    repair = load_dataset(r'C:\Models\MetaRepair\data\output\metarepair_results.csv')
    tribunal = load_dataset(r'C:\Models\EvidenceTribunal\data\output\tribunal_results.csv')
    conformal = load_dataset(r'C:\Models\ConformalMA\data\output\conformal_results.csv')

    # Common reviews
    common = set(fragility) & set(prediction) & set(orb) & set(halflife) & set(repair) & set(tribunal) & set(conformal) & set(entropy)
    print(f"  Common reviews across all 8 projects: {len(common)}")

    # Build feature matrix
    feature_names = [
        'k', 'robustness_score', 'frac_significant', 'frac_reversed',
        'pi_ci_ratio', 'I2', 'tau2',
        'orb_score', 'excess_significance',
        'entropy_nei', 'n_modes', 'skewness', 'kurtosis',
        'volatility', 'n_flips', 'stabilizes',
        'n_pathologies', 'correction_pct', 'pct_sampling', 'pct_heterogeneity', 'pct_bias',
        'adversarial_gap', 'split_verdict',
        'cov_conformal', 'cov_standard', 'width_ratio',
    ]

    review_ids = sorted(common)
    X = np.zeros((len(review_ids), len(feature_names)))

    for i, rid in enumerate(review_ids):
        f = fragility[rid]
        p = prediction[rid]
        o = orb[rid]
        e = entropy[rid]
        h = halflife[rid]
        r = repair[rid]
        t = tribunal[rid]
        c = conformal[rid]

        X[i] = [
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

    print(f"  Feature matrix: {X.shape[0]} reviews x {X.shape[1]} features")

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Replace NaN/inf after scaling
    X_scaled = np.nan_to_num(X_scaled, nan=0, posinf=3, neginf=-3)

    # PCA (for visualization — UMAP needs umap-learn which may not be installed)
    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X_scaled)
    var_explained = pca.explained_variance_ratio_

    print(f"  PCA: {var_explained[0]*100:.1f}% + {var_explained[1]*100:.1f}% = {sum(var_explained)*100:.1f}% variance")

    # Also do PCA with more components for analysis
    pca_full = PCA(n_components=min(10, X.shape[1]))
    X_pca = pca_full.fit_transform(X_scaled)
    cumvar = np.cumsum(pca_full.explained_variance_ratio_)
    n_components_90 = np.searchsorted(cumvar, 0.90) + 1
    print(f"  Components for 90% variance: {n_components_90}")

    # K-Means clustering (k=4, matching the ABCD grading metaphor)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels_km = kmeans.fit_predict(X_scaled)

    # Characterise clusters
    print(f"\n{'='*60}")
    print("GENOME CLUSTERS (K-Means, k=4)")
    print(f"{'='*60}")

    cluster_profiles = {}
    for c in range(4):
        mask = labels_km == c
        n_c = np.sum(mask)
        profile = {}
        for j, fname in enumerate(feature_names):
            vals = X[mask, j]
            profile[fname] = {'mean': float(np.mean(vals)), 'std': float(np.std(vals))}

        # Determine cluster character
        rob = profile['robustness_score']['mean']
        gap = profile['adversarial_gap']['mean']
        corr = profile['correction_pct']['mean']
        stab = profile['stabilizes']['mean']

        if rob > 70 and corr < 30:
            archetype = 'Healthy'
        elif rob > 50 and gap < 0.3:
            archetype = 'Moderate'
        elif corr > 60 or gap > 0.5:
            archetype = 'Pathological'
        else:
            archetype = 'Mixed'

        cluster_profiles[c] = {
            'n': int(n_c),
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

    # Feature importance: which features best separate clusters?
    # Use F-statistic per feature
    from scipy.stats import f_oneway
    f_scores = []
    for j, fname in enumerate(feature_names):
        groups = [X_scaled[labels_km == c, j] for c in range(4)]
        groups = [g for g in groups if len(g) > 1]
        if len(groups) >= 2:
            f_stat, p_val = f_oneway(*groups)
            f_scores.append((fname, float(f_stat), float(p_val)))
        else:
            f_scores.append((fname, 0, 1))

    f_scores.sort(key=lambda x: -x[1])
    print(f"\n{'='*60}")
    print("TOP GENOME FEATURES (most discriminating)")
    print(f"{'='*60}")
    for fname, f_stat, p_val in f_scores[:10]:
        print(f"  {fname:25s}  F={f_stat:8.1f}  p={p_val:.4f}")

    # EXPORT
    rows = []
    for i, rid in enumerate(review_ids):
        row = {'review_id': rid, 'pc1': round(float(X_2d[i, 0]), 4), 'pc2': round(float(X_2d[i, 1]), 4),
               'cluster': int(labels_km[i]), 'archetype': cluster_profiles[labels_km[i]]['archetype']}
        for j, fname in enumerate(feature_names):
            row[fname] = round(float(X[i, j]), 4)
        rows.append(row)

    fields = list(rows[0].keys())
    with open(OUTPUT_DIR / 'genome_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        'n_reviews': len(review_ids),
        'n_features': len(feature_names),
        'pca_variance_explained': [round(float(v), 3) for v in var_explained],
        'n_components_90pct': int(n_components_90),
        'clusters': cluster_profiles,
        'top_features': [{'name': n, 'f_stat': round(f, 1)} for n, f, _ in f_scores[:10]],
        'elapsed': round(time.time() - t0, 1),
    }
    with open(OUTPUT_DIR / 'genome_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Saved to {OUTPUT_DIR}/ in {time.time()-t0:.1f}s")


if __name__ == '__main__':
    main()
