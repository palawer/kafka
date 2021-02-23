import os
import logging
from db.dao      import DataObject
from db.domain   import Domain
from db.domain_check   import DomainCheck
from db.snapshot import Snapshot
from db.snapshot_checkdata import SnapshotCheckData
from db.snapshot_metadata import SnapshotMetadata


table_name__class = [
    ["domain"           , Domain],
    ["domaincheck"      , DomainCheck],
    ["snapshot"         , Snapshot],
    ["snapshotcheckdata", SnapshotCheckData],
    ["snapshotmetadata" , SnapshotMetadata],
]

def delete_tables():
    con = DataObject.db_connect()
    with con.cursor() as cursor:
        for table_name,_class in table_name__class:
            sql = _class.get_delete_statement()
            cursor.execute(sql)
            logging.info(sql)
            con.commit()
    

def create_tables():
    con = DataObject.db_connect()
    created_tables = []
    with con.cursor() as cursor:
        for table_name,_class in table_name__class:
            sql = _class.get_create_statement()
            cursor.execute(sql)
            logging.info(sql)
            con.commit()
            created_tables.append(table_name)
    
    return created_tables
