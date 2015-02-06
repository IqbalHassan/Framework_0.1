'''
Created on Sep 9, 2014

@author: Admin
'''
import logging

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('FrameworkLogger.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

def LogInfo(sModuleInfo,sDetails,iLogLevel=1,sStatus=""):
    """
    1- info
    2 - warning
    3 - error
    """
    if iLogLevel == 1:
        logger.info(sModuleInfo + ' - ' + sDetails + '' + sStatus)
    elif iLogLevel == 2:
        logger.warning(sModuleInfo + ' - ' + sDetails + '' + sStatus)
    elif iLogLevel == 3:
        logger.error(sModuleInfo + ' - ' + sDetails + '' + sStatus)
    else:
        print "Unknown Log Level"
    

def PassMessasge(sModuleInfo,msg,level,debug=True):
    if debug:
        print msg
        LogInfo(sModuleInfo, msg, level)
    return msg