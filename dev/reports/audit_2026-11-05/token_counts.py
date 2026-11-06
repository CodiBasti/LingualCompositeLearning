"""Tokenize saved historical outputs with the pinned local tokenizer, CPU only."""
import os
os.environ['HF_HUB_OFFLINE']='1'
import collections
import json
import pathlib
from transformers import AutoTokenizer

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
snapshot=pathlib.Path(os.environ['HF_HOME'])/'hub/models--Qwen--Qwen2.5-14B-Instruct/snapshots/cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8'
tok=AutoTokenizer.from_pretrained(str(snapshot),local_files_only=True)
out={'tokenizer_snapshot':snapshot.name,'caveat':'Retokenized saved decoded/stripped outputs. Historical generated token IDs and EOS were not saved. Near-cap count is evidence consistent with truncation, not a definitive generation termination log.',
    'label_tokens':{x:tok.encode(x,add_special_tokens=False) for x in ['fufu','weli','zubu','zeze','gugi','kuku','fufu-weli','clearance','compliance','nava','pemi']},'conditions':{}}
for exp in ['EXP-001','EXP-002','EXP-003']:
    data=json.loads((ROOT/'dev/runs'/exp/(exp.replace('EXP-','exp')+'_results.json')).read_text(encoding='utf-8'))
    for arm,items in data.items():
        if not arm.startswith('condition_') or not isinstance(items,list):continue
        counts=[len(tok.encode(r['plan'],add_special_tokens=False)) for r in items]
        cap=300 if exp=='EXP-002' and arm=='condition_B_verbose' else 250
        out['conditions'][exp+'/'+arm]={'n':len(counts),'mean_retokenized_output_tokens':sum(counts)/len(counts),
            'configured_output_cap_in_current_source':cap,'at_or_above_cap_minus_one':sum(c>=cap-1 for c in counts),
            'count_distribution':dict(collections.Counter(counts)),
            'rows':[{'scenario_id':r['scenario_id'],'tokens':c,'ends_with':r['plan'][-90:]} for r,c in zip(items,counts)]}
(HERE/'historical_token_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:{x:v[x] for x in ['n','mean_retokenized_output_tokens','at_or_above_cap_minus_one']} for k,v in out['conditions'].items()}))
