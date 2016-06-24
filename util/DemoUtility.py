import json
from model.Link import Link
__author__ = 'wangc31'


def generate_reference(resource):
    representation = dict()
    representation['href'] = resource.find_link(Link.REL_SELF).href()
    return dict_to_body(representation)


def dict_to_body(dictionary):
    return json.dumps(dictionary)


def new_dummy_cabinet(**kwargs):
    representation = dict()
    kwargs['r_object_type'] = 'dm_cabinet'
    representation['properties'] = kwargs

    representation['name'] = 'cabinet'
    representation['type'] = 'dm_cabinet'
    return dict_to_body(representation)


def new_dummy_folder(**kwargs):
    representation = dict()
    kwargs['r_object_type'] = 'dm_folder'
    representation['properties'] = kwargs
    return dict_to_body(representation)


def new_dummy_sysobject(**kwargs):
    representation = dict()
    kwargs['r_object_type'] = 'dm_sysobject'
    representation['properties'] = kwargs
    return dict_to_body(representation)


def new_dummy_document(**kwargs):
    representation = dict()
    kwargs['r_object_type'] = 'dm_document'
    representation['properties'] = kwargs
    return dict_to_body(representation)


def new_dummy_user(**kwargs):
    representation = dict()
    representation['properties'] = kwargs
    return dict_to_body(representation)


def new_dummy_group(**kwargs):
    representation = dict()
    representation['properties'] = kwargs
    return dict_to_body(representation)
