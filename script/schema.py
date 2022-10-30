schema = {
    'bulk': {
        'required': True,
        'schema': {
            'edit': {
                'required': True,
                'schema': {
                    'files': {
                        "type": "list",
                        'required': True,
                        "schema":
                            {
                                "type": "dict",
                                "schema": {

                                    'path': {
                                        'required': True,
                                        'type': 'string'
                                    },
                                    'changes': {
                                        "type": "list",
                                        'required': True,
                                        "schema": {
                                            'type': 'dict',
                                            'required': True,
                                            'schema': {
                                                'from': {'type': 'string', 'required': True},
                                                'to': {'type': 'string', 'required': True},
                                            }
                                        }
                                    }

                                }
                            }
                    },
                    'github': {
                        'required': True,
                        'schema': {
                            'branch': {
                                'required': True,
                                'type': 'string'
                            },
                            'commit': {
                                'required': True,
                                'type': 'string'
                            },
                            'cancel': {
                                'required': True,
                                'schema': {
                                    'pipeline': {
                                        'required': True,
                                        'type': 'boolean'
                                    }
                                }
                            }
                        }
                    },
                    'repos': {
                        'required': True,
                        'type': 'string'
                    }
                }
            },

        }
    }
}
