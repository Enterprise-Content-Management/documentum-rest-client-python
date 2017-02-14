import collections

from model.QueryDocument import QueryDocument
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


def generate_query_document(all_versions=True, include_hidden_objects=True, max_results_for_facets=10,
                            types=('dm_sysobject',),
                            columns=tuple(), sorts=tuple(), locations=tuple(), cs_collections=tuple(),
                            expression_set=None,
                            facet_definitions=tuple()):
    query_doc = QueryDocument()
    query_doc.all_versions = all_versions
    query_doc.include_hidden_objects = include_hidden_objects
    query_doc.max_results_for_facets = max_results_for_facets
    query_doc.types = types
    query_doc.columns = columns
    query_doc.sorts = sorts
    query_doc.locations = locations
    query_doc.collections = cs_collections
    query_doc.expression_set = expression_set
    query_doc.facet_definitions = facet_definitions
    return query_doc


def generate_saved_search(name, description, is_public, query_doc):
    properties = {'object_name': name, 'title': description, 'r_is_public': is_public}
    raw_saved_search = {'properties': properties,
                        'query-document': query_doc.dump()}
    return _generate_resource(**raw_saved_search)


def generate_search_template(name, description, is_public, query_doc):
    properties = {'object_name': name, 'subject': description, 'r_is_public': is_public}
    raw_saved_search = {'properties': properties,
                        'query-document-template': query_doc.dump()}
    return _generate_resource(**raw_saved_search)


def generate_search_template_variables(variables, prompt_var):
    external_variables = {'external-variables': [_fill_variable_value(variable.get('id'), variable.get('variable-type'),
                                                                      prompt_var(variable.get('id'),
                                                                                 variable.get('variable-value')),
                                                                      variable.get('variable-value'))
                                                 for variable in variables]}
    return _generate_resource(**external_variables)


def _fill_variable_value(variable_id, variable_type, value, original_value):
    variable = collections.OrderedDict()
    variable['variable-type'] = variable_type
    variable['id'] = variable_id

    if value:
        variable['variable-value'] = value
    else:
        variable['variable-value'] = original_value

    return variable


def _generate_resource(**raw_resource):
    return Resource(raw_resource)
