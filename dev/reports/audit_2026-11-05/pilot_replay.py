"""Check bit-exact text replay separately from changing evaluator scores."""
import hashlib
import json
import pathlib
from analyze import stats
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
old=json.loads((ROOT/'dev/runs/EXP-001/exp001_results.json').read_text(encoding='utf-8'))
new=json.loads((HERE/'replication_exp001_german/exp001_results.json').read_text(encoding='utf-8'))
result={'interpretation':'Fresh greedy replay using recovered historical German inputs reproduces saved plan text. This supports reproducibility of these texts; it does not recover the old evaluator or prove every claimed historical execution event.',
    'conditions':{}}
for condition,rr in new.items():
    if not condition.startswith('condition_'):continue
    historical={r['scenario_id']:r for r in old[condition]}
    records=[]
    for r in rr:
        o=historical[r['scenario_id']]
        records.append({'scenario_id':r['scenario_id'],'plan_identical':o['plan']==r['plan'],
            'plan_sha256':hashlib.sha256(r['plan'].encode()).hexdigest(),
            'stored_old_recall':o['eval']['recall'],'fresh_current_recall':r['eval']['recall'],
            'invariant_assignment_identical':o['eval']['matched_invariants']==r['eval']['matched_invariants']})
    result['conditions'][condition]={'n':len(records),'identical_plans':sum(x['plan_identical'] for x in records),
        'changed_invariant_assignments':sum(not x['invariant_assignment_identical'] for x in records),'records':records}
result['paired_pilot_comparisons_exploratory']={}
for version,data in [('stored_historical_scores',old),('fresh_current_evaluator_scores',new)]:
    def exact(item):
        e=item['eval'];return len(e['matched_invariants'])/e['total_invariants']
    b={r['scenario_id']:r for r in data['condition_B_verbose_cot']}
    c={r['scenario_id']:r for r in data['condition_C_concept_routed']}
    ids=sorted(set(b)&set(c))
    result['paired_pilot_comparisons_exploratory'][version]=stats([exact(c[s]) for s in ids],[exact(b[s]) for s in ids])
(HERE/'pilot_replay.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:{x:v[x] for x in ['n','identical_plans','changed_invariant_assignments']} for k,v in result['conditions'].items()}))
