from db.dao import DataObject


class DomainCheck(DataObject):
    id          = type('')
    domain_id   = type('')
    name        = type('')
    regexp      = type('')
