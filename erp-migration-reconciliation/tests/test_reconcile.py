import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from reconcile import reconcile
class Tests(unittest.TestCase):
    def test_diff(self):
        summary,rows=reconcile({'1':{'record_id':'1','status':'ok'}},{'1':{'record_id':'1','status':'bad'}})
        self.assertEqual(summary['difference_count'],1)
        self.assertEqual(rows[0]['field'],'status')
if __name__=='__main__': unittest.main()
