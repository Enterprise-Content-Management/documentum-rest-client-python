import collections
import json


class Sort(object):
    def __init__(self, prop, ascending, lang, is_ascii):
        self.property = prop
        self.ascending = ascending
        self.lang = lang
        self.ascii = is_ascii

    def as_dict(self):
        return {
            "property": self.property,
            "ascending": self.ascending,
            "lang": self.lang,
            "ascii": self.ascii
        }

    def __repr__(self):
        return 'Sort({}, {}, {}, {})'.format(self.property, self.ascending, self.lang, self.ascii)


class Location(object):
    def __init__(self, location_type, repository, descendent, value):
        self.location_type = location_type
        self.repository = repository
        self.descendent = descendent
        self.value = value

    def as_dict(self):
        location = collections.OrderedDict([
            ('location-type', self.location_type),
            ('repository', self.repository),
            ('descendent', self.descendent)
        ])

        if self.location_type == 'id-location':
            location['id'] = self.value
        elif self.location_type == 'path-location':
            location['path'] = self.value

        return location

    def __repr__(self):
        return 'Location({},{},{},{})'.format(self.location_type, self.repository, self.descendent, self.value)


class ExpSet(object):
    def __init__(self, operator, *expressions):
        self.operator = operator
        self.expressions = expressions

    def as_dict(self):
        return collections.OrderedDict([("expression-type", "expression-set"),
                                        ("operator", self.operator),
                                        ("expressions", [exp.as_dict() for exp in self.expressions])])

    def __repr__(self):
        return 'ExpSet({}, {})'.format(self.operator, self.expressions)


class FtExp(object):
    def __init__(self, value, fuzzy=True, is_template=False):
        self.value = value
        self.fuzzy = fuzzy
        self.is_template = is_template

    def as_dict(self):
        return collections.OrderedDict([
            ("expression-type", "fulltext"),
            ("value", self.value),
            ("fuzzy", self.fuzzy),
            ("template", self.is_template)
        ])

    def __repr__(self):
        return 'FtExp({}, {})'.format(self.value, self.fuzzy)


class FacetDefinition(object):
    def __init__(self, facet_id, attributes, properties=None, group_by='string', sort='NONE', max_values=10):
        self.facet_id = facet_id
        self.attributes = attributes
        self.group_by = group_by
        self.sort = sort
        self.properties = properties
        self.max_values = max_values

    def as_dict(self):
        return {
            "id": self.facet_id,
            "attributes": self.attributes,
            "group-by": self.group_by,
            "sort": self.sort,
            "properties": self.properties,
            "max-values": self.max_values
        }


class QueryDocument(object):
    def __init__(self):
        self.all_versions = True
        self.include_hidden_objects = True
        self.max_results_for_facets = 10
        self.types = []
        self.columns = []
        self.collections = []
        self.sorts = []
        self.locations = []
        self.expression_set = ExpSet('OR')
        self.facet_definitions = []

    def dump(self):
        aql = {'all-versions': self.all_versions, 'include-hidden-objects': self.include_hidden_objects,
               'max-results-for-facets': self.max_results_for_facets, 'types': self.types, 'columns': self.columns,
               'collections': self.collections, 'sorts': [sort.as_dict() for sort in self.sorts],
               'locations': [location.as_dict() for location in self.locations],
               'expression-set': self.expression_set.as_dict(),
               'facet-definitions': [facet.as_dict() for facet in self.facet_definitions]}

        return json.dumps(aql, indent=4)

    def __repr__(self):
        return 'RestQuery({},\n{},\n{},\n{},\n{},\n{},\n{},\n{},\n{},\n)'.format(self.all_versions,
                                                                                 self.include_hidden_objects,
                                                                                 self.max_results_for_facets,
                                                                                 self.types,
                                                                                 self.columns,
                                                                                 self.collections,
                                                                                 self.sorts,
                                                                                 self.locations,
                                                                                 self.expression_set)

    def __str__(self):
        return self.dump()
