# -*- coding:utf-8 -*-
import os
import re

mysql_manual_path = "/Users/Leo/Desktop/FSE/配置项/MYSQL-100/refman-8.0-en.html-chapter"

parameter_list_path = "server-administration.html"

class Parameter(object):
    name = ""
    link = ""
    command_line = ""
    option_file = ""
    system_value = ""
    status_value = ""
    value_scope = ""
    dynamic = ""
    type = ""
    default_value = ""

    def __init__(self, content, parameter_name):
        content_vars = content.split(parameter_name)[1].split('</tr><tr><td scope="row">')[0]
        self.link = parameter_name.split('<a class="link" href="')[1].split('">')[0]
        self.name = parameter_name.split('">')[1].split('</a>')[0]
        self.command_line = content_vars.split('<td>')[1].split('</td>')[0]
        self.option_file = content_vars.split('<td>')[2].split('</td>')[0]
        self.system_value = content_vars.split('<td>')[3].split('</td>')[0]
        self.status_value = content_vars.split('<td>')[4].split('</td>')[0]
        self.value_scope = content_vars.split('<td>')[5].split('</td>')[0]
        self.dynamic = content_vars.split('<td>')[6].split('</td>')[0]

def relative_path(root, path):
    return mysql_manual_path + os.sep + path

def generate_details(ls):
    for parameter in ls:
        print "Parameter: " + parameter.name
        link = parameter.link.split('#')[0]
        keyword = parameter.link.split('#')[1]
        #print keyword
        with open(relative_path(mysql_manual_path, link), 'r') as fp:
            content = fp.read()
            try:
                details_string = content.split('<li class="listitem"><p><a name="'+keyword+'"></a>')[1].split('</li>')[0]
                if '<strong>Type</strong></span></td>\n<td>' in details_string:
                    parameter.type = details_string.split('<strong>Type</strong></span></td>\n<td>')[1].split('</td>')[0]
                if '<strong>Default Value</strong></span></td>\n<td><code class="literal">' in details_string:
                    parameter.default_value = details_string.split('<strong>Default Value</strong></span></td>\n<td><code class="literal">')[1].split('</code>')[0]
            except IndexError:
                print "list index out of range"
        print "Type: " + parameter.type
        print "Default Value: " + parameter.default_value

def search(dic, str):
    temp_ls = []
    for key, value in dic.items():
        if str in key:
            if value.option_file == "Yes":
                temp_ls.append(value)
    return temp_ls

with open(relative_path(mysql_manual_path, parameter_list_path), 'r') as fp:
    content = fp.read()
    pattern = '<a class="link" href=".+'
    match_list = re.findall(pattern, content)
    para_dict = {}
    for parameter_name in match_list:
        new_parameter = Parameter(content, parameter_name)
        para_dict[new_parameter.name] = new_parameter


keyword = "innodb"
results = search(para_dict, keyword)
generate_details(results)


