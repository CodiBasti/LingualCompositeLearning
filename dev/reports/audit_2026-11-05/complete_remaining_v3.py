"""Use remaining global budget after the original per-stage soft allocations.

Decision is based on missing IDs and elapsed time only, never on scores.
Can wait without loading a model until the main GPU process has closed its ledger.
"""
import argparse
import datetime as dt
import json
import pathlib
import shutil
import time
import traceback
import gpu_audit as g

HERE=pathlib.Path(__file__).resolve().parent

def wait_main():
    start=time.monotonic()
    while True:
        try:
            if (HERE/'gpu_completion.json').exists() and len(g.rows('gpu_sessions.jsonl'))>=3:return
        except (ValueError,OSError):pass
        if time.monotonic()-start>28800:raise TimeoutError('Main audit did not finish within eight hours of waiting')
        time.sleep(10)

def supplement_controls(engine,c,protocol,templates):
    done={(x['scenario_id'],x['arm']) for x in g.rows('controls.jsonl')}
    old=json.loads((g.ROOT/'dev/data/benchmarks/benchmark_v2.json').read_text(encoding='utf-8'))
    tasks=g.balanced(g.read('holdout.json'))+g.balanced(old)
    for i,s in enumerate(tasks):
        missing=[arm for arm in g.ARMS[i%5:]+g.ARMS[:i%5] if (s['scenario_id'],arm) not in done]
        if not missing:continue
        if not engine.allowed(300):return
        block=[]
        for arm in missing:
            engine.begin('supplement_controls',s['scenario_id'],arm)
            start=time.perf_counter();r=g.fair_plan(engine,c,s,arm,templates,protocol)
            block.append({**r,'arm':arm,'domain':s['domain'],'dataset':'holdout' if s['scenario_id'].startswith('AUD') else 'VHC100',
                'wall_seconds':time.perf_counter()-start,'costs':engine.costs()})
        for r in block:g.append('controls.jsonl',r)
        print(f'supplement controls {s["scenario_id"]}, global {engine.elapsed()/3600:.3f}h',flush=True)

def supplement_replication(engine,a,c):
    done={(x['experiment'],x['scenario_id'],x['arm']) for x in g.rows('replication.jsonl')}
    tasks=g.balanced(json.loads((g.ROOT/'dev/data/benchmarks/benchmark_v2.json').read_text(encoding='utf-8')))
    funcs=[('EXP002','A',a.run_condition_a_naive),('EXP002','B',a.run_condition_b_verbose_cot),('EXP002','C',a.run_condition_c_concept),('EXP003','D',c.run_scenario)]
    for s in tasks:
        missing=[(exp,arm,fn) for exp,arm,fn in funcs if (exp,s['scenario_id'],arm) not in done]
        if not missing:continue
        if not engine.allowed(240):return
        block=[]
        for exp,arm,fn in missing:
            engine.begin('supplement_replication',s['scenario_id'],arm)
            start=time.perf_counter();r=fn(s)
            block.append({'experiment':exp,'arm':arm,'domain':s['domain'],**r,'wall_seconds':time.perf_counter()-start,'costs':engine.costs()})
        for r in block:g.append('replication.jsonl',r)
        print(f'supplement replication {s["scenario_id"]}, global {engine.elapsed()/3600:.3f}h',flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--wait',action='store_true');args=parser.parse_args()
    if args.wait:wait_main()
    # No model load if all work already exists or conservative remaining budget
    # is too small for a complete scenario block plus loading/warm-up.
    counts={name:len(g.rows(name+'.jsonl')) for name in ['controls','judge','latency','replication']}
    spent=sum(x['process_seconds'] for x in g.rows('gpu_sessions.jsonl'))
    if counts=={'controls':700,'judge':600,'latency':300,'replication':400} or spent+360>=28800:
        g.write('supplement_completion.json',{'status':'all_complete' if counts['replication']==400 and counts['controls']==700 and counts['judge']==600 and counts['latency']==300 else 'insufficient_budget_for_block',
            'counts':counts,'recorded_seconds':spent});return
    frozen=g.read(g.FREEZE_NAME)
    for path,h in frozen['files'].items():
        if g.digest(g.ROOT/path)!=h:raise RuntimeError('Frozen execution source changed: '+path)
    for name,h in g.read('supplement_freeze_v3.json')['files'].items():
        if g.digest(HERE/name)!=h:raise RuntimeError('Supplement source changed: '+name)
    if (HERE/'environment.json').exists():shutil.copyfile(HERE/'environment.json',HERE/'environment_before_supplement.json')
    from gpu_watchdog import register
    register('supplement',3)
    start=time.monotonic();engine=None
    try:
        engine=g.Engine();a,c,j=g.proxies(engine)
        engine.begin('supplement_calibration','warmup','warmup')
        engine.generate([{'role':'user','content':'Return the single word ready.'}],max_new_tokens=8)
        # This priority is frozen before new holdout inference or inspection.
        supplement_controls(engine,c,g.read('protocol.json'),frozen['templates'])
        if engine.allowed(90):g.judge(engine,j)
        if engine.allowed(300):g.latency(engine,c,g.read('protocol.json'),frozen['templates'])
        if engine.allowed(240):supplement_replication(engine,a,c)
        g.write('supplement_completion.json',{'status':'finished','global_gpu_process_seconds':engine.elapsed(),
            'counts':{name:len(g.rows(name+'.jsonl')) for name in ['controls','judge','latency','replication']},
            'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    except Exception as exc:
        g.append('failures.jsonl',{'stage':'supplement','type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()})
        traceback.print_exc();raise
    finally:
        g.append('gpu_sessions.jsonl',{'process_seconds':time.monotonic()-start,'model_loaded':engine is not None,
            'role':'supplement','timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat()})

if __name__=='__main__':main()
