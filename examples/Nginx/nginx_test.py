import sys
sys.path.append("../..")
from ceitinspector.core.main import MainEngine
from ceitinspector.core.global_variables import *

me = MainEngine()
me.print_options()
#me.self_check()
me.run()



#OFFLINE MODE
#me = MainEngine()
#me.start_offline_analyzing()
#me.failures_analyzing([KEY,CONF_PATH,"directive invalid number", "invalid parameter", "directive invalid value"])
#me.success_analyzing([KEY,CONF_PATH,"directive invalid number", "invalid parameter", "directive invalid value"])
#me.dump_overall_results("/Users/anonymous/Desktop/confuzz_nginx_conftest.csv")
