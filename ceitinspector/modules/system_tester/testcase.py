import os
import subprocess
import time
from logging import info,warn,error,debug
from threading import Timer

from ceitinspector.core import config


class TestCase( object ):
    script_dict = {}
    oracle_dict = {}
    script = ""
    oracle = ""
    id = ""
    result = False
    directory = ""
    end = ""
    log_file = ""
    event_listener = None
    test_path = ""

    def __init__(self, id, script_dict, oracle_dict, interval, log_file, end):
        self.id = id
        self.script_dict = script_dict
        self.oracle_dict = oracle_dict
        self.script = script_dict["script"]
        self.oracle = oracle_dict["oracle"]
        self.interval = interval
        self.end = end
        self.log_file = log_file
        self.timeout = oracle_dict["timeout"]
        self.test_path = config.config.test_path
        self.test_mode = config.config.test_mode
        self.timeout_flag = False
        if "check_for_absence" in oracle_dict:
            self.check_for_absence = oracle_dict["check_for_absence"]
        else:
            self.check_for_absence = False

    def timeout_callback(self):
        self.timeout_flag = True


    def run(self):
        if self.test_mode == "Default":
            if self.test_path != "":
                os.chdir( self.test_path )
            console2save = self.directory + '/' + str( self.id ) + "_console.txt"
            log2save = self.directory + '/' + str( self.id ) + "_log.txt"
            cov2save = self.directory + '/' + str( self.id ) + "_cov"

            command = self.script + " > " + console2save + " 2>&1 ; " + "lcov --directory /postgresql-11.2 --capture --output-file --rc lcov_branch_coverage=1  " + cov2save + " "
            self.start_log_record()
            res = subprocess.Popen( command, shell=True )
            if self.timeout == "default":
                self.timeout = 0
            #time.sleep( self.timeout )
            self.timeout_flag = False
            my_timer = Timer( self.timeout, self.timeout_callback, [])
            my_timer.start()
            while True:
                time.sleep(0.1)
                if self.timeout_flag == True:
                    break
                elif res.poll() != None:
                    break
                else:
                    pass
            self.event_listener.push_observer_event( self.id )

            time.sleep( self.interval )

            self.stop_log_record( log2save )

            with open( console2save, 'r' ) as fp:
                raw_result = fp.read()

            self.result = self.check_oracle( raw_result )

        elif self.test_mode == "Httpd":
            if self.test_path != "":
                os.chdir( self.test_path )
            console2save = self.directory + '/' + str( self.id ) + "_console.txt"
            log2save = self.directory + '/' + str( self.id ) + "_log.txt"
            self.event_listener.push_daemon_event( "consolefile=" + console2save )
            self.event_listener.push_daemon_event( "logfile=" + self.log_file )
            if self.oracle_dict["running"] == True:
                command = self.script + " > " + console2save + " 2>&1 "
            else:
                command = self.script + " > " + console2save + " 2>&1 "
            self.start_log_record()
            res = subprocess.Popen( command, shell=True )
            res.wait()
            if self.timeout == "default":
                self.timeout = 0
            time.sleep( self.timeout )
            self.event_listener.push_observer_event( self.id )
            time.sleep( self.interval )
            self.stop_log_record( log2save )

            with open( console2save, 'r' ) as fp:
                raw_result = fp.read()

            self.result = self.check_oracle( raw_result )

        elif self.test_mode == "Nginx":
            if self.test_path != "":
                os.chdir( self.test_path )
            console2save = self.directory + '/' + str( self.id ) + "_console.txt"
            log2save = self.directory + '/' + str( self.id ) + "_log.txt"

            if self.oracle_dict["running"] == True:
                command = self.script + " > " + console2save + " 2>&1 "
            else:
                command = self.script + " > " + console2save + " 2>&1 "

            old_path = os.listdir( self.log_file )

            res = subprocess.Popen( command, shell=True )
            res.wait()
            if self.timeout == "default":
                self.timeout = 0
            time.sleep( self.timeout )
            self.event_listener.push_observer_event( self.id )
            time.sleep( self.interval )

            new_path = os.listdir( self.log_file )

            temp_log_file = [item for item in new_path if item not in old_path]
            f = open( "/tmp/error.log", 'w' )
            for filename in temp_log_file:
                try:
                    #startup log
                    filepath = "/tmp/" + ''.join( filename ) + "/logs/error.log"
                    content = open( filepath ).read()
                    f.write( content )
                except (IOError,), e:
                    print e
                try:
                    #runtime log
                    filepath = "/tmp/" + ''.join( filename ) + "/error.log"
                    content = open( filepath ).read()
                    f.write( content )
                except (IOError,), e:
                    print e
            f.close()
            # self.log_file = "/tmp/error.log"
            self.nginx_stop_log_record( log2save )

            with open( console2save, 'r' ) as fp:
                raw_result = fp.read()

            self.result = self.check_oracle( raw_result )

        elif self.test_mode == "MySQL":
            if self.test_path != "":
                os.chdir( self.test_path )

            console2save = self.directory + '/' + str( self.id ) + "_console.txt"
            log2save = self.directory + '/' + str( self.id ) + "_log.txt"

            if self.oracle_dict["running"] == True:
                command = self.script + " > " + console2save + " 2>&1 "
            else:
                command = self.script + " > " + console2save + " 2>&1 "
            #self.start_log_record()
            self.file_index = 0
            res = subprocess.Popen( command, shell=True )
            if self.timeout == "default":
                self.timeout = 0

            time.sleep( self.timeout )
            self.event_listener.push_observer_event( self.id )

            time.sleep( self.interval )

            self.stop_log_record( log2save )

            with open( console2save, 'r' ) as fp:
                raw_result = fp.read()

            self.result = self.check_oracle( raw_result )
        else:
            return

    def run_offline(self):

        console2save = self.directory + '/' + str( self.id ) + "_console.txt"

        try:
            with open( console2save, 'r' ) as fp:
                raw_result = fp.read()
        except Exception as e:
            raise ValueError("Unable to open file: " + console2save)

        self.result = self.check_oracle( raw_result )

    def start_log_record(self):
        if self.log_file == "":
            return
        try:
            with open( self.log_file, 'r' ) as fp:
                fp.read()
                self.file_index = fp.tell()
        except:
            self.file_index = 0


    def stop_log_record(self, log2save):
        if self.log_file == "":
            return
        try:
            with open( self.log_file, 'r' ) as fp:
                fp.seek( self.file_index )
                result = fp.read()
        except:
            result = ""
        with open( log2save, 'w' ) as fp:
            fp.write( result )

    def nginx_stop_log_record(self, log2save):
        if self.log_file == "":
            return
        with open( "/tmp/error.log", 'r' ) as fp:
            result = fp.read()
        with open( log2save, 'w' ) as fp:
            fp.write( result )

    def check_oracle(self, raw_result):
        if self.check_for_absence and self.oracle not in raw_result:
            return True
        elif self.check_for_absence == False and self.oracle in raw_result:
            return True
        else:
            return False

    def bind(self, listener):
        self.event_listener = listener

    def set_directory(self, directory):
        self.directory = directory
