import logging
import logging.config
import sys
import time
from builtins import input
from configparser import ConfigParser

from model import RestLink
from network import RestClient
from network.RestClient import MEDIA_TYPE_DM_JSON
from util import ResourceUtility

__author__ = 'wangc31'

DEMO_CABINET = 'demo-cabinet'
DEMO_NEW_FOLDER = 'demo-new-folder'
DEMO_UPDATE_FOLDER = 'demo-update-folder'
DEMO_TEMP_FOLDER = 'demo-temp-folder'
DEMO_NEW_SYSOBJECT = 'demo-new-sysobj'
DEMO_UPDATE_SYSOBJECT = 'demo-update-sysobj'
DEMO_NEW_DOCUMENT = 'demo-doc'
DEMO_CHECK_IN_WITHOUT_CONTENT = 'demo-check-in-without-content'
DEMO_CHECK_IN_WITH_CONTENT = 'demo-check-in-with-content'
DEMO_NEW_USER = 'demo-py-client-user'
DEMO_UPDATE_USER = 'demo-py-client-user-updated'
DEMO_NEW_GROUP = 'demo-py-client-group'
DEMO_ANOTHER_NEW_GROUP = 'demo-py-client-another-group'
DEMO_UPDATE_GROUP = 'demo-py-client-group-updated'
DEMO_SHARABLE_OBJECT = 'demo_sharable_obj'
DEMO_ANOTHER_SHARABLE_OBJECT = 'demo_another_sharable_obj'
DEMO_LIGHT_WEITHT_OBJECT = 'demo_lightweight_obj'
DEMO_OBJECT_TO_ATTACH = 'obj_to_attach'

VERSION_72 = '7.2'
VERSION_73 = '7.3'

SUPPORT_SINCE = 'support-since'
ITEM_NAME = 'item-name'
ITEM_CALLABLE = 'item-callable'

logger = logging.getLogger(__name__)


