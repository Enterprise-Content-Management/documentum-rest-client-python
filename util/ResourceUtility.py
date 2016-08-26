from model.RestResource import Resource

__author__ = 'wangc31'


def generate_cabinet(**properties):
    properties['r_object_type'] = 'dm_cabinet'
    return _generate_resource(properties=properties)


def generate_folder(**properties):
    properties['r_object_type'] = 'dm_folder'
    return _generate_resource(properties=properties)


def generate_sysobject(subtype=None, **properties):
    if subtype is None:
        properties['r_object_type'] = 'dm_sysobject'
    else:
        properties['r_object_type'] = subtype
    return _generate_resource(properties=properties)


def generate_object_aspects(*aspects):
    return _generate_resource(aspects=aspects)


def generate_document(**properties):
    properties['r_object_type'] = 'dm_document'
    return _generate_resource(properties=properties)


def generate_user(**properties):
    return _generate_resource(properties=properties)


def generate_group(**properties):
    return _generate_resource(properties=properties)


def generate_relation(**properties):
    return _generate_resource(type='dm_relation', properties=properties)


def generate_assist_value_request(**properties):
    return _generate_resource(properties=properties)


def generate_batch_request(*operations):
    batch_operations = [operation.raw_resource() for operation in operations]
    batch_request = {'operations': batch_operations}
    return _generate_resource(**batch_request)


def generate_batch_operation(batch_id, description, uri, method, entity=None, **headers):
    operation_headers = [{'name': k, 'value': v}
                         for k, v in headers.items()]

    request = {'uri': uri, 'method': method, 'headers': operation_headers}
    if entity is not None:
        request['entity'] = entity

    operation = {'id': batch_id, 'description': description, 'request': request}

    return _generate_resource(**operation)


def _generate_resource(**raw_resource):
    return Resource(raw_resource)
