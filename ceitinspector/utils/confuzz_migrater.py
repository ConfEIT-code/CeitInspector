# -*- coding:utf-8 -*-


nginx_dic = {
    "fuzzing" : "/Volumes/Transcend/Docker0304/nginx/Results/confuzz_nginx_fuzzing.csv",
    "conferr" : "/Volumes/Transcend/Docker0304/nginx/Results/confuzz_nginx_conferr.csv",
    "conftest" : "/Volumes/Transcend/Docker0304/nginx/Results/confuzz_nginx_conftest.csv",
    "from" : "/Volumes/Transcend/Docker0304/nginx/Results/indeterminate.xlsx",
    "out" : "/Volumes/Transcend/Docker0304/nginx/Results/confuzz_nginx1.xls"
}

httpd_dic = {
    "fuzzing": "/Volumes/Transcend/Docker0304/httpd1/Results/confuzz_httpd_fuzzing.csv",
    "conferr": "/Volumes/Transcend/Docker0304/httpd1/Results/confuzz_httpd_conferr.csv",
    "conftest": "/Volumes/Transcend/Docker0304/httpd1/Results/confuzz_httpd_conftest.csv",
    "from" : "/Volumes/Transcend/Docker0304/httpd1/Results/indeterminate.xlsx",
    "out" : "/Volumes/Transcend/Docker0304/httpd1/Results/confuzz_httpd1.xls",
}

from copy import deepcopy
import xlrd
import xlwt
import pandas as pd

input_dic = nginx_dic

def get_indeterminate_reaction(para, mutation):
    for i in range( row_num ):
        in_para = sheet.row(i)[0].value.strip()
        in_mutation = sheet.row(i)[1].value.strip()
        if in_para == para and in_mutation == mutation:
            if int(sheet.row(i)[2].value) == 1:
                return "ValidInput"
            elif int(sheet.row(i)[3].value) == 1:
                return "NotEnabled"
            elif int(sheet.row(i)[4].value) == 1:
                return "SilentOverulling"
            elif int(sheet.row(i)[5].value) == 1:
                return "PoorTests"
            else:
                return "Error"

excel = xlrd.open_workbook(input_dic["from"])
workbook = xlwt.Workbook( encoding="ascii" )

for key,value in input_dic.iteritems():

    if key in ["fuzzing", "conferr", "conftest"]:
        sheet = excel.sheet_by_name(key)
        row_num = sheet.nrows
        csv_data = pd.read_csv(value)


        worksheet = workbook.add_sheet(key)

        line_idx = 0

        for line in csv_data.values:
            para_name = line[0].strip()
            mutation = line[1].strip()
            pass_or_not = line[2].strip()
            good_or_bad = line[3].strip()
            reaction_type = "NULL"
            if pass_or_not == "Pass" and good_or_bad == "Bad":
                reaction_type = get_indeterminate_reaction(para_name, mutation)
                if reaction_type == "Error":
                    print para_name, "is Error!"
                else:
                    print para_name, reaction_type
            worksheet.write(line_idx, 0, para_name)
            worksheet.write(line_idx, 1, mutation)
            worksheet.write(line_idx, 2, pass_or_not)
            worksheet.write(line_idx, 3, good_or_bad)
            worksheet.write(line_idx, 4, reaction_type)
            line_idx += 1


workbook.save(input_dic["out"])




