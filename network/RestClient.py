from model.Link import Link
from model import Resource

__author__ = 'wangc31'

# media type
MEDIA_TYPE_DM_JSON = 'application/vnd.emc.documentum+json'
MEDIA_TYPE_HOME_JSON = 'application/home+json'
MEDIA_TYPE_OCTET_STREAM = 'application/octet-stream'


class RestClient:
    def __init__(self, user, pwd, rest_uri):
        self._id = user
        self._pwd = pwd
        self._root_uri = rest_uri

    def get_home_resource(self):
        home_link = Link('home', self._root_uri)
        return Resource.Home(self._link_get(home_link, accept=MEDIA_TYPE_HOME_JSON).resource())

    def get_repositories(self, home):
        return self._link_get(home.get_home_entry_link(Link.REL_REPOSITORIES))

    def get_repository(self, home, repo_name):
        repositories = self.get_repositories(home).resource()
        return self._get_resource_via_entry(repositories, 'title', repo_name)

    def get_cabinets(self, repository, params=None):
        return self._get_objects(repository, Link.REL_CABINETS, params=params)

    def get_cabinet(self, repository, cabinet_name):
        filter_criteria = 'starts-with(object_name,\'' + cabinet_name + '\')'
        cabinets = self.get_cabinets(repository, params={'filter': filter_criteria})
        return self._get_resource_via_entry(cabinets, 'title', cabinet_name)

    def get_sysobjects(self, parent):
        return self._get_objects(parent, Link.REL_OBJECTS)

    def get_sysobject(self, parent, object_name):
        return self._get_object(parent, Link.REL_OBJECTS, 'title', object_name)

    def get_documents(self, parent):
        return self._get_objects(parent, Link.REL_DOCUMENTS)

    def get_document(self, parent, object_name):
        return self._get_object(parent, Link.REL_DOCUMENTS, 'title', object_name)

    def get_types(self, parent):
        return self._get_objects(parent, Link.REL_TYPES)

    def get_type(self, parent, type_name):
        return self._get_object(parent, Link.REL_TYPES, 'title', type_name)

    def get_users(self, parent):
        return self._get_object(parent, Link.REL_USERS)

    def get_user(self, parent, user_name):
        return self._get_object(parent, Link.REL_USERS, 'title', user_name)

    def get_folders(self, parent, params=None):
        return self._get_objects(parent, Link.REL_FOLDERS, params=params)

    def get_folder(self, parent, folder_name):
        return self._get_object(parent, Link.REL_FOLDERS, 'title', folder_name)

    def get_primary_content(self, obj, params=None):
        return self._follow_resource_link(obj, Link.REL_PRIMARY_CONTENT, params=params)

    def get_contents(self, obj, params=None):
        return self._follow_resource_link(obj, Link.REL_CONTENTS, params=params)

    def create_cabinet(self, parent, cabinet):
        return self._create_object(parent, Link.REL_CABINETS, cabinet).resource()

    def create_folder(self, parent, folder_properties):
        return self._create_object(parent, Link.REL_FOLDERS, folder_properties).resource()

    def create_sysobj(self, parent, properties, content=None):
        return self._create_object(parent, Link.REL_OBJECTS, properties, content).resource()

    def create_document(self, parent, obj, content=None, params=None):
        return self._create_object(parent, Link.REL_DOCUMENTS, properties=obj, content=content,
                                   params=params).resource()

    def create_user(self, parent, properties):
        return self._create_object(parent, Link.REL_USERS, properties).resource()

    def create_group(self, parent, properties):
        return self._create_object(parent, Link.REL_GROUPS, properties).resource()

    def add_user_to_group(self, group, properties):
        return self._create_object(group, Link.REL_USERS, properties).resource()

    def add_group_to_group(self, group, properties):
        return self._create_object(group, Link.REL_GROUPS, properties).resource()

    def remove_user_from_group(self, group, member_name):
        self._remove_member_from_group(group, Link.REL_USERS, member_name)

    def remove_group_from_group(self, group, member_name):
        self._remove_member_from_group(group, Link.REL_GROUPS, member_name)

    def create_content(self, obj, content, content_type, params):
        self._link_post(obj.find_link(Link.REL_CONTENTS), data=content, accept=MEDIA_TYPE_DM_JSON,
                        content_type=content_type, params=params)

    def check_out(self, obj):
        return self._link_put(obj.find_link(Link.REL_CHECK_OUT), data=None).resource()

    def cancel_check_out(self, obj):
        self._link_delete(obj.find_link(Link.REL_CANCEL_CHECK_OUT))

    def check_in_minor(self, obj, new_obj, content=None, params=None):
        return self._check_in(obj, Link.REL_CHECK_IN_MINOR, new_obj, content, params).resource()

    def check_in_major(self, obj, new_obj, content=None, params=None):
        return self._check_in(obj, Link.REL_CHECK_IN_MAJOR, new_obj, content, params).resource()

    def check_in_branch(self, obj, new_obj, content=None, params=None):
        return self._check_in(obj, Link.REL_CHECK_IN_BRANCH, new_obj, content, params).resource()

    def dql(self, repository, dql, params=None):
        if params:
            params['dql'] = dql
        else:
            params = {'dql': dql}

        return self._link_get(repository.find_link(Link.REL_DQL), params=params).resource()

    def simple_search(self, repository, q, params=None):
        if params:
            params['q'] = q
        else:
            params = {'q': q}

        return self._link_get(repository.find_link(Link.REL_SEARCH), params=params).resource()

    def refresh(self, obj):
        return self._follow_resource_link(obj, Link.REL_SELF)

    def update(self, obj, properties):
        return self._link_post(obj.find_link(Link.REL_EDIT), data=properties).resource()

    def delete(self, obj, params=None):
        self._link_delete(obj.find_link(Link.REL_DELETE), params=params)

    def follow_link(self, link):
        return self._link_get(link, accept=MEDIA_TYPE_DM_JSON).resource()

    def previous_page(self, collection):
        return self._link_get(collection.find_link(Link.REL_PREVIOUS)).resource()

    def next_page(self, collection):
        return self._link_get(collection.find_link(Link.REL_NEXT)).resource()

    def first_page(self, collection):
        return self._link_get(collection.find_link(Link.REL_FIRST)).resource()

    def last_page(self, collection):
        return self._link_get(collection.find_link(Link.REL_LAST)).resource()

    def delete_folder_recursively(self, folder):
        if not folder:
            return

        for sub_folder_entry in self.get_folders(folder).get_entries():
            sub_folder = self.follow_link(sub_folder_entry.find_link(Link.REL_EDIT))
            self.delete_folder_recursively(sub_folder)

        for obj_entry in self.get_sysobjects(folder).get_entries():
            obj = self.follow_link(obj_entry.find_link(Link.REL_EDIT))
            self.delete(obj)

        self.delete(folder)

    def _follow_resource_link(self, resource, rel, params=None):
        return self._link_get(resource.find_link(rel), params=params).resource()

    def _get_objects(self, parent, rel, params=None):
        return self._follow_resource_link(parent, rel, params)

    def _get_object(self, parent, rel, attr_name=None, attr_value=None):
        objects = self._get_objects(parent, rel)
        return self._get_resource_via_entry(objects, attr_name, attr_value)

    def _create_object(self, parent, rel, properties, content=None, params=None):
        if content:
            return self._link_post_multipart(parent.find_link(rel), properties, content, params=params)
        else:
            return self._link_post(parent.find_link(rel), properties, params=params)

    def _check_in(self, obj, rel, new_obj, content=None, params=None):
        if new_obj and content:
            return self._link_post_multipart(obj.find_link(rel), obj=new_obj, content=content, params=params)
        elif not new_obj:
            return self._link_post(obj.find_link(rel), data=content, content_type=MEDIA_TYPE_OCTET_STREAM,
                                   params=params)
        elif not content:
            return self._link_post(obj.find_link(rel), data=new_obj, params=params)

        return None

    def _remove_member_from_group(self, group, rel, member_name):
        members_in_group = self._get_objects(group, rel)
        for member_in_group in members_in_group.get_entries():
            if member_name == member_in_group.get('title'):
                self.delete(member_in_group)

    def _link_get(self, link, accept=MEDIA_TYPE_DM_JSON, params=None):
        return link.request().auth(self._id, self._pwd).accept(
            accept).get(params=params)

    def _link_post_multipart(self, link, obj, content=None, accept=MEDIA_TYPE_DM_JSON,
                             content_type=MEDIA_TYPE_DM_JSON, params=None):
        multipart = [
            ('medadata', ('', obj, MEDIA_TYPE_DM_JSON)),
            ('binary', ('', content, ''))
        ]
        return link.request().auth(self._id, self._pwd).accept(accept).as_(content_type).post(files=multipart,
                                                                                              params=params)

    def _link_post(self, link, data, accept=MEDIA_TYPE_DM_JSON, content_type=MEDIA_TYPE_DM_JSON, params=None):
        return link.request().auth(self._id, self._pwd).accept(accept).as_(content_type).post(data=data, params=params)

    def _link_put(self, link, data, accept=MEDIA_TYPE_DM_JSON, content_type=MEDIA_TYPE_DM_JSON, params=None):
        return link.request().auth(self._id, self._pwd).accept(accept).as_(content_type).put(data=data, params=params)

    def _link_delete(self, link, params=None):
        return link.request().auth(self._id, self._pwd).delete(params=params)

    def _get_resource_via_entry(self, collection, attr_name, attr_value):
        for resource_entry in collection.get_entries():
            if attr_value == resource_entry.get(attr_name):
                return self._link_get(resource_entry.find_link(Link.REL_EDIT)).resource()
        return None


def main():
    return


if __name__ == '__main__':
    main()
else:
    print('RestClient as a module\n')
