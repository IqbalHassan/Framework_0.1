import time, datetime, inspect
import os
import win32pdh, win32api, win32con
import DataBaseUtilities as DB
import wmi
import subprocess
import win32com.client
import logging




logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('execlog.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

def ExecLog(sModuleInfo, sDetails, iLogLevel=1, sStatus="",):
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
        print "unknown log level"

def GetProcessID(ProcessName):
    c = wmi.WMI()
    ProcessID = "None"
    for process in c.Win32_Process (name=ProcessName):
        ProcessID = process.ProcessId
        print process.ProcessId, process.Name
    return ProcessID


def TimeStamp(frmt):
    """

    ========= Instruction: ============

    Function Description:
    This function is used to create a Time Stamp.
    It will return current Day-Month-Date-Hour:Minute:Second-Year all in one string
    OR
    It will return current YearMonthDayHourMinuteSecond all in a integer.

    Parameter Description:

    - string: this returns a readable string for the current date and time frmt
        Example:
        TimeStamp = TimeStamp("string") = Fri-Jan-20-10:20:31-2012

    - integer: this returns a readable string for the current date and time frmt
        Example:
        TimeStamp = TimeStamp("integer") = 2012120102051
    ======= End of Instruction: =========

    """
    if frmt == "string":
        TimeStamp = datetime.datetime.now().ctime().replace(' ', '-').replace('--', '-')
    elif frmt == "integer":
        now = datetime.datetime.now()
        year = "%d" % now.year
        month = "%d" % now.month
        day = "%d" % now.day
        hour = "%d" % now.hour
        minute = "%d" % now.minute
        second = "%d" % now.second
        TimeStamp = year + month + day + hour + minute + second
        #TimeStamp = int (TimeStamp)

    return TimeStamp

def ReadFile(filename):
    print "reading file from ", filename
    with open(filename, 'r') as fileObj:
        x = fileObj.read()
        fileObj.close()
    print "File Object Closed: ", fileObj.closed
    return(x)

def WriteToFile(fileName, cont):
    fileObj = open(fileName, 'w')     # Writing permission
    fileObj.write(cont)
    fileObj.close()

def GetLocalOS():
    import platform
    return platform.system() + " " + platform.release()

def GetLocalUser():
    return os.environ.get("USERNAME")




def FormatSeconds(sec):
        hours, remainder = divmod(sec, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_formatted = '%d:%02d:%02d' % (hours, minutes, seconds)
        return duration_formatted

