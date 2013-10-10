import os, shutil, subprocess
from stat import *
import time, datetime
import operator
import psycopg2
import inspect
import CommonUtil, FileUtilities
import DataBaseUtilities as DBU
import urllib
if os.name == 'nt':
    import WinCommonFoldersPaths as ComPath
    import _winreg
    import ctypes
    from ctypes import wintypes
elif os.name == 'posix':
    import MacCommonFoldersPaths as ComPath



def ReturnBuildInstalled(file_path):
    #file_path = "C:\\DailyBuild\\BuildNum.txt"
    return CommonUtil.ReadFile(file_path)

def NewBuildPath(directory):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        alist = {}
        now = time.time()
        os.chdir(directory)
        SortByTime = True
        latest = ''
        try:
            for file in os.listdir("."):
                #if not("bb10") in file:
                if os.path.isdir(file):
                    timestamp = os.path.getmtime(file)
                    # get timestamp and directory name and store to dictionary
                    alist[os.path.join(os.getcwd(), file)] = timestamp

                # sort the timestamp
            if SortByTime:
                for i in sorted(alist.iteritems(), key=operator.itemgetter(1)):
                    latest = "%s" % (i[0])
            else:
                for i in sorted(alist.iteritems(), key=operator.itemgetter(0)):
                    latest = "%s" % (i[0])
        except Exception, e:
            print "Exception %s" % e

        # latest=sorted(alist.iteritems(), key=operator.itemgetter(1))[-1]
        #latest = r'\\rim.net\builds_publish\Deliverables\BlackBerry_Link\1.0.0\bundle029'
        #print "newest directory is ", latest
        return latest
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Critical"

def NewestJenkinsBuild(Jenkins_Job_Name='BlackBerryDesktop_bb10_ux', Jenkins_URL="http://jenkins001cnc.rim.net:8080/"):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        from jenkinsapi import api
        latest_build_number = False
        jenkins = api.Jenkins(Jenkins_URL)
        jenkins_job = jenkins.get_job(Jenkins_Job_Name)
        for eachbuild in jenkins_job.get_build_ids():
            if jenkins_job.get_build(eachbuild).is_good():
                if jenkins_job.get_build(eachbuild).get_artifact_dict().has_key('BlackBerry Link.msi'):
                    latest_build_number = eachbuild
                    break
        return str(latest_build_number)
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Critical"

def CleaningUpRegistryDTSKeys():
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        shlwapi = ctypes.windll.shlwapi
        SHDeleteKey = shlwapi.SHDeleteKeyW
        try:
            root, keypath = wintypes.HKEY (_winreg.HKEY_CURRENT_USER), ur"Software\Research In Motion"
            result = SHDeleteKey (root, keypath)
            if result == 0:
                print "HKEY_CURRENT_USER\Software\Research In Motion Reg key deleted"
            else:
                print "HKEY_CURRENT_USER\Software\Research In Motion Reg key not found"
        except Exception, e:
            print "Exception %s" % e
            return "Error in deleting HKEY_CURRENT_USER\Software\Research In Motion Reg key", e

        if CommonUtil.GetOSBit() == '32':
            try:
                root, keypath = wintypes.HKEY (_winreg.HKEY_LOCAL_MACHINE), ur"Software\Research In Motion"
                result = SHDeleteKey (root, keypath)
                if result == 0:
                    print "HKEY_LOCAL_MACHINE\Software\Research In Motion Reg key deleted"
                else:
                    print "HKEY_LOCAL_MACHINE\Software\Research In Motion Reg key not found"
            except Exception, e:
                print "Exception %s" % e
                return "Error in deleting HKEY_LOCAL_MACHINE\Software\Research In Motion Reg key", e

        if CommonUtil.GetOSBit() == '64':
            try:
                root, keypath = wintypes.HKEY (_winreg.HKEY_LOCAL_MACHINE), ur"Software\Wow6432Software\Research In Motion"
                result = SHDeleteKey (root, keypath)
                if result == 0:
                    print "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Research In Motion Reg key deleted"
                else:
                    print "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Research In Motion Reg key not found"
            except Exception, e:
                print "Exception %s" % e
                return "Error in deleting HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Research In Motion Reg key", e
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Critical"

