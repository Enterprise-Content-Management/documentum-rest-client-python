import json


def prompt_user(message):
    return input(message)


def print_properties(logger, prop_collection, *properties):
    info = []
    for prop in properties:
        info.append('%s: %s' % (prop, prop_collection.get(prop)))
    logger.info('>%s\n', ", ".join(info))


def print_resource_properties(logger, res, *properties):
    print_properties(logger, res.get('properties'), *properties)


def format_json(raw_str):
    return json.dumps(json.loads(raw_str))
