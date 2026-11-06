"""Hash the closed audit artifacts and final report, or verify that release."""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REPORT=HERE.parent/'review_audit_2026-11-05_FULL_PROJECT.md'
MANIFEST=HERE/'release_manifest.json'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files():
    return sorted([p for p in HERE.rglob('*') if p.is_file() and p!=MANIFEST and '__pycache__' not in p.parts and p.suffix!='.pyc']+[REPORT])

def main():
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');args=p.parse_args()
    if args.verify:
        m=json.loads(MANIFEST.read_text(encoding='utf-8'));errors=[]
        for r in m['files']:
            path=ROOT/r['path']
            if not path.is_file() or digest(path)!=r['sha256']:errors.append(r['path'])
        expected={r['path'] for r in m['files']};actual={p.relative_to(ROOT).as_posix() for p in files()}
        errors+=sorted(actual^expected)
        print(json.dumps({'hashed_artifacts':len(m['files']),'changed_missing_or_unlisted':errors}))
        if errors:raise SystemExit(1)
        return
    if MANIFEST.exists():raise RuntimeError('Existing release manifest must not be silently overwritten')
    final=json.loads((HERE/'final_checks.json').read_text(encoding='utf-8'))
    if final['errors']:raise RuntimeError('Closure checks have errors')
    m={'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
       'source_git_head':json.loads((HERE/'source_manifest.json').read_text(encoding='utf-8'))['git_head'],
       'scope':'Final report and all delivered audit files; excludes this manifest and Python bytecode caches. Original project hashes separately in source_manifest.json.',
       'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files()]}
    MANIFEST.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'hashed_artifacts':len(m['files']),'manifest':str(MANIFEST)}))

if __name__=='__main__':main()
