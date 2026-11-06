"""Check substantive manuscript quantities directly against historical raw rows."""
import collections
import json
import pathlib

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def main():
    m=json.loads((HERE/'historical_metrics.json').read_text(encoding='utf-8'))
    tokens=json.loads((HERE/'historical_token_audit.json').read_text(encoding='utf-8'))['conditions']
    oldjudge=json.loads((HERE/'historical_judge_provenance.json').read_text(encoding='utf-8'))['active']['report']['condition_matrices']
    raw2=json.loads((ROOT/'dev/runs/EXP-002/exp002_results.json').read_text(encoding='utf-8'))
    raw3=json.loads((ROOT/'dev/runs/EXP-003/exp003_results.json').read_text(encoding='utf-8'))
    keys=['EXP-002/condition_A_naive','EXP-002/condition_B_verbose','EXP-002/condition_C_concept_routed','EXP-003/condition_C_composite']
    checks=[]
    def add(source,quantity,reported,reconstructed,status,meaning):
        checks.append(dict(source=source,quantity=quantity,reported=reported,reconstructed=reconstructed,status=status,meaning=meaning))
    for arm,key in zip('ABCD',keys):
        d=m['active/'+key]
        add('PAPER_MANUSCRIPT.md:204-207; main.tex:107-110',f'{arm}: recall',dict(zip('ABCD',[35,50.25,46.25,47.25]))[arm],100*d['macro_recall'],'reconstructed','Textual regex measure, not executed safety.')
        add('PAPER_MANUSCRIPT.md:204-207; main.tex:107-110',f'{arm}: latency seconds',dict(zip('ABCD',[6.74,10.13,8.54,8.67]))[arm],d['mean_seconds'],'reconstructed_to_reported_rounding','Historical logged per-record elapsed time; historical hardware load not reconstructible.')
    for pair,value in [('B-A',5.846),('C-A',4.753),('D-A',4.882)]:
        d=m['active/comparisons']['overall'][pair]
        add('PAPER_MANUSCRIPT.md:205-207; main.tex:108-110',f'{pair}: paired t',value,d['paired_t'],'mismatch' if pair=='D-A' else 'reconstructed_to_reported_rounding','All three actual t-test p-values remain <0.0001; comparison is versus naive A, not CoT B.')
        add('main.tex:108-110',f'{pair}: two-sided p','<0.0001',d['paired_t_p_two_sided'],'reconstructed','No causal identification of the artificial name from this comparison.')
    domains=['domestic','emergency','precision_lab','clinical_care']
    reported=[[39.2,63.3,62.5,58.3],[43.3,41.7,45,53.3],[28,41,31,30],[32.5,49.2,43.3,47.5]]
    for domain,values in zip(domains,reported):
        computed=[100*m['active/'+key]['domains'][domain]['macro_recall'] for key in keys]
        add('PAPER_MANUSCRIPT.md:219-222; main.tex:122-125',domain+' four recalls A/B/C/D',values,computed,'reconstructed_to_reported_rounding','Domestic D-B=-5, emergency +11.6667, precision -11, clinical -1.6667 percentage points. +11.6 truncates rather than conventionally rounding +11.6667 to one decimal.')
    a,b,c,d=[m['active/'+key] for key in keys]
    add('PAPER_MANUSCRIPT.md:16', 'Composite-naive gain',12.25,100*(d['macro_recall']-a['macro_recall']),'reconstructed','Percentage points, not relative percent.')
    add('main.tex:39','Composite-naive gain',13,100*(d['macro_recall']-a['macro_recall']),'archive_only','Archived German means support +13 points; current English means support +12.25.')
    add('PAPER_MANUSCRIPT.md:227','Emergency relative gain',27.8,100*(d['domains']['emergency']['macro_recall']/b['domains']['emergency']['macro_recall']-1),'rounding_mismatch','Unrounded raw means imply 28%; rounded displayed 53.3/41.7 imply about27.82%. No demonstrated causal elimination of vacillation.')
    add('PAPER_MANUSCRIPT.md:228','Latency reduction %: composite/atomic',[14.4,15.7],[100*(1-d['mean_seconds']/b['mean_seconds']),100*(1-c['mean_seconds']/b['mean_seconds'])],'approximately_reconstructed','Raw data give about14.37 and15.68%; caps differ.')
    add('PAPER_MANUSCRIPT.md:228','Seconds saved versus CoT','>1.45',[b['mean_seconds']-d['mean_seconds'],b['mean_seconds']-c['mean_seconds']],'reconstructed','Recorded mean savings, with unequal output caps.')
    add('PAPER_MANUSCRIPT.md:59; main.tex:50','CoT latency increase versus naive %','30-50',100*(b['mean_seconds']/a['mean_seconds']-1),'approximately_reconstructed','About50.32% in this logged run, just above stated range; not an external general law.')
    token_increase=100*(tokens['EXP-002/condition_B_verbose']['mean_retokenized_output_tokens']/tokens['EXP-002/condition_A_naive']['mean_retokenized_output_tokens']-1)
    add('PAPER_MANUSCRIPT.md:59; main.tex:50','CoT generated-token increase %','200-300',token_increase,'mismatch','Exact retokenization artifact is historical_token_audit.json; ~299.89 versus199.45 tokens, not200-300% increase.')
    add('PAPER_MANUSCRIPT.md:36,58; main.tex:49','Failure percentage',66.5,100*(1-a['macro_recall']),'archive_only_and_construct_mismatch','One minus archived naive recall gives66.5%; current gives65%. Neither is a physical catastrophic failure rate or fraction of whole tasks failing.')
    add('PAPER_MANUSCRIPT.md:70; main.tex:91-94','Domain scenario counts',[30,30,25,15],[a['domains'][x]['n'] for x in ['domestic','clinical_care','precision_lab','emergency']],'reconstructed','100 independent scenario IDs evaluated in each of four arms; independence beyond shared authored families not established.')
    add('PAPER_MANUSCRIPT.md:16,186; main.tex:39,98','Inference runs',400,{'scenario_condition_records':400,'generation_calls_required_by_code':600,'distinct_scenarios':100},'unit_ambiguity','Two stages in each concept arm. Scenario-condition records are not independent tasks or equal to generation calls.')
    add('PAPER_MANUSCRIPT.md:71-72','Atomic/composite routing old figures',[44,68],[100*c['routing_membership'],100*d['routing_membership']],'archive_only','Current values47 and72. Composite membership and atomic exact match are different scoring rules.')
    add('PAPER_MANUSCRIPT.md:254; main.tex:131','Precision composite label coverage',88,100*d['domains']['precision_lab']['routing_membership'],'reconstructed','Coverage of one expected label in up to2 predictions; not full-set routing accuracy.')
    atoms=['fufu','weli','zubu','zeze','gugi','kuku']
    matrix=[[0]*6 for _ in atoms]
    benchmark={s['scenario_id']:s for s in json.loads((ROOT/'dev/data/benchmarks/benchmark_v2.json').read_text(encoding='utf-8'))}
    for r in raw2['condition_C_concept_routed']:
        i=atoms.index(benchmark[r['scenario_id']]['expected_concept']);j=atoms.index(r['activated_concept']);matrix[i][j]+=1
    displayed=[[10,1,0,0,9,1],[10,24,0,0,8,1],[6,1,3,0,1,0],[5,1,0,0,0,0],[3,2,0,0,3,0],[0,0,0,0,4,7]]
    add('PAPER_MANUSCRIPT.md:243-250','6x6 atomic confusion matrix',displayed,matrix,'reconstructed' if matrix==displayed else 'mismatch','Counts support confusion description, not a demonstrated causal dimensionality mechanism.')
    add('PAPER_MANUSCRIPT.md:288','fufu-weli activation count',84,m['active/comparisons']['composite_pair_counts']['fufu-weli'],'archive_only','Current85, archived84; majority pairing alone does not establish physical necessity.')
    judge_counts=[[q['both_pass']+q['eval_pass_judge_fail'],q['eval_pass_judge_fail']] for q in oldjudge.values()]
    add('PAPER_MANUSCRIPT.md:268-270','Judge regex passes/rejections A/B/C',[[12,5],[14,10],[14,6]],judge_counts,'counts_reconstructed_condition_misattributed','Historical provenance independently checked in historical_judge_provenance.json: C is atomic, not composite; first5 domestic cases, same checkpoint.')
    add('PAPER_MANUSCRIPT.md:186; main.tex:98','Historical VRAM allocation GB',27.65,None,'not_reconstructible','Original allocation telemetry absent. Current hardware/model load does not prove historical exact allocation.')
    add('PAPER_MANUSCRIPT.md:119-128; main.tex:66-78','1/1.5m, <3N, 1.5N/s,0dB', 'chosen policy definitions',None,'definitions_not_empirical_findings','Not measurements or validated universal safety thresholds; conflicting1.0N/s specification elsewhere. No physical force/sound samples.')
    allplans=[]
    for path in (ROOT/'dev/runs').rglob('*results.json'):
        data=json.loads(path.read_text(encoding='utf-8'))
        for v in data.values():
            if isinstance(v,list):allplans.extend(x.get('plan','') for x in v if isinstance(x,dict))
    for text in ['Axiom 1: I must maintain a wide standoff and crawl speed near the infant','Step 1: Move directly across the room. Step 2: Grasp the cup.']:
        add('PAPER_MANUSCRIPT.md:275-279','Purported quotation',text,sum(text in p for p in allplans),'not_located_in_preserved_plans','No matching full phrase in preserved result plans. May be illustrative; manuscript must label as such or provide exact source. Not proof that no similar behavior occurs.')
    (HERE/'manuscript_numbers.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    lines=['# Abgleich wesentlicher Manuskriptzahlen','', 'Quellstand wie im Auditmanifest. Prozentangaben unterscheiden relative Änderung und Prozentpunkte. Diese Prüfung ist retrospektiv; technische Hyperparameter und definierte Grenzwerte sind keine gemessenen Ergebnisse.','', '| Fundstelle | Größe | Behauptet | Rekonstruiert | Befund |','|---|---|---|---|---|']
    for q in checks:
        lines.append('| '+' | '.join(str(q[k]).replace('|','/') for k in ['source','quantity','reported','reconstructed','status'])+' |')
    lines+=['','Vollständige Interpretationsgrenzen pro Zeile: [manuscript_numbers.json](manuscript_numbers.json). Tabellenwerte sind aus Einzelzeilen rekonstruiert; Rohtexte wurden für die beiden wörtlich markierten Beispiele durchsucht. Fehlendes wörtliches Zitat widerlegt nicht die Möglichkeit ähnlicher Fehler.']
    (HERE/'manuscript_numbers.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'checks':len(checks),'statuses':dict(collections.Counter(x['status'] for x in checks))}))

if __name__=='__main__':main()
