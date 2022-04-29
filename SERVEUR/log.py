#!/usr/bin/python
import logging
class LOG():
    def __init__(self,FILE_LOG):
        self.FILE_LOG = FILE_LOG

    def initialise_log(self):
        self.logging.basicConfig(
            filename=self.FILE_LOG,
            level=logging.DEBUG,\
            format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s'
        )





"""
exemple log :

LOG.logging.debug('Debug error')
LOG.logging.info('INFO ERROR')
LOG.logging.warning('Warning Error %s: %s', '01234', 'Erreur Oracle')
LOG.logging.error('error message')
LOG.logging.critical('critical error')
"""