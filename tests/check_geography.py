"""Check additive labels, API consistency, and dashboard interactions."""
import sys
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pandas as pd
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest
from nammaflow.data import load_data
import api

profiles, suggestions = load_data(ROOT)
for frame, relative, dtype in [
    (profiles, 'reports/ward_level_intelligence/ward_profiles.csv', {'ward_num': 'string'}),
    (suggestions, 'reports/decision_recommendation/investigation_suggestions.csv', {'ward_num': 'string', 'rule_id': 'string'}),
]:
    original = pd.read_csv(ROOT / relative, dtype=dtype)
    pd.testing.assert_frame_equal(frame[original.columns], original)
    assert frame.ward_name.notna().all()
assert len(profiles) == 244
expected = {'b_181': 'Shantala Nagar', 'b_168': 'Padarayanapura', 'b_186': 'Koramangala', 'w_0': 'Other Wards'}
with TestClient(api.app) as client:
    for identifier, name in expected.items():
        detail = client.get(f'/records/{identifier}').json()
        assert detail['profile']['ward_name'] == name
        assert detail['profile']['display_name'] == f'{name} ({identifier})'
        assert all(s['ward_name'] == name for s in detail['suggestions'])
    items = client.get('/investigations', params={'limit': 250}).json()['items']
    lookup = profiles.set_index('ward_num').ward_name.to_dict()
    assert all(item['ward_name'] == lookup[item['ward_num']] for item in items)

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    shutil.copytree(ROOT / 'reports', root / 'reports')
    (root / 'data/reference').mkdir(parents=True)
    path = root / 'data/reference/ward_names.json'
    metadata = json.loads((ROOT / 'data/reference/ward_names.json').read_text())
    del metadata['ward_names']['b_181']
    path.write_text(json.dumps(metadata))
    unmapped, _ = load_data(root)
    row = unmapped.set_index('ward_num').loc['b_181']
    assert row.display_name == 'Unknown area (b_181)'
    assert row.ward_name_status == 'unmapped' and len(unmapped) == 244
    path.write_text('{"ward_names":{"b_181":"A","b_181":"B"}}')
    try:
        load_data(root)
    except ValueError as exc:
        assert 'Duplicate' in str(exc)
    else:
        raise AssertionError('Duplicate lookup accepted')

at = AppTest.from_file(str(ROOT / 'streamlit_app.py'), default_timeout=30).run()
assert not at.exception
assert 'Shantala Nagar (b_181)' in at.selectbox[0].options
assert 'Koramangala (b_186)' in at.selectbox[0].options
for identifier, name in expected.items():
    at.selectbox[0].select(identifier).run()
    assert not at.exception
    assert f'{name} ({identifier})' in [s.value for s in at.subheader]
    if identifier == 'b_168':
        assert any('undefined' in x.value for x in at.info)
at.selectbox[1].select('R01').run()
assert not at.exception
assert any('2 suggestions across 2 records' in x.value for x in at.markdown)
print('PASS: all original report values preserved, 244 labels, API names, unknown-ID fallback, duplicate rejection, dashboard selection and R01.')
