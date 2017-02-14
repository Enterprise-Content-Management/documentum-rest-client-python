import collections
import inspect
import json
import logging
import logging.config
import sys
import time

from builtins import input
from configparser import ConfigParser

from model import RestLink
from model.QueryDocument import Sort, ExpSet, FtExp, FacetDefinition
from network import RestClient
from network.RestClient import MEDIA_TYPE_DM_JSON
from util import ResourceUtility
from util.DemoUtil import print_resource_properties
from util.DemoUtil import print_properties
from util.DemoUtil import prompt_user
from util.DemoUtil import format_json

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

logger = logging.getLogger(__name__)

Demo = collections.namedtuple('Demo', ['version', 'description', 'callable'])


class RestDemo:
    def __init__(self, prompt_func):
        self.prompt_func = prompt_func

        self._init_logger()

        self._init_client()

        self._init_demo_items()

    def _init_demo_items(self):

        try:
            demos = tuple(
                Demo(self._get_method_version(method), self._get_method_doc(method), method) for name, method in
                (inspect.getmembers(self, predicate=inspect.ismethod))
                if str(name).startswith('demo'))

            product_version = float(self.client.get_product_info().get('properties').get('major'))

            print('This is Documentum REST {}'.format(product_version))
            self._populate_demo_items(demos, product_version)
        except Exception as e:
            logger.info('Error occurs... Quit demo.\n{}'.format(e))
            sys.exit(0)

    @staticmethod
    def _get_method_version(demo):
        return inspect.getdoc(demo).split('\n')[1].split(':')[1].strip()

    @staticmethod
    def _get_method_doc(demo):
        return inspect.getdoc(demo).split('\n')[0]

    def _populate_demo_items(self, demos, product_version):
        items = [demo
                 for demo in demos
                 if float(demo.version) <= product_version]

        # hardcode quit and reset at the top
        items.insert(0, Demo(self._get_method_version(self.quit), self._get_method_doc(self.quit), self.quit))
        items.insert(1, Demo(self._get_method_version(self.reset_environment),
                             self._get_method_doc(self.reset_environment), self.reset_environment))

        self.choices = {i: item
                        for i, item in enumerate(items)}

    def _init_client(self):
        config_parser = ConfigParser()
        config_parser.read("resources/rest.properties")

        self.REST_URI = config_parser.get("environment", "rest.host")
        rest_uri = self.prompt_func("Input Documentum REST Entry Path: [default - %s]" % self.REST_URI)
        if rest_uri:
            self.REST_URI = rest_uri

        self.REST_REPOSITORY = config_parser.get("environment", "rest.repository")
        rest_repo = self.prompt_func("Input Repository Name: [default - %s]" % self.REST_REPOSITORY)
        if rest_repo:
            self.REST_REPOSITORY = rest_repo

        self.REST_USER = config_parser.get("environment", "rest.username")
        rest_user = self.prompt_func("Input User Name: [default - %s]" % self.REST_USER)
        if rest_user:
            self.REST_USER = rest_user

        self.REST_PWD = config_parser.get("environment", "rest.password")
        rest_pwd = self.prompt_func("Input User Password: [default - %s]" % self.REST_PWD)
        if rest_pwd:
            self.REST_PWD = rest_pwd

        self.client = RestClient.RestClient(self.REST_USER, self.REST_PWD, self.REST_URI, self.REST_REPOSITORY)

    def _init_logger(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

        is_debug = self.prompt_func("Enable debugging messages (yes|no)? [default - no]")
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
        """Quit the demo
        version: 7.2"""

        logger.info("\nQuit the demo.")
        sys.exit(0)

    def create_demo_cabinet(self):
        logger.debug("\n+++++++++++++++++++++++++++++++Create temp cabinet Start+++++++++++++++++++++++++++++++")

        self.client.create_cabinet(ResourceUtility.generate_cabinet(object_name=DEMO_CABINET))

        logger.debug("+++++++++++++++++++++++++++++++Create temp cabinet End+++++++++++++++++++++++++++++++")

    def demo_user_group_member_crud(self):
        """
        REST user, group and member CRUD
        version:7.3
        """
        logger.info("\n+++++++++++++++++++++++++++++++User CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Create user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        new_user = self.client.create_user(ResourceUtility.generate_user(user_name=DEMO_NEW_USER,
                                                                         user_login_name=DEMO_NEW_USER))
        print_resource_properties(logger, new_user, 'user_name', 'r_object_id')

        logger.info('Update user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        new_user = self.client.update(new_user, ResourceUtility.generate_user(user_login_name=DEMO_UPDATE_USER))
        print_resource_properties(logger, new_user, 'user_name', 'r_object_id')

        logger.info('Refresh user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        self.client.refresh(new_user)
        print_resource_properties(logger, new_user, 'user_name', 'r_object_id')

        logger.info('Get user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        new_user = self.client.get_user(DEMO_NEW_USER)
        print_resource_properties(logger, new_user, 'user_name', 'r_object_id')

        logger.info("\n+++++++++++++++++++++++++++++++Group and Group Member CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Create group %s in repository %s' % (DEMO_NEW_GROUP, self.REST_REPOSITORY))
        new_group = self.client.create_group(ResourceUtility.generate_group(group_name=DEMO_NEW_GROUP))
        print_resource_properties(logger, new_group, 'group_name', 'r_object_id')

        logger.info('Update group %s in repository %s' % (DEMO_NEW_GROUP, self.REST_REPOSITORY))
        new_group = self.client.update(new_group, ResourceUtility.generate_group(group_display_name=DEMO_UPDATE_USER))
        print_resource_properties(logger, new_group, 'group_name', 'r_object_id')

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
        """
        REST folder CRUD
        version:7.2
        """
        logger.info("\n+++++++++++++++++++++++++++++++Folder CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create new folder %s in cabinet %s...' % (DEMO_NEW_FOLDER, DEMO_CABINET))
        new_folder = self.client.create_folder(cabinet, ResourceUtility.generate_folder(object_name=DEMO_NEW_FOLDER))
        print_resource_properties(logger, new_folder, 'object_name', 'r_object_id')

        logger.info('Update folder %s in cabinet %s...' % (DEMO_NEW_FOLDER, DEMO_CABINET))
        new_folder = self.client.update(new_folder, ResourceUtility.generate_folder(object_name=DEMO_UPDATE_FOLDER))
        print_resource_properties(logger, new_folder, 'object_name', 'r_object_id')

        logger.info('Get folder %s in cabinet %s...' % (DEMO_UPDATE_FOLDER, DEMO_CABINET))
        new_folder = self.client.get_folder(cabinet, DEMO_UPDATE_FOLDER)
        print_resource_properties(logger, new_folder, 'object_name', 'r_object_id')

        logger.info('Delete folder %s' % DEMO_UPDATE_FOLDER)
        self.client.delete(new_folder)

        logger.info("+++++++++++++++++++++++++++++++Folder CRUD End+++++++++++++++++++++++++++++++")

    def demo_sysobject_crud(self):
        """
        REST sysObject CRUD
        version: 7.2
        """
        logger.info("\n+++++++++++++++++++++++++++++++Object CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create temp folder %s in cabinet %s...' % (DEMO_TEMP_FOLDER, DEMO_CABINET))
        temp_folder = self.client.create_folder(cabinet, ResourceUtility.generate_folder(object_name=DEMO_TEMP_FOLDER))
        print_resource_properties(logger, temp_folder, 'object_name', 'r_object_id')

        logger.info('Create new sysobject %s in folder %s...' % (DEMO_NEW_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.create_sysobj(temp_folder,
                                               ResourceUtility.generate_sysobject(object_name=DEMO_NEW_SYSOBJECT))
        print_resource_properties(logger, new_sysobj, 'object_name', 'r_object_id')

        logger.info('Update sysobject %s in folder %s...' % (DEMO_UPDATE_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.update(new_sysobj,
                                        ResourceUtility.generate_sysobject(object_name=DEMO_UPDATE_SYSOBJECT))
        print_resource_properties(logger, new_sysobj, 'object_name', 'r_object_id')

        logger.info('Refresh sysobject %s in folder %s...' % (DEMO_UPDATE_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.refresh(new_sysobj)
        print_resource_properties(logger, new_sysobj, 'object_name', 'r_object_id')

        logger.info('Get sysobject %s in folder %s...' % (DEMO_UPDATE_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.get_sysobject(temp_folder, DEMO_UPDATE_SYSOBJECT)
        print_resource_properties(logger, new_sysobj, 'object_name', 'r_object_id')

        logger.info('Delete sysobject %s' % DEMO_UPDATE_SYSOBJECT)
        self.client.delete(new_sysobj)

        logger.info('Delete folder %s' % DEMO_TEMP_FOLDER)
        self.client.delete(temp_folder)

        logger.info("+++++++++++++++++++++++++++++++Object CRUD End+++++++++++++++++++++++++++++++")

    def demo_content_management(self):
        """REST content management
        version: 7.2"""
        logger.info("\n+++++++++++++++++++++++++++++++Content Management Start+++++++++++++++++++++++++++++++")

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create temp folder %s in cabinet %s...' % (DEMO_TEMP_FOLDER, DEMO_CABINET))
        temp_folder = self.client.create_folder(cabinet, ResourceUtility.generate_folder(object_name=DEMO_TEMP_FOLDER))

        logger.info('Create new document %s with content...' % DEMO_NEW_DOCUMENT)
        new_doc = self.client.create_document(temp_folder,
                                              ResourceUtility.generate_document(object_name=DEMO_NEW_DOCUMENT),
                                              'It\'s created by python client', params={'format': 'crtext'})
        print_resource_properties(logger, new_doc, 'object_name', 'r_object_id')

        logger.info('Get primary content of %s...' % DEMO_NEW_DOCUMENT)
        primary_content = self.client.get_primary_content(new_doc, params={'media-url-policy': 'all'})
        print_resource_properties(logger, primary_content, 'object_name', 'r_object_id', 'format_name',
                                  'full_content_size')

        logger.info('All media URLs for primary content of %s...' % DEMO_NEW_DOCUMENT)
        for link in primary_content.all_links():
            logger.info(str(link) + '\n')

        logger.info('Create new html rendition for document %s...' % DEMO_NEW_DOCUMENT)
        new_content = self.client.create_content(new_doc, content='This is html rendition.', content_type='text/html',
                                                 params={'primary': 'false'})
        print_resource_properties(logger, new_content, 'object_name', 'r_object_id', 'format_name', 'full_content_size')

        logger.info('Create new rendition with large file for document %s...' % DEMO_NEW_DOCUMENT)
        path = self.prompt_func('Input the file path. Press \'Enter\' directly to skip uploading file:\n')
        if path:
            logger.info('Start to create document with file %s', path)
            try:
                with open(path, 'rb') as f:
                    new_content = self.client.create_content(new_doc, content=f,
                                                             content_type=RestClient.MEDIA_TYPE_OCTET_STREAM,
                                                             params={'primary': 'false'})
                    print_resource_properties(logger, new_content, 'object_name', 'r_object_id', 'format_name',
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
        """
        REST version management
        version:7.2
        """
        logger.info("\n+++++++++++++++++++++++++++++++Version Management Start+++++++++++++++++++++++++++++++")

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create temp folder %s in cabinet %s...' % (DEMO_TEMP_FOLDER, DEMO_CABINET))
        temp_folder = self.client.create_folder(cabinet, ResourceUtility.generate_folder(object_name=DEMO_TEMP_FOLDER))

        logger.info('Create new document %s with content...' % DEMO_NEW_DOCUMENT)
        doc = self.client.create_document(temp_folder, ResourceUtility.generate_document(object_name=DEMO_NEW_DOCUMENT))
        print_resource_properties(logger, doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check out document...')
        doc = self.client.check_out(doc)
        print_resource_properties(logger, doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Cancel check out')
        self.client.cancel_check_out(doc)

        logger.info('Refresh document...')
        doc = self.client.refresh(doc)
        print_resource_properties(logger, doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check out document...')
        doc = self.client.check_out(doc)
        print_resource_properties(logger, doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check in minor with new name...')
        doc = self.client.check_in_minor(doc,
                                         ResourceUtility.generate_document(object_name=DEMO_CHECK_IN_WITHOUT_CONTENT))
        print_resource_properties(logger, doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check out document...')
        doc = self.client.check_out(doc)
        print_resource_properties(logger, doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check in minor with content')
        doc = self.client.check_in_minor(doc, new_obj=None, content='I am new content.')
        print_resource_properties(logger, doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check out document...')
        doc = self.client.check_out(doc)
        print_resource_properties(logger, doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Check in major with new name and content')
        doc = self.client.check_in_major(doc,
                                         new_obj=ResourceUtility.generate_document(
                                             object_name=DEMO_CHECK_IN_WITH_CONTENT),
                                         content='I am new content again.')
        print_resource_properties(logger, doc, 'object_name', 'r_object_id', 'r_version_label')

        logger.info('Delete document %s' % DEMO_NEW_DOCUMENT)
        self.client.delete(doc, {'del-version': 'all'})

        logger.info('Delete folder %s' % DEMO_TEMP_FOLDER)
        self.client.delete(temp_folder)

        logger.info("+++++++++++++++++++++++++++++++Version Management End+++++++++++++++++++++++++++++++")

    def demo_batch(self):
        """
        REST batch
        version:7.2
        """
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
            print_properties(logger, operation, 'id', 'description')
            print_properties(logger, operation.get('request'), 'method', 'uri')

        batch_results = self.client.create_batch(batch)
        logger.info("\nThe batch results:\n")
        for result in batch_results.get('operations'):
            logger.info("------------------")
            print_properties(logger, result, 'id', 'description', 'state')

        logger.info("\n+++++++++++++++++++++++++++++++Batch End+++++++++++++++++++++++++++++++")

    def demo_dql(self):
        """
        REST DQL
        version: 7.2
        """
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
        """
        REST search with URL parameters
        version:7.2
        """
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
        """
        REST search with AQL
        version:7.3
        """
        logger.info("\n+++++++++++++++++++++++++++++++AQL Search Start+++++++++++++++++++++++++++++++")

        query_doc = ResourceUtility.generate_query_document(types=['dm_sysobject'], columns=['object_name'],
                                                            sorts=[Sort('object_name', True, 'en', True)],
                                                            expression_set=ExpSet('AND', FtExp('emc or rest')))
        logger.info('AQL search for keyword emc and parameters items-per-page=3,page=2,inline=true...')

        results = []
        try:
            results = self.client.aql_search(query_doc.dump(), {'items-per-page': '2', 'page': '1', 'inline': 'true'})
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

        # add facet definitions in search criteria
        self.step_separator('Facet against attribute {}'.format('r_object_type'))
        query_doc.facet_definitions = [
            FacetDefinition(facet_id='facet_r_object_type', attributes=['r_object_type'])]

        try:
            results = self.client.aql_search(query_doc.dump(), {'items-per-page': '2', 'page': '1', 'inline': 'true'})
        except IOError:
            logger.info('Fail to search with AQL.')

        logger.info('Facet results:')
        for facet in results.get('facets')[0].get('facet-value'):
            logger.info('group for %s has %s results and the navigation link is %s',
                        facet.get('facet-value-constraint'), facet.get('facet-value-count'),
                        facet.get('link').get('href'))

        logger.info("\n+++++++++++++++++++++++++++++++AQL Search End+++++++++++++++++++++++++++++++")

    def demo_saved_search(self):
        """
        REST Saved Search
        version: 7.3
        """

        logger.info("\n+++++++++++++++++++++++++++++++Saved Search Start+++++++++++++++++++++++++++++++")

        self.step_separator('Create a saved search...')
        query_doc = ResourceUtility.generate_query_document(types=['dm_sysobject'], columns=['object_name'],
                                                            sorts=[Sort('object_name', True, 'en', True)],
                                                            expression_set=ExpSet('AND', FtExp('emc or rest')))
        new_saved_search = ResourceUtility.generate_saved_search('New saved search',
                                                                 'This is a new saved search for demo', True,
                                                                 query_doc=query_doc)
        saved_search = self.client.create_saved_search(new_saved_search)
        properties = saved_search.get('properties')
        logger.info('New saved search is created at {}.\n name:{},\n description: {},\n is_public: {}'.format(
            properties.get('r_creation_date'), properties.get('object_name'), properties.get('title'),
            properties.get('r_is_public')))

        self.step_separator("Get saved searches...")
        saved_searches = self.client.get_saved_searches()

        if len(saved_searches.get_entries()) > 0:
            logger.info('Saved searches: ')
            for saved_search in saved_searches.get_entries():
                logger.info(saved_search.get('title'))

        self.step_separator('Get one saved search "{0}"...'.format(saved_searches.get_entry(0).get('title')))
        saved_search = self.client.get_saved_search(saved_searches.get_entry(0).get('title'))
        properties = saved_search.get('properties')
        logger.info(
            'name: {},\n public: {},\n has results: {}'.format(properties.get('object_name'),
                                                               properties.get('r_is_public'),
                                                               properties.get('has_results')))
        logger.info('saved AQL is:\n {}'.format(format_json(saved_search.get('query-document')), indent=4))

        self.step_separator('Update the saved search...')
        update_saved_search = ResourceUtility.generate_saved_search('New saved search',
                                                                    'This is a new saved search for demo', False,
                                                                    query_doc=query_doc)
        saved_search = self.client.update(saved_search, update_saved_search)
        properties = saved_search.get('properties')
        logger.info('New saved search is created at {}.\n name:{},\n description: {},\n is_public: {}'.format(
            properties.get('r_creation_date'), properties.get('object_name'), properties.get('title'),
            properties.get('r_is_public')))

        self.step_separator('Execute the saved search...')
        results = self.client.execute_saved_search(saved_search,
                                                   {'items-per-page': '2', 'page': '1', 'inline': 'true'})
        logger.info('Object names in page %d...', 2)
        for result in results.get_entries():
            logger.info(result.get('content').get('properties').get('object_name'))

        self.step_separator('Get saved results...')
        # noinspection PyBroadException
        try:
            self.client.get_saved_results(saved_search)
        except:
            logger.info('The saved results are disabled by default.')

        self.step_separator('Enable saved results...')
        results = self.client.enable_saved_results(saved_search)
        for result in results.get_entries():
            logger.info(result.get('title'))

        self.step_separator('Get saved results after it is enabled...')
        results = self.client.get_saved_results(saved_search, {'items-per-page': '2', 'page': '1', 'inline': 'true'})
        logger.info('Object names in page %d...', 2)
        for result in results.get_entries():
            logger.info(result.get('content').get('properties').get('object_name'))

        self.step_separator('Disable saved results...')
        self.client.disable_saved_results(saved_search)

        self.step_separator('Get saved results again after it is disabled...')
        # noinspection PyBroadException
        try:
            self.client.get_saved_results(saved_search)
        except:
            logger.info('The saved results are disabled again - no results')

        self.step_separator('Delete saved search...')
        self.client.delete(saved_search)

        logger.info("\n+++++++++++++++++++++++++++++++Saved Search End+++++++++++++++++++++++++++++++")

    def demo_search_template(self):
        """
        REST Search Template
        version:7.3
        """
        logger.info("\n+++++++++++++++++++++++++++++++Search Template Start+++++++++++++++++++++++++++++++")

        self.step_separator('Create a search template...')
        query_doc = ResourceUtility.generate_query_document(types=['dm_sysobject'], columns=['object_name'],
                                                            sorts=[Sort('object_name', True, 'en', True)],
                                                            expression_set=ExpSet('AND', FtExp('emc or rest',
                                                                                               is_template=True)))
        new_search_template = ResourceUtility.generate_search_template('New search template',
                                                                       'This is a new search template for demo', True,
                                                                       query_doc=query_doc)

        search_template = self.client.create_search_template(new_search_template)
        properties = search_template.get('properties')
        logger.info('New search template is created at {}.\n name:{},\n description: {},\n is_public: {}'.format(
            properties.get('r_creation_date'), properties.get('object_name'), properties.get('subject'),
            properties.get('r_is_public')))

        logger.info('Get search templates...')
        search_templates = self.client.get_search_templates()

        if len(search_templates.get_entries()) > 0:
            logger.info('Saved searches: ')
            for search_template in search_templates.get_entries():
                logger.info(search_template.get('title'))

        self.step_separator('Get one search template "{0}"...'.format(search_templates.get_entry(0).get('title')))
        search_template = self.client.get_search_template(search_templates.get_entry(0).get('title'))
        properties = search_template.get('properties')
        logger.info(
            'name: {},\n public: {},\n description: {}'.format(properties.get('object_name'),
                                                               properties.get('r_is_public'),
                                                               properties.get('subject')))
        logger.info('\nexternal variables:')
        for v in search_template.get('external-variables'):
            logger.info(
                'id: {},\nvariable type: {},\ndata type: {},\nvalue: {}'.format(v.get('id'), v.get('variable-type'),
                                                                                v.get('data-type'),
                                                                                v.get('variable-value')))

        logger.info(
            'saved AQL is:\n {}'.format(
                format_json(search_template.get('query-document-template')), indent=4))

        self.step_separator('Execute the search template...')

        time.sleep(1)
        input_variables = ResourceUtility.generate_search_template_variables(search_template.get('external-variables'),
                                                                             self.prompt_func)

        results = self.client.execute_search_template(search_template, variables=input_variables,
                                                      params={'items-per-page': '2', 'page': '1', 'inline': 'true'})
        logger.info('Object names in page %d...', 2)
        for result in results.get_entries():
            logger.info(result.get('content').get('properties').get('object_name'))

        self.step_separator('Delete the search template...')
        self.client.delete(search_template)

        logger.info("\n+++++++++++++++++++++++++++++++Search Template End+++++++++++++++++++++++++++++++")

    def demo_type(self):
        """
        REST type
        version:7.2
        """
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
        """
        REST value assistance
        version:7.3
        """
        logger.info("\n+++++++++++++++++++++++++++++++Value Assistance Start+++++++++++++++++++++++++++++++")

        logger.info('Get the value assistance of the type...')
        dm_type_str = self.prompt_func(
            'Input the type name with fixed value assistance list. Press \'Enter\' directly to skip.\n')
        if dm_type_str:
            dm_type = self.client.get_type(dm_type_str)

            if dm_type:
                included_property = self.prompt_func(
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
        dm_type_str = self.prompt_func(
            '\nInput the type name with value assistance dependencies. Press \'Enter\' directly to skip.\n')
        if dm_type_str:
            dm_type = self.client.get_type(dm_type_str)

            for attr in dm_type.get('properties'):
                logger.info('Attribute %s.%s has dependency %s' % (
                    dm_type.get('name'), attr.get('name'), attr.get('dependencies')))

            attr_name = self.prompt_func('Input the attribute name of %s which has dependencies:' % dm_type_str)
            dependency_attr_name = self.prompt_func('Input the dependency name of %s.%s:\n' % (dm_type_str, attr_name))
            dependency_attr_value = self.prompt_func(
                'Input the dependency value of attribute %s:\n' % dependency_attr_name)

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
        """
        REST relation CRUD
        version:7.2
        """
        logger.info("\n+++++++++++++++++++++++++++++++Relation CRUD Start+++++++++++++++++++++++++++++++")

        logger.info('Get relations in repository %s...' % self.REST_REPOSITORY)
        self.client.get_relations()

        logger.info('Create relation in repository %s...' % self.REST_REPOSITORY)

        logger.info('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        logger.info('Create new sysobject as relation parent...')
        parent = self.client.create_sysobj(cabinet,
                                           ResourceUtility.generate_sysobject(object_name='relation-parent'))
        print_resource_properties(logger, parent, 'object_name', 'r_object_id')

        logger.info('Create new sysobject as relation child...')
        child = self.client.create_sysobj(cabinet,
                                          ResourceUtility.generate_sysobject(object_name='relation-child'))
        print_resource_properties(logger, child, 'object_name', 'r_object_id')

        logger.info('Create new relation...')
        new_relation = self.client.create_relation(ResourceUtility.generate_relation(relation_name='peer',
                                                                                     parent_id=parent.get(
                                                                                         'properties').get(
                                                                                         'r_object_id'),
                                                                                     child_id=child.get(
                                                                                         'properties').get(
                                                                                         'r_object_id'),
                                                                                     ))
        print_resource_properties(logger, new_relation, 'object_name', 'r_object_id')

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
        """
        REST formats
        version: 7.2
        """
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
        """
        REST network locations
        version:7.2
        """
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
        """REST lightweight object
        version:7.3
        """
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

        sharable_type = self.prompt_func('\nInput the sharable type. Press \'Enter\' directly to skip.\n')
        if not sharable_type:
            logger.info('Skip lightweight object demo.')
        else:
            logger.info('Create object %s of sharable type %s...' % (DEMO_SHARABLE_OBJECT, sharable_type))
            sharable_obj = self.client.create_sysobj(cabinet,
                                                     ResourceUtility.generate_sysobject(
                                                         sharable_type,
                                                         object_name=DEMO_SHARABLE_OBJECT,
                                                         title='demo_sharable_type'))

            lightweight_type = self.prompt_func('\nInput the lightweight type:\n')
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
        """
        REST aspect
        version:7.3
        """
        logger.info("\n+++++++++++++++++++++++++++++++Aspect Start+++++++++++++++++++++++++++++++")

        logger.info('Get all aspects...')
        aspects = self.client.get_aspects()
        for entry in aspects.get_entries():
            logger.info('Aspect name: %s', entry.get('title'))

        aspect_type = self.prompt_func('\nInput the aspect type to attach... Press \'Enter\' directly to skip.\n')

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

    @staticmethod
    def step_separator(message):
        logger.info('\n' + message)

    def clean_demo_cabinet(self):
        logger.debug("\n+++++++++++++++++++++++++++++++Delete demo cabinet Start+++++++++++++++++++++++++++++++")
        cabinet = self.client.get_cabinet(DEMO_CABINET)

        if cabinet is not None:
            logger.debug('Deleting cabinet %s.', DEMO_CABINET)
            self.client.delete_folder_recursively(cabinet)
        else:
            logger.debug('Cabinet %s does not exist.', DEMO_CABINET)

        logger.debug("+++++++++++++++++++++++++++++++Delete demo cabinet End+++++++++++++++++++++++++++++++")

    def clean_demo_user_group(self):
        logger.debug("+++++++++++++++++++++++++++++++Delete demo users/groups Start+++++++++++++++++++++++++++++++")

        user = self.client.get_user(DEMO_NEW_USER)
        if user is not None:
            logger.debug('Delete user %s...' % DEMO_NEW_USER)
            self.client.delete(user)
        else:
            logger.debug('User %s does not exist.', DEMO_NEW_USER)

        group = self.client.get_group(DEMO_NEW_GROUP)
        if group is not None:
            logger.debug('Delete group %s...' % DEMO_NEW_GROUP)
            self.client.delete(group)
        else:
            logger.debug('Group %s does not exist.', DEMO_NEW_GROUP)

        group = self.client.get_group(DEMO_ANOTHER_NEW_GROUP)
        if group is not None:
            logger.debug('Delete group %s...' % DEMO_ANOTHER_NEW_GROUP)
            self.client.delete(group)
        else:
            logger.debug('Group %s does not exist.', DEMO_ANOTHER_NEW_GROUP)
        logger.debug("+++++++++++++++++++++++++++++++Delete demo users/groups End+++++++++++++++++++++++++++++++")

    def prepare_env(self):
        self.reset_environment()
        self.create_demo_cabinet()

    def reset_environment(self):
        """Reset demo environment
        version: 7.2"""
        logger.info("\n+++++++++++++++++++++++++++++++Reset Environment Start+++++++++++++++++++++++++++++++")

        self.clean_demo_cabinet()
        self.clean_demo_user_group()

        logger.info("+++++++++++++++++++++++++++++++Reset Environment End+++++++++++++++++++++++++++++++")

    def run_all(self):
        self.prepare_env()
        [item.callable()
         for key, item in self.choices.items()
         if not (item.callable == self.quit or item.callable == self.reset_environment)]

        self.reset_environment()

    def run(self):

        while True:
            try:
                for k, v in self.choices.items():
                    print("%d. %s" % (k, v.description))

                user_choice = int(self.prompt_func("\nWhat's your choice?\n"))

                if user_choice not in self.choices:
                    print('#Invalid choice!#\n')
                    continue

                self.prepare_env()
                self.choices[user_choice].callable()
                self.reset_environment()
                time.sleep(1)
            except ValueError:
                print("\n#Enter number of the demo items instead of other characters.#\n")
            except Exception as e:
                logger.exception(e)
                time.sleep(1)
                print("\n#Error is detected during demo. Please refer the log for the exception detail.#\n")


def main():
    RestDemo(prompt_user).run()


if __name__ == '__main__':
    main()
else:
    logger.info('RestDemo as a module')
