"""
This is a module for REST related link classes.
"""

import re
from network import RestRequest

__author__ = 'wangc31'


class LinkRelation(object):
    """This class represents link relation."""

    def __init__(self, rel, hreftemplate):
        self.rel = rel
        self.hreftemplate = hreftemplate

    def __repr__(self):
        return super(LinkRelation, self).__repr__()


# link relation
REL_ABOUT = LinkRelation('about', False)
REL_SELF = LinkRelation('self', False)
REL_EDIT = LinkRelation('edit', False)
REL_DELETE = LinkRelation('http://identifiers.emc.com/linkrel/delete', False)
REL_NEXT = LinkRelation('next', False)
REL_PREVIOUS = LinkRelation('previous', False)
REL_FIRST = LinkRelation('first', False)
REL_LAST = LinkRelation('last', False)
REL_CONTENTS = LinkRelation('contents', False)
REL_PRIMARY_CONTENT = LinkRelation('http://identifiers.emc.com/linkrel/primary-content', False)
REL_FOLDERS = LinkRelation('http://identifiers.emc.com/linkrel/folders', False)
REL_REPOSITORIES = LinkRelation('http://identifiers.emc.com/linkrel/repositories', False)
REL_CABINETS = LinkRelation('http://identifiers.emc.com/linkrel/cabinets', False)
REL_OBJECTS = LinkRelation('http://identifiers.emc.com/linkrel/objects', False)
REL_DOCUMENTS = LinkRelation('http://identifiers.emc.com/linkrel/documents', False)
REL_USERS = LinkRelation('http://identifiers.emc.com/linkrel/users', False)
REL_GROUPS = LinkRelation('http://identifiers.emc.com/linkrel/groups', False)
REL_CHECK_OUT = LinkRelation('http://identifiers.emc.com/linkrel/checkout', False)
REL_CANCEL_CHECK_OUT = LinkRelation('http://identifiers.emc.com/linkrel/cancel-checkout', False)
REL_CHECK_IN_MINOR = LinkRelation('http://identifiers.emc.com/linkrel/checkin-next-minor', False)
REL_CHECK_IN_MAJOR = LinkRelation('http://identifiers.emc.com/linkrel/checkin-next-major', False)
REL_CHECK_IN_BRANCH = LinkRelation('http://identifiers.emc.com/linkrel/checkin-branch', False)
REL_SEARCH = LinkRelation('http://identifiers.emc.com/linkrel/search', True)
REL_SAVED_SEARCHES = LinkRelation('http://identifiers.emc.com/linkrel/saved-searches', False)
REL_SEARCH_EXECUTION = LinkRelation('http://identifiers.emc.com/linkrel/search-execution', False)
REL_SAVED_SEARCH_RESULTS = LinkRelation('http://identifiers.emc.com/linkrel/saved-search-results', False)
REL_SEARCH_TEMPLATES = LinkRelation('http://identifiers.emc.com/linkrel/search-templates', False)
REL_DQL = LinkRelation('http://identifiers.emc.com/linkrel/dql', True)
REL_TYPES = LinkRelation('http://identifiers.emc.com/linkrel/types', False)
REL_ASSIST_VALUES = LinkRelation('http://identifiers.emc.com/linkrel/assist-values', False)
REL_RELATIONS = LinkRelation('http://identifiers.emc.com/linkrel/relations', False)
REL_RELATION_TYPES = LinkRelation('http://identifiers.emc.com/linkrel/relation-types', False)
REL_FORMATS = LinkRelation('http://identifiers.emc.com/linkrel/formats', False)
REL_NETWORK_LOCATIONS = LinkRelation('http://identifiers.emc.com/linkrel/network-locations', False)
REL_MATERIALIZE = LinkRelation('http://identifiers.emc.com/linkrel/materialize', False)
REL_DEMATERIALIZE = LinkRelation('http://identifiers.emc.com/linkrel/dematerialize', False)
REL_LIGHTWEIGHT_OBJECTS = LinkRelation('http://identifiers.emc.com/linkrel/lightweight-objects', False)
REL_SHARED_PARENT = LinkRelation('http://identifiers.emc.com/linkrel/shared-parent', False)
REL_ASPECT_TYPES = LinkRelation('http://identifiers.emc.com/linkrel/aspect-types', False)
REL_OBJECT_ASPECTS = LinkRelation('http://identifiers.emc.com/linkrel/object-aspects', False)
REL_BATCH_CAPABILITIES = LinkRelation('http://identifiers.emc.com/linkrel/batch-capabilities', False)
REL_BATCHES = LinkRelation('http://identifiers.emc.com/linkrel/batches', False)


class Link(object):
    """This class represents link"""

    def __init__(self, rel, href, hreftemplate=False, title=None):
        """
        Init Link
        :param rel: link relation
        :param href: url
        :param hreftemplate: mark whether the link is normal url or url template
        :param title: title of the link
        """

        self.rel = rel
        self.href = href
        self.title = title
        self.hreftemplate = hreftemplate

    def request(self):
        """
        Get the instance of RestRequest, which contains the request url
        :return: the instance of RestRequest
        """
        if not self.hreftemplate:
            return RestRequest.RestRequest(self.href)
        else:
            return RestRequest.RestRequest(re.sub(r"\{.+\}$", "", str(self.href)))

    def __repr__(self):
        return 'Link(%r, %r, %r, %r)' % (self.rel, self.href, self.hreftemplate, self.title)

    def __str__(self):
        return 'rel: %s, hreftemplate: %s, title: %s \nhref: %s' % (self.rel, self.hreftemplate, self.title, self.href)
