import requests
import os
import logging
from db import Domain
from db import Snapshot
from db import SnapshotMetadata
from datetime import datetime
import os
import logging

def run(*args,domain_id = '', **kwargs):
    """Collector execution, get domains HTML running an HTTP GET request
    
    Keyword arguments:
    domain_id  -- domain_id that should be retrieved
    """
    logging.info("start collector run")
    domain    = Domain.get_by_filters(id = domain_id)
    if domain:
        domain=domain[0]
        headers = {
            #custom headers
        }
        proxies = {
            #custom proxies
        }
        params = {
            #custom query string
        }
        res = None
        
        try:
            res = requests.get(
                domain.url, 
                headers = headers,
                proxies = proxies,
                data    = params,
                timeout = 10 #avoid hangs! -> https://requests.readthedocs.io/en/master/user/advanced/#timeouts
            )
        except:
            #bad things can happen with users' input and i/o operations
            #here a good error callback function will be super!
            logging.exception(f"Error fething {domain.url}")
        snapshot_id = None
        if res:
            s = Snapshot(
                domain_id = domain_id,
                pulled_at = datetime.utcnow(),
                html      = res.text
            )
            s.save()
            
            domain.last_snapshot_at=datetime.utcnow()
            domain.save()
            
            snapshot_id = s.id
            SnapshotMetadata(
                snapshot_id    = s.id,
                domain_id      = domain_id,
                request_time   = res.elapsed.total_seconds(),
                request_status = res.status_code,
            ).save()
        return snapshot_id

