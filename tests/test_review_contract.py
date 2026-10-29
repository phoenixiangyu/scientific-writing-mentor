import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review_check',ROOT/'skills/scientific-writing-mentor/scripts/check_review.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def issue(**changes):
    data=dict(id='E01',anchor='Removal increased from 70% to 82%.',location='Results, paragraph 1',kind='statistics',severity='blocking',question='What is the uncertainty?',needed='Provide replicate counts and variability.',status='open')
    data.update(changes)
    return data

class ReviewContractTests(unittest.TestCase):
    def test_clean_draft_can_keep_open_questions_outside_body(self):
        self.assertEqual(module.validate('Removal increased from 70% to 82%.',{'issues':[issue()]}),[])

    def test_finalization_blocks_unresolved_evidence(self):
        errors=module.validate('Removal increased from 70% to 82%.',{'issues':[issue()]},True)
        self.assertTrue(any('unresolved' in e for e in errors))

    def test_resolved_blocker_permits_final_check(self):
        self.assertEqual(module.validate('Removal increased from 70% to 82%.',{'issues':[issue(status='resolved')]},True),[])

    def test_missing_anchor_is_rejected_after_revision(self):
        self.assertTrue(module.validate('The revised draft changed.',{'issues':[issue()]}))

    def test_placeholders_cannot_leak_into_clean_copy(self):
        for text in ['A result [TODO: supply n].','The effect [待核实].','Claim [citation needed].']:
            with self.subTest(text=text):
                self.assertTrue(module.validate(text,{'issues':[]}))

    def test_duplicate_ids_are_rejected(self):
        self.assertTrue(module.validate('Removal increased from 70% to 82%.',{'issues':[issue(),issue()]}))

    def test_invalid_issue_data_is_rejected(self):
        for value in [{},None,{'issues':[None]},{'issues':[issue(severity='minor')]},{'issues':[issue(anchor=3)]}]:
            with self.subTest(value=value):
                self.assertTrue(module.validate('',value))

    def test_an_unproblematic_edit_does_not_require_invented_issues(self):
        self.assertEqual(module.validate('The samples were dried at 60 °C.',{'issues':[]},True),[])

if __name__=='__main__':
    unittest.main()
