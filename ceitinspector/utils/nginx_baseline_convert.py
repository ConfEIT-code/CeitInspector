# -*- coding:utf-8 -*-

import re

pattern1 = re.compile("\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}")
pattern2 = re.compile("\d+\#0")
pattern3 = re.compile("[0-9A-F]{2,}")
pattern4 = re.compile("[0-9]+")
pattern5 = re.compile(" \[debug\] .*\n")
pattern6 = re.compile(" \[error\] .*\n")

file_baseline = open("/Users/Leo/Desktop/对比/baseline.txt", 'r')
file_tocompare = open("/Users/Leo/Desktop/对比/1_log.txt", 'r')
baseline_content = file_baseline.read()
tocompare_content = file_tocompare.read()
new_baseline = re.sub(pattern1, "", baseline_content)
new_baseline = re.sub(pattern2, "", new_baseline)
new_baseline = re.sub(pattern3, "", new_baseline)
new_baseline = re.sub(pattern4, "", new_baseline)
new_baseline = re.sub(pattern5, "", new_baseline)
new_baseline = re.findall(pattern6, new_baseline)
new_tocompare = re.sub(pattern1, "", tocompare_content)
new_tocompare = re.sub(pattern2, "", new_tocompare)
new_tocompare = re.sub(pattern3, "", new_tocompare)
new_tocompare = re.sub(pattern4, "", new_tocompare)
new_tocompare = re.sub(pattern5, "", new_tocompare)
new_tocompare = re.findall(pattern6, new_tocompare)

with open("/Users/Leo/Desktop/对比/baseline_new.txt", 'w') as fp_base:
    fp_base.writelines(new_baseline)
with open("/Users/Leo/Desktop/对比/tocompare_new.txt", 'w') as fp_tocompare:
    fp_tocompare.writelines(new_tocompare)