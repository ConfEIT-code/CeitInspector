from copy import deepcopy


class PlainTextParser( object ):
    log_engine = None
    conf_path = ""
    options = {}
    format = ""
    conf_backup = ""
    add_new_options = True
    conf_parser = None
    option_dict = {}
    option_num = 0

    def __init__(self, conf_engine):
        self.log_engine = conf_engine.log_engine
        self.conf_path = conf_engine.conf_path
        self.options = {}
        self.format = conf_engine.format
        self.conf_backup = conf_engine.conf_backup
        self.add_new_options = conf_engine.add_new_options
        self.option_dict = conf_engine.option_dict
        self.option_num = conf_engine.option_num

    def read_conf(self):
        if self.add_new_options == True:
            for i in range( self.option_num ):
                i = i + 1
                temp = deepcopy( self.option_dict["optionList"][str( i )] )
                value = self.get_value( temp["key"] )
                if value == None:
                    self.log_engine.info( "Option not found: " + temp["key"] )
                    if self.add_new_options == True:
                        self.log_engine.info( "Add new options" )
                        self.add_option( temp )
                        self.options[str( i )] = temp
                    else:
                        self.log_engine.info( "Skip these options" )
                else:
                    temp["value"] = value
                    self.options[str( i )] = temp
            return self.options

        else:
            for i in range( self.option_num ):
                i = i + 1
                temp = deepcopy( self.option_dict["optionList"][str( i )] )
                if "value" not in temp:
                    value_list = []
                    for j in range( 99 ):
                        j = str( j + 1 )
                        try:
                            value = temp["value" + j]
                            value_list.append( value )
                        except:
                            pass
                    values = ' '.join( value_list )
                    temp["value"] = values
                self.options[str( i )] = temp
            return self.options

    def add_option(self, option):
        if option.has_key( "value" ):
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
            try:
                with open( self.conf_path, 'a' ) as fp:
                    fp.writelines( lines )
            except IOError:

                self.log_engine.error( "plain_text.py:60 | Configuration File Not Found" )

        elif option.has_key( "value1" ):
            value_list = []
            for i in range( 99 ):
                i = str( i + 1 )
                try:
                    value = option["value" + i]
                    value_list.append( value )
                except:
                    pass
            key = option["key"]
            values = ' '.join( value_list )
            option["value"] = values
            constraint = option["constraint"]
            new_option = self.format.replace( "$key", key )
            new_option = new_option.replace( "$value", values )
            lines = []
            lines.append( '\n' )
            lines.append( "#" + constraint + '\n' )
            lines.append( new_option + '\n' )
            try:
                with open( self.conf_path, 'a' ) as fp:
                    fp.writelines( lines )
            except IOError:

                self.log_engine.error( "plain_text.py:87 | Configuration File Not Found" )

    def get_value(self, key):
        try:
            with open( self.conf_path, 'r' ) as fp:
                lines = fp.readlines()
                for line in lines:
                    if key in line and line[0] != "#":
                        operator = self.format.strip( "$key" ).strip( "$value" )
                        value = line.lstrip().rstrip()
                        value = value.lstrip( key )
                        value = value.lstrip( operator )
                        return value
            return None
        except IOError:
            self.log_engine.error( "plain_text.py:702 | Configuration File Not Found" )
            return None

    def set_option(self, key, option):

        if self.add_new_options == True:

            temp_key = key
            new_key = option["key"]
            new_operator = option["operator"]
            new_value = option["value"]
            misconf = ""
            operator = ""
            value = ""
            if new_value != None:
                if "~" in new_value:
                    new_value = new_value.replace( "~", " " )
            try:
                with open( self.conf_path, 'r' ) as fp:
                    lines = fp.readlines()
                    for line in lines:
                        if key in line and line[0] != "#":
                            operator = self.format.strip( "$key" ).strip( "$value" )
                            value = line.lstrip().rstrip()
                            value = value.lstrip( key )
                            value = value.lstrip( operator )
                            if new_key != None:
                                key = new_key
                            if new_operator != None:
                                operator = new_operator
                            if new_value != None:
                                value = new_value
                            new_line = key + operator + value + "\n"
                            lines[lines.index( line )] = new_line
                            key = temp_key
                            break
                with open( self.conf_path, 'w' ) as fp:
                    fp.writelines( lines )
            except IOError:
                self.log_engine.error( "plain_text.py:73 | Configuration File Not Found" )
                return misconf

            misconf = key + operator + value
            return misconf

        else:
            new_key = option["key"]
            new_operator = option["operator"]
            new_value = option["value"]
            operator = self.format.strip( "$key" ).strip( "$value" )
            value = self.get_temp_value( key )

            if new_key != None:
                key = new_key
            if new_operator != None:
                operator = new_operator
            if new_value != None:
                if "~" in new_value:
                    new_value = new_value.replace( "~", " " )
                value = new_value

            try:
                new_line = key + operator + value + "\n"
                with open( self.conf_path, 'a' ) as fp:
                    fp.writelines( new_line )
            except IOError:
                self.log_engine.error( "plain_text.py:73 | Configuration File Not Found" )
            misconf = key + operator + value
            return misconf

    def get_temp_value(self, key):
        for key1, value in self.options.iteritems():
            if value["key"] == key:
                return value["value"]
            else:
                self.log_engine.error( "get_temp_value error: key not found!" )
