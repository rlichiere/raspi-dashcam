

class Logger(object):
    
    def __init__(self, logs_dir):
        self._logDir = logs_dir
        self._logFile = None
    
    def log(self, message):
        with open('%s/log.txt' % self._logDir, 'a') as self._logFile:
            self._logFile.write('\n%s' % message)

    def add(self, message):
        with open('%s/log.txt' % self._logDir, 'a') as self._logFile:
            self._logFile.write(' %s' % message)
