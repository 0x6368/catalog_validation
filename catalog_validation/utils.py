import re


CACHED_CATALOG_FILE_NAME = 'catalog.json'
METADATA_JSON_SCHEMA = {
    'type': 'object',
    'properties': {
        'runAsContext': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string'},
                    'gid': {'type': 'integer'},
                    'groupName': {'type': 'string'},
                    'userName': {'type': 'string'},
                    'uid': {'type': 'integer'},
                },
                'required': ['description'],
            },
        },
        'capabilities': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string'},
                    'name': {'type': 'string'},
                },
                'required': ['description', 'name'],
            },
        },
        'hostMounts': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string'},
                    'hostPath': {'type': 'string'},
                },
                'required': ['description', 'hostPath'],
            },
        },
    },
}
VALID_TRAIN_REGEX = re.compile(r'^\w+[\w.-]*$')
WANTED_FILES_IN_ITEM_VERSION = {'questions.yaml', 'app-readme.md', 'Chart.yaml', 'README.md'}


def validate_key_value_types(data_to_check, mapping, verrors, schema):
    for key_mapping in mapping:
        if len(key_mapping) == 2:
            key, value_type, required = *key_mapping, True
        else:
            key, value_type, required = key_mapping

        if required and key not in data_to_check:
            verrors.add(f'{schema}.{key}', f'Missing required {key!r} key.')
        elif key in data_to_check and not isinstance(data_to_check[key], value_type):
            verrors.add(f'{schema}.{key}', f'{key!r} value should be a {value_type.__name__!r}')
