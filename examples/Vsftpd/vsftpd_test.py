import sys
sys.path.append( "../.." )
from ceitinspector import MainEngine

me = MainEngine()
#me.print_options()
#me.self_check()
#me.run()
#me.failures_analyzing()
#me.dump_overall_results(file_path="/confuzz_vsftpd_conftest.csv")

me.start_offline_analyzing()
me.failures_analyzing()
me.success_analyzing()
me.dump_overall_results("/Users/anonymous/Desktop/confuzz_vsftpd_confdiag.csv")