# -*- coding:utf-8 -*-
from copy import deepcopy
from ceitinspector.utils import file_system_utils
from ceitinspector.core import config

class NginxParser( object ):
    def __init__(self, conf_engine):

        self.log_engine = conf_engine.log_engine
        self.test_path = config.config.test_path
        self.conf_path = ""
        self.options = {}
        self.format = conf_engine.format
        self.conf_backup = conf_engine.conf_backup
        self.add_new_options = conf_engine.add_new_options
        self.option_dict = conf_engine.option_dict
        self.option_num = conf_engine.option_num

        """

        self.conf_path = "/Users/Leo/Desktop/Docker/nginx-tests"
        self.format = "$key $value;"
        self.options = {}
        self.add_new_options = True
        self.option_dict = {
    "optionList": {
        "1": {
            "value": "localhost",
            "key": "server_name",
            "constraint": "STR",
            "locale" : "server"
        },
        "2": {
            "value": "localhost",
            "key": "test_key",
            "constraint": "STR",
            "locale" : "server"
        }
    },
    "format": "$key $value;"
}
        
        self.option_num = 2
        """

    def read_conf(self):
        for i in range( self.option_num ):
            i = i + 1
            temp = deepcopy( self.option_dict["optionList"][str( i )] )
            self.options[str( i )] = temp
        return self.option_dict["optionList"]

    def transfer_nginx_conf(self, index):
        file_tuple = file_system_utils.get_files_in_dir(self.test_path)
        for dir, files in file_tuple.items():
            for file in files:
                file_path = dir + '/' + file
                self.conf_path = file_path
                i = index
                temp = deepcopy( self.option_dict["optionList"][str( i )] )
                value = self.get_value( temp["key"] )

                if value == None:
                    self.add_option( temp )
                else:
                    pass

        return

    def add_option(self, option):
        locale = option["locale"].split('|')[0]
        if option.has_key("value"):
            key = option["key"]
            value = option["value"]
            if "~" in value:
                value = value.replace( "~", " " )
            constraint = option["constraint"]
            new_option = self.format.replace( "$key", key )
            new_option = new_option.replace( "$value", value )
            lines = []
            lines.append( '\n' )
            lines.append( "#" + constraint + '\n' )
            lines.append( new_option + '\n' )
            if ".t" in self.conf_path and "txt" not in self.conf_path:
                with open( self.conf_path, 'r' ) as fp:

                    temp_lines2write = []
                    old_lines = fp.readlines()
                    start = False
                    stop = False
                    add_flag = False
                    for line in old_lines:
                        if "%%TEST_GLOBALS%%" in line:
                            start = True
                        elif "EOF" in line and "nginx.conf" not in line:
                            stop = True
                        else:
                            pass

                        if start == True and stop == False:
                            if locale != "main":
                                if locale in line.split() and "{" in line.split():
                                    temp_lines2write.append(line)
                                    temp_lines2write.extend(lines)
                                else:
                                    temp_lines2write.append(line)
                            else:
                                if add_flag == False:
                                    temp_lines2write.append( line )
                                    temp_lines2write.extend( lines )
                                    add_flag = True
                                else:
                                    temp_lines2write.append( line )
                        else:
                            temp_lines2write.append( line )
                #print temp_lines2write
                with open(self.conf_path, 'w') as fp:

                    fp.writelines(temp_lines2write)

        elif option.has_key("value1"):

            value_list = []
            for i in range(99):
                i = str(i+1)
                try:
                    value = option["value"+i]
                    value_list.append(value)
                except:
                    pass
            key = option["key"]
            values = ' '.join(value_list)
            option["value"] = values
            if "~" in values:
                values = values.replace( "~", " " )
            constraint = option["constraint"]
            new_option = self.format.replace( "$key", key )
            new_option = new_option.replace( "$value", values )
            lines = []
            lines.append( '\n' )
            lines.append( "#" + constraint + '\n' )
            lines.append( new_option + '\n' )
            if ".t" in self.conf_path and "txt" not in self.conf_path:
                with open( self.conf_path, 'r' ) as fp:

                    temp_lines2write = []
                    old_lines = fp.readlines()
                    start = False
                    stop = False
                    add_flag = False
                    for line in old_lines:
                        if "%%TEST_GLOBALS%%" in line:
                            start = True
                        elif "EOF" in line and "nginx.conf" not in line:
                            stop = True
                        else:
                            pass
                        if start == True and stop == False:
                            if locale != "main":
                                if locale in line.split() and "{" in line.split():
                                    temp_lines2write.append(line)
                                    temp_lines2write.extend(lines)
                                else:
                                    temp_lines2write.append(line)
                            else:
                                if add_flag == False:
                                    temp_lines2write.append( line )
                                    temp_lines2write.extend( lines )
                                    add_flag = True
                                else:
                                    temp_lines2write.append( line )
                        else:
                            temp_lines2write.append( line )
                #print temp_lines2write
                with open(self.conf_path, 'w') as fp:

                    fp.writelines(temp_lines2write)


    def get_value(self, key):
        try:
            with open( self.conf_path, 'r' ) as fp:
                lines = fp.readlines()
                start = False
                stop = False
                for line in lines:
                    if "TEST_GLOBALS" in line:
                        start = True
                    elif "EOF" in line and "nginx.conf" not in line:
                        stop = True
                    else:
                        pass
                    if start == True and stop == False:
                        if key in line.split() and line[0] != "#":
                            operator = " "
                            value = line.lstrip().rstrip()
                            value = value.lstrip(key)
                            value = value.lstrip(operator).rstrip(';')
                            return value
                    else:
                        pass
            if start == True and stop == True:
                return None
            else:
                self.log_engine.debug( "CONFIGURATION NOT FOUND IN: " + self.conf_path)
        except IOError:
            #self.log_engine.error( "plain_text.py:702 | Configuration File Not Found" )
            return None

    def set_option(self, key, option):
        temp_key = key
        new_key = option["key"]
        new_operator = option["operator"]
        new_value = option["value"]
        misconf = ""
        if new_value != None:
            if "~" in new_value:
                new_value = new_value.replace( "~", " " )
        file_tuple = file_system_utils.get_files_in_dir(self.test_path)
        for dir, files in file_tuple.items():
            for file in files:
                file_path = dir + '/' + file
                self.conf_path = file_path
                try:
                    with open( self.conf_path, 'r' ) as fp:
                        start = False
                        stop = False
                        lines = fp.readlines()
                        for line in lines:
                            if "TEST_GLOBALS" in line:
                                start = True
                            elif "EOF" in line and "nginx.conf" not in line:
                                stop = True
                            else:
                                pass
                            if start == True and stop == False:
                                if key in line.split() and line[0] != "#":
                                    if key in line.split() and line[0] != "#":
                                        operator = self.format.strip( "$key" ).strip( "$value;" )
                                        value = line.lstrip().rstrip( ';\n' )
                                        value = value.lstrip( key )
                                        value = value.lstrip( operator )
                                        if new_key != None:
                                            key = new_key
                                        if new_operator != None:
                                            operator = new_operator
                                        if new_value != None:
                                            value = new_value
                                        new_line = key + operator + value + ";\n"
                                        lines[lines.index( line )] = new_line
                                        key = temp_key
                            else:
                                pass

                    with open( self.conf_path, 'w' ) as fp:
                        fp.writelines( lines )

                except IOError:
                    self.log_engine.error( "plain_text.py:73 | Configuration File Not Found" )

        misconf = ""
        return misconf