class RestDemo:
    def __init__(self):
        self._init_logger()

        self._init_client()

        self._init_demo_items()

    def _init_demo_items(self):
        product_info = self.client.get_product_info()

        all_items = [
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'Quit the demo', ITEM_CALLABLE: self.quit},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'Reset demo environment', ITEM_CALLABLE: self.reset_environment},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST sysObject CRUD', ITEM_CALLABLE: self.demo_sysobject_crud},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST content management',
             ITEM_CALLABLE: self.demo_content_management},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST version management',
             ITEM_CALLABLE: self.demo_version_management},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST DQL', ITEM_CALLABLE: self.demo_dql},
            {SUPPORT_SINCE: VERSION_73, ITEM_NAME: 'REST user, group and member CRUD',
             ITEM_CALLABLE: self.demo_user_group_member_crud},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST search with URL parameters ',
             ITEM_CALLABLE: self.demo_simple_search},
            {SUPPORT_SINCE: VERSION_73, ITEM_NAME: 'REST search with AQL ', ITEM_CALLABLE: self.demo_aql_search},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST formats ', ITEM_CALLABLE: self.demo_format},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST network locations ',
             ITEM_CALLABLE: self.demo_network_location},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST relation CRUD ', ITEM_CALLABLE: self.demo_relation_crud},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST folder CRUD', ITEM_CALLABLE: self.demo_folder_crud},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST type', ITEM_CALLABLE: self.demo_type},
            {SUPPORT_SINCE: VERSION_73, ITEM_NAME: 'REST value assistance', ITEM_CALLABLE: self.demo_value_assistance},
            {SUPPORT_SINCE: VERSION_73, ITEM_NAME: 'REST lightweight object',
             ITEM_CALLABLE: self.demo_lightweight_object},
            {SUPPORT_SINCE: VERSION_73, ITEM_NAME: 'REST aspect', ITEM_CALLABLE: self.demo_aspect},
            {SUPPORT_SINCE: VERSION_72, ITEM_NAME: 'REST batch', ITEM_CALLABLE: self.demo_batch}
        ]

        version = product_info.get('properties').get('major')
        if version == VERSION_73:
            print('This is Documentum REST 7.3')
            self._populate_demo_items(all_items, VERSION_72, VERSION_73)
        elif version == VERSION_72:
            print('This is Documentum REST 7.2')
            self._populate_demo_items(all_items, VERSION_72)
        else:
            logger.info('Unrecognized product version:' + version + '. Quit demo.')
            sys.exit(0)

    def _populate_demo_items(self, all_items, *versions):
        items = [item
                 for item in all_items
                 if item[SUPPORT_SINCE] in versions]
        self.choices = {i: item
                        for i, item in enumerate(items)}

    def _init_client(self):
        config_parser = ConfigParser()
        config_parser.read("resources/rest.properties")
        self.REST_URI = config_parser.get("environment", "rest.host")
        rest_uri = input("Input Documentum REST Entry Path: [default - %s]" % self.REST_URI)
        if rest_uri:
            self.REST_URI = rest_uri
        self.REST_REPOSITORY = config_parser.get("environment", "rest.repository")
        rest_repo = input("Input Repository Name: [default - %s]" % self.REST_REPOSITORY)
        if rest_repo:
            self.REST_REPOSITORY = rest_repo
        self.REST_USER = config_parser.get("environment", "rest.username")
        rest_user = input("Input User Name: [default - %s]" % self.REST_USER)
        if rest_user:
            self.REST_USER = rest_user
        self.REST_PWD = config_parser.get("environment", "rest.password")
        rest_pwd = input("Input User Password: [default - %s]" % self.REST_PWD)
        if rest_pwd:
            self.REST_PWD = rest_pwd
        self.client = RestClient.RestClient(self.REST_USER, self.REST_PWD, self.REST_URI, self.REST_REPOSITORY)

    @staticmethod
    def _init_logger():
        logging.getLogger("requests").setLevel(logging.WARNING)

        is_debug = input("Enable debugging messages (yes|no)? [default - no]")
        if is_debug == 'yes':
            level = 'DEBUG'
        else:
            level = 'INFO'
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,

            'handlers': {
                'default': {
                    'level': level,
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default'],
                    'level': 'DEBUG',
                    'propagate': True
                }
            }
        })

    @staticmethod
    def quit():
        logger.info("\nQuit the demo.")
        sys.exit(0)

    def create_demo_cabinet(self):
        logger.info("\n+++++++++++++++++++++++++++++++Create temp cabinet Start+++++++++++++++++++++++++++++++")

        self.client.create_cabinet(ResourceUtility.generate_cabinet(object_name=DEMO_CABINET))

        logger.info("+++++++++++++++++++++++++++++++Create temp cabinet End+++++++++++++++++++++++++++++++")

    def demo_user_group_member_crud(self):
        logger.info("\n+++++++++++++++++++++++++++++++User CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Create user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        new_user = self.client.create_user(ResourceUtility.generate_user(user_name=DEMO_NEW_USER,
                                                                         user_login_name=DEMO_NEW_USER))
        self.print_resource_properties(new_user, 'user_name', 'r_object_id')

        logger.info('Update user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        new_user = self.client.update(new_user, ResourceUtility.generate_user(user_login_name=DEMO_UPDATE_USER))
        self.print_resource_properties(new_user, 'user_name', 'r_object_id')

        logger.info('Refresh user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        self.client.refresh(new_user)
        self.print_resource_properties(new_user, 'user_name', 'r_object_id')

        logger.info('Get user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        new_user = self.client.get_user(DEMO_NEW_USER)
        self.print_resource_properties(new_user, 'user_name', 'r_object_id')

        logger.info("\n+++++++++++++++++++++++++++++++Group and Group Member CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Create group %s in repository %s' % (DEMO_NEW_GROUP, self.REST_REPOSITORY))
        new_group = self.client.create_group(ResourceUtility.generate_group(group_name=DEMO_NEW_GROUP))
        self.print_resource_properties(new_group, 'group_name', 'r_object_id')

        logger.info('Update group %s in repository %s' % (DEMO_NEW_GROUP, self.REST_REPOSITORY))
        new_group = self.client.update(new_group, ResourceUtility.generate_group(group_display_name=DEMO_UPDATE_USER))
        self.print_resource_properties(new_group, 'group_name', 'r_object_id')

        logger.info('Add user %s in the group %s\n' % (DEMO_NEW_USER, DEMO_NEW_GROUP))
        self.client.add_user_to_group(new_group, new_user)

        logger.info('Remove user %s in the group %s\n' % (DEMO_NEW_USER, DEMO_NEW_GROUP))
        self.client.remove_user_from_group(new_group, DEMO_NEW_USER)

        logger.info('Create another group %s in repository %s\n' % (DEMO_ANOTHER_NEW_GROUP, self.REST_REPOSITORY))
        another_new_group = self.client.create_group(
            ResourceUtility.generate_group(group_name=DEMO_ANOTHER_NEW_GROUP))

        logger.info('Add group %s in the group %s\n' % (DEMO_ANOTHER_NEW_GROUP, DEMO_NEW_GROUP))
        self.client.add_group_to_group(new_group, another_new_group)

        logger.info('Remove group %s in the group %s\n' % (DEMO_ANOTHER_NEW_GROUP, DEMO_NEW_GROUP))
        self.client.remove_group_from_group(new_group, DEMO_ANOTHER_NEW_GROUP)

        logger.info('Delete user %s in repository %s\n' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        self.client.delete(new_user)

        logger.info('Delete group %s in repository %s\n' % (DEMO_NEW_GROUP, self.REST_REPOSITORY))
        self.client.delete(new_group)

        logger.info('Delete group %s in repository %s\n' % (DEMO_ANOTHER_NEW_GROUP, self.REST_REPOSITORY))
        self.client.delete(another_new_group)

    def demo_folder_crud(self):
        logger.info("\n+++++++++++++++++++++++++++++++Folder CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create new folder %s in cabinet %s...' % (DEMO_NEW_FOLDER, DEMO_CABINET))
        new_folder = self.client.create_folder(cabinet, ResourceUtility.generate_folder(object_name=DEMO_NEW_FOLDER))
        self.print_resource_properties(new_folder, 'object_name', 'r_object_id')

        logger.info('Update folder %s in cabinet %s...' % (DEMO_NEW_FOLDER, DEMO_CABINET))
        new_folder = self.client.update(new_folder, ResourceUtility.generate_folder(object_name=DEMO_UPDATE_FOLDER))
        self.print_resource_properties(new_folder, 'object_name', 'r_object_id')

        logger.info('Get folder %s in cabinet %s...' % (DEMO_UPDATE_FOLDER, DEMO_CABINET))
        new_folder = self.client.get_folder(cabinet, DEMO_UPDATE_FOLDER)
        self.print_resource_properties(new_folder, 'object_name', 'r_object_id')

        logger.info('Delete folder %s' % DEMO_UPDATE_FOLDER)
        self.client.delete(new_folder)

        logger.info("+++++++++++++++++++++++++++++++Folder CRUD End+++++++++++++++++++++++++++++++")

    def demo_sysobject_crud(self):
        logger.info("\n+++++++++++++++++++++++++++++++Object CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create temp folder %s in cabinet %s...' % (DEMO_TEMP_FOLDER, DEMO_CABINET))
        temp_folder = self.client.create_folder(cabinet, ResourceUtility.generate_folder(object_name=DEMO_TEMP_FOLDER))
        self.print_resource_properties(temp_folder, 'object_name', 'r_object_id')

        logger.info('Create new sysobject %s in folder %s...' % (DEMO_NEW_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.create_sysobj(temp_folder,
                                               ResourceUtility.generate_sysobject(object_name=DEMO_NEW_SYSOBJECT))
        self.print_resource_properties(new_sysobj, 'object_name', 'r_object_id')

        logger.info('Update sysobject %s in folder %s...' % (DEMO_UPDATE_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.update(new_sysobj,
                                        ResourceUtility.generate_sysobject(object_name=DEMO_UPDATE_SYSOBJECT))
        self.print_resource_properties(new_sysobj, 'object_name', 'r_object_id')

        logger.info('Refresh sysobject %s in folder %s...' % (DEMO_UPDATE_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.refresh(new_sysobj)
        self.print_resource_properties(new_sysobj, 'object_name', 'r_object_id')

        logger.info('Get sysobject %s in folder %s...' % (DEMO_UPDATE_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.get_sysobject(temp_folder, DEMO_UPDATE_SYSOBJECT)
        self.print_resource_properties(new_sysobj, 'object_name', 'r_object_id')

        logger.info('Delete sysobject %s' % DEMO_UPDATE_SYSOBJECT)
        self.client.delete(new_sysobj)

        logger.info('Delete folder %s' % DEMO_TEMP_FOLDER)
        self.client.delete(temp_folder)

        logger.info("+++++++++++++++++++++++++++++++Object CRUD End+++++++++++++++++++++++++++++++")

    def demo_content_management(self):
        logger.info("\n+++++++++++++++++++++++++++++++Content Management Start+++++++++++++++++++++++++++++++")

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create temp folder %s in cabinet %s...' % (DEMO_TEMP_FOLDER, DEMO_CABINET))
        temp_folder = self.client.create_folder(cabinet, ResourceUtility.generate_folder(object_name=DEMO_TEMP_FOLDER))

        logger.info('Create new document %s with content...' % DEMO_NEW_DOCUMENT)
        new_doc = self.client.create_document(temp_folder,
                                              ResourceUtility.generate_document(object_name=DEMO_NEW_DOCUMENT),
                                              'It\'s created by python client', params={'format': 'crtext'})
        self.print_resource_properties(new_doc, 'object_name', 'r_object_id')

        logger.info('Get primary content of %s...' % DEMO_NEW_DOCUMENT)
        primary_content = self.client.get_primary_content(new_doc, params={'media-url-policy': 'all'})
        self.print_resource_properties(primary_content, 'object_name', 'r_object_id', 'format_name',
                                       'full_content_size')

        logger.info('All media URLs for primary content of %s...' % DEMO_NEW_DOCUMENT)
        for link in primary_content.all_links():
            logger.info(str(link) + '\n')

        logger.info('Create new html rendition for document %s...' % DEMO_NEW_DOCUMENT)
        new_content = self.client.create_content(new_doc, content='This is html rendition.', content_type='text/html',
                                                 params={'primary': 'false'})
        self.print_resource_properties(new_content, 'object_name', 'r_object_id', 'format_name', 'full_content_size')

        logger.info('Create new rendition with large file for document %s...' % DEMO_NEW_DOCUMENT)
        path = input('Input the file path. Press \'Enter\' directly to skip uploading file:\n')
        if path:
            try:
                with open(path, 'rb') as f:
                    new_content = self.client.create_content(new_doc, content=f,
                                                             content_type=RestClient.MEDIA_TYPE_OCTET_STREAM,
                                                             params={'primary': 'false'})
                    self.print_resource_properties(new_content, 'object_name', 'r_object_id', 'format_name',
                                                   'full_content_size')
            except IOError:
                logger.info('The file %s does not exist or can not be opened.' % path)
        else:
            logger.info('Skip create new rendition with large file for document %s...' % DEMO_NEW_DOCUMENT)

        logger.info('Get contents for document %s...' % DEMO_NEW_DOCUMENT)
        contents = self.client.get_contents(new_doc)

        logger.info('All renditions for document %s...' % DEMO_NEW_DOCUMENT)
        for rendition in contents.get_entries():
            logger.info(str(rendition.get('content')) + '\n')

        logger.info('Delete document %s' % DEMO_NEW_DOCUMENT)
        self.client.delete(new_doc)

        logger.info('Delete folder %s' % DEMO_TEMP_FOLDER)
        self.client.delete(temp_folder)

        logger.info("+++++++++++++++++++++++++++++++Content Management End+++++++++++++++++++++++++++++++")

    def demo_version_management(self):
        logger.info("\n+++++++++++++++++++++++++++++++Version Management Start+++++++++++++++++++++++++++++++")

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create temp folder %s in cabinet %s...' % (DEMO_TEMP_FOLDER, DEMO_CABINET))
        temp_folder = self.client.create_folder(cabinet, ResourceUtility.generate_folder(object_name=DEMO_TEMP_FOLDER))

        logger.info('Create new document %s with content...' % DEMO_NEW_DOCUMENT)
        doc = self.client.create_document(temp_folder, ResourceUtility.generate_document(object_name=DEMO_NEW_DOCUMENT))
        self.print_resource_properties(doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check out document...')
        doc = self.client.check_out(doc)
        self.print_resource_properties(doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Cancel check out')
        self.client.cancel_check_out(doc)

        logger.info('Refresh document...')
        doc = self.client.refresh(doc)
        self.print_resource_properties(doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check out document...')
        doc = self.client.check_out(doc)
        self.print_resource_properties(doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check in minor with new name...')
        doc = self.client.check_in_minor(doc,
                                         ResourceUtility.generate_document(object_name=DEMO_CHECK_IN_WITHOUT_CONTENT))
        self.print_resource_properties(doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check out document...')
        doc = self.client.check_out(doc)
        self.print_resource_properties(doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check in minor with content')
        doc = self.client.check_in_minor(doc, new_obj=None, content='I am new content.')
        self.print_resource_properties(doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check out document...')
        doc = self.client.check_out(doc)
        self.print_resource_properties(doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check in major with new name and content')
        doc = self.client.check_in_major(doc,
                                         new_obj=ResourceUtility.generate_document(
                                             object_name=DEMO_CHECK_IN_WITH_CONTENT),
                                         content='I am new content again.')
        self.print_resource_properties(doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Delete document %s' % DEMO_NEW_DOCUMENT)
        self.client.delete(doc, {'del-version': 'all'})

        logger.info('Delete folder %s' % DEMO_TEMP_FOLDER)
        self.client.delete(temp_folder)

        logger.info("+++++++++++++++++++++++++++++++Version Management End+++++++++++++++++++++++++++++++")

    def demo_batch(self):
        logger.info("\n+++++++++++++++++++++++++++++++Batch Start+++++++++++++++++++++++++++++++")

        batch_caps = self.client.get_batch_capabilities()

        logger.info("\nBatchable resource:")
        for batchable in batch_caps.get('batchable-resources'):
            logger.info("  " + batchable)

        logger.info("\nNon-batchable resource:")
        for non_batchable in batch_caps.get('non-batchable-resources'):
            logger.info("  " + non_batchable)

        logger.info("\nsequence: " + batch_caps.get("sequence"))
        logger.info("\ntransactions: " + batch_caps.get("transactions"))

        cabinets_uri = self.client.get_cabinets().find_link(RestLink.REL_SELF).href
        operation_1 = ResourceUtility.generate_batch_operation('id1', 'get cabinets', cabinets_uri, 'GET',
                                                               Accept=MEDIA_TYPE_DM_JSON)

        users_uri = self.client.get_users(self.client.get_current_repository()).find_link(RestLink.REL_SELF).href
        operation_2 = ResourceUtility.generate_batch_operation('id2', 'get users', users_uri, 'GET',
                                                               Accept=MEDIA_TYPE_DM_JSON)

        cabinet_uri = self.client.get_cabinet(DEMO_CABINET).find_link(RestLink.REL_SELF).href
        operation_3 = ResourceUtility.generate_batch_operation('id3', 'get cabinet', cabinet_uri, 'GET',
                                                               Accept=MEDIA_TYPE_DM_JSON)

        cabinet_folders_uri = self.client.get_cabinet(DEMO_CABINET).find_link(RestLink.REL_FOLDERS).href
        operation_4 = ResourceUtility.generate_batch_operation('id4', 'create folder in cabinet', cabinet_folders_uri,
                                                               'POST',
                                                               entity=ResourceUtility.generate_folder(
                                                                   object_name='folder for batch').representation(),
                                                               Accept=MEDIA_TYPE_DM_JSON)

        batch = ResourceUtility.generate_batch_request(operation_1, operation_2, operation_3, operation_4)
        logger.info("\nCreate batch:\n")
        for operation in batch.get('operations'):
            logger.info("------------------")
            print_properties(operation, 'id', 'description')
            print_properties(operation.get('request'), 'method', 'uri')

        batch_results = self.client.create_batch(batch)
        logger.info("\nThe batch results:\n")
        for result in batch_results.get('operations'):
            logger.info("------------------")
            print_properties(result, 'id', 'description', 'state')

        logger.info("\n+++++++++++++++++++++++++++++++Batch End+++++++++++++++++++++++++++++++")

    def demo_dql(self):
        logger.info("\n+++++++++++++++++++++++++++++++DQL Start+++++++++++++++++++++++++++++++")

        logger.info('Query \'select * from dm_user\' with items-per-page=3,page=2...')
        results = self.client.dql('select * from dm_user', {'items-per-page': '2', 'page': '2'})

        logger.info('Object names in page %d...', 2)
        for result in results.get_entries():
            logger.info(result.get('content').get('properties').get('user_name'))
        logger.info('')

        logger.info('Navigate to next page...')
        results = self.client.next_page(results)

        if results is None:
            logger.info('Next page does not exist.')
        else:
            logger.info('Object names in page %d...', 3)
            for result in results.get_entries():
                logger.info(result.get('content').get('properties').get('user_name'))

        logger.info("+++++++++++++++++++++++++++++++DQL End+++++++++++++++++++++++++++++++")

    def demo_simple_search(self):
        logger.info("\n+++++++++++++++++++++++++++++++Simple Search Start+++++++++++++++++++++++++++++++")

        logger.info('Simple search with keyword emc and parameters items-per-page=3,page=2,inline=true...')
        results = self.client.simple_search('emc', {'items-per-page': '2', 'page': '1', 'inline': 'true'})

        logger.info('Object names in page %d...', 2)
        for result in results.get_entries():
            logger.info(result.get('content').get('properties').get('object_name'))

        logger.info('Navigate to next page...')
        results = self.client.next_page(results)

        if results is None:
            logger.info('Next page does not exist.')
        else:
            logger.info('Object names in page %d...', 3)
            for result in results.get_entries():
                logger.info(result.get('content').get('properties').get('object_name'))

        logger.info("+++++++++++++++++++++++++++++++Simple Search End+++++++++++++++++++++++++++++++")

    def demo_aql_search(self):
        logger.info("\n+++++++++++++++++++++++++++++++AQL Search Start+++++++++++++++++++++++++++++++")

        logger.info('AQL search for keyword emc and parameters items-per-page=3,page=2,inline=true...')
        results = []
        try:
            with open("resources/aql.json", 'rb') as f:
                results = self.client.aql_search(f, {'items-per-page': '2', 'page': '1', 'inline': 'true'})
        except IOError:
            logger.info('Fail to search with AQL.')

        logger.info('Object names in page %d...', 2)
        for result in results.get_entries():
            logger.info(result.get('content').get('properties').get('object_name'))

        logger.info('Navigate to next page...')
        results = self.client.next_page(results)

        if results is None:
            logger.info('Next page does not exist.')
        else:
            logger.info('Object names in page %d...', 3)
            for result in results.get_entries():
                logger.info(result.get('content').get('properties').get('object_name'))

        logger.info("\n+++++++++++++++++++++++++++++++AQL Search End+++++++++++++++++++++++++++++++")

    def demo_type(self):
        logger.info("\n+++++++++++++++++++++++++++++++Type Start+++++++++++++++++++++++++++++++")

        logger.info('Get types resource...')
        dm_types = self.client.get_types()

        if len(dm_types.get_entries()) > 0:
            logger.info('Types are \n')
            for dm_type in dm_types.get_entries():
                logger.info(dm_type.get('title'))

        logger.info('\nGet single dm_document type resource...')
        dm_type = self.client.get_type('dm_document')
        logger.info('Type name: %s, Type label: %s, Type category: %s', dm_type.get('name'), dm_type.get('label'),
                    dm_type.get('category'))

        logger.info("\n+++++++++++++++++++++++++++++++Type End+++++++++++++++++++++++++++++++")

    def demo_value_assistance(self):
        logger.info("\n+++++++++++++++++++++++++++++++Value Assistance Start+++++++++++++++++++++++++++++++")

        logger.info('Get the value assistance of the type...')
        dm_type_str = input(
            'Input the type name with fixed value assistance list. Press \'Enter\' directly to skip.\n')
        if dm_type_str:
            dm_type = self.client.get_type(dm_type_str)

            if dm_type:
                included_property = input(
                    'Input attribute name of %s with fixed value assistance list. Press \'Enter\' directly to skip.\n'
                    % dm_type_str)

                value_assistance = self.client.get_value_assistance(dm_type,
                                                                    ResourceUtility.generate_assist_value_request(),
                                                                    included_property)
                for va in value_assistance.get('properties').items():
                    logger.info('Attribute %s allow-user-values: %s' % (va[0], va[1].get('allow-user-values')))

                    for value in va[1].get('values'):
                        logger.info('Allowed value is %s, label is %s' % (value.get('value'), value.get('label')))

            else:
                logger.info('Skip get value assistance as type specified does not exist.')
        else:
            logger.info('Skip get value assistance.')

        # E.G. city_type.city depends on city_type.country
        # country China has cities Shanghai, Beijing, Chongqing, Grangzhou, Shenzhen and Tianjing
        dm_type_str = input(
            '\nInput the type name with value assistance dependencies. Press \'Enter\' directly to skip.\n')
        if dm_type_str:
            dm_type = self.client.get_type(dm_type_str)

            for attr in dm_type.get('properties'):
                logger.info('Attribute %s.%s has dependency %s' % (
                    dm_type.get('name'), attr.get('name'), attr.get('dependencies')))

            attr_name = input('Input the attribute name of %s which has dependencies:' % dm_type_str)
            dependency_attr_name = input('Input the dependency name of %s.%s:\n' % (dm_type_str, attr_name))
            dependency_attr_value = input('Input the dependency value of attribute %s:\n' % dependency_attr_name)

            properties = {dependency_attr_name: dependency_attr_value}
            value_assistance = self.client.get_value_assistance(dm_type,
                                                                ResourceUtility.generate_assist_value_request(
                                                                    **properties),
                                                                attr_name)

            logger.info('Attribute %s.%s allows values:' % (dm_type_str, attr_name))
            for value in value_assistance.get('properties').get('city').get('values'):
                logger.info('%s, label: %s' % (value.get('value'), value.get('label')))
        else:
            logger.info('Skip get value assistance dependencies.')

        logger.info("\n+++++++++++++++++++++++++++++++Value Assistance End+++++++++++++++++++++++++++++++")

    def demo_relation_crud(self):
        logger.info("\n+++++++++++++++++++++++++++++++Relation CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Get relations in repository %s...' % self.REST_REPOSITORY)
        self.client.get_relations()

        logger.info('Create relation in repository %s...' % self.REST_REPOSITORY)

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create new sysobject as relation parent...')
        parent = self.client.create_sysobj(cabinet,
                                           ResourceUtility.generate_sysobject(object_name='relation-parent'))
        self.print_resource_properties(parent, 'object_name', 'r_object_id')

        logger.info('Create new sysobject as relation child...')
        child = self.client.create_sysobj(cabinet,
                                          ResourceUtility.generate_sysobject(object_name='relation-child'))
        self.print_resource_properties(child, 'object_name', 'r_object_id')

        logger.info('Create new relation...')
        new_relation = self.client.create_relation(ResourceUtility.generate_relation(relation_name='peer',
                                                                                     parent_id=parent.get(
                                                                                         'properties').get(
                                                                                         'r_object_id'),
                                                                                     child_id=child.get(
                                                                                         'properties').get(
                                                                                         'r_object_id'),
                                                                                     ))
        self.print_resource_properties(new_relation, 'object_name', 'r_object_id')

        logger.info('Delete the new relation...')
        self.client.delete(new_relation)

        logger.info('Get relation types...')
        relation_types = self.client.get_relation_types()

        if len(relation_types.get_entries()) > 0:
            logger.info('Types are \n')
            for relation_type in relation_types.get_entries():
                logger.info(relation_type.get('title'))

        if len(relation_types.get_entries()) > 0:
            logger.info('Get relation type resource...')
            title = relation_types.get_entry(0).get('title')
            relation_type = self.client.get_relation_type(title)
            logger.info('The relation type %s is returned; \nits link is %s',
                        relation_type.get('properties').get('relation_name'),
                        relation_type.find_link(RestLink.REL_SELF).href)

        logger.info("\n+++++++++++++++++++++++++++++++Relation CRUD End+++++++++++++++++++++++++++++++")

    def demo_format(self):
        logger.info("\n+++++++++++++++++++++++++++++++Format CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Get formats in repository %s...' % self.REST_REPOSITORY)
        formats = self.client.get_formats({'items-per-page': 5})

        if len(formats.get_entries()) > 0:
            logger.info('Formats are \n')
            for dm_format in formats.get_entries():
                logger.info(dm_format.get('title'))

        if len(formats.get_entries()) > 0:
            logger.info('\nGet single format in repository %s...' % self.REST_REPOSITORY)
            title = formats.get_entry(0).get('title')
            dm_format = self.client.get_format(title)
            logger.info('The format name is %s, description is %s', dm_format.get('properties').get('name'),
                        dm_format.get('properties').get('description'))

        logger.info("\n+++++++++++++++++++++++++++++++Format CRUD End+++++++++++++++++++++++++++++++")

    def demo_network_location(self):
        logger.info("\n+++++++++++++++++++++++++++++++Network location Start+++++++++++++++++++++++++++++++")

        logger.info('Get network locations in repository %s...' % self.REST_REPOSITORY)
        locations = self.client.get_network_locations()

        if len(locations.get_entries()) > 0:
            logger.info('Locations are \n')
            for location in locations.get_entries():
                logger.info(location.get('title'))

        if len(locations.get_entries()) > 0:
            logger.info('Get single network location in repository %s...' % self.REST_REPOSITORY)
            title = locations.get_entry(0).get('title')
            location = self.client.get_network_location(title)
            logger.info('The single network location %s is returned; \nits link is %s',
                        location.get('properties').get('object_name'), location.find_link(RestLink.REL_SELF).href)

        logger.info("\n+++++++++++++++++++++++++++++++Network location End+++++++++++++++++++++++++++++++")

    def demo_lightweight_object(self):
        logger.info(
            "\n+++++++++++++++++++++++++++++++Lightweight object Start+++++++++++++++++++++++++++++++")

        sharable_types = self.client.get_types({'filter': 'type_category=2'})
        logger.info('\nSharable types:')
        for entry in sharable_types.get_entries():
            logger.info(entry.get('title'))

        lightweight_types = self.client.get_types({'filter': 'type_category=4'})
        logger.info('\nLightweight types:')
        for entry in lightweight_types.get_entries():
            logger.info(entry.get('title'))

        cabinet = self.client.get_cabinet(DEMO_CABINET)

        sharable_type = input('\nInput the sharable type. Press \'Enter\' directly to skip.\n')
        if not sharable_type:
            logger.info('Skip lightweight object demo.')
        else:
            logger.info('Create object %s of sharable type %s...' % (DEMO_SHARABLE_OBJECT, sharable_type))
            sharable_obj = self.client.create_sysobj(cabinet,
                                                     ResourceUtility.generate_sysobject(
                                                         sharable_type,
                                                         object_name=DEMO_SHARABLE_OBJECT,
                                                         title='demo_sharable_type'))

            lightweight_type = input('\nInput the lightweight type:\n')
            logger.info('Create object %s of lightweight type %s...' % (DEMO_LIGHT_WEITHT_OBJECT, lightweight_type))
            lw_obj = self.client.create_sysobj(sharable_obj,
                                               ResourceUtility.generate_sysobject(lightweight_type,
                                                                                  object_name=DEMO_LIGHT_WEITHT_OBJECT),
                                               RestLink.REL_LIGHTWEIGHT_OBJECTS)

            logger.info('Materialize the lightweight object %s...\n' % lw_obj.get('properties').get('object_name'))
            materialized_object = self.client.materialize(lw_obj)

            if materialized_object.find_link(RestLink.REL_DEMATERIALIZE) is not None:
                logger.info('Materializing succeeds...\n')

            logger.info('Dematerialize the lightweight object %s...\n' % lw_obj.get('properties').get('object_name'))
            self.client.dematerialize(materialized_object)

            lw_obj = self.client.refresh(lw_obj)
            if lw_obj.find_link(RestLink.REL_MATERIALIZE) is not None:
                logger.info('Dematerializing succeeds...\n')

            logger.info(
                'Create another object %s of sharable type %s...\n' % (DEMO_ANOTHER_SHARABLE_OBJECT, sharable_type))
            another_sharable_obj = self.client \
                .create_sysobj(cabinet,
                               ResourceUtility.generate_sysobject(sharable_type,
                                                                  object_name=DEMO_ANOTHER_SHARABLE_OBJECT,
                                                                  title='demo_sharable_type'))

            logger.info('Reparent the lightweight object %s to the new sharable object %s...\n' % (
                lw_obj.get('properties').get('object_name'),
                another_sharable_obj.get('properties').get('object_name')))
            self.client.reparent(lw_obj, another_sharable_obj)

            new_parent = self.client.get_sharable_parent(lw_obj)
            if new_parent.get('properties').get('r_object_id') == another_sharable_obj.get('properties').get(
                    'r_object_id'):
                logger.info('Reparent succeeds...\n')

            self.client.delete(lw_obj)
            self.client.delete(sharable_obj)
            self.client.delete(another_sharable_obj)

        logger.info("\n+++++++++++++++++++++++++++++++Lightweight object End+++++++++++++++++++++++++++++++")

    def demo_aspect(self):
        logger.info("\n+++++++++++++++++++++++++++++++Aspect Start+++++++++++++++++++++++++++++++")

        logger.info('Get all aspects...')
        aspects = self.client.get_aspects()
        for entry in aspects.get_entries():
            logger.info('Aspect name: %s', entry.get('title'))

        aspect_type = input('\nInput the aspect type to attach... Press \'Enter\' directly to skip.\n')

        if aspect_type:
            cabinet = self.client.get_cabinet(DEMO_CABINET)

            logger.info('Create object %s to attach aspect...', DEMO_OBJECT_TO_ATTACH)
            obj = self.client.create_sysobj(cabinet,
                                            ResourceUtility.generate_sysobject(
                                                object_name=DEMO_OBJECT_TO_ATTACH))

            logger.info('Attaching aspect %s to object %s...' % (aspect_type, obj.get('properties').get('object_name')))
            object_aspects = self.client.attach_aspects(obj, ResourceUtility.generate_object_aspects(aspect_type))
            logger.info('Aspects %s attached...' % object_aspects.get('aspects'))

            logger.info('Detach aspect %s... ' % aspect_type)
            self.client.detach(object_aspects, aspect_type)
            object_aspects = self.client.refresh(object_aspects)
            logger.info('Aspects %s attached...' % object_aspects.get('aspects'))

            self.client.delete(obj)
        else:
            logger.info('Skip aspect demo.')

        logger.info("\n+++++++++++++++++++++++++++++++Aspect End+++++++++++++++++++++++++++++++")

    def clean_demo_cabinet(self):
        logger.info("\n+++++++++++++++++++++++++++++++Delete demo cabinet Start+++++++++++++++++++++++++++++++")
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        if cabinet is not None:
            logger.info('Deleting cabinet %s.', DEMO_CABINET)
            self.client.delete_folder_recursively(cabinet)
        else:
            logger.info('Cabinet %s does not exist.', DEMO_CABINET)

        logger.info("+++++++++++++++++++++++++++++++Delete demo cabinet End+++++++++++++++++++++++++++++++")

    def clean_demo_user_group(self):
        logger.info("+++++++++++++++++++++++++++++++Delete demo users/groups Start+++++++++++++++++++++++++++++++")

        user = self.client.get_user(DEMO_NEW_USER)
        if user is not None:
            logger.info('Delete user %s...' % DEMO_NEW_USER)
            self.client.delete(user)
        else:
            logger.info('User %s does not exist.', DEMO_NEW_USER)

        group = self.client.get_group(DEMO_NEW_GROUP)
        if group is not None:
            logger.info('Delete group %s...' % DEMO_NEW_GROUP)
            self.client.delete(group)
        else:
            logger.info('Group %s does not exist.', DEMO_NEW_GROUP)

        group = self.client.get_group(DEMO_ANOTHER_NEW_GROUP)
        if group is not None:
            logger.info('Delete group %s...' % DEMO_ANOTHER_NEW_GROUP)
            self.client.delete(group)
        else:
            logger.info('Group %s does not exist.', DEMO_ANOTHER_NEW_GROUP)
        logger.info("+++++++++++++++++++++++++++++++Delete demo users/groups End+++++++++++++++++++++++++++++++")

    def prepare_env(self):
        self.reset_environment()
        self.create_demo_cabinet()

    def reset_environment(self):
        logger.info("\n+++++++++++++++++++++++++++++++Reset Environment Start+++++++++++++++++++++++++++++++")

        self.clean_demo_cabinet()
        self.clean_demo_user_group()

        logger.info("+++++++++++++++++++++++++++++++Reset Environment End+++++++++++++++++++++++++++++++")

    @staticmethod
    def print_resource_properties(res, *properties):
        print_properties(res.get('properties'), *properties)

    def demo_all(self):
        self.demo_folder_crud()
        self.demo_sysobject_crud()
        self.demo_content_management()
        self.demo_version_management()
        self.demo_dql()
        self.demo_user_group_member_crud()

    def demo(self):

        while True:
            try:
                for k, v in self.choices.items():
                    print("%d. %s" % (k, v[ITEM_NAME]))

                user_choice = int(input("\nWhat's your choice?\n"))

                if user_choice not in self.choices:
                    print('#Invalid choice!#\n')
                    continue

                self.prepare_env()
                self.choices[user_choice][ITEM_CALLABLE]()
                self.reset_environment()
                time.sleep(1)
            except ValueError:
                print("\n#Enter number of the demo items instead of other characters.#\n")
            except Exception as e:
                logger.exception(e)
                time.sleep(1)
                print("\n#Error is detected during demo. Please refer the log for the exception detail.#\n")


def print_properties(prop_collection, *properties):
    info = []
    for prop in properties:
        info.append('%s: %s' % (prop, prop_collection.get(prop)))
    logger.info('>%s\n', ", ".join(info))


def main():
    RestDemo().demo()


if __name__ == '__main__':
    main()
else:
    logger.info('RestDemo as a module')
