import logging

class SMLog:
"""Custom logging class"""
    logging = {
        'version':1,
        'disable_existing_loggers':False,
        'handlers':{
            'file':{
                'level':'DEBUG',
                'class':'logging.Filehandler',
                'filename':'/var/log/app-logs/flask.log',

            },
        },
        'loggers':{
            'flask':{
                'handlers':['file'],
                'level':'DEBUG',
                'propagate':True,
            },
        },
    }
    def __init__(self):
        self.