"""Post-hoc diagnostic: identical prompts, outputs and token counts, varying time."""
import collections
import hashlib
import json
import pathlib
import statistics
HERE=pathlib.Path(__file__).resolve().parent

def digest(s):return hashlib.sha256(s.encode()).hexdigest()

def main():
    groups=collections.defaultdict(list)
    for s in (HERE/'generation_trace.jsonl').read_text(encoding='utf-8').splitlines():
        r=json.loads(s)
        if r['stage'] not in ['controls','latency','supplement_latency'] or r['max_new_tokens']!=250:continue
        prompt=digest(json.dumps(r['messages'],sort_keys=True,ensure_ascii=False))
        output=digest(r['output'])
        key=(r['scenario_id'],r['arm'],prompt,output,r['input_tokens'],r['output_tokens'])
        groups[key].append(r)
    comparisons=[]
    for (sid,arm,prompt,output,ntin,ntout),rr in groups.items():
        if len(rr)<2:continue
        seconds=[r['seconds'] for r in rr]
        comparisons.append({'scenario_id':sid,'arm':arm,'prompt_sha256':prompt,'output_sha256':output,
                            'input_tokens':ntin,'output_tokens':ntout,'n_calls':len(rr),
                            'min_seconds':min(seconds),'max_seconds':max(seconds),'max_min_ratio':max(seconds)/min(seconds),
                            'calls':[{'stage':r['stage'],'rep':r['rep'],'seconds':r['seconds']} for r in rr]})
    comparisons.sort(key=lambda r:r['max_min_ratio'],reverse=True)
    ratios=[r['max_min_ratio'] for r in comparisons]
    result={'status':'post_hoc_descriptive_timing_diagnostic','registration':'After inspecting600 judge checks and ongoing latency timings; primary tests and ratings unchanged.',
            'definition':'Group exact rendered message payload and output text hashes, equal input/output token counts, same scenario and arm; planner calls only. Same pinned model/settings under V3 adapter.',
            'caveat':'Time variation is observed. This diagnostic does not identify its cause or separate concurrent application load, paging, thermal/clock state, cache/runtime effects and other factors. Reruns may span main/supplement processes. No new independent accuracy observations.',
            'identical_prompt_output_groups_repeated':len(comparisons),
            'median_within_group_max_min_ratio':statistics.median(ratios) if ratios else None,
            'largest_within_group_max_min_ratio':max(ratios) if ratios else None,
            'groups':comparisons}
    (HERE/'runtime_drift.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in ['identical_prompt_output_groups_repeated','median_within_group_max_min_ratio','largest_within_group_max_min_ratio']}))

if __name__=='__main__':main()
