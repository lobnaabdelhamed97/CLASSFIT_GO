view_game_schema = {
    'type': 'object',
    'properties': {
        'GmID': {'type': 'number', "minimum": 1},
        'PlyID': {'type': 'number', "minimum": 1},
        'ProjectKey': {'type': 'string', "minimum": 2},
        'ProjectSecret': {'type': 'string', "minimum": 2},
        'tkn': {'type': 'string', "minimum": 2},
        'dev_id': {'type': 'string', "minimum": 2},

    },
    'required': ['GmID', 'PlyID', 'ProjectKey', 'ProjectSecret', 'tkn', 'dev_id']
}
