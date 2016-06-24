import re
from network import RestRequest

__author__ = 'wangc31'


class Relation(object):
    def __init__(self, rel, template):
        self._rel_ = rel
        self._template_ = template

    def rel(self):
        return self._rel_

    def is_template(self):
        return self._template_


class Link(object):
    # link relation
    REL_SELF = Relation('self', False)
    REL_EDIT = Relation('edit', False)
    REL_DELETE = Relation('http://identifiers.emc.com/linkrel/delete', False)
    REL_NEXT = Relation('next', False)
    REL_PREVIOUS = Relation('previous', False)
    REL_FIRST = Relation('first', False)
    REL_LAST = Relation('last', False)
    REL_CONTENTS = Relation('contents', False)
    REL_PRIMARY_CONTENT = Relation('http://identifiers.emc.com/linkrel/primary-content', False)
    REL_FOLDERS = Relation('http://identifiers.emc.com/linkrel/folders', False)
    REL_REPOSITORIES = Relation('http://identifiers.emc.com/linkrel/repositories', False)
    REL_CABINETS = Relation('http://identifiers.emc.com/linkrel/cabinets', False)
    REL_OBJECTS = Relation('http://identifiers.emc.com/linkrel/objects', False)
    REL_DOCUMENTS = Relation('http://identifiers.emc.com/linkrel/documents', False)
    REL_USERS = Relation('http://identifiers.emc.com/linkrel/users', False)
    REL_GROUPS = Relation('http://identifiers.emc.com/linkrel/groups', False)
    REL_CHECK_OUT = Relation('http://identifiers.emc.com/linkrel/checkout', False)
    REL_CANCEL_CHECK_OUT = Relation('http://identifiers.emc.com/linkrel/cancel-checkout', False)
    REL_CHECK_IN_MINOR = Relation('http://identifiers.emc.com/linkrel/checkin-next-minor', False)
    REL_CHECK_IN_MAJOR = Relation('http://identifiers.emc.com/linkrel/checkin-next-major', False)
    REL_CHECK_IN_BRANCH = Relation('http://identifiers.emc.com/linkrel/checkin-branch', False)
    REL_SEARCH = Relation('http://identifiers.emc.com/linkrel/search', True)
    REL_DQL = Relation('http://identifiers.emc.com/linkrel/dql', True)
    REL_TYPES = Relation('http://identifiers.emc.com/linkrel/types', False)

    def __init__(self, rel, href, is_template=False):
        self._rel_ = rel
        self._href_ = href
        self._is_template_ = is_template

    def request(self):
        if not self._is_template_:
            return RestRequest.RestRequest(self._href_)
        else:
            return RestRequest.RestRequest(re.sub(r"\{.+\}$", "", str(self._href_)))

    def rel(self):
        return self._rel_

    def href(self):
        return self._href_

    def is_template(self):
        return self._is_template_

    def __str__(self):
        return 'rel: ' + self._rel_ + '\n' + 'href: ' + self._href_ + '\n'
