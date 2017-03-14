import os
import utils
import sys
import session
import re
import apkutils

def cd(args):
    if len(args) > 0:
        os.chdir(args[0])
    else:
        os.chdir(os.getenv('HOME'))
    return utils.SHELL_STATUS_RUN

def exit(args):
    return utils.SHELL_STATUS_STOP

def export(args):
    if len(args) > 0:
        var = args[0].split('=', 1)
        os.environ[var[0]] = var[1]
    return utils.SHELL_STATUS_RUN

def getenv(args):
    if len(args) > 0:
        print(os.getenv(args[0]))
    return utils.SHELL_STATUS_RUN

def history(args):
    with open(utils.HISTORY_PATH, 'r') as history_file:
        lines = history_file.readlines()

        # default limit is whole file
        limit = len(lines)

        if len(args) > 0:
            limit = int(args[0])

        # start history line to print out
        start = len(lines) - limit

        for line_num, line in enumerate(lines):
            if line_num >= start:
                sys.stdout.write('%d %s' % (line_num + 1, line))
        sys.stdout.flush()


    return utils.SHELL_STATUS_RUN

def setapk(args):
    if len(args) > 0:
        apk_path = args[0]
        if os.path.isfile(apk_path):
            sys.stdout.write("Setting path to %s\n" % apk_path)
            sys.stdout.flush()
            session.get_session().set_apk_path(apk_path)
            apkutils.disassemble_apk(apk_path, session.get_session())
        else:
            sys.stderr.write("%s is not a valid APK file\n" % apk_path)
            sys.stderr.flush()
    return utils.SHELL_STATUS_RUN

def validSession():
    return session.get_session()

def strings(args):
    if (validSession() is False):
        return
    strings = session.get_session().get_strings()
    if(len(args) > 0):
        regex = re.compile(args[0])
    else:
        regex = re.compile(".*")
    for string in strings:
        if regex.match(string):
            print string