def CleaningLeftoverDTSFolders():
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        CommonUtil.KillAllRimProcess()
        FoldersList = []
        FoldersList.append(ComPath.Get_Appdata_Path())
        FoldersList.append(ComPath.Get_local_Appdata_Path())
        FoldersList.append(ComPath.Get_Program_Files_Common_Path())
        FoldersList.append(ComPath.Get_Program_Files_Path())
        FoldersList.append(unicode('C:\\ProgramData'))
        FoldersList.append(unicode('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs'))

        try:

            for eachElement in FoldersList:
                eachPath = str(eachElement)
                for Root, Folders, Files in os.walk(eachPath):
                    for file in Files:
                        if file == "Rim" or file == "Research" or file == "Blackberry":
                            os.unlink(os.path.join(Root, file))
                    for Folder in Folders:
                        if "Research" in Folder:
                            FileUtilities.ChangePermission(Root + '\\' + Folder)
                            shutil.rmtree(os.path.join(Root, Folder))
        except Exception, e:
            print "Exception %s" % e
            return "Error in cleaning left over dts files", e
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Critical"

def AddingWorkaroundRegistryKeys():
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        print "Adding Reg Keys"
        if CommonUtil.GetOSBit() == '32':
            print "32 bit os"
            keyVal1 = r'SOFTWARE\Research In Motion\AppLoader'
            keyVal2 = r'Software\Research In Motion\Blackberry\Manager'
            keyVal3 = r'SOFTWARE\Research In Motion\BlackBerry Desktop\Device Characteristics'
            keyVal4 = r'SOFTWARE\Research In Motion\Common\Installations\Desktop 10'
            keyVal5 = r'SOFTWARE\Research In Motion\BBDevMgr'
            keyVal6 = r'SOFTWARE\Research In Motion\BlackBerry 10 Desktop\DesktopPolicy'
            try:
                key1 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, keyVal1, 0, _winreg.KEY_ALL_ACCESS)
                key2 = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyVal2, 0, _winreg.KEY_ALL_ACCESS)
                key3 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, keyVal3, 0, _winreg.KEY_ALL_ACCESS)
                key4 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, keyVal4, 0, _winreg.KEY_ALL_ACCESS)
                key5 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, keyVal5, 0, _winreg.KEY_ALL_ACCESS)
                key6 = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyVal6, 0, _winreg.KEY_ALL_ACCESS)
            except:
                key1 = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, keyVal1)
                key2 = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, keyVal2)
                key3 = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, keyVal3)
                key4 = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, keyVal4)
                key5 = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, keyVal5)
                key6 = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, keyVal6)

            _winreg.SetValueEx(key1, "SLSURL", 0, _winreg.REG_SZ, "https://cse.beta.sl.eval.blackberry.com/cse/ping/1.0.0/")
            _winreg.SetValueEx(key2, "DeviceXMLInternalURL", 0, _winreg.REG_SZ, "http://x-desktop.rim.net/XML/Device.xml")
            _winreg.SetValueEx(key3, "InternalUrl", 0, _winreg.REG_SZ, "http://x-desktop.rim.net/")
            _winreg.SetValueEx(key5, "DisableLogOut", 0, _winreg.REG_DWORD, 0x00000000)
            _winreg.SetValueEx(key5, "LogMask", 0, _winreg.REG_DWORD, 0x000000ff)
            _winreg.SetValueEx(key6, "PimImportEnabled", 0, _winreg.REG_DWORD, 0x00000001)

            #Set Version Registry key only if it is 0.x.x.x
            try:
                i = 0
                SetVersion = True
                while True:
                    subkey = _winreg.EnumValue(key4, i)
                    if subkey[0] == 'Version':
                        if subkey[1].startswith('0'):
                            print "version starting with 0:", subkey[1]
                        else:
                            print "version is:", subkey[1]
                            SetVersion = False
                        break

                    i += 1
            except WindowsError:
                pass
            if SetVersion:
                _winreg.SetValueEx(key4, "Version", 0, _winreg.REG_SZ, "10.0.0.0")

            #Close all keys
            _winreg.CloseKey(key1)
            _winreg.CloseKey(key2)
            _winreg.CloseKey(key3)
            _winreg.CloseKey(key4)
            _winreg.CloseKey(key6)

        if CommonUtil.GetOSBit() == '64':
            print "64 bit os"
            keyVal1 = r'SOFTWARE\Wow6432Node\Research In Motion\AppLoader'
            keyVal2 = r'Software\Research In Motion\Blackberry\Manager'
            keyVal3 = r'SOFTWARE\Wow6432Node\Research In Motion\BlackBerry Desktop\Device Characteristics'
            keyVal4 = r'SOFTWARE\Wow6432Node\Research In Motion\Common\Installations\Desktop 10'
            keyVal6 = r'SOFTWARE\Research In Motion\BlackBerry 10 Desktop\DesktopPolicy'

            try:
                key1 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, keyVal1, 0, _winreg.KEY_ALL_ACCESS)
                key2 = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyVal2, 0, _winreg.KEY_ALL_ACCESS)
                key3 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, keyVal3, 0, _winreg.KEY_ALL_ACCESS)
                key4 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, keyVal4, 0, _winreg.KEY_ALL_ACCESS)
                key6 = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyVal6, 0, _winreg.KEY_ALL_ACCESS)

            except:
                key1 = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, keyVal1)
                key2 = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, keyVal2)
                key3 = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, keyVal3)
                key4 = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, keyVal4)
                key6 = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, keyVal6)

            _winreg.SetValueEx(key1, "SLSURL", 0, _winreg.REG_SZ, "https://cse.beta.sl.eval.blackberry.com/cse/ping/1.0.0/")
            _winreg.SetValueEx(key2, "DeviceXMLInternalURL", 0, _winreg.REG_SZ, "http://x-desktop.rim.net/XML/Device.xml")
            _winreg.SetValueEx(key3, "InternalUrl", 0, _winreg.REG_SZ, "http://x-desktop.rim.net/")
            _winreg.SetValueEx(key4, "Version", 0, _winreg.REG_SZ, "10.0.0.0")
            _winreg.SetValueEx(key6, "PimImportEnabled", 0, _winreg.REG_DWORD, 0x00000001)

            _winreg.CloseKey(key1)
            _winreg.CloseKey(key2)
            _winreg.CloseKey(key3)
            _winreg.CloseKey(key4)
            _winreg.CloseKey(key6)
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Critical"

