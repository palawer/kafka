from db.dao import DataObject


class SnapshotMetadata(DataObject):
    """ SnapshotMetadata holds HTTP GET response metadata"""
    id             = type('')
    snapshot_id    = type('')
    domain_id      = type('')
    request_time   = type(0.0)
    request_status = type(0)