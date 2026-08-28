from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_ci_and_release_workflows_exist_and_parse():
    ci = ROOT / '.github/workflows/ci.yml'
    release = ROOT / '.github/workflows/release.yml'
    assert ci.exists() and release.exists()
    # PyYAML parses the YAML 1.1 key `on` as bool; parsing still catches malformed YAML.
    assert isinstance(yaml.safe_load(ci.read_text(encoding='utf-8')), dict)
    assert isinstance(yaml.safe_load(release.read_text(encoding='utf-8')), dict)


def test_ci_runs_core_quality_gates_and_builds_both_distributions():
    s = (ROOT / '.github/workflows/ci.yml').read_text(encoding='utf-8')
    for expected in [
        'python -m pytest -q',
        'python scripts/run_evals.py --json',
        'scripts/lint_gpt_project.py',
        'scripts/project_hygiene.py',
        'scripts/build_chat_runtime.py',
        'scripts/build_custom_gpt_runtime.py',
        'scripts/validate_distributions.py',
        'sha256sum --check',
    ]:
        assert expected in s


def test_release_uses_release_tag_as_distribution_version_and_uploads_assets():
    s = (ROOT / '.github/workflows/release.yml').read_text(encoding='utf-8')
    assert 'github.event.release.tag_name' in s
    assert 'VERSION="${RELEASE_TAG#v}"' in s
    assert '--version "${{ steps.version.outputs.version }}"' in s
    assert 'gh release upload' in s
    assert 'dist/*.zip' in s and 'dist/*.zip.sha256' in s


def test_project_declares_github_release_support():
    cfg = yaml.safe_load((ROOT/'gpt-project.yaml').read_text(encoding='utf-8'))
    github = cfg['release']['github']
    assert github['enabled'] is True
    assert github['version_source'] == 'github_release_tag'


def test_python_setup_cache_uses_actual_dependency_file_and_current_actions():
    for rel in ['.github/workflows/ci.yml', '.github/workflows/release.yml']:
        text = (ROOT / rel).read_text(encoding='utf-8')
        assert 'actions/checkout@v7' in text
        assert 'actions/setup-python@v7' in text
        assert 'cache: pip' in text
        assert 'cache-dependency-path: requirements-dev.txt' in text
