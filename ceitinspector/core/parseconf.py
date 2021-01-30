import json
#from ceitinspector.modules.conf_parser import PlainTextParser, AugeasParser, ElektraParser, NginxParser
from ceitinspector.modules.conf_parser import PlainTextParser, NginxParser, HdfsParser
from subprocess import Popen
from ceitinspector.core import config

class ConfEngine( object ):
    log_engine = None
    conf_path = ""
    conf_parse_mode = ""
    # options = {"id" : {"key": "hello", "value" : 1, "constraint" : ""}}
    options = {}
    format = ""
    conf_backup = ""
    add_new_options = True
    conf_parser = None
    option_dict = {}
    option_num = 0

    def __init__(self, log_engine, conf_path, conf_parse_mode, add_new_options):
        self.log_engine = log_engine
        self.log_engine.info( "ConfEngine Startup." )
        self.conf_path = conf_path
        self.conf_parse_mode = conf_parse_mode
        self.add_new_options = add_new_options
        try:
            with open( self.conf_path, 'r' ) as fp:
                self.conf_backup = fp.read()
        except IOError:
            self.log_engine.error("Configuration File Not Found")
        option_list_path = "option_list.json"
        with open( option_list_path, 'r' ) as fp:
            content = fp.read()
            self.option_dict = json.loads( content )
            self.format = self.option_dict["format"]
            self.option_num = self.option_dict["optionList"].__len__()
        if self.conf_parse_mode == "PlainText":
            self.conf_parser = PlainTextParser( self )
        elif self.conf_parse_mode == "Augeas":
            self.conf_parser = AugeasParser( self )
        elif self.conf_parse_mode == "Elektra":
            self.conf_parser = ElektraParser( self )
        elif self.conf_parse_mode == "Nginx":
            self.conf_parser = NginxParser( self )
        elif self.conf_parse_mode == "HDFS":
            self.conf_parser = HdfsParser( self )
        else:
            self.log_engine.error( "Not found conf_parse_mode")

    def read_conf(self):

        self.options = self.conf_parser.read_conf()

        return self.options

    def add_option(self, option):

        self.conf_parser.add_option( option )

    def get_value(self, key):

        value = self.conf_parser.get_value( key )
        return value

    def set_value(self, key, value):

        self.conf_parser.set_key( key, value )

    def set_option(self, key, option):

        return self.conf_parser.set_option( key, option )

    def recoverConf(self):
        if self.conf_parse_mode == "Nginx":
            backup_dir = config.config.nginx.nginx_backup_dir
            test_dir = config.config.test_path
            try:
                res = Popen("cp " + backup_dir + " " + test_dir + " -rf", shell=True)
                res.wait()
            except:
                self.log_engine.error("parseconf.py:75 | Configuration File Not Found")
        else:
            try:
                with open( self.conf_path, 'w' ) as fp:
                    fp.write( self.conf_backup )
                if self.conf_parse_mode == "HDFS":
                    self.conf_parser = HdfsParser( self )
            except IOError:
                self.log_engine.error("parseconf.py:75 | Configuration File Not Found")

    def set_test_path(self, test_path):
        self.conf_parser.test_path = test_path
