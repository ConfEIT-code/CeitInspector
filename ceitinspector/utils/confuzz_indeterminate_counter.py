import xlrd

dict = {
    "Squid" : "/Volumes/Transcend/Docker0106/Squid/indeterminate_reactions.xlsx",
    "Vsftpd" : "/Volumes/Transcend/Docker0106/Vsftpd/vsftpd_indeterminate.xls",
    "Httpd" : "/Volumes/Transcend/Docker0304/httpd1/Results/indeterminate.xlsx",
    "Nginx" : "/Volumes/Transcend/Docker0304/nginx/Results/indeterminate.xlsx",
    "PostgreSQL" : "/Volumes/Transcend/Docker0304/pgsql/indeterminate.xlsx",
}

class ValidInput(object):
    Free = 0
    Case = 0
    Unexpected = 0

    def __init__(self):
        pass

    def handle(self, string):
        if string.lower() == "free":
            self.Free += 1
        elif string.lower() == "case":
            self.Case += 1
        elif string.lower() == "unexpected":
            self.Unexpected += 1
        else:
            if not string.isalpha():
                pass
            else:
                print "Error found: ", string
                return False
        return True

class NotEnabled(object):
    Macros = 0
    Control = 0
    Unsatisfied = 0
    Obsolete = 0

    def __init__(self):
        pass

    def handle(self, string):
        if string.lower() == "macros":
            self.Macros += 1
        elif string.lower() == "control":
            self.Control += 1
        elif string.lower() == "unsatisfied":
            self.Unsatisfied += 1
        elif string.lower() == "obsolete":
            self.Obsolete += 1
        else:
            if not string.isalpha():
                pass
            else:
                print "Error found: ", string
                return False
        return True

class SilentOverruling(object):
    Unsafe = 0
    Unlogged = 0

    def __init__(self):
        pass


    def handle(self, string):
        if string.lower() == "unsafe":
            self.Unsafe += 1
        elif string.lower() == "unlogged":
            self.Unlogged += 1
        else:
            if not string.isalpha():
                pass
            else:
                print "Error found: ", string
                return False
        return True


def get_indeterminate_reaction():
    VI = ValidInput()
    NE = NotEnabled()
    SO = SilentOverruling()
    for i in range( row_num ):
        if type(sheet.row(i)[0].value) == unicode and type(sheet.row(i)[1].value) == unicode:
            in_para = sheet.row(i)[0].value.strip()
            in_mutation = sheet.row(i)[1].value.strip()
            if in_para != "" and in_mutation != "":
                if str(sheet.row(i)[2].value) != "":
                    if VI.handle(str(sheet.row(i)[2].value)):
                        pass
                    else:
                        print "Error occured in line: ", i
                        return False
                elif str(sheet.row(i)[3].value) != "":
                    if NE.handle(str(sheet.row(i)[3].value)):
                        pass
                    else:
                        print "Error occured in line: ", i
                        return False
                elif str(sheet.row(i)[4].value) != "":
                    if SO.handle(str(sheet.row(i)[4].value)):
                        pass
                    else:
                        print "Error occured in line: ", i
                        return False
                elif str(sheet.row(i)[5].value) != "":
                    pass
                else:
                    return False
    print "ValidInput: "

    print "Free: "
    print VI.Free
    print "Case: "
    print VI.Case
    print "Unexpected: "
    print VI.Unexpected


    print "NotEnabled: "
    print "Macros: "
    print NE.Macros
    print "Control: "
    print NE.Control
    print "Unsatified: "
    print NE.Unsatisfied
    print "Obsolete: "
    print NE.Obsolete

    print "SilentOverruling: "
    print "Unsafe: "
    print SO.Unsafe
    print "Unlogged: "
    print SO.Unlogged

    return True

name = "Squid"
excel = xlrd.open_workbook( dict[name] )
for key in ["fuzzing", "conferr", "conftest"]:
    print "Now counting: ", key
    sheet = excel.sheet_by_name(key)
    row_num = sheet.nrows
    if get_indeterminate_reaction():

        pass
    else:
        print "Error occured in sheet: ", key