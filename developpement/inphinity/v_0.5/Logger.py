##
#   Created by: Deruaz Vincent
#   Core of Inphinity
#   17.11.2016
##

#from toolsIo import ToolsIO
import datetime


class Logger():
    def __init__(self, verbose=False):
        self.verbose=verbose
        self.filename = '/tmp/logs_inphinity.txt'
        self.write(self.filename, '\n')

    def write(self, filename, txt):
        file = open(filename, "a")
        file.write(txt)
        file.close()

    def log_detailed(self, msg, log_detailed=False):
        if(log_detailed):
            msg = '\nDETAILS %s| %s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), msg)
            if(self.verbose):
                print(msg)
            self.write(self.filename, msg)

    def log_normal(self, msg):
        msg = '\nNORMAL %s| %s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), msg)
        if(self.verbose):
            print(msg)
        self.write(self.filename, msg)

    def log_error(self, msg):
        msg = '\nERROR %s| %s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), msg)
        if(self.verbose):
            print(msg)
        self.write(self.filename, msg)

    def log_warnnings(self, msg):
        msg = '\nWARNNINGS %s| %s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), msg)
        if(self.verbose):
            print(msg)
        self.write(self.filename, msg)

    def log_debug(self, msg):
        msg = '\nDEBUG %s| %s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), msg)
        if(self.verbose):
            print(msg)
        self.write(self.filename, msg)