# -*- coding:utf-8 -*-
import os
import time
from threading import Thread

from ceitinspector.core import config

INTERVAL = 0.2
SIGNAL_FILE_2_READ = config.config.httpd.signal_file_2_read
SIGNAL_FILE_2_WRITE = config.config.httpd.signal_file_2_write


# SIGNAL_FILE_2_READ = "/Users/Leo/Desktop/Docker/Signal/read.dat"
# SIGNAL_FILE_2_WRITE = "/Users/Leo/Desktop/Docker/Signal/write.dat"

class HttpdDaemon( Thread ):

    def __init__(self):
        Thread.__init__( self )
        self.old_signal = None
        self.setDaemon( True )
        self.console_file = ""
        self.log_file = ""
        self.directory = ""
        self.log_index = 0
        self.console_index = 0
        self.directory = ""
        self.last_signal = None

        with open( SIGNAL_FILE_2_READ, 'w' ) as fp:
            fp.write( "" )
        with open( SIGNAL_FILE_2_WRITE, 'w' ) as fp:
            fp.write( "" )

    def run(self):
        self.finished = False
        self.running = True

        time.sleep(3)
        self.handle("daemon_startup.t ready!")

        first_time = True
        while True:

            if self.running:
                time.sleep( INTERVAL )
                signal = self.check()


                if signal != None and "!" in signal and ".t " in signal:
                    if first_time == True:
                        self.handle("daemon_startup.t over!")
                        first_time = False
                    self.handle( signal )
                if signal == "log.t over!":
                    self.handle( signal )
                    time.sleep(4)
                    self.handle("shudown.t ready!")
                    break
                if self.finished:
                    self.running = False
            else:
                break


    def check(self):
        with open( SIGNAL_FILE_2_READ, 'r' ) as fp:
            signal = fp.read()
            if self.isnew( signal ):
                self.old_signal = signal
                return signal
            else:
                return None

    def isnew(self, signal):
        if self.old_signal == signal or signal == "":
            return False
        elif "!" in signal:
            return True
        else:
            return False

    def handle(self, signal):
        if signal == None:
            return
        if signal.split() == []:
            return
        print "handling: ", signal
        if self.last_signal == None:
            if "ready!" in signal:
                self.start_record()
        else:
            t_file_name = self.last_signal.split( "." )[0]
            results_path = self.directory
            console_result_path = results_path + '/' + t_file_name + "_console.txt"
            log_result_path = results_path + '/' + t_file_name + "_log.txt"

            # signal = "log.t over!"
            if "ready!" in signal:
                self.stop_record(console_result_path, log_result_path)
                self.start_record()


        # Be careful, things should be done before the file writing

        with open( SIGNAL_FILE_2_WRITE, 'w' ) as fp:
            fp.write( signal )
        self.last_signal = signal

    def stop(self):
        self.finished = True

    def get_event(self, string):
        if "consolefile=" in string:
            self.console_file = string.split( "consolefile=" )[-1]
        elif "logfile=" in string:
            self.log_file = string.split( "logfile=" )[-1]
        else:
            pass

    def start_record(self):
        with open( self.log_file, 'r' ) as fp:
            fp.read()
            self.log_index = fp.tell()
        with open( self.console_file, 'r' ) as fp:
            fp.read()
            self.console_index = fp.tell()

    def stop_record(self, console2save, log2save):
        with open( self.console_file, 'r' ) as fp:
            fp.seek( self.console_index )
            result = fp.read()
        if os.path.exists(console2save):
            console2save += "2"
        else:
            pass
        with open( console2save, 'w' ) as fp:
            fp.write( result )

        with open( self.log_file, 'r' ) as fp:
            fp.seek( self.log_index )
            result = fp.read()
        if os.path.exists(log2save):
            log2save += "2"
        else:
            pass
        with open( log2save, 'w' ) as fp:
            fp.write( result )

    def set_directory(self, directory):
        self.directory = config.config.root_path + '/Results' + '/' + directory




if __name__ == '__main__':
    hd = HttpdDaemon()
    hd.start()
