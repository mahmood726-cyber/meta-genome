import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

REQUIRED_SUBMISSION_FILES = ('config.json', 'paper.md', 'protocol.md', 'index.html')


def test_repository_smoke():
    assert REPO_ROOT.exists()

    submission = REPO_ROOT / 'e156-submission'
    if submission.is_dir():
        for name in REQUIRED_SUBMISSION_FILES:
            assert (submission / name).exists(), name

        config = json.loads((submission / 'config.json').read_text(encoding='utf-8'))
        body = config.get('body', '')
        assert len(body.split()) == 156

        sentences = config.get('sentences', [])
        assert len(sentences) == 7
        assert all((entry.get('text') if isinstance(entry, dict) else str(entry)).strip() for entry in sentences)
        assert config.get('notes', {}).get('code')
        return

    candidates = []
    for base in [REPO_ROOT, REPO_ROOT / 'src', REPO_ROOT / 'app', REPO_ROOT / 'scripts']:
        if not base.is_dir():
            continue
        for pattern in ('*.py', '*.R', '*.html', '*.js', '*.ts'):
            candidates.extend(base.glob(pattern))
    assert candidates


def test_safe_float_handles_bad_input():
    from pipeline import safe_float
    assert safe_float('1.5') == 1.5
    assert safe_float('') == 0.0
    assert safe_float(None) == 0.0
    assert safe_float('nan') == 0.0
    assert safe_float('inf') == 0.0
    assert safe_float('not-a-number', default=-1) == -1


def test_csv_safe_neutralises_formula_prefixes():
    from pipeline import csv_safe
    assert csv_safe('=SUM(A1:A2)') == "'=SUM(A1:A2)"
    assert csv_safe('+1') == "'+1"
    assert csv_safe('@cmd') == "'@cmd"
    assert csv_safe('\tHELLO') == "'\tHELLO"
    assert csv_safe('CD000028') == 'CD000028'
    assert csv_safe(None) == ''
    assert csv_safe(3.14) == '3.14'


def test_classify_archetype_boundaries():
    from pipeline import classify_archetype
    assert classify_archetype(robustness=80, adversarial_gap=0.1, correction_pct=10) == 'Healthy'
    assert classify_archetype(robustness=60, adversarial_gap=0.2, correction_pct=40) == 'Moderate'
    assert classify_archetype(robustness=40, adversarial_gap=0.8, correction_pct=50) == 'Pathological'
    assert classify_archetype(robustness=40, adversarial_gap=0.1, correction_pct=10) == 'Mixed'


def test_resolve_input_paths_prefers_cli_then_env_then_default(tmp_path, monkeypatch):
    from pipeline import resolve_input_paths, PROJECTS

    class Args:
        pass

    args = Args()
    args.input_root = str(tmp_path)
    cli_override = tmp_path / 'custom_fragility.csv'
    for key in PROJECTS:
        setattr(args, key, None)
    args.fragility = str(cli_override)

    env = {'METAGENOME_ORB': '/env/orb.csv'}
    paths, root = resolve_input_paths(args, env=env)

    assert paths['fragility'] == cli_override          # CLI wins
    assert str(paths['orb']) == '/env/orb.csv'         # env when no CLI
    assert paths['entropy'].is_relative_to(tmp_path)   # default under input_root
    assert root == tmp_path
