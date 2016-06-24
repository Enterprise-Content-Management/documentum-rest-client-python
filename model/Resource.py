import Link
import json

__author__ = 'wangc31'


class Resource(object):
    def __init__(self, raw_resource):
        self._raw_resource_ = raw_resource
        self._rest_links_ = []
        self._init_links()

    def _init_links(self):
        if not self.is_key_existing('links'):
            return

        for link in self.get('links'):
            if self._is_valid_link(link):
                self._rest_links_.append(self._generate_link(link))

    def keys(self):
        return self._raw_resource_.keys()

    def get(self, key):
        return self._raw_resource_.get(key)

    def put(self, key, value):
        self._raw_resource_[key] = value

    def all_links(self):
        return self._rest_links_

    def find_link(self, rel, title=None):
        for link in self._rest_links_:
            if link.rel() == rel.rel() and link.is_template() == rel.is_template() and (
                            title is None or title == link.title()):
                return link

        return None

    def entry_count(self):
        return len(self.get('entries'))

    def get_entry(self, index):
        entry = Resource(self.get('entries')[index])
        return entry

    def get_entries(self):
        if not self.is_key_existing('entries'):
            return []

        entries = []
        for raw_entry in self.get('entries'):
            entries.append(Resource(raw_entry))

        return entries

    def is_key_existing(self, key):
        return key in self._raw_resource_

    def raw_resource(self):
        return self._raw_resource_

    def representation(self, indent=4):
        return json.dumps(self._raw_resource_, indent=indent)

    def reference(self, indent=4):
        reference = {'href': self.find_link(Link.REL_SELF).href()}
        return json.dumps(reference, indent=indent)

    @staticmethod
    def _generate_link(link):
        if 'href' in link:
            return Link.Link(link['rel'], link['href'], False, link['title'] if 'title' in link else None)
        elif 'hreftemplate' in link:
            return Link.Link(link['rel'], link['hreftemplate'], True)

        return None

    @staticmethod
    def _is_valid_link(link):
        if 'rel' not in link:
            return False

        if 'href' in link or 'hreftemplate' in link:
            return True

        return False


class Home(Resource):
    def __init__(self, resource):
        super(Home, self).__init__(resource.raw_resource())

    def get_home_entry_link(self, rel):
        for key in self.get('resources'):
            if key == rel.rel():
                return Link.Link(key, self.get('resources').get(key).get('href'))

    def get_product_info_link(self):
        return Link.Link('about', self.get('resources').get('about').get('href'))

    def get_home_entry_methods(self, rel):
        for key in self.get('resources'):
            if key == rel.rel():
                return self.get('resources').get(key).get('hints').get('allow')

    def get_home_entry_media_types(self, rel):
        for key in self.get('resources'):
            if key == rel.rel():
                return self.get('resources').get(key).get('hints').get('representations')
