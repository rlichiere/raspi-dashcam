
import picamera
from datetime import datetime as dt
import os


class Dashcam(object):
    
    def __init__(self, config):
       print('Dashcam.init')
       self._active = config.get('active', False)
       self._outputRootDir = config.get('target_dir', 'videos')
       self._numberOfShots = config.get('number_of_shots', 1) # Number of captures. -1 for infinite captures
       self._shotDuration = config.get('shot_duration', 10)   # seconds
       self._camera = None
    
    def cameraIsAvailable(self):
        if not self._active:
            return False
        
        try:
            self._camera = picamera.PiCamera()
            return True
        except Exception as e:
            print('Dashcam.init: error while using PiCamera(). Please check connections. (%s : %s)' % (type(e), e))
        return False
    
    def start(self):
        if not self._active:
            return False

        if not self._camera:
            if not self.checkCameraAvailability():
                print ('Dashcam.start: Camera unavailable.')
                return False

        _targetFolderName = dt.strftime(dt.now(), '%Y-%m-%d_%Hh%M')
        targetFolder = _targetFolderName

        _counter = 1
        while os.path.exists('%s/%s' % (self._outputRootDir, _targetFolderName)):
            targetFolder = '%s_%d' % (_targetFolderName, _counter)
            _counter += 1

        os.mkdir('%s/%s' % (self._outputRootDir, targetFolder))
        print('Dashcam.start: targetFolder %s created.' % targetFolder)

        self._camera.resolution = (640, 480)
        print('Dashcam.start: Resolution 640x480 set.')

        fileCounter = 1
        continueLoop = True
        while continueLoop:

            targetFileName = '%s/%s/cam_%04d.h264' % (self._outputRootDir, targetFolder, fileCounter)
            
            print('\nstart_recording : %s' % targetFileName)
            self._camera.start_recording(targetFileName)

            self._camera.wait_recording(self._shotDuration)

            self._camera.stop_recording()
            print('stop_recording.')

            if self._numberOfShots > 0:
                if fileCounter >= self._numberOfShots:
                    continueLoop = False
            
            fileCounter += 1
            
        print ('\nDashcam.start: End.')
        return True
