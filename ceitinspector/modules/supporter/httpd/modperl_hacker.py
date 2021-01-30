from subprocess import Popen

from ceitinspector.core import config
from ceitinspector.utils.file_system_utils import get_files_in_dir

INSTRUMENTATION = config.config.root_path + "/../../ceitinspector/modules/system_tester/perlscripts/instrumentation.pl"
TESTSTART1 = "ConfuzzTestingStartSignal-1"
TESTSTART2 = "ConfuzzTestingStartSignal-2"
TESTEND1 = "ConfuzzTestingEndSignal-1"
TESTEND2 = "ConfuzzTestingEndSignal-2"

SIGNAL_FILE_2_READ = config.config.httpd.signal_file_2_read
SIGNAL_FILE_2_WRITE = config.config.httpd.signal_file_2_write
CONVERT_ALL_T_FILES = config.config.httpd.convert_all_t_files
T_DIR = config.config.httpd.t_dir
BACKUP_ALL_T_FILES = config.config.httpd.backup_all_t_files
BACKDUP_DIR = config.config.httpd.httpd_backup_dir


def _change_signal(ls, filename):
    start_signal = filename + " ready!"
    end_signal = filename + " over!"
    file2read = SIGNAL_FILE_2_WRITE
    file2write = SIGNAL_FILE_2_READ
    temp_ls = []
    for l in ls:
        if "signal2start" in l:
            new_l = l.replace( "signal2start", start_signal )
            temp_ls.append( new_l )
        elif "signal2end" in l:
            new_l = l.replace( "signal2end", end_signal )
            temp_ls.append( new_l )
        elif "file2read" in l:
            new_l = l.replace( "file2read", file2read )
            temp_ls.append( new_l )
        elif "file2write" in l:
            new_l = l.replace( "file2write", file2write )
            temp_ls.append( new_l )
        else:
            temp_ls.append( l )
    return temp_ls


def _get_instrumentation():
    flg1 = False
    flg3 = False
    start_test_lines = []
    end_test_lines = []
    with open( INSTRUMENTATION, 'r' ) as fp:
        lines = fp.readlines()

        for line in lines:
            if TESTSTART1 in line:
                flg1 = True
            elif TESTSTART2 in line:
                flg1 = False
            elif TESTEND1 in line:
                flg3 = True
            elif TESTEND2 in line:
                flg3 = False
            else:
                if flg1:
                    start_test_lines.append( line )
                elif flg3:
                    end_test_lines.append( line )
                else:
                    pass
    return start_test_lines, end_test_lines


def _get_all_t_files(path):
    print path
    t_files = []
    files = get_files_in_dir( path, True )
    print files
    for dir, filenames in files.items():
        for filename in filenames:
            if ".t" in filename and ".txt" not in filename:
                temp_path = (dir, filename)
                t_files.append( temp_path )
    return t_files


def _hack_t_file(path_tuple):
    dir, filename = path_tuple
    path = dir + '/' + filename
    start_instrumentation, end_instrumentation = _get_instrumentation()
    start_instrumentation = _change_signal( start_instrumentation, filename )
    with open( path, 'r' ) as fp:
        lines = fp.readlines()
        for line in lines:
            if "Confuzz-code" in line:
                return
    temp_lines = start_instrumentation + ["\n"] + lines + ["\n"] + end_instrumentation
    with open( path, 'w' ) as fp:
        fp.writelines( temp_lines )


def _back_up_t_files():
    command = "cp -rf " + T_DIR + " " + BACKDUP_DIR
    p = Popen( command, shell=True )
    p.wait()


def convert_all_t_files():
    if CONVERT_ALL_T_FILES:
        if BACKUP_ALL_T_FILES:
            _back_up_t_files()
        files = _get_all_t_files( T_DIR )
        for file_tuple in files:
            _hack_t_file( file_tuple )

    else:
        pass
