"""Read-only checks of source semantics, citation keys and history attribution."""
import ast
import collections
import hashlib
import json
import pathlib
import re
import subprocess

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def main():
    source=(ROOT/'dev/src/lingual_research/runner_exp003.py').read_text(encoding='utf-8')
    cls=next(x for x in ast.parse(source).body if isinstance(x,ast.ClassDef))
    methods=[x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name in ['classify_composite_concepts','synthesize_composite_contract']]
    ns={'List':list,'Dict':dict,'Any':object}
    exec(compile(ast.Module(body=methods,type_ignores=[]),'<original_pure_methods>','exec'),ns)
    captures=[]
    class Dummy:
        def generate(self,messages,max_new_tokens=250): return self.output
    obj=Dummy();scenario={'context':'A context','user_command':'A command'}
    for output in ['weli fufu','fufu weli','gugi kuku','nonsense','zubu zeze gugi','fufu-weli']:
        obj.output=output;parsed=ns['classify_composite_concepts'](obj,scenario)
        captures.append({'raw':output,'parsed':parsed,'contract':ns['synthesize_composite_contract'](obj,parsed)})
    save('routing_structure_probes.json',{'captures':captures,
        'interpretation':'Tests source parsing/synthesis only. Not an empirical model generalization test.'})
    bib=(ROOT/'dev/papers/neurips_2026/references.bib').read_text(encoding='utf-8')
    keys=set(re.findall(r'@\w+\{([^,]+),',bib));citations={}
    for name in ['PAPER_MANUSCRIPT.md','main.tex']:
        text=(ROOT/'dev/papers/neurips_2026'/name).read_text(encoding='utf-8')
        used={x.strip() for match in re.findall(r'\\cite\w*\{([^}]+)\}',text) for x in match.split(',')}
        citations[name]={'cited_keys':sorted(used),'missing_bib_keys':sorted(used-keys)}
    save('citation_key_check.json',{'bib_keys':sorted(keys),'documents':citations})
    # Historical input language is discoverable in git; no fabricated metadata.
    revs=['aa766fd','8235305','f4802de','58df587'];history={}
    paths=['dev/data/benchmarks/benchmark_v1.json','dev/data/benchmarks/benchmark_v2.json','dev/runs/EXP-001/exp001_results.json','dev/runs/EXP-002/exp002_results.json','dev/runs/EXP-003/exp003_results.json','dev/HYPOTHESES.md','dev/src/lingual_research/evaluator.py']
    for rev in revs:
        history[rev]={}
        for path in paths:
            raw=subprocess.check_output(['git','show',rev+':'+path],cwd=ROOT)
            value={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
            if '/benchmarks/' in path:
                data=json.loads(raw);value.update(n=len(data),first_command=data[0]['user_command'],first_context=data[0]['context'],all_commands=[s['user_command'] for s in data])
            history[rev][path]=value
    save('git_provenance.json',history)
    archive={}
    for exp in ['EXP-002','EXP-003']:
        name=exp.replace('EXP-','exp')+'_results.json'
        first=json.loads(subprocess.check_output(['git','show',f'aa766fd:dev/runs/{exp}/{name}'],cwd=ROOT))
        archived=json.loads((ROOT/f'dev/runs/_archive_german_input/{exp}/{name}').read_text(encoding='utf-8'))
        archive[exp]={'entire_json_identical':first==archived,
            'all_condition_records_identical':all(first[k]==archived.get(k) for k in first if k.startswith('condition_')),
            'different_summary_fields':[k for k in first.get('summary',{}) if first['summary'][k]!=archived.get('summary',{}).get(k)]}
    save('archive_identity.json',{'archived_json_equals_initial_git_json':archive,
        'EXP001_inputs':'Initial git benchmark v1 includes German commands; current v1 is English. EXP001 result JSON stayed byte-identical across the four inspected revisions.',
        'historical_runtime_versions':'No package lock or model revision recorded in tracked run results; historical environment cannot be exactly recovered.',
        'EXP003_zero_walltime_note':'Archive preserves all initial condition records but resets summary total walltime to zero. A fully resumed execute_benchmark() can recalculate walltime with no new calls; that is a code-compatible explanation, not established historical provenance. No inference of deliberate manipulation.'})
    print(json.dumps({'parser_probes':len(captures),'citations':citations,'archive_matches':archive}))

if __name__=='__main__':main()
