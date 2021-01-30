# -*- coding:utf-8 -*-
import xlrd

INPUT_FP = ["/Volumes/Transcend/Docker0304/httpd1/Results/confuzz_httpd1.xls",
            "/Volumes/Transcend/Docker0106/Squid/confuzz_squid.xls",
            "/Volumes/Transcend/Docker0106/Vsftpd/confuzz_vsftpd.xls",
            "/Volumes/Transcend/Docker0304/nginx/Results/confuzz_nginx1.xls",
            "/Volumes/Transcend/Docker0304/pgsql/confuzz_pgsql.xls"]

OUTPUT_FP = "/Users/Leo/Desktop/ceitinspector.txt"
with open(OUTPUT_FP, 'w') as out_fp:

    for file in INPUT_FP:

        workbook_data = xlrd.open_workbook(file)
        for sheet in ["fuzzing", "conferr", "conftest"]:
            print file
            sheet_data = workbook_data.sheet_by_name(sheet)

            G1_reaction = []
            G1_parameter = []
            G2_reaction = []
            G2_parameter = []
            B_reaction = []
            B_parameter = []
            I1_reaction = []
            I1_parameter = []
            I2_reaction = []
            I2_parameter = []
            I3_reaction = []
            I3_parameter = []
            I4_reaction = []
            I4_parameter = []

            for line_idx in range(sheet_data.nrows):
                para_name = sheet_data.row(line_idx)[0].value.strip()
                mutation_name = sheet_data.row(line_idx)[1].value.strip()
                pass_or_not = sheet_data.row(line_idx)[2].value.strip()
                good_or_bad = sheet_data.row(line_idx)[3].value.strip()
                indeterminate_type = sheet_data.row(line_idx)[4].value.strip()

                if pass_or_not == "Fail" and good_or_bad == "Good":
                    G1_reaction.append(para_name)
                    if para_name not in G1_parameter:
                        G1_parameter.append(para_name)
                elif pass_or_not == "Fail" and good_or_bad == "Bad":
                    B_reaction.append(para_name)
                    if para_name not in B_parameter:
                        B_parameter.append(para_name)
                elif pass_or_not == "Pass" and good_or_bad == "Good":
                    G2_reaction.append(para_name)
                    if para_name not in G2_parameter:
                        G2_parameter.append(para_name)
                elif pass_or_not == "Pass" and good_or_bad == "Bad":
                    if indeterminate_type.lower() == "validinput":
                        I1_reaction.append(para_name)
                        if para_name not in I1_parameter:
                            I1_parameter.append(para_name)
                    elif indeterminate_type.lower() == "notenabled":
                        I2_reaction.append(para_name)
                        if para_name not in I2_parameter:
                            I2_parameter.append(para_name)
                    elif indeterminate_type.lower() == "silentoverulling":
                        I3_reaction.append(para_name)
                        if para_name not in I3_parameter:
                            I3_parameter.append(para_name)
                    elif indeterminate_type.lower() == "poortests":
                        I4_reaction.append(para_name)
                        if para_name not in I4_parameter:
                            I4_parameter.append(para_name)
                    else:
                        print sheet, para_name, mutation_name, "Error in finding indeterminate reaction!"
                        break
                else:
                    print "Error: in line ", sheet_data.row(line_idx)

            strings_2_write = []
            strings_2_write.append( "G1: " + str(G1_reaction.__len__()) + "/" + str(G1_parameter.__len__()) + '\n' )
            strings_2_write.append( "G2: " + str(G2_reaction.__len__()) + "/" + str(G2_parameter.__len__()) + '\n' )
            strings_2_write.append( "B: " + str(B_reaction.__len__()) + "/" + str(B_parameter.__len__()) + '\n' )
            strings_2_write.append( "I1: " + str(I1_reaction.__len__()) + "/" + str(I1_parameter.__len__()) + '\n' )
            strings_2_write.append( "I2: " + str(I2_reaction.__len__()) + "/" + str(I2_parameter.__len__()) + '\n' )
            strings_2_write.append( "I3: " + str(I3_reaction.__len__()) + "/" + str(I3_parameter.__len__()) + '\n' )
            strings_2_write.append( "I4: " + str(I4_reaction.__len__()) + "/" + str(I4_parameter.__len__()) + '\n' )
            strings_2_write.append( "Total: " + str(G1_reaction.__len__() + G2_reaction.__len__() + B_reaction.__len__()
                                                    + I1_reaction.__len__() + I2_reaction.__len__() + I3_reaction.__len__()
                                                    + I4_reaction.__len__()) + '\n')

            out_fp.write(file)
            out_fp.write("\n")
            out_fp.write(sheet)
            out_fp.write("\n")
            out_fp.writelines(strings_2_write)
            out_fp.write("\n\n\n\n\n")