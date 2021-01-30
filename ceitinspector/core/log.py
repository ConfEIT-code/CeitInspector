import datetime
import logging
import os
from ceitinspector.core import config
NOWTIME = datetime.datetime.now().strftime( '%Y-%m-%d-%H%M%S' )
LOGPATH = ""


class LogEngine( object ):
    LEVEL_DEBUG = logging.DEBUG
    LEVEL_INFO = logging.INFO
    LEVEL_WARN = logging.WARN
    LEVEL_ERROR = logging.ERROR
    LEVEL_CRITICAL = logging.CRITICAL

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        global LOGPATH
        LOGPATH = config.config.root_path + '/Log'

        self.logger = logging.getLogger()
        self.formatter = logging.Formatter( '%(asctime)s  %(levelname)s: %(message)s' )
        self.level = self.LEVEL_CRITICAL

        self.console_handler = None
        self.file_handler = None

        null_handler = logging.NullHandler()
        self.logger.addHandler( null_handler )

        self.mkdir()

        self.level_function_dict = {
            self.LEVEL_DEBUG: self.debug,
            self.LEVEL_INFO: self.info,
            self.LEVEL_WARN: self.warn,
            self.LEVEL_ERROR: self.error,
            self.LEVEL_CRITICAL: self.critical,
        }



    # ----------------------------------------------------------------------
    def set_log_level(self, level):

        self.logger.setLevel( level )
        self.level = level

    # ----------------------------------------------------------------------
    def add_console_handler(self):

        if not self.console_handler:
            self.console_handler = logging.StreamHandler()
            self.console_handler.setLevel( self.level )
            self.console_handler.setFormatter( self.formatter )
            self.logger.addHandler( self.console_handler )

    # ----------------------------------------------------------------------
    def add_file_handler(self):

        if not self.file_handler:
            filepath = LOGPATH + '/' + NOWTIME + '.log'
            self.file_handler = logging.FileHandler( filepath )
            self.file_handler.setLevel( self.level )
            self.file_handler.setFormatter( self.formatter )
            self.logger.addHandler( self.file_handler )

    # ----------------------------------------------------------------------
    def debug(self, msg):

        self.logger.debug( msg )

    # ----------------------------------------------------------------------
    def info(self, msg):

        self.logger.info( msg )

    # ----------------------------------------------------------------------
    def warn(self, msg):

        self.logger.warn( msg )

    # ----------------------------------------------------------------------
    def error(self, msg):

        self.logger.error( msg )

    # ----------------------------------------------------------------------
    def exception(self, msg):

        self.logger.exception( msg )

    # ----------------------------------------------------------------------
    def critical(self, msg):

        self.logger.critical( msg )

    # ----------------------------------------------------------------------
    def mkdir(self):
        if os.path.exists( LOGPATH ):
            pass
        else:
            os.makedirs( LOGPATH )


if __name__ == "__main__":
    le = LogEngine()
    le.set_log_level( le.LEVEL_DEBUG )
    le.add_console_handler()
    le.add_file_handler()
    le.info( u'info' )
    le.debug( u'debug' )
