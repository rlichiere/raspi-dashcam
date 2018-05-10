
import os
from shutil import copyfile


class Backup(object):
    
    def __init__(self, logger, config):
       self._logger = logger
       self._config = config
       self._active = config.get('active', False)
       self._logger.logLine('Backup._active : %s' % self._active)
       
       self._outputRootDir = config.get('output_dir', None)
       self._logger.logLine('Backup._outputRootDir : %s' % self._outputRootDir)
       if not self._outputRootDir:
           raise Exception('Backup.init: output_dir not configured')
    
    """ synchronize target from source """
    def synchronize(self, program):
        _sourceDir = program.getStorageDir()
        _programKey = program.getKey()
        
        if _programKey not in self._config['sources']:
            # configuration of backup do not targets this program
            return
        
        self._logger.logGroup('Synchronize %s data from %s ...' % (program.__class__, _sourceDir))
        _skippedFilesCount = 0
        _copiedFilesCount = 0
        for _srcDirName, _srcDirNames, _srcFileNames in os.walk(_sourceDir):        
            for _srcFileName in _srcFileNames:
                
                _fileRelativePath = _srcDirName.split(_sourceDir)[1]
                _sourcePath = '%s/%s' % (_srcDirName, _srcFileName)
                _targetPath = '%s/%s%s/%s' % (self._outputRootDir, _programKey, _fileRelativePath, _srcFileName)
                
                if os.path.exists(_targetPath):
                    _skippedFilesCount += 1
                    continue
                else:
                    _path = '%s/%s%s' % (self._outputRootDir, _programKey, _fileRelativePath)
                    if not os.path.exists(_path):
                        os.mkdir(_path)
                        
                    self._logger.logLine('Copy : %s ...' % _sourcePath)
                    copyfile(_sourcePath, _targetPath)
                    self._logger.commitLine()
                    _copiedFilesCount += 1
        self._logger.logLine('%d files skipped.' % _skippedFilesCount)
        self._logger.logLine('%d files copied.' % _copiedFilesCount)
        self._logger.commitGroup()
