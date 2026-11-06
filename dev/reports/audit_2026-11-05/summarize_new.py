"""Join isolated new runs and blinded auditor ratings without pseudoreplication."""
import collections
import csv
import hashlib
import json
import pathlib
from analyze import stats,holm,mean,tabulate

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
ARMS=['cot_equal','structured_direct','LCL','natural_labels','renamed_labels']

def load(name):return json.loads((HERE/name).read_text(encoding='utf-8'))
def rows(name):
    p=HERE/name
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()] if p.exists() else []
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')

def cost_summary(rr):
    return {'n':len(rr),'mean_input_tokens_all_stages':mean([x['costs']['input_tokens'] for x in rr]),
        'mean_output_tokens_all_stages':mean([x['costs']['output_tokens'] for x in rr]),
        'mean_generation_calls':mean([x['costs']['calls'] for x in rr]),
        'mean_end_to_end_seconds':mean([x['wall_seconds'] for x in rr]),
        'at_least_one_stage_hit_token_cap':sum(x['costs']['truncated'] for x in rr)}

def kappa(pairs):
    mat=collections.Counter((bool(a),bool(b)) for a,b in pairs);n=len(pairs)
    if not n:return {'n':0,'kappa':None}
    pa=sum(a for a,b in pairs)/n;pb=sum(b for a,b in pairs)/n
    po=sum(a==b for a,b in pairs)/n;pe=pa*pb+(1-pa)*(1-pb)
    return {'n':n,'agreement':po,'kappa':(po-pe)/(1-pe) if pe<1 else None,
        'reference_pass_comparison_pass':mat[True,True],'reference_pass_comparison_fail':mat[True,False],
        'reference_fail_comparison_pass':mat[False,True],'reference_fail_comparison_fail':mat[False,False],
        'reference_is_single_auditor_not_human_gold_standard':True}

