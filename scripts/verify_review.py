"""Read-only consistency checks for the current final mainline evidence."""
import csv
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def table(name):
    with (ROOT / 'data' / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def quantile(values, q):
    values = sorted(values)
    pos = (len(values)-1)*q
    lo, hi = math.floor(pos), math.ceil(pos)
    return values[lo]+(values[hi]-values[lo])*(pos-lo)


def main():
    manifest = json.loads((ROOT/'RELEASE_MANIFEST.json').read_text(encoding='utf-8'))
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and '.git' not in p.relative_to(ROOT).parts}
    assert actual == set(manifest['files']) | {'RELEASE_MANIFEST.json'}
    for name, record in manifest['files'].items():
        p = (ROOT/name).resolve()
        assert p.is_relative_to(ROOT)
        data = p.read_bytes()
        assert len(data) == record['bytes'], name
        assert hashlib.sha256(data).hexdigest() == record['sha256'], name
    expected_rows = {'derived_event_locations.csv':71, 'location_quantiles.csv':32,
        'location_summary_all_N.csv':464, 'probability_points.csv':696,
        'simultaneous_bands.csv':4872, 'exposure_counts.csv':5800}
    tables = {name:table(name) for name in expected_rows}
    for name, count in expected_rows.items():
        assert len(tables[name]) == count, name
    events = tables['derived_event_locations.csv']
    assert all(r['side'] == 'bull' for r in events)
    groups = []
    for n,count,days,origins,no_pass,target in [
        (5,35,24,152,34,[.5718,1.7148,3.0473,6.6751,9.5017]),
        (10,36,27,112,36,[.8689,1.8556,3.226,6.3369,9.6446])]:
        g = [r for r in events if int(r['N']) == n]
        assert len(g) == count and len({r['session_date'] for r in g}) == days
        vals = [float(r['pivot_signed_bp']) for r in g]
        assert all(math.isfinite(x) for x in vals)
        qs = [quantile(vals,q) for q in [.1,.25,.5,.75,.9]]
        assert all(abs(a-b)<.00011 for a,b in zip(qs,target))
        matches = [r for r in tables['location_quantiles.csv'] if
            r['direction']=='bull' and r['context']=='1' and int(r['N'])==n
            and r['origin_band']=='0' and r['outcome']=='0']
        assert len(matches)==1
        row=matches[0]
        assert int(row['nonoverlap_events'])==count and int(row['event_days'])==days
        assert int(row['nonoverlap_origins'])==origins
        assert all(abs(a-b)<.00011 for a,b in zip(qs,json.loads(row['pivot_bp_q10_q25_q50_q75_q90'])))
        for key in ['pivot_order_counts','confirm_order_counts']:
            order=json.loads(row[key]);assert sum(order)==count and order[0]==no_pass
        assert sum(x<0 for x in vals)==(1 if n==5 else 0)
        groups.append({'N':n,'records':count,'days':days,'eligible_nonoverlap_origins':origins,'no_close_passage':no_pass,'pivot_quantiles':[round(x,4) for x in qs]})
    probabilities=[]
    for cohort,b,p in [('all',-.4754,-.9716),('pullback_A',4.6580,4.5448),('uptrend_C',-.8413,-1.2839)]:
        match=[r for r in tables['probability_points.csv'] if r['cohort']==cohort and r['configuration']=='S3' and r['anchor']=='0' and r['N']=='5']
        assert len(match)==1
        row=match[0]
        assert abs(float(row['delta_B_pp'])-b)<.00011 and abs(float(row['delta_P_pp'])-p)<.00011
        probabilities.append({'cohort':cohort,'strict_gap_pp':b,'tolerant_gap_pp':p})
    bands=tables['simultaneous_bands.csv']
    native=[r for r in bands if r['configuration_or_change'] in ['S0','S1','S2','S3'] and r['metric']=='delta']
    assert len(native)==1392
    for r in native:
        assert abs(float(r['point_pct_or_pp'])) <= float(r['halfwidth20'])
        assert abs(float(r['point_pct_or_pp'])) <= float(r['halfwidth60'])
    adverse=[r for r in bands if r['N']=='14' and r['configuration_or_change']=='S2-S1' and r['context_0all_1A_2C']=='1' and r['outcome_0Borigin_1Blow_2Porigin_3Plow']=='0' and r['metric']=='delta']
    assert len(adverse)==1
    row=adverse[0];point=float(row['point_pct_or_pp'])
    assert point<0 and float(row['halfwidth60'])<abs(point)<float(row['halfwidth20'])
    links=0
    for p in ROOT.glob('*.md'):
        for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if link.startswith(('https://','http://','#')):continue
            dest=(p.parent/link).resolve();assert dest.is_relative_to(ROOT) and dest.exists(),(p.name,link)
            links+=1
    print(json.dumps({'status':'PASS','scope':'current final mainline saved evidence only',
        'files':len(actual),'event_groups':groups,'quoted_probability_gaps':probabilities,
        'table_rows':expected_rows,'native_gaps_spanning_zero_both_settings':len(native),
        'adverse_block_sensitive_change_retained':True,'local_markdown_links':links,
        'writes':0,'network_calls':0,'empirical_recomputation':False,
        'limitation':'Verifies saved consistency; not source-price reconstruction, estimator correctness or an end-to-end empirical pipeline.'},indent=2))


if __name__=='__main__':
    main()
