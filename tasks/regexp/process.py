import requests
import os
import logging
import re
import json
from db import Domain
from db import DomainCheck
from db import Snapshot
from db import SnapshotCheckData
from datetime import datetime

def run(*args,snapshot_id='', **kwargs):
    """Regexp execution, all DomainCheck will be checked 
    against current snapshot
    
    Keyword arguments:
    snapshot_id  -- domain_id that should be retrieved
    """
    snapshot  = Snapshot.get_by_filters(id = snapshot_id)
    if snapshot:
        snapshot=snapshot[0]
        for scd in DomainCheck.get_by_filters(domain_id = snapshot.domain_id):
            regexp      = scd.regexp
            check_value = None
            try:
                check_value = re.findall(scd.regexp,snapshot.html)
            except:
                #bad things can happen with users' input
                #if there's a failure lets log it without breaking DomainCheck's loop 
                logging.exception(f"Errow evaluating regex {regexp} against snapshot_id {snapshot_id}.CONTINUE")
                continue
            
            scd = SnapshotCheckData(
                snapshot_id    = snapshot.id,
                domain_id      = snapshot.domain_id,
                check_id       = scd.id,
                check_value    = None,
                run_at         = datetime.utcnow()
            )
            if check_value:
                check_value = json.dumps(check_value)
                logging.info(f"MATCHES {regexp} against snapshot_id {snapshot_id} -> {check_value}")
                scd.check_value=check_value
            scd.save()
        

