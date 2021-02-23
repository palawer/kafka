from datetime import datetime
from db.dao import DataObject


class Snapshot(DataObject):
    """ 
    Snapshot is the abstraction for each pull 
    that has been done to a concrete domain
    """
    id        = type('')
    domain_id = type('')
    pulled_at = type(datetime)
    html      = type('')