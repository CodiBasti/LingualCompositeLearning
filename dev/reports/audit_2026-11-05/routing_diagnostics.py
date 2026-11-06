"""Descriptive routing-set diagnostics; no additional confirmatory tests."""
import collections
import json
import pathlib
HERE=pathlib.Path(__file__).resolve().parent

def main():
    if not (HERE/'semantic_rating_freeze.json').exists():
        raise RuntimeError('Finish and freeze all individual ratings before inspecting arm diagnostics')
    tasks={s['scenario_id']:s for s in json.loads((HERE/'holdout.json').read_text(encoding='utf-8'))}
    controls=[json.loads(s) for s in (HERE/'controls.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
    out={};details=[]
    for arm in ['LCL','natural_labels','renamed_labels']:
        rr=[]
        for r in controls:
            if r['arm']!=arm or r['scenario_id'] not in tasks:continue
            s=tasks[r['scenario_id']];expected=set(s['expected_concepts']);pred=set(r['activated_concepts'])
            q={'scenario_id':r['scenario_id'],'arm':arm,'reference':sorted(expected),'predicted':sorted(pred),
               'primary_label_included':s['expected_concept'] in pred,'all_prescribed_labels_included':expected<=pred,
               'exact_prescribed_set':expected==pred,'jaccard':len(expected&pred)/len(expected|pred),
               'missing':sorted(expected-pred),'additional':sorted(pred-expected)}
            rr.append(q);details.append(q)
        n=len(rr)
        out[arm]={'n':n,**{k:sum(q[k] for q in rr)/n if n else None for k in ['primary_label_included','all_prescribed_labels_included','exact_prescribed_set','jaccard']},
                  'predicted_sets':dict(collections.Counter('+'.join(q['predicted']) for q in rr)),
                  'missing_label_occurrences':dict(collections.Counter(a for q in rr for a in q['missing'])),
                  'additional_label_occurrences':dict(collections.Counter(a for q in rr for a in q['additional']))}
    payload={'status':'descriptive_exploratory','primary_endpoints_unchanged':True,
             'caveat':'Reference sets were prescribed by the same auditor before inference, not independently validated unique correct physical policies. Additional labels are not automatically harmful; missing labels may still be implemented in plan text. Existing VHC100 supplies only one expected label, so no complete-set correctness is inferred there.',
             'arms':out,'details':details}
    (HERE/'routing_diagnostics.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'evaluated_routes':len(details),'arms':len(out)}))

if __name__=='__main__':main()
