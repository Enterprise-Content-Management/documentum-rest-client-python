from configparser import ConfigParser

import pytest

from RestDemo import RestDemo


def prompt_4ut(message):
    print(message)
    return ''


@pytest.fixture(autouse=True)
def demo():
    demo = RestDemo(prompt_4ut)
    demo.prepare_env()
    yield demo
    demo.reset_environment()


@pytest.fixture(autouse=True)
def config():
    config_parser = ConfigParser()
    config_parser.read('resources/test.properties')
    return config_parser


class TestRestDemo():
    def test_sysobject_crud(self, demo):
        demo.demo_sysobject_crud()

    def test_folder_crud(self, demo):
        demo.demo_folder_crud()

    def test_version_mgt(self, demo):
        demo.demo_version_management()

    def test_dql(self, demo):
        demo.demo_dql()

    def test_simple_search(self, demo):
        demo.demo_simple_search()

    def test_aql_search(self, demo):
        demo.demo_aql_search()

    def test_saved_search(self, demo):
        demo.demo_saved_search()

    def test_search_template(self, demo, config, monkeypatch):
        kw = config.get("inputs", 'search.keyword')
        monkeypatch.setattr(demo, 'prompt_func', lambda x: kw)
        demo.demo_search_template()

    def test_user_group_member_crud(self, demo):
        demo.demo_user_group_member_crud()

    def test_types(self, demo):
        demo.demo_type()

    def test_value_assistance(self, demo):
        demo.demo_value_assistance()

    def test_lightweight_objects(self, demo, config, monkeypatch):
        sharable = config.get('inputs', 'sharable.type.name')
        monkeypatch.setattr(demo, 'prompt_func', lambda x: sharable)
        lightweight = config.get('inputs', 'lightweight.type.name')
        monkeypatch.setattr(demo, 'prompt_func', lambda x: lightweight)
        demo.demo_lightweight_object()

    def test_relation_crud(self, demo):
        demo.demo_relation_crud()

    def test_formats(self, demo):
        demo.demo_format()

    def test_network_locations(self, demo):
        demo.demo_network_location()

    def test_aspects(self, demo, config, monkeypatch):
        value = config.get('inputs', 'aspect.name')
        monkeypatch.setattr(demo, 'prompt_func', lambda x: value)
        demo.demo_aspect()

    def test_batch(self, demo):
        demo.demo_batch()

    def test_content_mgt(self, demo, config, monkeypatch):
        value = config.get('inputs', 'content.file')
        monkeypatch.setattr(demo, 'prompt_func', lambda x: value)
        demo.demo_content_management()
