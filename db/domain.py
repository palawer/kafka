from datetime import datetime
from db.dao import DataObject


class Domain(DataObject):
    """ 
    Snapshot is the abstraction for each pull 
    that has been done to a concrete domain
    """
    id               = type('')
    domain           = type('')
    url              = type('')
    frequency        = type('') #allow to set up the periodicty
    last_snapshot_at = type(datetime)