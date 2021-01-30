#!/usr/bin/python
# coding:utf-8
import urllib
import re
 
def getHtmlContent(url):
    page = urllib.urlopen(url)
    return page.read()
 
def getOptions(html):
    jpgReg = re.compile(r'<tr.*?><td><a href=".+?</a></td><td>.*?</td><td>.*?</td><td>.*?</td></tr>') 
    jpgs = re.findall(jpgReg, html)
    return jpgs
 
 
 
def download(url):
    html = getHtmlContent(url)
    options = getOptions(html)
    i = 0
    count = 0
    with open("/Users/Leo/Desktop/httpd_option_list.csv", 'w') as fp:
        for o in options:
            if i < 10:
                #print o
                raw_option = o.split("</a></td><td>")[0].split('">')[-1].replace("<var>", "").replace("</var>", "")
                key = raw_option.split()[0]
                default_value = o.split("</td><td>")[-3].strip()
                module = o.split("</td><td>")[-1].split("</td></tr>")[0]
                context = o.split("</td><td>")[-2].strip()

                line = ",".join([raw_option, key, default_value, context, module])
                line += "\n"
                fp.write(line)



    print options.__len__()
    #batchDownloadJPGs(jpgs)
 
def main():
    #download(url)
    #print getHtmlContent("http://httpd.apache.org/docs/2.4/mod/quickreference.html")
    download("http://httpd.apache.org/docs/2.4/mod/quickreference.html")
if __name__ == '__main__':
    main()
    print 1
