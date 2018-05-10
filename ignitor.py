"""
This program is launched at boot in order to manage automatic programs :
- dashcam
- backup
- ? other ideas incoming ?

The configuration of programs must be se in ignition_config.yml file.
"""

import os
import yaml

from dashcam import Dashcam
from logger import Logger

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
logger = Logger('%s/logs' % PROJECT_ROOT)

logger.log('************************ New execution ***')
logger.log('- PROJECT_ROOT : %s' % PROJECT_ROOT)

try:
    logger.log('- imports...')
    logger.add('done.')
    
    logger.log('- load config...')
    configFile = open('%s/ignitor_config.yml' % PROJECT_ROOT)
    ignitorConfig = yaml.load(configFile)
    logger.add('done.')

    logger.log('- manage dashcam...')
    if 'dashcam' in ignitorConfig:
        dashcam = Dashcam(ignitorConfig['dashcam'])
        if dashcam.cameraIsAvailable():
            dashcam.start()
            print('Ignitor: dashcam started.')
        else:
            print('Ignitor: dashcam not started (camera unavailable)')
    logger.add('done.')

    logger.log('- manage backup...')
    if 'backup' in ignitorConfig:
        print('Ignitor: should launch backup !')
    logger.add('done.')

except Exception as e:
    logger.log('Ignitor error : %s : %s' % (type(e), e))
    
logger.log('- End.\n')
