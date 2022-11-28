schema = {
    'bulk': {
        'required': True,
        'schema': {
            'edit': {
                'schema': {
                    'files': {
                        "type": "list",
                        'required': True,
                        "schema":
                            {
                                "type": "dict",
                                "schema": {
                                    'absolute-path': {
                                        'required': False,
                                        'type': 'string'
                                    },
                                    'find-folder': {
                                        'required': False,
                                        'type': 'string'
                                    },
                                    'find-file': {
                                        'required': False,
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
            'create': {
                'schema': {
                    'files': {
                        "type": "list",
                        'required': True,
                        "schema":
                            {
                                "type": "dict",
                                "schema": {

                                    'filename': {
                                        'required': True,
                                        'type': 'string'
                                    },
                                    'destination': {
                                        'required': True,
                                        'type': 'string'
                                    },

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
            'pr': {
                'schema': {
                    'from': {'type': 'string', 'required': True},
                    'to': {'type': 'string', 'required': True},
                    'name': {'type': 'string', 'required': True},
                    'body': {'type': 'string', 'required': True},
                    'assignee': {'type': 'string', 'required': True},
                    'cancel': {
                        'required': True,
                        'schema': {
                            'pipeline': {
                                'required': True,
                                'type': 'boolean'
                            }
                        }
                    },
                    'repos': {
                        'required': True,
                        'type': 'string'
                    }
                },
            }
        }
    }
}