def Initialworkaround(DailyBuildNWPath, build_type, release_branch):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        print "NewInitialWorkAround"
        if os.name == 'nt':
            DailyBuildLocalPath = 'C:\\DailyBuild\\'
            InstallFolderName = 'Desktop_Installer_MultiLang'
            LatestBuildLocSCM = 'C:\\DailyBuild\\Latest\\MultiLanguage\\CD\\'

        elif os.name == 'posix':
            DailyBuildLocalPath = ComPath.Get_Current_User_Path() + os.sep + 'Downloads' + os.sep + 'DailyBuild'
            InstallFolderName = 'MacDesktop'
            LatestBuildLocSCM = DailyBuildLocalPath + os.sep + 'Latest' + os.sep
        newFolder = 'Latest'
        BuildNumFilePath = DailyBuildLocalPath + os.sep + 'BuildNum.txt'
        #DailyBuildNWPath = "\\\\rim.net\\software\\Tachyon\\Desktop"
        #Create the download location if its not there already
        if os.path.isdir(DailyBuildLocalPath) != True:
            FileUtilities.CreateFolder(DailyBuildLocalPath)

        try:
            if build_type == 'SCM':
                print "SCM path in initialisation"
                NewNWBuildPath = NewBuildPath(DailyBuildNWPath + os.sep + release_branch)
                PathLoc = NewNWBuildPath + os.sep + InstallFolderName
                NewNWBuildPath = NewBuildPath(PathLoc)
                FolName = os.path.basename(NewNWBuildPath)#ExtractFolderFromPath(NewNWBuildPath)
                #DestLoc = DailyBuildLocalPath+FolName
            else:
                NewNWBuildPath = NewBuildPath(DailyBuildNWPath)
        except Exception, e:
            print "Exception %s" % e
            CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
            return "Error in retrieving latest build path", e

        #FileUtilities.CreateEmptyFolder(DailyBuildLocalPath,newFolder)
        try:
            print "Copying build"
            shutil.copytree(NewNWBuildPath, DailyBuildLocalPath + os.sep + 'Latest')
        except Exception, e:
            print "Exception %s" % e
            CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
            return "Error in copying new build to destination location", e

        # Install
        try:
            print "Installation process"
            if build_type == 'SCM':
                LatestBuildLoc = LatestBuildLocSCM
            elif build_type == 'Tachyon':
                LatestBuildLoc = 'C:\\DailyBuild\\Latest\\INSTALLER_MULTILANG\\MultiLanguage\\CD\\'
            else:
                LatestBuildLoc = 'C:\\DailyBuild\\Latest\\DISK1'
            #insLoc = "msiexec /i " + LatestBuildLoc + "\\BlackB~1.msi /quiet /log install.log"
            if os.name == 'nt':
                insLoc = LatestBuildLoc + '\\setup.exe /S /v/qn'
            elif os.name == 'posix':
                insLoc = ""
            print "insLoc:", insLoc
            exitCode = CommonUtil.InstallUninstallBuild(insLoc)
        except Exception, e:
            print "Exception %s" % e
            CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
            return "Error in installing latest build- ", e

        # Uninstall
        try:
            unInstallLoc = "msiexec /uninstall " + LatestBuildLoc + "\\BlackB~1.msi /quiet /log install.log"
            exitCode = CommonUtil.InstallUninstallBuild(unInstallLoc)
            CleaningUpRegistryDTSKeys()
            CleaningLeftoverDTSFolders()
        except Exception, e:
            print "Exception %s" % e
            CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
            return "Error in uninstalling latest build- ", e

        # deleting the latest folder
        try:
            shutil.rmtree('C:\\DailyBuild\\Latest')
        except Exception, e:
            print "Exception %s" % e
            CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
            return "Error in deleting temporary Latest Folder- ", e

        # update TxtFileContent variable
        try:
            CommonUtil.WriteToFile(BuildNumFilePath, "No Build")
        except Exception, e:
            print "Exception %s" % e
            return "Error in writing initial value to the Build.txt file- ", e
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Critical"


