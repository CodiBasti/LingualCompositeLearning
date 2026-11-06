"""Enforce the eight-hour cap on registered audit processes only (Windows).

PID plus exact process creation time prevents acting on a reused/foreign PID.
Waiting CPU processes are not charged until their model-loading phase begins.
"""
import argparse
import ctypes as c
from ctypes import wintypes as w
import datetime as dt
import json
import os
import pathlib
import time

HERE=pathlib.Path(__file__).resolve().parent
K=c.WinDLL('kernel32',use_last_error=True)
K.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];K.OpenProcess.restype=w.HANDLE
K.GetProcessTimes.argtypes=[w.HANDLE,c.POINTER(w.FILETIME),c.POINTER(w.FILETIME),c.POINTER(w.FILETIME),c.POINTER(w.FILETIME)];K.GetProcessTimes.restype=w.BOOL
K.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)];K.GetExitCodeProcess.restype=w.BOOL
K.TerminateProcess.argtypes=[w.HANDLE,w.UINT];K.TerminateProcess.restype=w.BOOL
K.CloseHandle.argtypes=[w.HANDLE]

def rows(name):
    p=HERE/name
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()] if p.exists() else []
def append(name,value):
    with (HERE/name).open('a',encoding='utf-8') as f:f.write(json.dumps(value)+'\n')
def write(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def process(pid):
    h=K.OpenProcess(0x1000|0x1,False,pid)
    if not h:return None,None,None
    created,exited,kernel,user=w.FILETIME(),w.FILETIME(),w.FILETIME(),w.FILETIME()
    code=w.DWORD()
    if not K.GetProcessTimes(h,c.byref(created),c.byref(exited),c.byref(kernel),c.byref(user)) or not K.GetExitCodeProcess(h,c.byref(code)):
        K.CloseHandle(h);return None,None,None
    ticks=(created.dwHighDateTime<<32)|created.dwLowDateTime
    return h,ticks,code.value==259

def register(role,index,pid=None,expected_start=None):
    pid=pid or os.getpid();h,ticks,alive=process(pid)
    if h:K.CloseHandle(h)
    if not alive:raise RuntimeError('Audit process is not active')
    created=dt.datetime.fromtimestamp(ticks/1e7-11644473600,dt.timezone.utc)
    started=dt.datetime.now(dt.timezone.utc) if expected_start is None else dt.datetime.fromisoformat(expected_start)
    if expected_start is not None and abs((created-started).total_seconds())>5:
        raise RuntimeError('PID creation time does not match recorded audit start')
    record={'pid':pid,'creation_ticks':ticks,'role':role,'ledger_index':index,'gpu_started_utc':started.isoformat()}
    append('gpu_processes.jsonl',record)
    return record

def monitor():
    while True:
        ledger=rows('gpu_sessions.jsonl');closed=sum(r['process_seconds'] for r in ledger)
        for r in rows('gpu_processes.jsonl'):
            if len(ledger)>r['ledger_index']:continue
            h,ticks,alive=process(r['pid'])
            if not h:continue
            try:
                if ticks!=r['creation_ticks']:raise RuntimeError('Audit PID was reused; refusing to terminate')
                elapsed=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(r['gpu_started_utc'])).total_seconds()
                if alive and closed+elapsed>=28770:
                    if not K.TerminateProcess(h,124):raise OSError(c.get_last_error(),'Cannot stop registered audit process')
                    append('gpu_sessions.jsonl',{'process_seconds':elapsed,'model_loaded':True,'role':r['role'],
                        'pid':r['pid'],'watchdog_budget_stop':True,'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
                    append('failures.jsonl',{'type':'BudgetStop','stage':r['role'],'message':'Known audit PID stopped conservatively 30s before global eight-hour process-wall cap. Incomplete scenario blocks excluded.'})
                    output='gpu_completion.json' if r['role']=='main' else 'supplement_completion.json'
                    write(output,{'status':'budget_stopped','global_gpu_process_seconds':closed+elapsed})
                    print('Registered audit process stopped at global GPU cap',flush=True)
            finally:K.CloseHandle(h)
        if (HERE/'supplement_completion.json').exists():
            print('Supplement concluded; watchdog exits.',flush=True);return
        time.sleep(2)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--register-main',type=int);p.add_argument('--expected-start');args=p.parse_args()
    if args.register_main:print(json.dumps(register('main',2,args.register_main,args.expected_start)))
    else:monitor()
