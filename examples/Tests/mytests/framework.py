#this file is to simulate all the cases ceitinspector could meet.
# -*- coding:utf-8 -*-


import sys
from threading import Timer
import time

timeout = False

def main():
    commands = sys.argv
    if commands.__len__() < 3:
        print "Too few commands to condut, please check!"
        return
    operation = commands[1]
    argvs = commands[2:]

    if operation == "--normal_run_shut":
        return normal_run_shut(argvs)

    elif operation == "--normal_keep_run":
        return normal_keep_run(argvs)

    elif operation == "--failed_run_shut":
        return failed_run_shut(argvs)

    elif operation == "--failed_keep_run":
        return failed_keep_run(argvs)

    elif operation == "--crash_run_shut":
        return crash_run_shut(argvs)

    else:
        print "command can not be recognized, please check!"



def normal_run_shut(argvs):
    global timeout
    timeout = False
    def timer_callback():
        print "get called"
        global timeout
        timeout = True

    time_duration = float(argvs[0])
    my_timer = Timer(time_duration, timer_callback)
    my_timer.start()
    print "Start!"
    while True:
        time.sleep(0.5)
        if timeout == False:
            print "Running!"
            pass
        else:
            print "Success!"
            print "End!"
            break
    return 0

def normal_keep_run(argvs):
    global timeout
    timeout = False
    def timer_callback():
        print "get called"
        global timeout
        timeout = True

    my_timer = Timer(600, timer_callback)
    my_timer.start()
    print "Start!"
    while True:
        time.sleep(0.5)
        if timeout == False:
            print "Success!"
            pass
        else:
            print "End!"
            break

def failed_run_shut(argvs):
    global timeout
    timeout = False
    def timer_callback():
        print "get called"
        global timeout
        timeout = True

    time_duration = float(argvs[0])
    my_timer = Timer(time_duration, timer_callback)
    my_timer.start()
    print "Start!"
    while True:
        time.sleep(0.5)
        if timeout == False:
            print "Running!"
            pass
        else:
            print "Failed!"
            print "End!"
            break

def failed_keep_run(argvs):
    global timeout
    timeout = False
    def timer_callback():
        print "get called"
        global timeout
        timeout = True

    my_timer = Timer(600, timer_callback)
    my_timer.start()
    print "Start!"
    while True:
        time.sleep(0.5)
        if timeout == False:
            print "Failed!"
            pass
        else:
            print "End!"
            break

def crash_run_shut(argvs):
    global timeout
    timeout = False
    def timer_callback():
        print "get called"
        global timeout
        timeout = True

    time_duration = float(argvs[0])
    my_timer = Timer(time_duration, timer_callback)
    my_timer.start()
    print "Start!"
    while True:
        time.sleep(0.5)
        if timeout == False:
            print "Running!"
            pass
        else:
            print "Crash!"
            print "End!"
            coredumpfile = "/corefile/myframework"
            try:
                with open (coredumpfile, 'w') as fp:
                    fp.write("0000000000000")
            except Exception:
                print Exception.message
            break







main()


