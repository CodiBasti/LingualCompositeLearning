"""Display full masked plans in small, condition-blind scenario batches."""
import argparse
import collections
import json
import pathlib

HERE=pathlib.Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--start',type=int,default=1);p.add_argument('--count',type=int,default=4);args=p.parse_args()
    data=json.loads((HERE/'blinded_plans.json').read_text(encoding='utf-8'))
    groups=collections.defaultdict(list)
    for r in data:groups[r['scenario_id']].append(r)
    ids=[f'AUD-{i:03d}' for i in range(args.start,args.start+args.count)]
    for sid in ids:
        rr=groups.get(sid,[])
        if len(rr)!=5:
            print(f'{sid}: incomplete ({len(rr)}/5), no review batch emitted');continue
        print('\nSCENARIO '+sid+'\nCONTEXT: '+rr[0]['context']+'\nCOMMAND: '+rr[0]['command'])
        for i,criterion in enumerate(rr[0]['rubric'],1):print(f'R{i}: {criterion}')
        for r in sorted(rr,key=lambda r:r['id']):
            print('\nPLAN '+r['id']+'\n'+r['plan']+'\nEND PLAN '+r['id'])

if __name__=='__main__':main()
