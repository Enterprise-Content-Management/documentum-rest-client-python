import ConfigParser
from network import RestClient
from util import DemoUtility

__author__ = 'wangc31'

DEMO_CABINET = 'demo-cabinet'
DEMO_NEW_FOLDER = 'demo-new-folder'
DEMO_UPDATE_FOLDER = 'demo-update-folder'
DEMO_TEMP_FOLDER = 'demo-temp-folder'
DEMO_NEW_SYSOBJECT = 'demo-new-sysobj'
DEMO_UPDATE_SYSOBJECT = 'demo-udpate-sysobj'
DEMO_NEW_DOCUMENT = 'demo-doc'
DEMO_CHECK_IN_WITHOUT_CONTENT = 'demo-check-in-without-content'
DEMO_CHECK_IN_WITH_CONTENT = 'demo-check-in-with-content'
DEMO_NEW_USER = 'demo-py-client-user'
DEMO_UPDATE_USER = 'demo-py-client-user-updated'
DEMO_NEW_GROUP = 'demo-py-client-group'
DEMO_ANOTHER_NEW_GROUP = 'demo-py-client-another-group'
DEMO_UPDATE_GROUP = 'demo-py-client-group-updated'


class RestDemo:
    def __init__(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read("rest.properties")

        self.REST_URI = config_parser.get("environment", "rest.host")
        self.REST_REPOSITORY = config_parser.get("environment", "rest.repository")
        self.REST_ID = config_parser.get("environment", "rest.username")
        self.REST_PWD = config_parser.get("environment", "rest.password")
        self.client = RestClient.RestClient(self.REST_ID, self.REST_PWD, self.REST_URI)

        self.choices = {1: ['REST folder CRUD', self.demo_folder_crud],
                        2: ['REST sysObject CRUD', self.demo_sysobject_crud],
                        3: ['REST content management', self.demo_content_management],
                        4: ['REST version management', self.demo_version_management],
                        5: ['REST DQL', self.demo_dql],
                        6: ['REST user, group and member CRUD', self.demo_user_group_member_crud],
                        7: ['REST Search with URL parameters ', self.demo_simple_search],
                        8: ['REST all demos', self.demo_all],
                        0: ['Reset demo environment', self.reset_environment]}

    def create_temp_cabinet(self):
        print("\n+++++++++++++++++++++++++++++++Create temp cabinet Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        self.client.create_cabinet(repository, DemoUtility.new_dummy_cabinet(object_name=DEMO_CABINET))

        print("+++++++++++++++++++++++++++++++Create temp cabinet End+++++++++++++++++++++++++++++++")

    def delete_temp_cabinet(self):
        print("\n+++++++++++++++++++++++++++++++Delete temp cabinet Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        cabinet = self.client.get_cabinet(repository, DEMO_CABINET)
        if cabinet is not None:
            self.client.delete(cabinet)

        print("+++++++++++++++++++++++++++++++Delete temp cabinet End+++++++++++++++++++++++++++++++")

    def demo_user_group_member_crud(self):
        print ("\n+++++++++++++++++++++++++++++++User CRUD Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        print('Create user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        new_user = self.client.create_user(repository, DemoUtility.new_dummy_user(user_name=DEMO_NEW_USER,
                                                                                  user_login_name=DEMO_NEW_USER))
        print('Update user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        new_user = self.client.update(new_user, DemoUtility.new_dummy_user(user_login_name=DEMO_UPDATE_USER))

        print('Refresh user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        self.client.refresh(new_user)

        print('Get user %s in repository %s' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        new_user = self.client.get_user(repository, DEMO_NEW_USER)

        print ("\n+++++++++++++++++++++++++++++++Group and Group Member CRUD Start+++++++++++++++++++++++++++++++")

        print('Create group %s in repository %s' % (DEMO_NEW_GROUP, self.REST_REPOSITORY))
        new_group = self.client.create_group(repository, DemoUtility.new_dummy_group(group_name=DEMO_NEW_GROUP))

        print('Update group %s in repository %s' % (DEMO_NEW_GROUP, self.REST_REPOSITORY))
        new_group = self.client.update(new_group, DemoUtility.new_dummy_group(group_display_name=DEMO_UPDATE_USER))

        print('Add user %s in the group %s' % (DEMO_NEW_USER, DEMO_NEW_GROUP))
        self.client.add_user_to_group(new_group, DemoUtility.generate_reference(new_user))

        print('Remove user %s in the group %s' % (DEMO_NEW_USER, DEMO_NEW_GROUP))
        self.client.remove_user_from_group(new_group, DEMO_NEW_USER)

        print('Create another group %s in repository %s' % (DEMO_ANOTHER_NEW_GROUP, self.REST_REPOSITORY))
        another_new_group = self.client.create_group(repository,
                                                     DemoUtility.new_dummy_group(group_name=DEMO_ANOTHER_NEW_GROUP))

        print('Add group %s in the group %s' % (DEMO_ANOTHER_NEW_GROUP, DEMO_NEW_GROUP))
        self.client.add_group_to_group(new_group, DemoUtility.generate_reference(another_new_group))

        print('Remove group %s in the group %s' % (DEMO_ANOTHER_NEW_GROUP, DEMO_NEW_GROUP))
        self.client.remove_group_from_group(new_group, DEMO_ANOTHER_NEW_GROUP)

        print('Delete user %s in repository %s...' % (DEMO_NEW_USER, self.REST_REPOSITORY))
        self.client.delete(new_user)

        print('Delete group %s in repository %s...' % (DEMO_NEW_GROUP, self.REST_REPOSITORY))
        self.client.delete(new_group)

        print('Delete group %s in repository %s...' % (DEMO_ANOTHER_NEW_GROUP, self.REST_REPOSITORY))
        self.client.delete(another_new_group)

    def demo_folder_crud(self):
        print("\n+++++++++++++++++++++++++++++++Folder CRUD Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        print('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(repository, DEMO_CABINET)

        print('Create new folder %s in cabinet %s...' % (DEMO_NEW_FOLDER, DEMO_CABINET))
        new_folder = self.client.create_folder(cabinet, DemoUtility.new_dummy_folder(object_name=DEMO_NEW_FOLDER))

        print('Update folder %s in cabinet %s...' % (DEMO_NEW_FOLDER, DEMO_CABINET))
        new_folder = self.client.update(new_folder, DemoUtility.new_dummy_folder(object_name=DEMO_UPDATE_FOLDER))

        print('Refresh folder %s in cabinet %s...' % (DEMO_UPDATE_FOLDER, DEMO_CABINET))
        self.client.refresh(new_folder)

        print('Get folder %s in cabinet %s...' % (DEMO_UPDATE_FOLDER, DEMO_CABINET))
        self.client.get_folder(cabinet, DEMO_UPDATE_FOLDER)

        print('Delete folder %s' % DEMO_UPDATE_FOLDER)
        self.client.delete(new_folder)

        print("+++++++++++++++++++++++++++++++Folder CRUD End+++++++++++++++++++++++++++++++")

    def demo_sysobject_crud(self):
        print("\n+++++++++++++++++++++++++++++++Object CRUD Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        print('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(repository, DEMO_CABINET)

        print('Create temp folder %s in cabinet %s...' % (DEMO_TEMP_FOLDER, DEMO_CABINET))
        temp_folder = self.client.create_folder(cabinet, DemoUtility.new_dummy_folder(object_name=DEMO_TEMP_FOLDER))

        print('Create new sysobject %s in folder %s...' % (DEMO_NEW_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.create_sysobj(temp_folder,
                                               DemoUtility.new_dummy_sysobject(object_name=DEMO_NEW_SYSOBJECT))

        print('Update sysobject %s in folder %s...' % (DEMO_UPDATE_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.update(new_sysobj, DemoUtility.new_dummy_sysobject(object_name=DEMO_UPDATE_SYSOBJECT))

        print('Refresh sysobject %s in folder %s...' % (DEMO_UPDATE_SYSOBJECT, DEMO_TEMP_FOLDER))
        self.client.refresh(new_sysobj)

        print('Get sysobject %s in folder %s...' % (DEMO_UPDATE_SYSOBJECT, DEMO_TEMP_FOLDER))
        new_sysobj = self.client.get_sysobject(temp_folder, DEMO_UPDATE_SYSOBJECT)

        print('Delete sysobject %s' % DEMO_UPDATE_SYSOBJECT)
        self.client.delete(new_sysobj)

        print('Delete folder %s' % DEMO_TEMP_FOLDER)
        self.client.delete(temp_folder)

        print("+++++++++++++++++++++++++++++++Object CRUD End+++++++++++++++++++++++++++++++")

    def demo_content_management(self):
        print("\n+++++++++++++++++++++++++++++++Content Management Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        print('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(repository, DEMO_CABINET)

        print('Create temp folder %s in cabinet %s...' % (DEMO_TEMP_FOLDER, DEMO_CABINET))
        temp_folder = self.client.create_folder(cabinet, DemoUtility.new_dummy_folder(object_name=DEMO_TEMP_FOLDER))

        print('Create new document %s with content...' % DEMO_NEW_DOCUMENT)
        new_doc = self.client.create_document(temp_folder,
                                              DemoUtility.new_dummy_document(object_name=DEMO_NEW_DOCUMENT),
                                              'It\'s created by python client', params={'format': 'crtext'})

        print('Get primary content of %s...' % DEMO_NEW_DOCUMENT)
        primary_content = self.client.get_primary_content(new_doc, params={'media-url-policy': 'all'})

        print('All media urls for primary content of %s...' % DEMO_NEW_DOCUMENT)
        for link in primary_content.all_links():
            print(link)

        print('Create new rendition for document %s...' % DEMO_NEW_DOCUMENT)
        self.client.create_content(new_doc, content='This is html rendition.', content_type='text/html',
                                   params={'primary': 'false'})

        print('Create new rendition with large file for document %s...' % DEMO_NEW_DOCUMENT)
        path = raw_input('Input the file path. Press \'Enter\' directly to skip uploading file:\n')
        if path:
            try:
                with open(path, 'rb') as f:
                    self.client.create_content(new_doc, content=f, content_type=RestClient.MEDIA_TYPE_OCTET_STREAM,
                                               params={'primary': 'false'})
            except IOError:
                print('The file %s does not exist or can not be opened.' % path)
        else:
            print('Skip create new rendition with large file for document %s...' % DEMO_NEW_DOCUMENT)

        print('Get contents for document %s...' % DEMO_NEW_DOCUMENT)
        contents = self.client.get_contents(new_doc)

        print('All renditions for document %s...' % DEMO_NEW_DOCUMENT)
        for rendition in contents.get_entries():
            print(rendition.get('id') + '\n')

        print('Delete document %s' % DEMO_NEW_DOCUMENT)
        self.client.delete(new_doc)

        print('Delete folder %s' % DEMO_TEMP_FOLDER)
        self.client.delete(temp_folder)

        print("+++++++++++++++++++++++++++++++Content Management End+++++++++++++++++++++++++++++++")

    def demo_version_management(self):
        print("\n+++++++++++++++++++++++++++++++Version Management Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        print('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(repository, DEMO_CABINET)

        print('Create temp folder %s in cabinet %s...' % (DEMO_TEMP_FOLDER, DEMO_CABINET))
        temp_folder = self.client.create_folder(cabinet, DemoUtility.new_dummy_folder(object_name=DEMO_TEMP_FOLDER))

        print('Create new document %s with content...' % DEMO_NEW_DOCUMENT)
        doc = self.client.create_document(temp_folder, DemoUtility.new_dummy_document(object_name=DEMO_NEW_DOCUMENT))

        print('Check out document...')
        doc = self.client.check_out(doc)

        print('Cancel check out')
        self.client.cancel_check_out(doc)

        print('Refresh document...')
        doc = self.client.refresh(doc)

        print('Check out document...')
        doc = self.client.check_out(doc)

        print('Check in minor with new name...')
        doc = self.client.check_in_minor(doc, DemoUtility.new_dummy_document(object_name=DEMO_CHECK_IN_WITHOUT_CONTENT))

        print('Check out document...')
        doc = self.client.check_out(doc)

        print('Check in minor with content')
        doc = self.client.check_in_minor(doc, new_obj=None, content='I am new content.')

        print('Check out document...')
        doc = self.client.check_out(doc)

        print('Check in major with new name and content')
        doc = self.client.check_in_major(doc,
                                         new_obj=DemoUtility.new_dummy_document(object_name=DEMO_CHECK_IN_WITH_CONTENT),
                                         content='I am new content again.')

        print('Delete document %s' % DEMO_NEW_DOCUMENT)
        self.client.delete(doc, {'del-version': 'all'})

        print('Delete folder %s' % DEMO_TEMP_FOLDER)
        self.client.delete(temp_folder)

        print("+++++++++++++++++++++++++++++++Version Management End+++++++++++++++++++++++++++++++")

    def demo_dql(self):
        print("\n+++++++++++++++++++++++++++++++DQL Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        print('Query \'select * from dm_user\' with items-per-page=3,page=2...')
        results = self.client.dql(repository, 'select * from dm_user', {'items-per-page': '2', 'page': '2'})

        print('User names in current page...')
        for result in results.get_entries():
            print(result.get('content').get('properties').get('user_name'))
        print('')

        print('Navigate to next page...')
        results = self.client.next_page(results)

        print('User names in current page...')
        for result in results.get_entries():
            print(result.get('content').get('properties').get('user_name'))
        print('')

        print("+++++++++++++++++++++++++++++++DQL End+++++++++++++++++++++++++++++++")

    def demo_simple_search(self):
        print("\n+++++++++++++++++++++++++++++++Simple Search Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        print('Simple search with keyword emc and parameters items-per-page=3,page=2,inline=true...')
        results = self.client.simple_search(repository, 'emc', {'items-per-page': '2', 'page': '1', 'inline': 'true'})

        print('Object names in current page...')
        for result in results.get_entries():
            print(result.get('content').get('properties').get('object_name'))
        print('')

        print('Navigate to next page...')
        results = self.client.next_page(results)

        print('Object names in current page...')
        for result in results.get_entries():
            print(result.get('content').get('properties').get('object_name'))
        print('')

        print("+++++++++++++++++++++++++++++++Simple Search End+++++++++++++++++++++++++++++++")

    def demo_types(self):
        print("\n+++++++++++++++++++++++++++++++Types and Values Assistance Start+++++++++++++++++++++++++++++++")

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        print('Get types resource...')
        types = self.client.get_types(repository)

        print('Get dm_document type resource...')
        dm_doc_type = self.client.get_type(repository, 'dm_document')

        # print('Get the value assistance of the type...')
        # dm_type = raw_input('Input the type name for value assistance. Press \'Enter\' directly to skip the demo item:\n')
        # TODO need env




        print("\n+++++++++++++++++++++++++++++++Types and Values Assistance End+++++++++++++++++++++++++++++++")

    def reset_environment(self):
        print("\n+++++++++++++++++++++++++++++++Reset Environment Start+++++++++++++++++++++++++++++++")

        print('Start resetting environment')

        print('Get home resource...')
        home = self.client.get_home_resource()

        print('Get repository %s...' % self.REST_REPOSITORY)
        repository = self.client.get_repository(home, self.REST_REPOSITORY)

        print('Get cabinet %s...' % DEMO_CABINET)
        cabinet = self.client.get_cabinet(repository, DEMO_CABINET)

        if cabinet:
            self.client.delete_folder_recursively(cabinet)

        print('Finish resetting environment')

        print("+++++++++++++++++++++++++++++++Reset Environment End+++++++++++++++++++++++++++++++")

    def demo_all(self):
        self.demo_folder_crud()
        self.demo_sysobject_crud()
        self.demo_content_management()
        self.demo_version_management()
        self.demo_dql()
        self.demo_user_group_member_crud()

    def demo(self):
        print("\nInput the number to show the demo.\n")

        choice = -1
        while choice not in self.choices.keys():
            for k, v in self.choices.items():
                print ("%d. %s" % (k, v[0]))

            choice = input("\nWhat's your choice?\n")

        self.prepare_env()
        self.choices[choice][1]()
        self.clean_env()

    def clean_env(self):
        self.delete_temp_cabinet()

    def prepare_env(self):
        self.reset_environment()
        self.create_temp_cabinet()


def main():
    rest_demo = RestDemo()
    rest_demo.demo()


if __name__ == '__main__':
    main()
else:
    print('RestDemo as a module')
