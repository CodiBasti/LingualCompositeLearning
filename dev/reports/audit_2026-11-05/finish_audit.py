"""Recompute and verify the completed audit; never edits original project files."""
import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys
import time
from monitor_status import rows,process,K

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--wait',action='store_true');args=parser.parse_args()
    if args.wait:
        started=time.monotonic()
        while True:
            concluded=all((HERE/n).exists() for n in ['gpu_completion.json','supplement_completion.json'])
            active=False
            for r in rows('gpu_processes.jsonl'):
                h,ticks,alive=process(r['pid'])
                if h:K.CloseHandle(h)
                active=active or (alive and ticks==r['creation_ticks'])
            if concluded and not active:break
            if time.monotonic()-started>28800:raise TimeoutError('Model-stage completion not available after8h CPU waiting')
            time.sleep(10)
    if not all((HERE/n).exists() for n in ['gpu_completion.json','supplement_completion.json','semantic_rating_freeze.json']):
        raise RuntimeError('Model stages and rating freeze must be complete')
    ledger=rows('gpu_sessions.jsonl')
    for r in rows('gpu_processes.jsonl'):
        h,ticks,alive=process(r['pid'])
        if h:K.CloseHandle(h)
        if alive and ticks==r['creation_ticks']:raise RuntimeError('Registered model process still active')
    commands=[['analyze.py','verify'],['summarize_new.py'],['family_sensitivity.py'],
              ['control_integrity_check.py'],['routing_diagnostics.py'],['manuscript_numbers.py'],['judge_parser_probes.py'],['runtime_drift.py']]
    validations=[]
    for args in commands:
        r=subprocess.run([sys.executable,'-X','utf8',str(HERE/args[0]),*args[1:]],cwd=ROOT,text=True,encoding='utf-8',capture_output=True)
        validations.append({'command':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
        if r.returncode:raise RuntimeError('Closure command failed: '+str(validations[-1]))
    r=subprocess.run([sys.executable,'-X','utf8','-m','unittest','discover','-s',str(HERE),'-p','test_*.py','-v'],cwd=ROOT,text=True,encoding='utf-8',capture_output=True)
    validations.append({'command':'unittest test_*.py','exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    (HERE/'validation_results.json').write_text(json.dumps(validations,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    if r.returncode:raise RuntimeError('Audit method tests failed')
    r=subprocess.run([sys.executable,'-X','utf8',str(HERE/'build_report.py')],cwd=ROOT,text=True,encoding='utf-8',capture_output=True)
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    print(r.stdout.strip())
    guide=HERE/'README.md';s=guide.read_text(encoding='utf-8')
    old='**Arbeitsstatus:** Durchführung läuft. Maßgeblich für den späteren Abschluss sind der Abschlussbericht und `new_metrics.json`; Zwischenstände enthalten ausdrücklich noch keine vollständige neue Kontrollstudie.'
    new='**Arbeitsstatus:** Abgeschlossen mit den im [Abschlussbericht](../review_audit_2026-11-05_FULL_PROJECT.md) und [new_metrics.json](new_metrics.json) ausgewiesenen Replikations- und Budgetgrenzen. Alle40 neuen Szenarien sind in allen fünf Bedingungen vorhanden und inhaltlich bewertet; nicht abgeschlossene ursprüngliche Vergleichsblöcke werden ausdrücklich ausgewiesen.'
    s=s.replace(old,new)
    if '**Arbeitsstatus:** Durchführung läuft' in s:raise RuntimeError('Status guide replacement did not apply')
    guide.write_text(s,encoding='utf-8')
    p=HERE/'progress.json';progress=json.loads(p.read_text(encoding='utf-8'))
    progress.update(status='complete_with_documented_limits',updated_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                    active_sessions={},active_main_pid=None,final_report='dev/reports/review_audit_2026-11-05_FULL_PROJECT.md')
    p.write_text(json.dumps(progress,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    r=subprocess.run([sys.executable,'-X','utf8',str(HERE/'final_checks.py')],cwd=ROOT,text=True,encoding='utf-8',capture_output=True)
    print(r.stdout.strip())
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)

if __name__=='__main__':main()