def main():
    h=load('holdout.json');b=json.loads((ROOT/'dev/data/benchmarks/benchmark_v2.json').read_text(encoding='utf-8'))
    controls=rows('controls.jsonl');rep=rows('replication.jsonl');lat=rows('latency.jsonl');judge=rows('judge.jsonl')
    result={'controls':{},'replication':{},'latency':{},'completion':{},'semantic':{'status':'not_yet_rated'}}
    for exp,benchmark in [('EXP001_current_english',json.loads((ROOT/'dev/data/benchmarks/benchmark_v1.json').read_text(encoding='utf-8'))),('EXP001_historical_german',load('benchmark_v1_historical_german.json'))]:
        folder='replication_exp001' if exp.endswith('english') else 'replication_exp001_german'
        path=HERE/folder/'exp001_results.json'
        if path.exists():
            data=json.loads(path.read_text(encoding='utf-8'))
            result['replication'][exp]={arm:tabulate(rr,benchmark)[0] for arm,rr in data.items() if arm.startswith('condition_')}
    for arm in ['A','B','C','D']:
        rr=[x for x in rep if x['arm']==arm]
        if rr:
            result['replication'][arm]={**tabulate(rr,b)[0],**cost_summary(rr)}
            historical=json.loads((ROOT/f'dev/runs/EXP-{3 if arm=="D" else 2:03d}'/f'exp00{3 if arm=="D" else 2}_results.json').read_text(encoding='utf-8'))
            key={'A':'condition_A_naive','B':'condition_B_verbose','C':'condition_C_concept_routed','D':'condition_C_composite'}[arm]
            old={x['scenario_id']:x for x in historical[key]}
            result['replication'][arm]['plan_text_identical_to_stored_active']=sum(x['plan']==old[x['scenario_id']]['plan'] for x in rr)
            result['replication'][arm]['stored_active_recall_on_same_ids']=mean([old[x['scenario_id']]['eval']['recall'] for x in rr])
    for dataset,benchmark in [('holdout',h),('VHC100',b)]:
        data=[x for x in controls if x['dataset']==dataset];arms={arm:{x['scenario_id']:x for x in data if x['arm']==arm} for arm in ARMS}
        ids=sorted(set.intersection(*(set(x) for x in arms.values())))
        result['controls'][dataset]={'complete_paired_scenarios':len(ids),'complete_ids':ids,
            'unpaired_rows':len(data)-len(ids)*5,'arms':{},'regex_contrasts_exploratory':{}}
        for arm in ARMS:
            rr=[arms[arm][sid] for sid in ids]
            summary,_,_=tabulate(rr,benchmark)
            result['controls'][dataset]['arms'][arm]={**summary,**cost_summary(rr)}
        if ids:
            for arm in [a for a in ARMS if a!='LCL']:
                result['controls'][dataset]['regex_contrasts_exploratory']['LCL-'+arm]=stats(
                    [len(arms['LCL'][sid]['eval']['matched_invariants'])/arms['LCL'][sid]['eval']['total_invariants'] for sid in ids],
                    [len(arms[arm][sid]['eval']['matched_invariants'])/arms[arm][sid]['eval']['total_invariants'] for sid in ids])
    # Latency repeats collapse within scenario; do not inflate n by repetitions.
    latency_ids={}
    for arm in ARMS:
        groups=collections.defaultdict(list)
        for r in lat:
            if r['arm']==arm:groups[r['scenario_id']].append(r)
        complete={sid:rr for sid,rr in groups.items() if {r['rep'] for r in rr}=={0,1,2} and len(rr)==3}
        latency_ids[arm]={sid:mean([r['wall_seconds'] for r in rr]) for sid,rr in complete.items()}
        result['latency'][arm]={'rows':sum(map(len,groups.values())),'scenarios_with_three_repetitions':len(complete),
            'mean_scenario_seconds_three_repeats':mean(list(latency_ids[arm].values())),
            'scenarios_with_nonidentical_plan_hashes':sum(len({x['plan_sha256'] for x in rr})>1 for rr in complete.values())}
    complete_latency=sorted(set.intersection(*(set(v) for v in latency_ids.values())))
    result['latency']['paired_complete_scenarios']=len(complete_latency)
    result['latency']['contrasts_exploratory']={
        'LCL-'+arm:stats([latency_ids['LCL'][sid] for sid in complete_latency],[latency_ids[arm][sid] for sid in complete_latency])
        for arm in ARMS if arm!='LCL'}
    ratings_path=HERE/'semantic_ratings.json'
    if ratings_path.exists():
        ratings=load('semantic_ratings.json');mapping=load('blind_mapping.json')
        slookup={s['scenario_id']:s for s in h};rlookup={(r['scenario_id'],r['arm']):r for r in controls};jlookup={(r['scenario_id'],r['arm'],r['invariant_index']):r for r in judge}
        assert len({r['id'] for r in ratings})==len(ratings),'Duplicate blinded rating IDs'
        assert {r['id'] for r in ratings}==set(mapping),'Every generated blinded plan must receive a rating before final analysis'
        semantic={arm:{} for arm in ARMS};uncertain_count=0;flat=[];disagreements=[];agreement={}
        for r in ratings:
            assert r['id'] in mapping,r['id'];key=mapping[r['id']];sid=key['scenario_id'];arm=key['arm'];s=slookup[sid]
            assert len(r['invariants'])==3
            assert all(x in [0,1,'uncertain'] for x in r['invariants'])
            strict=[int(x==1) for x in r['invariants']];lenient=[int(x in [1,'uncertain']) for x in r['invariants']]
            uncertain_count+=r['invariants'].count('uncertain')
            semantic[arm][sid]={'strict':mean(strict),'lenient':mean(lenient),'all_pass':all(strict),
                'task_fulfillment':r['task_fulfillment'],'unnecessary_refusal':r['unnecessary_refusal'],'strict_bits':strict,'rating_id':r['id']}
            raw=rlookup[sid,arm]
            for i,(inv,decision) in enumerate(zip(s['required_invariants'],strict)):
                q={'scenario_id':sid,'arm':arm,'invariant_index':i,'auditor_pass':decision,
                    'regex_pass':inv in raw['eval']['matched_invariants'],'judge_pass':jlookup.get((sid,arm,i),{}).get('pass'),
                    'rating_id':r['id'],'rating_note':r['note']}
                flat.append(q)
                if q['auditor_pass']!=q['regex_pass'] or (q['judge_pass'] is not None and q['auditor_pass']!=q['judge_pass']):disagreements.append(q)
        ids=sorted(set.intersection(*(set(v) for v in semantic.values())))
        for arm in ARMS:
            arm_flat=[q for q in flat if q['arm']==arm]
            agreement[arm]={'regex_vs_auditor':kappa([(q['auditor_pass'],q['regex_pass']) for q in arm_flat]),
                'judge_vs_auditor':kappa([(q['auditor_pass'],q['judge_pass']) for q in arm_flat if q['judge_pass'] is not None])}
        comparisons={};sensitivity={}
        for arm in ARMS:
            if arm=='LCL':continue
            for metric,target in [('strict',comparisons),('lenient',sensitivity)]:
                target['LCL-'+arm]=stats([semantic['LCL'][sid][metric] for sid in ids],[semantic[arm][sid][metric] for sid in ids],[slookup[sid]['family'] for sid in ids])
        holm(comparisons);holm(sensitivity)
        result['semantic']={'status':'rated','single_auditor':'Codex assistant; no independent human gold standard; artificial identifiers masked, style may reveal condition',
            'rated_plans':len(ratings),'rated_invariant_decisions':len(flat),'uncertain_decisions':uncertain_count,
            'complete_paired_scenarios':len(ids),'confirmatory_contrasts':comparisons,'uncertainty_sensitivity':sensitivity,'arms':{},'agreement':agreement}
        for arm in ARMS:
            rr=[semantic[arm][sid] for sid in ids]
            result['semantic']['arms'][arm]={'n':len(rr),'strict_macro_recall':mean([r['strict'] for r in rr]),
                'lenient_macro_recall':mean([r['lenient'] for r in rr]),'all_invariants_pass':mean([r['all_pass'] for r in rr]),
                'task_fulfillment':dict(collections.Counter(str(r['task_fulfillment']) for r in rr)),
                'unnecessary_refusal':dict(collections.Counter(str(r['unnecessary_refusal']) for r in rr))}
        save('semantic_rows.json',flat);save('semantic_disagreements.json',disagreements)
    ledger=rows('gpu_sessions.jsonl');stages=rows('stage_status.jsonl')
    result['completion']={'replication_rows':len(rep),'replication_expected':400,'controls_rows':len(controls),'controls_expected':700,
        'judge_invariant_checks':len(judge),'judge_expected':600,'latency_rows':len(lat),'latency_expected':300,
        'recorded_gpu_process_wall_seconds':sum(s['process_seconds'] for s in ledger),'ledger':ledger,'stages':stages,
        'failures':rows('failures.jsonl'),'historical_and_new_analysis_are_separate':True}
    save('new_metrics.json',result)
    # Preserve a compact evidence matrix usable without Python.
    claims=load('claims.json')
    with (HERE/'claim_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(claims[0]));w.writeheader();w.writerows(claims)
    print(json.dumps({'completion':{k:v for k,v in result['completion'].items() if k not in ['ledger','stages','failures']},'semantic':result['semantic'].get('rated_plans',0)}))

if __name__=='__main__':main()
