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


# link relation
REL_ABOUT = Relation('about', False)
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
REL_ASSIST_VALUES = Relation('http://identifiers.emc.com/linkrel/assist-values', False)
REL_RELATIONS = Relation('http://identifiers.emc.com/linkrel/relations', False)
REL_RELATION_TYPES = Relation('http://identifiers.emc.com/linkrel/relation-types', False)
REL_FORMATS = Relation('http://identifiers.emc.com/linkrel/formats', False)
REL_NETWORK_LOCATIONS = Relation('http://identifiers.emc.com/linkrel/network-locations', False)
REL_MATERIALIZE = Relation('http://identifiers.emc.com/linkrel/materialize', False)
REL_DEMATERIALIZE = Relation('http://identifiers.emc.com/linkrel/dematerialize', False)
REL_LIGHTWEIGHT_OBJECTS = Relation('http://identifiers.emc.com/linkrel/lightweight-objects', False)
REL_SHARED_PARENT = Relation('http://identifiers.emc.com/linkrel/shared-parent', False)
REL_ASPECT_TYPES = Relation('http://identifiers.emc.com/linkrel/aspect-types', False)
REL_OBJECT_ASPECTS = Relation('http://identifiers.emc.com/linkrel/object-aspects', False)
REL_BATCH_CAPABILITIES = Relation('http://identifiers.emc.com/linkrel/batch-capabilities', False)
REL_BATCHES = Relation('http://identifiers.emc.com/linkrel/batches', False)


class Link(object):
    def __init__(self, rel, href, is_template=False, title=None):
        """
        Init Link
        :param rel: link relation
        :param href: url
        :param is_template: mark whether the link is normal url or url template
        :param title: title of the link
        """

        self._rel_ = rel
        self._href_ = href
        self._title_ = title
        self._is_template_ = is_template

    def request(self):
        """
        Get the instance of RestRequest, which contains the request url
        :return: the instance of RestRequest
        """
        if not self._is_template_:
            return RestRequest.RestRequest(self._href_)
        else:
            return RestRequest.RestRequest(re.sub(r"\{.+\}$", "", str(self._href_)))

    def rel(self):
        return self._rel_

    def href(self):
        return self._href_

    def title(self):
        return self._title_

    def is_template(self):
        return self._is_template_

    def __repr__(self):
        return 'Link(%r, %r, %r, %r)' % (self._rel_, self._href_, self._is_template_, self._title_)

    def __str__(self):
        return 'rel: ' + self._rel_ + '\n' + 'href: ' + self._href_ + '\n' \
               + self._is_template_ + '\n' + self._title_ + '\n'
