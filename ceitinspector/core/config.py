# -*- coding:utf-8 -*-
import json
from os import getcwd

SETTING_PATH = "setting.json"

config = None

class VoidConfig(object):
    def __init__(self):
        pass

class Config( object ):
    # Default Values

    core_config = {
        "root_path": "",
        "test_path": "",
        "software_name": "",
        "conf_path": "",
        "conf_parse_mode": "",
        "test_mode": "",
        "add_new_options": "",
        "interval": "",
        "log_file_path": "",
        "char2cut": "",
        "misconf_mode" :"",
    }
    httpd_config = {
        "signal_file_2_read" : "",
        "signal_file_2_write" : "",
        "convert_all_t_files" : "",
        "t_dir" : "",
        "backup_all_t_files": "",
        "httpd_backup_dir": "",
    }
    nginx_config = {
        "nginx_backup_dir": "",
    }



    httpd = VoidConfig()
    nginx = VoidConfig()
    # print config.root_path
    root_path = ""
    test_path = ""
    software_name = ""
    conf_path = ""
    conf_parse_mode = ""
    misconf_mode = ""
    log_file_path = ""
    add_new_options = ""
    char2cut = ""
    test_mode = ""
    interval = ""
    def __init__(self):

        self.load_setting()
        self.root_path = getcwd()
        global config
        config = self


    def load_setting(self, filePath=None):
        if filePath:
            pass
        else:
            filePath = SETTING_PATH
        with open( filePath, 'r' ) as fp:
            content = fp.read()
            dict = json.loads( content )
            for k, v in dict.items():
                if k in self.core_config:
                    setattr(self, k.decode('utf-8'), v)
                elif k in self.httpd_config:
                    setattr(self.httpd, k.decode('utf-8'), v)
                elif k in self.nginx_config:
                    setattr(self.nginx, k.decode('utf-8'), v)
                else:
                    print "unrecognized option: ", k