def RestartMachine():
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        if os.name == 'nt':
            retValue = CommonUtil.InstallUninstallBuild("shutdown /r /t 1")
        if retValue == 1:
            print "Restarted machine successfully"
            CommonUtil.ExecLog(sModuleInfo, "Restarted machine successfully", 4)
        else:
            print "Machine restart failed"
            CommonUtil.ExecLog(sModuleInfo, "restart failed", 4)
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Critical"


def InstallBuild(LatestLocalBuildName, testerid, build_type, release_branch, DailyBuildLocalPath, LatestNWBundleName):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        #update status
        UpdateBuildStatusDB(testerid, "Installing", LatestLocalBuildName, "Insert", build_type, release_branch, "N/A", "N/A")

        if os.name == 'nt':
            if build_type == 'SCM':
                print "Building install location"
                LatestBuildLoc = DailyBuildLocalPath + os.sep + LatestLocalBuildName + os.sep + 'MultiLanguage' + os.sep + 'CD' + os.sep
            elif build_type == 'Tachyon':
                LatestBuildLoc = DailyBuildLocalPath + os.sep + LatestLocalBuildName + os.sep + 'MultiLanguage' + os.sep + 'CD' + os.sep
            else:
                LatestBuildLoc = DailyBuildLocalPath + os.sep + LatestLocalBuildName + os.sep + 'DISK1' + os.sep
            #insLoc = "msiexec /i " + LatestBuildLoc + "BlackB~1.msi /quiet /log install.log"
            insLoc = LatestBuildLoc + os.sep + 'setup.exe /S /v/qn'
            print "Install command: " + insLoc
            exitCode = CommonUtil.InstallUninstallBuild(insLoc)
            print "Install exit code:", exitCode
            print "Restarting Machine"
            print RestartMachine()
        elif os.name == 'posix':
            applescriptpath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Install_MacBBL.scpt'
            insLoc = "osascript %s %s" % (applescriptpath, LatestLocalBuildName)
            print "Install command: " + insLoc
            exitCode = CommonUtil.InstallUninstallBuild(insLoc)
            print "Install exit code:", exitCode
        time.sleep(5)
        IsInstalled = False
        seconds = 0
        while IsInstalled == False and seconds < 60:
            time.sleep(1)
            IsInstalled = CommonUtil.FindingProcess("BlackBerry Link")
            seconds = seconds + 1

        if IsInstalled == True:
            print "Installation completed successfully"
            CommonUtil.ExecLog(sModuleInfo, "Installation completed successfully", 4)
            retValue = "Pass"
            ############################# UPDATE STATUS TO NEW BUILD INSTALLED SUCCESSFULLLY
            UpdateBuildStatusDB(testerid, "Latest build installed locally", LatestNWBundleName, "Insert", build_type, release_branch, "N/A", "N/A")
            #update status
            UpdateBuildStatusDB(testerid, "Installed", LatestLocalBuildName, "Insert", build_type, release_branch, "N/A", "N/A")
        else:
            print "Installation failed"
            CommonUtil.ExecLog(sModuleInfo, "Installation failed", 4)
            retValue = "Critical"
            UpdateBuildStatusDB(testerid, "Not able to install latest build", LatestNWBundleName, "Insert", build_type, release_branch, "N/A", "N/A")

            UpdateBuildStatusDB(testerid, "Failed", LatestNWBundleName, "Insert", build_type, release_branch, "N/A", "N/A")
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Critical"
def UninstallBuild(testerid, DailyBuildLocalPath, LatestLocalBuildName, LatestNWBundleName, build_type, release_branch):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        #if BBL is installed, then uninstall it
        if CommonUtil.FindingProcess("BlackBerry Link"):
            print "Previous build exist. Will uninstall now"
            CommonUtil.ExecLog(sModuleInfo, "Uninstalling previous build found", 4)

            CommonUtil.KillAllRimProcess()
            #using the name, create path to msi and do uninstall
            if os.name == 'nt':
                if build_type == 'SCM':
                    print "Building uninstall location"
                    PrevBuildLoc = DailyBuildLocalPath + os.sep + LatestLocalBuildName + '\\MultiLanguage\\CD\\'
                elif build_type == 'Tachyon':
                    PrevBuildLoc = 'C:\\DailyBuild\\' + LatestLocalBuildName + '\\INSTALLER_MULTILANG\\MultiLanguage\\CD\\'
                else:
                    PrevBuildLoc = 'C:\\DailyBuild\\' + LatestLocalBuildName + '\\DISK1\\'

                #unInstallLoc = "msiexec /uninstall " + PrevBuildLoc + "BlackB~1.msi /quiet /log install.log"
                #print "Uninstall command: "+unInstallLoc
                #exitCode = CommonUtil.InstallUninstallBuild(unInstallLoc)
                #print "uninstall exitcode:"
                #print exitCode
                try:
                    import wmi
                    c = wmi.WMI()
                    for product in c.Win32_Product(Name='BlackBerry Link'):
                        print "Found BlackBerry Link in installed products"
                        CommonUtil.ExecLog(sModuleInfo, "Found BlackBerry Link in installed products", 4)
                        retValue = product.Uninstall()
                        print "Uninstall of BlackBerry Link completed:", retValue
                        CommonUtil.ExecLog(sModuleInfo, "Uninstall completed:%s" % retValue, 4)
                        break
                    print "Restarting Machine"
                    print RestartMachine()
                except Exception, e:
                    print "Uninstall exception:", e
                    CommonUtil.ExecLog(sModuleInfo, "Uninstall exception:%s" % e, 4)
                time.sleep(30)
                CleaningUpRegistryDTSKeys()
                time.sleep(30)
                CleaningLeftoverDTSFolders()
            elif os.name == 'posix':
                applescriptpath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Uninstall_MacBBL.scpt'
                insLoc = "osascript %s %s" % (applescriptpath, LatestLocalBuildName)
                print "Uninstall command:", insLoc
                exitCode = CommonUtil.InstallUninstallBuild(insLoc)
                print "Uninstall exit code:", exitCode
             ##################################### UPDATE STATUS TO PREVIOUS BUILD UIINSTALLED

        #keep checking in a loop if uninstall is done, then only proceed to next step
        print "Checking if build is uninstalled successfully"
        IsInstalled = True
        seconds = 0
        while IsInstalled == True and seconds < 60:
            time.sleep(1)
            IsInstalled = CommonUtil.FindingProcess("BlackBerry Link")
            seconds = seconds + 1
        time.sleep(5)

        if IsInstalled == False:
            print "Uninstall completed successfully"
            CommonUtil.ExecLog(sModuleInfo, "Uninstall completed successfully", 4)
            UpdateBuildStatusDB(testerid, "Previous build uninstalled", LatestNWBundleName, "Insert", build_type, release_branch, "N/A", "N/A")
            return "Pass"
        else:
            print "Uninstall of the current build failed"
            CommonUtil.ExecLog(sModuleInfo, "Uninstall of the current build failed", 4)
            UpdateBuildStatusDB(testerid, "Not able to uninstall previous build", LatestNWBundleName, "Insert", build_type, release_branch, "N/A", "N/A")
            return "Critical"
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Critical"
def InstallationProcessNew(DailyBuildNWPath, build_type, release_branch, testerid):
    #Get latest build name from network
    #Get latest build locally from the buildname.txt file
    #Get latest build installed
    # if there is a new build available in the network, 
    #    download it first. 
    #    uninstall the current build if it is installed already
    #    restart machine & continue to run the tests
    #else if local installed build & network build is the same
    #    then continue to run the tests
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        ############Initialize constants##################
        if os.name == 'nt':
            DailyBuildLocalPath = 'C:\\DailyBuild'
            InstallFolderName = 'Desktop_Installer_MultiLang'
        elif os.name == 'posix':
            DailyBuildLocalPath = ComPath.Get_Current_User_Path() + os.sep + 'Downloads' + os.sep + 'DailyBuild'
            InstallFolderName = 'MacDesktop'

        if not os.path.isdir(DailyBuildLocalPath):
            FileUtilities.CreateFolder(DailyBuildLocalPath)

        # In a variable(NewBuildPathLoc) save the path returned from Tachyon location
        if build_type == 'SCM':
            #if os.name == 'posix':
            #    MountDrive('/Volumes/deliverables', '//rim.net/deliverables/BlackBerry_Link_Mac')
            NewNWBundlePath = NewBuildPath(DailyBuildNWPath + os.sep + release_branch)
            NewNWBuildPath = NewBuildPath(NewNWBundlePath + os.sep + InstallFolderName)
            print "Newest build in Network is ", NewNWBuildPath
            LatestNWBundleName = os.path.basename(NewNWBundlePath)#ExtractFolderFromPath(NewNWBuildPath)
            LatestNWBuildName = os.path.basename(NewNWBuildPath)

        else:
            #NewNWBuildPath = NewBuildPath(DailyBuildNWPath)
            #DailyBuildNWPah contains the Jenkins URL and Build_Type contains the Job Name
            LatestNWBuildName = NewestJenkinsBuild(build_type, DailyBuildNWPath)
            NewNWBuildPath = DailyBuildNWPath + "/job/" + build_type + "/" + LatestNWBuildName
            print "Newest build in Network is ", NewNWBuildPath
            LatestNWBundleName = LatestNWBuildName

        NewLocalBuildPath = NewBuildPath(DailyBuildLocalPath)
        if NewLocalBuildPath != '':
            print "Newest build in local download path is ", NewLocalBuildPath
        else:
            print "No build found in local download path"

        LatestLocalBuildName = os.path.basename(NewLocalBuildPath)

        #Get the Current status of Install Process for this machine from DB
        try:
            conn = DBU.ConnectToDataBase()
        except:
            print "unable to connect to the database"

        BuildInstallDetails = DBU.GetData(conn, "select bundle,status from daily_build_status where daily_build_user = '%s' order by id desc limit 1" % testerid, False)
        if BuildInstallDetails != []:
            LocalInstalledBuild = BuildInstallDetails[0][0]
            LocalInstallStatus = BuildInstallDetails[0][1]
        else:
            LocalInstalledBuild = ''
            LocalInstallStatus = ''

        ########Checking Network & deciding next action
        # Compare NewNWBuildPath with TxtFileContent
        if LatestLocalBuildName == LatestNWBuildName:
            print "Latest build from network is already present in local download path"
            #Latest folder in network is already copied to local
            #Check if BBL is installed
            if CommonUtil.FindingProcess("BlackBerry Link"):
                if LocalInstalledBuild == LatestLocalBuildName and LocalInstallStatus == 'Completed':
                    print "Smoke test for newest build is already completed. Wait for a new build"
                    CommonUtil.ExecLog(sModuleInfo, "Smoke test for newest build is already completed. Wait for a new build", 4)
                    retValue = "Latest already installed "
                elif LocalInstalledBuild == LatestLocalBuildName and (LocalInstallStatus == 'Installing' or LocalInstallStatus == 'Installed'):
                    print "Newest build is already installed. Starting to run Smoke tests"
                    CommonUtil.ExecLog(sModuleInfo, "Newest build is already installed. Starting to run Smoke tests", 4)
                    retValue = "Installation done successfully. "
                    ############################# UPDATE STATUS TO NEW BUILD INSTALLED SUCCESSFULLLY
                    UpdateBuildStatusDB(testerid, "Newest build is already installed. Starting to run Smoke tests", LatestNWBuildName, "Insert", build_type, release_branch, "N/A", "N/A")
                else:
                    print "Unknown status:", LocalInstallStatus
                    CommonUtil.ExecLog(sModuleInfo, "Unknown status:%s" % LocalInstallStatus, 4)
                    retValue = "Unknown status:%s" % LocalInstallStatus

            else:
                #Install current build & run tests
                print "BBLink is not installed currently. Starting to Install the newest build from local download path"
                CommonUtil.ExecLog(sModuleInfo, "BBLink is not installed currently. Starting to Install the newest build from local download path", 4)
                #install the recently copied build
                retValue = InstallBuild(LatestLocalBuildName, testerid, build_type, release_branch, DailyBuildLocalPath, LatestNWBundleName)
                if retValue == "Pass":
                    retValue = "Installation done successfully. "
                else:
                    retValue = "Installation failed. "


        elif LatestLocalBuildName != LatestNWBuildName:
            print "Latest build from network is not present in local download path"
            #### UPDATE THE STATUS TO NEW BUILD AVAILABLE 
            # if strings dont compare then copy the folder to the C:\DailyBuild location
            if build_type == 'SCM':
                print "SCM path"
                DestLoc = DailyBuildLocalPath + os.sep + LatestNWBuildName
            elif build_type == 'Tachyon':
                NewNWBuildPath = NewNWBuildPath + '\\INSTALLER_MULTILANG'
                DestLoc = DailyBuildLocalPath + os.sep + LatestNWBuildName
            else:
                DestLoc = DailyBuildLocalPath + os.sep + LatestNWBuildName
            print "Copying build to local folder:", NewNWBuildPath
            if os.path.isdir(NewNWBuildPath):
                Build_Copy = shutil.copytree(NewNWBuildPath, DestLoc)
            else:
                #Download build from Jenkins
                Build_Copy = urllib.urlretrieve(DailyBuildNWPath + "/job/" + build_type + "/" + LatestNWBuildName + "/artifact/Desktop/Installer/Build/Multilanguage/DiskImages/DISK1/*zip*/DISK1.zip", DestLoc + ".zip")
                print FileUtilities.UnzipFolder(DestLoc)
                FileUtilities.DeleteFile(DestLoc + ".zip")

            NewLocalBuildPath = NewBuildPath(DailyBuildLocalPath)
            LatestLocalBuildName = os.path.basename(NewLocalBuildPath)

            ################################ UPDATE THE STATUS TO NEW BUILD COPIED LOCALLY
            UpdateBuildStatusDB(testerid, "New build copied locally", LatestNWBuildName, "Insert", build_type, release_branch, "N/A", "N/A")
            time.sleep(10)

            retValue = UninstallBuild(testerid, DailyBuildLocalPath, LatestLocalBuildName, LatestNWBundleName, build_type, release_branch)
            if retValue == "Pass":
                print "Uninstall completed successfully"
                #once uninstall is done, install the recently copied build
                retValue = InstallBuild(LatestLocalBuildName, testerid, build_type, release_branch, DailyBuildLocalPath, LatestNWBundleName)
                if retValue == "Pass":
                    retValue = "Installation done successfully. "
                else:
                    retValue = "Installation failed"

            else:
                print "Uninstall of the current build failed"
                retValue = "Uninstall failed"
        # else if they are same, then latest is already installed, exit out
        else:
            retValue = "Latest already installed"
        RetVal = []

        val = retValue
        RetVal.append(val)
        print RetVal[0] + ":" + LatestNWBundleName
        return RetVal[0] + ":" + LatestNWBundleName
    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Error"

