import contextlib
import git
import os

from datetime import datetime
from typing import Optional

from catalog_validation.schema.migration_schema import MIGRATION_DIRS
from catalog_validation.utils import VALID_TRAIN_REGEX


DEVELOPMENT_DIR = 'ix-dev'
RECOMMENDED_APPS_FILENAME = 'recommended_apps.yaml'
RECOMMENDED_APPS_SCHEMA = {
    'type': 'object',
    'patternProperties': {
        '.*': {
            'type': 'array',
            'items': {'type': 'string'},
        }
    },
}
TRAIN_IGNORE_DIRS = ['library', 'docs', DEVELOPMENT_DIR] + MIGRATION_DIRS


ACL_QUESTION = [
    {
        'variable': 'path',
        'label': 'Path',
        'description': 'Path to perform ACL',
        'schema': {
            'type': 'string',
            'required': True,
            'empty': False,
        }
    },
    {
        'variable': 'entries',
        'label': 'ACL Entries',
        'description': 'ACL Entries',
        'schema': {
            'type': 'list',
            'items': [{
                'variable': 'aclEntry',
                'label': 'ACL Entry',
                'schema': {
                    'type': 'dict',
                    'attrs': [
                        {
                            'variable': 'id_type',
                            'label': 'ID Type',
                            'schema': {
                                'type': 'string',
                                'enum': [
                                    {'value': 'USER', 'description': 'Entry is for a USER'},
                                    {'value': 'GROUP', 'description': 'Entry is for a GROUP'},
                                ],
                                'default': 'USER',
                            }
                        },
                        {
                            'variable': 'id',
                            'label': 'ID',
                            'schema': {
                                'type': 'int',
                                'required': True,
                                'min': 0,
                            }
                        },
                        {
                            'variable': 'access',
                            'label': 'Access',
                            'schema': {
                                'type': 'string',
                                'enum': [
                                    {'value': 'READ', 'description': 'Read Access'},
                                    {'value': 'MODIFY', 'description': 'Modify Access'},
                                    {'value': 'FULL_CONTROL', 'description': 'FULL_CONTROL Access'},
                                ],
                            }
                        }
                    ],
                }
            }]
        }
    }
]

IX_VOLUMES_ACL_QUESTION = [
    {
        'variable': 'path',
        'label': 'Path',
        'description': 'Path to perform ACL',
        'schema': {
            'type': 'string',
            'hidden': True
        }
    },
    ACL_QUESTION[1]
]


def get_catalog_json_schema() -> dict:
    return {
        'type': 'object',
        'patternProperties': {
            '.*': {
                'type': 'object',
                'title': 'Train',
                'patternProperties': {
                    '.*': {
                        'type': 'object',
                        'title': 'Item',
                        'properties': {
                            'name': {
                                'type': 'string',
                                'title': 'Name',
                            },
                            'categories': {
                                'type': 'array',
                                'items': {
                                    'type': 'string'
                                },
                            },
                            'app_readme': {
                                'type': 'string',
                            },
                            'location': {
                                'type': 'string',
                            },
                            'healthy': {
                                'type': 'boolean',
                            },
                            'healthy_error': {
                                'type': ['string', 'null'],
                            },
                            'last_update': {
                                'type': ['string', 'null'],
                            },
                            'latest_version': {
                                'type': 'string',
                            },
                            'latest_app_version': {
                                'type': 'string',
                            },
                            'latest_human_version': {
                                'type': 'string',
                            },
                            'description': {
                                'type': ['string', 'null'],
                            },
                            'title': {
                                'type': 'string',
                            },
                            'icon_url': {
                                'type': ['string', 'null'],
                            },
                            'maintainers': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {'type': 'string'},
                                        'url': {'type': ['string', 'null']},
                                        'email': {'type': 'string'}
                                    },
                                    'required': ['name', 'email'],
                                }
                            },
                        },
                        'required': [
                            'name', 'categories', 'location', 'healthy', 'icon_url',
                            'latest_version', 'latest_app_version', 'latest_human_version',
                            'last_update', 'recommended', 'healthy_error',
                        ],
                    }
                }

            }
        }
    }


def get_last_updated_date(repo_path: str, folder_path: str) -> Optional[str]:
    with contextlib.suppress(Exception):
        # We don't want to fail querying items if for whatever reason this fails
        repo = git.Repo(repo_path)
        latest_commit = next(repo.iter_commits(paths=folder_path, max_count=1), None)
        if latest_commit:
            timestamp = datetime.fromtimestamp(latest_commit.committed_date)
            return timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None


def valid_train(train_name: str, train_location: str) -> bool:
    return VALID_TRAIN_REGEX.match(
        train_name
    ) and not train_name.startswith('.') and train_name not in TRAIN_IGNORE_DIRS and os.path.isdir(train_location)
