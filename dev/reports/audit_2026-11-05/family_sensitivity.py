"""Additional exploratory cross-domain family sensitivity, not a new primary test."""
import collections
import datetime as dt
import json
import pathlib
from analyze import stats
HERE=pathlib.Path(__file__).resolve().parent

def main():
    h=json.loads((HERE/'holdout.json').read_text(encoding='utf-8'))
    rows=json.loads((HERE/'semantic_rows.json').read_text(encoding='utf-8'))
    lookup={s['scenario_id']:s for s in h};bits=collections.defaultdict(list)
    for r in rows:bits[r['arm'],r['scenario_id']].append(r['auditor_pass'])
    arms=sorted({r['arm'] for r in rows});out={}
    for arm in arms:
        if arm=='LCL':continue
        ids=sorted(s for s in lookup if ('LCL',s) in bits and (arm,s) in bits)
        labels=['+'.join(lookup[s]['expected_concepts']) for s in ids]
        result=stats([sum(bits['LCL',s])/len(bits['LCL',s]) for s in ids],[sum(bits[arm,s])/len(bits[arm,s]) for s in ids],labels)
        out['LCL-'+arm]={'n':len(ids),'mean_difference':result.get('mean_difference'),
            'cross_domain_operator_family_clusters':result.get('cluster_sensitivity')}
    payload={'status':'additional_exploratory_sensitivity','primary_tests_unchanged':True,
        'rationale':'The same rule/task families occur across domains. domain+operator clusters can still split structurally related tasks. This broader grouping is a conservative heuristic, not a proven dependency model.',
        'caveat':'Few clusters; intervals unstable. Does not provide a replacement confirmatory p-value.',
        'families':dict(collections.Counter('+'.join(s['expected_concepts']) for s in h)),
        'comparisons':out,'registration':'additional_checks_freeze.json'}
    (HERE/'family_sensitivity.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'family_clusters':len(payload['families']),'comparisons':len(out)}))

if __name__=='__main__':main()
