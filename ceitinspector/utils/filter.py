# -*- coding:utf-8 -*-

from file_system_utils import get_files_in_dir

files = get_files_in_dir("/Users/Leo/Desktop/Docker/Httpd", recursion=False)["/Users/Leo/Desktop/Docker/Httpd"]
di = {}
for f in files:
    if "console" in f:
        with open("/Users/Leo/Desktop/Docker/Httpd/" + f, 'r') as fp:
            content = fp.read()
            if "Result:" in content:
                di[f] = content.split("Result: ")[-1].split("\n")[0]
            else:
                print f
values = {}
for k,v in di.items():
    if v not in values:
        values[v] = [k]
    else:
        values[v].append(k)

for k,v in values.items():
    print k
    print [i.split("_")[0] for i in v ]
    print v.__len__()