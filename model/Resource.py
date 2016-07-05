import json
import model.Link

__author__ = 'wangc31'


class Resource(object):
    def __init__(self, raw_resource):
        """
        This is the model for REST resources. Actually it stores the data of resource in a dictionary.
        Besides, a resource is linkable, which means it contains a list of links.
        :param raw_resource: the raw resource is a dictionary.
        """
        self._raw_resource_ = raw_resource
        self._rest_links_ = []
        self._init_links()

    def _init_links(self):
        """
        Initialize the links of a resource
        :return:
        """
        if not self.is_key_existing('links'):
            return

        for link in self.get('links'):
            if self._is_valid_link(link):
                self._rest_links_.append(self._generate_link(link))

    def keys(self):
        """
        Get the top level keys of a resource
        :return: top level keys
        """
        return self._raw_resource_.keys()

    def get(self, key):
        """
        Get the attribute value according to the key
        :param key: attribute key
        :return: attribute value
        """
        return self._raw_resource_.get(key)

    def put(self, key, value):
        """
        Add the attribute key and value
        :param key: attribute key
        :param value: attribute value
        :return:
        """
        self._raw_resource_[key] = value

    def all_links(self):
        """
        Get all the links
        :return: links
        """
        return self._rest_links_

    def find_link(self, rel, title=None):
        """
        Get the link according to link relation and title
        :param rel: link relation
        :param title: link title
        :return: matched link
        """
        for link in self._rest_links_:
            if link.rel() == rel.rel() and link.is_template() == rel.is_template() and (
                            title is None or title == link.title()):
                return link

        return None

    def entry_count(self):
        """
        Get count of the entries if the resource is a collection
        :return: count of entries
        """
        return len(self.get('entries'))

    def get_entry(self, index):
        """
        Get an entry at position index
        :param index: entry index
        :return: entry
        """
        entry = Resource(self.get('entries')[index])
        return entry

    def get_entries(self):
        """
        Get the collection of entries
        :return: entries
        """
        if not self.is_key_existing('entries'):
            return []

        entries = []
        for raw_entry in self.get('entries'):
            entries.append(Resource(raw_entry))

        return entries

    def is_key_existing(self, key):
        """
        Check whether an attribute key exists
        :param key: the attribute key
        :return: True if existing
        """
        return key in self._raw_resource_

    def raw_resource(self):
        """
        Get the raw resource, which is actually a dictionary
        :return: raw resource
        """
        return self._raw_resource_

    def representation(self, indent=4):
        """
        Get the representation of the raw resource, which is in JSON
        :param indent: indent of JSON representation
        :return: JSON representation
        """
        return json.dumps(self._raw_resource_, indent=indent)

    def reference(self, indent=4):
        """
        Get the reference of a resource in JSON, like:
        {"reference": "http://localhost:8080/dctm-rest/repositories/REPO/objects/090000058000251a"}
        :param indent: indent of JSON representation
        :return: reference in JSON
        """
        reference = {'href': self.find_link(model.Link.REL_SELF).href()}
        return json.dumps(reference, indent=indent)

    @staticmethod
    def _generate_link(link_dict):
        """
        Generate instance of model.Link from link in raw resource
        :param link_dict: the link in the raw resource
        :return: instance of model.Link
        """
        if 'href' in link_dict:
            return model.Link.Link(link_dict['rel'], link_dict['href'], False,
                                   link_dict['title'] if 'title' in link_dict else None)
        elif 'hreftemplate' in link_dict:
            return model.Link.Link(link_dict['rel'], link_dict['hreftemplate'], True)

        return None

    @staticmethod
    def _is_valid_link(link_dict):
        """
        Check whether a link in raw resource is valid
        :param link_dict: link in raw resource
        :return: True if the link is valid
        """
        if 'rel' in link_dict and ('href' in link_dict or 'hreftemplate' in link_dict):
            return True
        else:
            return False


class Home(Resource):
    """
    This is the model of home resource
    """

    def __init__(self, resource):
        """
        Initialize the home resource
        :param resource: data in response of the entry url
        """
        super(Home, self).__init__(resource.raw_resource())

    def get_home_entry_link(self, rel):
        """
        Get link from home resource according to link relation
        :param rel: link relation
        :return: matched link
        """
        for key in self.get('resources'):
            if key == rel.rel():
                return model.Link.Link(key, self.get('resources').get(key).get('href'))

    def get_product_info_link(self):
        return self.get_home_entry_link(model.Link.REL_ABOUT)

    def get_home_entry_methods(self, rel):
        """
        Get supported HTTP methods for a link specified by the link relation
        :param rel: link relation
        :return: array of support HTTP methods
        """
        for key in self.get('resources'):
            if key == rel.rel():
                return self.get('resources').get(key).get('hints').get('allow')

    def get_home_entry_media_types(self, rel):
        """
        Get supported media types for a link specified by the link relation
        :param rel: link relation
        :return: array supported media types
        """
        for key in self.get('resources'):
            if key == rel.rel():
                return self.get('resources').get(key).get('hints').get('representations')
