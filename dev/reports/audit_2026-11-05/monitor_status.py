"""Read-only process/data progress, with conservative active wall-time accounting."""
import datetime as dt
import json
from gpu_watchdog import HERE,rows,process,K

def main():
    ledger=rows('gpu_sessions.jsonl');closed=sum(x['process_seconds'] for x in ledger)
    active=[];seconds=closed
    for r in rows('gpu_processes.jsonl'):
        if len(ledger)>r['ledger_index']:continue
        h,ticks,alive=process(r['pid'])
        if h:K.CloseHandle(h)
        if alive and ticks==r['creation_ticks']:
            elapsed=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(r['gpu_started_utc'])).total_seconds()
            seconds+=elapsed;active.append({'role':r['role'],'pid':r['pid']})
    counts={name:len(rows(name+'.jsonl')) for name in ['replication','controls','judge','latency']}
    result={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'counts':counts,
            'conservative_gpu_process_hours_including_active':round(seconds/3600,3),'active_model_processes':active,
            'main_concluded':(HERE/'gpu_completion.json').exists(),
            'supplement_concluded':(HERE/'supplement_completion.json').exists()}
    print(json.dumps(result))

if __name__=='__main__':main()
