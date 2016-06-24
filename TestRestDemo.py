import unittest
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner
from RestDemo import RestDemo


class TestRestDemo(unittest.TestCase):
    rest_demo = RestDemo()

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

    def test_user_group_member_crud(self):
        TestRestDemo.rest_demo.demo_user_group_member_crud()

    def test_types(self):
        TestRestDemo.rest_demo.demo_type()

    # def test_value_assistance(self):
    #     TestRestDemo.rest_demo.demo_value_assistance()

    # def test_lightweight_objects(self):
    #     TestRestDemo.rest_demo.demo_lightweight_object()

    def test_relation_crud(self):
        TestRestDemo.rest_demo.demo_relation_crud()

    def test_formats(self):
        TestRestDemo.rest_demo.demo_format()

    def test_network_locations(self):
        TestRestDemo.rest_demo.demo_network_location()

    # def test_aspects(self):
    #     TestRestDemo.rest_demo.demo_aspect()

    @classmethod
    def tearDownClass(cls):
        TestRestDemo.rest_demo.reset_environment()


if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