def UpdateBuildStatusDB(testerid, Status_Update, Bundle_Info, Axn, build_type, release_branch, runid, Path):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        oLocalEnvInfo = CommonUtil.LocalInfo()
        conn = DBU.ConnectToDataBase()
        if Axn == "Insert":
            print "Inserting status"
            DBU.InsertNewRecordInToTable(conn, 'daily_build_status',
                                            Daily_Build_User=testerid,
                                            Status=Status_Update,
                                            Last_Checked_Time=str(datetime.datetime.now()),
                                            machine_os=oLocalEnvInfo.getLocalOS(),
                                            local_IP=oLocalEnvInfo.getLocalIP(),
                                            Bundle=Bundle_Info,
                                            branch=build_type,
                                            release=release_branch,
                                            run_id=runid,
                                            build_path=Path
                                            )
        if Axn == "Update":
            print "Updating status"
            DBU.UpdateRecordInTable(conn, 'daily_build_status', "Where daily_build_user = '%s' and status = '%s'" % (testerid, Status_Update),
                                            #Daily_Build_User = testerid, 
                                            #Status = Status_Update, 
                                            Last_Checked_Time=str(datetime.datetime.now()),
                                            machine_os=oLocalEnvInfo.getLocalOS(),
                                            local_IP=oLocalEnvInfo.getLocalIP(),
                                            Bundle=Bundle_Info,
                                            branch=build_type,
                                            release=release_branch,
                                            run_id=runid,
                                            build_path=Path
                                            )

    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return False
def MountDrive(drive, networkpath, domain='rimnet', user='username', password='password'):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        mountoutput = subprocess.check_output('mount')
        if networkpath.startswith('//'):
            networkpath = networkpath.replace('//', '')
        if drive in mountoutput:
            print "%s is already mounted" % drive
            return True

        else:
            if not os.path.isdir(drive):
                print subprocess.check_call('mkdir \"%s\"' % drive, shell=True)
            print subprocess.check_call('mount -t smbfs \'//%s;%s:%s@%s\' \'%s\'' % (domain, user, password, networkpath, drive), shell=True)
            print "%s is mounted" % drive
            return True

    except Exception, e:
        print "Exception:", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return False

#print NewestJenkinsBuild()
#print InstallationProcessNew("http://jenkins001cnc.rim.net:8080", "BlackBerryDesktop_bb10_ux", "10.2", "jnibumon3e03")
