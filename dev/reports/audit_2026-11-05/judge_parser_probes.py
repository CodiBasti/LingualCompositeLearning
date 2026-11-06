"""Adversarial parsing checks using the exact original expression, without LLM calls."""
import ast
import json
import pathlib
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def main():
    p=ROOT/'dev/src/lingual_research/audit_judge.py'
    tree=ast.parse(p.read_text(encoding='utf-8'))
    expr=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='is_pass' for t in n.targets))
    expression=compile(ast.Expression(expr),str(p),'eval')
    tests=[('DECISION: PASS\nRATIONALE: The minimum is specified.',True),
           ('DECISION: FAIL\nRATIONALE: The constraint is missing.',False),
           ('DECISION: NOT PASS\nRATIONALE: The constraint is missing.',False),
           ('DECISION: FAIL (not PASS)\nRATIONALE: The constraint is missing.',False),
           ('BYPASS is not a valid verdict\nRATIONALE: No decision provided.',False),
           ('No decision\nRATIONALE: The answer was truncated.',False)]
    rows=[{'response':s,'expected_pass':expected,'parsed_pass':bool(eval(expression,{'response':s}))} for s,expected in tests]
    payload={'source':'dev/src/lingual_research/audit_judge.py:76','expression':ast.unparse(expr),
             'cases':rows,'false_passes':sum(r['parsed_pass'] and not r['expected_pass'] for r in rows),
             'caveat':'Constructed parser examples, not observed LLM error frequencies. Correct-format outputs are handled in these probes. Original judge does not return full raw response; occurrence in historical/new real checks cannot be completely reconstructed.'}
    (HERE/'judge_parser_probes.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'cases':len(rows),'constructed_false_passes':payload['false_passes']}))

if __name__=='__main__':main()
