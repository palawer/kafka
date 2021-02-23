from datetime import datetime
from db.dao import DataObject


class SnapshotCheckData(DataObject):
    """ SnapshotCheckData holds DomainCheck regexp results"""
    id             = type('')
    snapshot_id    = type('')
    domain_id      = type('')
    check_id       = type('')
    check_value    = type('')
    run_at         = type(datetime) #its always a good idea store when it run!