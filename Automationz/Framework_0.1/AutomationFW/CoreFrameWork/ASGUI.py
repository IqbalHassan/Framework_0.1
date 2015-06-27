import wx,time
import wx.wizard
import sys
import threading
import os
import DataBaseUtilities as DB
from dependencyCollector import product_version,dependency
import CommonUtil
import Global
import MainDriver
import FileUtilities
import ConfigParser
class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl
    def write(self,string):
        self.out.WriteText(string)

class WizardPage(wx.wizard.PyWizardPage):
    def __init__(self, parent, title):
        wx.wizard.PyWizardPage.__init__(self, parent)
        self.next = None
        self.prev = None
        self.initializeUI(title)

    def initializeUI(self, title):
        # create grid layout manager
        self.sizer = wx.GridBagSizer(5)
        self.SetSizerAndFit(self.sizer)

    def addWidget(self, widget, pos, span):
        self.sizer.Add(widget, pos, span, wx.EXPAND)

    # getters and setters
    def SetPrev(self, prev):
        self.prev = prev

    def SetNext(self, next):
        self.next = next

    def GetPrev(self):
        return self.prev

    def GetNext(self):
        return self.next
class MyWizard(wx.wizard.Wizard):
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.wizard.Wizard.__init__(self, None, -1, "Automation Solutionz")
        self.SetPageSize((500, 350))
        self.login_page=self.create_login_page()
        self.console_log=self.create_log_page()
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED,self.pageChanged)
        self.Bind(wx.wizard.EVT_WIZARD_FINISHED,self.Destruction)
        self.RunWizard(self.login_page)
    def Destruction(self):
        self.Destroy()
    def create_login_page(self):
        login_page=WizardPage(self,"login_page")
        Username_label=wx.StaticText(login_page,label="Username: ")
        login_page.addWidget(Username_label,(1,10),(1,10))
        self.username = wx.TextCtrl(login_page)
        self.username.SetValue('shetu')
        login_page.addWidget(self.username,(1,20),(1,20))
        password_label = wx.StaticText(login_page,label="Password: ")
        login_page.addWidget(password_label,(2,10),(1,10))
        self.password = wx.TextCtrl(login_page,style=wx.TE_PASSWORD)
        self.password.SetValue('shetu')
        login_page.addWidget(self.password,(2,20),(1,20))
        server_text=wx.StaticText(login_page,label="Server: ")
        login_page.addWidget(server_text,(3,10),(1,10))
        self.ServerText=wx.TextCtrl(login_page)
        self.ServerText.SetValue('127.0.0.1')
        login_page.addWidget(self.ServerText,(3,20),(1,20))
        port_text=wx.StaticText(login_page,label="Port: ")
        login_page.addWidget(port_text,(4,10),(1,10))
        self.port=wx.TextCtrl(login_page)
        self.port.SetValue('5432')
        login_page.addWidget(self.port,(4,20),(1,20))
        project_text=wx.StaticText(login_page,label="Project: ")
        login_page.addWidget(project_text,(5,10),(1,10))
        self.project=wx.TextCtrl(login_page)
        self.project.SetValue('Automation Solutionz')
        login_page.addWidget(self.project,(5,20),(1,20))
        team_text=wx.StaticText(login_page,label="Team: ")
        login_page.addWidget(team_text,(6,10),(1,10))
        self.team=wx.TextCtrl(login_page)
        self.team.SetValue('AutomationTester')
        login_page.addWidget(self.team,(6,20),(1,20))
        return login_page
    def create_log_page(self):
        console_log=WizardPage(self,"console_page")
        console_log.SetName("consolePage")
        self.log=wx.TextCtrl(console_log,style=wx.TE_MULTILINE|wx.TE_READONLY,size=(600,600))
        #self.log.Disable()
        dir=RedirectText(self.log)
        sys.stdout=dir
        sys.stderr=dir
        self.login_page.SetNext(console_log)

    def OnUpdate(self,event):
        username = self.username.GetValue()
        password = self.password.GetValue()
        server = self.ServerText.GetValue()
        port = self.port.GetValue()
        project = self.project.GetValue()
        team = self.team.GetValue()
        forward_btn = self.FindWindowById(wx.ID_FORWARD)
        if username and password and server and project and team and port:
            forward_btn.Enable()
        else:
            forward_btn.Disable()
    def pageChanged(self,evt):
        page=evt.GetPage()
        if page.GetName()=='consolePage':
            username=self.username.GetValue()
            password=self.password.GetValue()
            server = self.ServerText.GetValue()
            port = self.port.GetValue()
            project = self.project.GetValue()
            team = self.team.GetValue()
            worker=AS(username,password,project,team,server,port)
            worker.setName("Automation Solutionz is running")
            worker.start()
