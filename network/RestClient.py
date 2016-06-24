import logging

from model.Link import *
from model import Resource

__author__ = 'wangc31'

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# media type
MEDIA_TYPE_DM_JSON = 'application/vnd.emc.documentum+json'
MEDIA_TYPE_HOME_JSON = 'application/home+json'
MEDIA_TYPE_OCTET_STREAM = 'application/octet-stream'


class RestClient:
    def __init__(self, user, pwd, rest_uri, repo):
        self._id = user
        self._pwd = pwd
        self._root_uri = rest_uri
        self._repo = repo
        self._repo_resource = self.get_repository(self._repo)

    def get_home_resource(self):
        home_link = Link('home', self._root_uri)
        return Resource.Home(self._link_get(home_link, accept=MEDIA_TYPE_HOME_JSON).resource())

    def get_product_info(self):
        return self._link_get(self.get_home_resource().get_product_info_link()).resource()

    def get_repositories(self):
        return self._link_get(self.get_home_resource().get_home_entry_link(REL_REPOSITORIES))

    def get_repository(self, repo_name):
        repositories = self.get_repositories().resource()
        return self._get_resource_via_entry(repositories, 'title', repo_name)

    def _get_repository(self):
        return self._repo_resource

    def get_cabinets(self, params=None):
        return self._get_objects(self._get_repository(), REL_CABINETS, params=params)

    def get_cabinet(self, cabinet_name):
        filter_criteria = 'starts-with(object_name,\'' + cabinet_name + '\')'
        cabinets = self.get_cabinets(params={'filter': filter_criteria})
        return self._get_resource_via_entry(cabinets, 'title', cabinet_name)

    def get_sysobjects(self, parent):
        return self._get_objects(parent, REL_OBJECTS)

    def get_sysobject(self, parent, object_name):
        return self._get_object(parent, REL_OBJECTS, 'title', object_name)

    def get_sharable_parent(self, lightweight_obj):
        return self._link_get(lightweight_obj.find_link(REL_SHARED_PARENT)).resource()

    def get_documents(self, parent):
        return self._get_objects(parent, REL_DOCUMENTS)

    def get_document(self, parent, object_name):
        return self._get_object(parent, REL_DOCUMENTS, 'title', object_name)

    def get_types(self, params=None):
        return self._get_objects(self._get_repository(), REL_TYPES, params=params)

    def get_type(self, type_name):
        return self._get_object(self._get_repository(), REL_TYPES, 'title', type_name)

    def get_value_assistance(self, dm_type, assist_value_request, included_property=None):
        return self._link_post(link=dm_type.find_link(REL_ASSIST_VALUES), data=assist_value_request.representation(),
                               params={'included-properties': included_property}).resource()

    def get_relations(self):
        return self._get_objects(self._get_repository(), REL_RELATIONS)

    def get_relation(self, parent, relation_name):
        return self._get_object(parent, REL_RELATIONS, 'title', relation_name)

    def get_formats(self, params):
        return self._get_objects(self._get_repository(), REL_FORMATS, params=params)

    def get_format(self, format_name):
        return self._get_object(self._get_repository(), REL_FORMATS, 'title', format_name)

    def get_network_locations(self):
        return self._get_objects(self._get_repository(), REL_NETWORK_LOCATIONS)

    def get_network_location(self, network_location_name):
        return self._get_object(self._get_repository(), REL_NETWORK_LOCATIONS, 'title', network_location_name)

    def get_relation_types(self):
        return self._get_objects(self._get_repository(), REL_RELATION_TYPES)

    def get_relation_type(self, relation_name):
        return self._get_object(self._get_repository(), REL_RELATION_TYPES, 'title', relation_name)

    def get_users(self, parent):
        return self._get_object(parent, REL_USERS)

    def get_user(self, user_name):
        return self._get_object(self._get_repository(), REL_USERS, 'title', user_name)

    def get_group(self, group_name):
        return self._get_object(self._get_repository(), REL_GROUPS, 'title', group_name)

    def get_folders(self, parent, params=None):
        return self._get_objects(parent, REL_FOLDERS, params=params)

    def get_folder(self, parent, folder_name):
        return self._get_object(parent, REL_FOLDERS, 'title', folder_name)

    def get_primary_content(self, obj, params=None):
        return self._follow_resource_link(obj, REL_PRIMARY_CONTENT, params=params)

    def get_contents(self, obj, params=None):
        return self._follow_resource_link(obj, REL_CONTENTS, params=params)

    def get_aspects(self):
        return self._get_objects(self._get_repository(), REL_ASPECT_TYPES)

    def get_aspect(self, aspect_name):
        return self._get_object(self._get_repository(), REL_ASPECT_TYPES, aspect_name)

    def create_cabinet(self, cabinet):
        return self._create_object_by_representation(self._get_repository(), REL_CABINETS, cabinet).resource()

    def create_folder(self, parent, new_folder):
        return self._create_object_by_representation(parent, REL_FOLDERS, new_folder).resource()

    def create_sysobj(self, parent, new_sysobj, rel=None, content=None):
        if rel is None:
            return self._create_object_by_representation(parent, REL_OBJECTS, new_sysobj, content).resource()
        else:
            return self._create_object_by_representation(parent, rel,
                                                         new_sysobj).resource()

    def create_document(self, parent, new_doc, content=None, params=None):
        return self._create_object_by_representation(parent, REL_DOCUMENTS, resource=new_doc, content=content,
                                                     params=params).resource()

    def create_user(self, new_user):
        return self._create_object_by_representation(self._get_repository(), REL_USERS, new_user).resource()

    def create_group(self, new_group):
        return self._create_object_by_representation(self._get_repository(), REL_GROUPS, new_group).resource()

    def create_relation(self, new_relation):
        return self._create_object_by_representation(self._get_repository(), REL_RELATIONS, new_relation).resource()

    def add_user_to_group(self, group, user_to_add):
        return self._create_object_by_reference(group, REL_USERS, user_to_add.reference()).resource()

    def add_group_to_group(self, group, group_to_add):
        return self._create_object_by_reference(group, REL_GROUPS, group_to_add.reference()).resource()

    def remove_user_from_group(self, group, member_name):
        self._remove_member_from_group(group, REL_USERS, member_name)

    def remove_group_from_group(self, group, member_name):
        self._remove_member_from_group(group, REL_GROUPS, member_name)

    def create_content(self, obj, content, content_type, params):
        return self._link_post(obj.find_link(REL_CONTENTS), data=content, accept=MEDIA_TYPE_DM_JSON,
                               content_type=content_type, params=params).resource()

    def check_out(self, obj):
        return self._link_put(obj.find_link(REL_CHECK_OUT), data=None).resource()

    def cancel_check_out(self, obj):
        self._link_delete(obj.find_link(REL_CANCEL_CHECK_OUT))

    def check_in_minor(self, obj, new_obj, content=None, params=None):
        return self._check_in(obj, REL_CHECK_IN_MINOR, new_obj, content, params).resource()

    def check_in_major(self, obj, new_obj, content=None, params=None):
        return self._check_in(obj, REL_CHECK_IN_MAJOR, new_obj, content, params).resource()

    def check_in_branch(self, obj, new_obj, content=None, params=None):
        return self._check_in(obj, REL_CHECK_IN_BRANCH, new_obj, content, params).resource()

    def dql(self, dql, params=None):
        if params:
            params['dql'] = dql
        else:
            params = {'dql': dql}

        return self._link_get(self._get_repository().find_link(REL_DQL), params=params).resource()

    def simple_search(self, q, params=None):
        if params:
            params['q'] = q
        else:
            params = {'q': q}

        return self._link_get(self._get_repository().find_link(REL_SEARCH), params=params).resource()

    def aql_search(self, aql, params=None):
        return self._link_post(self._get_repository().find_link(REL_SEARCH), data=aql, params=params).resource()

    def materialize(self, lightweight_obj):
        return self._link_put(lightweight_obj.find_link(REL_MATERIALIZE)).resource()

    def dematerialize(self, lightweight_obj):
        return self._link_delete(lightweight_obj.find_link(REL_DEMATERIALIZE))

    def reparent(self, lightweight_obj, new_parent):
        return self._create_object_by_reference(lightweight_obj, REL_SHARED_PARENT, new_parent.reference())

    def attach_aspects(self, obj, object_aspects):
        return self._link_post(obj.find_link(REL_OBJECT_ASPECTS), object_aspects.representation()).resource()

    def detach(self, obj, aspect):
        self._link_delete(obj.find_link(REL_DELETE, aspect))

    def refresh(self, obj):
        return self._follow_resource_link(obj, REL_SELF)

    def update(self, obj, update_resource):
        return self._link_post(obj.find_link(REL_EDIT), data=update_resource.representation()).resource()

    def delete(self, obj, params=None):
        if obj.find_link(REL_DELETE) is not None:
            self._link_delete(obj.find_link(REL_DELETE), params=params)
        elif obj.find_link(REL_SELF) is not None:
            self._link_delete(obj.find_link(REL_SELF), params=params)
        else:
            raise Exception(
                'Object %s is not deletable as there is no link detected for the delete operation.' % obj.get(
                    'properties').get('r_object_id'))

    def follow_link(self, link):
        return self._link_get(link, accept=MEDIA_TYPE_DM_JSON).resource()

    def previous_page(self, collection):
        return self._link_get(collection.find_link(REL_PREVIOUS)).resource()

    def next_page(self, collection):
        return self._link_get(collection.find_link(REL_NEXT)).resource()

    def first_page(self, collection):
        return self._link_get(collection.find_link(REL_FIRST)).resource()

    def last_page(self, collection):
        return self._link_get(collection.find_link(REL_LAST)).resource()

    def delete_folder_recursively(self, folder):
        # logger.info('Delete folder %s recursively.', folder.get('properties').get('object_name'))
        if not folder:
            return

        for sub_folder_entry in self.get_folders(folder).get_entries():
            sub_folder = self.follow_link(sub_folder_entry.find_link(REL_EDIT))
            self.delete_folder_recursively(sub_folder)

        for obj_entry in self.get_sysobjects(folder).get_entries():
            obj = self.follow_link(obj_entry.find_link(REL_EDIT))
            self.delete(obj)

        self.delete(folder)

    def _follow_resource_link(self, resource, rel, params=None):
        return self._link_get(resource.find_link(rel), params=params).resource()

    def _get_objects(self, parent, rel, params=None):
        return self._follow_resource_link(parent, rel, params)

    def _get_object(self, parent, rel, attr_name=None, attr_value=None):
        objects = self._get_objects(parent, rel)
        return self._get_resource_via_entry(objects, attr_name, attr_value)

    def _create_object_by_representation(self, parent, rel, resource, content=None, params=None):
        if content:
            return self._link_post_multipart(parent.find_link(rel), resource.representation(), content, params=params)
        else:
            return self._link_post(parent.find_link(rel), resource.representation(), params=params)

    def _create_object_by_reference(self, parent, rel, reference, params=None):
        return self._link_post(parent.find_link(rel), reference, params=params)

    def _check_in(self, obj, rel, new_obj, content=None, params=None):
        if new_obj and content:
            return self._link_post_multipart(obj.find_link(rel), obj=new_obj.representation(), content=content,
                                             params=params)
        elif not new_obj:
            return self._link_post(obj.find_link(rel), data=content, content_type=MEDIA_TYPE_OCTET_STREAM,
                                   params=params)
        elif not content:
            return self._link_post(obj.find_link(rel), data=new_obj.representation(), params=params)

        return None

    def _remove_member_from_group(self, group, rel, member_name):
        members_in_group = self._get_objects(group, rel)
        for member_in_group in members_in_group.get_entries():
            if member_name == member_in_group.get('title'):
                self.delete(member_in_group)

    def _link_get(self, link, accept=MEDIA_TYPE_DM_JSON, params=None):
        if link is not None:
            return link.request().auth(self._id, self._pwd).accept(
                accept).get(params=params)
        else:
            return None

    def _link_post_multipart(self, link, obj, content=None, accept=MEDIA_TYPE_DM_JSON,
                             content_type=MEDIA_TYPE_DM_JSON, params=None):
        if link is not None:
            multipart = [
                ('metadata', ('', obj, MEDIA_TYPE_DM_JSON)),
                ('binary', ('', content, ''))
            ]
            return link.request().auth(self._id, self._pwd).accept(accept).as_(content_type).post(files=multipart,
                                                                                                  params=params)
        else:
            return None

    def _link_post(self, link, data, accept=MEDIA_TYPE_DM_JSON, content_type=MEDIA_TYPE_DM_JSON, params=None):
        if link is not None:
            return link.request().auth(self._id, self._pwd).accept(accept).as_(content_type).post(data=data,
                                                                                                  params=params)
        else:
            return None

    def _link_put(self, link, data=None, accept=MEDIA_TYPE_DM_JSON, content_type=MEDIA_TYPE_DM_JSON, params=None):
        if link is not None:
            return link.request().auth(self._id, self._pwd).accept(accept).as_(content_type).put(data=data,
                                                                                                 params=params)
        else:
            return None

    def _link_delete(self, link, params=None):
        if link is not None:
            return link.request().auth(self._id, self._pwd).delete(params=params)
        else:
            return None

    def _get_resource_via_entry(self, collection, attr_name, attr_value):
        for resource_entry in collection.get_entries():
            if attr_value == resource_entry.get(attr_name):
                return self._link_get(resource_entry.find_link(REL_EDIT)).resource()
        return None


def main():
    return


if __name__ == '__main__':
    main()
else:
    print('RestClient as a module\n')
