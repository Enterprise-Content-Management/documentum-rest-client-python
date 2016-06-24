import unittest
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner
from RestDemo import RestDemo


class TestRestDemo(unittest.TestCase):
    def setUp(self):
        self.rest_demo = RestDemo()
        self.rest_demo.prepare_env()

    def test_sysobject_crud(self):
        self.rest_demo.demo_sysobject_crud()

    def test_folder_crud(self):
        self.rest_demo.demo_folder_crud()

    def test_version_mgt(self):
        self.rest_demo.demo_version_management()

    def test_dql(self):
        self.rest_demo.demo_dql()

    def test_simple_search(self):
        self.rest_demo.demo_simple_search()

    def test_user_group_member_crud(self):
        self.rest_demo.demo_user_group_member_crud()

    def test_types_value_assistance(self):
        self.rest_demo.demo_types()

    def tearDown(self):
        self.rest_demo.clean_env()


if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
