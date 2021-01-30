# encoding: UTF-8
import json

OPTION_LIST_FILE = "/Users/Leo/Desktop/core_option_list.txt"
JSON_FILE = "/Users/Leo/Desktop/core_option_list.json"

json_template = {
    "optionList": {
    },
    "format": "$key $value"
}

COUNT = 0
with open( OPTION_LIST_FILE ) as fp:
    lines = fp.readlines()
    for line in lines:
        elements = line.split()
        # if elements.__len__() > 2:
        if elements.__len__() == 3:
            option_name = elements[0]
            option_value = elements[1]
            option_constraint = elements[2]
            COUNT += 1
            json_template["optionList"][str( COUNT )] = {"key": option_name, "value": option_value,
                                                         "constraint": option_constraint}
        elif elements.__len__() == 4:
            option_name = elements[0]
            option_value1 = elements[1]
            option_value2 = elements[2]
            option_constraint = elements[3]
            COUNT += 1
            json_template["optionList"][str(COUNT)] = {"key": option_name, "value1": option_value1,
                                                       "value2": option_value2,
                                                       "constraint": option_constraint}
        elif elements.__len__() == 5:
            option_name = elements[0]
            option_value1 = elements[1]
            option_value2 = elements[2]
            option_value3 = elements[3]
            option_constraint = elements[4]
            COUNT += 1
            json_template["optionList"][str(COUNT)] = {"key": option_name, "value1": option_value1,
                                                       "value2": option_value2, "value3": option_value3,
                                                       "constraint": option_constraint}
        elif elements.__len__() == 6:
            option_name = elements[0]
            option_value1 = elements[1]
            option_value2 = elements[2]
            option_value3 = elements[3]
            option_value4 = elements[4]
            option_constraint = elements[5]
            COUNT += 1
            json_template["optionList"][str(COUNT)] = {"key": option_name, "value1": option_value1,
                                                       "value2": option_value2, "value3": option_value3,
                                                       "value4": option_value4,
                                                       "constraint": option_constraint}
        elif elements.__len__() == 7:
            option_name = elements[0]
            option_value1 = elements[1]
            option_value2 = elements[2]
            option_value3 = elements[3]
            option_value4 = elements[4]
            option_value5 = elements[5]
            option_constraint = elements[6]
            COUNT += 1
            json_template["optionList"][str(COUNT)] = {"key": option_name, "value1": option_value1,
                                                       "value2": option_value2, "value3": option_value3,
                                                       "value4": option_value4, "value5": option_value5,
                                                       "constraint": option_constraint}


with open( JSON_FILE, 'w' ) as fp:
    json.dump( json_template, fp )

# json formalization website: http://tool.oschina.net/codeformat/json
import webbrowser

webbrowser.open( "http://www.kjson.com/jsonformat/?f=1" )
