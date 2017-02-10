import unittest
from unittest.mock import patch
from RestDemo import RestDemo


def prompt_4ut(message):
    print(message)
    return ''


class TestRestDemo(unittest.TestCase):
    rest_demo = RestDemo(prompt_4ut)

    @classmethod
    def setUpClass(cls):
        TestRestDemo.rest_demo.prepare_env()

    def test_sysobject_crud(self):
        TestRestDemo.rest_demo.demo_sysobject_crud()

    def test_folder_crud(self):
        TestRestDemo.rest_demo.demo_folder_crud()

    def test_version_mgt(self):
        TestRestDemo.rest_demo.demo_version_management()

    def test_dql(self):
        TestRestDemo.rest_demo.demo_dql()

    def test_simple_search(self):
        TestRestDemo.rest_demo.demo_simple_search()

    def test_aql_search(self):
        TestRestDemo.rest_demo.demo_aql_search()

    def test_saved_search(self):
        TestRestDemo.rest_demo.demo_saved_search()

    @patch('util.DemoUtil.prompt_user', return_value='rest')
    def test_search_template(self, key_word):
        TestRestDemo.rest_demo.demo_search_template()

    def test_user_group_member_crud(self):
        TestRestDemo.rest_demo.demo_user_group_member_crud()

    def test_types(self):
        TestRestDemo.rest_demo.demo_type()

    def test_value_assistance(self):
        TestRestDemo.rest_demo.demo_value_assistance()

    def test_lightweight_objects(self):
        TestRestDemo.rest_demo.demo_lightweight_object()

    def test_relation_crud(self):
        TestRestDemo.rest_demo.demo_relation_crud()

    def test_formats(self):
        TestRestDemo.rest_demo.demo_format()

    def test_network_locations(self):
        TestRestDemo.rest_demo.demo_network_location()

    def test_aspects(self):
        TestRestDemo.rest_demo.demo_aspect()

    def test_batch(self):
        TestRestDemo.rest_demo.demo_batch()

    def test_content_mgt(self):
        TestRestDemo.rest_demo.demo_content_management()

    @classmethod
    def tearDownClass(cls):
        TestRestDemo.rest_demo.reset_environment()


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
