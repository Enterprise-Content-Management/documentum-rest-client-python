from configparser import ConfigParser

import pytest

from RestDemo import RestDemo, PromptUserInput


@pytest.fixture(autouse=True)
def demo(monkeypatch):
    prompt = PromptUserInput()
    monkeypatch.setattr(prompt, 'demo_logging', lambda: '')
    monkeypatch.setattr(prompt, 'rest_entry', lambda x: '')
    monkeypatch.setattr(prompt, 'rest_repo', lambda x: '')
    monkeypatch.setattr(prompt, 'rest_user', lambda x: '')
    monkeypatch.setattr(prompt, 'rest_pwd', lambda x: '')

    demo_inst = RestDemo(prompt)
    demo_inst.prepare_env()
    yield demo_inst
    demo_inst.reset_environment()


@pytest.fixture(autouse=True)
def config():
    config_parser = ConfigParser()
    config_parser.read('resources/test.properties')
    return config_parser


class TestRestDemo:
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
        monkeypatch.setattr(demo.prompt, 'search_template_var', lambda x, y: kw)
        demo.demo_search_template()

    def test_user_group_member_crud(self, demo):
        demo.demo_user_group_member_crud()

    def test_types(self, demo):
        demo.demo_type()

    def test_value_assistance(self, demo, config, monkeypatch):
        type_fixed_va = config.get('inputs', 'type.fixed.value.assistance')
        attr_fixed_va = config.get('inputs', 'type.attribute.fixed.value.assistance')
        type_dep_va = config.get('inputs', 'type.dependency.value.assistance')
        attr_with_dep_va = config.get('inputs', 'type.attribute.with.dependency.value.assistence')
        attr_dep_va = config.get('inputs', 'type.attribute.dependency.value.assistance')
        attr_value_dep_va = config.get('inputs', 'type.attribute.value.dependency.value.assistance')

        monkeypatch.setattr(demo.prompt, 'type_fixed_va', lambda: type_fixed_va)
        monkeypatch.setattr(demo.prompt, 'attribute_fixed_va', lambda x: attr_fixed_va)
        monkeypatch.setattr(demo.prompt, 'type_dep_va', lambda: type_dep_va)
        monkeypatch.setattr(demo.prompt, 'attribute_va', lambda x: attr_with_dep_va)
        monkeypatch.setattr(demo.prompt, 'attribute_dep_va', lambda x, y: attr_dep_va)
        monkeypatch.setattr(demo.prompt, 'attribute_dep_value_va', lambda x: attr_value_dep_va)

        demo.demo_value_assistance()

    def test_lightweight_objects(self, demo, config, monkeypatch):
        sharable = config.get('inputs', 'sharable.type.name')
        lightweight = config.get('inputs', 'lightweight.type.name')
        monkeypatch.setattr(demo.prompt, 'lightweight_type', lambda: lightweight)
        monkeypatch.setattr(demo.prompt, 'sharable_type', lambda: sharable)

        demo.demo_lightweight_object()

    def test_relation_crud(self, demo):
        demo.demo_relation_crud()

    def test_formats(self, demo):
        demo.demo_format()

    def test_network_locations(self, demo):
        demo.demo_network_location()

    def test_aspects(self, demo, config, monkeypatch):
        value = config.get('inputs', 'aspect.name')
        monkeypatch.setattr(demo.prompt, 'aspect_type', lambda: value)
        demo.demo_aspect()

    def test_batch(self, demo):
        demo.demo_batch()

    def test_content_mgt(self, demo, config, monkeypatch):
        value = config.get('inputs', 'content.file')
        monkeypatch.setattr(demo.prompt, 'content_file', lambda: value)
        demo.demo_content_management()
