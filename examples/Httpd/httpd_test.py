import sys
sys.path.append("../..")
from ceitinspector.core.global_variables import *
from ceitinspector.core.main import MainEngine
from ceitinspector.modules.supporter.httpd import modperl_hacker, httpd_daemon
#modperl_hacker.convert_all_t_files()
#me = MainEngine()
#me.print_options()
#me.self_check()
#
#me.run()

"""#DEBUG MODE
hd = httpd_daemon.HttpdDaemon()
hd.setDaemon(False)
hd.get_event("consolefile=/ceitinspector-code/examples/Httpd/Results/Self-Check/1_console.txt")
hd.get_event("logfile=/mod_perl-2.0.10/t/logs/error_log")
hd.set_directory("Self-Check")
hd.start()
"""

#OFFLINE MODE
me = MainEngine()
me.print_options()
me.start_offline_analyzing()
me.failures_analyzing( [KEY, "Syntax error on"] )
me.success_analyzing([KEY])
me.dump_overall_results("/Users/anonymous/Desktop/confuzz_httpd_confdiag.csv")