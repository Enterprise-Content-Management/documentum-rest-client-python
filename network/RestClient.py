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
        """
        Initialize the essential info user name, user password and REST context URL.
        Besides, the repository resource that the REST client is specific to is populated.
        :param user: user name
        :param pwd: user password
        :param rest_uri: REST context URL
        :param repo: the repository resource of the REST client
        """
        self._id = user
        self._pwd = pwd
        self._root_uri = rest_uri
        self._repo = repo
        self._repo_resource = self.get_repository(self._repo)

    def get_home_resource(self):
        """
        Get home resource
        :return: home resource
        """
        home_link = Link('home', self._root_uri)
        return Resource.Home(self._link_get(home_link, accept=MEDIA_TYPE_HOME_JSON).resource())

    def get_product_info(self):
        """
        Get production info resource
        :return: production info resource
        """
        return self._link_get(self.get_home_resource().get_product_info_link()).resource()

    def get_repositories(self, params=None):
        """
        Get repositories resource
        :return: repositories resource
        """
        return self._link_get(self.get_home_resource().get_home_entry_link(REL_REPOSITORIES), params=params)

    def get_repository(self, repo_name):
        """
        Get repository resource
        :param repo_name: repository name
        :return: repository resource
        """
        repositories = self.get_repositories().resource()
        return self._get_resource_via_entry(repositories, 'title', repo_name)

    def get_cabinets(self, params=None):
        """
        Get cabinets resource
        :param params: URL parameters
        :return: cabinets resources
        """
        return self._get_objects(self._get_repository(), REL_CABINETS, params=params)

    def get_cabinet(self, cabinet_name):
        """
        Get cabinet resource
        :param cabinet_name: cabinet name
        :return: cabinet resource
        """
        filter_criteria = 'starts-with(object_name,\'' + cabinet_name + '\')'
        cabinets = self.get_cabinets(params={'filter': filter_criteria})
        return self._get_resource_via_entry(cabinets, 'title', cabinet_name)

    def get_sysobjects(self, parent, params=None):
        """
        Get system objects
        :param parent: the parent resource of the system objects
        :param params: URL parameters
        :return: system objects
        """
        return self._get_objects(parent, REL_OBJECTS, params=params)

    def get_sysobject(self, parent, object_name):
        """
        Get system object
        :param parent: the parent resource of the system objects
        :param object_name: name of system object
        :return: system object
        """
        return self._get_object(parent, REL_OBJECTS, 'title', object_name)

    def get_sharable_parent(self, lightweight_obj):
        """
        Get sharable parent
        :param lightweight_obj: the lightweight object to find its sharable parent
        :return: sharable parent
        """
        return self._link_get(lightweight_obj.find_link(REL_SHARED_PARENT)).resource()

    def get_documents(self, parent, params=None):
        """
        Get documents resource
        :param parent: the parent resource of the documents
        :param params: URL parameters
        :return: documents resource
        """
        return self._get_objects(parent, REL_DOCUMENTS, params)

    def get_document(self, parent, object_name):
        """
        Get document resource
        :param parent: the parent resource of the documents
        :param object_name: object name of the document
        :return: document resource
        """
        return self._get_object(parent, REL_DOCUMENTS, 'title', object_name)

    def get_types(self, params=None):
        """
        Get types resource
        :param params: URL parameters
        :return: types resource
        """
        return self._get_objects(self._get_repository(), REL_TYPES, params=params)

    def get_type(self, type_name):
        """
        Get type resource
        :param type_name: type name
        :return: type resource
        """
        return self._get_object(self._get_repository(), REL_TYPES, 'title', type_name)

    def get_value_assistance(self, dm_type, assist_value_request, included_property=None):
        """
        Get value assistance of one type
        :param dm_type: the type to get its value assistance
        :param assist_value_request: assist value request
        :param included_property: URL parameter included-properties
        :return: value assistance
        """
        return self._link_post(link=dm_type.find_link(REL_ASSIST_VALUES), data=assist_value_request.representation(),
                               params={'included-properties': included_property}).resource()

    def get_relations(self, params=None):
        """
        Get relations resource
        :param params: URL parameters
        :return: relations resource
        """
        return self._get_objects(self._get_repository(), REL_RELATIONS, params=params)

    def get_relation(self, parent, relation_name):
        """
        Get relation resource
        :param parent: parent resource of relations
        :param relation_name: relation name
        :return: relation resource
        """
        return self._get_object(parent, REL_RELATIONS, 'title', relation_name)

    def get_formats(self, params=None):
        """
        Get formats resource
        :param params: URL parameters
        :return: formats resource
        """
        return self._get_objects(self._get_repository(), REL_FORMATS, params=params)

    def get_format(self, format_name):
        """
        Get format resource
        :param format_name: format name
        :return: format resource
        """
        return self._get_object(self._get_repository(), REL_FORMATS, 'title', format_name)

    def get_network_locations(self, params=None):
        """
        Get network locations resource
        :param params: URL parameters
        :return: network locations resource
        """
        return self._get_objects(self._get_repository(), REL_NETWORK_LOCATIONS, params=params)

    def get_network_location(self, network_location_name):
        """
        Get network location resource
        :param network_location_name: network location name
        :return: network location resource
        """
        return self._get_object(self._get_repository(), REL_NETWORK_LOCATIONS, 'title', network_location_name)

    def get_relation_types(self, params=None):
        """
        Get relation types resource
        :param params: URL parameters
        :return: relation types resource
        """
        return self._get_objects(self._get_repository(), REL_RELATION_TYPES, params)

    def get_relation_type(self, relation_type_name):
        """
        Get relation type resource
        :param relation_type_name: relation type name
        :return: relation type resource
        """
        return self._get_object(self._get_repository(), REL_RELATION_TYPES, 'title', relation_type_name)

    def get_users(self, parent, params=None):
        """
        Get users resource
        :param parent: parent resource of users
        :param params: URL parameters
        :return: users resource
        """
        return self._get_objects(parent, REL_USERS, params=params)

    def get_user(self, user_name):
        """
        Get user resource
        :param user_name: user name
        :return: user resource
        """
        return self._get_object(self._get_repository(), REL_USERS, 'title', user_name)

    def get_group(self, group_name):
        """
        Get group resource
        :param group_name: group name
        :return: group resource
        """
        return self._get_object(self._get_repository(), REL_GROUPS, 'title', group_name)

    def get_folders(self, parent, params=None):
        """
        Get folders resource
        :param parent: parent resource of folders
        :param params: URL parameters
        :return: folders resource
        """
        return self._get_objects(parent, REL_FOLDERS, params=params)

    def get_folder(self, parent, folder_name):
        """
        Get folder resource
        :param parent: parent resource of folders
        :param folder_name: folder name
        :return: folder resource
        """
        return self._get_object(parent, REL_FOLDERS, 'title', folder_name)

    def get_primary_content(self, obj, params=None):
        """
        Get primary content resource
        :param obj: system object owning the primary content
        :param params: URL parameters
        :return: primary content resource
        """
        return self._follow_resource_link(obj, REL_PRIMARY_CONTENT, params=params)

    def get_contents(self, obj, params=None):
        """
        Get contents resource
        :param obj: system object owning the contents
        :param params: URL parameters
        :return: content resource
        """
        return self._follow_resource_link(obj, REL_CONTENTS, params=params)

    def get_aspects(self, params=None):
        """
        Get aspects resource
        :param params: URL parameters
        :return: aspects resource
        """
        return self._get_objects(self._get_repository(), REL_ASPECT_TYPES, params=params)

    def get_aspect(self, aspect_name):
        """
        Get aspect resource
        :param aspect_name: aspect name
        :return: aspect resource
        """
        return self._get_object(self._get_repository(), REL_ASPECT_TYPES, aspect_name)

    def create_cabinet(self, cabinet):
        """
        Create cabinet resource
        :param cabinet: cabinet resource to create
        :return: created cabinet resource
        """
        return self._create_object_by_representation(self._get_repository(), REL_CABINETS, cabinet).resource()

    def create_folder(self, parent, new_folder):
        """
        Create folder resource
        :param parent: parent resource of the folder
        :param new_folder: folder resource to create
        :return: created folder resource
        """
        return self._create_object_by_representation(parent, REL_FOLDERS, new_folder).resource()

    def create_sysobj(self, parent, new_sysobj, rel=None, content=None, params=None):
        """
        Create system object resource
        :param parent: parent resource of the system object
        :param new_sysobj: system object resource to created
        :param rel: the link relation which defines the sub-type of the system object to create;
                    default is system object
        :param params: URL parameters
        :param content: the content of the system object to create
        :return: created system object resource
        """
        if rel is None:
            return self._create_object_by_representation(parent, REL_OBJECTS, new_sysobj, content,
                                                         params=params).resource()
        else:
            return self._create_object_by_representation(parent, rel,
                                                         new_sysobj, params=params).resource()

    def create_document(self, parent, new_doc, content=None, params=None):
        """
        Create system document resource
        :param parent: parent resource of the document
        :param new_doc: document resource to create
        :param content: the content of the document to create
        :param params: URL parameters
        :return: created document resource
        """
        return self._create_object_by_representation(parent, REL_DOCUMENTS, resource=new_doc, content=content,
                                                     params=params).resource()

    def create_user(self, new_user):
        """
        Create user resource
        :param new_user: user resource to create
        :return: created user resource
        """
        return self._create_object_by_representation(self._get_repository(), REL_USERS, new_user).resource()

    def create_group(self, new_group):
        """
        Create group resource
        :param new_group: group resource to create
        :return: created group resource
        """
        return self._create_object_by_representation(self._get_repository(), REL_GROUPS, new_group).resource()

    def create_relation(self, new_relation):
        """
        Create relation resource
        :param new_relation: relation resource to create
        :return: created relation resource
        """
        return self._create_object_by_representation(self._get_repository(), REL_RELATIONS, new_relation).resource()

    def add_user_to_group(self, group, user_to_add):
        """
        Add user to group
        :param group: the target group resource
        :param user_to_add: the user resource to add
        :return:
        """
        self._create_object_by_reference(group, REL_USERS, user_to_add.reference()).resource()

    def add_group_to_group(self, group, group_to_add):
        """
        Add group to group
        :param group: the target group resource
        :param group_to_add: the group resource to add
        :return:
        """
        self._create_object_by_reference(group, REL_GROUPS, group_to_add.reference()).resource()

    def remove_user_from_group(self, group, user_to_remove):
        """
        Remove user from group
        :param group: the target group
        :param user_to_remove: the user resource to remove
        :return:
        """
        self._remove_member_from_group(group, REL_USERS, user_to_remove)

    def remove_group_from_group(self, group, group_to_remove):
        """
        Remove group from group
        :param group: the target gtoup
        :param group_to_remove: the group resource to remove
        :return:
        """
        self._remove_member_from_group(group, REL_GROUPS, group_to_remove)

    def create_content(self, obj, content, content_type, params):
        """
        Create content
        :param obj: the system object owning the content
        :param content: the content to remove
        :param content_type: content type
        :param params: URL parameters
        :return:
        """
        return self._link_post(obj.find_link(REL_CONTENTS), data=content, accept=MEDIA_TYPE_DM_JSON,
                               content_type=content_type, params=params).resource()

    def check_out(self, obj):
        """
        Check out system object
        :param obj: the system out to check out
        :return:
        """
        return self._link_put(obj.find_link(REL_CHECK_OUT), data=None).resource()

    def cancel_check_out(self, obj):
        """
        Cancel check out
        :param obj: the checked out system object
        :return:
        """
        self._link_delete(obj.find_link(REL_CANCEL_CHECK_OUT))

    def check_in_minor(self, obj, new_obj, content=None, params=None):
        """
        Check in minor version
        :param obj: the original system object
        :param new_obj: the new system object to check in
        :param content: the content
        :param params: URL parameters
        :return:
        """
        return self._check_in(obj, REL_CHECK_IN_MINOR, new_obj, content, params).resource()

    def check_in_major(self, obj, new_obj, content=None, params=None):
        """
        Check in major version
        :param obj: the original system object
        :param new_obj: the new system object to check in
        :param content: the content
        :param params: URL parameters
        :return:
        """
        return self._check_in(obj, REL_CHECK_IN_MAJOR, new_obj, content, params).resource()

    def check_in_branch(self, obj, new_obj, content=None, params=None):
        """
        Check in branch
        :param obj: the original system object
        :param new_obj: the new system object to check in
        :param content: the content
        :param params: URL paramters
        :return:
        """
        return self._check_in(obj, REL_CHECK_IN_BRANCH, new_obj, content, params).resource()

    def dql(self, dql, params=None):
        """
        Execute DQL
        :param dql: DQL statement
        :param params: URL parameters
        :return: query results
        """
        if params:
            params['dql'] = dql
        else:
            params = {'dql': dql}

        return self._link_get(self._get_repository().find_link(REL_DQL), params=params).resource()

    def simple_search(self, q, params=None):
        """
        Execute search via simple search language
        :param q: query criteria in simple search language
        :param params: URl parameter
        :return: query results
        """
        if params:
            params['q'] = q
        else:
            params = {'q': q}

        return self._link_get(self._get_repository().find_link(REL_SEARCH), params=params).resource()

    def aql_search(self, aql, params=None):
        """
        Execute search via AQL
        :param aql: query criteria in abstract query language
        :param params: URL parameters
        :return: query results
        """
        return self._link_post(self._get_repository().find_link(REL_SEARCH), data=aql, params=params).resource()

    def materialize(self, lightweight_obj):
        """
        Materialize lightweight object
        :param lightweight_obj: the lightweight object to materialize
        :return:
        """
        return self._link_put(lightweight_obj.find_link(REL_MATERIALIZE)).resource()

    def dematerialize(self, lightweight_obj):
        """
        Dematerialize lightweight object
        :param lightweight_obj: the lightweight object to dematerialize
        :return:
        """
        return self._link_delete(lightweight_obj.find_link(REL_DEMATERIALIZE))

    def reparent(self, lightweight_obj, new_parent):
        """
        Reparent lightweight object
        :param lightweight_obj: the lightweight object to reparent
        :param new_parent: the new parent
        :return:
        """
        return self._create_object_by_reference(lightweight_obj, REL_SHARED_PARENT, new_parent.reference())

    def attach_aspects(self, obj, object_aspects):
        """
        Attach aspects
        :param obj: the target system object
        :param object_aspects: aspects to attach
        :return:
        """
        return self._link_post(obj.find_link(REL_OBJECT_ASPECTS), object_aspects.representation()).resource()

    def detach(self, obj, aspect):
        """
        Detach aspect
        :param obj: the target system object
        :param aspect: aspect to detach
        :return:
        """
        self._link_delete(obj.find_link(REL_DELETE, aspect))

    def refresh(self, obj):
        """
        Refresh system object by getting it again
        :param obj: the system object
        :return: refreshed system object
        """
        return self._follow_resource_link(obj, REL_SELF)

    def update(self, sys_obj, new_sys_object):
        """
        Update system object
        :param sys_obj: the original object
        :param new_sys_object: the new object
        :return: the updated object
        """
        return self._link_post(sys_obj.find_link(REL_EDIT), data=new_sys_object.representation()).resource()

    def delete(self, obj, params=None):
        """
        Delete system object
        :param obj: the system object to delete
        :param params: URL parameters
        :return:
        """
        if obj.find_link(REL_DELETE) is not None:
            self._link_delete(obj.find_link(REL_DELETE), params=params)
        elif obj.find_link(REL_SELF) is not None:
            self._link_delete(obj.find_link(REL_SELF), params=params)
        else:
            raise Exception(
                'Object %s is not deletable as there is no link detected for the delete operation.' % obj.get(
                    'properties').get('r_object_id'))

    def follow_link(self, link):
        """
        GET request for the link href
        :param link: the link
        :return: response of GET request
        """
        return self._link_get(link, accept=MEDIA_TYPE_DM_JSON).resource()

    def previous_page(self, current_page):
        """
        Get previous page if existing
        :param current_page: current page
        :return: system objects in previous page
        """
        return self._link_get(current_page.find_link(REL_PREVIOUS)).resource()

    def next_page(self, current_page):
        """
        GET next page if existing
        :param current_page: current page
        :return: system objects in next page
        """
        return self._link_get(current_page.find_link(REL_NEXT)).resource()

    def first_page(self, current_page):
        """
        GET first page if existing
        :param current_page: current page
        :return: system objects in first page
        """
        return self._link_get(current_page.find_link(REL_FIRST)).resource()

    def last_page(self, current_page):
        """
        GET last page if exiting
        :param current_page: current page
        :return: system objects in last page
        """
        return self._link_get(current_page.find_link(REL_LAST)).resource()

    def delete_folder_recursively(self, folder):
        """
        Delete folder and its members
        :param folder: the folder to delete
        :return:
        """
        logger.info('Delete folder %s recursively.', folder.get('properties').get('object_name'))
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
        """
        GET the link href of a resource
        :param resource: the resource
        :param rel: the link relation for the target link
        :param params: URL parameters
        :return: requested resource
        """
        return self._link_get(resource.find_link(rel), params=params).resource()

    def _get_objects(self, parent, rel, params=None):
        """
        GET the link href of parent resource for system object
        :param parent: parent resource
        :param rel: link relation
        :param params: URL parameters
        :return: system objects
        """
        return self._follow_resource_link(parent, rel, params)

    def _get_repository(self):
        """
        Get repository resource specifc to the REST client
        :return: repository resource
        """
        return self._repo_resource

    def _get_object(self, parent, rel, attr_name=None, attr_value=None):
        """
        Follow link of parent resource and get the resource based on attribute value.
        For example, parent is repository resource and link relation is http://identifiers.emc.com/linkrel/users,
        it will get users of the repository resource and return the one specified by attribute value.
        :param parent: the parent resource
        :param rel: link relation
        :param attr_name: attribute name to specify object
        :param attr_value: attribute value to specify object
        :return: the object
        """
        objects = self._get_objects(parent, rel)
        return self._get_resource_via_entry(objects, attr_name, attr_value)

    def _create_object_by_representation(self, parent, rel, resource, content=None, params=None):
        """
        Create system object by POST resource representation
        :param parent: the parent resource
        :param rel: link relation
        :param resource: the resource representation
        :param content: the content
        :param params: URL parameters
        :return: created system object
        """
        if content:
            return self._link_post_multipart(parent.find_link(rel), resource.representation(), content, params=params)
        else:
            return self._link_post(parent.find_link(rel), resource.representation(), params=params)

    def _create_object_by_reference(self, parent, rel, reference, params=None):
        """
        Create system object by resource reference
        :param parent: the parent resource
        :param rel: link relation
        :param reference: the resource reference
        :param params: URL parameters
        :return: created system object
        """
        return self._link_post(parent.find_link(rel), reference, params=params)

    def _check_in(self, obj, rel, new_obj, content=None, params=None):
        """
        Check in object with different strategy
        :param obj: original object
        :param rel: link relation
        :param new_obj: new object
        :param content: the content
        :param params: URL parameters
        :return:
        """
        if new_obj and content:
            return self._link_post_multipart(obj.find_link(rel), meta=new_obj.representation(), content=content,
                                             params=params)
        elif not new_obj:
            return self._link_post(obj.find_link(rel), data=content, content_type=MEDIA_TYPE_OCTET_STREAM,
                                   params=params)
        elif not content:
            return self._link_post(obj.find_link(rel), data=new_obj.representation(), params=params)

        return None

    def _remove_member_from_group(self, group, rel, member_name):
        """
        Remove members from group
        :param group: the parent group
        :param rel: link relation for user or group member
        :param member_name: the name of the member to remove
        :return:
        """
        members_in_group = self._get_objects(group, rel)
        for member_in_group in members_in_group.get_entries():
            if member_name == member_in_group.get('title'):
                self.delete(member_in_group)

    def _link_get(self, link, accept=MEDIA_TYPE_DM_JSON, params=None):
        """
        GET the link href
        :param link: the link
        :param accept: HTTP header accept
        :param params: URL parameters
        :return: HTTP response
        """
        if link is not None:
            return link.request().auth(self._id, self._pwd).accept(
                accept).get(params=params)
        else:
            return None

    def _link_post_multipart(self, link, meta, content=None, accept=MEDIA_TYPE_DM_JSON,
                             content_type=MEDIA_TYPE_DM_JSON, params=None):
        """
        POST the link href iwht multipart
        :param link: the link
        :param meta: the meta date
        :param content: the content
        :param accept: HTTP header accept
        :param content_type: HTTP haeder content-type
        :param params: URL parameters
        :return: HTTP response
        """
        if link is not None:
            multipart = [
                ('metadata', ('', meta, MEDIA_TYPE_DM_JSON)),
                ('binary', ('', content, ''))
            ]
            return link.request().auth(self._id, self._pwd).accept(accept).as_(content_type).post(files=multipart,
                                                                                                  params=params)
        else:
            return None

    def _link_post(self, link, data, accept=MEDIA_TYPE_DM_JSON, content_type=MEDIA_TYPE_DM_JSON, params=None):
        """
        POST the link href
        :param link: the link
        :param data: requst data
        :param accept: HTTP header accept
        :param content_type: HTTP header content-type
        :param params: URL parameters
        :return: HTTP response
        """
        if link is not None:
            return link.request().auth(self._id, self._pwd).accept(accept).as_(content_type).post(data=data,
                                                                                                  params=params)
        else:
            return None

    def _link_put(self, link, data=None, accept=MEDIA_TYPE_DM_JSON, content_type=MEDIA_TYPE_DM_JSON, params=None):
        """
        PUT the link href
        :param link:
        :param data: requst data
        :param accept: HTTP header accept
        :param content_type: HTTP header content-type
        :param params: URL parameters
        :return: HTTP response
        """
        if link is not None:
            return link.request().auth(self._id, self._pwd).accept(accept).as_(content_type).put(data=data,
                                                                                                 params=params)
        else:
            return None

    def _link_delete(self, link, params=None):
        """
        DELETE the link href
        :param link: the link
        :param params: URL parameters
        :return: HTTP response
        """
        if link is not None:
            return link.request().auth(self._id, self._pwd).delete(params=params)
        else:
            return None

    def _get_resource_via_entry(self, collection, attr_name, attr_value):
        """
        GET one resource from collection by filtering with attribute
        :param collection: collection resource
        :param attr_name: attribute name to filter
        :param attr_value: attribute value to fileter
        :return:
        """
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
