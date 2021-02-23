"""
This is the "test" module.

The example module supplies all functional tests that could be run at once typing

python test.py
"""

import unittest
import os
import sys
import logging
import json
from datetime import datetime
from db import delete_tables
from db import create_tables
from db import DataObject
from db import Domain
from db import DomainCheck
from db import Snapshot
from db import SnapshotCheckData
from tasks.collector.process import run as run_collector
from tasks.regexp.process    import run as run_regexp



sys.path.append(
    os.path.dirname(os.path.realpath(__file__))
)
basename,ext = os.path.splitext(
    os.path.basename(__file__)
)
logging.basicConfig(
    format='%(asctime)s: %(pathname)s:%(lineno)d  [%(levelname)s] -> %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/tests.log"),
    ]
)
logging.getLogger('kafka').setLevel(logging.ERROR) #hide kafka traces

domains = {
    "helsinkitimes" : "https://www.helsinkitimes.fi/",
    "berlin"        : "https://www.berlin.de/en/news/",
    "9news"         : "https://www.9news.com.au/sydney",
    "fail!"         : "fail://fail.com",
}

class TestAiven(unittest.TestCase):
    """Container class for all unit tests"""
    
    def test_00_create_db(self):
        """create-drop tables.test"""
        try:
            delete_tables()
        except:
            pass #first execution
        
        table_names = create_tables()
        sql = []
        sql.append("SELECT  table_schema, table_name")
        sql.append("FROM information_schema.tables")
        sql.append("WHERE (table_schema = 'public')")
        sql.append("ORDER BY table_schema, table_name")
        connection = DataObject.db_connect()
        with connection.cursor() as cursor:
            cursor.execute(" ".join(sql))
            list_tables = cursor.fetchall()
            for _schema,table_name in list_tables:
                table_names.remove(table_name)
        
        self.assertEqual(table_names, [])
    
    
    def test_01_insert_init_data(self):
        """sample domain insertion test"""
        _domains = dict(domains)
        for name,url in _domains.items():
            d = Domain(
                domain = name,
                url    = url
            )
            d.save()
        
        for d in Domain.get_by_filters():
            _domains.pop(d.domain,None)
        self.assertEqual(_domains, {})
    
    
    def test_02_collector(self):
        """collector process test"""
        done_snapshots = Snapshot.count_by_filters()
        for d in Domain.get_by_filters():
            ok = run_collector(
                domain_id = d.id
            )
            if ok:
                done_snapshots += 1
        total_snapshots = Snapshot.count_by_filters()
        self.assertEqual(done_snapshots, total_snapshots)
    
    
    def test_03_regexp(self):
        """regexp process test"""
        d = Domain(
            domain = 'dummy',
            url    = 'dummy'
        )
        d.save()
        s = Snapshot(
            domain_id = d.id,
            pulled_at = datetime.utcnow(),
            html      = "find me with a regexp!!",
        )
        s.save()
        dc = DomainCheck(
            domain_id   = d.id,
            name        = "dummy_check",
            regexp      = "find (me|you)"
        )
        dc.save()
        run_regexp(
            snapshot_id = s.id
        )
        scd = SnapshotCheckData.get_by_filters(check_id=dc.id)[0]
        self.assertEqual(json.loads(scd.check_value) , ["me"])


if __name__ == '__main__':
    unittest.main()

