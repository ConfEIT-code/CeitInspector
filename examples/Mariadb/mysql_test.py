import sys
sys.path.append( "../.." )
from ceitinspector.core.main import MainEngine
from ceitinspector.core.global_variables import *


#me = MainEngine()
#me.print_options()
#me.self_check()
#me.run()



#OFFLINE MODE
me = MainEngine()
me.start_offline_analyzing()
me.failures_analyzing(mode="stemming" )
me.success_analyzing(mode="stemming")
me.dump_overall_results("/Users/anonymous/Desktop/confuzz_mysql_fuzzing.csv")