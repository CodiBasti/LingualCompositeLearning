"""Check condition counts, masking joins and observed alias-parser parity.

No output is corrected or regenerated. If capitalization changes alias parsing,
flag the affected cases as a control limitation rather than hiding the error.
"""
import ast
import collections
import json
import pathlib
import re

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def read(name):return json.loads((HERE/name).read_text(encoding='utf-8'))
def rows(name):
    p=HERE/name
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()] if p.exists() else []

def main():
    tree=ast.parse((ROOT/'dev/src/lingual_research/runner_exp003.py').read_text(encoding='utf-8'))
    cls=next(x for x in tree.body if isinstance(x,ast.ClassDef))
    fn=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='classify_composite_concepts')
    ns={'List':list,'Dict':dict,'Any':object};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<original_parser>','exec'),ns)
    class Dummy:
        def generate(self,*args,**kwargs):return self.raw
    d=Dummy();scenario={'context':'','user_command':''}
    mismatches=[];checked=0
    mappings=read('protocol.json')
    for r in rows('generation_trace.jsonl'):
        if r['stage'] not in ['controls','supplement_controls'] or r['arm'] not in ['natural_labels','renamed_labels'] or r['max_new_tokens']!=20:continue
        reverse={v:k for k,v in mappings[r['arm']].items()}
        raw=r['output'];case_sensitive=raw;case_insensitive=raw
        for alias,canonical in reverse.items():
            case_sensitive=re.sub(r'\b'+re.escape(alias)+r'\b',canonical,case_sensitive)
            case_insensitive=re.sub(r'\b'+re.escape(alias)+r'\b',canonical,case_insensitive,flags=re.I)
        d.raw=case_sensitive;a=ns['classify_composite_concepts'](d,scenario)
        d.raw=case_insensitive;b=ns['classify_composite_concepts'](d,scenario)
        checked+=1
        if a!=b:mismatches.append({'scenario_id':r['scenario_id'],'arm':r['arm'],'raw':raw,'actual_parse':a,'casefolded_parse':b})
    controls=rows('controls.jsonl');counts=collections.Counter((r['scenario_id'],r['arm']) for r in controls)
    result={'observed_alias_routes_checked':checked,'capitalization_changes_parse':mismatches,
        'interpretation':'Case-sensitive reverse aliases are a potential wrapper asymmetry relative to original lowercasing. Only observed mismatches constrain label-effect interpretation; no data are repaired.',
        'duplicate_control_keys':[list(k) for k,v in counts.items() if v>1],
        'generated_condition_counts':dict(collections.Counter(r['arm'] for r in controls)),
        'information_matching':read('information_matching_check.json')}
    (HERE/'control_integrity_check.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'checked':checked,'capitalization_parse_mismatches':len(mismatches),'duplicate_keys':len(result['duplicate_control_keys'])}))

if __name__=='__main__':main()
