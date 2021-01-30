from copy import deepcopy
from xml.etree import ElementTree


class HdfsParser( object ):
    log_engine = None
    conf_path = ""
    options = {}
    format = ""
    conf_backup = ""
    add_new_options = True
    conf_parser = None
    option_dict = {}
    option_num = 0
    curXmlTree = None
    curXmlRoot = None

    def __init__(self, conf_engine):
        self.log_engine = conf_engine.log_engine
        self.conf_path = conf_engine.conf_path
        self.options = {}
        self.format = conf_engine.format
        self.conf_backup = conf_engine.conf_backup
        self.add_new_options = conf_engine.add_new_options
        self.option_dict = conf_engine.option_dict
        self.option_num = conf_engine.option_num
        self.curXmlTree = ElementTree.ElementTree()
        self.curXmlTree.parse(self.conf_path)
        self.curXmlRoot = self.curXmlTree.getroot()

    def read_conf(self):
        if self.add_new_options == True:
            for i in range( self.option_num ):
                i = i + 1
                temp = deepcopy( self.option_dict["optionList"][str( i )] )
                value = self.get_value( temp["key"] )
                if value == None:
                    self.log_engine.info( "Option not found: " + temp["key"] )
                    self.log_engine.info( "Add new options" )
                    self.add_option( temp )
                    self.options[str( i )] = temp
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

            newItem = ElementTree.SubElement(self.curXmlRoot, "property")
            itemKey = ElementTree.SubElement(newItem, "name")
            itemKey.text = key
            itemValue = ElementTree.SubElement(newItem, "value")
            itemValue.text = value

            try:
                self.curXmlTree.write(self.conf_path)
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

            newItem = ElementTree.SubElement(self.curXmlRoot, "property")
            itemKey = ElementTree.SubElement(newItem, "name")
            itemKey.text = key
            for i in range(len(value_list)):
                curValue = value_list[i]
                if "~" in curValue:
                    curValue = curValue.replace( "~", " " )
                curIdx = i + 1
                itemCurValue = ElementTree.SubElement(newItem, "value" + curIdx)
                itemCurValue.text = curValue
            
            option["value"] = values # add new option to current option list
            try:
                self.curXmlTree.write(self.conf_path)
            except IOError:
                self.log_engine.error( "plain_text.py:87 | Configuration File Not Found" )

    def get_value(self, key):
        try:
            for node in self.curXmlRoot:
                if node.tag == "property":
                    foundFlag = False
                    tempValue = ""
                    for item in node:
                        if item.tag == "name" and item.text == key:
                            foundFlag = True
                        elif item.tag == "value":
                            tempValue = item.text
                    if foundFlag:
                        return tempValue
            return None
        except IOError:
            self.log_engine.error( "plain_text.py:702 | Configuration File Not Found" )
            return None

    def set_option(self, key, option):
        new_key = option["key"]
        new_value = option["value"]
        misconf = ""
        value = ""
        if new_value != None:
            if "~" in new_value:
                new_value = new_value.replace( "~", " " )
        try:
            foundFlag = False
            if new_key != None:
                key = new_key
            if new_value != None:
                value = new_value
            
            for node in self.curXmlRoot:
                if node.tag == "property":
                    for item in node:
                        if item.tag == "name" and item.text == key:
                            foundFlag = True
                    if foundFlag:
                        for item in node:
                            if item.tag == "value":
                                item.text = value
                            elif item.tag == "name":
                                item.text = key
                        break
            if foundFlag == False:
                newItem = ET.SubElement(self.curXmlRoot, "property")
                itemKey = ET.SubElement(newItem, "name")
                itemKey.text = key
                itemValue = ET.SubElement(newItem, "value")
                itemValue.text = value
            
            self.curXmlTree.write(self.conf_path)
            
        except IOError:
            self.log_engine.error( "plain_text.py:73 | Configuration File Not Found" )
            return misconf

        misconf = key + " " + value
        return misconf

    def get_temp_value(self, key):
        for key1, value in self.options.iteritems():
            if value["key"] == key:
                return value["value"]
        return None
