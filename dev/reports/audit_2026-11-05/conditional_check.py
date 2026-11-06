"""Audit the specific correctly-routed-subset claim; explicitly exploratory."""
import json
import pathlib
from analyze import stats
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
raw=json.loads((ROOT/'dev/runs/EXP-002/exp002_results.json').read_text(encoding='utf-8'))
arms={k:{r['scenario_id']:r for r in v} for k,v in raw.items() if k.startswith('condition_')}
c=arms['condition_C_concept_routed'];b=arms['condition_B_verbose']
ids=sorted(s for s,r in c.items() if r['eval']['concept_match'])
def recall(r):return len(r['eval']['matched_invariants'])/r['eval']['total_invariants']
cv=[recall(c[s]) for s in ids];bv=[recall(b[s]) for s in ids]
result={'n':len(ids),'selection':'condition_C_concept_routed eval.concept_match is true; post-treatment selection, not an end-to-end primary comparison',
    'scenario_ids':ids,'conditional_C_recall':sum(cv)/len(cv),'conditional_B_recall_same_ids':sum(bv)/len(bv),
    'unconditional_B_recall':sum(recall(r) for r in b.values())/len(b),
    'paired_conditional_exploratory':stats(cv,bv)}
(HERE/'conditional_routing.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='scenario_ids'}))
