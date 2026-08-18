from pathlib import Path
import yaml

for path in (Path('action.yml'), Path('.github/workflows/example-diffly.yml')):
    parsed = yaml.safe_load(path.read_text())
    assert isinstance(parsed, dict), path
workflow = yaml.safe_load(Path('.github/workflows/example-diffly.yml').read_text())
assert workflow['permissions']['contents'] == 'read'
assert workflow['permissions']['pull-requests'] == 'write'
assert len(Path('.github/workflows/example-diffly.yml').read_text().splitlines()) <= 10
print('Action YAML and workflow invariants validated')