class AS(threading.Thread):
    def __init__(self,username,password,project,team,server,port):
        threading.Thread.__init__(self)
        self.username=username
        self.password=password
        self.project=project
        self.team=team
        self.server=server
        self.port=port
    def run(self):
        print threading.currentThread().getName()
        if self.check_credential():
            self.run_process(self.update_machine(self.collectAllDependency(dependency)))
        else:
            self.update_machine(self.collectAllDependency(dependency))
    def run_process(self,sTesterid):
        while (1):
            try:
                conn = DB.ConnectToDataBase(sHost=self.server)
                status = DB.GetData(conn, "Select status from test_run_env where tester_id = '%s' and status in ('Submitted','Unassigned') limit 1 " % (sTesterid))
                conn.close()
                if len(status) == 0:
                    continue
                if status[0] != "Unassigned":
                    if status[0] == "Submitted":
                        #first Create a temp folder in the samefolder
                        current_path=os.getcwd()+os.sep+'LogFiles'
                        retVal=FileUtilities.CreateFolder(current_path,forced=False)
                        if retVal:
                            Global.RunIdTempPath=current_path
                            #now save it in the global_config.ini
                            current_path_file=os.getcwd()+os.sep+'global_config.ini'
                            config=ConfigParser.SafeConfigParser()
                            config.add_section('sectionOne')
                            config.set('sectionOne','temp_run_file_path',current_path)
                            with (open(current_path_file,'w')) as configFile:
                                config.write(configFile)
                        value=MainDriver.main(self.server)
                        print "updating db with parameter"
                        if value=="pass":
                            break
                        print "Successfully updated db with parameter"

                elif status[0] == "Unassigned":
                    time.sleep(3)
                    conn = DB.ConnectToDataBase(sHost=self.server)
                    last_updated_time=CommonUtil.TimeStamp("string")
                    DB.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'Unassigned'" % sTesterid, last_updated_time=last_updated_time)
                    conn.close()
            except Exception, e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
                print Error_Detail
        return True

    def update_machine(self,dependency):
        try:
            #Get Local Info object
            oLocalInfo = CommonUtil.LocalInfo()

            if os.path.isdir(Global.NetworkFolder) != True:
                print "Failed to access Network folder"
                #return False
                local_ip = oLocalInfo.getLocalIP() #+ " - Network Error"
            else:
                local_ip = oLocalInfo.getLocalIP()
            testerid = (oLocalInfo.getLocalUser()).lower()
            #product_version = ' '
            productVersion=product_version
            UpdatedTime = CommonUtil.TimeStamp("string")
            query="select count(*) from permitted_user_list where user_level='Automation' and user_names='%s'"%testerid
            Conn=DB.ConnectToDataBase(sHost=self.server)
            count=DB.GetData(Conn,query)
            Conn.close()
            if isinstance(count,list) and count[0]==0:
                #insert to the permitted_user_list
                temp_Dict={
                    'user_names':testerid,
                    'user_level':'Automation',
                    'email':testerid+"@machine.com"
                }
                Conn=DB.ConnectToDataBase(sHost=self.server)
                result=DB.InsertNewRecordInToTable(Conn,"permitted_user_list",**temp_Dict)
                Conn.close()

            #update the test_run_env table
            dict={
                'tester_id':testerid,
                'status':'Unassigned',
                'last_updated_time':UpdatedTime,
                'machine_ip':local_ip,
                'branch_version':productVersion
            }
            conn=DB.ConnectToDataBase(sHost=self.server)
            status = DB.GetData(conn, "Select status from test_run_env where tester_id = '%s'" % testerid)
            conn.close()
            for eachitem in status:
                if eachitem == "In-Progress":
                    conn=DB.ConnectToDataBase(sHost=self.server)
                    DB.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'In-Progress'" % testerid, status="Cancelled")
                    conn.close()
                    conn=DB.ConnectToDataBase(sHost=self.server)
                    DB.UpdateRecordInTable(conn, "test_env_results", "where tester_id = '%s' and status = 'In-Progress'" % testerid, status="Cancelled")
                    conn.close()
                elif eachitem == "Submitted":
                    conn=DB.ConnectToDataBase(sHost=self.server)
                    DB.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'Submitted'" % testerid, status="Cancelled")
                    conn.close()
                    conn=DB.ConnectToDataBase(sHost=self.server)
                    DB.UpdateRecordInTable(conn, "test_env_results", "where tester_id = '%s' and status = 'Submitted'" % testerid, status="Cancelled")
                    conn.close()
                elif eachitem == "Unassigned":
                    conn=DB.ConnectToDataBase(sHost=self.server)
                    DB.DeleteRecord(conn, "test_run_env", tester_id=testerid, status='Unassigned')
                    conn.close()
            conn=DB.ConnectToDataBase(sHost=self.server)
            result=DB.InsertNewRecordInToTable(conn,"test_run_env",**dict)
            conn.close()
            if result:
                conn=DB.ConnectToDataBase(sHost=self.server)
                machine_id=DB.GetData(conn,"select id from test_run_env where tester_id='%s' and status='Unassigned'"%testerid)
                conn.close()
                if isinstance(machine_id,list) and len(machine_id)==1:
                    machine_id=machine_id[0]
                for each in dependency:
                    type_name=each[0]
                    listings=each[1]
                    for eachitem in listings:
                        temp_dict={
                            'name':eachitem[0],
                            'bit':eachitem[1],
                            'version':eachitem[2],
                            'type':type_name,
                            'machine_serial':machine_id
                        }
                        conn=DB.ConnectToDataBase(sHost=self.server)
                        result=DB.InsertNewRecordInToTable(conn,"machine_dependency_settings",**temp_dict)
                        conn.close()
                query="select project_id from projects where project_name='%s'"%self.project
                Conn=DB.ConnectToDataBase(sHost=self.server)
                project_id=DB.GetData(Conn,query)
                Conn.close()
                if isinstance(project_id,list) and len(project_id):
                    project_id=project_id[0]
                else:
                    project_id=''
                conn=DB.ConnectToDataBase(sHost=self.server)
                teamValue=DB.GetData(conn,"select id from team where team_name='%s' and project_id='%s'"%(self.team,project_id))
                conn.close()
                if isinstance(teamValue,list) and len(teamValue)==1:
                    team_identity=teamValue[0]
                temp_dict={
                    'machine_serial':machine_id,
                    'project_id':project_id,
                    'team_id':team_identity
                }
                conn=DB.ConnectToDataBase(sHost=self.server)
                result=DB.InsertNewRecordInToTable(conn,"machine_project_map",**temp_dict)
                conn.close()
                if result:
                    return testerid
            return False
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
            print Error_Detail
    def check_credential(self):
        try:
            query="select distinct user_id::text from user_project_map upm, projects p where upm.project_id=p.project_id and p.project_name='%s'"%(self.project.strip())
            Conn=DB.ConnectToDataBase(sHost=self.server)
            user_list=DB.GetData(Conn, query)
            Conn.close()
            #user_list=user_list[0]
            message=",".join(user_list)
            query="select count(*) from user_info ui, permitted_user_list pul where ui.full_name=pul.user_names and username='%s' and password='%s' and user_level not in ('email','Automation', 'Manual') and user_id in (%s)"%(self.username,self.password,message)
            Conn=DB.ConnectToDataBase(sHost=self.server)
            count=DB.GetData(Conn,query)
            Conn.close()
            if len(count)==1 and count[0]==1:
                return True
            else:
                print "No user found with Name: %s"%self.username
                return False
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
            print Error_Detail
    def collectAllDependency(self,dependency):
        try:
            query="select distinct project_id from projects where project_name='%s'"%self.project.strip()
            Conn=DB.ConnectToDataBase(sHost=self.server)
            project_id=DB.GetData(Conn,query)
            Conn.close()
            if isinstance(project_id,list) and len(project_id)==1:
                project_id=project_id[0]
            else:
                project_id=''
            query="select distinct dependency_name from dependency d ,dependency_management dm where d.id=dm.dependency and dm.project_id='%s' and dm.team_id=(select id from team where team_name='%s' and project_id='%s')"%(project_id,self.team.strip(),project_id)
            Conn=DB.ConnectToDataBase(sHost=self.server)
            dependency_list=DB.GetData(Conn, query)
            Conn.close()
            #print "Dependency: ",dependency_list

            #Get Local Info object
            oLocalInfo = CommonUtil.LocalInfo()

            final_dependency=[]
            for each in dependency_list:
                temp=""
                temp_list=[]
                if each in dependency.keys():
                    if dependency[each]!='':
                        temp=dependency[each]
                    else:
                        if each=='Platform':
                            temp=oLocalInfo.getLocalOS()
                        if each=='Browser':
                            temp=oLocalInfo.getInstalledClients()
                else:
                    if each=='Platform':
                        temp=oLocalInfo.getLocalOS()
                    if each=='Browser':
                        temp=oLocalInfo.getInstalledClients()
                    if each=='OS':
                        import platform
                        temp=platform.platform()
                if temp!='':
                    if each=='Platform':
                        bit=int(temp.split('-')[1].strip()[0:2])
                        version=temp.split('-')[0].split(' ')[1].strip()
                        name=temp.split('-')[0].split(' ')[0].strip()
                        temp_list.append((name,bit,version))
                    if each=='Browser':
                        temp=temp.split(",")
                        for eachitem in temp:
                            bit=int(eachitem.split(";")[1].strip()[0:2])
                            version=eachitem.split(";")[0].split("(")[1].split("V")[1].strip()
                            name=eachitem.split(";")[0].split("(")[0].strip()
                            temp_list.append((name,bit,version))
                    if each=='TestCaseType':
                        temp_list.append((temp,0,''))
                    if each=='OS':
                        if temp.index('Windows')==0:
                            name='PC'
                            version=platform.platform()[platform.platform().index('Windows')+len('Windows')+1:platform.platform().index('Windows')+len('Windows')+2]
                            if 'PROGRAMFILES(x86)' in os.environ:
                                bit=64
                            else:
                                bit=32
                        else:
                            name='MAC'
                            version='0'
                            bit=''
                        temp_list.append((name,bit,version))
                    final_dependency.append((each,temp_list))

            return final_dependency
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
            print Error_Detail
def main():
    """"""
    wizard = MyWizard()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(redirect=True)
    main()
    app.MainLoop()
    print 'ok'