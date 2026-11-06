"""Closure verification without altering frozen evidence or original sources."""
import collections
import datetime as dt
import hashlib
import json
import pathlib
import re
from urllib.parse import unquote

HERE=pathlib.Path(__file__).resolve().parent
REPORT=HERE.parent/'review_audit_2026-11-05_FULL_PROJECT.md'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    errors=[];checked_json=0;checked_lines=0
    for p in HERE.rglob('*'):
        if not p.is_file():continue
        try:
            if p.suffix=='.json':load(p);checked_json+=1
            if p.suffix=='.jsonl':
                for n,s in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
                    if s.strip():json.loads(s);checked_lines+=1
        except Exception as exc:errors.append(f'{p.name}: {exc}')
    ratings=load(HERE/'semantic_ratings.json');freeze=load(HERE/'semantic_rating_freeze.json')
    for name,digest in freeze['files'].items():
        if sha(HERE/name)!=digest:errors.append('Changed after rating freeze: '+name)
    ids=[r['id'] for r in ratings];mapping=load(HERE/'blind_mapping.json')
    if len(ids)!=200 or len(ids)!=len(set(ids)) or set(ids)!=set(mapping):errors.append('Rating coverage/uniqueness not200 matched plans')
    claims=load(HERE/'claims.json');uncertainty=load(HERE/'claim_uncertainty.json')
    if not {c['id'] for c in claims}<=set(uncertainty):errors.append('Missing claim uncertainty')
    integrity=load(HERE/'original_integrity_check.json')
    if integrity['changed_originals'] or integrity['missing_originals']:errors.append('Original file integrity violation')
    if not all((HERE/n).exists() for n in ['gpu_completion.json','supplement_completion.json']):errors.append('Unconcluded GPU stages')
    metrics=load(HERE/'new_metrics.json')
    if {k:v for k,v in metrics['semantic'].items() if k!='agreement'}!=load(HERE/'primary_holdout_results.json'):
        errors.append('Frozen primary holdout results changed during remaining stages')
    if metrics['completion']['recorded_gpu_process_wall_seconds']>28800:errors.append('GPU budget exceeded')
    # Relative Markdown destinations in the final report and main guide must exist.
    local_links=0
    for p in [REPORT,HERE/'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):continue
            target=unquote(target.split('#')[0]);local_links+=1
            if not (p.parent/target).exists():errors.append(f'Broken link in{p.name}: {target}')
    result={'checked_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'json_files':checked_json,
            'jsonl_records':checked_lines,'local_report_guide_links':local_links,'rating_plans':len(ratings),
            'original_files_unchanged':not integrity['changed_originals'] and not integrity['missing_originals'],
            'gpu_process_hours':metrics['completion']['recorded_gpu_process_wall_seconds']/3600,'errors':errors}
    (HERE/'final_checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
