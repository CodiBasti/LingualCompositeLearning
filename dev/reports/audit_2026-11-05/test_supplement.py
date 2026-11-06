"""Budget admission and complete-block resumption checks without loading a model."""
import unittest
from unittest.mock import patch
import complete_remaining as s

class BudgetBlocks(unittest.TestCase):
    def test_insufficient_budget_does_not_start_latency_block(self):
        class E:
            def allowed(self,margin):return False
        with patch.object(s.g,'rows',return_value=[]),patch.object(s.g,'append') as appended,patch.object(s.g,'fair_plan') as generate:
            s.complete_latency_blocks(E(),None,{}, {})
            generate.assert_not_called()
            self.assertFalse(any(x.args[0]=='latency.jsonl' for x in appended.call_args_list))

    def test_resume_finishes_third_repeat_before_another_scenario(self):
        task=s.g.balanced(s.g.read('holdout.json'))[0]
        old=[{'scenario_id':task['scenario_id'],'arm':a,'rep':rep,'wall_seconds':1} for rep in [0,1] for a in s.g.ARMS]
        class E:
            admissions=0
            def allowed(self,margin):self.admissions+=1;return self.admissions==1
            def begin(self,*args):pass
            def costs(self):return {}
            def elapsed(self):return 1
        with patch.object(s.g,'rows',side_effect=lambda name:old if name=='latency.jsonl' else []),patch.object(s.g,'append') as appended,patch.object(s.g,'fair_plan',return_value={'plan':'one plan'}):
            s.complete_latency_blocks(E(),None,{}, {})
            new=[x.args[1] for x in appended.call_args_list if x.args[0]=='latency.jsonl']
        self.assertEqual([r['arm'] for r in new],['LCL','natural_labels','renamed_labels','cot_equal','structured_direct'])
        self.assertEqual({r['scenario_id'] for r in new},{task['scenario_id']})
        self.assertEqual({r['rep'] for r in new},{2})
        self.assertEqual(len({(r['arm'],r['rep']) for r in old+new}),15)

if __name__=='__main__':unittest.main(verbosity=2)
