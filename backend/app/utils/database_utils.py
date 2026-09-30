import json


def list_to_json(items):
    return json.dumps(items)


def json_to_list(value):
    if not value:
        return []

    return json.loads(value)