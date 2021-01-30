from config import Config
import os

CONFIG = Config()
from parseconf import ConfEngine
from database import DataEngine
from log import LogEngine
from misconf import MisconfEngine
from analysis import ResultEngine
from test import TestEngine
from ceitinspector.utils.file_system_utils import path_is_existed


class MainEngine( object ):
    log_engine = None
    conf_engine = None
    test_engine = None
    misconf_engine = None
    result_engine = None
    data_engine = None
    config = None

    failed_case = {}
    options = {}
    options_num = 0

    def __init__(self):
        # Self-Config
        self.config = CONFIG

        # Log Setting
        self.log_engine = LogEngine()
        self.log_engine.set_log_level( self.log_engine.LEVEL_DEBUG )
        self.log_engine.add_console_handler()
        self.log_engine.add_file_handler()

        self.init_config()

        # Conf Parser
        self.conf_engine = ConfEngine( self.log_engine,
                                       conf_path=self.conf_path,
                                       conf_parse_mode=self.conf_parse_mode,
                                       add_new_options=self.add_new_options )

        self.options = self.read_conf()
        self.options_num = self.options.__len__()

        # Misconf Generator
        self.misconf_engine = MisconfEngine( self.log_engine, conf_path=self.conf_path, misconf_mode=self.misconf_mode )

        # System Tester
        self.test_engine = TestEngine( self.log_engine, test_mode=self.test_mode, interval=self.interval,
                                       log_file_path=self.log_file_path )

        # Data Recorder
        self.data_engine = DataEngine( self.log_engine, self.software_name )

        # Result Analyzer
        self.result_engine = ResultEngine( self.log_engine, self.char2cut )

        if self.software_name == "Httpd" and self.config.httpd.backup_all_t_files == True:
            self.test_engine.convert_t_files()
        if self.software_name == "Nginx":
            self.conf_engine.set_test_path( self.test_path )
        self.continue_run_flag = False

    def init_config(self):
        self.root_path = self.config.root_path
        self.test_path = self.config.test_path
        self.software_name = self.config.software_name
        self.conf_path = self.config.conf_path
        self.conf_parse_mode = self.config.conf_parse_mode
        self.misconf_mode = self.config.misconf_mode
        self.log_file_path = self.config.log_file_path
        self.add_new_options = self.config.add_new_options
        self.char2cut = self.config.char2cut
        self.test_mode = self.config.test_mode
        self.interval = self.config.interval

    def self_check(self):
        if self.test_mode == "Default" or self.test_mode == "MySQL" :
            failed_case = []
            self.log_engine.info( "----------Self-check Report----------" )
            self.test_engine.set_directory( "Self-Check" )
            self.test_engine.start_observer()
            test_cases = self.test_engine.test_cases
            for testCase in test_cases:
                testCase.run()
                self.log_engine.info( "Test Case ID: " + str( testCase.id ) + "  Test Case Script: " +
                                      testCase.script + "  Test Case Result: " + str( testCase.result ) )
                if testCase.result == False:
                    failed_case.append( testCase )
            self.test_engine.stop_observer()
            self.log_engine.info( "----------Failed Test Case-----------" )
            for testCase in failed_case:
                self.log_engine.info( "Test Case ID: " + str( testCase.id ) )
            self.log_engine.info( "----------Self-check Over-----------" )

        elif self.test_mode == "Httpd":
            self.log_engine.info( "----------Self-check Report----------" )
            self.test_engine.set_directory( "Self-Check" )
            self.test_engine.start_observer()
            self.test_engine.start_daemon( "Self-Check" )
            test_cases = self.test_engine.test_cases
            for testCase in test_cases:
                testCase.run()
            self.test_engine.stop_observer()
            self.test_engine.stop_daemon()
        elif self.test_mode == "Nginx":
            self.log_engine.info( "----------Self-check Report----------" )
            for i in range( self.options_num ):
                i = i + 1
                try:
                    self.log_engine.info( "Testing No." + str( i ) + " option: " + self.options[str( i )]["key"] )
                    self.conf_engine.conf_parser.transfer_nginx_conf( i )
                    self.test_engine.set_directory( "Self-Check/" + self.options[str( i )]["key"] )
                    self.test_engine.start_observer()
                    test_cases = self.test_engine.test_cases
                    for testCase in test_cases:
                        testCase.run()
                        self.log_engine.info( "Test Case ID: " + str( testCase.id ) + "  Test Case Script: " +
                                              testCase.script + "  Test Case Result: " + str( testCase.result ) )
                    self.test_engine.stop_observer()
                except RuntimeError as e:
                    self.log_engine.error( "Exception while testing: " + e.message )
                finally:
                    self.recover_conf()




        else:
            self.log_engine.error( "main.py//self_check()//Unrecognized test_mode!" )
            return

    def read_conf(self):
        return self.conf_engine.read_conf()

    def print_options(self):
        for i in range( self.options_num ):
            option = self.options[str( i + 1 )]
            if option.has_key( "value" ):
                self.log_engine.info( "No: " + str( i + 1 )
                                      + ", Key: " + option["key"]
                                      + ", Value: " + option["value"]
                                      + ", Constraints: " + option["constraint"] )
            else:
                value = option["value1"] + " " + option["value2"]
                self.log_engine.info( "No: " + str( i + 1 )
                                      + ", Key: " + option["key"]
                                      + ", Value: " + value
                                      + ", Constraints: " + option["constraint"] )

    def set_value(self, key, value):
        self.conf_engine.set_value( key, value )

    def set_option(self, key, option):
        self.conf_engine.set_option( key, option )

    def recover_conf(self):
        self.conf_engine.recoverConf()

    def run(self):
        if self.test_mode == "Default" or self.test_mode == "MySQL":
            if self.continue_run_flag == False:
                self.test_engine.mkdir()
            else:
                pass
            self.failed_case = {}
            option_ids = []
            test_cases = self.test_engine.test_cases
            for i in range( self.options_num ):
                i = str( i + 1 )
                option = self.options[i]
                mutants = self.misconf_engine.mutate( option )
                key = option["key"]
                option["mutants"] = mutants

                self.data_engine.set_name( key )

                for mutant in mutants:
                    self.log_engine.info( "Testing No." + i + " option: " + key + "  mutant name: " + mutant["name"] )
                    misconf = self.conf_engine.set_option( key, mutant )
                    if self.continue_run_flag == False:
                        self.test_engine.set_directory( self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] )
                    else:
                        if path_is_existed(
                                self.root_path + "/Results/" + self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] ):
                            continue
                        else:
                            self.test_engine.set_directory(
                                self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] )
                    self.test_engine.start_observer()
                    self.data_engine.set_key( mutant["name"] )
                    self.data_engine.set_misconf( misconf )
                    self.data_engine.set_mutation_type( self.misconf_mode )
                    self.data_engine.set_test_case_num( test_cases.__len__() )
                    self.data_engine.init_value()
                    cleancom = "rm -f `find /postgresql-11.2 -name '*.gcda' -print` & "
                    res = os.system(cleancom)
                    try:
                        for test_case in test_cases:
                            test_case.run()
                            if test_case.result == False:
                                if self.failed_case.has_key( i ):
                                    self.failed_case[i].append( mutant["name"] + "_" + str( test_case.id ) )
                                    self.data_engine.set_testcase_results_fail( test_case.id )
                                else:
                                    self.failed_case[i] = []
                                    self.failed_case[i].append( mutant["name"] + "_" + str( test_case.id ) )
                                    self.data_engine.set_testcase_results_fail( test_case.id )
                                    option_ids.append( i )
                    except Exception as e:
                        self.log_engine.error( "Exception while testing: " + e.message )
                    finally:
                        self.recover_conf()
                        # observer_results = self.test_engine.stop_observer( i, mutant )

                        # self.data_engine.set_observer_results( observer_results )
                    self.data_engine.flush()
            self.log_engine.info( "-----------Test Report-------------" )
            self.log_engine.info(
                "There are " + str( self.failed_case.__len__() ) + " options failed to pass the tests." )
            self.log_engine.info( "Option IDs are: " + str( option_ids ) + '.' )
            # self.log_engine.info( "Details:" )
            # for i in self.failed_case:
            #     self.log_engine.info( "Option ID: " + i + "  Option Key: " + self.options[i]["key"] +
            #                           "  Mutant&Test Case ID: " + str( self.failed_case[i] ) )
            #     reactions = deepcopy( self.test_engine.get_reactions( i ) )
            #     self.log_engine.info( "Option ID: " + i + "  Mutants&Reactions: " + str( reactions ) )
            #
            for i in range( self.options_num ):
                if not self.failed_case.has_key( str( i + 1 ) ):
                    self.log_engine.info( "Option ID: " + str( i + 1 ) + "  Option Key: " + self.options[str( i + 1 )][
                        "key"] + " Pass all the tests" )
            self.log_engine.info( "-----------Test Report Over-------------" )
        elif self.test_mode == "Httpd":
            if self.continue_run_flag == False:
                self.test_engine.mkdir()
            else:
                pass
            self.failed_case = {}
            option_ids = []
            test_cases = self.test_engine.test_cases
            for i in range( self.options_num ):
                i = str( i + 1 )
                option = self.options[i]
                mutants = self.misconf_engine.mutate( option )
                key = option["key"]
                option["mutants"] = mutants
                self.data_engine.set_name( key )
                for mutant in mutants:
                    self.log_engine.info( "Testing No." + i + " option: " + key + "  mutant name: " + mutant["name"] )
                    misconf = self.conf_engine.set_option( key, mutant )
                    if self.continue_run_flag == False:
                        self.test_engine.set_directory( self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] )
                    else:
                        if path_is_existed(
                                self.root_path + "/Results/" + self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] ):
                            continue
                        else:
                            self.test_engine.set_directory(
                                self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] )
                    self.test_engine.start_observer()
                    self.test_engine.start_daemon( self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] )
                    self.data_engine.set_key( mutant["name"] )
                    self.data_engine.set_misconf( misconf )
                    self.data_engine.set_mutation_type( self.misconf_mode )
                    self.data_engine.set_test_case_num( test_cases.__len__() )
                    self.data_engine.init_value()
                    try:
                        for test_case in test_cases:
                            test_case.run()
                            if test_case.result == False:
                                if self.failed_case.has_key( i ):
                                    self.failed_case[i].append( mutant["name"] + "_" + str( test_case.id ) )
                                    self.data_engine.set_testcase_results_fail( test_case.id )
                                else:
                                    self.failed_case[i] = []
                                    self.failed_case[i].append( mutant["name"] + "_" + str( test_case.id ) )
                                    self.data_engine.set_testcase_results_fail( test_case.id )
                                    option_ids.append( i )
                    except Exception as e:
                        self.log_engine.error( "Exception while testing: " + e.message )
                    finally:
                        self.recover_conf()
                        observer_results = self.test_engine.stop_observer( i, mutant )
                        self.test_engine.stop_daemon()

                        self.data_engine.set_observer_results( observer_results )
                    self.data_engine.flush()
            self.log_engine.info( "-----------Test Report-------------" )
            self.log_engine.info(
                "There are " + str( self.failed_case.__len__() ) + " options failed to pass the tests." )
            self.log_engine.info( "Option IDs are: " + str( option_ids ) + '.' )
            for i in range( self.options_num ):
                if not self.failed_case.has_key( str( i + 1 ) ):
                    self.log_engine.info( "Option ID: " + str( i + 1 ) + "  Option Key: " + self.options[str( i + 1 )][
                        "key"] + " Pass all the tests" )
            self.log_engine.info( "-----------Test Report Over-------------" )


        elif self.test_mode == "Nginx":
            if self.continue_run_flag == False:
                self.test_engine.mkdir()
            else:
                pass
            self.failed_case = {}
            option_ids = []
            test_cases = self.test_engine.test_cases
            for i in range( self.options_num ):
                i = str( i + 1 )
                self.conf_engine.conf_parser.transfer_nginx_conf( int( i ) )
                option = self.options[i]
                mutants = self.misconf_engine.mutate( option )
                key = option["key"]
                option["mutants"] = mutants

                self.data_engine.set_name( key )

                for mutant in mutants:
                    self.log_engine.info( "Testing No." + i + " option: " + key + "  mutant name: " + mutant["name"] )
                    self.conf_engine.conf_parser.transfer_nginx_conf( int( i ) )
                    misconf = self.conf_engine.set_option( key, mutant )
                    if self.continue_run_flag == False:
                        self.test_engine.set_directory( self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] )
                    else:
                        if path_is_existed(
                                self.root_path + "/Results/" + self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] ):
                            self.recover_conf()
                            continue

                        else:
                            self.test_engine.set_directory(
                                self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] )
                    self.test_engine.start_observer()
                    self.data_engine.set_key( mutant["name"] )
                    self.data_engine.set_misconf( misconf )
                    self.data_engine.set_mutation_type( self.misconf_mode )
                    self.data_engine.set_test_case_num( test_cases.__len__() )
                    self.data_engine.init_value()
                    try:
                        for test_case in test_cases:
                            test_case.run()
                            if test_case.result == False:
                                if self.failed_case.has_key( i ):
                                    if self.failed_case[i].has_key( mutant["name"] ):
                                        self.failed_case[i][mutant["name"]].append( str( test_case.id ) )
                                        self.data_engine.set_testcase_results_fail( test_case.id )
                                    else:
                                        self.failed_case[i][mutant["name"]] = [str( test_case.id )]
                                        self.data_engine.set_testcase_results_fail( test_case.id )
                                else:
                                    self.failed_case[i] = {}
                                    self.failed_case[i][mutant["name"]] = [str( test_case.id )]
                                    self.data_engine.set_testcase_results_fail( test_case.id )
                                    option_ids.append( i )
                    except Exception as e:
                        self.log_engine.error( "Exception while testing: " + e.message )
                    finally:
                        self.recover_conf()
                        observer_results = self.test_engine.stop_observer( i, mutant )

                        self.data_engine.set_observer_results( observer_results )
                    self.data_engine.flush()
            self.log_engine.info( "-----------Test Report-------------" )
            self.log_engine.info(
                "There are " + str( self.failed_case.__len__() ) + " options failed to pass the tests." )
            self.log_engine.info( "Option IDs are: " + str( option_ids ) + '.' )
            # self.log_engine.info( "Details:" )
            # for i in self.failed_case:
            #     self.log_engine.info( "Option ID: " + i + "  Option Key: " + self.options[i]["key"] +
            #                           "  Mutant&Test Case ID: " + str( self.failed_case[i] ) )
            #     reactions = deepcopy( self.test_engine.get_reactions( i ) )
            #     self.log_engine.info( "Option ID: " + i + "  Mutants&Reactions: " + str( reactions ) )
            #
            for i in range( self.options_num ):
                if not self.failed_case.has_key( str( i + 1 ) ):
                    self.log_engine.info( "Option ID: " + str( i + 1 ) + "  Option Key: " + self.options[str( i + 1 )][
                        "key"] + " Pass all the tests" )
            self.log_engine.info( "-----------Test Report Over-------------" )
        else:
            self.log_engine.error( "main.py//run()//Unrecognized test_mode!" )
            return

    def failures_analyzing(self, words=[], mode="default"):

        self.log_engine.info( "-----------Failures Anazlyzing: -------------" )

        base_dir = "Results/" + self.misconf_mode

        for i in self.failed_case:
            option = self.options[i]
            key = option["key"]
            value = option["value"]
            for mutant, test_case_id in self.failed_case[i].items():
                target_dir = '/'.join( [base_dir, key, mutant] )
                self.result_engine.set_directory( target_dir )
                self.result_engine.build_indexes()
                if words == []:
                    if mode == "default":
                        overall_results = self.result_engine.query_with_filter( [key, self.conf_path] )
                    elif mode == "stemming":
                        overall_results = self.result_engine.query([key, self.conf_path])
                    elif mode == "baseline":
                        self.result_engine.build_baseline(target_dir)
                        overall_results = self.result_engine.query_with_baseline([key, self.conf_path])
                    else:
                        overall_results = self.result_engine.query_with_filter( [key, self.conf_path] )

                else:
                    new_words = []
                    for word in words:
                        if word == "KEY":
                            new_words.append( key )
                        elif word == "VALUE":
                            new_words.append( value )
                        elif word == "CONF_PATH":
                            new_words.append( self.conf_path )
                        else:
                            new_words.append( word )
                    if mode == "default":
                        overall_results = self.result_engine.query_with_filter( [key, self.conf_path] )
                    elif mode == "stemming":
                        overall_results = self.result_engine.query([key, self.conf_path])
                    elif mode == "baseline":
                        self.result_engine.build_baseline(target_dir)
                        overall_results = self.result_engine.query_with_baseline( [key, self.conf_path] )
                    else:
                        overall_results = self.result_engine.query_with_filter( [key, self.conf_path] )
                analyzer_results = self.result_engine.get_analyzer_results()
                self.data_engine.set_name( key )
                self.data_engine.set_key( mutant )
                self.data_engine.load_value()
                self.data_engine.set_analyzer_results( analyzer_results )
                self.data_engine.flush()
                if overall_results:
                    self.log_engine.info( "Option ID: " + i + "  Option Key: " + key +
                                          "  Mutant: " + mutant + "  Result: Good" )
                else:
                    self.log_engine.info( "Option ID: " + i + "  Option Key: " + key +
                                          "  Mutant: " + mutant + "  Result: Bad" )

        self.log_engine.info( "-----------Failures Anazlyzing -------------" )

    def success_analyzing(self, words=[], mode="default"):

        self.log_engine.info( "-----------Success Anazlyzing: -------------" )

        base_dir = "Results/" + self.misconf_mode

        for i in range( self.options_num ):
            i = str( i + 1 )
            option = self.options[i]
            key = option["key"]
            value = option["value"]
            for mutant in option["mutants"]:
                if ("omission" not in mutant["name"]) and ("paramter" not in mutant["name"]) and ("parameter" not in mutant["name"]) and ("delimiter" not in mutant["name"]):
                    mutant = mutant["name"]
                    if i in self.failed_case:
                        if mutant in self.failed_case[i]:
                            continue
                    target_dir = '/'.join( [base_dir, key, mutant] )
                    self.result_engine.set_directory( target_dir )
                    self.result_engine.build_indexes()
                    if words == []:
                        if mode == "default":
                            overall_results = self.result_engine.query_with_filter( [key, self.conf_path] )
                        elif mode == "stemming":
                            overall_results = self.result_engine.query( [key, self.conf_path] )
                        elif mode == "baseline":
                            self.result_engine.build_baseline(target_dir)
                            overall_results = self.result_engine.query_with_baseline( [key, self.conf_path] )
                        else:
                            overall_results = self.result_engine.query_with_filter( [key, self.conf_path] )

                    else:
                        new_words = []
                        for word in words:
                            if word == "KEY":
                                new_words.append( key )
                            elif word == "VALUE":
                                new_words.append( value )
                            elif word == "CONF_PATH":
                                new_words.append( self.conf_path )
                            else:
                                new_words.append( word )
                        if mode == "default":
                            overall_results = self.result_engine.query_with_filter( [key, self.conf_path] )
                        elif mode == "stemming":
                            overall_results = self.result_engine.query( [key, self.conf_path] )
                        elif mode == "baseline":
                            self.result_engine.build_baseline(target_dir)
                            overall_results = self.result_engine.query_with_baseline( [key, self.conf_path] )
                        else:
                            overall_results = self.result_engine.query_with_filter( [key, self.conf_path] )
                    analyzer_results = self.result_engine.get_analyzer_results()
                    self.data_engine.set_name( key )
                    self.data_engine.set_key( mutant )
                    self.data_engine.load_value()
                    self.data_engine.set_analyzer_results( analyzer_results )
                    self.data_engine.flush()
                    if overall_results:
                        self.log_engine.info( "Option ID: " + i + "  Option Key: " + key +
                                              "  Mutant: " + mutant + "  Result: Good" )
                    else:
                        self.log_engine.info( "Option ID: " + i + "  Option Key: " + key +
                                              "  Mutant: " + mutant + "  Result: Bad" )

        self.log_engine.info( "-----------Success Anazlyzing Over-------------" )

    def show_detailed_results_for_option(self, option_name):
        detailed_results = str( self.data_engine.show_all( option_name ) )
        self.log_engine.info( "Option Key: " + option_name +
                              "  Detailed results" + detailed_results )

    def show_overall_results_for_all(self):
        for i in range( self.options_num ):
            i = str( i + 1 )
            option = self.options[i]
            option_name = option["key"]
            mutants = option["mutants"]
            for mutant in mutants:
                overall_results = str( self.data_engine.show_overall_results( option_name, mutant["name"] ) )
                self.log_engine.info( "Option ID: " + i + "  Option Key: " + option_name )
                self.log_engine.info( "Mutant Name: " + mutant["name"] + "   Overall Results: " + overall_results )

    def dump_overall_results(self, file_path):
        self.data_engine.dump_overall_results( file_path )

    def start_offline_analyzing(self, mode="default"):
        self.failed_case = {}
        option_ids = []
        test_cases = self.test_engine.test_cases
        for i in range( self.options_num ):
            i = str( i + 1 )
            option = self.options[i]
            mutants = self.misconf_engine.mutate( option )
            option["mutants"] = mutants

            self.data_engine.set_name( option["key"] )

            self.log_engine.info( "Offline Testing No." + i + " option: " + option["key"] + " ..." )

            for mutant in mutants:
                if ("omission" not in mutant["name"]) and ("parameter" not in mutant["name"]) and ("delimiter" not in mutant["name"]):
                    misconf = self.conf_engine.set_option( option["key"], mutant )
                    self.test_engine.set_directory_offline( self.misconf_mode + "/" + option["key"] + "/" + mutant["name"] )
                    self.data_engine.set_key( mutant["name"] )
                    self.data_engine.set_misconf( misconf )
                    self.data_engine.set_mutation_type( self.misconf_mode )
                    self.data_engine.set_test_case_num( test_cases.__len__() )
                    self.data_engine.init_value()
                    try:
                        for test_case in test_cases:
                            test_case.run_offline()
                            if test_case.result == False:
                                if self.failed_case.has_key( i ):
                                    if self.failed_case[i].has_key( mutant["name"] ):
                                        self.failed_case[i][mutant["name"]].append( str( test_case.id ) )
                                        self.data_engine.set_testcase_results_fail( test_case.id )
                                    else:
                                        self.failed_case[i][mutant["name"]] = [str( test_case.id )]
                                        self.data_engine.set_testcase_results_fail( test_case.id )
                                else:
                                    self.failed_case[i] = {}
                                    self.failed_case[i][mutant["name"]] = [str( test_case.id )]
                                    self.data_engine.set_testcase_results_fail( test_case.id )
                                    option_ids.append( i )
                    except Exception as e:
                        self.log_engine.error( "Exception while testing: " + e.message )
                    finally:
                        self.recover_conf()
                    self.data_engine.flush()
        self.log_engine.info( "-----------Offline Test Report-------------" )
        self.log_engine.info( "There are " + str( self.failed_case.__len__() ) + " options failed to pass the tests." )
        self.log_engine.info( "Option IDs are: " + str( option_ids ) + '.' )
        # self.log_engine.info( "Details:" )
        # for i in self.failed_case:
        #     self.log_engine.info( "Option ID: " + i + "  Option Key: " + self.options[i]["key"] +
        #                           "  Mutant&Test Case ID: " + str( self.failed_case[i] ) )
        #     reactions = deepcopy( self.test_engine.get_reactions( i ) )
        #     self.log_engine.info( "Option ID: " + i + "  Mutants&Reactions: " + str( reactions ) )
        #
        for i in range( self.options_num ):
            if not self.failed_case.has_key( str( i + 1 ) ):
                self.log_engine.info( "Option ID: " + str( i + 1 ) + "  Option Key: " + self.options[str( i + 1 )][
                    "key"] + " Pass all the tests" )
        self.log_engine.info( "-----------Test Report Over-------------" )

    def continue_run(self):
        self.continue_run_flag = True
        self.run()


if __name__ == '__main__':
    me = MainEngine()
