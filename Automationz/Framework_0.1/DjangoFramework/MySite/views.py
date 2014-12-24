
# -*- coding: utf-8 -*-

# Create your views here.
import inspect
import itertools
from mimetypes import MimeTypes
import operator
import re
import time
import datetime
import EmailNotify
import urllib2
import datetime
            

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.db import connection
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.template.loader import get_template
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from psycopg2.extras import DictCursor

from CommonUtil import TimeStamp
from FileUploader import FileUploader
import DataBaseUtilities as DB
from TestCaseCreateEdit import LogMessage
import TestCaseCreateEdit
from TestCaseOperations import Cleanup_TestCase
import TestCaseOperations
from models import GetData, GetColumnNames, GetQueryData, GetConnection

from MySite.forms import Comment
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from settings import MEDIA_ROOT,PROJECT_ROOT
import os
import RequirementOperations
import TaskOperations
from TaskOperations import testConnection
import BugOperations
import LogModule
from LogModule import PassMessasge
from django.contrib.messages.storage.base import Message
from _ast import BitAnd
# #
#=======
# >>>>>>> parent of 5208765... Create Test Set added with create,update and  function
# from django.shortcuts import render_to_response
#=======
# >>>>>>> 79295d8a9281fee2054c6e15061b281b41f17493
try:
    import simplejson as json
except ImportError:
    import json


'''
Global variables
'''
path_to_uploaded_files = os.path.join(os.getcwd(), 'site_media', 'file_uploads')



# import DjangoConstants
# from pylab import * #http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib and http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
# import pylab
#Conn = GetConnection()
# import logging

""" Misc functions """
def TimeDiff(sYourTime):
    from datetime import datetime

    def mytime(stime):
        Year = stime[0:4]
        Month = stime[4:6]
        Day = stime[6:8]
        Hour = stime[8:10]
        Minute = stime[10:12]
        Second = stime[12:14]
        MyTime = "%s-%s-%s-%s-%s-%s" % (Year, Month, Day, Hour, Minute, Second)
        tim = datetime.strptime(MyTime, '%Y-%m-%d-%H-%M-%S')
        return tim

    NowTime = datetime.now().strftime("%Y%m%d%H%M%S")
    CurrentTime = mytime(NowTime)
    MachineTime = mytime(sYourTime)
    if CurrentTime > MachineTime:
        Sec = (CurrentTime - MachineTime).seconds
        Min = Sec / 60
    else:
        Min = 0
    return Min



def GetProjectNameForTopBar(request):
    if request.is_ajax():
        if request.method=='GET':
            query="select project_id from projects"
            Conn=GetConnection()
            project_name_id=DB.GetData(Conn, query,False)
            #Conn.close()
            #be sure that there will be a project name other wise the page will refresh
            user_id=request.GET.get(u'user_id','')
            Dict={
                  'projects':project_name_id,
                  }
            query="select id,value from config_values where type='Team'"
            #testConnection(Conn)
            #Conn=GetConnection()
            all_teams=DB.GetData(Conn,query,False)
            Conn.close()
            Dict.update({
                'teams':all_teams
            })
    result=simplejson.dumps(Dict)
    return HttpResponse(result,mimetype='application/json')

""" Main Pages functions """
# @login_required(login_url='/Home/Login/')
def HomePage(req):
    templ = get_template('HomePage.html')
    variables = Context({})
    output = templ.render(variables)
    return HttpResponse(output)

def RunTest(request):
    #get the available machine definition
    #query="select distinct tester_id,machine_ip,last_updated_time,status,branch_version,project_id,(select value from config_values where type='Team' and id=team_id),array_agg( distinct case when bit=0 then  type||' : '||name when bit!=0 then  type||' : '||name||' - '||bit||' Bit - '||version end ) from machine_dependency_settings mds,test_run_env tre,machine_project_map mpm where tre.id=mds.machine_serial and mpm.machine_serial=tre.id and status='Unassigned' group by tester_id,last_updated_time,status,branch_version,machine_ip,mpm.project_id,mpm.team_id"
    query="select distinct user_names from permitted_user_list pul where user_level='Manual'"
    Conn=GetConnection()
    machine_list=DB.GetData(Conn,query)
    Conn.close()        
    templ = get_template('RunTest_new.html')
    column=['Machine Name']
    #column=['Machine Name','Machine IP','Last Updated Time','Status','Version','Project ID','Team Name' ,'Dependency']
    variables = Context({'machine_list':machine_list,'dependency':column})
    output = templ.render(variables)
    return HttpResponse(output)
def edit_machine(request,machine_id):
    return render_to_response('EditMachine.html',{})
"""def Search(request):
    templ = get_template('SearchResults.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)"""

def make_array(get_list):
    refined_list = []
    for each in get_list:
        temp = []
        # print temp
        for eachitem in each:
            temp.append(eachitem)
        temp.pop()
        temp.insert(4, "status")
        temp = tuple(temp)
        refined_list.append(temp)
    print refined_list
    return refined_list        
def make_status_array(Conn, refined_list):
    pass_list = []
    for each in refined_list:
        #print each
        try:
            run_id = each[0]
            print "run id is: %s" %run_id
            temp = []
            total_query = "select count(*) from test_run where run_id='%s'" % run_id
            print "tota_query: %s" %total_query
            pass_query = "select count(*) from test_case_results where run_id='%s' and status='Passed'" % run_id
            print "pass_query: %s" %pass_query
            fail_query = "select count(*) from test_case_results where run_id='%s' and status='Failed'" % run_id
            print "fail_query: %s" %fail_query
            blocked_query = "select count(*) from test_case_results where run_id='%s' and status='Blocked'" % run_id
            print "blocked_query: %s" %blocked_query
            progress_query = "select count(*) from test_case_results where run_id='%s' and status='In-Progress'" % run_id
            print "progress_query: %s" %progress_query
            notrun_query = "select count(*) from test_case_results where run_id='%s' and status='Submitted'" % run_id
            print "notrun_query: %s" %notrun_query
            skipped_query = "select count(*) from test_case_results where run_id='%s' and status='Skipped'" % run_id
            print "skipped_query: %s" %skipped_query
            Conn=GetConnection()
            total = DB.GetData(Conn, total_query)
            #Conn.close()
            print "total: %s"%total
            for iTem in total:
                print iTem
            #Conn=GetConnection()
            passed = DB.GetData(Conn, pass_query)
            #Conn.close()
            print "passed: %s"%passed
            for iTem in passed:
                print iTem
            #Conn=GetConnection()
            failed = DB.GetData(Conn, fail_query)
            #Conn.close()
            print "failed: %s"%failed
            for iTem in failed:
                print iTem
            #Conn=GetConnection()
            blocked = DB.GetData(Conn, blocked_query)
            #Conn.close()
            print "blocked: %s"%blocked
            for iTem in blocked:
                print iTem
            #Conn=GetConnection()
            progress = DB.GetData(Conn, progress_query)
            #Conn.close()
            print "progress: %s"%progress
            for iTem in total:
                print iTem
            #Conn=GetConnection()
            submitted = DB.GetData(Conn, notrun_query)
            #Conn.close()
            print "submitted: %s"%submitted
            for iTem in progress:
                print iTem
            #Conn=GetConnection()
            skipped = DB.GetData(Conn, skipped_query)
            Conn.close()
            print "skipped: %s"%skipped
            for iTem in skipped:
                print iTem
        
            pass_percent = str((int(passed[0]) * 100 / int(total[0]))) + '%'
            fail = str((int(failed[0]) * 100 / int(total[0]))) + '%'
            block = str((int(blocked[0]) * 100 / int(total[0]))) + '%'
            progress = str((int(progress[0]) * 100 / int(total[0]))) + '%'
            submitted = str((int(submitted[0]) * 100 / int(total[0]))) + '%'
            pending = str((int(skipped[0]) * 100 / int(total[0]))) + '%'
            temp.append(pass_percent)
            temp.append(fail)
            temp.append(block)
            temp.append(progress)
            temp.append(submitted)
            temp.append(pending)
            temp = tuple(temp)
            pass_list.append(temp)
        except Exception, e:
            print "Exception %s" % e
    print pass_list
    return pass_list

def ResultTableFetch(index):
    
    # interval="1"
    try:
        step = 20
        limit = "limit " + str(step)
        ########Code for selecting offset#########
        index = int(index)
        index = index - 1
        index = index * step
        offset = "offset " + str(index)
        offset = offset.strip()
        total_query = "select * from ((select ter.run_id as run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(now()-ter.teststarttime,'HH24:MI:SS') as Duration,tre.product_version,tre.test_milestone,ter.teststarttime as starttime " 
        total_query += "from test_run_env tre, test_env_results ter " 
        total_query += "where tre.run_id=ter.run_id and ter.status=tre.status and ter.status in ('Submitted','In-Progress')) "
        total_query += "union all "
        total_query += "(select ter.run_id as run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(ter.testendtime-ter.teststarttime,'HH24:MI:SS') as Duration,tre.product_version,tre.test_milestone,ter.teststarttime as starttime " 
        total_query += "from test_run_env tre, test_env_results ter " 
        total_query += "where tre.run_id=ter.run_id and ter.status=tre.status and ter.status not in ('Submitted','In-Progress'))) as A order by starttime desc,run_id asc "
        count_query = total_query
        total_query += (limit + ' ' + offset)
        Conn = GetConnection()
        get_list = DB.GetData(Conn, total_query, False)
        #Conn.close()
        refine_list = []
        for each in get_list:
            if each not in refine_list:
                refine_list.append(each)
        total_run = make_array(refine_list)
        print total_run
        #Conn = GetConnection()
        all_status = make_status_array(Conn, total_run)
        #Conn.close()
        #time.sleep(0.5)
        #Conn = GetConnection()
        dataCount = DB.GetData(Conn, count_query, False)
        Conn.close()
        data = {
              'total':total_run,
              'all_status':all_status,
              'totalCount':len(dataCount),
              'start':index + 1,
              'end':index + step
              }
        return data
    except Exception, e:
        print "Exception %s" % e
def zipdata(data_array, status_array):
    data = []
    for each in zip(data_array, status_array):
        temp = []
        temp.append(each[0])
        temp.append(each[1])
        temp = tuple(temp)
        data.append(temp)
    return data

def GetPageCount(request):
    step = 20
    totalPage = 0
    if request.is_ajax():
        if request.method == 'GET':
            
            query = "select count(*) from test_run_env tre,test_env_results ter where tre.run_id=ter.run_id"
            Conn = GetConnection()
            totalEntry = DB.GetData(Conn, query)
            Conn.close()
            totalPage = totalEntry[0] / step
            if((totalEntry[0] % step) > 0):
                totalPage += 1
    result = simplejson.dumps(totalPage)
    return HttpResponse(result, mimetype='application/json')
def ResultPage(request, Page_No):
    print Page_No
    Page_No = str(Page_No)
    index = Page_No.split('-')[1].strip()
    print index
    data = ResultTableFetch(index)
    print data
    Column = ["Run ID", "Objective", "Run Type", "Tester", "Report", "Status", "Duration", "Version", "MileStone"]
    template = get_template('Result.html')
    all_data = zipdata(data['total'], data['all_status'])
    """complete_data=zipdata(data['complete'],data['complete_status'])
    progress_data=zipdata(data['progress'],data['progress_status'])
    cancelled_data=zipdata(data['cancelled'],data['cancelled_status'])
    submitted_data=zipdata(data['submitted'],data['submitted_status'])"""
    Dict = {
        'column':Column,
        'all':all_data,
        'start':data['start'],
        'end':data['end'],
        'total_count':data['totalCount']
        }
    variables = Context(Dict)
    output = template.render(variables)
    return HttpResponse(output)

def Result_Table(request):
    results = []
    if request.method == "GET":
        tester = request.GET.get(u'tester', '')
        status = request.GET.get(u'status', '')
        version = request.GET.get(u'version', '')
        run_type = request.GET.get(u'run_type', '')
        

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Search2(request, Run_Id):
    # RunId = request.GET.get('ClickedRunId', '')
    if Run_Id != "":
        return RunId_TestCases(request, Run_Id)
def ExceptionSearch(request):
        templ = get_template('SearchResults.html')
        variables = Context({'error_message':'You have not given a RunID' })
        output = templ.render(variables)
        return HttpResponse(output)

def Create(request):
    TC_Id = request.GET.get('TC_Id', '')
    if TC_Id != "":
        return ViewTestCase(TC_Id)
    else:
        templ = get_template('CreateTest.html')
        variables = Context({ })
        output = templ.render(variables)
        return HttpResponse(output)
    
def CreateNew(request):
    query="select label_id,label_name,Label_color from labels order by label_name"
    Conn=GetConnection()
    labels=DB.GetData(Conn,query,False)
    Conn.close()        
    templ = get_template('CreateTestCase.html')
    variables = Context({'labels':labels})
    output = templ.render(variables)
    return HttpResponse(output)
    """templ = get_template('CreateTestCase.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)"""

def CopyTestCase(request,tc_id):
    query="select label_id,label_name,Label_color from labels order by label_name"
    Conn=GetConnection()
    labels=DB.GetData(Conn,query,False)
    Conn.close()        
    templ = get_template('CreateTestCase.html')
    variables = Context({'labels':labels})
    output = templ.render(variables)
    return HttpResponse(output)
    """templ = get_template('CreateTestCase.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)"""
    
def ManageTestCases(request):
    templ = get_template('ManageTestCases.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

@csrf_protect
def DeleteExisting(request):
    """if request.method == 'GET':
        TC_Id = request.GET.get('TC_Id', '')
        print TC_Id
        if TC_Id != '':
            return DeleteExistingTestCase(TC_Id)
        else:
            t = get_template('DeleteExisting.html')
            c = Context({})
            c.update(csrf(request))
            output = t.render(c)
            return HttpResponse(output)
    elif request.method == 'POST':
        TC_Ids = request.POST.getlist('selectTC')
        if TC_Ids:
            return DeleteExistingTestCase(TC_Ids)
        else:
            data = GetData('test_cases')
            
            tc_ids = []
            tc_names = []
            counter = 0
            
            for row in data:
                tc_ids.append(row[0])
                tc_names.append(row[1])
                counter += 1
            
            t = get_template('DeleteMultiple.html')
            c = Context({'TC_ids': tc_ids, 'TC_names': tc_names})
            c.update(csrf(request))
            return HttpResponse(t.render(c))
    """
    return render_to_response('DeleteExisting.html', {})

def CreateProductSections(request):
    templ = get_template('CreateProductSections.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

@csrf_exempt
def ProductSectionsCreated(request):
    context = Context({ })
    if request.method == 'POST':
        sections = list()
        sections.append(request.POST['section_main'])
        sections.append(request.POST['subsection_1'])
        sections.append(request.POST['subsection_2'])
        sections.append(request.POST['subsection_3'])
        sections.append(request.POST['subsection_4'])
        sections_string = ''
        for i in range(len(sections) - 1):
            if sections[i].strip() != '':
                if sections_string != '':
                    sections_string += "."
                sections_string += sections[i]
        sections_string.strip()
        conn = GetConnection()
        if sections_string:
            DB.InsertNewRecordInToTable(conn, "product_sections", section_path=sections_string)
        print (sections_string)
        conn.close()
    return render(request, 'ProductSectionsCreated.html', context)

def SearchEdit(request):
    templ = get_template('SearchEdit.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def Edit(request,tc_id):
    TC_Id = request.GET.get('TC_Id', '')
    if TC_Id != "":
        return ViewTestCase(TC_Id)
    else:
        query="select label_id,label_name,Label_color from labels order by label_name"
        Conn=GetConnection()
        labels=DB.GetData(Conn,query,False)
        Conn.close()        
        templ = get_template('CreateTestCase.html')
        variables = Context({'labels':labels})
        output = templ.render(variables)
        return HttpResponse(output)
        """templ = get_template('CreateTestCase.html')
        variables = Context({ })
        output = templ.render(variables)
        return HttpResponse(output)"""
    
def EditMilestone(request,ms_id):
    ms_id = request.GET.get('ms_id', '')
    if ms_id != "":
        return render_to_response('Milestone.html')
    else:
        Conn=GetConnection()
        query="select project_id, project_name from projects"
        project_info=DB.GetData(Conn,query,False)
        query="select id,value from config_values where type='milestone'"
        milestone_info=DB.GetData(Conn,query,False)
        #get the current projects team info
        query="select distinct id,value from config_values where type='Team'"
        team_info=DB.GetData(Conn,query,False)
        #get the existing requirement id for parenting
        #query="select distinct requirement_id,requirement_title from requirements where project_id='%s' order by requirement_id"%project_id
        #requirement_list=DB.GetData(Conn,query,False)
        Dict={
              #'project_id':project_id,
              #'project_list':project_info,
              #'milestone_list':milestone_info,
              'team_info':team_info
              #'requirement_list':requirement_list
        }
        Conn.close()
        return render_to_response('Milestone.html',Dict)
        """templ = get_template('Milestone.html')
        variables = Context({ })
        output = templ.render(variables)
        return HttpResponse(output)"""
    
def EditBug(request,bug_id):
    bug_id = request.GET.get('bug_id', '')
    if bug_id != "":
        return render_to_response('CreateBug.html')
    else:
        query="select project_id from projects"
        Conn=GetConnection()
        project=DB.GetData(Conn,query)
        query="select distinct value from config_values where type='Team'"
        team=DB.GetData(Conn,query)
        query="select distinct user_names from permitted_user_list where user_level='manager'"
        manager=DB.GetData(Conn,query)
        query="select label_name, label_color, label_id from labels order by label_name"
        labels=DB.GetData(Conn,query,False)
        query="select distinct tc_id,tc_name from test_cases where tc_id not in (select id2 from components_map) order by tc_id"
        cases=DB.GetData(Conn,query,False)
        query="select id,value from config_values where type='milestone'"
        milestone_list=DB.GetData(Conn,query,False)
        Dict={'project':project,'team':team,'manager':manager,'labels':labels,'cases':cases,'milestone_list':milestone_list}
        Conn.close()
        return render_to_response('CreateBug.html',Dict)
        """templ = get_template('CreateBug.html')
        variables = Context({ })
        output = templ.render(variables)
        return HttpResponse(output)  """  

"""def ViewBug(bug_id):
    def returnResult(string):
        json = simplejson.dumps(string)
        return HttpResponse(json, mimetype='application/json')

    try:
        bug_id=bug_id.GET.get('bug_id')
        err_msg = ''
        # Search for TC_ID
        Conn = GetConnection()
        tmp_id = DB.GetData(Conn, "select bug_Id from bugs where bug_Id = '%s'" % bug_id)
        if len(tmp_id) > 0:
            # TestCaseOperations.LogMessage(sModuleInfo,"TEST CASE id is found:%s"%(TC_Id),4)

            # find all the details about test case
            Conn = GetConnection()
            query="select bug_id,bug_title,bug_description,cast(bug_startingdate as text),cast(bug_endingdate as text),mi.name,b.status from bugs b, milestone_info mi where b.bug_milestone::int=mi.id where bug_id='"+bug_id+"'"
            bug_details=DB.GetData(Conn, query, False)
            Conn.close()
            
                        # return values
            results = {'bug_details':bug_details}

            json = simplejson.dumps(results)
            return HttpResponse(json, mimetype='application/json')

        else:
            err_msg = "Bug is not found:%s" % (bug_id)
            return returnResult(err_msg)

    except Exception, e:
        err_msg = "Bug search failed due to exception: %s" % (bug_id)
        return returnResult(err_msg)"""


def Performance(request):
    templ = get_template('Performance.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

# def Performance_Details_NewWindow(request):
#    templ = get_template('Performance_Details_NewWindow.html')
#    variables = Context( { } )
#    output = templ.render(variables)
#    return HttpResponse(output)

# def PerformanceGraph_Window(request):
#    templ = get_template('PerformanceGraph_Window.html')
#    variables = Context( { } )
#    output = templ.render(variables)
#    return HttpResponse(output)


def Daily_Build(request):
    templ = get_template('DailyBuildResults.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def MKSReport(request):
    templ = get_template('MKS-Report.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def Analysis(request):                                          
    templ = get_template('Analysis.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def TestTypeStatus(request):
    templ = get_template('TestTypeStatus.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)



def MKS_Report_Table(request):

    Results = []
    TotalTime = ''



    Headings = ["Objective Name", "Seccion ID", "Test ID", "Test Case Name", "Status", "Annotation", "Related Items",
                 "Client OS", "Client Software", "Test Type"
                ]


    results = {'Headings':Headings, 'Result': Results, 'TotalTime':TotalTime }

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def AutoCompleteTestCasesSearch(request):  #==================Returns Data in List as user Type on Run Test Page==============================

    
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        Environment = request.GET.get(u'Env', '')
        if Environment == "Mac":
            Section = "MacSection"
            Test_Run_Type = "Mac_test_run_type"
            Priority = "MacPriority"
            TCStatusName = "MacStatus"
            CustomTag = "MacCustomTag"
            CustomSet = "set"
            Tag = 'tag'
            Client = 'client'
            Feature = 'feature'
        if Environment == "PC":
            Section = "Section"
            Test_Run_Type = "test_run_type"
            Priority = "Priority"
            TCStatusName = "Status"
            CustomTag = "CustomTag"
            CustomSet = "set"
            Tag = 'tag'
            Client = 'client'
            Feature = 'feature'
        
        Conn = GetConnection()
        results = DB.GetData(Conn, "select distinct name,property from test_case_tag "
                                   "where name Ilike '%" + value + "%' "
                                     "and property in('" + Section + "','" + Feature + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','" + CustomSet + "','" + Tag + "','" + Client + "') "
                                     "and tc_id in (select tc_id from test_case_tag where name = '" + Environment + "' and property = 'machine_os' ) ", False
                                     )

        
        status_result = DB.GetData(Conn, "select distinct property,name from test_case_tag "
                                   "where property Ilike '%" + value + "%' "
                                     "and name ='" + TCStatusName + "'"
                                     "and tc_id in (select tc_id from test_case_tag where name = '" + Environment + "' and property = 'machine_os' ) ", False
                                     , False)
        tcidresults = DB.GetData(Conn, "select distinct name || ' - ' || tc_name,'Test Case' from test_case_tag tct,test_cases tc "
                                   "where tct.tc_id = tc.tc_id and (tct.tc_id Ilike '%" + value + "%' or tc.tc_name Ilike '%" + value + "%')"
                                     "and property in('tcid') "
                                     "and tct.tc_id in (select tc_id from test_case_tag where name = '" + Environment + "' and property = 'machine_os' ) ", False
                                     )

        results = list(set(results + tcidresults + status_result))

        # if len(results) > 0:
        #   results.append(("*Dev","Status"))

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
def AutoCompleteTestCasesSearchOtherPages(request):  #===============Returns Available Test Case in other page without the platform =========================#
    if request.is_ajax():
        if request.method == 'GET':
            value = request.GET.get(u'term', '')
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team_id','')
            print project_id
            print team_id
            Section_Tag = 'Section'
            Feature_Tag='Feature'
            Custom_Tag = 'CustomTag'
            Section_Path_Tag = 'section_id'
            Feature_Path_Tag = 'feature_id'
            Priority_Tag = 'Priority'
            Status='Status'
            set_type='set'
            tag_type='tag'
            query="select distinct dependency_name from dependency d, dependency_management dm where d.id=dm.dependency and dm.project_id='%s' and dm.team_id=%d"%(project_id,int(team_id))
            Conn=GetConnection()
            dependency=DB.GetData(Conn,query)
            Conn.close()
            wherequery=""
            for each in dependency:
                wherequery+=("'"+each.strip()+"'")
                wherequery+=','
            wherequery+=("'"+Feature_Tag+"','"+Section_Tag+"','"+Custom_Tag+"','"+Section_Path_Tag+"','"+Feature_Path_Tag+"','"+Priority_Tag+"','"+Status+"','"+set_type+"','"+tag_type+"'")
            print wherequery
            tag_query="select distinct name,property from test_case_tag where name Ilike '%%%s%%' and property in(%s)"%(value,wherequery)
            id_query="select distinct name || ' - ' || tc_name,'Test Case' from test_case_tag tct,test_cases tc where tct.tc_id = tc.tc_id and (tct.tc_id Ilike '%%%s%%' or tc.tc_name Ilike '%%%s%%') and property in('tcid')"%(value,value)
            Conn=GetConnection()
            tag_cases=DB.GetData(Conn,tag_query,False)
            id_cases=DB.GetData(Conn,id_query,False)
            results=list(set(list(tag_cases+id_cases)))            
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteUsersSearch(request):  #==================Returns Abailable User Name in List as user Type on Run Test Page==============================
    
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == "GET":
            value = request.GET.get(u'term', '')
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team_id','')
            print value
            Usable_Machine = []
            query = "select distinct tre.tester_id,pul.user_level from test_run_env tre,permitted_user_list pul,machine_project_map mpm where tre.tester_id Ilike '%%%s%%' and tre.tester_id=pul.user_names and mpm.machine_serial=tre.id and tre.status='Unassigned' and pul.user_level in('Automation') and mpm.project_id='%s' and mpm.team_id=%d"%(value,project_id,int(team_id)) 
            Conn=GetConnection()
            Automation_Machine = DB.GetData(Conn, query, False)
            Conn.close()
            for each in Automation_Machine:
                Usable_Machine.append(each)
            query = "select distinct tre.tester_id,pul.user_level from test_run_env tre,permitted_user_list pul,machine_project_map mpm where tre.tester_id Ilike '%%%s%%' and tre.tester_id=pul.user_names and mpm.machine_serial=tre.id and tre.status='Unassigned' and pul.user_level in('Manual') and mpm.project_id='%s' and mpm.team_id=%d"%(value,project_id,int(team_id))
            Conn=GetConnection()
            Manual_Machine = DB.GetData(Conn, query, False)
            Conn.close()
            for each in Manual_Machine:
                query = "select distinct status from test_run_env tre,machine_project_map mpm where tester_id='%s' and tre.id=mpm.machine_serial"% (each[0].strip())
                Conn=GetConnection()
                machine_status = DB.GetData(Conn, query)
                Conn.close()
                if len(machine_status) == 0:
                    continue
                else:
                    if 'In-Progress' in machine_status or 'Submitted' in machine_status:
                        continue
                    else:
                        Usable_Machine.append(each)
            
    json = simplejson.dumps(Usable_Machine)
    return HttpResponse(json, mimetype='application/json')


def AutoCompleteEmailSearch(request):  #==================Returns Abailable Emails in List as user Type on Select Email Input Box on Run Test Page==============================

    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        # Ignore queries shorter than length 3
        # if len(value) > 1:
        results = DB.GetData(Conn, "Select  DISTINCT user_names from permitted_user_list where user_names Ilike '%" + value + "%' and user_level = 'email'")
    Conn.close()
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteTag(request):
    if request.is_ajax():
        if request.method == 'GET':
            value = request.GET.get(u'term', '')
            print value
            Conn = GetConnection()
            query = "select value,type from config_values where value Ilike '%%%s%%' and type='tag'" % value
            tag_list = DB.GetData(Conn, query, False)
            Conn.close()
    json = simplejson.dumps(tag_list)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteLabel(request):
    if request.is_ajax():
        if request.method == 'GET':
            value = request.GET.get(u'term', '')
            print value
            Conn = GetConnection()
            query = "select * from labels where label_name Ilike '%%%s%%' or label_id Ilike '%%%s%%'" % (value, value)
            label_list = DB.GetData(Conn, query, False)
            Conn.close()
    json = simplejson.dumps(label_list)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteTask(request):
    if request.is_ajax():
        if request.method == 'GET':
            value = request.GET.get(u'term', '')
            project_id = request.GET.get(u'project_id','')
            team_id = request.GET.get(u'team_id','')
            print value
            Conn = GetConnection()
            query = "select distinct tasks_id,tasks_title,tasks_description ,cast(tasks_startingdate as text),cast(tasks_endingdate as text),mi.name,t.status from tasks t, milestone_info mi where mi.id::text=t.tasks_milestone and (tasks_title Ilike '%%%s%%' or tasks_id Ilike '%%%s%%') and t.project_id='%s' and t.team_id='%s'" % (value, value, project_id,team_id)
            task_list = DB.GetData(Conn, query, False)
            Conn.close()
    json = simplejson.dumps(task_list)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteRequirements(request):
    if request.is_ajax():
        if request.method == 'GET':
            value = request.GET.get(u'term', '')
            project_id = request.GET.get(u'project_id','')
            team_id = request.GET.get(u'team_id','')
            
            Conn = GetConnection()
            query = "select distinct r.requirement_id,r.requirement_title,r.status,mi.name from requirements r, milestone_info mi,requirement_team_map rtm where r.requirement_milestone=mi.id::text and r.project_id='%s' and (r.requirement_title Ilike '%%%s%%' or r.requirement_id Ilike '%%%s%%') and rtm.team_id='%s' and r.requirement_id=rtm.requirement_id" % (project_id, value, value,team_id)
            req_list = DB.GetData(Conn, query, False)
            Conn.close()
    json = simplejson.dumps(req_list)
    return HttpResponse(json, mimetype='application/json')
 
def AutoCompleteTesterSearch(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            value = request.GET.get(u'term', '')
            results = DB.GetData(Conn, "Select DISTINCT user_names,user_id from permitted_user_list where user_names Ilike '%" + value + "%' and user_level = 'assigned_tester'")
    Conn.close()
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteTagSearch(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        Environment = request.GET.get(u'Env', '')
        if Environment == "Mac":
            Section = "MacSection"
            CustomTag = "MacCustomTag"

        if Environment == "PC":
            Section = "Section"
            CustomTag = "CustomTag"


        # results = DB.GetData(Conn, "select distinct name,property from test_case_tag where name Ilike '%" + value + "%' "
        #                           + "and property in ('" + CustomTag + "') order by name",False)

        query = "select distinct value,type from config_values where type='tag' order by value"
        mastertags = DB.GetData(Conn, query, False)
        
        # results = list(set(results + mastertags))
    Conn.close()
    json = simplejson.dumps(mastertags)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteTestStepSearch(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')

        results = DB.GetData(Conn, "select stepname,data_required,steptype,description,step_editable,case_desc,expected,verify_point,estd_time from test_steps_list where stepname Ilike '%" + value + "%' order by stepname", False)

    json = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(json, mimetype='application/json')


def Table_Data_TestCases(request):  #==================Returns Test Cases When User Send Query List From Run Page===============================
    Conn = GetConnection()
    propertyValue = "Ready"
    tabledata = []
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Query', '')
            UserText = UserData.split(":");
            Environment = request.GET.get(u'Env', '')
            if Environment == "Mac":
                Section = "MacSection"
                Test_Run_Type = "Mac_test_run_type"
                Priority = "MacPriority"
                TCStatusName = "MacStatus"
                CustomTag = "MacCustomTag"
                CustomSet = "set"
                Tag = 'tag'
                Client = 'client'
                Feature = 'feature'
            if Environment == "PC":
                Section = "Section"
                Test_Run_Type = "test_run_type"
                Priority = "Priority"
                TCStatusName = "Status"
                CustomTag = "CustomTag"
                CustomSet = "set"
                Tag = 'tag'
                Client = 'client'
                Feature = 'feature'
            QueryText = []
            for eachitem in UserText:
                if len(eachitem) != 0 and  len(eachitem) != 1:
                    QueryText.append(eachitem.strip())

    if "Dev" in QueryText:
        QueryText.remove("Dev")
        propertyValue = "Dev"


    # In case if user search test cases using test case ids    
    TestIDList = []
    for eachitem in QueryText:
        TestID = DB.GetData(Conn, "Select property from test_case_tag where name = '%s' " % eachitem)
        for eachProp in TestID:
            if eachProp == 'tcid':
                TestIDList.append(eachitem)
                break


    RefinedData = []
    TableData = []
    if len(TestIDList) > 0:
        for eachitem in TestIDList:
            tabledata = DB.GetData(Conn, "select distinct tc_id,tc_name from test_cases "
                        "where tc_id = '%s'" % eachitem, False)
            TableData.append(tabledata[0])


    elif len(QueryText) > 0:
        count = 1
        for eachitem in QueryText:
            if count == 1:
                #if eachitem in ('Dev', 'Ready','Forced'):
                #   Query = "HAVING COUNT(CASE WHEN property = '" + eachitem + "' and name='" + TCStatusName + "'  THEN 1 END) > 0 "
                #else:
                Query = "HAVING COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + Feature + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','" + CustomSet + "','" + Tag + "','" + Client + "') THEN 1 END) > 0 "
                count = count + 1
            elif count >= 2:
                #if eachitem in ('Dev', 'Ready','Forced'):
                #   Query = Query + "AND COUNT(CASE WHEN property = '" + eachitem + "' and name='" + TCStatusName + "'  THEN 1 END) > 0 "
                #else:
                Query = Query + "AND COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + Feature + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','" + CustomSet + "','" + Tag + "','" + Client + "') THEN 1 END) > 0 "
        Query = Query + " AND COUNT(CASE WHEN name = '%s' and property = '%s' THEN 1 END) > 0 " % (TCStatusName, propertyValue)
        Query = Query + " AND COUNT(CASE WHEN property = 'machine_os' and name = '" + Environment + "' THEN 1 END) > 0"
        query = "select distinct tct.tc_id,tc.tc_name from test_case_tag tct,test_cases tc where tct.tc_id=tc.tc_id group by tct.tc_id,tc.tc_name " + Query
        TableData = DB.GetData(Conn, query, False)
    TempTableData = []
    Check_TestCase(TableData, RefinedData)
    final = []
    for each in RefinedData:
        if DB.IsDBConnectionGood(Conn) == False:
            time.sleep(1)
            Conn = GetConnection()
        query = "select property from test_case_tag where tc_id='%s' and name='Status'" % each[0].strip()
        temp = []
        for eachitem in each:
            temp.append(eachitem)
        test_case_status = DB.GetData(Conn, query)
        if len(test_case_status) == 0:
            status = ""
        else: 
            status = test_case_status[0]
        temp.append(status)
        temp = tuple(temp)
        final.append(temp)
    RefinedData = final
    for each in RefinedData:
        temp = []
        for eachitem in each:
            temp.append(eachitem)
        query = "select name from test_case_tag where tc_id='%s' and property='machine_os'" % each[0]
        platform = DB.GetData(Conn, query)
        temp.append(platform[0])
        temp = tuple(temp)
        TempTableData.append(temp)
    RefinedData = TempTableData
    totalRunIDTime = 0
    test_case_time = []
    for each in RefinedData:
        temp_tc_id = each[0]
        temp_tc_time = 0
        step_count = DB.GetData(Conn, "select count(*) from test_steps where tc_id='%s'" % temp_tc_id)
        for eachstep in range(1, step_count[0] + 1):
            temp_id = temp_tc_id + '_s' + str(eachstep)
            query = "select description from master_data where field='estimated' and value='time' and id='%s'" % temp_id
            step_time = DB.GetData(Conn, query)
            temp_tc_time += int(step_time[0])
            totalRunIDTime += int(step_time[0])
        tempFormat = ConvertTime(temp_tc_time)
        test_case_time.append(tempFormat)
    formatTime = ConvertTime(totalRunIDTime)
    data_temp = []
    for eachitem in zip(RefinedData, test_case_time):
        temp = []
        for eachelement in eachitem[0]:
            temp.append(eachelement)
        temp.append(eachitem[1])
        temp = tuple(temp)
        data_temp.append(temp)
    RefinedData = data_temp
    Heading = ['Test Case ID', 'Test Case Name', 'Test Case Type', 'Status', 'Platform', 'Time Required']

    # results = {"Section":Section, "TestType":Test_Run_Type,"Priority":Priority}         
    results = {'Heading':Heading, 'TableData':RefinedData, 'TimeEstimated':formatTime}

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Table_Data_TestResult(request):  #==================Returns Test Results When User Launch Test Result Page===============================
    Conn = GetConnection()
    tabledata = []
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'ResultRequest', '')

        if UserData == "Show All":
            limit = ""
            InProgress_Interval = 7
        else:
            limit = "limit 20"
            InProgress_Interval = 1

#        TotalRecord = DB.GetData(Conn,"Select COUNT(*) from test_env_results")

        tabledata = DB.GetData(Conn, "(Select te.run_id,"
                                     "te.test_objective, "
                                    "te.tester_id,"
                                    "tr.status,"
                                    "to_char(now() - tr.teststarttime,'HH24:MI:SS'), "
                                    "te.product_version,"
                                    "te.os_name||' '||te.os_version||' - '||te.os_bit as machine_os,"
                                    "te.machine_ip, "
                                    "te.client "
                                    "from test_env_results tr, test_run_env te where tr.run_id = te.run_id and (tr.status = 'In-Progress' or tr.status = 'Submitted')  and (cast (now() AS timestamp without time zone)-teststarttime ) < interval '%s day' ORDER BY tr.teststarttime DESC)"
                                    " union all "
                                    "(Select te.run_id,"
                                    "te.test_objective, "
                                    "te.tester_id,"
                                    "tr.status,"
                                    "to_char(tr.duration,'HH24:MI:SS'), "
                                    "te.product_version,"
                                    "te.os_name||' '||te.os_version||' - '||te.os_bit as machine_os,"
                                    "te.machine_ip, "
                                    "te.client "
                                    "from test_env_results tr, test_run_env te where tr.run_id = te.run_id and tr.status != 'In-Progress' ORDER BY tr.teststarttime DESC %s)" % (InProgress_Interval, limit)

                                     , False)



        Col = ['Run ID',
                   'Test Objective',
                   'Tester ID',
                   'Status',
                    'Duration',
                    'Product Version',
                    'Machine OS',
                    'Machine IP',
                    'Client'
                    ]

        Results = []
        Count = 0
        Col.insert(3, "Passed/Failed By Rate")
        Col.insert(4, "Passed/Failed By Count")
        Col.insert(5, "Completed/Total")

        for eachitem in tabledata:
                mylist = list(eachitem)
                TotalTestCase = DB.GetData(Conn, "Select count(*) as TotalTests from test_run_env te, test_run tr where te.run_id = '%s' and te.run_id = tr.run_id" % eachitem[0])
                TotalRun = DB.GetData(Conn, "Select count(*) as TotalRun from test_case_results where run_id = '%s' and status in ('Passed', 'Failed')" % eachitem[0])
                Passed = DB.GetData(Conn, "Select count(*) as Passed from test_case_results where run_id = '%s' and status = 'Passed'" % eachitem[0])
                Failed = DB.GetData(Conn, "Select count(*) as Passed from test_case_results where run_id = '%s' and status = 'Failed'" % eachitem[0])

                if TotalRun[0] == 0:
                    PassedPercentage = 0
                    FailedPercentage = 0
                else:
                    PassedPercentage = (1.0 * Passed[0] / TotalRun[0]) * 100
                    FailedPercentage = (1.0 * Failed[0] / TotalRun[0]) * 100
                mylist.insert(3, "%0.0f" % (PassedPercentage) + "%" + " / " + "%0.0f" % (FailedPercentage) + "%")
                mylist.insert(4, str(Passed[0]) + "/" + str(Failed[0]))
                mylist.insert(5, (str(TotalRun[0]) + "/" + str(TotalTestCase[0])))


                Results.insert(Count, mylist)
                Count = Count + 1

    results = {'Heading':Col, 'TableData':Results}

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def Table_Data_DailyBuild(request):
    import datetime
    Conn = GetConnection()
    results = {}
    tabledata = []
    if request.method == 'GET':
        Branch = request.GET.get(u'Branch', '')
    tabledata = DB.GetData(Conn, "select daily_build_user, "
                                "status,"
                                "date_part('hours',last_checked_time) || ':' || date_part('minutes',last_checked_time) || ':' || round ( date_part('seconds',last_checked_time) )  as last_checked, "
                                "bundle,machine_os, "
                                "local_ip "
                                "from daily_build_status where branch = '%s' ORDER BY last_checked_time DESC" % Branch, False
                                )


    Col = ['Daily Build User',
               'Status',
               'TimeStamp',
                'Product Bundle',
                'Machine OS',
                'Machine IP'
                ]

    Duration = ''
    CurrentStatus = ''
    SinceLastRun = ''
    SinceLastRunBundle = 'Not Yet'
    SinceLastBuild = ''
    SinceLastBuildBundle = ''

    if len(tabledata) > 0:
        DurationTime = DB.GetData(Conn, "select last_checked_time from daily_build_status where branch = '%s' ORDER BY last_checked_time DESC" % Branch, False)
        Duration = datetime.datetime.now() - DurationTime[0][0]
        Duration = str(Duration).split('.')[0]
        Duration = str(Duration)
        CurrentStatus = DB.GetData(Conn, "select status from daily_build_status where branch = '%s' ORDER BY last_checked_time DESC" % Branch, False)
        CurrentStatus = CurrentStatus[0][0]

        StatusData = DB.GetData(Conn, "Select status, last_checked_time, bundle from daily_build_status where branch = '%s' ORDER BY last_checked_time DESC" % Branch, False)

        for eachitem in  StatusData:
            if eachitem[0] == "SI successful":
                SinceLastRun = datetime.datetime.now() - eachitem[1]
                SinceLastRun = str(SinceLastRun).split('.')[0]
                SinceLastRunBundle = str(eachitem[2])
            if eachitem[0] == "Latest build installed locally":
                SinceLastBuild = datetime.datetime.now() - eachitem[1]
                SinceLastBuild = str(SinceLastBuild).split('.')[0]
                SinceLastBuildBundle = str(eachitem[2])

    results = {'Heading':Col, 'TableData':tabledata,
               'CurrentStatus':CurrentStatus, 'DurationTime':Duration,
               'SinceLastBuild':SinceLastBuild,
               'SinceLastRunBundle':SinceLastRunBundle,
               'SinceLastRun':SinceLastRun,
               'SinceLastBuildBundle':SinceLastBuildBundle
               }

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def TestCase_TestSteps(request):  #==================Returns Test Steps When User Click on Test Case on Test Run Page===============================
    Conn = GetConnection()
    results = {}
    if request.is_ajax():
         if request.method == 'GET':

            # If User Click on Test Case ID 
            TestCaseName = request.GET.get('ClickedTC', '')
            RunID = request.GET.get('RunID', '')
            TC_NameID = DB.GetData(Conn, "select  tc.tc_name, tr.tc_id from test_run tr, test_cases tc where tr.tc_id = tc.tc_id and tr.run_id = '%s'" % RunID, False)

            for eachitem in TC_NameID:
                if TestCaseName in eachitem:
                    TC_ID = eachitem[1]

            if TC_ID != '':
                Result = DB.GetData(Conn, "Select stepname from test_steps tst,test_steps_list tsl where tst.step_id = tsl.step_id and tc_id  = '%s' order by teststepsequence" % TC_ID)

    results = {'Result':Result

               }
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestCase_TestSteps_SearchPage(request):  #==================Returns Test Steps When User Click on Test Case on Test Search Page===============================
    Conn = GetConnection()
    results = {}
    if request.is_ajax():
         if request.method == 'GET':

            # If User Click on Test Case ID 
            TestCaseName = request.GET.get('ClickedTC', '')
            RunID = request.GET.get('RunID', '')
            print RunID
            RunID = str(RunID.strip())
            RunID = str(RunID.replace(u'\xa0', u''))
#            TC_NameID = DB.GetData(Conn,"select  tc.tc_name, tr.tc_id from test_run tr, test_cases tc where tr.tc_id = tc.tc_id and tr.run_id = '%s'" %RunID,False)
#
#            for eachitem in TC_NameID:
#                if TestCaseName in eachitem:
#                    TC_ID = eachitem[1]
            result = []
            if RunID != '':
                Result = DB.GetData(Conn, "Select stepname from test_steps tst,test_steps_list tsl where tst.step_id = tsl.step_id and tc_id  = '%s' order by teststepsequence" % RunID)
            for each in Result:
                query = "select '" + each + "-'||steptype from test_steps_list where stepname='" + each + "'"
                Result_type = DB.GetData(Conn, query)
                result.append(Result_type[0])
    results = {'Result':result}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
def GetRunIDStatus(RunId):
    run_status = ""
    query = "select status from test_case_results where run_id='%s'" % RunId
    Conn = GetConnection()
    status_list = DB.GetData(Conn, query)
    for each in status_list:
        if each != 'Submitted':
            run_status = 'Not Submitted'
            break
    if run_status == 'Not Submitted':
        if 'In-Progress' in status_list:
            run_status = 'In-Progress'
        elif 'Submitted' in status_list:
            run_status = 'In-Progress'
        else:
            run_status = 'Complete'
    else:
        run_status = 'Submitted'
    return run_status
def Modify(AllTestCases1):
        AllTestCases = []
        AllTestCases2 = []
        Check_TestCase(AllTestCases1, AllTestCases2)
        for each in zip(AllTestCases1, AllTestCases2):
            temp = []
            for eachitem in each[0]:
                temp.append(eachitem)
            temp.insert(2, each[1][2])
            temp = tuple(temp)
            AllTestCases.append(temp)
        return AllTestCases
def ConvertTime(total_time):
    seconds = total_time % 60
    minuates = total_time / 60
    minuate = minuates % 60
    hour = minuates / 60
    if seconds < 10:
        seconds = ('0' + str(seconds))
    else:
        seconds = str(seconds)
    if minuate < 10:
        minuate = ('0' + str(minuate))
    else:
        minuate = str(minuate)
    if hour < 10:
        hour = ('0' + str(hour))
    else:
        hour = str(hour)
    timeformat = hour + ':' + minuate + ':' + seconds
    timeformat = timeformat.strip()
    return timeformat
def AddEstimatedTime(TestCaseList, run_id):
    ModifiedTestCaseList = []
    for each in TestCaseList:
        print each[0]
        query = "select count(*) from result_test_steps where tc_id='%s' and run_id='%s'" % (each[0], run_id)
        Conn = GetConnection()
        step_count = DB.GetData(Conn, query)
        total_time = 0
        for eachstep in range(1, step_count[0] + 1):
            step_id = each[0] + '_s' + str(eachstep)
            time_query = "select description from result_master_data where field='estimated' and value='time' and id='%s' and run_id='%s'" % (step_id, run_id)
            step_time = DB.GetData(Conn, time_query)
            total_time += int(step_time[0])
        format_time = ConvertTime(total_time)
        temp = []
        for eachitem in each:
            temp.append(eachitem)
        temp.insert(5, format_time)
        temp = tuple(temp)
        ModifiedTestCaseList.append(temp)
    return ModifiedTestCaseList
def RunId_TestCases(request, RunId):  #==================Returns Test Cases When User Click on Run ID On Test Result Page===============================
    RunId = RunId.strip()
    print RunId
    Env_Details_Col = ["Run ID", "Mahchine", "Tester", "Estd. Time", "Status", "Version","Dependency", "Machine IP", "Objective", "MileStone" ,"Email","Project","Team"]
    run_id_status = GetRunIDStatus(RunId)
    query = "Select DISTINCT run_id,tester_id,assigned_tester,'%s',branch_version,array_agg( distinct case when bit=0 then type||' : '||name when bit!=0 then  type||' : '||name||' - '||bit||' - '||version end ),machine_ip,test_objective,test_milestone from test_run_env tre,machine_dependency_settings mds Where tre.id=mds.machine_serial and run_id = '%s' group by run_id,tester_id,assigned_tester,branch_version,machine_ip,test_objective,test_milestone" % (run_id_status,RunId)
    Conn=GetConnection()
    Env_Details_Data = DB.GetData(Conn, query, False)
    Conn.close()
    # Code for the total estimated time for the RUNID
    totalRunIDTime = 0
    query = "select tc_id from test_run where run_id='%s'" % RunId
    Conn=GetConnection()
    test_case_list = DB.GetData(Conn, query)
    Conn.close()
    for each in test_case_list:
        # Get the step_count
        query = "select count(*) from result_test_steps where tc_id='%s' and run_id='%s'" % (each, RunId)
        Conn=GetConnection()
        step_count = DB.GetData(Conn, query)
        Conn.close()
        count = step_count[0]
        count = int(count)
        for eachstep in range(1, count + 1):
            temp_id = each + '_s' + str(eachstep)
            query = "select description from result_master_data where field='estimated' and value='time' and id='%s' and run_id='%s'" % (temp_id, RunId)
            Conn=GetConnection()
            step_time = DB.GetData(Conn, query)
            Conn.close()
            totalRunIDTime += int(step_time[0])
    formatTime = ConvertTime(totalRunIDTime) 
    ################################################
    # code for fetching email notification
    email_query = "select email_notification from test_run_env where run_id='%s'" % RunId
    Conn=GetConnection()
    email_list = DB.GetData(Conn, email_query, False)
    Conn.close()
    print email_list
    emails = email_list[0][0]
    email_list = emails.split(",")
    email_list = list(set(email_list))
    print email_list
    email_receiver = []
    for each in email_list:
        if each != "":
            query = "select user_names from permitted_user_list where user_level='email' and email='%s'" % each
            Conn=GetConnection()
            name = DB.GetData(Conn, query)
            Conn.close()
            email_receiver.append(name[0])
    print email_receiver
    email_name = ",".join(email_receiver)
    query="select p.project_id||' - '||p.project_name from projects p, test_run_env tre,machine_project_map mpm where mpm.machine_serial=tre.id and p.project_id=mpm.project_id and tre.run_id='%s'"%RunId
    Conn=GetConnection()
    project_name=DB.GetData(Conn,query,False)
    Conn.close()
    query="select value from config_values c,test_run_env tre,machine_project_map mpm where mpm.machine_serial=tre.id and  c.id=mpm.team_id and c.type='Team' and tre.run_id='%s'"%RunId
    Conn=GetConnection()
    team_name=DB.GetData(Conn,query,False)
    Conn.close()
    temp = []
    for each in Env_Details_Data[0]:
        temp.append(each)
    temp.insert(3, formatTime)
    temp.append(email_name)
    temp.append(project_name[0][0])
    temp.append(team_name[0][0])
    temp = tuple(temp)
    Env_Details_Data = []
    Env_Details_Data.append(temp)
    print Env_Details_Data
    #####################################
    ReRunColumn = ['Test Case ID', 'Test Case Name', 'Type', 'Status']
    query = "select tc.tc_id,tc.tc_name,tcr.status from result_test_cases tc,test_case_results tcr where tc.run_id=tcr.run_id and tc.tc_id=tcr.tc_id and tcr.run_id='%s'" % RunId
    Conn=GetConnection()
    ReRunList = DB.GetData(Conn, query, False)
    Conn.close()
    ReRun = Modify(ReRunList)
    results = {
             'Env_Details_Col':Env_Details_Col,
             'Env_Details_Data':Env_Details_Data,
             'Env_length':len(Env_Details_Data),
             'rerun_col':ReRunColumn,
             'rerun_list':ReRun
             }
    return render(request, 'RunID_Detail.html', results)

def TestCase_Detail_Table(request):  #==================Returns Test Steps and Details Table When User Click on Test Case Name On Test Result Page========
    Conn = GetConnection()
    results = {}
    TC_ID = ""
    TestCase_Detail_Data = []
    TestCase_Detail_Col = []
    if request.is_ajax():
        if request.method == 'GET':
            # If User Click on Fail Step 
            RunId = request.GET.get('RunID', '')
            TestCaseName = request.GET.get('TestCaseName', '')
            TestCaseName = str(TestCaseName.strip())
            TC_ID = TestCaseName

            # TC_NameID = DB.GetData(Conn,"select  tc.tc_name, tr.tc_id from test_run tr, test_cases tc where tr.tc_id = tc.tc_id and tr.run_id = '%s'" %RunId,False)

            # for eachitem in TC_NameID:
            #    if TestCaseName in eachitem:
            #        TC_ID = eachitem[1]

            if RunId != '' and TC_ID != '':
                RunId = str(RunId.strip())


                """TestCase_Detail_Data = DB.GetData(Conn, "(select "
                                                   " tl.stepname as stepname,"
                                                   " tr.status as status,"
                                                   " to_char(tr.duration,'HH24:MI:SS') as duration,"
                                                   " tr.memory_consumed as memory"
                                                   " from  test_step_results tr, test_cases tc, test_steps_list tl  "
                                                   " where tr.run_id = '%s' and tc.tc_id = '%s'"
                                                   " and tc.tc_id = tr.tc_id and tr.teststep_id = tl.step_id"
                                                   " ORDER BY tr.stepstarttime ASC)"
                                                   "union all"
                                                   "(select stepname as stepname,'Skipped' as status,'' as duration,'' as memory "
                                                   "from test_steps ts, test_steps_list tl "
                                                   "where ts.tc_id = '%s' and ts.step_id = tl.step_id and ts.teststepsequence > (select max(teststepsequence) "
                                                   " from test_step_results tr where tr.run_id = '%s' and tr.tc_id = '%s') "
                                                   "order by ts.teststepsequence)" % (RunId, TC_ID, TC_ID, RunId, TC_ID), False)
"""
#                DB.GetData(Conn,"Select    "
#                                                        "tl.stepname,"
#                                                        " tr.status, "
#                                                        "to_char(tr.duration,'HH24:MI:SS'), "
#                                                        " tr.memory_consumed " 
#                                   "from  test_step_results tr, test_cases tc, test_steps_list tl  where tr.run_id = '%s' and tc.tc_id = '%s' " 
#                                   "and tc.tc_id = tr.tc_id and tr.teststep_id = tl.step_id " 
#                                   "ORDER BY tr.stepstarttime ASC" % (RunId, TC_ID),False
#                              )
                query = "select tsl.stepname, tsr.status,to_char(tsr.duration,'HH24:MI:SS') as duration,tsr.memory_consumed as MemoryUsage from test_step_results tsr,result_test_steps_list tsl where tsr.teststep_id=tsl.step_id and tsr.run_id=tsl.run_id and tsr.run_id='%s' and tsr.tc_id='%s' order by tsr.id" % (RunId, TC_ID)
                TestCase_Detail_Data = DB.GetData(Conn, query, False)
                TestCase_Detail_Col = ['Test Step Name', 'Status', 'Duration', 'Memory Usage']

    results = {
               'TestCase_Detail_Data':TestCase_Detail_Data,
               'TestCase_Detail_Col' :TestCase_Detail_Col,
               }
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def TestStep_Detail_Table(request):  #==================Returns Test Step Details Table When User Click on Test Step Name On Test Result Page=======
    Conn = GetConnection()
    results = {}
    TestStep_Details = ""
    TestStep_Col = ""
    TestStep_Description_Col = ""
    TestStep_Description = ""
    data_col = ""
    data_val = ""
    data_val_comp = ""
    dataset = ""
    data_required = ""
    if request.is_ajax():
        if request.method == 'GET':

            # If User Click on Fail Step 
            RunId = request.GET.get('RunID', '')
            TestCaseName = request.GET.get('TestCaseName', '')
            TestStepName = request.GET.get('TestStepName', '')
            TestStepSeqId = request.GET.get('TestStepSeqID', '')

            if RunId != '' and TestCaseName != '' and TestStepName != '' and TestStepSeqId != '':
                RunId = str(RunId.strip())
                TestCaseName = str(TestCaseName.strip())
                TestStepName = str(TestStepName.strip())
                TestStepSeqId = int(TestStepSeqId.strip())
                StepSequence = str(TestStepSeqId)
                query = "select tc_id from test_cases where tc_name='" + TestCaseName + "'"
                TestCaseId = DB.GetData(Conn, query)
                TestCaseId = str(TestCaseId[0])
                TestStep_Details = []
                StepSeqId = DB.GetData(Conn, "Select tst.teststepsequence "
                                            " from test_steps tst,test_steps_list tsl "
                                            " where tc_id = '%s' and "
                                            "tst.step_id = tsl.step_id and "
                                            "tsl.stepname='%s'" % (TestCaseId, TestStepName)
                                        )
                TestStepSeqId = str(StepSeqId[0])
                TestStep_Details = DB.GetData(Conn, "Select  el.status, el.modulename, el.details "
                                        "from test_step_results tsr, execution_log el "
                                        "where run_id = '%s' and "
                                        "tc_id = '%s' and teststepsequence = '%s' and tsr.logid = el.logid"
                                        % (RunId, TestCaseId, TestStepSeqId), False
                                    )
#                for each in TestStep_Details:
#                    if str(list(each)).find("(") != -1:
#                        TestStep_Details.remove(each)

                TestStep_Col = ['Log Status', 'Module Name', 'Execution Log']
                TestStep_Description_Col = ['StepSequence', 'Description', 'Purpose']
                TestStep_Description = []
                TestStep_Description.append(StepSequence)
                query = "select description,data_required from test_steps_list where stepname='" + TestStepName + "'"
                step_desc = DB.GetData(Conn, query, False)
                TestStep_Description.append(step_desc[0][0])
                query = "select tc_id from test_cases where tc_name='" + TestCaseName + "'"
                tc_id = DB.GetData(Conn, query, False)
                test_case_step_length = DB.GetData(Conn, "select count(*) from test_steps where tc_id='%s'" % (tc_id[0][0]), False)
                datasetid = ""
                if int(StepSequence) < test_case_step_length[0][0] + int(1):
                    datasetid = tc_id[0][0] + "_s" + StepSequence
                else:
                    query = "select teststepsequence from test_steps where tc_id='%s'" % tc_id[0][0]
                    test_sequence = DB.GetData(Conn, query)
                    stepsequence = 1
                    for each in test_sequence:
                        if StepSeqId[0] == each:
                            break
                        else:
                            stepsequence += 1
                    datasetid = tc_id[0][0] + "_s" + str(stepsequence)
                query = "select description from master_data where id='" + datasetid + "' and field='step' and value='description'"
                purpose = DB.GetData(Conn, query, False)
                TestStep_Description.append(purpose[0][0])
                TestStep_Description = tuple(TestStep_Description)
                TestStep_Description = [TestStep_Description]
                data_required = ""
                if step_desc[0][1] == True:
                    data_required = "yes"
                else:
                    data_required = "no"
                data_col = ["DataSetId", "Data"]
                data_val = []
                data_val_comp = []
                dataset = []
                if data_required == "yes":
                    datasetid += '_d'
                    query = "select distinct id from master_data where id Ilike '" + datasetid + "%'"
                    dataset_temp = DB.GetData(Conn, query)
                    for each in dataset_temp:
                        if len(each) == 14:
                            dataset.append(each)
                    count = 1
                    for each in dataset:
                        data_val.append((count, ""))
                        count += 1
                        print str(count) + " - " + each
                        query = "select field,value from master_data where id Ilike'" + each + "%' and field!=''"
                        data_set_val = DB.GetData(Conn, query, False)
                        data_val_comp.append(data_set_val)        
                    """data_val.append((1,""))
                    query="select field,value from master_data where id='"+datasetid+"'"
                    data_set_val=DB.GetData(Conn,query,False)"""
    results = {
               'TestStep_Details':TestStep_Details,
               'TestStep_Col':TestStep_Col,
               'TestStep_Description_Col':TestStep_Description_Col,
               'TestStep_Description':TestStep_Description,
               'data_required':data_required,
               'data_col':data_col,
               'data_val':data_val,
              # 'data_set_val':data_set_val,
               'data_val_comp':data_val_comp,
               'data_set_count':len(dataset)
               }

    JS = simplejson.dumps(results)
#    return HttpResponse(json.dumps(results, encoding='utf-8', ensure_ascii=False), mimetype='application/json') 
    return HttpResponse(JS, mimetype='application/json')


def FailStep_TestCases(request):  #==================Returns Test Cases When User Click on Fail Step On Test Result Page===============================
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':

            # If User Click on Fail Step 
            RunId = request.GET.get('RunID', '')
            FailStep = request.GET.get('FailedStep', '')
            if RunId != '' and FailStep != '':
                RunId = str(RunId.strip())
                FailStep = str(FailStep.strip())
                FailStep_TestCases = DB.GetData(Conn, "select "
                                                 "tct.name as MKSID, "
                                                 "tc.tc_name, "
                                                 "tr.status, "
                                                 "to_char(tr.duration,'HH24:MI:SS'), "
                                                 "tr.failreason, "
                                                 "tr.logid, "
                                                 "tc.tc_id "
                                                 "from test_case_results tr, test_step_results tsr, test_steps_list tsl, test_cases tc, test_case_tag tct "
                                                 "where tr.run_id = '%s' and tr.status = 'Failed' and tr.run_id = tsr.run_id "
                                                 "and tr.tc_id = tsr.tc_id and tsr.status in ('Failed') and tsr.teststep_id = tsl.step_id "
                                                 "and tr.tc_id = tc.tc_id and tc.tc_id = tct.tc_id and tct.property = 'MKS' and tsl.stepname = '%s' "
                                                 "order by tr.id " % (RunId, FailStep), False
                                                 )
                FailStep_TestCases1 = Modify(FailStep_TestCases)
                FailStep_TC_Col = ['Test Case ID', 'Failed Test Case', 'Test Case Type', 'Status', 'Duration', 'Fail Reason', 'Test Log', 'Autmation ID']
    results = {
               'FailStep_TestCases':FailStep_TestCases1,
               'FailStep_TC_Col': FailStep_TC_Col
               }
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def Verify_Query(request):  #==================Returns Message if Depandency is missing when User Click on Verify button on Test Run Page==============================
    Conn = GetConnection()
    propertyValue = "Ready"
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Query', '')
            UserText = UserData.split(":");

            Environment = request.GET.get(u'Env', '')
            if Environment == "Mac":
                Section = "MacSection"
                Test_Run_Type = "Mac_test_run_type"
                Priority = "MacPriority"
                Env_Dependency = "MacDependency"
                TCStatusName = "MacStatus"
                CustomTag = "MacCustomTag"
                Feature = 'feature'
                

            if Environment == "PC":
                Section = "Section"
                Test_Run_Type = "test_run_type"
                Priority = "Priority"
                Env_Dependency = "Dependency"
                TCStatusName = "Status"
                CustomTag = "CustomTag"
                CustomSet = 'set'
                Tag = 'tag'
                Feature = 'feature'
            Client='client'
            QueryText = []
            for eachitem in UserText:
                if len(eachitem) != 0 and  len(eachitem) != 1:
                    QueryText.append(eachitem.strip())

    if "Dev" in QueryText:
        QueryText.remove("Dev")
        propertyValue = "Dev"

#    Response = ""
#    Result = 'Pass'
#    DepandList = []

    #==========Depandency Checking=============

    # Making list of test case id ( when user selects only test case)
    TestIDList = []
    for eachitem in QueryText:
        TestID = DB.GetData(Conn, "Select property from test_case_tag where name = '%s' " % eachitem)
        for eachProp in TestID:
            if eachProp == 'tcid':
                TestIDList.append(eachitem)
                break




    if len(TestIDList) > 0:
        count = 1

        for eachitem in TestIDList:
            if count == 1:
                query = "t1.tc_id = '%s'" % eachitem
                count = count + 1

            elif count >= 2:
                query = query + " or " + "t1.tc_id = '%s'" % eachitem
                count = count + 1
        Query="select distinct t1.property, t2.property from test_case_tag t1, test_case_tag t2 where t1.tc_id = t2.tc_id and t1.property = t2.name and t1.name = '" + Env_Dependency + "' and (%s)" % query
        DepandencyNamesValues = DB.GetData(Conn, Query, False)
    elif len(QueryText) > 0:
        count = 1
        for eachitem in QueryText:
            if count == 1:
                Query = "HAVING COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + Feature + "','"+ CustomTag + "','" + Test_Run_Type + "','" + Priority + "','" + CustomSet + "','" + Tag +"','" + Client + "') THEN 1 END) > 0 "
                count = count + 1
            elif count >= 2:
                Query = Query + "AND COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + Feature + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','" + CustomSet + "','" + Tag + "','" + Client +"') THEN 1 END) > 0 "
        Query = Query + "AND COUNT(CASE WHEN name = '" + TCStatusName + "' and property = '" + propertyValue + "' THEN 1 END) > 0 "
        Query = Query + "AND COUNT(CASE WHEN property = 'machine_os' and name = '" + Environment + "' THEN 1 END) > 0 "
        query="Select distinct t1. property,t2. property from test_case_tag t1, test_case_tag t2 "
        query+="where t1.tc_id = t2.tc_id and t1.property = t2.name and t1.name = '" + Env_Dependency + "' and t1.tc_id in ("
        query+="select distinct tct.tc_id from test_case_tag tct, test_cases tc "
        query+="where tct.tc_id = tc.tc_id "
        query+="group by tct.tc_id,tc.tc_name %s ) " % Query
        DepandencyNamesValues = DB.GetData(Conn, query, False)
    DepandencyNames = []
    for eachitem in DepandencyNamesValues:
        if eachitem[1] not in DepandencyNames: DepandencyNames.append(eachitem[1])

    TempItem = []
    DepandencyList = []
    for eachitem in DepandencyNames:
        TempItem.append(eachitem)
        for item in DepandencyNamesValues:
            if eachitem in item: TempItem.append(item[0])

        DepandencyList.append(TempItem)
        TempItem = []



    results = {"DepandencyList":DepandencyList}
#     results = {'Response':Response, 'Result': Result}

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def Table_Data_UserList(request):  #==================Returns Available user list When there is no error in depandency ==============================
    Conn = GetConnection()
    results = {}
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'UserListRequest', '')
            Env = request.GET.get(u'Env', '')
            if Env == u"PC": Environment = "Windows"
            if Env == u"Mac": Environment = "Darwin"
            Machine_List = []
            Usable_Machine = []
            if UserData == "True":
                query = "select distinct tre.tester_id,pul.user_level from test_run_env tre,permitted_user_list pul where tre.tester_id=pul.user_names and tre.status='Unassigned' and pul.user_level in('Automation')" 
                Automation_Machine = DB.GetData(Conn, query, False)
                for each in Automation_Machine:
                    Usable_Machine.append(each)
                query = "select distinct user_names,user_level from permitted_user_list where user_level='Manual'"
                Manual_Machine = DB.GetData(Conn, query, False)
                for each in Manual_Machine:
                    query = "select distinct status from test_run_env where tester_id='%s'" % each[0].strip()
                    machine_status = DB.GetData(Conn, query)
                    if len(machine_status) == 0:
                        Usable_Machine.append(each)
                    else:
                        if 'In-Progress' in machine_status or 'Submitted' in machine_status:
                            continue
                        else:
                            Usable_Machine.append(each)
                for each in Usable_Machine:
                    query = "Select  distinct tester_id,os_name ||' '||os_version||' - '||os_bit as machine_os,client,last_updated_time,machine_ip from test_run_env where tester_id='" + each[0] + "' and os_name ='" + Environment + "' and status='Unassigned'"
                    tabledata = DB.GetData(Conn, query, False)
                    if len(tabledata) == 0:
                        continue
                    else:
                        temp = []
                        for eachitem in tabledata[0]:
                            temp.append(eachitem)
                        temp.insert(1, each[1])
                        Machine_List.append(temp)
                Heading = ["Machine Name", "Machine Type", "Machine OS", "Client", "Last Updated Time", "Machine IP"]
                # Heading.reverse()
    results = {'Heading':Heading, 'TableData':Machine_List}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def Run_Test(request):  #==================Returns True/Error Message  When User Click on Run button On Test Run Page==============================
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.is_ajax():
            if request.method == 'GET':
                is_rerun = request.GET.get(u'ReRun', '')
                previous_run = request.GET.get('RunID', '')    
                UserData = request.GET.get('RunTestQuery', '')
                UserData = str(UserData.replace(u'\xa0', u''))
                
                if is_rerun=="rerun":
                    query="select email_notification, assigned_tester, test_objective,test_milestone, branch_version, project_id,team_id, start_date,end_date,tester_id,machine_ip from test_run_env tre, machine_project_map mpm where mpm.machine_serial=tre.id and run_id='%s'"%previous_run
                    Conn=GetConnection()
                    Meta_info=DB.GetData(Conn,query,False)
                    Conn.close()
                    stEmailIds=Meta_info[0][0]
                    Testers=Meta_info[0][1]
                    TestObjective=(Meta_info[0][2]+' -ReRun')
                    TestMileStone=Meta_info[0][3]
                    Branch_Version=Meta_info[0][4]
                    project_id=Meta_info[0][5]
                    team_id=Meta_info[0][6]
                    starting_date=Meta_info[0][7]
                    ending_date=Meta_info[0][8]
                    TesterId=Meta_info[0][9]
                    machine_ip=Meta_info[0][10]
                    query="select type,name,bit,version from machine_dependency_settings mds, test_run_env tre where mds.machine_serial=tre.id and tre.tester_id='%s' and run_id='%s'"%(TesterId,previous_run)
                    Conn=GetConnection()
                    machine_data=DB.GetData(Conn,query,False)
                    Conn.close()
                else:
                    EmailIds = request.GET.get('EmailIds', '')
                    EmailIds = str(EmailIds.replace(u'\xa0', u''))
                    
                    TesterIds = request.GET.get('TesterIds', '')
                    TesterIds = str(TesterIds.replace(u'\xa0', u''))
                    
                    TestObjective = request.GET.get('TestObjective', '')
                    TestObjective = str(TestObjective.replace(u'\xa0', u''))
                    
                    TestMileStone = request.GET.get('TestMileStone', '')
                    TestMileStone = str(TestMileStone.replace(u'\xa0', u'').split(":")[0])
                    
                    project_id=request.GET.get(u'project_id','')
                    team_id=request.GET.get(u'team_id','')
                    start_date=request.GET.get(u'start_date','')
                    end_date=request.GET.get(u'end_date','')
                    
                    start_date=start_date.split('-')
                    starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
                    end_date=end_date.split('-')
                    ending_date=datetime.datetime(int(end_date[0].strip()),int(end_date[1].strip()),int(end_date[2].strip())).date()
                        
                    #processing email
                    EmailIds = EmailIds.split(":")
                    Emails = []
                    for eachitem in EmailIds :
                        if eachitem != "":
                            Conn=GetConnection()
                            Eid = DB.GetData(Conn, "Select email from permitted_user_list where user_names = '%s'" % str(eachitem))
                            Conn.close()
                        if len(Eid) > 0:
                            Emails.append(Eid[0])    
                    stEmailIds = ','.join(Emails)
                    
                    #getting testers
                    TesterIds = TesterIds.split(":")
                    Testers = []
                    for each in TesterIds:
                        if each != "" and each != ":":
                            Testers.append(each)
                    if is_rerun == 'rerun':
                        Testers.remove(" ")
                        if len(Testers) == 1:
                            Testers = Testers[0]
                        else:
                            Testers = ','.join(Testers)
                    else:
                        Testers = ','.join(Testers)
                
                
                UserText = UserData.split(":")
                QueryText=[]
                for eachitem in UserText:
                    if len(eachitem) != 0 and  eachitem != "" and eachitem.strip() not in QueryText:
                        QueryText.append(str(eachitem.strip()))
                print QueryText
                if is_rerun!="rerun":
                    TesterId = QueryText.pop()
                    TesterId = TesterId.strip()
                runid = TimeStamp("string")
                query = "select user_level from permitted_user_list where user_names='%s'" % TesterId
                Conn=GetConnection()
                Machine_Status = DB.GetData(Conn, query, False)
                Conn.close()
                if Machine_Status[0][0] == 'Manual':
                    if is_rerun != 'rerun':
                        status = "Unassigned"
                        updateTime = TimeStamp("string")
                        print status
                        print updateTime
                        Dict = {'run_id':runid,'last_updated_time':updateTime, 'test_objective':TestObjective}
                        sWhereQuery = "where tester_id='%s' and status='%s'" % (TesterId,status)
                        Conn=GetConnection()
                        print DB.UpdateRecordInTable(Conn, "test_run_env", sWhereQuery, **Dict)
                        Conn.close()
                    else:
                        status='Unassigned'
                        Conn=GetConnection()
                        result=DB.DeleteRecord(Conn, "test_run_env",tester_id=TesterId, status=status)
                        updated_time = TimeStamp("string")
                        Dict = {'tester_id':TesterId.strip(), 'status':'Unassigned', 'last_updated_time':updated_time.strip(), 'machine_ip':machine_ip, 'branch_version':Branch_Version.strip()}
                        Conn=GetConnection()
                        tes2 = DB.InsertNewRecordInToTable(Conn, "test_run_env", **Dict)
                        Conn.close()
                        if(tes2 == True):
                            query="select id from test_run_env where tester_id='%s' and status='Unassigned' limit 1"%(TesterId.strip())
                            Conn=GetConnection()
                            temp_id=DB.GetData(Conn,query)
                            if isinstance(temp_id,list):
                                machine_id=temp_id[0]
                                problem=False
                                for each in machine_data:
                                    Dict={}
                                    Dict.update({'machine_serial':machine_id,'name':each[1],'type':each[0],'bit':each[2],'version':each[3]})                                   
                                    Conn=GetConnection()
                                    result=DB.InsertNewRecordInToTable(Conn,"machine_dependency_settings",**Dict)
                                    Conn.close()
                            Conn=GetConnection()
                            Dict={
                                  'machine_serial':machine_id,
                                  'project_id':project_id,
                                  'team_id':team_id
                            }
                            print DB.InsertNewRecordInToTable(Conn,"machine_project_map", **Dict)
                TestIDList = []
                for eachitem in QueryText:
                    if is_rerun == "rerun":
                        Conn=GetConnection()
                        TestID = DB.GetData(Conn, "Select property from result_test_case_tag where name = '%s' and run_id='%s'" % (eachitem, previous_run))
                        Conn.close()
                    else:
                        Conn=GetConnection()
                        TestID = DB.GetData(Conn, "Select property from test_case_tag where name = '%s' " % eachitem)
                        Conn.close()
                    for eachProp in TestID:
                        if eachProp == 'tcid':
                            TestIDList.append(eachitem)
                            break
                if len(TestIDList) > 0:
                    TestCasesIDs = TestIDList
                else:
                    Feature_tag='Feature'
                    Section_Tag = 'Section'
                    Custom_Tag = 'CustomTag'
                    Section_Path_Tag = 'section_id'
                    Feature_Path_Tag = 'feature_id'
                    Priority_Tag = 'Priority'
                    set_type='set'
                    tag_type='tag'
                    Status='Status'
                    query="select distinct dependency_name from dependency d, dependency_management dm where d.id=dm.dependency and dm.project_id='%s' and dm.team_id=%d"%(project_id,int(team_id))
                    Conn=GetConnection()
                    dependency=DB.GetData(Conn,query)
                    Conn.close()
                    wherequery=""
                    for each in dependency:
                        wherequery+=("'"+each.strip()+"'")
                        wherequery+=','
                    wherequery+=("'"+Feature_tag+"','"+Section_Tag+"','"+Custom_Tag+"','"+Section_Path_Tag+"','"+Feature_Path_Tag+"','"+Priority_Tag+"','"+Status+"','"+set_type+"','"+tag_type+"'")
                    print wherequery
                    
                    count = 1
                    for eachitem in QueryText:
                        if count == 1:
                            Query = "HAVING COUNT(CASE WHEN name = '%s' and property in (%s) THEN 1 END) > 0 "%(eachitem.strip(),wherequery)
                            count=count+1
                        else:
                            Query+="AND COUNT(CASE WHEN name = '%s' and property in (%s) THEN 1 END) > 0 "%(eachitem.strip(),wherequery)
                            count=count+1
                    Query = Query + " AND COUNT(CASE WHEN property = 'Project' and name = '" + project_id + "' THEN 1 END) > 0"
                    Query = Query + " AND COUNT(CASE WHEN property = 'Team' and name = '" + team_id + "' THEN 1 END) > 0"
                    query = "select distinct tct.tc_id from test_case_tag tct,test_cases tc where tct.tc_id=tc.tc_id  group by tct.tc_id,tc.tc_name " + Query
                    Conn=GetConnection()
                    TestCasesIDs = DB.GetData(Conn, query)        
                    Conn.close()
                    print TestCasesIDs
                if is_rerun == "rerun":
                    Conn=GetConnection()
                    RegisterReRunPermanentInfo(Conn, runid, previous_run, TestCasesIDs)
                    Conn.close()
                    for eachitem in TestCasesIDs:
                        Dict = {'run_id':runid, 'tc_id':str(eachitem)}
                        Conn=GetConnection()
                        Result = DB.InsertNewRecordInToTable(Conn, "test_run", **Dict)
                        Conn.close()
                        print Result
                    AddReRunInfo(runid, previous_run)
                else:
                    Conn=GetConnection()
                    RegisterPermanentInfo(Conn, runid, TestCasesIDs)
                    Conn.close()
                    for eachitem in TestCasesIDs:
                        Dict = {'run_id':runid, 'tc_id':str(eachitem)}
                        Conn=GetConnection()
                        Result = DB.InsertNewRecordInToTable(Conn, "test_run", **Dict)
                        Conn.close()
                        print Result
                    AddInfo(runid)    
                run_description=""
                for each in QueryText:
                    run_description+=(each+" ")
                run_description=run_description.strip()
                Dict={
                      'rundescription':run_description,
                      'status':'Submitted',
                      'email_notification':stEmailIds,
                      'run_id':runid,
                      'test_objective':TestObjective,
                      #'project_id':project_id,
                      #'team_id':team_id,
                      'test_milestone':TestMileStone,
                      'run_type':'Manual',
                      'assigned_tester':Testers,
                      'start_date':starting_date,
                      'end_date':ending_date
                }
                Conn=GetConnection()
                sWhereQuery="where tester_id='%s' and status='Unassigned'"%(TesterId)
                result=DB.UpdateRecordInTable(Conn,"test_run_env",sWhereQuery,**Dict)
                Conn.close()
                Conn=GetConnection()
                now = DB.GetData(Conn, "SELECT CURRENT_TIMESTAMP;", False)
                sTestSetStartTime = str(now[0][0])
                Conn.close()
                print sTestSetStartTime
                Dict = {'run_id':runid, 'tester_id':str(TesterId), 'status': 'Submitted', 'rundescription':TestObjective, 'teststarttime':sTestSetStartTime}
                Conn=GetConnection()
                EnvResults = DB.InsertNewRecordInToTable(Conn, "test_env_results", **Dict)
                Conn.close()
                results = {'Result': result, 'runid':runid}
            json = simplejson.dumps(results)
            return HttpResponse(json, mimetype='application/json')

    except Exception,e:
        PassMessasge(sModuleInfo,e, error_tag)
        
def RegisterReRunPermanentInfo(Conn, run_id, previous_run, TestCasesIDs):
    # query="select tc_id from test_run where run_id='%s'"%run_id.strip()
    # est_cases=DB.GetData(Conn, query)
    test_cases = TestCasesIDs
    test_case_column_query = "select column_name from information_schema.columns where table_name='result_test_cases'"
    test_case_column = DB.GetData(Conn, test_case_column_query)
    for each in test_cases:
        test_case = each
        test_case_query = "select * from result_test_cases where tc_id='%s' and run_id='%s'" % (test_case, previous_run)
        Dict = {}
        test_case_column_data = DB.GetData(Conn, test_case_query, False)
        # ##populate Dict for the test_cases
        for each in test_case_column_data:
            for eachitem in zip(each, test_case_column):
                Dict.update({eachitem[1]:eachitem[0]})
        Dict.update({'run_id':run_id})
        print Dict
        result = DB.InsertNewRecordInToTable(Conn, "result_test_cases", **Dict)
        if result == False:
            CleanRun(run_id)
        ##########################################Result_Test_Steps_List##############################################
        test_step_column_query = "select column_name from information_schema.columns where table_name='result_test_steps_list'"
        test_step_column = DB.GetData(Conn, test_step_column_query)
        test_step_query = "select * from result_test_steps_list where step_id in (select step_id from result_test_steps where tc_id='" + test_case + "' and run_id='" + previous_run + "') and run_id='" + previous_run + "'"
        test_step_list_data = DB.GetData(Conn, test_step_query, False)
        # #form the dictionary
        for each in test_step_list_data:
            step_list_dict = {}
            for eachitem in zip(test_step_column, each):
                step_list_dict.update({eachitem[0]:eachitem[1]})
            step_list_dict.update({'run_id':run_id})
            available_query = "select count(*) from result_test_steps_list where run_id='%s' and step_id='%d'" % (step_list_dict['run_id'], step_list_dict['step_id'])
            available_count = DB.GetData(Conn, available_query)
            if available_count[0] == 0:
                result = DB.InsertNewRecordInToTable(Conn, "result_test_steps_list", **step_list_dict)
            elif available_count[0] > 0:
                condition = "exists"
                if condition == "exists":
                    result = True
            else:
                result = False
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Test_Steps##############################################
        test_steps_query = "select column_name from information_schema.columns where table_name='result_test_steps'"
        test_steps = DB.GetData(Conn, test_steps_query)
        test_steps_data_query = "select * from result_test_steps where tc_id='%s' and run_id='%s'" % (test_case, previous_run)
        test_steps_data = DB.GetData(Conn, test_steps_data_query, False)
        for each in test_steps_data:
            steps_dict = {}
            for eachitem in zip(test_steps, each):
                steps_dict.update({eachitem[0]:eachitem[1]})
            steps_dict.update({'run_id':run_id})
            result = DB.InsertNewRecordInToTable(Conn, "result_test_steps", **steps_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Master_Data##############################################
        master_data_column_query = "select column_name from information_schema.columns where table_name='result_master_data'"
        master_data_column = DB.GetData(Conn, master_data_column_query)
        master_data_query = "select * from result_master_data where id Ilike '%s%%' and run_id='%s'" % (test_case, previous_run)
        master_data = DB.GetData(Conn, master_data_query, False)
        for each in master_data:
            master_data_dict = {}
            for eachitem in zip(master_data_column, each):
                master_data_dict.update({eachitem[0]:eachitem[1]})
            master_data_dict.update({'run_id':run_id})
            result = DB.InsertNewRecordInToTable(Conn, "result_master_data", **master_data_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Test_Case_DataSets##############################################
        test_case_datasets_column_query = "select column_name from information_schema.columns where table_name='result_test_case_datasets'"
        test_case_dataset_column = DB.GetData(Conn, test_case_datasets_column_query)
        test_case_dataset_query = "select * from result_test_case_datasets where tc_id='%s' and run_id='%s'" % (test_case, previous_run)
        test_case_dataset = DB.GetData(Conn, test_case_dataset_query, False)
        for each in test_case_dataset:
            dataset_dict = {}
            for eachitem in zip(test_case_dataset_column, each):
                dataset_dict.update({eachitem[0]:eachitem[1]})
            dataset_dict.update({'run_id':run_id})
            result = DB.InsertNewRecordInToTable(Conn, "result_test_case_datasets", **dataset_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Test_Case_DataSets##############################################
        test_case_tag_column_query = "select column_name from information_schema.columns where table_name='result_test_case_tag'"
        test_case_tag_column = DB.GetData(Conn, test_case_tag_column_query)
        test_case_tag_query = "select * from result_test_case_tag where tc_id='%s' and run_id='%s'" % (test_case, previous_run)
        test_case_tag = DB.GetData(Conn, test_case_tag_query, False)
        for each in test_case_tag:
            tag_dict = {}
            for eachitem in zip(test_case_tag_column, each):
                tag_dict.update({eachitem[0]:eachitem[1]})
            tag_dict.update({'run_id':run_id})
            result = DB.InsertNewRecordInToTable(Conn, "result_test_case_tag", **tag_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Test_Steps_Data##############################################
        test_steps_data_column_query = "select column_name from information_schema.columns where table_name='result_test_steps_data'"
        test_steps_data_column = DB.GetData(Conn, test_steps_data_column_query)
        test_case_dataset_entry_query = "select distinct tsd.run_id,tsd.id,tsd.tcdatasetid,tsd.testdatasetid,tsd.teststepseq from result_test_case_datasets tcd,result_test_steps_data tsd where tcd.tcdatasetid=tsd.tcdatasetid and tcd.tc_id='%s' and tsd.run_id='%s'" % (test_case, previous_run)
        test_case_dataset_entry = DB.GetData(Conn, test_case_dataset_entry_query, False)
        for each in test_case_dataset_entry:
            step_data_dict = {}
            for eachitem in zip(test_steps_data_column, each):
                step_data_dict.update({eachitem[0]:eachitem[1]})
            step_data_dict.update({'run_id':run_id})
            result = DB.InsertNewRecordInToTable(Conn, "result_test_steps_data", **step_data_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Container_type_data##############################################
        container_type_data_column_query = "select column_name from information_schema.columns where table_name='result_container_type_data'"
        container_type_data_column = DB.GetData(Conn, container_type_data_column_query)
        container_type_data_query = "select distinct ctd.run_id,ctd.id,ctd.dataid,ctd.curname,ctd.newname,ctd.items_count from result_test_case_datasets tcd,result_test_steps_data tsd,result_container_type_data ctd where tcd.tcdatasetid=tsd.tcdatasetid and ctd.dataid=tsd.testdatasetid and tcd.tc_id='%s' and ctd.run_id='%s'" % (test_case, previous_run)
        container_type_data = DB.GetData(Conn, container_type_data_query, False)
        for each in container_type_data:
            ctd_dict = {}
            for eachitem in zip(container_type_data_column, each):
                ctd_dict.update({eachitem[0]:eachitem[1]})
            ctd_dict.update({'run_id':run_id})
            result = DB.InsertNewRecordInToTable(Conn, "result_container_type_data", **ctd_dict)
            if result == False:
                CleanRun(run_id)

def RegisterPermanentInfo(Conn, run_id, TestCasesIDs):
    print run_id
    # ##Enter the test Case Name in the result test_case table
    # get the test case name
    # query="select tc_id from test_run where run_id='%s'"%run_id.strip()
    # test_cases=DB.GetData(Conn, query)
    test_cases = TestCasesIDs
    test_case_column_query = "select column_name from information_schema.columns where table_name='test_cases'"
    test_case_column = DB.GetData(Conn, test_case_column_query)
    ##########################################Result_Test_Case##############################################
    for each in test_cases:
        test_case = each
        test_case_query = "select * from test_cases where tc_id='%s'" % test_case
        Dict = {}
        Dict.update({'run_id':run_id})
        test_case_column_data = DB.GetData(Conn, test_case_query, False)
        # ##populate Dict for the test_cases
        for each in test_case_column_data:
            for eachitem in zip(each, test_case_column):
                Dict.update({eachitem[1]:eachitem[0]})
        print Dict
        result = DB.InsertNewRecordInToTable(Conn, "result_test_cases", **Dict)
        if result == False:
            CleanRun(run_id)
        ##########################################Result_Test_Steps_List##############################################
        test_step_column_query = "select column_name from information_schema.columns where table_name='test_steps_list'"
        test_step_column = DB.GetData(Conn, test_step_column_query)
        test_step_query = "select * from test_steps_list where step_id in (select step_id from test_steps where tc_id='" + test_case + "')"
        test_step_list_data = DB.GetData(Conn, test_step_query, False)
        # #form the dictionary
        for each in test_step_list_data:
            step_list_dict = {}
            step_list_dict.update({'run_id':run_id})
            for eachitem in zip(test_step_column, each):
                step_list_dict.update({eachitem[0]:eachitem[1]})
            available_query = "select count(*) from result_test_steps_list where run_id='%s' and step_id='%d'" % (step_list_dict['run_id'], step_list_dict['step_id'])
            available_count = DB.GetData(Conn, available_query)
            if available_count[0] == 0:
                result = DB.InsertNewRecordInToTable(Conn, "result_test_steps_list", **step_list_dict)
            elif available_count[0] > 0:
                condition = "exists"
                if condition == "exists":
                    result = True
            else:
                result = False
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Test_Steps##############################################
        test_steps_query = "select column_name from information_schema.columns where table_name='test_steps'"
        test_steps = DB.GetData(Conn, test_steps_query)
        test_steps_data_query = "select * from test_steps where tc_id='%s'" % test_case
        test_steps_data = DB.GetData(Conn, test_steps_data_query, False)
        for each in test_steps_data:
            steps_dict = {}
            steps_dict.update({'run_id':run_id})
            for eachitem in zip(test_steps, each):
                steps_dict.update({eachitem[0]:eachitem[1]})
            result = DB.InsertNewRecordInToTable(Conn, "result_test_steps", **steps_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Master_Data##############################################
        master_data_column_query = "select column_name from information_schema.columns where table_name='master_data'"
        master_data_column = DB.GetData(Conn, master_data_column_query)
        master_data_query = "select * from master_data where id Ilike '%s%%'" % test_case
        master_data = DB.GetData(Conn, master_data_query, False)
        for each in master_data:
            master_data_dict = {}
            master_data_dict.update({'run_id':run_id})
            for eachitem in zip(master_data_column, each):
                master_data_dict.update({eachitem[0]:eachitem[1]})
            result = DB.InsertNewRecordInToTable(Conn, "result_master_data", **master_data_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Test_Case_DataSets##############################################
        test_case_datasets_column_query = "select column_name from information_schema.columns where table_name='test_case_datasets'"
        test_case_dataset_column = DB.GetData(Conn, test_case_datasets_column_query)
        test_case_dataset_query = "select * from test_case_datasets where tc_id='%s'" % test_case
        test_case_dataset = DB.GetData(Conn, test_case_dataset_query, False)
        for each in test_case_dataset:
            dataset_dict = {}
            dataset_dict.update({'run_id':run_id})
            for eachitem in zip(test_case_dataset_column, each):
                dataset_dict.update({eachitem[0]:eachitem[1]})
            result = DB.InsertNewRecordInToTable(Conn, "result_test_case_datasets", **dataset_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Test_Case_DataSets##############################################
        test_case_tag_column_query = "select column_name from information_schema.columns where table_name='test_case_tag'"
        test_case_tag_column = DB.GetData(Conn, test_case_tag_column_query)
        test_case_tag_query = "select * from test_case_tag where tc_id='%s'" % test_case
        test_case_tag = DB.GetData(Conn, test_case_tag_query, False)
        for each in test_case_tag:
            tag_dict = {}
            tag_dict.update({'run_id':run_id})
            for eachitem in zip(test_case_tag_column, each):
                tag_dict.update({eachitem[0]:eachitem[1]})
            result = DB.InsertNewRecordInToTable(Conn, "result_test_case_tag", **tag_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Test_Steps_Data##############################################
        test_steps_data_column_query = "select column_name from information_schema.columns where table_name='test_steps_data'"
        test_steps_data_column = DB.GetData(Conn, test_steps_data_column_query)
        test_case_dataset_entry_query = "select tsd.id,tsd.tcdatasetid,tsd.testdatasetid,tsd.teststepseq from test_case_datasets tcd,test_steps_data tsd where tcd.tcdatasetid=tsd.tcdatasetid and tcd.tc_id='%s'" % test_case
        test_case_dataset_entry = DB.GetData(Conn, test_case_dataset_entry_query, False)
        for each in test_case_dataset_entry:
            step_data_dict = {}
            step_data_dict.update({'run_id':run_id})
            for eachitem in zip(test_steps_data_column, each):
                step_data_dict.update({eachitem[0]:eachitem[1]})
            result = DB.InsertNewRecordInToTable(Conn, "result_test_steps_data", **step_data_dict)
            if result == False:
                CleanRun(run_id)
        ##########################################Result_Container_type_data##############################################
        container_type_data_column_query = "select column_name from information_schema.columns where table_name='container_type_data'"
        container_type_data_column = DB.GetData(Conn, container_type_data_column_query)
        container_type_data_query = "select ctd.id,ctd.dataid,ctd.curname,ctd.newname,ctd.items_count from test_case_datasets tcd,test_steps_data tsd,container_type_data ctd where tcd.tcdatasetid=tsd.tcdatasetid and ctd.dataid=tsd.testdatasetid and tcd.tc_id='%s'" % test_case
        container_type_data = DB.GetData(Conn, container_type_data_query, False)
        for each in container_type_data:
            ctd_dict = {}
            ctd_dict.update({'run_id':run_id})
            for eachitem in zip(container_type_data_column, each):
                ctd_dict.update({eachitem[0]:eachitem[1]})
            result = DB.InsertNewRecordInToTable(Conn, "result_container_type_data", **ctd_dict)
            if result == False:
                CleanRun(run_id)
def CleanRun(runid):
    print runid
def AddReRunInfo(run_id, previous_run):
    conn = GetConnection()
    query = "select tc_id from test_run where run_id='" + run_id + "'"
    TestCaseList = DB.GetData(conn, query)
    conn.close()
    for eachcase in TestCaseList:
        print eachcase
        conn=GetConnection()
        print DB.InsertNewRecordInToTable(conn, "test_case_results", run_id=run_id, tc_id=eachcase, status="Submitted")
        conn.close()
        query="select id from test_case_results where run_id='%s' and tc_id='%s' and status='Submitted'"%(run_id, eachcase)
        Conn=GetConnection()
        result_index=DB.GetData(Conn,query)
        Conn.close()        
        conn=GetConnection()
        TestStepsList = DB.GetData(conn, "Select ts.step_id,stepname,teststepsequence,tsl.driver,ts.test_step_type From result_Test_Steps ts,result_test_steps_list tsl where TC_ID = '%s' and ts.step_id = tsl.step_id and ts.run_id=tsl.run_id and ts.run_id='%s' Order By teststepsequence" % (eachcase, previous_run), False)
        conn.close()
        for eachstep in TestStepsList:
            # print eachcase +"step_sequence:"+str(eachstep[2])+" - "+str(eachstep[0])
            Dict = {'run_id':run_id, 'tc_id':eachcase, 'teststep_id':eachstep[0], 'status':"Submitted", 'teststepsequence':eachstep[2],'testcaseresulttindex':result_index[0]}
            conn=GetConnection()
            print DB.InsertNewRecordInToTable(conn, "test_step_results", **Dict)
            conn.close()
def AddInfo(run_id):
    conn = GetConnection()
    query = "select tc_id from test_run where run_id='" + run_id + "'"
    TestCaseList = DB.GetData(conn, query)
    conn.close()
    for eachcase in TestCaseList:
        print eachcase
        conn=GetConnection()
        print DB.InsertNewRecordInToTable(conn, "test_case_results", run_id=run_id, tc_id=eachcase, status="Submitted")
        conn.close()
        query="select id from test_case_results where run_id='%s' and tc_id='%s' and status='Submitted'"%(run_id, eachcase)
        Conn=GetConnection()
        result_index=DB.GetData(Conn,query)
        Conn.close()
        conn=GetConnection()
        TestStepsList = DB.GetData(conn, "Select ts.step_id,stepname,teststepsequence,tsl.driver,ts.test_step_type From Test_Steps ts,test_steps_list tsl where TC_ID = '%s' and ts.step_id = tsl.step_id Order By teststepsequence" % eachcase, False)
        conn.close()
        for eachstep in TestStepsList:
            # print eachcase +"step_sequence:"+str(eachstep[2])+" - "+str(eachstep[0])
            Dict = {'run_id':run_id, 'tc_id':eachcase, 'teststep_id':eachstep[0], 'status':"Submitted", 'teststepsequence':eachstep[2],'testcaseresulttindex':result_index[0]}
            conn=GetConnection()
            print DB.InsertNewRecordInToTable(conn, "test_step_results", **Dict)
            conn.close()
def ReRun_Fail_TestCases(request):
    Conn = GetConnection()
    results = {}
    Result = []
    Response = 'False'
    if request.is_ajax():
        if request.method == 'GET':
            RunID = request.GET.get('RunID', '')
            RunID = str(RunID)

            TesterID = request.GET.get('TesterID', '')
            TesterID = str(TesterID)

            ReRunType = request.GET.get('ReRunType', '')
            ReRunType = str(ReRunType)

            NewRunID = ''
            # Checking if the status of the user is not In-Progress or Submitted
            UserStatus = DB.GetData(Conn, "Select status from test_run_env where tester_id = '%s' ORDER BY id desc limit 1" % TesterID)
            if UserStatus[0] == "In-Progess" or UserStatus[0] == 'Submitted':
                Response = 'False'

            else:

                # gathering information using Run and TesterID to re-run the fail test cases
                UpdatedTime = TimeStamp("integer")
                NewRunID = TimeStamp("string")
                # generate the list of test cases to be run based on which button is clicked on the webpage
                FailedTestCases = DB.GetData(Conn, "Select tc_id from test_case_results where run_id = '%s' and status = 'Failed' " % RunID)
                PendingTestCases = DB.GetData(Conn, "select tc.tc_id "
                                        "from test_run tr,test_cases tc "
                                        "where tr.tc_id = tc.tc_id and tr.run_id = '%s' and "
                                        "tr.tc_id not in (select tc_id from test_case_results where run_id = '%s') " % (RunID, RunID))

                if ReRunType == 'Failed':
                    ReRunTestCases = FailedTestCases
                elif ReRunType == 'Pending':
                    ReRunTestCases = PendingTestCases
                elif ReRunType == 'FailedAndPending':
                    ReRunTestCases = FailedTestCases + PendingTestCases

                run_details = DB.GetData(Conn, "Select rundescription,product_version,machine_os,machine_ip,test_run_type,client,data_type,test_objective,email_notification from test_run_env where run_id = '%s'" % RunID, False)

                run_description = run_details[0][0]
                product_version = run_details[0][1]
                machine_os = run_details[0][2]
                machine_IP = run_details[0][3]
                testrun_type = run_details[0][4]
                client = run_details[0][5]
                data_type = run_details[0][6]
                test_objective = run_details[0][7]
                email_notification = run_details[0][8]

                # Adding fail test cases in test_sets table to make TestSet
                for eachTC in ReRunTestCases:
                    CreateFailedTestSet = DB.InsertNewRecordInToTable(Conn, "test_run",

                                                              run_id="%s" % NewRunID,
                                                              tc_id=str(eachTC),
                                                              )

                # Deleting entry of "Unassinged" if there is one
                try:
                    DeleteUnassignedRecord = DB.DeleteRecord(Conn, "test_run_env",

                                                            tester_id=TesterID,
                                                            status="Unassigned"
                                                            )
                except:
                    pass

                # Creating test run in testrunenv table for fail test cases of selected run id    
                testrunenv = DB.InsertNewRecordInToTable(Conn, "test_run_env",

                                        run_id=NewRunID,
                                        tester_id=TesterID,
                                        rundescription="Failed_Rerun_%s" % str(run_description),
                                        product_version=str(product_version),
                                        machine_os=str(machine_os),
                                        client=str(client),
                                        email_notification=str(email_notification),
                                        test_objective="Failed_Rerun_%s" % str(test_objective),
                                        data_type=str(data_type),
                                        machine_ip=str(machine_IP),
                                        status="Submitted",
                                        last_updated_time=UpdatedTime
                                         )
                if testrunenv == True:
                    Response = 'True'
                else:
                    Response = testrunenv



    results = {'Response':Response, 'RunID':NewRunID}

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def createTablefromString(request):
    import ast
    RunId = request.GET.get('mStr', '')
    RunId = ast.literal_eval(RunId)
    if len(RunId) > 0:
        for i in range(len(RunId)):
            eachId = RunId[i]
            if isinstance(eachId, tuple) == False:
                RunId[i] = (eachId,)

    numCol = len(RunId[0])
    results = {'Heading':numCol, 'TableData':RunId}

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')



def PerformanceResult_01(request):
    Conn = GetConnection()
    results = {}
    TestCaseList = []
    if request.is_ajax():
         if request.method == 'GET':
            UserData = request.GET.get(u'PerformanceResultRequest', '')


            Col = DB.GetData(Conn, "Select DISTINCT product_version from performance_results")
            Col.insert(0, "Test Cases / Bundles")
            DurationTempTable = []
            DurationTable = []
            MemoryTempTable = []
            MemoryTable = []
            DurationTableData = ''
            MemoryTableData = ''
            Bundles = DB.GetData(Conn, "Select DISTINCT product_version from performance_results")
            TestCases = DB.GetData(Conn, "Select tc_id from performance_results")
            for eachTC in TestCases:
                DurationTempTable.append(eachTC)
                MemoryTempTable.append(eachTC)
                for each in Bundles:
                    Memory = DB.GetData(Conn, "Select memory_avg from performance_results where tc_id = '%s' and product_version = '%s'" % (eachTC, each), False)
                    if Memory == [(None,)] or Memory == []:
                        MemoryTableData = "n/a"
                        MemoryTempTable.append(MemoryTableData)
                    else:
                        MemoryTableData = (str(list(Memory[0])[0]))
                        MemoryTempTable.append(MemoryTableData)
                    MemoryTableData = ''

                    Duration = DB.GetData(Conn, "Select to_char(duration,'HH24:MI:SS') from performance_results where tc_id = '%s' and product_version = '%s'" % (eachTC, each), False)
                    if Memory == [(None,)] or Memory == []:
                        DurationTableData = "n/a"
                        DurationTempTable.append(DurationTableData)
                    else:
                        DurationTableData = (str(list(Duration[0])[0]))
                        DurationTempTable.append(DurationTableData)
                    DurationTableData = ''

                MemoryTable.append(MemoryTempTable)
                MemoryTempTable = []
                DurationTable.append(DurationTempTable)
                DurationTempTable = []

            results = {'Heading':Col, 'DurationTable':DurationTable, 'MemoryTable': MemoryTable}

            json = simplejson.dumps(results)
            return HttpResponse(json, mimetype='application/json')


def getDatafromList(resp):
    for each in resp:
        if str(list(each)).find("(") != -1:
            resp.remove(each)
        TestStep_Col = ['Field', 'Value']
    results = {

               'TestStep_Details':resp,
               'TestStep_Col':TestStep_Col,

               }

    JS = simplejson.dumps(results)
#    return HttpResponse(json.dumps(results, encoding='utf-8', ensure_ascii=False), mimetype='application/json') 
    return HttpResponse(JS, mimetype='application/json')
#    mData = []
#    for eachField in resp:
#        col1 = eachField[0]
#        col2 = eachField[1]
#        mData.append(col1+","+col2)
#    return mData



def Bar_Chart(plot_data):

        data = plot_data[0]
        y_axis_lable = plot_data[1]
        graph_title = plot_data[2]
        path_to_output = plot_data[3]

        N = len(data)
        x = np.arange(1, N + 1)
        y = [ num for (s, num) in data ]
        labels = [ s for (s, num) in data ]
        width = 0.9
        bar1 = plt.bar(x, y, width, color=['#6FFFC3', '#6396FC', '#C69633', '#FF6F60', '#C6C63C', '#99CC33', '#CC9F9F', '#39C0CF', '#C9C9F3'], edgecolor='white')
        plt.ylabel(y_axis_lable)
        plt.suptitle(graph_title, fontsize=12, horizontalalignment='center', fontweight='bold')
        each_bar = 1
        for i in y:
            plt.text ((each_bar + 0.35), (i / 2) + 1, str(i))
            each_bar = each_bar + 1
        plt.xticks(x + width / 2, labels, rotation=30)
        plt.savefig(path_to_output, bbox_inches='tight')
        plt.clf()

def PerformanceResult(request):
    import FileUtilities as FL


    def average(rawlist):
        # sum divided by number of elements
        sum = 0
        for num in rawlist:
            sum += num
        return round (float(sum) / len(rawlist))

    def median(rawlist):
        # first sort the list
        rawlist.sort()
        # if list has even number of elements, then get the average of middle two elements
        if len(rawlist) % 2 == 0:
            # have to take avg of middle two
            mid = len(rawlist) / 2
            return (rawlist[mid - 1] + rawlist[mid]) / 2.0
        # if the list has odd number of elements, then get the middle element
        else:
            # find the middle (remembering that lists start at 0)
            mid = len(rawlist) / 2
            return rawlist[mid]

    def CleanRawData(rawlist):
        # return a list with good data removing data which are further away from median
        if len(rawlist) < 3:
            return rawlist
        else:
            IsListGood = False
            while IsListGood == False:
                difflist = []
                if len(rawlist) < 3:
                    return rawlist
                for eachNum in rawlist:
                    difflist.append(abs((float(median(rawlist) - eachNum) / median(rawlist) * 100)))

#                print "difflist:",difflist
                if max(difflist) >= 5.0:
#                    print "max:",max(difflist)
#                    print "index:",difflist.index(max(difflist))
#                    print "value to remove:",rawlist[difflist.index(max(difflist))]

                    rawlist.remove(rawlist[difflist.index(max(difflist))])
                else:
                    IsListGood = True
            return rawlist


    Conn = GetConnection()
    Environments = []
    Categories = []
    Bundles = []
    Col = []
    DurationTempTable = []
    DurationTable = []
    DurationTableData = []

    MemoryTempTable = []
    MemoryTable = []
    MemoryTableData = []

    CPUTempTable = []
    CPUTable = []
    CPUTableData = []

    Graph_BundleData = []
    Graph_BundleDataTuple_List = []
    GraphDataList = []
    GraphsPathList = []

    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'PerformanceResultRequest', '')
            GraphRequest = request.GET.get(u'GraphRequest', '')
        if UserData == "":
            tempEnvironments = DB.GetData(Conn, "select distinct machine_os, product_version,hw_model,tct.name from performance_results pr, test_case_tag tct where "
                                        "pr.tc_id = tct.tc_id and tct.property in ('Section','MacSection','CustomTag','MacCustomTag') and tct.name in ('PIM Performance','Media Performance','Other Performance')", False)
            # removing Performance from 'Media Performance' for eg
            for eachEnv in tempEnvironments:
                Environments.append((eachEnv[0], eachEnv[1], eachEnv[2], eachEnv[3].replace(' Performance', ''),))

            tempCategories = DB.GetData(Conn, "select distinct tct.name from performance_results pr, test_case_tag tct where "
                                        "pr.tc_id = tct.tc_id and tct.property in ('Section','MacSection','CustomTag','MacCustomTag') and tct.name in ('PIM Performance','Media Performance','Other Performance')", False)

            for eachCat in tempCategories:
                Categories.append((eachCat[0].replace(' Performance', ''),))

        else:
            ClickedEnvironment = request.GET.get(u'PerformanceResultRequest', '')
            Category = request.GET.get(u'category[]', '')
            Machine_os = ClickedEnvironment.split(",")[0]
            Product_Version = ClickedEnvironment.split(",")[1]
            Hadrware_model = ClickedEnvironment.split(",")[2]

            Bun = DB.GetData(Conn, "select product_version "
                                    "from "
                                        "(select distinct on (product_version) product_version, id from performance_results "
                                            "where machine_os = '%s' and "
                                            "product_version = '%s' and "
                                            "hw_model = '%s' ) foo order by id" % (Machine_os, Product_Version, Hadrware_model)
                               )
            Bundles = []
            for eachBun in Bun:
                Bundles.append(eachBun)


            Duration_TC_ID = DB.GetData(Conn, "Select DISTINCT pr.tc_id "
                            "from performance_results pr,test_case_tag tct "
                            "where pr.tc_id = tct.tc_id and "
                            "machine_os = '%s' and "
                            "product_version = '%s' and "
                            "hw_model = '%s' "
                            "group by pr.tc_id "
                            "HAVING COUNT(CASE WHEN name = 'Duration' and property in ('MacSection','Section','CustomTag','MacCustomTag') THEN 1 END) > 0"
                            "AND COUNT(CASE WHEN name = '%s Performance'  and property in ('MacSection','Section','CustomTag','MacCustomTag') THEN 1 END) > 0"
                            % (Machine_os, Product_Version, Hadrware_model, Category))



            # Finding All Duration Testing Cases Ran on Clicked Environment
            Memory_TC_ID = DB.GetData(Conn, "Select DISTINCT pr.tc_id "
                            "from performance_results pr,test_case_tag tct "
                            "where pr.tc_id = tct.tc_id and "
                            "machine_os = '%s' and "
                            "product_version = '%s' and "
                            "hw_model = '%s' "
                            "group by pr.tc_id "
                            "HAVING COUNT(CASE WHEN name = 'Memory' and property in ('MacSection','Section','CustomTag','MacCustomTag') THEN 1 END) > 0"
                            "AND COUNT(CASE WHEN name = '%s Performance'  and property in ('MacSection','Section','CustomTag','MacCustomTag') THEN 1 END) > 0"
                            % (Machine_os, Product_Version, Hadrware_model, Category))


                        # Finding All Duration Testing Cases Ran on Clicked Environment
            CPU_TC_ID = DB.GetData(Conn, "Select DISTINCT pr.tc_id "
                            "from performance_results pr,test_case_tag tct "
                            "where pr.tc_id = tct.tc_id and "
                            "machine_os = '%s' and "
                            "product_version = '%s' and "
                            "hw_model = '%s' "
                            "group by pr.tc_id "
                            "HAVING COUNT(CASE WHEN name = 'CPU' and property in ('MacSection','Section','CustomTag','MacCustomTag') THEN 1 END) > 0"
                            "AND COUNT(CASE WHEN name = '%s Performance'  and property in ('MacSection','Section','CustomTag','MacCustomTag') THEN 1 END) > 0"
                            % (Machine_os, Product_Version, Hadrware_model, Category))

            # Creating Folder for Graph if request is for Graph
            if  GraphRequest == "Graph":

                    FL.DelFolderWithExpTime("C:\Python27\WorkSpace\DjangoFramework10\site_media", "Graph", 1)
                    GraphFolderName = "Graph_%s" % str(time.time())
                    FL.CreateEmptyFolder("C:\Python27\WorkSpace\DjangoFramework10\site_media", GraphFolderName)
                    # FL.CreateEmptyFolder("W:\site_media", GraphFolderName)


            # Duration Table Data    
            for eachTC_ID in Duration_TC_ID:

                DurationTempTable.append(eachTC_ID)
                TC_Name = DB.GetData(Conn, "select tc_name from test_cases where tc_id = '%s'" % (eachTC_ID))
                DurationTempTable.append(TC_Name[0])

                for eachBun in Bun:


                    Duration = DB.GetData(Conn, "Select floor(extract('epoch' from pr.duration))::integer "
                                          "from performance_results pr, test_case_tag tct"
                                          " where "
                                                    "pr.tc_id = tct.tc_id and "
                                                    "pr.tc_id = '%s' and "
                                                    "pr.product_version = '%s' and "
                                                    "pr.machine_os = '%s' and "
                                                    "pr.hw_model = '%s' and "
                                                    "tct.name = 'Duration' and "
                                                    "tct.property in ('Section','MacSection','CustomTag','MacCustomTag') "

                                                     % (eachTC_ID, eachBun, Machine_os, Hadrware_model))
        #                DurationCount = DB.GetData(Conn,"Select Count( duration ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
        #                DurationMax = DB.GetData(Conn,"Select to_char(MAX(duration),'HH24:MI:SS') from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
        #                DurationMin = DB.GetData(Conn,"Select to_char(MIN(duration),'HH24:MI:SS') from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    if Duration == [(None,)] or Duration == []:
                        DurationTableData = ""
                        DurationTempTable.append(DurationTableData)
                    else:
                        DurationTableData = CleanRawData(Duration)
                        if len(DurationTableData) < 3:
                            DurationTableData = "Insufficient Data"
                        else:
                            DurationTableData = average(DurationTableData)

                        # Duration = (str(list(Duration[0])[0]))
        #                    DurationTableData = "%s(%s) <br>  Max(%s) <br> Min(%s)" %(Duration,(str(list(DurationCount[0])[0])),(str(list(DurationMax[0])[0])),(str(list(DurationMin[0])[0])))
                        DurationTempTable.append(DurationTableData)

                    if DurationTableData != "" and DurationTableData != "Insufficient Data":
                        Graph_BundleData.append(eachBun)
                        Graph_BundleData.append(int(DurationTableData))
                        Graph_BundleData = tuple(Graph_BundleData)
                        Graph_BundleDataTuple_List.append(Graph_BundleData)

                    DurationTableData = ''
                    Graph_BundleData = []

                DurationTable.append(DurationTempTable)
                DurationTempTable = []

                if  GraphRequest == "Graph":
                    TargetValue = DB.GetData(Conn, "Select name from test_case_tag where tc_id = '%s' and property = 'Target' " % (eachTC_ID))
                    if TargetValue != []:
                        TargetValue = ("Target", int(TargetValue[0]))
                        Graph_BundleDataTuple_List.insert(0, TargetValue)
                        Target_Flag = 1
                    WinTargetValue = DB.GetData(Conn, "Select name from test_case_tag where tc_id = '%s' and property = 'WinTarget' " % (eachTC_ID))
                    if WinTargetValue != []:
                        WinTargetValue = ("Windows", int(WinTargetValue[0]))
                        Graph_BundleDataTuple_List.insert(0, WinTargetValue)
                        Target_Flag = 2
                    CompTargetValue = DB.GetData(Conn, "Select name from test_case_tag where tc_id = '%s' and property = 'CompTarget' " % (eachTC_ID))
                    if CompTargetValue != []:
                        CompTargetValue = ("Competitor", int(CompTargetValue[0]))
                        Graph_BundleDataTuple_List.insert(0, CompTargetValue)
                        Target_Flag = 2

                GraphDataList.append(Graph_BundleDataTuple_List)
                GraphDataList.append("y_%s" % TC_Name[0])
                GraphDataList.append(TC_Name[0])

                if  GraphRequest == "Graph":
                    if len(Graph_BundleDataTuple_List) > 1 and Target_Flag == 1:
                        GraphDataList.append("C:\Python27\WorkSpace\DjangoFramework10\site_media\%s\%s.png" % (GraphFolderName, TC_Name[0]))
                        Bar_Chart(GraphDataList)
                        GraphsPathList.append("/site_media/%s/%s.png" % (GraphFolderName, TC_Name[0]))
                    elif len(Graph_BundleDataTuple_List) > 2 and Target_Flag == 2:
                        GraphDataList.append("C:\Python27\WorkSpace\DjangoFramework10\site_media\%s\%s.png" % (GraphFolderName, TC_Name[0]))
                        Bar_Chart(GraphDataList)
                        GraphsPathList.append("/site_media/%s/%s.png" % (GraphFolderName, TC_Name[0]))

                GraphDataList = []
                Graph_BundleDataTuple_List = []



                # Memory Table Data
            for eachTC_ID in Memory_TC_ID:

                MemoryTempTable.append(eachTC_ID)
                TC_Name = DB.GetData(Conn, "select tc_name from test_cases where tc_id = '%s'" % (eachTC_ID))
                MemoryTempTable.append(TC_Name[0])

                for eachBun in Bun:

                    Memory = DB.GetData(Conn, "Select memory_delta from performance_results where tc_id = '%s' and product_version = '%s'" % (eachTC_ID, eachBun), False)
                    # MemoryCount = DB.GetData(Conn,"Select count( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    # MemoryMax = DB.GetData(Conn,"Select MAX( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    # MemoryMin = DB.GetData(Conn,"Select MIN( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    if Memory == [(None,)] or Memory == []:
                        MemoryTableData = "n/a"
                        MemoryTempTable.append(MemoryTableData)
                    else:
                        MemoryList = []
                        for each in Memory:
                            MemoryList.append(each[0])
                        MemoryTableData = average(MemoryList)

                        #    Memory = (str(list(Memory[0])[0]))
                        #    MemoryTableData = "%s(%s) <br> Max(%s) <br> Min(%s)" %(Memory,(str(list(MemoryCount[0])[0])),(str(list(MemoryMax[0])[0])),(str(list(MemoryMin[0])[0])))
                        MemoryTempTable.append(MemoryTableData)

                    if MemoryTableData != "":
                        Graph_BundleData.append(eachBun)
                        Graph_BundleData.append(int(MemoryTableData))
                        Graph_BundleData = tuple(Graph_BundleData)
                        Graph_BundleDataTuple_List.append(Graph_BundleData)

                    Graph_BundleData = []
                    MemoryTableData = ''

                MemoryTable.append(MemoryTempTable)
                MemoryTempTable = []


            # CPU Table Data
            for eachTC_ID in CPU_TC_ID:
                CPUTempTable.append(eachTC_ID)
                TC_Name = DB.GetData(Conn, "select tc_name from test_cases where tc_id = '%s'" % (eachTC_ID))
                CPUTempTable.append(TC_Name[0])

                for eachBun in Bun:
                    CPU = DB.GetData(Conn, "Select cpu_avg from performance_results where tc_id = '%s' and product_version = '%s'" % (eachTC_ID, eachBun), False)
                    # MemoryCount = DB.GetData(Conn,"Select count( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    # MemoryMax = DB.GetData(Conn,"Select MAX( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    # MemoryMin = DB.GetData(Conn,"Select MIN( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    if CPU == [(None,)] or CPU == []:
                        CPUTableData = "n/a"
                        CPUTempTable.append(CPUTableData)
                    else:
                        CPUList = []
                        for each in CPU:
                            CPUList.append(each[0])
                        CPUTableData = average(CPUList)

                        CPUTempTable.append(CPUTableData)

                    if CPUTableData != "":
                        Graph_BundleData.append(eachBun)
                        Graph_BundleData.append(int(CPUTableData))
                        Graph_BundleData = tuple(Graph_BundleData)
                        Graph_BundleDataTuple_List.append(Graph_BundleData)

                    Graph_BundleData = []
                    CPUTableData = ''

                CPUTable.append(CPUTempTable)
                CPUTempTable = []


        Col = Bundles
        Col.insert(0, "Test Cases")
        Col.insert(1, "Test Case Name")

        # To make lenght of tables one, if they have nothing  
        if len(DurationTable) != 0:
            if len(DurationTable[0]) == 0: DurationTable = []
        if len(MemoryTable) != 0:
            if len(MemoryTable[0]) == 0: MemoryTable = []
        if len(CPUTable) != 0:
            if len(CPUTable[0]) == 0: MemoryTable = []
#        if len(GraphsPathList) != 0:
#            if len(GraphsPathList[0]) == 0: GraphsPathList = []

        results = {'Environments':Environments, 'Heading':Col, 'DurationTable':DurationTable, 'MemoryTable': MemoryTable, 'CPUTable':CPUTable, 'GraphPathList':GraphsPathList, 'Categories':Categories}

        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')


def Performance_ClickedBundle_Details(request, type):

    if request.method == 'GET':
        BundleNumber = request.GET.get(u'BundleNumber', '')
        # BundleNumber = BundleNumber.replace("B","")
        TestCaseNumber = request.GET.get(u'TestCaseNumber', '')
        Environment = request.GET.get(u'PerformanceResultRequest', '')
        Machine_os = Environment.split(",")[0]
        Hadrware_model = Environment.split(",")[2]

    variable = ''
    if type == "D":
        variable = "floor(extract('epoch' from pr.duration))::integer"
    elif type == "M":
        variable = "pr.memory_delta"
    elif type == "C":
        variable = "pr.cpu_peak,  to_char(pr.cpu_peaktime,'HH24:MI:SS')"
        # floor(extract('epoch' from pr.cpu_peaktime))::integer"

    Conn = GetConnection()

    Performance_TestCase_Duration_Table = DB.GetData(Conn, "Select pr.run_id,ter.status as test_run_status ," + variable + ",tcr.logid "
                      "from performance_results pr, test_case_results tcr, test_env_results ter "
                      "where "
                            "pr.run_id = tcr.run_id and "
                            "pr.run_id = ter.run_id and "
                            "pr.tc_id = tcr.tc_id and "
                            "product_version = '%s' and "
                            "pr.tc_id = '%s' and "
                            "machine_os = '%s' and "
                            "hw_model = '%s' " % (BundleNumber, TestCaseNumber, Machine_os, Hadrware_model), False
                        )

    Performance_TestCase_Duration_Table = sorted(Performance_TestCase_Duration_Table, key=lambda Performance_TestCase_Duration_Table: Performance_TestCase_Duration_Table[4], reverse=True)

    Col = []
    logIndx = 5
    Col.insert(0, "Run ID")
    Col.insert(1, "Run Status")
    if type == "D":
        Col.insert(4, "Duration (s)")
    elif type == "M":
        Col.insert(4, "Free Memory Consumption (%)")
    elif type == "C":
        Col.insert(4, "CPU Peak (%)")
        Col.insert(5, "CPU Peak Time")
        logIndx = 6
    Col.insert(logIndx, "Log")


    results = {"BundleNumber":BundleNumber, 'Performance_TestCase_Duration_Table':Performance_TestCase_Duration_Table, 'Heading':Col}

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def TestCaseSearch(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        # Ignore queries shorter than length 3
        # if len(value) > 1:
        # results = DB.GetData(Conn,"Select DISTINCT name from test_case_tag where name != 'Dependency' and name Ilike '%" + value + "%'")
        # results = DB.GetData(Conn, "Select DISTINCT tc_id from test_cases")
        results = DB.GetData(Conn, "Select  DISTINCT tc_id,tc_name,'Test Case' from test_cases where tc_id Ilike '%" + value + "%' or tc_name Ilike '%" + value + "%'", False)

    results = list(set(results))
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')



def Selected_TestCaseID_Analaysis(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Selected_TC_Analysis', '')

    query = "select run_id,tc.tc_name,status,failreason,logid from test_case_results tcr,test_cases tc where tc.tc_id='%s' and tcr.tc_id = tc.tc_id order by tcr.teststarttime desc" % UserData
    TestCase_Analysis_Result = DB.GetData(Conn, query, False)
    Col = ["Run ID", "Test Case Name", "Status", "Fail Reason", "Product logid"]

    results = {'Heading':Col, 'TestCase_Analysis_Result':TestCase_Analysis_Result}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Selected_TestCaseID_History(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Selected_TC_Analysis', '')

    query = "select tcr.run_id,tcr.status,tcr.failreason from test_case_results tcr,test_cases tc where tc.tc_id='%s' and tcr.tc_id = tc.tc_id order by tcr.teststarttime desc" % UserData
    TestCase_Analysis_Result = DB.GetData(Conn, query, False)
    Col = ["Run ID", "Status", "Fail Reason"]

    results = {'Heading':Col, 'TestCase_Analysis_Result':TestCase_Analysis_Result}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def ExecutionReport(request):
    templ = get_template('ExecutionReport.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def Execution_Report_Table(request):
    Conn = GetConnection()
    # find latest bundles for PC
    PCBundles = DB.GetData(Conn, "select split_part(split_part(product_version, E',',1),E':',2) from test_run_env where status in ('Complete') and product_version ilike '%Version:%'  and machine_os ilike 'Windows%' order by id desc" , False)
    BundleList = []
    BundleListFinal = []
    for eachbundle in PCBundles:
        BundleList.append(eachbundle[0])

    for eachbundle in BundleList:
        if eachbundle not in BundleListFinal:
            BundleListFinal.append(eachbundle)

    # for each bundle, get passed, failed, total and add it to the results table
    BundleResultTable = []
    for eachbundle in BundleListFinal:
        sqlQuery = """(select count(*) from test_case_results where run_id in (select run_id from test_run_env where product_version ilike '%""" + eachbundle + """%' and status in ('Complete'))
         group by status
         order by status)
         union
         select count from (
         select count(*) as count from test_case_results where run_id in (select run_id from test_run_env where product_version ilike '%""" + eachbundle + """%' and status in ('Complete'))
         ) total"""


        BundleResult = DB.GetData(Conn, sqlQuery)
        try:
            passedcount = int(BundleResult[0])
        except:
            continue
        try:
            failedcount = int(BundleResult[1])
        except:
            failedcount = 0
        try:
            totalcount = int(BundleResult[2])
        except:
            totalcount = passedcount + failedcount

        BundleResultTable.append((eachbundle, passedcount, failedcount, totalcount))


    Headings = ["Product Version", "Failed", "Passed", "Total"]

    results = {'Headings':Headings, 'Result': BundleResultTable}

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestCase_ParseData(temp, Steps_Name_List, Step_Description_List, Step_Expected, Step_Verification_Point, Step_Time_List):
    print Step_Expected
    Steps_Data_List = []
    # s = step # d = data # t = tuple # a = address
    d = 0
    index = -1
    for name in zip(Steps_Name_List, Step_Description_List, Step_Expected, Step_Verification_Point, Step_Time_List):
        # init step array
        Steps_Data_List.insert(d, (name[0].strip(), [], name[1].strip(), name[2].strip(), name[3].strip(), name[4].strip()))

        index = Steps_Name_List.index(name[0], index + 1)
        if index < len(temp):
            AllStepData = temp[index]
            if AllStepData == '%':
                d += 1
                continue
        else:
            d += 1
            continue
        t = 0
        for data in AllStepData.split("%"):
            # init data array
            Steps_Data_List[d][1].insert(t, [])

            if '#' in data:
                editList = []
                et = 0
                for dataEach in data.split("#"):
                    editList.insert(et, [])
                    # contact parse
                    regex = re.compile("\)\s*?,|\(|\)")
                    tupleList = regex.split(dataEach)

                    address = False
                    a = 0
                    for tupleItem in tupleList:
                        if ']' in tupleItem and address:
                            address = False
                            a += 1
                            continue
                        if tupleItem.strip() == '' or tupleItem == ']' or tupleItem == '[': continue

                        if address or '[' in tupleItem:
                            if not address:
                                addressTupleField, addressTupleData = tupleItem.replace('[', '').replace(']', '').split(",")
                                # init tuple array
                                editList[et].append((addressTupleField, []))
                                address = True
                                continue

                            strAddressTuple = tupleItem.replace('[', '').replace(']', '').split(",")
                            strAddressTuple[0] = strAddressTuple[0].strip()
                            strAddressTuple[1] = strAddressTuple[1].strip()
                            addressTuple = tuple(strAddressTuple)
                            editList[et][a][1].append(addressTuple)
                        else:
                            strNormalTuple = tupleItem.replace('[', '').replace(']', '').split(",")
                            strNormalTuple[0] = strNormalTuple[0].strip()
                            strNormalTuple[1] = strNormalTuple[1].strip()
                            normalTuple = tuple(strNormalTuple)
                            editList[et].append(normalTuple)
                            a += 1
                    et += 1
                Steps_Data_List[d][1][t] = (editList[0], editList[1])
            else:
                # contact parse
                regex = re.compile("\)\s*?,|\(|\)")
                tupleList = regex.split(data)

                address = False
                a = 0
                for tupleItem in tupleList:
                    if ']' in tupleItem and address:
                        address = False
                        a += 1
                        continue
                    if tupleItem.strip() == '' or tupleItem == ']' or tupleItem == '[': continue

                    if address or '[' in tupleItem:
                        if not address:
                            addressTupleField, addressTupleData = tupleItem.replace('[', '').replace(']', '').split(",")
                            # init tuple array
                            Steps_Data_List[d][1][t].append((addressTupleField.strip(), []))
                            address = True
                            continue
                        strAddressTuple = tupleItem.replace('[', '').replace(']', '').split(",")
                        strAddressTuple[0] = strAddressTuple[0].strip()
                        strAddressTuple[1] = strAddressTuple[1].strip()
                        addressTuple = tuple(strAddressTuple)
                        Steps_Data_List[d][1][t][a][1].append(addressTuple)
                    else:
                        strNormalTuple = tupleItem.replace('[', '').replace(']', '').split(",")
                        strNormalTuple[0] = strNormalTuple[0].strip()
                        strNormalTuple[1] = strNormalTuple[1].strip()
                        normalTuple = tuple(strNormalTuple)
                        Steps_Data_List[d][1][t].append(normalTuple)
                        a += 1
                t += 1
        d += 1

    return Steps_Data_List


def Create_Submit_New_TestCase(request):
    """
    @summary: Creates a new test case
    @param Platform: PC, Mac
    @param Manual_TC_Id: MKS/Jira test case id or empty
    @param TC_Name: Title of the test case
    @param TC_Type: Default / Performance / Localization
    @param Tag_List: List of Section names tag
    @param Tag_List: List of Feature names tag
    @param Dependency_List: List of dependent clients
    @param Priority_List: P1, P2, P3
    @param Steps_Data_List: [(Step1,Data1),(Step2,Data2),(Step3,Data3)]. Step1 = stepname, Data1 = [(Field,value)] format depends on the step
    """

    def returnResult(string):
        json = simplejson.dumps(string)
        return HttpResponse(json, mimetype='application/json')

    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        Conn = GetConnection()
        error = ''
        if request.is_ajax() and request.method == 'GET':
            #Platform = request.GET.get(u'Platform', '')
            #Manual_TC_Id = request.GET.get(u'Manual_TC_Id', '').split(',')
            TC_Name = request.GET.get(u'TC_Name', '')
            TC_Creator = request.GET.get(u'TC_Creator', '')
            #TC_Type = request.GET.get(u'TC_Type', '').split('|')
            Tag_List = request.GET.get(u'Tag_List', '').split('|')
            Dependency_List = request.GET.get(u'Dependency_List', '').split('|')
            Priority = request.GET.get(u'Priority', '')
            temp = request.GET.get(u'Steps_Data_List', '').split('|')
            Steps_Name_List = request.GET.get(u'Steps_Name_List', '').split('|')
            Associated_Bugs_List = request.GET.get(u'Associated_Bugs_List', '').split(',')
            Requirement_ID_List = request.GET.get(u'Requirement_ID_List', '').split(',')
            Status = request.GET.get(u'Status', '')
            Is_Edit = request.GET.get(u'Is_Edit', 'create')
            Section_Path = request.GET.get(u'Section_Path', '')
            Feature_Path = request.GET.get(u'Feature_Path', '')
            Step_Description_List = request.GET.get(u'Steps_Description_List', '')
            print Step_Description_List
            Step_Description_List = Step_Description_List.split('|')
            Step_Expected_Result = request.GET.get(u'Steps_Expected_List', '').split('|')
            Step_Verification_Point = request.GET.get(u'Steps_Verify_List', '').split('|')
            Step_Time_List = request.GET.get(u'Steps_Time_List', '').split('|')
            Project_id=request.GET.get(u'Project_Id','')
            Team_id=request.GET.get(u'Team_Id','')
            labels=request.GET.get(u'labels','')
                
            labels=labels.split("|")
            temp_list=[]
            for each in Dependency_List:
                temporary=each.split(":")
                temp_list.append((temporary[0],temporary[1].split(",")))
            Dependency_List=temp_list
            
            Steps_Data_List = TestCase_ParseData(temp, Steps_Name_List, Step_Description_List, Step_Expected_Result, Step_Verification_Point, Step_Time_List)

        # 1
        ##########Data Validation: Check if all required input fields have data
        test_case_validation_result = TestCaseCreateEdit.TestCase_DataValidation(TC_Name, Priority, Tag_List, Dependency_List, Steps_Data_List, Section_Path, Feature_Path)
        if test_case_validation_result != "Pass":
            return returnResult(test_case_validation_result)

        # 2
        ##########Test Case Id & Name
        if 'create' in Is_Edit:
            # Automation Test Case Id - automatically picked up from db
            tmp_id = DB.GetData(Conn, "select nextval('testcase_testcaseid_seq')")
            TC_Id = TestCaseCreateEdit.Generate_TCId(Section_Path, tmp_id[0])
            # Check if test case id is used before
            tmp_id = DB.GetData(Conn, "select tc_id from test_cases where tc_id = '%s'" % TC_Id)
            if len(tmp_id) > 0:
                print "Error. Test case id already used"
                error = "TEST CASE CREATION Failed. Test case id already used:%s***********************" % (TC_Name)
                TestCaseCreateEdit.LogMessage(sModuleInfo, error, 3)
                return returnResult(error)
            # Insert Test Case
            test_cases_result = TestCaseCreateEdit.Insert_TestCaseName(Conn, TC_Id, TC_Name, TC_Creator)
            if test_cases_result != 'Pass':
                # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
                error = "Returns from TestCaseCreateEdit Module by Failing to enter test case id %s" % TC_Id
                print error
                TestCaseCreateEdit.LogMessage(sModuleInfo, test_cases_result, 3)
                return returnResult(test_cases_result)
            if len(labels)>0:
                if (labels[0]!=''):
                    labels_result = TestCaseCreateEdit.Insert_Linkings(Conn, TC_Id, TC_Name, labels)
                    if labels_result != 'Pass':
                        # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
                        error = "Returns from TestCaseCreateEdit Module by Failing to enter labels for test case id %s" % TC_Id
                        print error
                        TestCaseCreateEdit.LogMessage(sModuleInfo, labels_result, 3)
                        return returnResult(labels_result)
        else:
            TC_Id = Is_Edit
        # 3
        ##########Test Case DataSet
        # tcdatasetid should be unique. And creating a test case, make sure there is no tcdatasetid existing for that test case
        # Test case dataset format of TC_Idds eg if TC_Id is 100, dataset id will be 100ds
        Test_Case_DataSet_Id = 0
        tmp_id = DB.GetData(Conn, "select tcdatasetid from test_case_datasets where tcdatasetid = '%sds'" % TC_Id)
        if len(tmp_id) > 0:
            for i in range(1, 10):
                tmp_id = DB.GetData(Conn, "select tcdatasetid from test_case_datasets where tcdatasetid = '%sds_%s'" % (TC_Id, i))
                if len(tmp_id) == 0:
                    Test_Case_DataSet_Id = '%sds_%s' % (TC_Id, i)
                    break
        else:
            Test_Case_DataSet_Id = '%sds' % (TC_Id)

        if Test_Case_DataSet_Id == 0:
            error = "Error. Test case Dataset id error"
            print error
            # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
            TestCaseCreateEdit.LogMessage(sModuleInfo, error, 3)
            return returnResult("Unable to create dataset for this test case")
        # Insert Test Case DataSet
        test_case_dataset_result = TestCaseCreateEdit.Insert_TestCaseDataSet(Conn, Test_Case_DataSet_Id, TC_Id)
        if test_case_dataset_result != 'Pass':
            # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)\
            msg = ("Returns from TestCaseCreateEdit Module by Failing to enter test case id %s" % Test_Case_DataSet_Id)
            print msg
            TestCaseCreateEdit.LogMessage(sModuleInfo, test_case_dataset_result, 3)
            return returnResult(test_case_dataset_result)

        # 4
        ##########Test Steps
        # Make sure test steps do no exist for the current TC_Id
        tmp_id = DB.GetData(Conn, "select step_id from test_steps where tc_id = '%s'" % TC_Id)
        if len(tmp_id) > 0:
            # We should be able to clean up test steps for this TC_Id
            # for now, just error out
            error = ("Test Steps existing already for the test case %s" % TC_Id)
            TestCaseCreateEdit.LogMessage(sModuleInfo, error, 2)
            # Here the test cases steps will be cleaned. We need to write a function there.
            # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
            # return returnResult("Test Case steps already exists for this test case")
            # Function for the cleaning the test steps will be here.
        # Insert Test Case Steps & Data
        test_case_steps_result = TestCaseCreateEdit.Insert_TestSteps_StepsData(Conn, TC_Id, Test_Case_DataSet_Id, Steps_Data_List)

        if test_case_steps_result != 'Pass':
            # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
            TestCaseCreateEdit.LogMessage(sModuleInfo, test_case_steps_result, 3)
            return returnResult(test_case_steps_result)

        # 5
        ##########Test Case Tags
        # Enter tags for the test case
        # Insert Test Case Tags
        test_case_tags_result = TestCaseCreateEdit.Insert_TestCase_Tags(Conn, TC_Id, Tag_List, Dependency_List, Priority, Associated_Bugs_List, Status, Section_Path, Feature_Path, Requirement_ID_List,Project_id,Team_id)

        if test_case_steps_result == "Pass":
            msg = "==========================================================================================================="
            TestCaseCreateEdit.LogMessage(sModuleInfo, msg, 1)
            return returnResult(TC_Id)
        else:
            # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
            error_message = "Tag is not added for the test case %s" % TC_Id
            TestCaseOperations.LogMessage(sModuleInfo, error_message, 2)
            msg = "==========================================================================================================="
            TestCaseOperations.LogMessage(sModuleInfo, msg, 1)
            return returnResult(test_case_tags_result)

    except Exception, e:
        print "Exception:", e
        TestCaseOperations.LogMessage(sModuleInfo, e, 2)
        # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
        Conn = GetConnection()
        return "Critical"

def ViewTestCase(TC_Id):
    def returnResult(string):
        json = simplejson.dumps(string)
        return HttpResponse(json, mimetype='application/json')

    try:
        TC_Id=TC_Id.GET.get('TC_Id')
        err_msg = ''
        # Search for TC_ID
        Conn = GetConnection()
        tmp_id = DB.GetData(Conn, "select tc_id from test_cases where tc_id = '%s'" % TC_Id)
        if len(tmp_id) > 0:
            # TestCaseOperations.LogMessage(sModuleInfo,"TEST CASE id is found:%s"%(TC_Id),4)

            # find all the details about test case
            Conn = GetConnection()
            test_case_details = DB.GetData(Conn, "select tc_name,tc_createdby from test_cases where tc_id = '%s'" % TC_Id, False)
            Conn.close()
            TC_Name = test_case_details[0][0]
            TC_Creator = test_case_details[0][1]
            
            # Test Case dataset details
            Conn = GetConnection()
            test_case_dataset_details = DB.GetData(Conn, "select tcdatasetid,data_type from test_case_datasets where tc_id = '%s'" % TC_Id, False)
            Conn.close()
            if len(test_case_dataset_details) > 0:
                Test_Case_DataSet_Id = test_case_dataset_details[0][0]
            else:
                Test_Case_DataSet_Id = ''

            Conn = GetConnection()
            test_case_tag_details = DB.GetData(Conn, "select name,property from test_case_tag where tc_id = '%s'" % TC_Id, False)
            Conn.close()
            TC_Project=[x[0] for x in test_case_tag_details if x[1] == 'Project']
            TC_Team=[x[0] for x in test_case_tag_details if x[1] == 'Team']
            query="select distinct property,array_to_string(array_agg(distinct name),',') from test_case_tag tct,dependency_management dm,dependency d where d.id=dm.dependency and tct.property=d.dependency_name and dm.project_id='%s' and dm.team_id=%d and tct.tc_id='%s'group by tct.property"%(TC_Project[0],int(TC_Team[0]),TC_Id)
            Conn = GetConnection()
            Dependency_List = DB.GetData(Conn,query,False)
            Conn.close()
            print Dependency_List
            Conn=GetConnection()
            query="select name from dependency_name dn,dependency_management dm where dn.dependency_id=dm.dependency and dm.project_id='%s' and dm.team_id=%d"%(TC_Project[0],int(TC_Team[0]))
            All_Names=DB.GetData(Conn,query)
            print All_Names
            Conn.close()
            temp_list=[]
            for each in Dependency_List:
                temp=[]
                for eachitem in each[1].split(","):
                    if eachitem in All_Names:
                        temp.append(eachitem)
                temp_list.append((each[0],temp))
            Dependency_List=temp_list
            print Dependency_List
            Tag_List = [x[0] for x in test_case_tag_details if x[1] == 'CustomTag']
            
            Priority_List = [x[0] for x in test_case_tag_details if x[1] == 'Priority']
            Priority = ''.join(Priority_List)
            Associated_Bugs_List = [x[0] for x in test_case_tag_details if x[1] == 'JiraId']
            Requirement_ID_List = [x[0] for x in test_case_tag_details if x[1] == 'PRDId']
            Status_List = [x[0] for x in test_case_tag_details if x[1] == 'Status']
            Status = ''.join(Status_List)
            print Status
            
            Section_Id = [x[0] for x in test_case_tag_details if x[1] == 'section_id']
            if len(Section_Id) > 0:
                Conn=GetConnection()
                Section_Path = DB.GetData(Conn, "select section_path from product_sections where section_id = '%d'" % int(Section_Id[0]), False)
                Conn.close()
                if len(Section_Path) > 0:
                    Section_Path = Section_Path[0][0]
                else:
                    Section_Path = ''
            else:
                Section_Path = ''
            
            Feature_Id = [x[0] for x in test_case_tag_details if x[1] == 'feature_id']
            if len(Feature_Id) > 0:
                Conn=GetConnection()
                Feature_Path = DB.GetData(Conn, "select feature_path from product_features where feature_id = '%d'" % int(Feature_Id[0]), False)
                Conn.close()
                if len(Feature_Path) > 0:
                    Feature_Path = Feature_Path[0][0]
                else:
                    Feature_Path = ''
            else:
                Feature_Path = ''

            
            query = "select distinct l.label_id,l.label_name,l.label_color from label_map blm, labels l where blm.id = '%s' and blm.type='TC' and blm.label_id = l.label_id" % TC_Id
            Conn = GetConnection()
            Labels = DB.GetData(Conn, query, False)
            Conn.close()
            
            # find all steps and data for the test case
            Steps_Data_List = []
            Conn=GetConnection()
            test_case_step_details = DB.GetData(Conn, "select ts.step_id,stepname,teststepsequence,data_required,steptype,step_editable from test_steps ts, test_steps_list tsl where ts.step_id = tsl.step_id and tc_id = '%s' order by teststepsequence" % TC_Id, False)
            Step_Iteration = 1
            for each_test_step in test_case_step_details:
                print "step %s - %s" % (Step_Iteration, each_test_step[1])
                Step_Id = each_test_step[0]
                Step_Name = each_test_step[1]
                Step_Seq = each_test_step[2]
                Step_Type = each_test_step[4]
                Step_Edit = each_test_step[5]
                Step_Data = []
                query = "select description from master_data where id Ilike '%s_s" % (TC_Id)
                query += "%s" % (str(Step_Iteration))
                query += "%' and field='step' and value='description'"
                # query="select description from master_data where id Ilike '%s_s%s%' and field='step' and value='description'" %(TC_Id,str(Step_Iteration))
                Step_Description = DB.GetData(Conn, query, False)
                if len(Step_Description) == 0:
                    step_description = ""
                else:
                    step_description = Step_Description[0][0]
                # print Step_Description[0][0]
                # select expected Result from the master data
                query = "select description from master_data where id Ilike '%s_s" % (TC_Id)
                query += "%s" % (str(Step_Iteration))
                query += "%' and field='expected' and value='result'"
                Step_Expected = DB.GetData(Conn, query, False)
                if len(Step_Expected) == 0:
                    step_expected = ""
                else:
                    step_expected = Step_Expected[0][0]
                # select verification point from master_data
                query = "select description from master_data where id Ilike '%s_s" % (TC_Id)
                query += "%s" % (str(Step_Iteration))
                query += "%' and field='verification' and value='point'"
                Step_Verified = DB.GetData(Conn, query, False)
                if len(Step_Verified) == 0:
                    step_verified = ""
                else:
                    step_verified = Step_Verified[0][0]
                query = "select description from test_steps_list where stepname='%s'" % (Step_Name.strip())
                Step_General_Description = DB.GetData(Conn, query, False)
                query = "select description from master_data where id Ilike '%s_s" % (TC_Id)
                query += "%s" % (str(Step_Iteration))
                query += "%' and field='estimated' and value='time'"
                Step_Time = DB.GetData(Conn, query, False)
                if len(Step_Time) == 0:
                    step_time = ""
                else:
                    step_time = Step_Time[0][0]
                # is data required for this step
                if each_test_step[3]:
                    # Is this a verify step
                    container_data_id_query = "select ctd.curname,ctd.newname from test_steps_data tsd, container_type_data ctd where tsd.testdatasetid = ctd.dataid and tcdatasetid = '%s' and teststepseq = %s and ctd.curname Ilike '%%_s%s%%'" % (Test_Case_DataSet_Id, Step_Seq, Step_Iteration)
                    Conn=GetConnection()
                    container_data_id_details = DB.GetData(Conn, container_data_id_query, False)
                    if Step_Edit:
                        for each_data_id in container_data_id_details:
                            if len(each_data_id) == 2:
                                From_Data = TestCaseCreateEdit.Get_PIM_Data_By_Id(Conn, each_data_id[0])
                                To_Data = TestCaseCreateEdit.Get_PIM_Data_By_Id(Conn, each_data_id[1])
                                Step_Data.append((From_Data, To_Data))
                    else:
                        # curname contains the data id
                        for each_data_id in container_data_id_details:
                            From_Data = TestCaseCreateEdit.Get_PIM_Data_By_Id(Conn, each_data_id[0])
                            Step_Data.append(From_Data)
                # append step name and data to send it back
                Steps_Data_List.append((Step_Name, Step_Data, Step_Type, step_description, step_expected, step_verified, Step_General_Description[0][0], step_time, Step_Edit, each_test_step[3]))
                Step_Iteration = Step_Iteration + 1
            # return values
            results = {'TC_Id':TC_Id, 'TC_Name': TC_Name, 'TC_Creator': TC_Creator, 'Tags List': Tag_List, 'Priority': Priority, 'Dependency List': Dependency_List, 'Associated Bugs': Associated_Bugs_List, 'Status': Status, 'Steps and Data':Steps_Data_List, 'Section_Path':Section_Path, 'Feature_Path':Feature_Path, 'Requirement Ids': Requirement_ID_List,'project_id':TC_Project,'team_id':TC_Team, 'Labels':Labels}

            json = simplejson.dumps(results)
            return HttpResponse(json, mimetype='application/json')

        else:
            err_msg = "TEST CASE id is not found:%s" % (TC_Id)
            return returnResult(err_msg)

    except Exception, e:
        err_msg = "TEST CASE search failed due to exception: %s" % (TC_Id)
        return returnResult(err_msg)

# def EditTestCase(TC_Id,Platform,Manual_TC_Id, TC_Name, TC_Creator, TC_Type,Tag_List,Dependency_List,Priority,Steps_Data_List,Associated_Bugs_List,Status):
def EditTestCase(request):
    def returnResult(string):
        json = simplejson.dumps(string)
        return HttpResponse(json, mimetype='application/json')

    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        Conn = GetConnection()
        err_msg = ''
        if request.is_ajax() and request.method == 'GET':
            TC_Id = request.GET.get(u'TC_Id', '')
            #Platform = request.GET.get(u'Platform', '')
            #Manual_TC_Id = request.GET.get(u'Manual_TC_Id', '')
            TC_Name = request.GET.get(u'TC_Name', '')
            TC_Creator = request.GET.get(u'TC_Creator', '')
            #TC_Type = request.GET.get(u'TC_Type', '')
            Tag_List = request.GET.get(u'Tag_List', '').split('|')
            Dependency_List = request.GET.get(u'Dependency_List', '').split('|')
            Priority = request.GET.get(u'Priority', '')
            temp = request.GET.get(u'Steps_Data_List', '').split('|')
            Steps_Name_List = request.GET.get(u'Steps_Name_List', '').split('|')
            Associated_Bugs_List = request.GET.get(u'Associated_Bugs_List', '')
            Requirement_ID_List = request.GET.get(u'Requirement_ID_List', '')
            Status = request.GET.get(u'Status', '')
            Step_Description_List = request.GET.get(u'Steps_Description_List', '')
            print Step_Description_List
            Step_Description_List = Step_Description_List.split('|')
            Step_Expected_Result = request.GET.get(u'Steps_Expected_List', '').split('|')
            Step_Verification_Point = request.GET.get(u'Steps_Verify_List', '').split('|')
            Steps_Time_List = request.GET.get(u'Steps_Time_List', '').split('|')
            Project_Id=request.GET.get(u'Project_Id','')
            Team_Id=request.GET.get(u'Team_Id','')
            labels=request.GET.get(u'labels','')       
            labels=labels.split("|")
            temp_list=[]
            for each in Dependency_List:
                temporary=each.split(":")
                temp_list.append((temporary[0],temporary[1].split(",")))
            Dependency_List=temp_list
            Steps_Data_List = TestCase_ParseData(temp, Steps_Name_List, Step_Description_List, Step_Expected_Result, Step_Verification_Point, Steps_Time_List)
            Section_Path = request.GET.get(u'Section_Path', '')
            Feature_Path = request.GET.get(u'Feature_Path', '')

        # LogMessage(sModuleInfo,"TEST CASE Edit START:%s"%(TC_Name),4)

        # 0
        ##########Data Validation: Check if all required input fields have data
        test_case_validation_result = TestCaseCreateEdit.TestCase_DataValidation(TC_Name, Priority, Tag_List, Dependency_List, Steps_Data_List, Section_Path, Feature_Path)
        if test_case_validation_result != "Pass":
            return returnResult(test_case_validation_result)

        # 1
        # Find if this is a new format test case created from web page or a manually created test case in backend
        # DeleteTestCaseData = False
        if '-' in TC_Id:
            """#this is a new format test case
            DeleteTestCaseData = True
            New_TC_Id = TC_Id
            #TestCaseOperations.Cleanup_TestCase(Conn, TC_Id, True, False, TC_Id)
            #if we are recreating a new format test case, then update details in test_case table
            test_cases_result = TestCaseOperations.Update_TestCaseDetails(Conn, New_TC_Id, TC_Name, TC_Creator)"""
            # #Test Case is existing.should be edited.
            # first update the test case name
            New_TC_Id = TC_Id
            if DB.IsDBConnectionGood(Conn) == False:
                time.sleep(1)
                Conn = GetConnection()
            test_cases_update_result = TestCaseCreateEdit.Update_TestCaseDetails(Conn, New_TC_Id, TC_Name, TC_Creator)
            if test_cases_update_result != "Pass":
                err_msg = "Test Case Detail is not updated successfully for test case %s" % New_TC_Id
                LogMessage(sModuleInfo, err_msg, 3)
                return err_msg
            labels_result = TestCaseCreateEdit.Insert_Linkings(Conn, TC_Id, TC_Name, labels)
            if labels_result != 'Pass':
                # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
                error = "Returns from TestCaseCreateEdit Module by Failing to enter labels for test case id %s" % TC_Id
                print error
                TestCaseCreateEdit.LogMessage(sModuleInfo, labels_result, 3)
                return returnResult(labels_result)
            
            # form the test case datasets
            test_case_datasets = '%sds' % New_TC_Id
            if DB.IsDBConnectionGood(Conn) == False:
                time.sleep(1)
                Conn = GetConnection()
            test_case_datasets_result = TestCaseCreateEdit.Update_Test_Case_Datasets(Conn, test_case_datasets, New_TC_Id)
            if test_case_datasets_result != "Pass":
                err_msg = "Test Case Datasets is not updated successfully for test case %s" % New_TC_Id
                LogMessage(sModuleInfo, err_msg, 3)
                return err_msg
            test_case_stepdata_result = TestCaseCreateEdit.Update_Test_Steps_Data(Conn, New_TC_Id, test_case_datasets, Steps_Data_List)
            if test_case_stepdata_result != "Pass":
                err_msg = "Test Case Step Data is not updated successfully for the test case %s" % New_TC_Id
                LogMessage(sModuleInfo, err_msg, 3)
                return err_msg
            test_case_tag_result = TestCaseCreateEdit.Update_Test_Case_Tag(Conn, TC_Id, Tag_List, Dependency_List, Priority, Associated_Bugs_List, Status, Section_Path,Feature_Path, Requirement_ID_List,Project_Id,Team_Id)
            if test_case_tag_result != "Pass":
                err_msg = "Test Case Step Data is not updated successfully for the test case %s" % New_TC_Id
                LogMessage(sModuleInfo, err_msg, 3)
                return err_msg
            if test_case_tag_result == "Pass":
                msg = "==========================================================================================================="
                TestCaseCreateEdit.LogMessage(sModuleInfo, msg, 1)
                return returnResult(New_TC_Id)
        
        else:
            # this is an old format test case
            tmp_id = DB.GetData(Conn, "select nextval('testcase_testcaseid_seq')")
            New_TC_Id = TestCaseOperations.Generate_TCId(Section_Path, tmp_id[0])
            test_cases_result = TestCaseOperations.Insert_TestCaseName(Conn, New_TC_Id, TC_Name, TC_Creator)
            # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id, True, True, New_TC_Id)
        msg = "==========================================================================================================="
        TestCaseCreateEdit.LogMessage(sModuleInfo, msg, 1)        
        return ViewTestCase(New_TC_Id)
        # 3
        # Recreate the new test case

        """if test_case_stepdata_result != 'Pass':
            #TestCaseOperations.Cleanup_TestCase(Conn, New_TC_Id)
            return test_case_stepdata_result
        """
        # GET_values = request.GET.copy()
        # GET_values['Is_Edit'] = New_TC_Id
        # request.GET = GET_values
        # return Create_Submit_New_TestCase(request)
        
    except Exception, e:
        print "Exception:", e
        msg = "==========================================================================================================="
        TestCaseCreateEdit.LogMessage(sModuleInfo, msg, 1)        
        # TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
        return "Critical"

def Documentation(request):
    templ = get_template('Documentation.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def Get_Sections(request):  #==================Returns Abailable User Name in List as user Type on Run Test Page==============================

    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        section = request.GET.get(u'section', '')
        project_id=request.GET.get(u'project_id','')
        team_id=request.GET.get(u'team_id','')
        if section == '':
            query="select distinct subltree(section_path,0,1) from team_wise_settings tws,product_sections ps where ps.section_id=tws.parameters and tws.type='Section' and tws.project_id='%s' and tws.team_id=%d"%(project_id,int(team_id))
            results = DB.GetData(Conn, query, False)
            levelnumber = 0
        else:
            levelnumber = section.count('.') + 1
            query="select distinct subltree(section_path,%d,%d) from team_wise_settings tws,product_sections ps where ps.section_id=tws.parameters and tws.type='Section' and tws.project_id='%s' and tws.team_id=%d and section_path~'*.%s.*' and nlevel(section_path)>%d"%(int(levelnumber),int(levelnumber+1),project_id,int(team_id),section,int(levelnumber))
            results = DB.GetData(Conn, query, False)

    results.insert(0, (str(levelnumber),))
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_SubSections(request):  #==================Returns Abailable User Name in List as user Type on Run Test Page==============================

    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        section = request.GET.get(u'section', '')
        if section == '':
            results = DB.GetData(Conn, "select distinct subpath(section_path,0,2) from product_sections", False)
            levelnumber = 0
        else:
            levelnumber = section.count('.') + 1
            results = DB.GetData(Conn, "select distinct subltree(section_path,0,2) FROM product_sections WHERE section_path ~ '*.%s.*' and nlevel(section_path) > 1" % (section), False)

    results.insert(0, (str(levelnumber),))
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def Get_Features(request):  #==================Returns Abailable User Name in List as user Type on Run Test Page==============================

    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        feature = request.GET.get(u'feature', '')
        project_id=request.GET.get(u'project_id','')
        team_id=request.GET.get(u'team_id','')
        if feature == '':
            query="select distinct subltree(feature_path,0,1) from team_wise_settings tws,product_features ps where ps.feature_id=tws.parameters and tws.type='Feature' and tws.project_id='%s' and tws.team_id=%d"%(project_id,int(team_id))
            #query = "select distinct subltree(feature_path,0,1) from product_features"
            results = DB.GetData(Conn, query, False)
            levelnumber = 0
        else:
            levelnumber = feature.count('.') + 1
            
            query="select distinct subltree(feature_path,%d,%d) from team_wise_settings tws,product_features ps where ps.feature_id=tws.parameters and tws.type='Feature' and tws.project_id='%s' and tws.team_id=%d and feature_path~'*.%s.*' and nlevel(feature_path)>%d"%(int(levelnumber),int(levelnumber+1),project_id,int(team_id),feature,int(levelnumber))
            #query = "select distinct subltree(feature_path,0,1) from product_features"
            results = DB.GetData(Conn, query, False)

    results.insert(0, (str(levelnumber),))
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_SubFeatures(request):  #==================Returns Abailable User Name in List as user Type on Run Test Page==============================

    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        feature = request.GET.get(u'feature', '')
        if feature == '':
            results = DB.GetData(Conn, "select distinct subpath(feature_path,0,2) from product_features", False)
            levelnumber = 0
        else:
            levelnumber = feature.count('.') + 1
            results = DB.GetData(Conn, "select distinct subltree(feature_path,0,2) FROM product_features WHERE feature_path ~ '*.%s.*' and nlevel(feature_path) > 1" % (feature), False)

    results.insert(0, (str(levelnumber),))
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')




def Get_Browsers(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        browser = request.GET.get(u'browser', '')
        project_id=request.GET.get(u'project_id','')
        team_id=request.GET.get(u'team_id','')
        if browser == '':
            query="select c.value from team_wise_settings tws,config_values c where c.id=tws.parameters and c.type=tws.type and c.type='Browser' and tws.project_id='%s' and tws.team_id=%d"%(project_id,int(team_id))
            results = DB.GetData(Conn, query, False)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Go_TestCaseID(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        runid = request.GET.get(u'runid', '')
        tcid = request.GET.get(u'tcid', '')
        go = request.GET.get(u'go', '')
        cases = DB.GetData(Conn, "select tc_id from test_case_results where run_id='" + runid + "' order by id", False)

    for c in cases:
        if c[0] == tcid:
            indx = cases.index(c)
            
    if go == 'previous' and indx > 0:
        results.append(cases[indx - 1])
    if go == 'next' and len(cases) > indx + 1:
        results.append(cases[indx + 1])

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Go_TestCaseStatus(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        runid = request.GET.get(u'runid', '')
        tcid = request.GET.get(u'tcid', '')
        cases = DB.GetData(Conn, "select tc_id from test_case_results where run_id='" + runid + "' order by id", False)

    for c in cases:
        if c[0] == tcid:
            indx = cases.index(c)
            
    results.append(indx + 1)
    total = len(cases)
    results.append(total)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Auto_Step_Create(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        step = request.GET.get(u'step', '')
        if step != '':
            results = DB.GetData(Conn, "select count(stepname) from test_steps_list where stepname =  '" + step + "'")

    if results[0] == 0:
        dbtest = DB.InsertNewRecordInToTable(Conn, "test_steps_list", stepname=step, description=step, driver='WebDriver', steptype='manual', data_required='false', stepfeature='Common', stepenable='true', step_editable='true', case_desc=step, expected=step, verify_point='false', step_continue='false', estd_time='59')

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def Get_Users(request):
    Conn = GetConnection()
    results = []
    userExists = False
    # if request.is_ajax():
    if request.method == "GET":
        username = request.GET.get(u'user', '').strip()
        password = request.GET.get(u'pwd', '').strip()
        # if username=='':        
        query="select user_id,full_name,user_level from user_info usr,permitted_user_list pul where pul.user_names = usr.full_name and pul.user_level in('manager','assigned_tester','admin') and usr.username='%s' and usr.password='%s'"%(username,password)
        results = DB.GetData(Conn,query,False)
    if len(results) > 0:
        message = results[0]
        Dict={'message':message}
        query="select default_project,default_team, cv.value from default_choice dc,config_values cv where dc.user_id='%s' and dc.default_team=cv.id"%results[0][0]
        testConnection(Conn)
        default_choice=DB.GetData(Conn,query,False)
        if isinstance(default_choice,list) and len(default_choice)==1:
            Dict.update({
                'project_id':default_choice[0][0],
                'team_id':default_choice[0][1],
                'team_name':default_choice[0][2]
            })
        else:
            Dict.update({
                'project_id':"",
                'team_id':"",
                'team_name':""
            })
    else:

        does_user_exists = []
        query="select user_id,full_name from user_info usr,permitted_user_list pul where pul.user_names = usr.full_name and pul.user_level in('manager','assigned_tester') and usr.username='%s'"%(username)
        does_user_exists = DB.GetData(Conn,query,False)
        if len  (does_user_exists) > 0:
            message = "Incorrect Password"
        else:
            message = "User Not Found!"
        Dict={'message':message}

    
    #get the default_team and project id

    json = simplejson.dumps(Dict)
    return HttpResponse(json, mimetype='application/json')

def Get_RunTypes(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        runtype = request.GET.get(u'run_type', '')
        if runtype == '':
            results = DB.GetData(Conn, "select distinct run_type from test_run_env", False)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Testers(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        tester = request.GET.get(u'tester', '')
        if tester == '':
            results = DB.GetData(Conn, "select distinct assigned_tester from test_run_env", False)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Status(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        status = request.GET.get(u'status', '')
        if status == '':
            results = DB.GetData(Conn, "select distinct status from test_run_env", False)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Versions(request):
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        ver = request.GET.get(u'term', '')
        if ver == '':
            versions = DB.GetData(Conn, "select distinct product_version from test_run_env order by product_version", False)
        else:
            versions = DB.GetData(Conn, "select distinct product_version from test_run_env where product_version='" + ver + "' order by product_version", False)
        
        flag1 = 0
        flag2 = 0
        flag3 = 0
        for i in versions:
            if i[0] == '':
                flag1 = 1
            elif i[0] == ' ':
                flag3 = 3
            elif i[0] == None:
                flag2 = 1  # 2
            else:
                results.append(i)
        if flag1 == 1:
            Nil = ['Nil']
            results.append(Nil)
        if flag2 == 2:
            Nil = ['Nil(None)']
            results.append(Nil)
        if flag3 == 3:
            Nil = ['Nil(Space)']
            results.append(Nil)
            

    json = simplejson.dumps(tuple(results))
    return HttpResponse(json, mimetype='application/json')

def BundleReport_Table(request):
    
    env_details = []
    ReportTable = []
    sections = []
    passed_cases = []

    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            version = request.GET.get(u'Product_Version', '')
            if version == 'Nil':
                version = ''
            elif version == 'Nil(None)':
                version = None
            elif version == 'Nil(Space)':
                version = ' '
            platform = request.GET.get(u'Platform', '')
            if platform == 'PC':
                OSName = 'Win'
            else:
                OSName = 'Darwin'
            os_query = "select distinct machine_os from test_run_env where machine_os ~ '" + OSName + ".*' and product_version = '" + version + "' order by machine_os"
            browser_query = "select distinct client from test_run_env where machine_os ~ '" + OSName + ".*' and product_version = '" + version + "' order by client"
            section_query = "select distinct subpath(section_path,0,1) from product_sections"
            sect_sub_q = "select ps.section_path from product_sections ps, result_test_case_tag rtct where ps.section_id::text = rtct.name and rtct.property='section_id' group by ps.section_path order by ps.section_path"
            
            feature_query = "select distinct subpath(feature_path,0,1) from product_features"
            feat_sub_q = "select ps.feature_path from product_features ps, result_test_case_tag rtct where ps.feature_id::text = rtct.name and rtct.property='feature_id' group by ps.feature_path order by ps.feature_path"

            
            OS_client_query = "select distinct machine_os,client from test_run_env where machine_os ~ '" + OSName + ".*' and product_version = '" + version + "' order by machine_os"
            OS = DB.GetData(Conn, os_query, False)
            browsers = DB.GetData(Conn, browser_query, False)
            env_details = DB.GetData(Conn, OS_client_query, False)
            sections = DB.GetData(Conn, sect_sub_q, False)
            features = DB.GetData(Conn, feat_sub_q, False)
            # env_details.append("Total")
            # Total = ["Total"]
            # sections.append(Total)
            
    """for each in OS:
        for item in browsers:
            temp = []
            temp.append(each[0])
            temp.append(item[0])
            env_details.append(tuple(temp))"""
    for i in env_details:
        # CountPerSection(sections,sel_cases,ReportTable)
        Data = []
        for s in sections:
            temp = []
            temp.append(s[0])
            # selected_cases_q = "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os like '"+i[0]+"%' and tre.product_version='"+i[1]+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and tcr.status = 'Passed'"
            passed_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tcr.status = 'Passed'" , False)
            pass_count = len(passed_cases)
            temp.append(pass_count)
            failed_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tcr.status = 'Failed'" , False)
            same = 0
            for j in failed_cases:
                for k in passed_cases:
                    if j[0] == k[0]:
                        same = same + 1
            fail_count = len(failed_cases)
            temp.append(fail_count - same)
            blocked_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tcr.status = 'Blocked'" , False)
            same1 = 0
            for j in blocked_cases:
                for k in passed_cases:
                    if j[0] == k[0]:
                        same1 = same1 + 1
                for h in failed_cases:
                    if j[0] == h[0]:
                        same1 = same1 + 1                        
            block_count = len(blocked_cases)
            temp.append(block_count - same1)
            notrun_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and (tcr.status = 'In-Progress' or tcr.status = 'Skipped' or tcr.status = 'Submitted')" , False)
            notrun_count = len(notrun_cases)
            temp.append(notrun_count)
            defected_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tct.property = 'JiraId' and tct.name != ''" , False)
            defect_count = len(defected_cases)
            temp.append(defect_count)
            temp.append(pass_count + fail_count - same + block_count - same1 + notrun_count + defect_count)
            
            Data.append(tuple(temp))
        sum = []
        Total = ["Total"]
        sum.append(Total)
        for y in range(1, len(temp)):
            huda = 0
            for z in range(len(sections)):
                huda = huda + Data[z][y]
            sum.append(huda)
        Data.append(sum)
        ReportTable.append(tuple(Data))
      
                    
    Heading = ['Section', 'Passed', 'Failed', 'Blocked', 'Not run', 'Defected', 'Total']
    results = {'Heading':Heading, 'Env':env_details, 'ReportTable':ReportTable}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def BundleReport_Table_Latest(request):
    
    env_details = []
    ReportTable = []
    sections = []
    passed_cases = []

    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            version = request.GET.get(u'Product_Version', '')
            if version == 'Nil':
                version = ''
            elif version == 'Nil(None)':
                version = None
            elif version == 'Nil(Space)':
                version = ' '
            platform = request.GET.get(u'Platform', '')
            if platform == 'PC':
                OSName = 'Win'
            else:
                OSName = 'Darwin'
            os_query = "select distinct machine_os from test_run_env where machine_os ~ '" + OSName + ".*' and product_version = '" + version + "' order by machine_os"
            browser_query = "select distinct client from test_run_env where machine_os ~ '" + OSName + ".*' and product_version = '" + version + "' order by client"
            section_query = "select distinct subpath(section_path,0,1) from product_sections"
            sect_sub_q = "select ps.section_path from product_sections ps, result_test_case_tag rtct where ps.section_id::text = rtct.name and rtct.property='section_id' group by ps.section_path order by ps.section_path"
            OS_client_query = "select distinct machine_os,client from test_run_env where machine_os ~ '" + OSName + ".*' and product_version = '" + version + "' order by machine_os"
            OS = DB.GetData(Conn, os_query, False)
            browsers = DB.GetData(Conn, browser_query, False)
            env_details = DB.GetData(Conn, OS_client_query, False)
            sections = DB.GetData(Conn, sect_sub_q, False)
            ready_cases = DB.GetData(Conn, "select * from result_test_case_tag where name='Status' and property='Ready'", False)
            ready_cases_fresh = DB.GetData(Conn, "select * from test_case_tag where name='Status' and property='Ready'", False)
            # env_details.append("Total")
            # Total = ["Total"]
            # sections.append(Total)
            
    """for each in OS:
        for item in browsers:
            temp = []
            temp.append(each[0])
            temp.append(item[0])
            env_details.append(tuple(temp))"""
            
        
    for i in env_details:
        # CountPerSection(sections,sel_cases,ReportTable)
        Data = []
        for s in sections:
            temp = []
            temp.append(s[0])
            latest_cases = DB.GetData(Conn, "select tcr.tc_id,tcr.status,tcr.teststarttime from test_case_results tcr,test_run_env tre where tcr.run_id=tre.run_id and tre.product_version='" + version + "' and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' order by tcr.teststarttime desc", False)
            # selected_cases_q = "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os like '"+i[0]+"%' and tre.product_version='"+i[1]+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and tcr.status = 'Passed'"
            passed_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tcr.status = 'Passed'" , False)
            pass_count = len(passed_cases)
            for m in passed_cases:
                for o in ready_cases:
                    if m[0] == o[0]:
                        for n in latest_cases:
                            if m[0] == n[0]:
                                if n[1] == 'Passed':
                                    break;
                                else:
                                    pass_count = pass_count - 1;
                                    break;
            temp.append(pass_count)
            failed_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tcr.status = 'Failed'" , False)
            """same = 0
            for j in failed_cases:
                for k in passed_cases:
                    if j[0]==k[0]:
                        same = same+1"""
            fail_count = len(failed_cases)
            for m in failed_cases:
                for o in ready_cases:
                    if m[0] == o[0]:
                        for n in latest_cases:
                            if m[0] == n[0]:
                                if n[1] == 'Failed':
                                    break;
                                else:
                                    fail_count = fail_count - 1;
                                    break;
            temp.append(fail_count)
            blocked_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tcr.status = 'Blocked'" , False)
            """same1 = 0
            for j in blocked_cases:
                for k in passed_cases:
                    if j[0]==k[0]:
                        same1 = same1 + 1
                for h in failed_cases:
                    if j[0]==h[0]:
                        same1 = same1 + 1"""                        
            block_count = len(blocked_cases)
            for m in blocked_cases:
                for o in ready_cases:
                    if m[0] == o[0]:
                        for n in latest_cases:
                            if m[0] == n[0]:
                                if n[1] == 'Blocked':
                                    break;
                                else:
                                    block_count = block_count - 1;
                                    break;
            temp.append(block_count)
            """notrun_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '"+i[0]+"' and tre.client = '"+i[1]+"' and tre.product_version = '"+version+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and (tcr.status = 'In-Progress' or tcr.status = 'Skipped' or tcr.status = 'Submitted')" , False)
            notrun_count = len(notrun_cases)
            temp.append(notrun_count)"""
            """defected_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '"+i[0]+"' and tre.client = '"+i[1]+"' and tre.product_version = '"+version+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and tct.property = 'JiraId' and tct.name != ''" , False)
            defect_count = len(defected_cases)
            temp.append(defect_count)
            temp.append(pass_count + fail_count - same + block_count - same1 + notrun_count + defect_count)"""
            submitted_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tcr.status = 'Submitted'" , False)
            submitted_count = len(submitted_cases)
            for m in submitted_cases:
                for o in ready_cases:
                    if m[0] == o[0]:
                        for n in latest_cases:
                            if m[0] == n[0]:
                                if n[1] == 'Submitted':
                                    break;
                                else:
                                    submitted_count = submitted_count - 1;
                                    break;
            temp.append(submitted_count)
            inprogress_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tcr.status = 'In-Progress'" , False)
            inprogress_count = len(inprogress_cases)
            for m in inprogress_cases:
                for o in ready_cases:
                    if m[0] == o[0]:
                        for n in latest_cases:
                            if m[0] == n[0]:
                                if n[1] == 'In-Progress':
                                    break;
                                else:
                                    inprogress_count = inprogress_count - 1;
                                    break;
            temp.append(inprogress_count)
            skipped_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, result_test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '" + i[0] + "' and tre.client = '" + i[1] + "' and tre.product_version = '" + version + "' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '" + s[0] + "' and tcr.status = 'Skipped'" , False)
            skipped_count = len(skipped_cases)
            for m in skipped_cases:
                for o in ready_cases:
                    if m[0] == o[0]:
                        for n in latest_cases:
                            if m[0] == n[0]:
                                if n[1] == 'Skipped':
                                    break;
                                else:
                                    skipped_count = skipped_count - 1;
                                    break;
            temp.append(skipped_count)
            env_cases = DB.GetData(Conn, "select distinct tc_id from test_case_tag where name='" + platform + "'", False)
            section_cases = DB.GetData(Conn, "select distinct tc_id from test_case_tag rtct, product_sections ps where rtct.property='section_id' and rtct.name::int = ps.section_id and ps.section_path = '" + s[0] + "'", False)
            if "FireFox" in i[1]:
                cquery = "select distinct tc_id from test_case_tag where property='FireFox'"
            if "Chrome" in i[1]:
                cquery = "select distinct tc_id from test_case_tag where property='Chrome'"
            if "IE" in i[1]:
                cquery = "select distinct tc_id from test_case_tag where property='IE'"
            if "Safari" in i[1]:
                cquery = "select distinct tc_id from test_case_tag where property='Safari'"
            browser_cases = DB.GetData(Conn, cquery, False)
            all_count = 0
            for a in env_cases:
                for o in ready_cases_fresh:
                    if a[0] == o[0]:
                        for b in section_cases:
                            if a[0] == b[0]:
                                for c in browser_cases:
                                    if a[0] == c[0]:
                                        all_count = all_count + 1
            run_count = pass_count + fail_count + block_count + submitted_count + inprogress_count + skipped_count
            if all_count > run_count:
                notrun_count = all_count - run_count
            else:
                notrun_count = 0
            temp.append(notrun_count)
            temp.append(run_count + notrun_count)
            
            Data.append(tuple(temp))
            
        sum = []
        Total = ["Total"]
        sum.append(Total)
        for y in range(1, len(temp)):
            huda = 0
            for z in range(len(sections)):
                huda = huda + Data[z][y]
            sum.append(huda)
        Data.append(sum)
        ReportTable.append(tuple(Data))
      
                    
    Heading = ['Section', 'Passed', 'Failed', 'Blocked', 'Submitted', 'In-Progress', 'Skipped', 'Not Run', 'Total']
    results = {'Heading':Heading, 'Env':env_details, 'ReportTable':ReportTable}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

"""def Single_Env(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            version = request.GET.get(u'Product_Version', '')
            platform = request.GET.get(u'Platform', '')
            if platform == 'PC':
                OSName = 'Win'
            else:
                OSName = 'Darwin'
            os_query = "select distinct machine_os from test_run_env where machine_os ~ '"+OSName+".*' and product_version = '"+version+"' order by machine_os"
            browser_query = "select distinct client from test_run_env where machine_os ~ '"+OSName+".*' and product_version = '"+version+"' order by client"
            section_query = "select distinct subpath(section_path,0,1) from product_sections"
            sect_sub_q = "select product_sections.section_path from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path"
            OS_client_query = "select distinct machine_os,client from test_run_env where machine_os ~ '"+OSName+".*' and product_version = '"+version+"' order by machine_os"
            OS = DB.GetData(Conn, os_query, False)
            browsers = DB.GetData(Conn, browser_query, False)
            env_details = DB.GetData(Conn, OS_client_query, False)
            sections = DB.GetData(Conn, sect_sub_q, False)
    
    Heading = ['Section','Passed','Failed','Blocked','Not run','Defected','Total']
    results = {'Heading':Heading}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')"""

def Bundle_Report(request):  #==================Returns Report data for a specific product version (eg 1.1.1.26 and platform 'PC'==============================

    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        Prod_Version = request.GET.get(u'Product_Version', '')
        PlatformName = request.GET.get(u'Platform', '')
        if PlatformName == 'PC':
            OSName = 'Win'
        else:
            OSName = 'Darwin'

            QueryResult = DB.GetData(Conn, "select f.path1 as path,f.status,count(*) from ("
                                            " select * from"
                                            " (select ps.section_path as path1 ,tct.tc_id as tcid1"
                                            " from test_case_tag tct, product_sections ps"
                                            " where tct.name = cast(ps.section_id as character varying) and tct.property = 'section_id' and tct.tc_id in ("
                                            " select tct.tc_id"
                                            " from test_case_tag tct"
                                            " group by tct.tc_id"
                                            " HAVING"
                                            " COUNT(CASE WHEN property = 'Ready' THEN 1 END) > 0"
                                            " AND COUNT(CASE WHEN property = 'machine_os' and name = '%s' THEN 1 END) > 0)"
                                            " group by ps.section_path,tct.tc_id"
                                            " ) as a1"
                                            " left outer join"
                                            " ("
                                            " select * from"
                                             " ("
                                             " select a1.tc_id,a1.status from"
                                             " ("
                                              " select distinct on (tcr.tc_id,tre.client,tre.machine_os) tcr.id,tcr.tc_id,tre.client,tre.machine_os,tre.run_id,tcr.status,tcr.teststarttime"
                                              " from test_case_results tcr,test_run_env tre"
                                              " where tcr.run_id = tre.run_id and split_part(split_part(tre.product_version, E',',1),E':',2) = '%s' and tre.machine_os ilike '%s%%'"
                                              " order by tcr.tc_id,tre.client,tre.machine_os,tcr.teststarttime desc"
                                              " ) as a1"
                                              " group by a1.tc_id,a1.status"
                                              " having"
                                              " count(case when status <> 'In-Progress' Then 1 end) > 0"
                                              " order by a1.tc_id"
                                              " ) as b1 where b1.status = 'Passed' and not exists"
                                              " ("
                                              " select * from (select a1.tc_id,a1.status from"
                                              " ("
                                              " select distinct on (tcr.tc_id,tre.client,tre.machine_os) tcr.id,tcr.tc_id,tre.client,tre.machine_os,tre.run_id,tcr.status,tcr.teststarttime"
                                              " from test_case_results tcr,test_run_env tre"
                                              " where tcr.run_id = tre.run_id and split_part(split_part(tre.product_version, E',',1),E':',2) = '%s' and tre.machine_os ilike '%s%%'"
                                              " order by tcr.tc_id,tre.client,tre.machine_os,tcr.teststarttime desc"
                                              " ) as a1"
                                              " group by a1.tc_id,a1.status"
                                              " having"
                                              " count(case when status <> 'In-Progress' Then 1 end) > 0"
                                              " order by a1.tc_id) as b2 where b2.tc_id = b1.tc_id and b2.status = 'Failed'"
                                              " )"
                                              " union all"
                                              " ("
                                              " select * from"
                                              " ("
                                              " select a1.tc_id,a1.status from"
                                              " ("
                                              " select distinct on (tcr.tc_id,tre.client,tre.machine_os) tcr.id,tcr.tc_id,tre.client,tre.machine_os,tre.run_id,tcr.status,tcr.teststarttime"
                                              " from test_case_results tcr,test_run_env tre"
                                              " where tcr.run_id = tre.run_id and split_part(split_part(tre.product_version, E',',1),E':',2) = '%s' and tre.machine_os ilike '%s%%'"
                                              " order by tcr.tc_id,tre.client,tre.machine_os,tcr.teststarttime desc"
                                              " ) as a1"
                                              " group by a1.tc_id,a1.status"
                                              " having"
                                              " count(case when status <> 'In-Progress' Then 1 end) > 0"
                                              " order by a1.tc_id"
                                              " ) as b1 where b1.status = 'Failed'"
                                              " )"
                                              " order by tc_id"
                                            " ) as a2"
                                            " on (a1.tcid1 = a2.tc_id)"
                                            " ) as f"
                                            " group by f.path1,f.status"
                                            " order by f.path1" % (PlatformName, Prod_Version, OSName, Prod_Version, OSName, Prod_Version, OSName), False)


            DefectsResult = DB.GetData(Conn, "select path2,tct2.name as defect from ("
                                            " select ps.section_path as path2 ,tct.tc_id as tcid2"
                                            " from test_case_tag tct, product_sections ps,test_case_results tcr,test_run_env tre"
                                            " where tct.name = cast(ps.section_id as character varying) and tct.property = 'section_id' and tct.tc_id in ("
                                            " select tct.tc_id"
                                            " from test_case_tag tct"
                                            " group by tct.tc_id"
                                            " HAVING"
                                            " COUNT(CASE WHEN property = 'Ready' THEN 1 END) > 0"
                                            " AND COUNT(CASE WHEN property = 'machine_os' and name = '%s' THEN 1 END) > 0)"
                                            " and tct.tc_id=tcr.tc_id and tcr.run_id = tre.run_id and split_part(split_part(tre.product_version, E',',1),E':',2) = '%s' and tre.machine_os ilike '%s%%'"
                                            " group by ps.section_path,tct.tc_id,tcr.status,tre.client"
                                            " order by ps.section_path,tct.tc_id"
                                            " ) as RunTestCases, test_case_tag as tct2"
                                            " where RunTestCases.tcid2 = tct2.tc_id and tct2.property = 'MKS'"
                                            " order by RunTestCases.path2" % (PlatformName, Prod_Version, OSName), False)

            SectionAllDefectsGroup = []
            SectionOpenDefectsGroup = []
            for key, group in itertools.groupby(DefectsResult, operator.itemgetter(0)):
                SectionAllDefectsGroup.append(list(group))

            for eachDataGroup in SectionAllDefectsGroup:
                DefectList = list(itertools.chain.from_iterable([x[1].split(',') for x in eachDataGroup]))
                # Call Jira api to get open defects list by passing all list
                OpenDefectList = DefectList

                # add the open defect count for this section to the Execution count results table
                QueryResult.append((eachDataGroup[0][0], 'Defects', len(OpenDefectList)))
                SectionOpenDefectsGroup.append((eachDataGroup[0][0], OpenDefectList))

            QueryResult.sort(cmp=None, key=operator.itemgetter(0), reverse=False)

            SectionDataGroup = []
            for key, group in itertools.groupby(QueryResult, operator.itemgetter(0)):
                SectionDataGroup.append(list(group))

            ReportTable = []
            for eachDataGroup in SectionDataGroup:
                SectionPath = eachDataGroup[0][0]
                # for eachtup in eachDataGroup:

                PassedList = [x[2] for x in eachDataGroup if x[1] == 'Passed']
                FailedList = [x[2] for x in eachDataGroup if x[1] == 'Failed']
                BlockedList = [x[2] for x in eachDataGroup if x[1] == 'Blocked']
                NoRunList = [x[2] for x in eachDataGroup if x[1] == None]
                DefectList = [x[2] for x in eachDataGroup if x[1] == 'Defects']

                if len(PassedList) > 0:
                    PassedCount = PassedList[0]
                else:
                    PassedCount = 0
                if len(FailedList) > 0:
                    FailedCount = FailedList[0]
                else:
                    FailedCount = 0
                if len(BlockedList) > 0:
                    BlockedCount = BlockedList[0]
                else:
                    BlockedCount = 0
                if len(NoRunList) > 0:
                    NoRunCount = NoRunList[0]
                else:
                    NoRunCount = 0
                if len(DefectList) > 0:
                    DefectCount = DefectList[0]
                else:
                    DefectCount = 0

                SectionList = SectionPath.split('.')
                for i in range(0, len(SectionList)):
                    if i == len(SectionList) - 1:
                        ReportTable.append((SectionList[i], PassedCount, FailedCount, BlockedCount, NoRunCount, DefectCount))
                    else:
                        ReportTable.append((SectionList[i], i))

            DefectTable = []
            for eachDataGroup in SectionOpenDefectsGroup:
                FormattedSectionName = eachDataGroup[0].replace('.', '-')
                pos = FormattedSectionName.rfind('-')
                FormattedSectionName = FormattedSectionName[:pos] + ' : ' + FormattedSectionName[pos + 1:]
                # Call jira api to get defect title by passing a list of jira ids
                DefectDetail = eachDataGroup[1]
                for eachDefect in DefectDetail:
                    # commenting till jira api is implemented
                    # DefectTable.append((eachDefect[0],eachDefect[1],FormattedSectionName))
                    DefectTable.append((eachDefect[0], FormattedSectionName))

    Heading = ['Section', 'Passed', 'Failed', 'Blocked', 'Never run', 'Total']
    results = {'Heading':Heading, 'ReportTable':ReportTable, 'DefectTable': DefectTable}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def BundleReport(request):
    templ = get_template('BundleReport.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def Admin(request):
    templ = get_template('Admin.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def FeaDri(request):
    templ = get_template('Feature_Driver.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def ManageStep(request):
    templ = get_template('ManageStep.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def Process_Git(request):
    # Conn = GetConnection()
    import GitApi
    # if request.is_ajax():
    if request.method == "GET":
        command = request.GET.get(u'command', '')
        if command == 'Pull':
            message = GitApi.pull_latest_git()
        elif command == 'Log':
            message = GitApi.git_log(-4)
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')

def DeleteExistingTestCase(TC_Ids):
    conn = GetConnection()
    is_string = False
    
    if type(TC_Ids) == type(u''):
        is_string = True
        Cleanup_TestCase(conn, TC_Ids)
        print is_string
        print "MESSAGE-----------------------------------------"
    else:
        for tc_id in TC_Ids:
            Cleanup_TestCase(conn, tc_id)
    
    
    t = get_template("DeletedExistingTestCase.html")
    c = Context({'is_string': is_string, 'tc_names': TC_Ids})
    output = t.render(c) 
    return HttpResponse(output)

"""Taitalus(shetu) changes"""
# Test Set and Tag Management section

def TestSet_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        data_type = request.GET.get(u'data_type', '')
        results = DB.GetData(Conn, "select  value,type from config_values where value Ilike '%" + value + "%' and type='" + data_type + "'", False)
        # test_tag=DB.GetData(Conn,"")
        # results=list(set(results+test_tag))
        # if len(results) > 0:
         #   results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestFeatureDriver_Auto(request):  # minar09
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        data_type = request.GET.get(u'data_type', '')
        results = DB.GetData(Conn, "select distinct value,type from config_values where value Ilike '%" + value + "%' and type='" + data_type + "'", False)
        # if len(results)>0:
            # results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestTag_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select tc_id from test_cases where tc_id in(select  tc_id from test_case_tag where property Ilike '%" + value + "%'")
        if len(results) > 0:
            results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestCase_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct tc_name from test_cases where tc_name Ilike '%" + value + "%'")
        if len(results) > 0:
            results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

"""def TestSet(request, message=""):
    return render_to_response('TestSet_Tag.html', {'error_message':message}, context_instance=RequestContext(request))

def Data_Process(request):
    # output="in the post processing page"
    if request.method == 'POST':
        data_type = request.POST['type']
        operation = request.POST['operation']
        command = request.POST['submit_button']
        first_name = request.POST['inputName']
        second_name = request.POST['inputName2']
        if data_type == "tag":
            return general_work(request, data_type)
        elif data_type == "set":
            return general_work(request, data_type)
        elif data_type == "":
            return TestSet(request, "data is not posted successfully")
        elif data_type != "" and (first_name == "" or operation == "" or second_name == "" or command == ""):
            return TestSet(request, "data is not posted successfully")
        else:
            return render_to_response('TestSet_Tag.html', {'error_message':"data is not posted successfully"}, context_instance=RequestContext(request))
    return TestSet(request, "data is not posted successfully")
def general_work(request, data_type):
    def Check_instance(x, data_type):
        if x in request.POST:
            name = request.POST[x]
            conn = GetConnection()
            result = DB.GetData(conn, "SELECT count(*) FROM config_values WHERE value='" + name + "' AND type='" + data_type + "'")
            return result[0]
        else:
            return -1
    temp = 0
    if request.method == 'POST':
        datatype = request.POST['type']
        operation = request.POST['operation']
        command = request.POST['submit_button']
        first_name = request.POST['inputName']
        second_name = request.POST['inputName2']
        if operation == "2"  and first_name != "" and second_name != "" and datatype != "":
            temp = Check_instance('inputName', data_type)
            if(temp == 0):
                if request.POST['inputName'] != "":
                    output = "no such test " + data_type + " with name '" + request.POST['inputName'] + "'"
                    return TestSet(request, output)
                else:
                    output = "Name field is empty"
                    return TestSet(request, output)
            if(temp > 0):
                if(first_name != "" and second_name != ""):
                    return rename(request, first_name, second_name, data_type)
                else:
                    output = "Name field is empty"
                    return TestSet(request, output)
        if operation == "1" and first_name != "" and second_name == "" and datatype != "":
            temp = Check_instance('inputName', data_type)
            if(temp == 0):
                name = request.POST['inputName']
                if(name != ""):
                    return create(request, name, data_type)
                else:
                    output = "Name field is empty"
                    return TestSet(request, output)
            if(temp > 0):
                output = "Test " + data_type + " with name '" + request.POST['inputName'] + "' is already in the database"
                return TestSet(request, output)
        if operation == "3" and first_name != "" and second_name == "" and datatype != "":
            temp = Check_instance('inputName', data_type)
            if(temp > 0):
                name = request.POST['inputName']
                if(name != ""):
                    return edit(request, name, data_type)
                else:
                    output = "Name field is empty"
            # output+=edit(name)
        if operation == "4" and first_name != "" and second_name == "" and datatype != "":
            temp = Check_instance('inputName', data_type)
            if(temp > 0):
                name = request.POST['inputName']
                if(name != ""):
                    return delete(request, name, data_type)
                else:
                    output = "Name field is empty"
                    TestSet(request, output)
            if(temp == 0):
                output = "No such test " + data_type + " with the name '" + request.POST['inputName'] + "'"
                return TestSet(request, output)
        if datatype == "":
            return TestSet(request, "data is not posted successfully")
            # output+=delete(name)
    # return output
def TestCases_InSet(name, data_type):
    conn = GetConnection()
    query = "select tc_id,tc_name from test_cases where tc_id in (select tc_id from test_case_tag where name='" + name + "' and property='" + data_type + "')"
    result = DB.GetData(conn, query, False)
    ex_tc_ids = []
    ex_tc_names = []
    for x in result:
        ex_tc_ids.append(x[0])
        ex_tc_names.append(x[1])
    ex_lst = [{'item1':t[0], 'item2':t[1]} for t in zip(ex_tc_ids, ex_tc_names)]
    conn.close()
    return ex_lst
def edit(request, name, data_type, error_message=""):
    output = {}
    ex_lst = TestCases_InSet(name, data_type)
    # Calculate the time for the test set
    time_required = 0
    Conn = GetConnection()
    # new_list=[]
    for each in ex_lst:
        query = "select count(*) from test_steps where tc_id='%s' group by tc_id" % each['item1']
        stepCount = DB.GetData(Conn, query)
        stepCount = int(stepCount[0])
        test_case_time = 0
        for count in range(1, stepCount + 1):
            temp_id = each['item1'] + '_s' + str(count)
            time_query = "select description from master_data where id='%s' and field='estimated' and value='time'" % temp_id
            time = DB.GetData(Conn, time_query)
            test_case_time += int(time[0])
            time_required += int(time[0])
        test_case_time = ConvertTime(test_case_time)
        each.update({'item3':test_case_time.strip()})
    formatTime = ConvertTime(time_required)
    print formatTime
    # ex_lst=new_list
    output.update({'name':name, 'data_type':data_type})
    output.update({'ex_lst':ex_lst, 'error_message':error_message, 'estimated_time':formatTime})
    return render_to_response('ManageTestSet.html', output, context_instance=RequestContext(request))

def rename(request, first, second, data_type):
    conn = GetConnection()
    if first != second and first != "" and second != "":
        query = "Where  value = '" + first + "' and type='" + data_type + "'"
        testrunenv = DB.UpdateRecordInTable(conn, "config_values", query, value=second)
        result = DB.GetData(conn, "SELECT count(*) FROM test_case_tag WHERE name='" + first + "'")
        if result[0] > 0:
            query = "Where name='" + first + "' and property='" + data_type + "'"
            testrunenv_2 = DB.UpdateRecordInTable(conn, "test_case_tag", query, name=second)
            if testrunenv_2 == True:
                query = ""
        conn.close()
        if testrunenv == True:
            return render_to_response('TestSet_Tag.html', {'error_message':"Old Test " + data_type + " name \"" + first + "\" is updated to \"" + second + "\""}, context_instance=RequestContext(request))
           
    return render_to_response('TestSet_Tag.html', {'error_message':"Check the input fields or Same name in both fields"}, context_instance=RequestContext(request))
    
def create(request, name, data_type):
    conn = GetConnection()
    testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", value=name, type=data_type)
    conn.close()
    if testrunenv == True:
        return render_to_response('TestSet_Tag.html', {'error_message':"Test " + data_type + " with name " + name + " is created successfully"}, context_instance=RequestContext(request))
    else:
        return render_to_response('TestSet_Tag.html', {'error_message':"Check the input fields"}, context_instance=RequestContext(request))
    

def delete(request, inputName, data_type):
    conn = GetConnection()
    testrunenv = DB.DeleteRecord(conn, "config_values", value=inputName, type=data_type)
    result = DB.GetData(conn, "SELECT count(*) FROM test_case_tag WHERE name='" + inputName + "'")
    if result[0] > 0:
        testrunenv_2 = DB.DeleteRecord(conn, "test_case_tag", name=inputName, property=data_type)
    conn.close()
    if testrunenv == True:
        return render_to_response('TestSet_Tag.html', {'error_message':"Test " + data_type + " name with \"" + inputName + "\" is deleted successfully."}, context_instance=RequestContext(request))

def AddTestCasesToSet(request):
    # output="in the add test case page"
    output = ""
    if request.method == 'POST':
        selected_tc = request.POST.getlist('selectTCAdd')
        test_set_name = request.POST['set_name']
        test_type = request.POST['set_type']
        if(len(selected_tc) == 0):
            ex_lst = TestCases_InSet(test_set_name, test_type)
            output = {}
            output.update({'ex_lst':ex_lst})
            output.update({'error_message':"No check box selected", 'name':test_set_name, 'data_type':test_type})
            return render_to_response('ManageTestSet.html', output, context_instance=RequestContext(request))
        else:
            conn = GetConnection()
            tc_cases = []
            available_tc = DB.GetData(conn, "SELECT tc_id FROM test_case_tag WHERE name='" + test_set_name + "'", False)
            for x in available_tc:
                tc_cases.append(x[0])
            count = 0
            for x in selected_tc:
                if x not in tc_cases:
                    testrunenv = DB.InsertNewRecordInToTable(conn, "test_case_tag", tc_id=x, name=test_set_name, property=test_type)
                    if testrunenv == True:
                        count += 1
            conn.close()
            if count == 0:
                    message = "No test cases are added to Test " + test_type + " '" + test_set_name + "'"
            if count > 0:
                message = str(count) + " test cases are added to Test " + test_type + " '" + test_set_name + "'," + str(len(selected_tc) - count) + " test cases are left"
            return edit(request, test_set_name, test_type, message)
    return edit(request, test_set_name, test_type, output)
    
def DeleteTestCasesFromSet(request):
    output = ""
    if request.method == 'POST':
        selected_tc = request.POST.getlist('selectTCremove')
        test_set_name = request.POST['set_name']
        test_type = request.POST['set_type']
        if(len(selected_tc) == 0):
            ex_lst = TestCases_InSet(test_set_name, test_type)
            output = {}
            output.update({'ex_lst':ex_lst})
            output.update({'error_message':"No check box selected", 'name':test_set_name, 'data_type':test_type})
            return render_to_response('ManageTestSet.html', output, context_instance=RequestContext(request))
        else:
            conn = GetConnection()
            count = 0
            for x in selected_tc:
                testrunenv = DB.DeleteRecord(conn, "test_case_tag", tc_id=x, name=test_set_name, property=test_type)
                if testrunenv == True:
                    count += 1
            conn.close()
            if count == 0:
                    message = "No test cases are deleted from Test " + test_type + " '" + test_set_name + "'"
            if count > 0:
                message = str(count) + " test cases are deleted from Test " + test_type + " '" + test_set_name + "'"
            return edit(request, test_set_name, test_type, message)
    return edit(request, test_set_name, test_type, output)
"""

# Test Step Management Section Functions
def TestStep_Delete(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select count(*) from test_steps where step_id=(select step_id from test_steps_list where stepname='" + value + "')")
        if(results[0] == 0):
            testrunenv = DB.DeleteRecord(Conn, "test_steps_list", stepname=value)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestFeature_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct value,type from config_values where value Ilike '%" + value + "%' and type='feature'", False)
        # if len(results)>0:
            # results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Feature(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        feature = request.GET.get(u'feature', '')
        if feature == '':
            results = DB.GetData(Conn, "select  distinct value from config_values where type='feature'", False)
        # if len(results)>0:
            # results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def ResultFilter(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select distinct assigned_tester from test_run_env", False)
        # if len(results)>0:
            # results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestDriver_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct value,type from config_values where value Ilike '%" + value + "%' and type='driver'", False)
        # if len(results)>0:
            # results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Driver(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        driver = request.GET.get(u'driver', '')
        if driver == '':
            results = DB.GetData(Conn, "select  distinct value from config_values where type='driver'", False)
        # if len(results)>0:
            # results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestStep_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct stepname,steptype from test_steps_list where stepname Ilike '%" + value + "%'", False)
        # if len(results)>0:
        #  results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

"""def Milestone_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        auto = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select value,type from config_values where type = 'milestone' and value Ilike '%" + auto + "%'",False)
        # if len(results)>0:
        #  results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def Milestone_Process(request):

    #if request.is_ajax():
    if request.method=='GET':
        operation=request.GET.get(u'operation','')
        input1=request.GET.get(u'inputName','')  

    Conn=GetConnection()
    if operation=='1':
        count = DB.GetData(Conn, "Select count(value) from config_values where type='milestone' and value="+input1+"")
        if (count[0]>0):
            test = DB.InsertNewRecordInToTable(Conn, 'config_values', type='milestone',value=input1)
            if test==True:
                message="Milestone '"+input1+"' is created."
            else:
                message="Milestone '"+input1+"' is not created."
    elif operation=='3':
        test = DB.DeleteRecord(Conn, 'config_values', type='milestone',value=input1)
        if test==True:
            message="Milestone '"+input1+"' is deleted."
        else:
            message="Milestone '"+input1+"' is not deleted."
    elif operation=='2':
        input2=request.GET.get(u'inputName2','')  
        test = DB.UpdateRecordInTable(Conn, 'config_values', "where type='milestone' and value="+input1+"", type='milestone', value=input2)
        if test==True:
                message="Milestone '"+input1+"' is updated to '"+input1+"'."
        else:
            message="Milestone '"+input1+"' is not updated."
    else:
        message="Input Fields are empty"
        
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
"""

def TestCase_Results(request):
    conn = GetConnection()
    TableData = []
    RefinedData = []
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Query', '')
            sQuery = "select tc_id,tc_name from test_cases where tc_id in (SELECT distinct tc_id FROM test_steps where step_id=(SELECT distinct step_id FROM test_steps_list WHERE stepname='" + UserData + "'))"
            TableData = DB.GetData(conn, sQuery, False)
            Check_TestCase(TableData, RefinedData)
    Heading = ['TestCase_ID', 'TestCase_Name', 'TestCase_Type']
    results = {'Heading':Heading, 'TableData':RefinedData}
    # results={'TableData':TableData}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestSteps_Results(request):
    conn = GetConnection()
    TableData = []
    # RefinedData=[]
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Query', '')
            sQuery = "select stepname from test_steps_list where stepFeature='" + UserData + "' or driver='" + UserData + "'" 
            TableData = DB.GetData(conn, sQuery, False)
            # Check_TestCase(TableData, RefinedData)
    Heading = ['TestStep_Name']
    results = {'Heading':Heading, 'TableData':TableData}
    # results={'TableData':TableData}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Check_TestCase(TableData, RefinedData):
    conn = GetConnection()
    test_type = [u'automated', u'manual', u'performance']
    type_selector = []
    query = "select tc_id from test_case_tag where name like '%Status%' and property='Forced'"
    forced = DB.GetData(conn, query, False)
    for each in TableData:
        type_selector = []
        data = []
        data.append(each[0])
        data.append(each[1])
        for item in test_type:
            sQuery = "select count(*) from test_steps_list where step_id in(select step_id from test_steps where tc_id='" + each[0] + "') and steptype='" + item + "'"
            result = DB.GetData(conn, sQuery, False)
            type_selector.append(result[0])
        # a = type_selector[0]
        b = type_selector[1]
        c = type_selector[2]
        if b[0] > 0L and c[0] == 0L:
            data.append(test_type[1])
            each = tuple(data)
            RefinedData.append(each)
        elif c[0] > 0L and b[0] == 0L:
            # print "performance"
            data.append(test_type[2])
            each = tuple(data)
            RefinedData.append(each)
        elif b[0] > 0L and c[0] > 0L:
            data.append(test_type[1])
            each = tuple(data)
            RefinedData.append(each)
        else:
            # print "automated"
            man = 0
            for f in forced:
                if f[0] == each[0]:
                    man = 1
            if man == 1:
                data.append(test_type[1])
            else:
                data.append(test_type[0])
            each = tuple(data)
            RefinedData.append(each)
            
def Populate_info_div(request):
    conn = GetConnection()
    if request.method == 'GET':
        value = request.GET.get(u'term', '')
        sQuery = "SELECT * from test_steps_list where stepname='" + value + "'"
    results = DB.GetData(conn, sQuery, False)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
def TestStepDelete(request):
    error_message = "Test Step is deleted successfully"
    return Manage_Step(request, error_message)
    # output={'error_message':error_message}
    # return render_to_response('ManageStep.html',error_message,context_instance=RequestContext(request))

def Manage_Step(request, error_message=""):
    """templ=get_template('TestStep.html')
    variables=Context({})
    output=templ.render(variables)
    return HttpResponse(output)"""
    output = {'error_message':error_message}
    return render_to_response('ManageStep.html', output, context_instance=RequestContext(request))

def TestStep(request, error_message=""):
    """templ=get_template('TestStep.html')
    variables=Context({})
    output=templ.render(variables)
    return HttpResponse(output)"""
    output = {'error_message':error_message}
    return render_to_response('TestStep.html', output, context_instance=RequestContext(request))

def CreateStep(request, error_message=""):
    """templ=get_template('TestStep.html')
    variables=Context({})
    output=templ.render(variables)
    return HttpResponse(output)"""
    output = {'error_message':error_message}
    return render_to_response('CreateStep.html', output, context_instance=RequestContext(request))

def Process_TestStep(request):
    output = "in the processing page"
    if request.method == 'POST':
        step_name = request.POST['step_name']
        step_desc = request.POST['step_desc']
        step_feature = request.POST['step_feature']
        step_data = request.POST['step_data']
        step_type = request.POST['step_type']
        step_driver = request.POST['step_driver'] 
        step_enable = request.POST['step_enable']
        if step_name != "" and step_desc != "" and step_feature != "" and step_data != "0" and step_enable != "0":
            if step_type != "0" and step_driver != "":
                conn = GetConnection()
                sQuery = "select count(*) from test_steps_list where stepname='" + step_name + "'"
                result = DB.GetData(conn, sQuery)
                if(result[0] > 0):
                    if(step_data == "1"):
                        data = "true"
                        edit_data = "false"
                    if(step_data == "3"):
                        data = "true"
                        edit_data = "true"
                    if(step_data == "2"):
                        data = "false"
                        edit_data = "false"
                    if(step_type == "1"):
                        s_type = "automated"
                    if(step_type == "2"):
                        s_type = "manual"
                    if(step_type == "3"):
                        s_type = "performance"
                    if(step_enable == "1"):
                        enable = "true"
                    if(step_enable == "2"):
                        enable = "false"
                    query = "Where  stepname = '" + step_name + "'"
                    testrunenv = DB.UpdateRecordInTable(conn, "test_steps_list", query, description=step_desc, data_required=data, steptype=s_type, driver=step_driver, stepfeature=step_feature, stepenable=enable, step_editable=edit_data)
                    query = "SELECT count(*) FROM config_values where type='feature' and value='" + step_feature + "'"
                    feature_count = DB.GetData(conn, query)
                    if(feature_count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type='feature', value=step_feature)
                    query = "SELECT count(*) FROM config_values where type='driver' and value='" + step_driver + "'"
                    driver_count = DB.GetData(conn, query)
                    if(driver_count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type='driver', value=step_driver)
                    if testrunenv == True:
                        message = "Test Step with name '" + step_name + "' is updated"
                        return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))
                    else:
                        message = "Test Step with name '" + step_name + "' is not updated.Please Try again"
                        return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))
                else:
                    if(step_data == "1"):
                        data = "true"
                        edit_data = "false"
                    if(step_data == "3"):
                        data = "true"
                        edit_data = "true"
                    if(step_data == "2"):
                        data = "false"
                        edit_data = "false"
                    if(step_type == "1"):
                        s_type = "automated"
                    if(step_type == "2"):
                        s_type = "manual"
                    if(step_type == "3"):
                        s_type = "performance"
                    if(step_enable == "1"):
                        enable = "true"
                    if(step_enable == "2"):
                        enable = "false"
                    
                    testrunenv = DB.InsertNewRecordInToTable(conn, "test_steps_list", stepname=step_name, description=step_desc, data_required=data, steptype=s_type, driver=step_driver, stepfeature=step_feature, stepenable=enable, step_editable=edit_data)
                    query = "SELECT count(*) FROM config_values where type='feature' and value='" + step_feature + "'"
                    feature_count = DB.GetData(conn, query)
                    if(feature_count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type='feature', value=step_feature)
                    query = "SELECT count(*) FROM config_values where type='driver' and value='" + step_driver + "'"
                    driver_count = DB.GetData(conn, query)
                    if(driver_count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type='driver', value=step_driver)
                    if testrunenv == True:
                        message = "Test Step with name '" + step_name + "' is created"
                        return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))
                    else:
                        message = "Test Step with name '" + step_name + "' is not created.Please Try again"
                        return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))         
            else:
                error_message = "Input Fields are empty.Check the input fields"
                error = {'error_message':error_message}
                return render_to_response('TestStep.html', error, context_instance=RequestContext(request))
        else:
                error_message = "Input Fields are empty.Check the input fields"
                error = {'error_message':error_message}
                return render_to_response('TestStep.html', error, context_instance=RequestContext(request))
    return HttpResponse(output)

def Process_CreateStep(request):
    output = "in the processing page"
    if request.method == 'POST':
        step_name = request.POST['step_name'].strip()
        step_desc = request.POST['step_desc'].strip()
        step_feature = request.POST['step_feature'].strip()
        step_data = request.POST['step_data'].strip()
        step_type = request.POST['step_type'].strip()
        step_driver = request.POST['step_driver'].strip()
        step_enable = request.POST['step_enable'].strip()
        case_desc = request.POST['case_desc'].strip()
        step_expect = request.POST['step_expect'].strip()
        verify_radio = request.POST['verify_radio'].strip()
        continue_radio = request.POST['continue_radio'].strip()
        step_time = request.POST['step_time'].strip()
        
        if step_name != "" and step_desc != "" and step_feature != "" and step_data != "0" and step_enable != "0" and case_desc != "" and step_expect != "" and step_time != "":
            if step_type != "0" and step_driver != "":
                conn = GetConnection()
                sQuery = "select count(*) from test_steps_list where stepname='" + step_name + "'"
                result = DB.GetData(conn, sQuery)
                if(result[0] > 0):
                    if(step_data == "1"):
                        data = "true"
                        edit_data = "false"
                    if(step_data == "3"):
                        data = "true"
                        edit_data = "true"
                    if(step_data == "2"):
                        data = "false"
                        edit_data = "false"
                    if(step_type == "1"):
                        s_type = "automated"
                    if(step_type == "2"):
                        s_type = "manual"
                    if(step_type == "3"):
                        s_type = "performance"
                    if(step_enable == "1"):
                        enable = "true"
                    if(step_enable == "2"):
                        enable = "false"
                    query = "Where  stepname = '" + step_name + "'"
                    testrunenv = DB.UpdateRecordInTable(conn, "test_steps_list", query, description=step_desc, data_required=data, steptype=s_type, driver=step_driver, stepfeature=step_feature, stepenable=enable, step_editable=edit_data, case_desc=case_desc, expected=step_expect, verify_point=verify_radio, step_continue=continue_radio, estd_time=step_time)
                    query = "SELECT count(*) FROM config_values where type='feature' and value='" + step_feature + "'"
                    feature_count = DB.GetData(conn, query)
                    if(feature_count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type='feature', value=step_feature)
                    query = "SELECT count(*) FROM config_values where type='driver' and value='" + step_driver + "'"
                    driver_count = DB.GetData(conn, query)
                    if(driver_count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type='driver', value=step_driver)
                    if testrunenv == True:
                        message = "Test Step with name '" + step_name + "' is updated"
                        return render_to_response('CreateStep.html', {'error_message':message}, context_instance=RequestContext(request))
                    else:
                        message = "Test Step with name '" + step_name + "' is not updated.Please Try again"
                        return render_to_response('CreateStep.html', {'error_message':message}, context_instance=RequestContext(request))
                else:
                    if(step_data == "1"):
                        data = "true"
                        edit_data = "false"
                    if(step_data == "3"):
                        data = "true"
                        edit_data = "true"
                    if(step_data == "2"):
                        data = "false"
                        edit_data = "false"
                    if(step_type == "1"):
                        s_type = "automated"
                    if(step_type == "2"):
                        s_type = "manual"
                    if(step_type == "3"):
                        s_type = "performance"
                    if(step_enable == "1"):
                        enable = "true"
                    if(step_enable == "2"):
                        enable = "false"
                    
                    testrunenv = DB.InsertNewRecordInToTable(conn, "test_steps_list", stepname=step_name, description=step_desc, data_required=data, steptype=s_type, driver=step_driver, stepfeature=step_feature, stepenable=enable, step_editable=edit_data, case_desc=case_desc, expected=step_expect, verify_point=verify_radio, step_continue=continue_radio, estd_time=step_time)
                    query = "SELECT count(*) FROM config_values where type='feature' and value='" + step_feature + "'"
                    feature_count = DB.GetData(conn, query)
                    if(feature_count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type='feature', value=step_feature)
                    query = "SELECT count(*) FROM config_values where type='driver' and value='" + step_driver + "'"
                    driver_count = DB.GetData(conn, query)
                    if(driver_count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type='driver', value=step_driver)
                    if testrunenv == True:
                        message = "Test Step with name '" + step_name + "' is created"
                        return render_to_response('CreateStep.html', {'error_message':message}, context_instance=RequestContext(request))
                    else:
                        message = "Test Step with name '" + step_name + "' is not created.Please Try again"
                        return render_to_response('CreateStep.html', {'error_message':message}, context_instance=RequestContext(request))         
            else:
                error_message = "Input Fields are empty.Check the input fields"
                error = {'error_message':error_message}
                return render_to_response('CreateStep.html', error, context_instance=RequestContext(request))
        else:
                error_message = "Input Fields are empty.Check the input fields"
                error = {'error_message':error_message}
                return render_to_response('CreateStep.html', error, context_instance=RequestContext(request))
    return HttpResponse(output)

def Process_FeatureDriver(request):  # minar09
    output = "in the processing page"
    if request.method == 'POST':
        data_type = request.POST['type']
        operation = request.POST['operation']
        input1 = request.POST['inputName']        
        if data_type != "" and operation != "" and input1 != "":
            if data_type != "0":
                conn = GetConnection()
                if operation == "1":                                       
                    query = "SELECT count(*) FROM config_values where type='" + data_type + "' and value='" + input1 + "'"
                    count = DB.GetData(conn, query)
                    if(count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type=data_type, value=input1)
                        if testrunenv == True:
                            message = "" + data_type + " with name '" + input1 + "' is created."
                            return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))
                        else:
                            message = "" + data_type + " with name '" + input1 + "' is not created. Please Try again."
                            return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request)) 
                    else:
                        message = "" + data_type + " with name '" + input1 + "' is already created."
                        return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))
                if operation == "2":
                    input2 = request.POST['inputName2']
                    if input2 == "":
                        error_message = "Input Fields are empty.Check the input fields"
                        error = {'error_message':error_message}
                        return render_to_response('TestStep.html', error, context_instance=RequestContext(request))
                    else:  
                        query = "SELECT count(*) FROM config_values where type='" + data_type + "' and value='" + input1 + "'"
                        count = DB.GetData(conn, query)
                        if(count[0] < 1):
                            message = "" + data_type + " with name '" + input1 + "' is not found."
                            return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))                            
                        else:
                            srquery = "SELECT count(*) FROM test_steps_list where driver='" + input1 + "' or stepfeature='" + input1 + "'"
                            searchCount = DB.GetData(conn, srquery)
                            if (searchCount[0] < 1):
                                whereQuery = "where type='" + data_type + "' and value = '" + input1 + "' "
                                testrunenv = DB.UpdateRecordInTable(conn, "config_values", whereQuery, value=input2, type=data_type) 
                                if testrunenv == True:
                                    message = "" + data_type + " with name '" + input1 + "' is updated to '" + input2 + "'."
                                    return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))
                                else:
                                    message = "" + data_type + " with name '" + input1 + "' is not updated. Please Try again."
                                return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))
                            else:  
                                whereQuery = "where type='" + data_type + "' and value = '" + input1 + "' "
                                testrunenv = DB.UpdateRecordInTable(conn, "config_values", whereQuery, value=input2, type=data_type)                                                                                                                    
                                whereQuery = "where driver='" + input1 + "'"
                                testrunenv1 = DB.UpdateRecordInTable(conn, "test_steps_list", whereQuery, driver=input2)
                                whereQuery = "where stepfeature='" + input1 + "'"
                                testrunenv2 = DB.UpdateRecordInTable(conn, "test_steps_list", whereQuery, stepfeature=input2)
                                if (testrunenv == True and testrunenv1 == True) or (testrunenv == True and testrunenv2 == True) or (testrunenv == True and testrunenv1 == True and testrunenv2 == True):
                                    message = "" + data_type + " with name '" + input1 + "' is updated to '" + input2 + "'."
                                    return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))
                                else:
                                    message = "" + data_type + " with name '" + input1 + "' is not updated. Please Try again."
                                    return render_to_response('TestStep.html', {'error_message':message}, context_instance=RequestContext(request))                             
                """if operation=="3":  
                    query="SELECT count(*) FROM config_values where type='"+data_type+"' and value='"+input1+"'"
                    count=DB.GetData(conn,query)
                    if(count[0]<1):
                        message=""+data_type+" with name '"+input1+"' is not found. Please Try again."
                        return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                    else:
                        srquery = "SELECT count(*) FROM test_steps_list where driver='"+input1+"' or stepfeature='"+input1+"'"
                        searchCount = DB.GetData(Conn, srquery)
                        if (searchCount[0]<1):
                            testrunenv=DB.DeleteRecord(conn, "config_values",type=data_type,value=input1)
                            if testrunenv==True:
                                message=""+data_type+" with name '"+input1+"' is deleted."
                                return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                            else:
                                message=""+data_type+" with name '"+input1+"' is not deleted. Please Try again."
                                return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))   
                        else:
                            message=""+data_type+" with name '"+input1+"' is being used by some test cases/steps. Please try another."
                            return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))   """                        
            else:
                error_message = "Input Fields are empty.Check the input fields"
                error = {'error_message':error_message}
                return render_to_response('TestStep.html', error, context_instance=RequestContext(request))
        else:
                error_message = "Input Fields are empty.Check the input fields"
                error = {'error_message':error_message}
                return render_to_response('TestStep.html', error, context_instance=RequestContext(request))
    return HttpResponse(output)

def FeatureDriverOperation(request):  # minar09
    if request.method == 'GET' and request.is_ajax():
        operation = request.GET.get[u'operation', '']
        data_type = request.GET.get[u'type', '']
        input1 = request.GET.get[u'inputName', '']       
        if data_type != "" and operation != "" and input1 != "":
            if data_type != "0":
                conn = GetConnection()
                if operation == "1":                                       
                    query = "SELECT count(*) FROM config_values where type='" + data_type + "' and value='" + input1 + "'"
                    count = DB.GetData(conn, query)
                    if(count[0] < 1):
                        testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", type=data_type, value=input1)
                        if testrunenv == True:
                            message = "" + data_type + " with name '" + input1 + "' is created."
                            # return render_to_response('Feature_Driver.html',{'error_message':message},context_instance=RequestContext(request))
                        else:
                            message = "" + data_type + " with name '" + input1 + "' is not created. Please Try again."
                            # return render_to_response('Feature_Driver.html',{'error_message':message},context_instance=RequestContext(request)) 
                    else:
                        message = "" + data_type + " with name '" + input1 + "' is already created."
                        # return render_to_response('Feature_Driver.html',{'error_message':message},context_instance=RequestContext(request))
                if operation == "2":
                    input2 = request.GET.get[u'inputName2', '']
                    if input2 == "":
                        error_message = "Input Fields are empty.Check the input fields"
                        # error={'error_message':error_message}
                        # return render_to_response('Feature_Driver.html',error,context_instance=RequestContext(request))
                    else:  
                        query = "SELECT count(*) FROM config_values where type='" + data_type + "' and value='" + input1 + "'"
                        count = DB.GetData(conn, query)
                        if(count[0] < 1):
                            message = "" + data_type + " with name '" + input1 + "' is not found."
                            # return render_to_response('Feature_Driver.html',{'error_message':message},context_instance=RequestContext(request))                            
                        else:
                            srquery = "SELECT count(*) FROM test_steps_list where driver='" + input1 + "' or stepfeature='" + input1 + "'"
                            searchCount = DB.GetData(conn, srquery)
                            if (searchCount[0] < 1):
                                whereQuery = "where type='" + data_type + "' and value = '" + input1 + "' "
                                testrunenv = DB.UpdateRecordInTable(conn, "config_values", whereQuery, value=input2, type=data_type) 
                                if testrunenv == True:
                                    message = "" + data_type + " with name '" + input1 + "' is updated to '" + input2 + "'."
                                    # return render_to_response('Feature_Driver.html',{'error_message':message},context_instance=RequestContext(request))
                                else:
                                    message = "" + data_type + " with name '" + input1 + "' is not updated. Please Try again."
                                # return render_to_response('Feature_Driver.html',{'error_message':message},context_instance=RequestContext(request))
                            else:  
                                whereQuery = "where type='" + data_type + "' and value = '" + input1 + "' "
                                testrunenv = DB.UpdateRecordInTable(conn, "config_values", whereQuery, value=input2, type=data_type)                                                                                                                    
                                whereQuery = "where driver='" + input1 + "'"
                                testrunenv1 = DB.UpdateRecordInTable(conn, "test_steps_list", whereQuery, driver=input2)
                                whereQuery = "where stepfeature='" + input1 + "'"
                                testrunenv2 = DB.UpdateRecordInTable(conn, "test_steps_list", whereQuery, stepfeature=input2)
                                if (testrunenv == True and testrunenv1 == True) or (testrunenv == True and testrunenv2 == True) or (testrunenv == True and testrunenv1 == True and testrunenv2 == True):
                                    message = "" + data_type + " with name '" + input1 + "' is updated to '" + input2 + "'."
                                    # return render_to_response('Feature_Driver.html',{'error_message':message},context_instance=RequestContext(request))
                                else:
                                    message = "" + data_type + " with name '" + input1 + "' is not updated. Please Try again."
                                    # return render_to_response('Feature_Driver.html',{'error_message':message},context_instance=RequestContext(request))                                                                    
            else:
                error_message = "Input Fields are empty.Check the input fields"
                # error={'error_message':error_message}
                # return render_to_response('Feature_Driver.html',error,context_instance=RequestContext(request))
        else:
                error_message = "Input Fields are empty.Check the input fields"
                # error={'error_message':error_message}
                # return render_to_response('Feature_Driver.html',error,context_instance=RequestContext(request))
    results = {'confirm_message':message,
             'error_message':error_message
             }
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
    
def FeatureDriver_Delete(request):  # minar09
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        data_type = request.GET.get(u'term', '')
        input1 = request.GET.get(u'inputName', '')
        results = DB.GetData(Conn, "select count(*) from test_steps_list where driver='" + input1 + "' or stepFeature='" + input1 + "'")
        if(results[0] == 0):
            testrunenv = DB.DeleteRecord(Conn, "config_values", type=data_type, value=input1)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def FeatureDriverDelete(request):  # minar09
    error_message = "Feature/Driver is deleted successfully"
    output = {'error_message':error_message}
    return render_to_response('TestStep.html', output, context_instance=RequestContext(request))

def TestTypeStatus_Report(request):  # minar09
    Conn = GetConnection()
    sections = []
    priority = ["P1", "P2", "P3", "P4", "Total"]
    testCases = []
    totalCases = []
    TableData = []
    manCount = []
    manP1Count = []
    manP2Count = []
    manP3Count = []
    manP4Count = []
    manIPCount = []
    manIPP1Count = []
    manIPP2Count = []
    manIPP3Count = []
    manIPP4Count = []
    autoCount = []
    autoP1Count = []
    autoP2Count = []
    autoP3Count = []
    autoP4Count = []
    autoIPCount = []
    autoIPP1Count = []
    autoIPP2Count = []
    autoIPP3Count = []
    autoIPP4Count = []
    perCount = []
    perP1Count = []
    perP2Count = []
    perP3Count = []
    perP4Count = []
    perIPCount = []
    perIPP1Count = []
    perIPP2Count = []
    perIPP3Count = []
    perIPP4Count = []
    Table = []
    Table1 = []
    Table2 = []
    Table3 = []
    Table4 = []
    Table5 = []
    Table6 = []
    manTab = []
    manP1Tab = []
    manP2Tab = []
    manP3Tab = []
    manP4Tab = []
    manIPTab = []
    manIPP1Tab = []
    manIPP2Tab = []
    manIPP3Tab = []
    manIPP4Tab = []
    autoTab = []
    autoP1Tab = []
    autoP2Tab = []
    autoP3Tab = []
    autoP4Tab = []
    autoIPTab = [] 
    autoIPP1Tab = []
    autoIPP2Tab = []
    autoIPP3Tab = []
    autoIPP4Tab = []
    perTab = []
    perP1Tab = []
    perP2Tab = []
    perP3Tab = []
    perP4Tab = []
    perIPTab = []
    perIPP1Tab = []
    perIPP2Tab = []
    perIPP3Tab = []
    perIPP4Tab = []
    RefinedData = []
    totalP1Count = []
    totalP2Count = []
    totalP3Count = []
    totalP4Count = []
    totalCount = []
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'choice', '')
            if " " in UserData:
                UserData = UserData.replace(' ', '_')
            if UserData == "All":
                sectionQuery = "select product_sections.section_path from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path"
                testCasesQuery = "select test_case_tag.tc_id, product_sections.section_path from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' group by test_case_tag.tc_id, product_sections.section_path"
                totalCaseQuery = "select count(test_case_tag.tc_id) from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path"
            else:
                sectionQuery = "select product_sections.section_path from product_sections,test_case_tag where product_sections.section_id::text = test_case_tag.name and product_sections.section_path ~ '" + UserData + ".*' and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path"
                testCasesQuery = "select test_case_tag.tc_id, product_sections.section_path from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' and product_sections.section_path ~ '" + UserData + ".*' group by test_case_tag.tc_id, product_sections.section_path"
                totalCaseQuery = "select count(test_case_tag.tc_id) from product_sections,test_case_tag where product_sections.section_id::text = test_case_tag.name and product_sections.section_path ~ '" + UserData + ".*' and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path" 
        sections = DB.GetData(Conn, sectionQuery, False)        
        totalCases = DB.GetData(Conn, totalCaseQuery, False)
        testCases = DB.GetData(Conn, testCasesQuery, False)
        progress = DB.GetData(Conn, "select tc_id from test_case_tag where property='Dev'", False)
        p1Priority = DB.GetData(Conn, "select tc_id from test_case_tag where property='Priority' and name='P1'", False)
        p2Priority = DB.GetData(Conn, "select tc_id from test_case_tag where property='Priority' and name='P2'", False)
        p3Priority = DB.GetData(Conn, "select tc_id from test_case_tag where property='Priority' and name='P3'", False)
        p4Priority = DB.GetData(Conn, "select tc_id from test_case_tag where property='Priority' and name='P4'", False)
        
    # sections.append('Summary Global')
    for each in sections:     
        for y in priority:
            data = []
            data.append(each[0].replace(".", "-"))
            data.append(y)
            Table.append(tuple(data))
            
    # Table = zip(sections,priority)
    Check_TestCase(testCases, RefinedData)
    # manual 
    for each in RefinedData:
        Data = []
        Data.append(each[0])
        Data.append(each[1])
        if each[2] == 'manual':
            this = True
            for x in progress:
                if x[0] == each[0]:
                    this = False
            if this == True:
                manTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0] == p1[0]:
                        manP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0] == p2[0]:
                        manP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0] == p3[0]:
                        manP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0] == p4[0]:
                        manP4Tab.append(tuple(Data))
            elif this == False:
                manIPTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0] == p1[0]:
                        manIPP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0] == p2[0]:
                        manIPP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0] == p3[0]:
                        manIPP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0] == p4[0]:
                        manIPP4Tab.append(tuple(Data))
        elif each[2] == 'automated':
            this = True
            for x in progress:
                if x[0] == each[0]:
                    this = False
            if this == True:
                autoTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0] == p1[0]:
                        autoP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0] == p2[0]:
                        autoP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0] == p3[0]:
                        autoP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0] == p4[0]:
                        autoP4Tab.append(tuple(Data))
            elif this == False:
                autoIPTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0] == p1[0]:
                        autoIPP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0] == p2[0]:
                        autoIPP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0] == p3[0]:
                        autoIPP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0] == p4[0]:
                        autoIPP4Tab.append(tuple(Data))
        elif each[2] == 'performance':
            this = True
            for x in progress:
                if x[0] == each[0]:
                    this = False
            if this == True:
                perTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0] == p1[0]:
                        perP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0] == p2[0]:
                        perP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0] == p3[0]:
                        perP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0] == p4[0]:
                        perP4Tab.append(tuple(Data))
            elif this == False:
                perIPTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0] == p1[0]:
                        perIPP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0] == p2[0]:
                        perIPP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0] == p3[0]:
                        perIPP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0] == p4[0]:
                        perIPP4Tab.append(tuple(Data))
                
    Count_Per_Section(manTab, sections, manCount)
    Count_Per_Section(manP1Tab, sections, manP1Count)
    Count_Per_Section(manP2Tab, sections, manP2Count)
    Count_Per_Section(manP3Tab, sections, manP3Count)
    Count_Per_Section(manP4Tab, sections, manP4Count)
    Count_Per_Section(manIPTab, sections, manIPCount) 
    Count_Per_Section(manIPP1Tab, sections, manIPP1Count)
    Count_Per_Section(manIPP2Tab, sections, manIPP2Count)
    Count_Per_Section(manIPP3Tab, sections, manIPP3Count)
    Count_Per_Section(manIPP4Tab, sections, manIPP4Count)
    Count_Per_Section(autoTab, sections, autoCount) 
    Count_Per_Section(autoP1Tab, sections, autoP1Count)
    Count_Per_Section(autoP2Tab, sections, autoP2Count)
    Count_Per_Section(autoP3Tab, sections, autoP3Count)
    Count_Per_Section(autoP4Tab, sections, autoP4Count)
    Count_Per_Section(autoIPTab, sections, autoIPCount)
    Count_Per_Section(autoIPP1Tab, sections, autoIPP1Count)
    Count_Per_Section(autoIPP2Tab, sections, autoIPP2Count)
    Count_Per_Section(autoIPP3Tab, sections, autoIPP3Count)
    Count_Per_Section(autoIPP4Tab, sections, autoIPP4Count)
    Count_Per_Section(perTab, sections, perCount) 
    Count_Per_Section(perP1Tab, sections, perP1Count)
    Count_Per_Section(perP2Tab, sections, perP2Count)
    Count_Per_Section(perP3Tab, sections, perP3Count)
    Count_Per_Section(perP4Tab, sections, perP4Count)
    Count_Per_Section(perIPTab, sections, perIPCount)
    Count_Per_Section(perIPP1Tab, sections, perIPP1Count)
    Count_Per_Section(perIPP2Tab, sections, perIPP2Count)
    Count_Per_Section(perIPP3Tab, sections, perIPP3Count)
    Count_Per_Section(perIPP4Tab, sections, perIPP4Count)
    Append_array(Table, manP1Count, manP2Count, manP3Count, manP4Count, manCount, Table1) 
    Append_array(Table1, manIPP1Count, manIPP2Count, manIPP3Count, manIPP4Count, manIPCount, Table2)
    Append_array(Table2, autoP1Count, autoP2Count, autoP3Count, autoP4Count, autoCount, Table3)
    Append_array(Table3, autoIPP1Count, autoIPP2Count, autoIPP3Count, autoIPP4Count, autoIPCount, Table4)
    Append_array(Table4, perP1Count, perP2Count, perP3Count, perP4Count, perCount, Table5)
    Append_array(Table5, perIPP1Count, perIPP2Count, perIPP3Count, perIPP4Count, perIPCount, Table6)
    # Append_array(Table4,totalCases,TableData)
    x = 1
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0   
    for each in Table6:
        data = []
        for y in each:
            data.append(y)
        if x == 1:
            count = manP1Count[a] + manIPP1Count[a] + autoP1Count[a] + autoIPP1Count[a] + perP1Count[a] + perIPP1Count[a]
            a = a + 1
            data.append(count)
            totalP1Count.append(count)
        elif x == 2:
            count = manP2Count[b] + manIPP2Count[b] + autoP2Count[b] + autoIPP2Count[b] + perP2Count[b] + perIPP2Count[b]
            b = b + 1
            data.append(count)
            totalP2Count.append(count)
        elif x == 3:
            count = manP3Count[c] + manIPP3Count[c] + autoP3Count[c] + autoIPP3Count[c] + perP3Count[c] + perIPP3Count[c]
            c = c + 1
            data.append(count)
            totalP3Count.append(count)
        elif x == 4:
            count = manP4Count[d] + manIPP4Count[d] + autoP4Count[d] + autoIPP4Count[d] + perP4Count[d] + perIPP4Count[d]
            d = d + 1
            data.append(count)
            totalP4Count.append(count)
        elif x == 5:
            count = manCount[e] + manIPCount[e] + autoCount[e] + autoIPCount[e] + perCount[e] + perIPCount[e]
            e = e + 1
            data.append(count)
            totalCount.append(count)
        TableData.append(tuple(data))
        if x == 5:
            x = 1
        elif x < 5:
            x = x + 1
    
    temp = []
    temp.append("Summary")
    temp.append("P1")
    manP1Sum = count_Sum(manP1Count)
    temp.append(manP1Sum)
    manIPP1Sum = count_Sum(manIPP1Count)
    temp.append(manIPP1Sum)
    autoP1Sum = count_Sum(autoP1Count)
    temp.append(autoP1Sum)
    autoIPP1Sum = count_Sum(autoIPP1Count)
    temp.append(autoIPP1Sum)
    perP1Sum = count_Sum(perP1Count)
    temp.append(perP1Sum)
    perIPP1Sum = count_Sum(perIPP1Count)
    temp.append(perIPP1Sum)
    totalP1Sum = count_Sum(totalP1Count)
    temp.append(totalP1Sum)
    TableData.append(tuple(temp))
    
    temp = []
    temp.append("Summary")
    temp.append("P2")
    manP2Sum = count_Sum(manP2Count)
    temp.append(manP2Sum)
    manIPP2Sum = count_Sum(manIPP2Count)
    temp.append(manIPP2Sum)
    autoP2Sum = count_Sum(autoP2Count)
    temp.append(autoP2Sum)
    autoIPP2Sum = count_Sum(autoIPP2Count)
    temp.append(autoIPP2Sum)
    perP2Sum = count_Sum(perP2Count)
    temp.append(perP2Sum)
    perIPP2Sum = count_Sum(perIPP2Count)
    temp.append(perIPP2Sum)
    totalP2Sum = count_Sum(totalP2Count)
    temp.append(totalP2Sum)
    TableData.append(tuple(temp))
    
    temp = []
    temp.append("Summary")
    temp.append("P3")
    manP3Sum = count_Sum(manP3Count)
    temp.append(manP3Sum)
    manIPP3Sum = count_Sum(manIPP3Count)
    temp.append(manIPP3Sum)
    autoP3Sum = count_Sum(autoP3Count)
    temp.append(autoP3Sum)
    autoIPP3Sum = count_Sum(autoIPP3Count)
    temp.append(autoIPP3Sum)
    perP3Sum = count_Sum(perP3Count)
    temp.append(perP3Sum)
    perIPP3Sum = count_Sum(perIPP3Count)
    temp.append(perIPP3Sum)
    totalP3Sum = count_Sum(totalP3Count)
    temp.append(totalP3Sum)
    TableData.append(tuple(temp))
    
    temp = []
    temp.append("Summary")
    temp.append("P4")
    manP4Sum = count_Sum(manP4Count)
    temp.append(manP4Sum)
    manIPP4Sum = count_Sum(manIPP4Count)
    temp.append(manIPP4Sum)
    autoP4Sum = count_Sum(autoP4Count)
    temp.append(autoP4Sum)
    autoIPP4Sum = count_Sum(autoIPP4Count)
    temp.append(autoIPP4Sum)
    perP4Sum = count_Sum(perP4Count)
    temp.append(perP4Sum)
    perIPP4Sum = count_Sum(perIPP4Count)
    temp.append(perIPP4Sum)
    totalP4Sum = count_Sum(totalP4Count)
    temp.append(totalP4Sum)
    TableData.append(tuple(temp))
    
    temp = []
    temp.append("Summary")
    temp.append("Total")
    manSum = count_Sum(manCount)
    temp.append(manSum)
    manIPSum = count_Sum(manIPCount)
    temp.append(manIPSum)
    autoSum = count_Sum(autoCount)
    temp.append(autoSum)
    autoIPSum = count_Sum(autoIPCount)
    temp.append(autoIPSum)
    perSum = count_Sum(perCount)
    temp.append(perSum)
    perIPSum = count_Sum(perIPCount)
    temp.append(perIPSum)
    totalSum = count_Sum(totalCount)
    temp.append(totalSum)
    TableData.append(tuple(temp))
    
    """FinalData = []
    
    for i in sections:
        tempsect = []
        tempsect.append(sections[i])
        k = 5*i
        while k<5*(i+1):
            j = 1
            temptuple = []
            temptuple.append(TableData[k])
            #for j in TableData:
                #temptuple.append(TableData[k][j])
            k = k+1
        tempsect.append(tuple(temptuple))
        FinalData.append(tuple(tempsect))"""
        
    Heading = ['Section', 'Priority', 'Manual', 'Manual in-progress', 'Automated', 'Automated in-progress', 'Performance', 'Performance in-progress', 'Total']
    results = {'Heading':Heading, 'TableData':TableData, 'Summary':tuple(temp)}
    # results = {'Heading':Heading, 'TableData':RefinedData}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def count_Sum(caseCount):
    count = 0
    for each in caseCount:
        count = count + each
    return count

def Count_Per_Section(testCases, sections, caseCount):  # minar09
    for each in sections:
        x = 0
        z = each[0]
        for case in testCases:
            y = case[1]
            if y == z:
                x = x + 1
        caseCount.append(x)
            
def Append_array(TableData, P1, P2, P3, P4, Total, RefinedData):  # minar09
    x = 1
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0                    
    for each in TableData:
        data = []
        for y in each:
            data.append(y)
        if x == 1:
            data.append(P1[a])
            a = a + 1
        elif x == 2:
            data.append(P2[b])
            b = b + 1
        elif x == 3:
            data.append(P3[c])
            c = c + 1
        elif x == 4:
            data.append(P4[d])
            d = d + 1
        elif x == 5:
            data.append(Total[e])
            e = e + 1
        RefinedData.append(tuple(data))
        if x == 5:
            x = 1
        elif x < 5:
            x = x + 1


def TestStepAutoComplete(request):
    Conn = GetConnection()
    results = []
    test = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        field = [u'stepname', u'stepfeature', u'steptype', u'driver']
        for each in field:
            statement = ""
            if each == 'stepname':
                statement = 'step'
            if each == 'stepfeature':
                statement = 'feature'
            if each == 'steptype':
                statement = 'type'
            if each == 'driver':
                statement = 'driver'
            test = DB.GetData(Conn, "select  distinct " + each + "||' - " + statement + "' from test_steps_list where " + each + " Ilike '%" + value + "%'")
            results = list(results + test)    
    if len(results) > 0:
        results.append("*Dev")    
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json') 

def TestStep_TestCases(request):
    Conn = GetConnection()
    fields = [u'stepfeature', u'driver', u'steptype']
    TableData = []
    RefinedData = []
    if request.is_ajax():
        if request.method == "GET":
            search_query = request.GET.get(u'Query', '')
            search_value = search_query.split(":")
            for each_item in search_value:
                each_item = each_item.strip();
                if each_item != "":
                    query = " where stepname='" + each_item + "'"
                    for each in fields:
                        query += " or " + each + "='" + each_item + "'"
                    query = "SELECT distinct tc_id,tc_name FROM test_cases where tc_id in (SELECT distinct tc_id from test_steps where step_id in(SELECT distinct step_id from test_steps_list " + query + "))"
                    TableData_1 = DB.GetData(Conn, query, False)
                    TableData.append(TableData_1)
            resultData = TableData[0]
            for each in TableData:
                setData = set(resultData).intersection(set(each))
                resultData = list(setData)
            Check_TestCase(resultData, RefinedData)
        Heading = ['TestCase_ID', 'TestCase_Name', 'TestCase_Type']
        results = {'Heading':Heading, 'TableData':RefinedData}
        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')
def TestStepWithTypeInTable(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            # TestCaseName = request.GET.get('ClickedTC', '')
            RunID = request.GET.get('RunID', '')
            print RunID
            RunID = str(RunID.strip())
            RunID = str(RunID.replace(u'\xa0', u''))
            result = []
            if RunID != '':
                Result = DB.GetData(Conn, "Select stepname from test_steps tst,test_steps_list tsl where tst.step_id = tsl.step_id and tc_id  = '%s' order by teststepsequence" % RunID)
            for each in Result:
                query = "select steptype from test_steps_list where stepname='" + each + "'"
                Result_type = DB.GetData(Conn, query)
                result.append((each, Result_type[0]))
    column = ['Step Name', 'Step Type']
    results = {'Result':result, 'column':column}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def ViewRunIDTestCases(request, Run_Id, TC_Id):
    print Run_Id
    print TC_Id
    Conn = GetConnection()
    query = "select tc_name from result_test_cases where tc_id='%s' and run_id='%s'" % (TC_Id, Run_Id)
    testcasename = DB.GetData(Conn, query, False)
    dquery = "select name from result_test_case_tag where tc_id='%s' and property='JiraId' and run_id='%s'" % (TC_Id, Run_Id)
    defectid = DB.GetData(Conn, dquery, False)
    defectid = [x[0] for x in defectid]
    id1 = ', '.join(defectid)
    tquery = "select name from result_test_case_tag where tc_id='%s' and property='MKS' and run_id='%s'" % (TC_Id, Run_Id)
    mksid = DB.GetData(Conn, tquery, False)
    mksid = [x[0] for x in mksid]
    id2 = ', '.join(mksid)
    rquery = "select name from result_test_case_tag where tc_id='%s' and property='PRDId' and run_id='%s'" % (TC_Id, Run_Id)
    requirementid = DB.GetData(Conn, rquery, False)
    requirementid = [x[0] for x in requirementid]
    id3 = ', '.join(requirementid)
    
    section_path = ''
    
    try:
        query = '''
        SELECT name FROM test_case_tag WHERE property='%s' AND tc_id='%s' 
        ''' % ('section_id', TC_Id)
        data = DB.GetData(Conn, query, False, False)
        section_id = int(data[0][0])
        
        query = '''
        SELECT section_path FROM product_sections WHERE section_id=%d
        ''' % section_id
        data = DB.GetData(Conn, query, False, False)
        section_path = '/'.join(data[0][0].replace('_', ' ').split('.'))
        
    except:
        print '-'
    
    return render_to_response('ViewRunIDEditTestCases.html',
                              {
                              'runid':Run_Id,
                              'testcaseid':TC_Id,
                              'testcasename':testcasename[0][0],
                              'defectid':id1,
                              'mksid':id2,
                              'requirementid':id3,
                              'section_path': section_path
                              })

def RunIDTestCases(request, Run_Id, TC_Id):
    print Run_Id
    print TC_Id
    Conn = GetConnection()
    query = "select tc_name from result_test_cases where tc_id='%s' and run_id='%s'" % (TC_Id, Run_Id)
    testcasename = DB.GetData(Conn, query, False)
    dquery = "select name from result_test_case_tag where tc_id='%s' and property='JiraId' and run_id='%s'" % (TC_Id, Run_Id)
    defectid = DB.GetData(Conn, dquery, False)
    defectid = [x[0] for x in defectid]
    id1 = ', '.join(defectid)
    tquery = "select name from result_test_case_tag where tc_id='%s' and property='MKS' and run_id='%s'" % (TC_Id, Run_Id)
    mksid = DB.GetData(Conn, tquery, False)
    mksid = [x[0] for x in mksid]
    id2 = ', '.join(mksid)
    rquery = "select name from result_test_case_tag where tc_id='%s' and property='PRDId' and run_id='%s'" % (TC_Id, Run_Id)
    requirementid = DB.GetData(Conn, rquery, False)
    requirementid = [x[0] for x in requirementid]
    id3 = ', '.join(requirementid)
    
    section_path = ''
    
    try:
        query = '''
        SELECT name FROM test_case_tag WHERE property='%s' AND tc_id='%s' 
        ''' % ('section_id', TC_Id)
        data = DB.GetData(Conn, query, False, False)
        section_id = int(data[0][0])
        
        query = '''
        SELECT section_path FROM product_sections WHERE section_id=%d
        ''' % section_id
        data = DB.GetData(Conn, query, False, False)
        section_path = '/'.join(data[0][0].replace('_', ' ').split('.'))
        
    except:
        print '-'
    
    return render_to_response('RunIDEditTestCases.html',
                              {
                              'runid':Run_Id,
                              'testcaseid':TC_Id,
                              'testcasename':testcasename[0][0],
                              'defectid':id1,
                              'mksid':id2,
                              'requirementid':id3,
                              'section_path': section_path
                              })

def Update_RelatedItems(request):
    if request.is_ajax() and request.method == 'GET':
        TC_Id = request.GET.get(u'TC_Id', '')
        Associated_Bugs_List = request.GET.get(u'Associated_Bugs_List', '').split(",")
        Manual_TC_Id = request.GET.get(u'Manual_TC_Id', '').split(",")
        Requirement_ID_List = request.GET.get(u'Requirement_ID_List', '').split(",")
        
        conn = GetConnection()
        delete = DB.DeleteRecord(conn, 'test_case_tag', tc_id=TC_Id, property='JiraId')
        for i in Associated_Bugs_List:
            update = DB.InsertNewRecordInToTable(conn, 'test_case_tag', tc_id=TC_Id, name=i, property='JiraId')
            
        delete = DB.DeleteRecord(conn, 'test_case_tag', tc_id=TC_Id, property='MKS')
        for i in Manual_TC_Id:
            update = DB.InsertNewRecordInToTable(conn, 'test_case_tag', tc_id=TC_Id, name=i, property='MKS')
            
        delete = DB.DeleteRecord(conn, 'test_case_tag', tc_id=TC_Id, property='PRDId')
        for i in Requirement_ID_List:
            update = DB.InsertNewRecordInToTable(conn, 'test_case_tag', tc_id=TC_Id, name=i, property='PRDId')
            
        message = "Related Items are updated."
            
    results = simplejson.dumps(message)
    return HttpResponse(results, mimetype='application/json')

def DataFetchForTestCases(request):
    # message="in the DataFetchForTestCases"
    if request.is_ajax():
        if request.method == 'GET':
            run_id = request.GET.get(u'run_id', '').strip()
            test_case_id = request.GET.get(u'test_case_id', '').strip()
            print run_id
            print test_case_id
            # Get the test steps from test_step_results
            Conn = GetConnection()
            query = "select step_id,teststepsequence from result_test_steps where tc_id='%s' and run_id='%s' order by teststepsequence" % (test_case_id, run_id)
            TestStepList = DB.GetData(Conn, query, False)
            DataCollected = []
            Conn.close()
            for each in range(0, len(TestStepList)):
                Conn = GetConnection()
                # Get the stepname fromt test_steps_list
                query = "select stepname,steptype,data_required from result_test_steps_list where step_id=%d and run_id='%s'" % (TestStepList[each][0], run_id)
                StepName = DB.GetData(Conn, query, False)
                Temp_Data = []
                Temp_Data.append(each + 1)
                Temp_Data.append(StepName[0][0])
                Temp_Data.append(StepName[0][1])
                if StepName[0][2] == True:
                    Temp_Data.append("true")
                else:
                    Temp_Data.append("false")
                datasetid = test_case_id + "_s" + str((each + 1))
                print datasetid
                # Get the description from the master_data
                query = "select description from result_master_data where id='%s' and field='step' and value='description' and run_id='%s'" % (datasetid, run_id)
                step_description = DB.GetData(Conn, query, False)
                Temp_Data.append(step_description[0][0])
                query = "select description from result_master_data where id='%s' and field='expected' and value='result' and run_id='%s'" % (datasetid, run_id)
                step_expected = DB.GetData(Conn, query, False)
                Temp_Data.append(step_expected[0][0])
                # Get the expected Result from the master data
                # Get the failreson from the test_step_results
                # Get the steps status from the test_step_results
                query = "select status,failreason from test_step_results where tc_id='%s' and run_id='%s' and teststep_id=%d and teststepsequence='%d'" % (test_case_id, run_id, (TestStepList[each][0]), (TestStepList[each][1])) 
                Status = DB.GetData(Conn, query, False) 
                Temp_Data.append(Status[0][1])  # FailReason
                Temp_Data.append(Status[0][0])
                query = "select verify_point,step_continue,estd_time,stepenable,driver,stepfeature from result_test_steps_list where step_id=%d and run_id='%s'" % (TestStepList[each][0], run_id)
                StepType = DB.GetData(Conn, query, False)
                # Temp_Data.append(StepType[0][0])
                if StepType[0][0] == True:
                    Temp_Data.append("true")
                else:
                    Temp_Data.append("false")
                # Temp_Data.append(StepType[0][1])
                if StepType[0][1] == True:
                    Temp_Data.append("true")
                else:
                    Temp_Data.append("false")
                Temp_Data.append(StepType[0][2])
                # Temp_Data.append(StepType[0][3])
                if StepType[0][3] == True:
                    Temp_Data.append("true")
                else:
                    Temp_Data.append("false")
                Temp_Data.append(StepType[0][4])
                Temp_Data.append(StepType[0][5])
                Conn.close()
                print Temp_Data
                # Temp_Data.append("Log")
                Temp_Data = tuple(Temp_Data)
                DataCollected.append(Temp_Data)
    DataColumn = ["#", "Step", "Type", "Data", "Description", "Expected", "Comment", "Status", "Verification Point", "Cont. On Fail", "Estd. Time", "State", "Driver", "Feature"]
    query = "select status from test_case_results where tc_id='%s' and run_id='%s'" % (test_case_id, run_id)
    Conn = GetConnection()
    test_case_status = DB.GetData(Conn, query, False)
    print DataColumn
    print DataCollected
    message = {
             'data_column':DataColumn,
             'data_collected':DataCollected,
             'test_case_status':test_case_status[0][0]
             }
    results = simplejson.dumps(message)
    return HttpResponse(results, mimetype='application/json')
def TestDataFetch(request):
    if request.is_ajax():
        if request.method == 'GET':
            run_id = request.GET.get(u'run_id', '')
            step_sequence = request.GET.get(u'step_sequence', '')
            tc_id = request.GET.get(u'tc_id', '')
            Conn = GetConnection()
            # get the step_sequence
            print step_sequence
            test_steps_get_query = "select step_editable,data_required,teststepsequence from result_test_steps ts,result_test_steps_list tsl where ts.run_id=tsl.run_id and ts.step_id=tsl.step_id and ts.run_id='%s' and ts.tc_id='%s' order by ts.teststepsequence" % (run_id, tc_id)
            test_steps = DB.GetData(Conn, test_steps_get_query, False)
            print test_steps
            step_sequence = int(step_sequence)
            step_editable = test_steps[step_sequence - 1][0]
            data_required = test_steps[step_sequence - 1][1]
            test_step_sequence = test_steps[step_sequence - 1][2]
            dataset = tc_id + 'ds'
            Step_Data = []
            if data_required:
                container_data_id_query = "select ctd.curname,ctd.newname from result_test_steps_data tsd, result_container_type_data ctd where tsd.run_id=ctd.run_id and tsd.run_id='" + run_id + "' and tsd.testdatasetid = ctd.dataid and tcdatasetid = '" + dataset + "' and teststepseq = " + str(test_step_sequence) + "and ctd.curname Ilike '%_s" + str(step_sequence) + "%'"
                container_data_id_details = DB.GetData(Conn, container_data_id_query, False)
                if step_editable:
                    for each_data_id in container_data_id_details:
                        if len(each_data_id) == 2:
                            From_Data = TestCaseCreateEdit.Result_Get_PIM_Data_By_Id(Conn, run_id, each_data_id[0])
                            To_Data = TestCaseCreateEdit.Result_Get_PIM_Data_By_Id(Conn, run_id, each_data_id[1])
                            Step_Data.append((From_Data, To_Data))
                else:
                    for each_data_id in container_data_id_details:
                        From_Data = TestCaseCreateEdit.Result_Get_PIM_Data_By_Id(Conn, run_id, each_data_id[0])
                        Step_Data.append(From_Data)
            else:
                print "wrong data"
            """query="select distinct id from result_master_data where id Ilike '%s" %data_set_id
            query+=("_%' and run_id='"+run_id+"'")
            data_set=DB.GetData(Conn,query)
            temp_data=[]
            for each in data_set:
                if(len(each)==14):
                    temp_data.append(each)
            data_set=temp_data
            row_array=[]
            data_array=[]
            count=0
            for each in data_set:
                count=count+1
                row_array.append((count,""))
                query="select field,value from result_master_data where id Ilike '%s" %each
                query+=("%%' and field!='step' and field!='' and value!='description' and run_id='"+run_id+"'")
                data=DB.GetData(Conn,query,False)
                data_array.append(data)"""
            print Step_Data
            Step_Data = ProcessRunIDData(Step_Data)
            print Step_Data
    results = simplejson.dumps(Step_Data)
    return HttpResponse(results, mimetype='application/json')

def ProcessRunIDData(Step_Data):
    step_data = 1
    final_data = []
    for each in Step_Data:
        temp = []
        if isinstance(each, tuple):
            print "edit data"
            from_data = each[0]
            to_data = each[1]
            tempData = []
            for eachitem in from_data:
                if isinstance(eachitem[0], basestring) and isinstance(eachitem[1], basestring):
                    tempData.append((eachitem[0], '', eachitem[1]))
                if isinstance(eachitem[0], basestring) and isinstance(eachitem[1], list):
                    group_name = eachitem[0]
                    for dataitem in eachitem[1]:
                        if isinstance(dataitem[0], basestring) and isinstance(dataitem[1], basestring):
                            tempData.append((group_name, dataitem[0], dataitem[1]))
            temp.append(('From Data', tempData))
            tempData = []
            for eachitem in to_data:
                if isinstance(eachitem[0], basestring) and isinstance(eachitem[1], basestring):
                    tempData.append((eachitem[0], '', eachitem[1]))
                if isinstance(eachitem[0], basestring) and isinstance(eachitem[1], list):
                    group_name = eachitem[0]
                    for dataitem in eachitem[1]:
                        if isinstance(dataitem[0], basestring) and isinstance(dataitem[1], basestring):
                            tempData.append((group_name, dataitem[0], dataitem[1]))
            temp.append(('To Data', tempData))
        if isinstance(each, list):
            tempData = []
            for eachitem in each:
                if isinstance(eachitem[0], basestring) and isinstance(eachitem[1], basestring):
                    tempData.append((eachitem[0], '', eachitem[1]))
                if isinstance(eachitem[0], basestring) and isinstance(eachitem[1], list):
                    group_name = eachitem[0]
                    for dataitem in eachitem[1]:
                        if isinstance(dataitem[0], basestring) and isinstance(dataitem[1], basestring):
                            tempData.append((group_name, dataitem[0], dataitem[1]))
            temp.append((step_data, tempData))
        step_data += 1
        final_data.append(temp)    
    return final_data
def LogFetch(request):
    if request.is_ajax():
        if request.method == 'GET':
            run_id = request.GET.get(u'run_id', '').strip()
            test_case_id = request.GET.get(u'test_case_id', '').strip()
            step_name = request.GET.get(u'step_name', '').strip()
            print run_id
            print test_case_id
            print step_name
            Conn = GetConnection()
            query = "select step_id from test_steps_list where stepname='%s'" % step_name
            step_id = DB.GetData(Conn, query, False)
            query = "Select  el.status, el.modulename, el.details from test_step_results tsr, execution_log el where run_id = '%s' and tc_id = '%s' and teststep_id='%s' and tsr.logid = el.logid" % (run_id, test_case_id, str(step_id[0][0]))
            log = DB.GetData(Conn, query, False)
            column = ["Status", "ModuleName", "Details"]
    message = {
             'column':column,
             'log':log,
             'step':step_name
             }
    result = simplejson.dumps(message)
    return HttpResponse(result, mimetype='application/json')
def RunIDStatus(request):
    if request.is_ajax():
        if request.method == 'GET':
                run_id = request.GET.get(u'run_id', '')
                temp = []
                total_query = "select count(*) from test_run where run_id='%s'" % run_id
                pass_query = "select count(*) from test_case_results where run_id='%s' and status='Passed'" % run_id
                fail_query = "select count(*) from test_case_results where run_id='%s' and status='Failed'" % run_id
                blocked_query = "select count(*) from test_case_results where run_id='%s' and status='Blocked'" % run_id
                progress_query = "select count(*) from test_case_results where run_id='%s' and status='In-Progress'" % run_id
                submitted_query = "select count(*) from test_case_results where run_id='%s' and status='Submitted'" % run_id
                Conn = GetConnection()
                total = DB.GetData(Conn, total_query)
                passed = DB.GetData(Conn, pass_query)
                failed = DB.GetData(Conn, fail_query)
                blocked = DB.GetData(Conn, blocked_query)
                progress = DB.GetData(Conn, progress_query)
                submitted = DB.GetData(Conn, submitted_query)
                # pending=total[0]-(passed[0]+failed[0]+progress[0]+not_run[0])
                temp.append(total[0])
                temp.append(passed[0])
                temp.append(failed[0])
                temp.append(blocked[0])
                temp.append(progress[0])
                temp.append(submitted[0])
    message = {
             'message':temp
             }
    result = simplejson.dumps(message)
    return HttpResponse(result, mimetype='application/json')
def Make_List(step_name, step_reason, step_status, test_case_id, test_step_sequence_list):
    ListAll = []
    if  isinstance(step_status, list):
        for name in zip(step_name, step_reason, step_status, test_step_sequence_list):
            ListAll.append((name[0].strip(), name[1].strip(), name[2].strip(), name[3]))
    if isinstance(step_status, basestring):
        for name in zip(step_name, step_reason, step_status, test_step_sequence_list):
            ListAll.append((name[0].strip(), name[1].strip(), step_status, name[3]))
    """if isinstance(step_status,basestring):
        for name in zip(step_name,step_reason,step_status):
            ListAll.append((name[0].strip(),name[1].strip(),step_status))"""
    print ListAll
    Conn = GetConnection()
    query = "select step_id,teststepsequence from test_steps where tc_id='%s' order by teststepsequence" % test_case_id
    test_step_sequence_list = DB.GetData(Conn, query, False)
    print test_step_sequence_list
    Refined_List = []
    for each in test_step_sequence_list:
        query = "select stepname from test_steps_list where step_id='%s'" % each[0]
        stepName = DB.GetData(Conn, query, False)
        for eachitem in ListAll:
            if eachitem[0] == stepName[0][0] and eachitem[3] == each[1]:
                Refined_List.append(eachitem)
                break
    return Refined_List

def update_runid(run_id, test_case_id):
    oConn = GetConnection()
    squery = "select distinct status from test_case_results where run_id='%s'" % run_id
    run_id_status = DB.GetData(oConn, squery)
    submit_count = 0
    count = 0
    progress = 0
    for each in run_id_status:
        if each == 'Submitted':
            submit_count += 1
        elif each == 'In-Progress':
            progress += 1
        else:
            count += 1
    Dict = {}
    Dict1 = {}
    if progress == 0 and submit_count == 0 and count == len(run_id_status):
        status = 'Complete'
        endtime = DB.GetData(oConn, "select current_timestamp", False)
        Dict.update({'testendtime':str(endtime[0][0])})
        """allEmailIds = DB.GetData(oConn, "select email_notification from test_run_env where run_id = '"+run_id+"'", False)
        TestObjective = DB.GetData(oConn, "select test_objective from test_run_env where run_id = '"+run_id+"'", False)
        import EmailNotify
        EmailNotify.Complete_Email(allEmailIds,run_id,TestObjective,status,'','')"""
        
    elif progress > 0 or submit_count > 0:
        status = 'In-Progress'
        Dict.update({'status':status})
    else:
        if count == 0 and progress == 0 and submit_count == len(run_id_status):
            status = 'Submitted'
            starttime = DB.GetData(oConn, "select current_timestamp", False)
            endtime = ""
            Dict.update({'testendtime':endtime, 'teststartime':str(starttime[0][0])})
    sWhereQuery = "where run_id='%s'" % run_id
    Dict1.update({'status':status})
    print DB.UpdateRecordInTable(oConn, "test_run_env", sWhereQuery, **Dict1)
    print DB.UpdateRecordInTable(oConn, "test_env_results", sWhereQuery, **Dict)
    print DB.UpdateRecordInTable(oConn, "test_env_results", sWhereQuery, **Dict1)
    #########################Add a new entry in the TestRunEnv Table#########################
    # Get Machine Information
    machine_query = "select * from test_run_env where run_id='%s'" % run_id
    machine_info = DB.GetData(oConn, machine_query, False)
    print machine_info
    status_query = "select distinct status from test_run_env where tester_id='%s'" % (machine_info[0][3].strip())
    status_list = DB.GetData(oConn, status_query)
    forbidden_status = ['Submitted', 'In-Progress']
    command = "create"
    for each in status_list:
        if each in forbidden_status:
            command = "can't create"
            print DB.DeleteRecord(oConn, "test_run_env", tester_id=machine_info[0][3].strip(), status='Unassigned')
    if command == "create":
        #currenttime = DB.GetData(oConn, "select current_timestamp", False)
        #updated_time = str(currenttime[0][0])
        updated_time=TimeStamp("string")
        print DB.DeleteRecord(oConn, "test_run_env", tester_id=machine_info[0][3].strip(), status='Unassigned')
        Dict = {'tester_id':machine_info[0][3].strip(), 'status':'Unassigned', 'last_updated_time':updated_time.strip(), 'machine_ip':machine_info[0][6].strip(), 'branch_version':machine_info[0][12].strip()}
        Conn=GetConnection()
        print DB.InsertNewRecordInToTable(Conn, "test_run_env", **Dict)
        Conn.close()
        query="select id from test_run_env where tester_id='%s' and status='Unassigned'"%(machine_info[0][3].strip())
        Conn=GetConnection()
        new_index=DB.GetData(Conn,query)
        Conn.close()
        query="select name,bit,version,type from machine_dependency_settings where machine_serial=%d"%int(machine_info[0][0])
        Conn=GetConnection()
        dependency_list=DB.GetData(Conn,query,False)
        Conn.close()
        for each in dependency_list:
            Dict={}
            Dict.update({'name':each[0], 'bit':each[1],'version':each[2],'type':each[3], 'machine_serial':new_index[0]})
            Conn=GetConnection()
            print DB.InsertNewRecordInToTable(Conn,'machine_dependency_settings', **Dict)
            Conn.close()
        query="select project_id,team_id from machine_project_map where machine_serial=%d"%int(machine_info[0][0])
        Conn=GetConnection()
        project_map=DB.GetData(Conn,query,False)
        Conn.close()
        for each in project_map:
            Dict={}
            Dict.update({'machine_serial':new_index[0], 'project_id':each[0],'team_id':each[1]})
            Conn=GetConnection()
            print DB.InsertNewRecordInToTable(Conn,'machine_project_map',**Dict)
            Conn.close()
    """if status == 'Complete':
        run_id = str(run_id)
        allEmailIds = DB.GetData(oConn, "select email_notification from test_run_env where run_id = '"+run_id+"'", False)
        TestObjective = DB.GetData(oConn, "select test_objective from test_run_env where run_id = '"+run_id+"'")
        Tester = DB.GetData(oConn, "select assigned_tester from test_run_env where run_id = '"+run_id+"'")
        list = []     
        pass_query = "select count(*) from test_case_results where run_id='%s' and status='Passed'" % run_id
        passed = DB.GetData(oConn, pass_query)
        list.append(passed[0])
        fail_query = "select count(*) from test_case_results where run_id='%s' and status='Failed'" % run_id
        fail = DB.GetData(oConn, fail_query)
        list.append(fail[0])
        blocked_query = "select count(*) from test_case_results where run_id='%s' and status='Blocked'" % run_id
        blocked = DB.GetData(oConn, blocked_query)
        list.append(blocked[0])
        progress_query = "select count(*) from test_case_results where run_id='%s' and status='In-Progress'" % run_id
        progress = DB.GetData(oConn, progress_query)
        list.append(progress[0])
        submitted_query = "select count(*) from test_case_results where run_id='%s' and status='Submitted'" % run_id
        submitted = DB.GetData(oConn, submitted_query)
        list.append(submitted[0])
        skipped_query = "select count(*) from test_case_results where run_id='%s' and status='Skipped'" % run_id
        skipped = DB.GetData(oConn, skipped_query)
        list.append(skipped[0])
        total_query = "select count(*) from test_case_results where run_id='%s'" % run_id
        total = DB.GetData(oConn, total_query)
        list.append(total[0])
        duration = DB.GetData(oConn, "select to_char(now()-teststarttime,'HH24:MI:SS') as Duration from test_env_results where run_id = '"+run_id+"'")
        
        EmailNotify.Complete_Email(allEmailIds[0],run_id,str(TestObjective[0]),status,list,Tester,duration,'','')
        """    
    """try:
            urllib2.urlopen("http://www.google.com").close()
            #import EmailNotify
            EmailNotify.Complete_Email(allEmailIds[0],run_id,str(TestObjective[0]),status,list,Tester,duration,'','')
            print "connected"
        except urllib2.URLError:
            print "disconnected"
        """
        
def Send_Report(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            run_id = request.GET.get(u'runid', '')
            run_id = str(run_id)
            EmailIds = request.GET.get(u'EmailIds', '')
            EmailIds = str(EmailIds.replace(u'\xa0', u''))
            EmailIds = EmailIds.split(":")
            Emails = []
            for eachitem in EmailIds :
                if eachitem != "":
                    Eid = DB.GetData(Conn, "Select email from permitted_user_list where user_names = '%s'" % str(eachitem))
                if len(Eid) > 0:
                    Emails.append(Eid[0])

            stEmailIds = ','.join(Emails)
            status = DB.GetData(Conn, "select status from test_run_env where run_id = '"+run_id+"'")
            TestObjective = DB.GetData(Conn, "select test_objective from test_run_env where run_id = '"+run_id+"'")
            Tester = DB.GetData(Conn, "select assigned_tester from test_run_env where run_id = '"+run_id+"'")
            list = []
            
            pass_query = "select count(*) from test_case_results where run_id='%s' and status='Passed'" % run_id
            passed = DB.GetData(Conn, pass_query)
            list.append(passed[0])
            fail_query = "select count(*) from test_case_results where run_id='%s' and status='Failed'" % run_id
            fail = DB.GetData(Conn, fail_query)
            list.append(fail[0])
            blocked_query = "select count(*) from test_case_results where run_id='%s' and status='Blocked'" % run_id
            blocked = DB.GetData(Conn, blocked_query)
            list.append(blocked[0])
            progress_query = "select count(*) from test_case_results where run_id='%s' and status='In-Progress'" % run_id
            progress = DB.GetData(Conn, progress_query)
            list.append(progress[0])
            submitted_query = "select count(*) from test_case_results where run_id='%s' and status='Submitted'" % run_id
            submitted = DB.GetData(Conn, submitted_query)
            list.append(submitted[0])
            skipped_query = "select count(*) from test_case_results where run_id='%s' and status='Skipped'" % run_id
            skipped = DB.GetData(Conn, skipped_query)
            list.append(skipped[0])
            total_query = "select count(*) from test_case_results where run_id='%s'" % run_id
            total = DB.GetData(Conn, total_query)
            list.append(total[0])
            duration = DB.GetData(Conn, "select to_char(now()-teststarttime,'HH24:MI:SS') as Duration from test_env_results where run_id = '"+run_id+"'")

            EmailNotify.Complete_Email(stEmailIds,run_id,str(TestObjective[0]),status[0],list,Tester,duration,'','')
            results = ['OK']
            
            """try:
                urllib2.urlopen("http://www.google.com").close()
                #import EmailNotify
                EmailNotify.Complete_Email(stEmailIds,run_id,str(TestObjective[0]),status[0],list,Tester,duration,'','')
                print "connected"
                results = ['OK']
            except urllib2.URLError:
                print "disconnected"
                results = ['NOK']
            """
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
    #########################################################################################
def UpdateTestStepStatus(List, run_id, test_case_id, test_case_status, failReason,start_time,end_time):
    """test_step_id_list=[]
    for each in List:
        print each
        query="select step_id from test_steps_list where stepname='%s'" %each[0].strip()
        Conn=GetConnection()
        step_id=DB.GetData(Conn, query, False)
        test_step_id_list.append(step_id[0][0])
    print test_step_id_list
    ##########Fetch the main order List for the 
        query="where run_id='%s' and tc_id='%s' and teststep_id='%d'"%(run_id,test_case_id,step_id[0][0])
        Dict={}
        Dict.update({'status':each[2],'failreason':each[1]})
        print DB.UpdateRecordInTable(Conn, "test_step_results", query,**Dict)
    query="where run_id='%s' and tc_id='%s'"%(run_id,test_case_id)
    Dict={}
    Dict.update({'status':test_case_status,'failreason':failReason})
    print DB.UpdateRecordInTable(Conn,"test_case_results",query,**Dict)
    update_runid(run_id,test_case_id)
    return "true"
    """
    ######Get the step List for the selected Test Case #######################
    query = "select step_id,teststepsequence from result_test_steps where tc_id='%s' and run_id='%s' order by teststepsequence" % (test_case_id, run_id)
    Conn = GetConnection()
    test_steps_list = DB.GetData(Conn, query, False)
    Conn.close()
    print test_steps_list
    count = 0
    for each in test_steps_list:
        name_query = "select stepname from result_test_steps_list where step_id='%s' and run_id='%s'" % (each[0], run_id)
        Conn=GetConnection()
        stepName = DB.GetData(Conn, name_query)
        Conn.close()
        if stepName[0] == List[count][0]:
            query = "where run_id='%s' and tc_id='%s' and teststep_id='%d' and teststepsequence='%d'" % (run_id, test_case_id, each[0], each[1])
            Dict = {}
            Dict.update({'status':List[count][2], 'failreason':List[count][1]})
            Conn=GetConnection()
            print DB.UpdateRecordInTable(Conn, "test_step_results", query, **Dict)
            Conn.close()
            count += 1
    query = "where run_id='%s' and tc_id='%s'" % (run_id, test_case_id)
    test_case_select_query="select teststarttime from test_case_results "+query
    Conn=GetConnection()
    case_start_time=DB.GetData(Conn,test_case_select_query,False)
    Conn.close()
    Dict = {}
    if case_start_time[0][0]==None:
        Dict.update({'teststarttime':start_time})
    Dict.update({'status':test_case_status, 'failreason':failReason, 'testendtime':end_time})
    Conn=GetConnection()
    print DB.UpdateRecordInTable(Conn, "test_case_results", query, **Dict)
    Conn.close()
    update_runid(run_id, test_case_id)
    return "true"
def UpdateData(request):
    if request.is_ajax():
        if request.method == 'GET':
            step_name = request.GET.get(u'step_name', '').split("|")
            step_status = request.GET.get(u'step_status', '').split("|")
            step_reason = request.GET.get(u'step_reason', '').split("|")
            run_id = request.GET.get(u'run_id', '')
            test_case_id = request.GET.get(u'test_case_id', '')
            start_time=request.GET.get(u'start_time','')
            end_time=request.GET.get(u'end_time','')
            Conn = GetConnection()
            query = "select teststepsequence from result_test_steps where tc_id='%s' and run_id='%s'" % (test_case_id, run_id)
            test_step_sequence_list = DB.GetData(Conn, query)
            if(len(step_status) == 1):
                Refined_List = Make_List(step_name, step_reason, step_status[0], test_case_id, test_step_sequence_list)
            else:
                Refined_List = Make_List(step_name, step_reason, step_status, test_case_id, test_step_sequence_list)
            print step_name
            print step_reason
            print step_status
            print run_id
            print test_case_id
            step_sequence = []
            FailReason = []
            for each in Refined_List:
                step_sequence.append(each[2])
                FailReason.append(each[1])
            print step_sequence
            failReason = ""
            found = "No-Status"
            index = 1
            for each in step_sequence:
                if each == 'In-Progress' or each == 'Submitted' or each == 'Failed':
                    found = each
                    break
                else:
                    index += 1
            if found == "No-Status":
                pass_count = 0
                skipped_count = 0
                for each in step_sequence:
                    if each == 'Passed':
                        pass_count += 1
                    if each == 'Skipped':
                        skipped_count += 1
                if (pass_count + skipped_count) == len(step_sequence) or skipped_count == 0:
                    test_case_status = 'Passed'
                    # failReason=""
                if skipped_count == len(step_sequence) and pass_count == 0:
                    test_case_status = 'Skipped'
            else:
                if found != 'Submitted':
                    test_case_status = found
                    if found != 'Failed':
                        rest_step_status = 'Submitted'
                        # failReason=""
                    else:
                        rest_step_status = 'Skipped'
                        failReason = Refined_List[index - 1][1]
                else:
                    if found == 'Submitted' and index == 1:
                        test_case_status = 'Submitted'
                        rest_step_status = 'Submitted'
                    else:
                        test_case_status = 'In-Progress'
                        rest_step_status = 'Submitted'
            print test_case_status
            if test_case_status == 'Failed':
                datasetid = test_case_id + '_s' + str(index)
                query = "select description from result_master_data where field='verification' and value='point' and id='%s' and run_id='%s'" % (datasetid, run_id)
                Conn = GetConnection()
                verification = DB.GetData(Conn, query, False)
                if verification[0][0] == "no":
                    test_case_status = 'Blocked'
                else:
                    test_case_status = 'Failed'
                print test_case_status
            for each in range(index, len(step_sequence)):
                step_sequence[each] = rest_step_status
                FailReason[each] = ""
                print step_sequence
            index = 0
            Final_List = []
            for each in zip(step_sequence, FailReason):
                temp = list(Refined_List[index])
                temp[2] = each[0]
                temp[1] = each[1]
                temp = tuple(temp)
                Final_List.append(temp)
                index += 1
            print Final_List
            message = UpdateTestStepStatus(Final_List, run_id, test_case_id, test_case_status, failReason, start_time,end_time)
    result = simplejson.dumps(message)
    return HttpResponse(result, mimetype='application/json')
def GetOS(request):
    if request.is_ajax():
        if request.method == 'GET':
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team_id','')
            final_list=[]
            query="select distinct dependency_name,array_agg(distinct name) from dependency d,dependency_management dm,dependency_name dn where d.id=dm.dependency and d.id=dn.dependency_id and dm.project_id='%s' and dm.team_id=%d group by dependency_name"%(project_id,int(team_id))
            Conn=GetConnection()
            dependency=DB.GetData(Conn,query,False)
            Conn.close()
            for each in dependency:
                name=each[0]
                listing=each[1]
                temp=[]
                for eachitem in listing:
                    query="select bit_name,array_agg(distinct version) from dependency_name dn,dependency_values dv where dn.id=dv.id and dn.name='%s' group by bit_name"%(eachitem)
                #   query="select distinct name from dependency d, dependency_name dn,dependency_values dv,dependency_management dm where dm.dependency=d.id and d.id =dn.dependency_id and dv.id=dn.id and d.dependency_name='%s' and dm.project_id='%s' and dm.team_id=%d group by d.dependency_name,dn.name,dv.bit_name"%(each,project_id,int(team_id))
                    Conn=GetConnection()
                    names=DB.GetData(Conn,query,False)                
                    Conn.close()
                    temp.append((eachitem,names))
                final_list.append((name,temp))
            query="select distinct branch_name,array_agg(distinct version_name) from branch b,branch_management bm, versions v where b.id=bm.branch and v.id=b.id and bm.project_id='%s' and bm.team_id=%d group by b.branch_name"%(project_id,int(team_id))
            Conn=GetConnection()
            version_list=DB.GetData(Conn,query,False)
            Conn.close()
            results={
                'version_list':version_list,
                'dependency_list':final_list
                } 
            results = simplejson.dumps(results)
            return HttpResponse(results, mimetype='application/json')
def Auto_MachineName(request):
    if request.is_ajax():
        if request.method == 'GET':
            machine_name = request.GET.get(u'term', '')
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team_id','')
            Conn = GetConnection()
            query = "select distinct user_names,user_level from permitted_user_list pul,test_run_env tre,machine_project_map mpm where pul.user_names=tre.tester_id and mpm.machine_serial=tre.id and user_level='Manual' and project_id='%s' and team_id=%d and user_names Ilike '%%%s%%' " % (project_id,int(team_id),machine_name)
            machine_list = DB.GetData(Conn, query, False)
            Conn.close()
    result = simplejson.dumps(machine_list)
    return HttpResponse(result, mimetype='application/json')
def CheckMachine(request):
    if request.is_ajax():
        if request.method == 'GET':
            name = request.GET.get(u'name', '')
            print name
            Conn = GetConnection()
            query = "select distinct machine_ip,branch_version,array_agg(distinct type||'|'||name||'|'||bit||'|'||version ) from test_run_env tre,permitted_user_list pul,machine_dependency_settings mds where pul.user_names=tre.tester_id and mds.machine_serial=tre.id and tester_id='%s' and pul.user_level='Manual' group by branch_version,machine_ip" % name
            machine_info = DB.GetData(Conn, query, False)
            Conn.close()
            print machine_info
    result = simplejson.dumps(machine_info)
    return HttpResponse(result, mimetype='application/json')
def AddManualTestMachine(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.is_ajax():
            if request.method == 'GET':
                machine_name = request.GET.get(u'machine_name', '').strip()
                machine_ip = request.GET.get(u'machine_ip', '').strip()
                branch=request.GET.get(u'branch_name','').strip()
                version=request.GET.get(u'branch_version','').strip()
                dependency=request.GET.get(u'dependency','').split('#')
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                new_dependency=[]
                for each in dependency:
                    new_dependency.append(each.split('|'))
                print machine_name
                print machine_ip
                print branch+":"+version
                print new_dependency
                user_level_tag='Manual'
                query = "select count(*) from permitted_user_list where user_names='%s' and user_level='%s'" % (machine_name,user_level_tag)
                Conn = GetConnection()
                count = DB.GetData(Conn, query)
                Conn.close()
                if count[0] > 0:
                    # update will go here.
                    print "yes"
                    query="Select id,status from test_run_env where tester_id = '%s'" % machine_name
                    Conn=GetConnection()
                    status = DB.GetData(Conn,query,False)
                    Conn.close()
                    for eachitem in status:
                        if eachitem[1] == "In-Progress":
                            Conn=GetConnection()
                            DB.UpdateRecordInTable(Conn, "test_run_env", "where tester_id = '%s' and status = 'In-Progress'" % machine_name, status="Cancelled")
                            Conn.close()
                            Conn=GetConnection()
                            DB.UpdateRecordInTable(Conn, "test_env_results", "where tester_id = '%s' and status = 'In-Progress'" % machine_name, status="Cancelled")
                            Conn.close()
                        elif eachitem[1] == "Submitted":
                            Conn=GetConnection()
                            DB.UpdateRecordInTable(Conn, "test_run_env", "where tester_id = '%s' and status = 'Submitted'" % machine_name, status="Cancelled")
                            Conn.close()
                        elif eachitem[1] == "Unassigned":
                            Conn=GetConnection()
                            DB.DeleteRecord(Conn, "test_run_env", tester_id=machine_name, status='Unassigned')
                            Conn.close()
                            Conn=GetConnection()
                            DB.DeleteRecord(Conn,'machine_dependency_settings',machine_serial=eachitem[0])
                            Conn.close()
                    updated_time = TimeStamp("string")
                    Dict = {'tester_id':machine_name.strip(), 'status':'Unassigned', 'last_updated_time':updated_time.strip(), 'machine_ip':machine_ip, 'branch_version':(branch+':'+version).strip()}
                    Conn=GetConnection()
                    tes2 = DB.InsertNewRecordInToTable(Conn, "test_run_env", **Dict)
                    Conn.close()
                    if(tes2 == True):
                        query="select id from test_run_env where tester_id='%s' and status='Unassigned' limit 1"%(machine_name.strip())
                        Conn=GetConnection()
                        temp_id=DB.GetData(Conn,query)
                        if isinstance(temp_id,list):
                            machine_id=temp_id[0]
                            problem=False
                            for each in new_dependency:
                                Dict={}
                                Dict.update({'machine_serial':machine_id,'name':each[1],'type':each[0]})
                                if(each[2]!='Nil'):
                                    Dict.update({'bit':each[2],'version':each[3]})
                                else:
                                    Dict.update({'bit':0,'version':''})
                                Conn=GetConnection()
                                result=DB.InsertNewRecordInToTable(Conn,"machine_dependency_settings",**Dict)
                                Conn.close()
                                if result==False:
                                    problem=True
                                    break
                            if problem:
                                log_message="Machine not registered successfully"
                                message=False
                            else:
                                Dict={'machine_serial':machine_id,'project_id':project_id,'team_id':team_id}
                                Conn=GetConnection()
                                result=DB.InsertNewRecordInToTable(Conn,'machine_project_map',**Dict)
                                Conn.close()
                                if result==True:
                                    log_message = "Machine Successfully Registered"
                                    message=True
                                else:
                                    log_message="Machine not registered successfully"
                                    message=False
                        else:
                            log_message="Machine not registered successfully"
                            message=False
                    else:
                        log_message="Machine not registered successfully"
                        message=False
                else:
                    print "none"
                    # new Entry will be inserted.
                    Dict = {'user_names':machine_name.strip(), 'user_level':user_level_tag, 'email':machine_name + '@machine.com'}
                    Conn=GetConnection()
                    tes1 = DB.InsertNewRecordInToTable(Conn, "permitted_user_list", **Dict)
                    Conn.close()
                    updated_time = TimeStamp("string")
                    Dict = {'tester_id':machine_name.strip(), 'status':'Unassigned', 'last_updated_time':updated_time.strip(), 'machine_ip':machine_ip, 'branch_version':(branch+':'+version).strip()}
                    Conn=GetConnection()
                    tes2 = DB.InsertNewRecordInToTable(Conn, "test_run_env", **Dict)
                    Conn.close()
                    if(tes1 == True and tes2 == True):
                        query="select id from test_run_env where tester_id='%s' and status='Unassigned' limit 1"%(machine_name.strip())
                        Conn=GetConnection()
                        temp_id=DB.GetData(Conn,query)
                        if isinstance(temp_id,list):
                            machine_id=temp_id[0]
                            problem=False
                            for each in new_dependency:
                                Dict={}
                                if each[2]=='Nil':
                                    Dict.update({'machine_serial':machine_id,'name':each[1],'bit':each[2],'version':each[3],'type':each[0]})
                                else:
                                    Dict.update({'machine_serial':machine_id,'name':each[1],'bit':0,'version':each[3],'type':each[0]})
                                Conn=GetConnection()
                                result=DB.InsertNewRecordInToTable(Conn,"machine_dependency_settings",**Dict)
                                Conn.close()
                                if result==False:
                                    problem=True
                                    break
                            if  not problem:
                                Dict={'machine_serial':machine_id,'project_id':project_id,'team_id':team_id}
                                Conn=GetConnection()
                                result=DB.InsertNewRecordInToTable(Conn,'machine_project_map',**Dict)
                                Conn.close()
                                if result==True:
                                    log_message = "Machine Successfully Registered"
                                    message=True
                                else:
                                    log_message="Machine not registered successfully"
                                    message=False
                            else:
                                log_message = "Machine Successfully Registered"
                                message=True
                        else:
                            log_message="Machine not registered successfully"
                            message=False
                    else:
                        log_message="Machine not registered successfully"
                        message=False
        result={
                'message':message,
                'log_message':log_message
                }
        result = simplejson.dumps(result)
        return HttpResponse(result, mimetype='application/json')
    except Exception,e:
        PassMessasge(sModuleInfo, e, error_tag)    
def chartDraw(request):
    if request.is_ajax():
        if request.method == 'GET':
            run_id = request.GET.get(u'runid', '')
            print run_id
            Conn = GetConnection()
            list = []
            total_query = "select count(*) from test_case_results where run_id='%s'" % run_id
            total = DB.GetData(Conn, total_query)
            list.append(total[0])
            pass_query = "select count(*) from test_case_results where run_id='%s' and status='Passed'" % run_id
            passed = DB.GetData(Conn, pass_query)
            list.append(passed[0])
            fail_query = "select count(*) from test_case_results where run_id='%s' and status='Failed'" % run_id
            fail = DB.GetData(Conn, fail_query)
            list.append(fail[0])
            blocked_query = "select count(*) from test_case_results where run_id='%s' and status='Blocked'" % run_id
            blocked = DB.GetData(Conn, blocked_query)
            list.append(blocked[0])
            progress_query = "select count(*) from test_case_results where run_id='%s' and status='In-Progress'" % run_id
            progress = DB.GetData(Conn, progress_query)
            list.append(progress[0])
            submitted_query = "select count(*) from test_case_results where run_id='%s' and status='Submitted'" % run_id
            submitted = DB.GetData(Conn, submitted_query)
            list.append(submitted[0])
            skipped_query = "select count(*) from test_case_results where run_id='%s' and status='Skipped'" % run_id
            skipped = DB.GetData(Conn, skipped_query)
            list.append(skipped[0])
    result = simplejson.dumps(list)
    return HttpResponse(result, mimetype='application/json')

def ReRun(request):
    if request.is_ajax():
        if request.method == 'GET':
            run_id = request.GET.get(u'RunID', '')
            status_name = request.GET.get(u'status', '').split(',')
            print run_id
            print status_name
            """status=[]
            if status_name=='failed':
                status.append('Failed')
            elif status_name=='failed+pending':
                status.append('Failed')
                status.append('Submitted')
            elif status_name=='pending':
                status.append('Submitted')
            else:
                status=[]"""
            Conn = GetConnection()
            """if len(status)==0:
                query="select tc.tc_id,tc.tc_name,tcr.status from test_cases tc,test_case_results tcr where tc.tc_id=tcr.tc_id and run_id='%s'"%run_id
                tc_list=DB.GetData(Conn, query,False)
                test_case_list=Modify(tc_list)
                print test_case_list
            else:"""
            tc_list = []
            for each in status_name:
                query = "select tc.tc_id,tc.tc_name,tcr.status from test_cases tc,test_case_results tcr where tc.tc_id=tcr.tc_id and tcr.run_id='%s' and tcr.status='%s'" % (run_id, each)
                get_list = DB.GetData(Conn, query, False)
                for eachitem in get_list:
                    tc_list.append(eachitem)
            print tc_list
            tc_list = list(set(tc_list))
            test_case_list = Modify(tc_list)
            print test_case_list
        print test_case_list    
        Column = ['Test Case ID', 'Test Case Name', 'Type', 'Status']
    result = {'col':Column, 'list':test_case_list}
    result = simplejson.dumps(result)
    return HttpResponse(result, mimetype='application/json')       

def LoginPage(request):
    return render_to_response('login.html', {}, context_instance=RequestContext(request))

def User_Login(request):
    
    if request.is_ajax() and request.method == 'GET':
        username = request.GET.get[u'username', '']
        password = request.GET.get[u'password', '']
    
    Conn = GetConnection()
    
    user = DB.GetData(Conn, "select full_name from user_info where username='" + username + "' and password='" + password + "'")
    if(len(user) == 1):
        message = "User Logged In"
    else:
        message = "User Not Found"
        
    result = simplejson.dumps(message)
    return HttpResponse(result, mimetype='application/json')

def getProductSection(request):
    """Conn=GetConnection()
    if request.is_ajax():
        if request.method=='GET':
            section=request.GET.get(u'section','')
            if section=="":
                main_result=[]
                query="select distinct section_path from product_sections"
                section_path=DB.GetData(Conn,query)
                for each in section_path:
                    main_result.append((section_path.split('.')[0],[]))
                    
                print section_path"""
    """Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        section = request.GET.get(u'section', '')
        if section == '':
            final_result=[]
            results = DB.GetData(Conn, "select distinct subpath(section_path,0,1) from product_sections", False)
            levelnumber = 0
            for each in results:
                top_level_query="select nlevel(section_path) from product_sections where section_path ~ '*.%s.*' order by nlevel(section_path) desc"%each[0]    
                top_level=DB.GetData(Conn,top_level_query)
                print top_level
                levelnumber = section.count('.') + 1
                results_sub = DB.GetData(Conn, "select distinct subltree(section_path,%d,%d) FROM product_sections WHERE section_path ~ '*.%s.*' and nlevel(section_path) > %d" % (levelnumber, levelnumber + 1, each[0], levelnumber), False)
                temp=[]
                for eachitem in results_sub:
                    temp.append(eachitem[0])
                final_result.append((each[0],temp))
            print final_result"""
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            section = request.GET.get(u'section', '')
            if section == "":
                query = "select distinct subpath(section_path,0,1) from product_sections"
                section_path = DB.GetData(Conn, query)
    result = simplejson.dumps(section_path)
    return HttpResponse(result, mimetype='application/json')

def getProductFeature(request):
    """Conn=GetConnection()
    if request.is_ajax():
        if request.method=='GET':
            feature=request.GET.get(u'feature','')
            if feature=="":
                main_result=[]
                query="select distinct feature_path from product_features"
                feature_path=DB.GetData(Conn,query)
                for each in feature_path:
                    main_result.append((feature_path.split('.')[0],[]))
                    
                print feature_path"""
    """Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        feature = request.GET.get(u'feature', '')
        if feature == '':
            final_result=[]
            results = DB.GetData(Conn, "select distinct subpath(feature_path,0,1) from product_features", False)
            levelnumber = 0
            for each in results:
                top_level_query="select nlevel(feature_path) from product_features where feature_path ~ '*.%s.*' order by nlevel(feature_path) desc"%each[0]    
                top_level=DB.GetData(Conn,top_level_query)
                print top_level
                levelnumber = feature.count('.') + 1
                results_sub = DB.GetData(Conn, "select distinct subltree(feature_path,%d,%d) FROM product_features WHERE feature_path ~ '*.%s.*' and nlevel(feature_path) > %d" % (levelnumber, levelnumber + 1, each[0], levelnumber), False)
                temp=[]
                for eachitem in results_sub:
                    temp.append(eachitem[0])
                final_result.append((each[0],temp))
            print final_result"""
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            feature = request.GET.get(u'feature', '')
            if feature == "":
                query = "select distinct subpath(feature_path,0,1) from product_features"
                feature_path = DB.GetData(Conn, query)
    result = simplejson.dumps(feature_path)
    return HttpResponse(result, mimetype='application/json')


##########MileStone Code####################
def AutoMileStone(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            milestone = request.GET.get(u'term', '')
            print milestone
            query = "select name,status,description,cast(starting_date as text),cast(finishing_date as text),created_by,cast(created_date as text),modified_by,cast(modified_date as text) from milestone_info where name ilike'%%%s%%'" % milestone
            milestone_list = DB.GetData(Conn, query, False)
    result = simplejson.dumps(milestone_list)
    return HttpResponse(result, mimetype='application/json')

def Get_MileStones(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            milestone = request.GET.get(u'term', '')
            print milestone
            query = "select distinct name,description,cast(starting_date as text),cast(finishing_date as text),status from milestone_info order by name"
            milestone_list = DB.GetData(Conn, query, False)
    Heading = ['Milestone Name','Description', 'Starting Date', 'Due Date', 'Status']
    results = {'Heading':Heading, 'TableData':milestone_list}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_MileStone_ID(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            milestone = request.GET.get(u'term', '')
            query = "select id from milestone_info where name = '"+milestone+"'"
            milestone_info = DB.GetData(Conn, query)
    json = simplejson.dumps(milestone_info)
    return HttpResponse(json, mimetype='application/json')

def Get_MileStone_By_ID(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            id = request.GET.get(u'term', '')
            query = "select id,name,cast(starting_date as text),cast(finishing_date as text),status,description,created_by,modified_by,cast(created_date as text),cast(modified_date as text) from milestone_info where id = '"+id+"'"
            milestone_info = DB.GetData(Conn, query, False)
    json = simplejson.dumps(milestone_info)
    return HttpResponse(json, mimetype='application/json')

def Milestone_Requirements(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            milestone = request.GET.get(u'term', '')
            print milestone
            query = "select r.requirement_id, r.requirement_title, r.status from requirements r, milestone_info mi where mi.id::varchar=r.requirement_milestone and mi.name like '%"+milestone+"%'"
            requirements_list = DB.GetData(Conn, query, False)
    Heading = ['Requirement ID','Requirement Name', 'Status']
    results = {'Heading':Heading, 'TableData':requirements_list}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Milestone_Tasks(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            milestone = request.GET.get(u'term', '')
            print milestone
            query = "select t.tasks_id,t.tasks_title,t.status from tasks t,milestone_info mi where t.tasks_milestone::int=mi.id and mi.name like '%"+milestone+"%'"
            tasks_list = DB.GetData(Conn, query, False)
    Heading = ['Task ID','Task title', 'Status']
    results = {'Heading':Heading, 'TableData':tasks_list}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Milestone_Bugs(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            milestone = request.GET.get(u'term', '')
            print milestone
            query = "select b.bug_id,b.bug_title,b.status from bugs b,milestone_info mi where b.bug_milestone::int=mi.id and mi.name like '%"+milestone+"%'"
            bugs_list = DB.GetData(Conn, query, False)
    Heading = ['Bug ID','Bug title', 'Status']
    results = {'Heading':Heading, 'TableData':bugs_list}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Milestone_Report(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            milestone = request.GET.get(u'term', '')
            print milestone
            complete_list = DB.GetData(Conn, "select cast(count(distinct run_id) as text) from test_run_env where test_milestone like '%"+milestone+"%' and status='Complete'")
            cancelled_list = DB.GetData(Conn, "select count(status) from test_run_env where test_milestone like '%"+milestone+"%' and status='Cancelled'")
            submitted_list = DB.GetData(Conn, "select count(status) from test_run_env where test_milestone like '%"+milestone+"%' and status='Submitted'")
            inprogress_list = DB.GetData(Conn, "select count(status) from test_run_env where test_milestone like '%"+milestone+"%' and status='In-progress'")
            #query="(select count(distinct run_id) from test_run_env where status='Complete' group by test_milestone)"
            #complete=DB.GetData(Conn,query)
            #query="select count(distinct run_id) from test_run_env where status not in ('Cancelled') group by test_milestone"
            all=DB.GetData(Conn,"select cast(count(distinct run_id) as text) from test_run_env where status not in ('Cancelled') and test_milestone like '%"+milestone+"%'")
        temp = []
        #temp.append(format((float(complete_list)*100)/float(all),'.2f'))
        for x in zip(complete_list,all):
            if x[1]=='0':
                temp.append(0)
            else:
                temp.append(format((float(x[0])*100)/float(x[1]),'.2f'))
        
        temp.append(int(all[0])-int(complete_list[0]))
        temp.append(int(all[0]))
    #Heading = ['Task ID','Task title', 'Status']
    results = {'Complete':complete_list, 'Cancelled':cancelled_list, 'Submitted':submitted_list, 'In-progress':inprogress_list, 'progress':temp}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Milestone_Testings(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            milestone = request.GET.get(u'term', '')
            print milestone
            query = "select run_id,test_objective,assigned_tester,run_type,status from test_run_env where test_milestone like '%"+milestone+"%'"
            testings_list = DB.GetData(Conn, query, False)
    Heading = ['Run ID','Run objective','Assigned Tester','Test Type', 'Status']
    results = {'Heading':Heading, 'TableData':testings_list}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Milestone_Teams(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            milestone = request.GET.get(u'term', '')
            print milestone
            query = "select distinct mtm.team_id from milestone_team_map mtm, milestone_info mi where mi.id=mtm.milestone_id and mi.name like '%"+milestone+"%'"
            teams_list = DB.GetData(Conn, query, False)
    json = simplejson.dumps(teams_list)
    return HttpResponse(json, mimetype='application/json')


def Get_AssignedTests(request):
    if request.is_ajax():
        if request.method == "GET":
            Conn = GetConnection()
            user = request.GET.get(u'user', '').strip()    
            print user    
            TableData = DB.GetData(Conn, "select run_id,rundescription,tester_id,status from test_run_env where assigned_tester like '%"+user+"%' and status not in ('Complete','Cancelled')", False)

    Heading = ['Run ID', 'Description', 'Tester', 'Status']
    results = {'Heading':Heading, 'TableData':TableData}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Requirements(request):
    if request.is_ajax():
        if request.method == "GET":
            Conn = GetConnection()
            user = request.GET.get(u'user', '').strip()    
            print user    
            TableData = DB.GetData(Conn, "select r.requirement_id,r.requirement_title,r.requirement_description,rtm.team_id from requirements r, requirement_team_map rtm,team_info ti, permitted_user_list pul where r.requirement_id=rtm.requirement_id and rtm.team_id::int=ti.team_id and ti.user_id::int=pul.user_id and pul.user_names like '%"+user+"%'", False)

    Heading = ['Requirement ID', 'Requirement Title', 'Requirement Description', 'Team ID']
    results = {'Heading':Heading, 'TableData':TableData}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def MileStoneOperation(request):
    if request.is_ajax():
        if request.method == 'GET':
            now=datetime.datetime.now().date()
            Conn = GetConnection()
            operation = request.GET.get(u'operation', '')
            description = request.GET.get(u'description','')
            status = request.GET.get(u'status','')
            team_id=request.GET.get(u'team','').split("|")
            confirm_message = ""
            error_message = ""
            if operation == "2":
                new_name = request.GET.get(u'new_name', '')
                old_name = request.GET.get(u'old_name', '')
                old_name = old_name.strip()
                modified_by = request.GET.get(u'modified_by','')
                start_date = request.GET.get(u'start_date','').strip()
                end_date = request.GET.get(u'end_date','').strip()
                start_date=start_date.split('-')
                starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
                end_date=end_date.split('-')
                ending_date=datetime.datetime(int(end_date[0].strip()),int(end_date[1].strip()),int(end_date[2].strip())).date()
                query = "select count(*) from config_values where type='milestone' and value='%s'" % old_name
                available = DB.GetData(Conn, query)
                if(available[0] > 0):
                    # check if old name is given again:
                    """againQuery = "select count(*) from milestone_info where name='%s' and starting_date='"+str(start_date)+"' and finishing_date='"+str(end_date)+"'" % new_name
                    again = DB.GetData(Conn, againQuery)
                    if(again[0] > 0):
                        error_message = "MileStone already exists, can't modify"
                    else:"""
                    # start Rename Operation
                    condition = "where type='milestone' and value='%s'" % old_name
                    mid = DB.GetData(Conn,"select id from config_values where type='milestone' and value = '"+old_name+"'")
                    Dict = {'value':new_name.strip()}
                    print DB.UpdateRecordInTable(Conn, "config_values", condition, **Dict)            
                    mcondition = "where id='%s' and name='%s'" % (mid[0],old_name)
                    mDict = {'name':new_name, 'starting_date':starting_date, 'finishing_date':ending_date,'status':status,'description':description,'modified_by':modified_by,'modified_date':now}
                    print DB.UpdateRecordInTable(Conn, "milestone_info", mcondition, **mDict)
                    result = DB.DeleteRecord(Conn,"milestone_team_map",milestone_id=mid[0])
                    for each in team_id:
                        team_Dict={
                                   'milestone_id':mid[0],
                                   'team_id':each.strip(),
                        }
                        result=DB.InsertNewRecordInToTable(Conn,"milestone_team_map",**team_Dict)
                    confirm_message = "MileStone is modified"
                else:
                    confirm_message = "No milestone is found"
            # start Create Operation
            if operation == "1":
                new_name = request.GET.get(u'new_name', '')
                new_name = new_name.strip()
                created_by = request.GET.get(u'created_by','')
                start_date = request.GET.get(u'start_date','').strip()
                end_date = request.GET.get(u'end_date','').strip()
                start_date=start_date.split('-')
                starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
                end_date=end_date.split('-')
                ending_date=datetime.datetime(int(end_date[0].strip()),int(end_date[1].strip()),int(end_date[2].strip())).date()
                query = "select count(*) from config_values where type='milestone' and value='%s'" % new_name
                available = DB.GetData(Conn, query)
                if(available[0] == 0):
                    Dict = {'type':'milestone', 'value':new_name.strip()}
                    print DB.InsertNewRecordInToTable(Conn, "config_values", **Dict)
                    mid = DB.GetData(Conn,"select id from config_values where type='milestone' and value = '"+new_name+"'")
                    mDict = {'id':mid[0], 'name':new_name, 'starting_date':starting_date, 'finishing_date':ending_date,'status':status,'description':description,'created_by':created_by,'created_date':now,'modified_by':created_by,'modified_date':now}
                    print DB.InsertNewRecordInToTable(Conn, "milestone_info", **mDict)
                    for each in team_id:
                        team_Dict={
                                   'milestone_id':mid[0],
                                   'team_id':each.strip(),
                        }
                        result=DB.InsertNewRecordInToTable(Conn,"milestone_team_map",**team_Dict)
                    confirm_message = "MileStone is created Successfully"
                else:
                    error_message = "MileStone name exists. Can't create a new one"
                # start  Operation
            if operation == "3":
                new_name = request.GET.get(u'new_name', '')
                new_name = new_name.strip()
                query = "select count(*) from config_values where type='milestone' and value='%s'" % new_name
                available = DB.GetData(Conn, query)
                if(available[0] > 0):
                    Dict = {'type':'milestone', 'value':new_name.strip()}
                    print DB.DeleteRecord(Conn, "config_values", **Dict)
                    mid = DB.GetData(Conn,"select id from config_values where type='milestone' and value = '"+new_name+"'")
                    mDict = {'id':mid[0], 'name':new_name}
                    print DB.DeleteRecord(Conn, "milestone_info", **mDict)
                    confirm_message = "MileStone is deleted Successfully"
                else:
                    error_message = "MileStone Not Found"
    results = {'confirm_message':confirm_message,
             'error_message':error_message
             }
    result = simplejson.dumps(results)
    return HttpResponse(result, mimetype='application/json')    

def TableDataTestCasesOtherPages(request):  #==================Returns Test Cases When User Send Query List From Run Page===============================
    Conn = GetConnection()
    test_status_request = request.GET.get(u'test_status_request', '')
    total_time=request.GET.get(u'total_time','')
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Query', '')
            if UserData!='':
                UserText = UserData.split(":");
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                QueryText = []
                for eachitem in UserText:
                    if len(eachitem) != 0 and  len(eachitem) != 1 and eachitem.strip() not in QueryText:
                        QueryText.append(eachitem.strip())
                print QueryText
                Section_Tag = 'Section'
                Feature_Tag = 'Feature'
                Custom_Tag = 'CustomTag'
                Section_Path_Tag = 'section_id'
                Feature_Path_Tag = 'feature_id'
                Priority_Tag = 'Priority'
                set_type='set'
                tag_type='tag'
                Status='Status'
                query="select distinct dependency_name from dependency d, dependency_management dm where d.id=dm.dependency and dm.project_id='%s' and dm.team_id=%d"%(project_id,int(team_id))
                Conn=GetConnection()
                dependency=DB.GetData(Conn,query)
                Conn.close()
                wherequery=""
                for each in dependency:
                    wherequery+=("'"+each.strip()+"'")
                    wherequery+=','
                wherequery+=("'"+Section_Tag+"','"+Feature_Tag+"','"+Custom_Tag+"','"+Section_Path_Tag+"','"+Feature_Path_Tag+"','"+Priority_Tag+"','"+Status+"','"+set_type+"','"+tag_type+"'")
                print wherequery
                TestIDList = []
                for eachitem in QueryText:
                    Conn=GetConnection()
                    TestID = DB.GetData(Conn, "Select property from test_case_tag where name = '%s' " % eachitem)
                    Conn.close()
                    for eachProp in TestID:
                        if eachProp == 'tcid':
                            TestIDList.append(eachitem)
                            break
                TableData = []
                if len(TestIDList) > 0:
                    for eachitem in TestIDList:
                        query="select distinct tct.tc_id,tc.tc_name from test_case_tag tct,test_cases tc where tct.tc_id=tc.tc_id and tct.tc_id='%s' group by tct.tc_id,tc.tc_name HAVING COUNT(CASE WHEN name = '%s' and property='Project' THEN 1 END) > 0 and COUNT(Case when name='%s' and property='Team' then 1 end)>0"%(eachitem,project_id,team_id)
                        Conn=GetConnection()
                        tabledata = DB.GetData(Conn,query, False)
                        Conn.close()
                        print tabledata
                        if tabledata:
                            TableData.append(tabledata[0])
                else:
                    count = 1
                    for eachitem in QueryText:
                        if count == 1:
                            Query = "HAVING COUNT(CASE WHEN name = '%s' and property in (%s) THEN 1 END) > 0 "%(eachitem.strip(),wherequery)
                            count=count+1
                        else:
                            Query+="AND COUNT(CASE WHEN name = '%s' and property in (%s) THEN 1 END) > 0 "%(eachitem.strip(),wherequery)
                            count=count+1
                    Query = Query + " AND COUNT(CASE WHEN property = 'Project' and name = '" + project_id + "' THEN 1 END) > 0"
                    Query = Query + " AND COUNT(CASE WHEN property = 'Team' and name = '" + team_id + "' THEN 1 END) > 0"
                    query = "select distinct tct.tc_id,tc.tc_name from test_case_tag tct,test_cases tc where tct.tc_id=tc.tc_id  group by tct.tc_id,tc.tc_name " + Query
                    Conn=GetConnection()
                    TableData = DB.GetData(Conn, query, False)        
                    Conn.close()
    
                RefinedDataTemp = []
                Check_TestCase(TableData, RefinedDataTemp)
                RefinedData=list(RefinedDataTemp)
                dataWithTime = []
                if total_time=="true":
                    time_collected=0
                for each in RefinedData:
                    query = "select count(*) from test_steps where tc_id='%s'" % each[0].strip()
                    Conn=GetConnection()
                    stepNumber = DB.GetData(Conn, query)
                    Conn.close()
                    test_case_time = 0
                    for count in range(0, int(stepNumber[0])):
                        temp_id = each[0] + '_s' + str(count + 1)
                        step_time_query = "select description from master_data where id='%s' and field='estimated' and value='time'" % temp_id.strip()
                        Conn=GetConnection()
                        step_time = DB.GetData(Conn, step_time_query)
                        Conn.close()
                        if len(step_time) == 0:
                            stepTime = 0
                        else:
                            stepTime = step_time[0]
                        test_case_time += int(stepTime)
                        if total_time=="true":
                            time_collected+=int(stepTime)
                    temp = []
                    for eachitem in each:
                        temp.append(eachitem)
                    temp.append(ConvertTime(test_case_time))
            #         temp=tuple(temp)
                    dataWithTime.append(temp)    
                RefinedData=dataWithTime
                for each in RefinedData:
                    print each
                Heading = ['ID', 'Title', 'Feature', 'Section' ,'Type','Time','']
                for i in dataWithTime:
                    x = i[1]
                    print x
                    try:
                        query = "SELECT name FROM test_case_tag WHERE property='%s' AND tc_id='%s'" % ('section_id', i[0])
                        Conn=GetConnection()
                        data = DB.GetData(Conn, query, False, False)
                        Conn.close()
                        section_id = int(data[0][0])
                        print "Section id is: %s" %section_id
                    except:
                        print "unable to get section id"
                    try:   
                        query = '''
                        SELECT name FROM test_case_tag WHERE property='%s' AND tc_id='%s' 
                        ''' % ('feature_id', i[0])
                        Conn=GetConnection()
                        data = DB.GetData(Conn, query, False, False)
                        Conn.close()
                        feature_id = int(data[0][0])        
                        print "Feature id is: %s" %feature_id                
                    except:
                        print "unable to get feature id"   
                    try:
                        query = '''
                        SELECT section_path FROM product_sections WHERE section_id=%d
                        ''' % section_id
                        Conn=GetConnection()
                        data = DB.GetData(Conn, query, False, False)
                        Conn.close()
                        section_path = '/'.join(data[0][0].replace('_', ' ').split('.'))
                        i.insert(2, section_path)
                        print "full path of section is: %s" %section_path
                    except:
                        print "unable to get full path of section"   
                    try:                            
                        query = '''
                        SELECT feature_path FROM product_features WHERE feature_id=%d
                        ''' % feature_id
                        Conn=GetConnection()
                        data = DB.GetData(Conn, query, False, False)
                        Conn.close()
                        feature_path = '/'.join(data[0][0].replace('_', ' ').split('.'))
                        i.insert(2, feature_path)
                        print "full path of feature is: %s"%feature_path
                    except:
                        print "unable to get full path of feature"
                    if test_status_request:
                        try:
                            query = '''
                            SELECT name FROM test_case_tag WHERE property='%s' AND tc_id='%s'
                            ''' % ('Status', i[0])
                            Conn=GetConnection()
                            data = DB.GetData(Conn, query, False, True)
                            Conn.close()
                            i.insert(4, data[0][0])           
                            Heading = ['ID', 'Title', 'Feature','Section' ,'Type', 'Status', 'Time']
                        except:
                            i[4] = ' - '
                results = {'Heading':Heading, 'TableData':RefinedData}
                if total_time=="true":
                    results.update({'time':ConvertTime(time_collected)})
            else:
                results = {'Heading':[], 'TableData':[]}
                if total_time=="true":
                    results.update({'time':""})
            json = simplejson.dumps(results)
            return HttpResponse(json, mimetype='application/json')

def GetStepNameType(request):
    if request.is_ajax():
        if request.method == 'GET':
            Conn = GetConnection()
            query = "select stepname,steptype from test_steps_list"
            test_steps_list = DB.GetData(Conn, query, False)

    Dict = {'test_steps':test_steps_list}
    result = simplejson.dumps(Dict)
    return HttpResponse(result, mimetype='appliction/json')

def Result(request):
    return render_to_response('Result.html', {}, context_instance=RequestContext(request))
def GetResultAuto(request):
    try:
        if request.is_ajax():
            if request.method == 'GET':            
                final = []
                term = request.GET.get(u'term', '')
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                # fetching the status
                query = "select distinct status,'Status' from test_run_env tre,machine_project_map mpm where mpm.machine_serial=tre.id and status Ilike '%%%s%%' and project_id='%s' and team_id=%d" %(term,project_id,int(team_id))
                Conn = GetConnection()
                status = DB.GetData(Conn, query, False)
                Conn.close()
                for each in status:
                    if each not in final:
                        final.append(each)
                ###Fetching the product version
                query = "select distinct branch_version,'Version' from test_run_env tre,machine_project_map mpm where mpm.machine_serial=tre.id and branch_version Ilike '%%%s%%' and project_id='%s' and team_id=%d" %(term,project_id,int(team_id))
                Conn=GetConnection()
                products = DB.GetData(Conn, query, False)
                Conn.close()
                for each in products:
                    if each not in final:
                        final.append(each)
                #Fetching the run_type
                query = "select distinct run_type,'Run Type' from test_run_env tre,machine_project_map mpm where mpm.machine_serial=tre.id and run_type Ilike '%%%s%%' and project_id='%s' and team_id=%d" %(term,project_id,int(team_id))
                Conn=GetConnection()
                run_types = DB.GetData(Conn, query, False)
                Conn.close()
                for each in run_types:
                    if each not in final:
                        final.append(each)
                # Fetching the distinct User From the Test Run Env
                query = "select assigned_tester from test_run_env tre,machine_project_map mpm where mpm.machine_serial=tre.id and project_id='%s' and team_id=%d"%(project_id,int(team_id))
                Conn=GetConnection()
                Testers = DB.GetData(Conn, query, False)
                Conn.close()
                tester = []
                ###Making Camel Case to accept####
                newTerm = ""
                TermList = []
                for each in range(0, len(term)):
                    TermList.append(term[each])
                newTerm = TermList[0].upper()
                for each in range(0, len(term)):
                    if each != 0:
                        newTerm += TermList[each]
                ########Making full CAPS LOCK ON ########
                newCap = ""
                TermList = []
                for each in range(0, len(term)):
                    TermList.append(term[each])
                newCap = TermList[0]
                for each in range(0, len(term)):
                    if each != 0:
                        newCap += (TermList[each].lower())
                ##########Making first Camel case Upper and all Lower#############
                firstup = ""
                TermList = []
                for each in range(0, len(term)):
                    TermList.append(term[each])
                firstup = TermList[0].upper()
                for each in range(0, len(term)):
                    if each != 0:
                        firstup += (TermList[each].lower())
                for each in Testers:
                    print each
                    for eachitem in each:
                        if eachitem is not None:
                            if "," not in eachitem:
                                if (term in eachitem or str(term).upper() in eachitem or str(term).lower() in eachitem or newTerm in eachitem or newCap in eachitem or firstup in eachitem) and eachitem not in tester:
                                    tester.append(eachitem)
                            else:
                                for eachitemdivide in eachitem.split(","):
                                    if (term in eachitemdivide.strip() or str(term).upper() in eachitemdivide.strip() or str(term).lower() in eachitemdivide.strip() or newTerm in eachitemdivide.strip() or newCap in eachitemdivide.strip() or firstup in eachitemdivide.strip()) and eachitemdivide.strip() not in tester:
                                        tester.append(eachitemdivide.strip())
                print tester
                for each in tester:
                    if (term in each or str(term).upper() in each or str(term).lower() in each or newTerm in each or newCap in each or firstup in each) and (each, 'Tester') not in final:
                        final.append((each, 'Tester'))
                # Fetch the objectives
                query = "select distinct ter.rundescription,'Objective' from test_env_results ter,test_run_env tre,machine_project_map mpm where tre.run_id=ter.run_id and mpm.machine_serial=tre.id and ter.rundescription Ilike '%%%s%%' and project_id='%s' and team_id=%d" %(term,project_id,int(team_id))
                Conn=GetConnection()
                objectives = DB.GetData(Conn, query, False)
                Conn.close()
                for each in objectives:
                    if each not in final:
                        final.append(each)
                # Fetch the milestones
                query = "select distinct test_milestone,'Milestone' from test_run_env tre,machine_project_map mpm where tre.id=mpm.machine_serial and test_milestone Ilike '%%%s%%'" % term
                Conn=GetConnection()
                milestone = DB.GetData(Conn, query, False)
                Conn.close()
                for each in milestone:
                    if each not in final:
                        final.append(each)
            result = simplejson.dumps(final)
            return HttpResponse(result, mimetype='application/json')
    except Exception,e:
        print e
    
def GetFilteredDataResult(request):
    if request.is_ajax():
        if request.method == 'GET':
            final = []
            UserText = request.GET.get(u'UserText', '')
            currentPagination = request.GET.get(u'pagination', '')
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team_id','')
            capacity=request.GET.get(u'capacity','')
            print currentPagination
            # UserText=str(UserText)
            UserText = UserText.replace(u'\xa0', u'|')
            UserText = UserText.split('|')
            for each in UserText:
                if each == "":
                    UserText.remove(each)
            print UserText
            # form query
            condition = ""
            for each in UserText:
                count=each.count(':')
                if count>1:
                    indices=[m.start() for m in re.finditer(':', each)]
                    listings=[]
                    listings.append(each[0:indices[-1]])
                    listings.append(each[indices[-1]+1:])
                    temp=list(listings)
                else:    
                    temp = each.split(":")
                if temp[1].strip() == "Version":
                    condition += "tre.branch_version='%s'" % temp[0]
                if temp[1].strip() == "Status":
                    condition += "tre.status='%s'" % temp[0]
                if temp[1].strip() == "Run Type":
                    condition += "tre.run_type='%s'" % temp[0]
                if temp[1].strip() == "Tester":
                    condition += "tre.assigned_tester Ilike '%%%s%%'" % temp[0]
                if temp[1].strip() == "Milestone":
                    condition += "tre.test_milestone='%s'" % temp[0]
                if temp[1].strip() == "Objective":
                    condition += "ter.rundescription='%s'" % temp[0]
                condition += " and "
            condition = condition[:-5].strip()
            print condition
            final = NewResultFetch(condition, currentPagination,project_id,team_id,capacity)
    result = simplejson.dumps(final)
    return HttpResponse(result, mimetype='application/json')
def NewResultFetch(condition, currentPagination,project_id,team_id,capacity):
    # pagination Code
    step = int(capacity)
    limit = ""
    limit += ("limit " + str(step))
    # ##determine offset
    offset = ""
    stepDelete = int(step) * int(int(currentPagination) - 1)
    offset += ("offset " + str(stepDelete))
    print condition
    total_query = "select * from ((select ter.run_id as run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(now()-ter.teststarttime,'HH24:MI:SS') as Duration, tre.branch_version,tre.test_milestone,ter.teststarttime as starttime " 
    total_query += "from test_run_env tre, test_env_results ter ,machine_project_map mpm " 
    total_query += "where tre.run_id=ter.run_id and mpm.machine_serial=tre.id and ter.status=tre.status and ter.status in ('Submitted','In-Progress')"
    if project_id!="ALL":
        total_query+=" and mpm.project_id='%s'"%project_id
    if team_id!="ALL":
        total_query+=" and mpm.team_id=%d"%int(team_id)
    if condition != "":
        total_query += " and "
        total_query += condition
    total_query += ") "
    total_query += "union all "
    total_query += "(select ter.run_id as run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(ter.testendtime-ter.teststarttime,'HH24:MI:SS') as Duration, tre.branch_version,tre.test_milestone,ter.teststarttime as starttime " 
    total_query += "from test_run_env tre, test_env_results ter ,machine_project_map mpm " 
    total_query += "where tre.run_id=ter.run_id and tre.id=mpm.machine_serial and ter.status=tre.status and ter.status not in ('Submitted','In-Progress')"
    if project_id!="ALL":
        total_query+=" and mpm.project_id='%s'"%project_id
    if team_id!="ALL":
        total_query+=" and mpm.team_id=%d"%int(team_id)
    if condition != "":
        total_query += " and "
        total_query += condition
    total_query += ")) as A order by starttime desc,run_id asc "
    count_query = total_query
    total_query += (limit + " " + offset)
    print total_query
    Conn = GetConnection()
    total_count = DB.GetData(Conn, count_query, False)
    Conn.close()
    received_data = []
    for each in total_count:
        if each not in received_data:
            received_data.append(each)
    Conn=GetConnection()
    get_list = DB.GetData(Conn, total_query, False)
    Conn.close()
    refine_list = []
    for each in get_list:
        if each not in refine_list:
            refine_list.append(each)
    total_run = make_array(refine_list)
    print total_run
    Conn=GetConnection()
    all_status = make_status_array(Conn, total_run)
    # make Dict
    Column = ["Run ID", "Objective", "Run Type", "Tester", "Report", "Status", "Duration", "Version", "MileStone"]
    Dict = {'total':total_run, 'status':all_status, 'column':Column, 'totalGet':len(received_data)}
    Conn.close()
    return Dict
def RunID_New(request):
    if request.is_ajax():
        if request.method == 'GET':
            run_id = request.GET.get(u'run_id', '')
            run_id = run_id.replace("%3A", ":")
            index = request.GET.get(u'pagination', '')
            userText = request.GET.get(u'UserText', '')
            capacity=request.GET.get(u'capacity','')
            if(userText == ""):
                runData = GetData(run_id, index,capacity)
            else:
                userText = FormCondition(userText)
                runData = GetData(run_id, index, capacity,userText)
            print '--------------------------- INSIDE -------------------------------------'
            print run_id
            print index
            print runData['allData'][0][3]
            print '--------------------------- INSIDE -------------------------------------'
            Col = ['ID', 'Title', 'Type', 'Status', 'Duration', 'Estd. Time', 'Comment', 'Log']
            runDetail = {'runData':runData['allData'], 'runCol':Col, 'total':runData['count']}
    result = simplejson.dumps(runDetail)
    return HttpResponse(result, mimetype='application/json')
def FormCondition(userText):
    UserText = userText.replace(u'\xa0', u'|')
    UserText = UserText.split('|')
    for each in UserText:
        if each == "":
            UserText.remove(each)
    print UserText
    condition = ""
    for each in UserText:
        eachitem = each.split(":")
        if eachitem[1].strip() == 'Status':
            condition += ("tcr.status='%s' and " % eachitem[0])
        if len(eachitem[0].strip()) == 8:
            condition += ("rtc.tc_id='%s' and " % eachitem[0])
    condition = condition[:-5].strip()
    return condition
def GetData(run_id, index, capacity,userText=""):
    step = int(capacity)
    limit = ("limit " + str(step))
    # offset
    offset = ""
    offset += ("offset " + str((int(index) - 1) * int(step)))
    condition = limit + " " + offset
    print condition
    # form the query
    query = ""
    query+="select * from ("
    query+="(select rtc.tc_id,tc_name,tcr.status,to_char((tcr.testendtime-tcr.teststarttime),'HH24:MI:SS'),tcr.failreason,tcr.logid from test_case_results tcr, result_test_cases rtc  where tcr.run_id='%s' and tcr.tc_id=rtc.tc_id and rtc.run_id=tcr.run_id "%run_id
    if userText != "":
        query += "and "
        query += userText
    query += " ORDER BY tcr.id) "
    query += "union all "
    query+="(select rtc.tc_id,tc_name,'Pending','','','' from test_case_results tcr, result_test_cases rtc  where tcr.run_id='%s' and tcr.tc_id=rtc.tc_id and rtc.run_id=tcr.run_id"%run_id
    if userText != "":
        query += " and "
        query += userText
    query += " and tcr.tc_id not in (select tc_id from test_case_results where run_id = '%s') )) AS A" % run_id
    count_query = query
    query += " %s" % condition
    print query
    Conn = GetConnection()
    runData = DB.GetData(Conn, query, False)
    print runData
    AllTestCases = Modify(runData)
    AllTestCases = AddEstimatedTime(AllTestCases, run_id)
    final=[]
    for each in AllTestCases:
        temp=list(each)
        temp.append('View')
        temp.append('Execute')
        final.append(tuple(temp))
    DataCount = DB.GetData(Conn, count_query, False)
    DataReturn = {'allData':final, 'count':len(DataCount)}
    Conn.close()
    return DataReturn

def manage_test_cases(request):
    if request.method == 'GET':
        if request.is_ajax():
            # Fetch the data from product_sections table
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team_id','')
            query = "select ps.section_id,ps.section_path from product_sections ps ,team_wise_settings tws where tws.parameters=ps.section_id and tws.type='Section' and tws.project_id='%s' and tws.team_id=%d"%(project_id,int(team_id))
            # Convert the data into a list
#             data = list(DB.GetData(Conn, query, False))
            Conn = GetConnection()
            data = DB.GetData(Conn, query, False, False)
#             cur = Conn.cursor()
#             cur.execute(query)
#             data = cur.fetchall()
#             time.sleep(0.5)
            
            sections = []
            parent_sections = []
            child_sections = []
            temp_list = []
            result = []

            for i in data:
                sections.append(i[1])
            
            parent_sections = list(set(i.split('.', 1)[0] for i in sections))
            
            for i in data:
                temp = {}
                for section_name in parent_sections:
                    # If its a parent section, save it one way
                    if section_name == i[1]:
                        temp['id'] = i[0]
                        temp['text'] = i[1]
                        temp['children'] = True
                        temp['type'] = 'parent_section'
                        temp['undetermined'] = True
                        temp_list.append(temp)
                        data.remove(i)
                        
            parent_sections = temp_list
            
            for i in data:
                temp = {}
                section = i[1].split('.')
#                 print section
                for parent_section in parent_sections:
                    if section[0] == parent_section['text']:
                        temp['id'] = i[0]
                        temp['text'] = section[-1]
                        temp['type'] = 'section'
                        if len(section) == 2:
                            temp['parent'] = parent_section['id']
                            temp['parent_text'] = parent_section['text']
                        else:
                            temp['parent_text'] = section[-2]
                        
                        child_sections.append(temp)
            
            for child_section in child_sections:
                for parent_section in child_sections:
                    if 'parent' not in child_section.keys() and parent_section['text'] == child_section['parent_text']:
                        child_section['parent'] = parent_section['id']
                        parent_section['children'] = True

            for i in parent_sections:
                i['text'] = i['text'].replace('_', ' ')

            requested_id = request.GET.get('id', '')
            
            if requested_id == '#':
                result = json.dumps(parent_sections)
            else:
                print "Node with id %s is being loaded" % requested_id
                
                try:
                    if requested_id != '':
                        for section in child_sections:
                            if unicode(section['parent']) == requested_id:
                                for i in data:
                                    temp = i[1].split('.')[-1]
                                    if temp == section['text'] and section['id'] == i[0]:
                                        section['text'] = section['text'] + '<span style="display:none;">' + i[1] + '</span>'
                                        
                                        section['id'] = str(section['id'])
                                        section.pop('parent_text')
                                        section['text'] = section['text'].replace('_', ' ')
                                        
                                        result.append(section)
                        result = json.dumps(result)
                except:
                    return HttpResponse("NULL")
                    
            
            return HttpResponse(result, mimetype="application/json")

        else:
            return render(request, 'ManageTestCases.html', {})

def manage_tc_data(request):
    if request.method == 'GET':
        if request.is_ajax():
            test_case_ids = ''
            decoded_string = json.loads(request.GET.get('selected_section_ids', []))
            selected_section_ids = list(decoded_string)

            if selected_section_ids != []:
                for i in range(0, len(selected_section_ids)):
                    selected_section_ids[i] = int(selected_section_ids[i])
                
                print "Selected section ids", selected_section_ids
                
                encoded_for_sql = "name='%s'" % selected_section_ids[0]
                
                if not len(selected_section_ids) == 1:
                    for i in range(1, len(selected_section_ids)):
                        encoded_for_sql += " OR name='%s'" % selected_section_ids[i]
                
                query = '''
                SELECT * FROM test_case_tag WHERE property='%s' AND %s
                ''' % ('section_id', encoded_for_sql)
                
                Conn = GetConnection()
                data = DB.GetData(Conn, query, False, True)
                
                first = True
                for row in data:
                    if first:
                        test_case_ids = row['tc_id'] + ':'
                        first = False
                    else:
                        test_case_ids += ' %s:' % row['tc_id'] 
                
                result = json.dumps(test_case_ids)
#                 print result
                Conn.close()
                return HttpResponse(result, mimetype='application/json')
            else:
                return HttpResponse('', mimetype='application/json')
def FilterDataForRunID(request):
    if request.is_ajax():
        if request.method == 'GET':
            term = request.GET.get('term', '')
            run_id = request.GET.get('run_id', '')
            Conn = GetConnection()
            status_query = "select distinct status,'Status' from test_case_results where run_id='%s' and status Ilike '%%%s%%'" % (run_id, term)
            status = DB.GetData(Conn, status_query, False)
            test_case_name_query = "select distinct tc.tc_id,tc_name from result_test_cases tc,test_case_results tcr where tc.run_id=tcr.run_id and tcr.run_id='%s' and (tc.tc_id Ilike'%%%s%%' or tc.tc_name Ilike '%%%s%%')" % (run_id, term, term)
            test_case_name = DB.GetData(Conn, test_case_name_query, False)
            final = []
            for each in status:
                if each not in final:
                    final.append(each)
            for each in test_case_name:
                if each not in final:
                    final.append(each)
    result = simplejson.dumps(final)
    Conn.close()
    return HttpResponse(result, mimetype='application/json')

def create_section(request):
    if request.method == 'GET' and request.is_ajax():
        section_text = request.GET.get('section_text', '')
        empty_section_id = None
        Conn = GetConnection()
        cur = Conn.cursor()
        query = '''
        SELECT section_id FROM product_sections
        '''
        
        data = DB.GetData(Conn, query, False, False)
        data = sorted(data)
        time.sleep(0.5)
        empty_section_id = int(data[-1][0]) + 1

        try:
            query = '''
            INSERT INTO product_sections VALUES (%d, '%s')
            ''' % (empty_section_id, section_text)
            time.sleep(0.5)
            
            cur.execute(query)
            Conn.commit()
            cur.close()

            return HttpResponse(1)
        except:
            cur.close()
            return HttpResponse(0)
        

def rename_section(request):
    if request.method == 'GET' and request.is_ajax():
        
        section_id = int(request.GET.get('section_id', ''))
        section_path = request.GET.get('section_path', '')
        new_text = request.GET.get('new_text', '')
        
        old_section_text = ''
        Conn=GetConnection()
        cur = Conn.cursor()
        
        temp = section_path.split('.')
        old_section_text = temp[-1]
        temp[-1] = new_text
        temp = '.'.join(temp)
        new_section_path = temp
        
        try:
            query = '''
            UPDATE product_sections SET section_path='%s' WHERE section_id=%d
            ''' % (new_section_path, section_id)
            time.sleep(0.5)
             
            cur.execute(query)
            Conn.commit()
                     
            query = '''
            UPDATE test_case_tag SET name='%s' WHERE name='%s' AND property='%s'
            ''' % (new_text, old_section_text, 'Section')
            time.sleep(0.5)
              
            cur.execute(query) 
            Conn.commit()
            cur.close()
        except:
            cur.close()
            return HttpResponse(0)                  
        return HttpResponse(1)


def delete_section(request):
    if request.method == 'GET' and request.is_ajax():
        section_id = int(request.GET.get('section_id', 0))
        query = '''
        DELETE FROM product_sections WHERE section_id=%d 
        ''' % section_id
        Conn = GetConnection()
        cur = Conn.cursor()
        cur.execute(query)
        Conn.commit()
        time.sleep(1)
        cur.close()
        return HttpResponse(section_id)
def DeleteTestCase(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            test_case_list = request.GET.get(u'Query', '')
            test_case_list = test_case_list.split("|")
            modified_test_case_list = TestCaseCreateEdit.Delete_Test_Case(Conn, test_case_list)
    result = simplejson.dumps(modified_test_case_list)
    return HttpResponse(result, mimetype='application/json')

def contact_page(request):
    return render(request, 'ContactForm.html', {})

def contact_page_with_url(request, url):
    return render(request, 'ContactForm.html', {'url': url})


#Test Set and Tag Redone.
def TestSetTagHome(request):
    return render_to_response('TestSetTag.html',{})

def GetSetTag(request):
    if request.is_ajax():
        if request.method=='GET':
            value=request.GET.get(u'term','')
            print value
            list_value=["set","tag"]
            conn=GetConnection()
            final=[]
            for each in list_value:
                #form query
                query="select distinct value from config_values where type='%s' and value iLike'%%%s%%'"%(each.strip(),value.strip())
                if value=="":
                    query="select distinct value from config_values where type='%s'"%(each.strip())
                if DB.IsDBConnectionGood(conn)==False:
                    time.sleep(1)
                    conn=GetConnection()
                get_list=DB.GetData(conn,query)
                temp=[]
                for eachitem in get_list:
                    if eachitem not in temp:
                        temp.append(eachitem)
                #if len(temp)!=0:
                final.append((each,temp))            
    result=simplejson.dumps(final)
    return HttpResponse(result,mimetype='application/json')
def SetTagEdit(request,type,name):
    return render_to_response('TestSetTagEdit.html',{})
def createNewSetTag(request):
    if request.is_ajax():
        if request.method=='GET':
            type_tag=request.GET.get(u'type','')
            name=request.GET.get(u'name','')
            if type_tag=='SET':
                type_tag='set'
            if type_tag=='TAG':
                type_tag='tag'
            available_query="select count(*) from config_values where value='%s' and type='%s'"%(name.strip(),type_tag.strip())
            Conn=GetConnection()
            available_count=DB.GetData(Conn,available_query)
            if available_count[0]==0:
                #from dictionary
                Dict={'type':type_tag.strip(),'value':name.strip()}
                result=DB.InsertNewRecordInToTable(Conn, "config_values",**Dict)
                if result==True:
                    message="Test %s with name '%s' created successfully."%(type_tag.strip(),name.strip())
                else:
                    message="Failed DataBaseError."
            else:
                message="Failed to create.Test %s with name '%s' exists already."%(type_tag.strip(),name.strip())
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
def DeleteSetTag(request):
    if request.is_ajax():
        if request.method=='GET':
            type_tag=request.GET.get(u'type','')
            name=request.GET.get(u'name','')
            if type_tag=='SET':
                type_tag='set'
            if type_tag=='TAG':
                type_tag='tag'
            available_query="select count(*) from config_values where value='%s' and type='%s'"%(name.strip(),type_tag.strip())
            Conn=GetConnection()
            available_count=DB.GetData(Conn,available_query)
            if available_count[0]>0:
                test_case_tag_result=DB.DeleteRecord(Conn, "test_case_tag",name=name.strip(), property=type_tag.strip())
                config_values_result=DB.DeleteRecord(Conn, "config_values",value=name.strip(),type=type_tag.strip())
                if test_case_tag_result ==True and config_values_result ==True: 
                    message="Test %s with name %s is deleted succesfully"%(type_tag.strip(),name.strip())
                else:
                    message="Failed.DataBaseError."
            else:
                message="Failed.No Test %s with name %s is found in DataBase"%(type_tag.strip(),name.strip())
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
def AddTestCasesSetTag(request):
    if request.is_ajax():
        if request.method=='GET':
            message=""
            type_tag=request.GET.get(u'type','')
            name=request.GET.get(u'name','')
            #name = name.replace("%20", " ")
            test_case_list=request.GET.get(u'list','').split('|')
            print test_case_list
            if type_tag=='SET':
                type_tag='set'
            if type_tag=='TAG':
                type_tag='tag'
            available_query="select count(*) from config_values where value='%s' and type='%s'"%(name.strip(),type_tag.strip())
            Conn=GetConnection()
            available_count=DB.GetData(Conn,available_query)
            if available_count[0]>0:
                added_list=[]
                for each in test_case_list:
                    #form directory
                    query="select count(*) from test_case_tag where tc_id='%s' and name='%s' and property='%s'"%(each.strip(),name.strip(),type_tag.strip())
                    if DB.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    count=DB.GetData(Conn,query)
                    if count[0]==0:
                        result=DB.InsertNewRecordInToTable(Conn,"test_case_tag",tc_id=each.strip(),name=name.strip(),property=type_tag.strip())
                        if result==True:
                            added_list.append(each)
                    else:
                        added_list.append(each)
                if len(added_list)>0:
                    message="%s added to Test %s:%s"%(",".join(added_list),type_tag.strip(),name.strip())
                else:
                    message="No Test Cases added to Test %s: %s"%(type_tag.strip(),name.strip())
            else:
                message="Failed.No Test %s with name %s exists."%(type_tag.strip(),name.strip())
            
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
def DeleteTestCasesSetTag(request):
    if request.is_ajax():
        if request.method=='GET':
            message=""
            type_tag=request.GET.get(u'type','')
            name=request.GET.get(u'name','')
            #name = name.replace("%20", " ")
            test_case_list=request.GET.get(u'list','').split('|')
            print test_case_list
            if type_tag=='SET':
                type_tag='set'
            if type_tag=='TAG':
                type_tag='tag'
            available_query="select count(*) from config_values where value='%s' and type='%s'"%(name.strip(),type_tag.strip())
            Conn=GetConnection()
            available_count=DB.GetData(Conn,available_query)
            if available_count[0]>0:
                added_list=[]
                for each in test_case_list:
                    #form directory
                    query="select count(*) from test_case_tag where tc_id='%s' and name='%s' and property='%s'"%(each.strip(),name.strip(),type_tag.strip())
                    if DB.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    count=DB.GetData(Conn,query)
                    if count[0]>0:
                        result=DB.DeleteRecord(Conn,"test_case_tag",tc_id=each.strip(),name=name.strip(),property=type_tag.strip())
                        if result==True:
                            added_list.append(each)
                if len(added_list)>0:
                    message="%s deleted from Test %s:%s"%(",".join(added_list),type_tag.strip(),name.strip())
                else:
                    message="No Test Cases deleted from Test %s: %s"%(type_tag.strip(),name.strip())
            else:
                message="Failed.No Test %s with name %s exists."%(type_tag.strip(),name.strip())
            
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
def UpdateSetTag(request):
    if request.is_ajax():
        if request.method=='GET':
            message=""
            type_tag=request.GET.get(u'type','')
            new_name=request.GET.get(u'new_name','')
            old_name=request.GET.get(u'old_name','')
            if type_tag=='SET':
                type_tag='set'
            if type_tag=='TAG':
                type_tag='tag'
            available_query="select count(*) from config_values where value='%s' and type='%s'"%(old_name.strip(),type_tag.strip())
            Conn=GetConnection()
            available_count=DB.GetData(Conn,available_query)
            if available_count[0]>0:
                test_case_get_query="select distinct tc_id from test_case_tag where name='%s' and property='%s'"%(old_name.strip(),type_tag.strip())
                test_cases=DB.GetData(Conn,test_case_get_query)
                added_list=[]
                for each in test_cases:
                    query="select count(*) from test_case_tag where tc_id='%s' and name='%s' and property='%s'"%(each.strip(),old_name.strip(),type_tag.strip())
                    if DB.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    count=DB.GetData(Conn,query)
                    if count[0]>0:
                        whereQuery="where tc_id='%s' and name='%s' and property='%s'"%(each.strip(),old_name.strip(),type_tag.strip())
                        result=DB.UpdateRecordInTable(Conn,"test_case_tag",whereQuery,tc_id=each.strip(),name=new_name.strip(),property=type_tag.strip())
                        if result==True:
                            added_list.append(each)
                whereQuery="where value='%s' and type='%s'"%(old_name.strip(),type_tag.strip())
                result=DB.UpdateRecordInTable(Conn,"config_values",whereQuery,value=new_name.strip())
                if len(added_list)>0 and result==True:
                    message="Updated Test %s:%s with %s"%(type_tag.strip(),old_name.strip(),new_name.strip())
                else:
                    message="Failed.Unable to update Test %s: %s"%(type_tag.strip(),old_name.strip())
            else:
                message="Failed.No Test %s with name %s exists."%(type_tag.strip(),old_name.strip())
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')

def select2(request):
    return render(request, 'select2.html', {})
"""def manageMilestone(request):
    return render_to_response('Milestone.html',{})"""
    
def Milestone(request):
    now=datetime.datetime.now().date()
    Conn=GetConnection()
    query="select * from milestone_info order by name"
    milestones=DB.GetData(Conn,query,False)
    """query="(select count(distinct run_id) from test_run_env where status='Complete' group by test_milestone)"
    complete=DB.GetData(Conn,query)
    query="select count(distinct run_id) from test_run_env where status not in ('Cancelled') group by test_milestone"
    all=DB.GetData(Conn,query)
    temp = []
    for x in zip(complete,all):
        temp.append(format((float(x[0])*100)/float(x[1]),'.2f'))"""
    milestone_list = []
    #i=0
    for each in milestones:
        data = []
        for x in each:
            data.append(x)
        #data.append(temp[i])
        complete = DB.GetData(Conn, "select cast(count(distinct run_id) as text) from test_run_env where test_milestone like '%"+each[1]+"%' and status='Complete'")
        all=DB.GetData(Conn,"select cast(count(distinct run_id) as text) from test_run_env where status not in ('Cancelled') and test_milestone like '%"+each[1]+"%'")
        for x in zip(complete,all):
            if x[1]=='0':
                data.append(0)
            else:
                data.append(format((float(x[0])*100)/float(x[1]),'.2f'))
        
        data.append(int(all[0])-int(complete[0]))
        data.append(int(complete[0]))
        """data.append(all[i]-complete[i])
        data.append(complete[i])"""
        left = (each[3]-now).days
        if left<0 and data[4]!='complete':
            data.append(-left)
            data.append("Past due by ")
            data.append('red')
        elif left<0 and data[4]=='complete':
            data.append(-left)
            data.append("Finished ago by ")
            data.append('green')
        else:
            data.append(left)
            data.append("Left only ")
            data.append('green')
        #i = i+1
        milestone_list.append(data)
        
        
    Dict={
          'milestone_list':milestone_list
    }
    Conn.close()
    return render_to_response('ManageMilestone.html',Dict)

def manageMilestone(request):
    Conn=GetConnection()
    query="select project_id, project_name from projects"
    project_info=DB.GetData(Conn,query,False)
    query="select id,value from config_values where type='milestone'"
    milestone_info=DB.GetData(Conn,query,False)
    #get the current projects team info
    query="select distinct id,value from config_values where type='Team'"
    team_info=DB.GetData(Conn,query,False)
    #get the existing requirement id for parenting
    #query="select distinct requirement_id,requirement_title from requirements where project_id='%s' order by requirement_id"%project_id
    #requirement_list=DB.GetData(Conn,query,False)
    Dict={
          #'project_id':project_id,
          #'project_list':project_info,
          #'milestone_list':milestone_info,
          'team_info':team_info
          #'requirement_list':requirement_list
    }
    Conn.close()
    return render_to_response('Milestone.html',Dict)
def ManageTask(request):
    #get the distinct milestone from the task table
    query="select id,value from config_values where id in(select cast(tasks_milestone as int) from tasks)"
    Conn=GetConnection()
    tasks_milestone_id=DB.GetData(Conn,query,False)
    final=[]
    for each in tasks_milestone_id:
        query="select tasks_id,tasks_title from tasks where tasks_milestone='%s'"%each[0]
        testConnection(Conn)
        task_id=DB.GetData(Conn,query,False)
        final.append((each,task_id))
    Dict={
          'milestone_list':final
    }  
    Conn.close()  
    return render_to_response('ManageTask.html',Dict)

def EditTask(request,task_id,project_id):
    task_id = request.GET.get('task_id', '')
    project_id = request.GET.get('project_id', '')
    
    if task_id != "":
        return render_to_response('CreateNewTask.html')
    else:
        Conn=GetConnection()
        query="select id,value from config_values where id in(select cast(team_id as int) from project_team_map)"
        team_info=DB.GetData(Conn,query,False)
        query="select value from config_values where type='Priority'"
        priority=DB.GetData(Conn,query,False)
        query="select id,value from config_values where type='milestone'"
        milestone_list=DB.GetData(Conn,query,False)
        #get the names from permitted_user_list
        query="select pul.user_id,user_names,user_level from permitted_user_list pul,team_info ti where pul.user_level='assigned_tester' and pul.user_id=cast(ti.user_id as int) and team_id in (select cast(team_id as int) from project_team_map)" 
        user_list=DB.GetData(Conn,query,False)
        query = "select label_id,label_name,Label_color from labels order by label_name"
        labels = DB.GetData(Conn,query,False)
        Dict={
              'team_info':team_info,
              'priority_list':priority,
              'milestone_list':milestone_list,
              'user_list':user_list,
              'labels':labels
        }
    return render_to_response("CreateNewTask.html",Dict)

def ChildTask(request,task_id,project_id):
    task_id = request.GET.get('task_id', '')
    project_id = request.GET.get('project_id', '')
    
    if task_id != "":
        return render_to_response('CreateNewTask.html')
    else:
        Conn=GetConnection()
        query="select id,value from config_values where id in(select cast(team_id as int) from project_team_map)"
        team_info=DB.GetData(Conn,query,False)
        query="select value from config_values where type='Priority'"
        priority=DB.GetData(Conn,query,False)
        query="select id,value from config_values where type='milestone'"
        milestone_list=DB.GetData(Conn,query,False)
        #get the names from permitted_user_list
        query="select pul.user_id,user_names,user_level from permitted_user_list pul,team_info ti where pul.user_level='assigned_tester' and pul.user_id=cast(ti.user_id as int) and team_id in (select cast(team_id as int) from project_team_map)" 
        user_list=DB.GetData(Conn,query,False)
        query = "select label_id,label_name,Label_color from labels order by label_name"
        labels = DB.GetData(Conn,query,False)
        Dict={
              'team_info':team_info,
              'priority_list':priority,
              'milestone_list':milestone_list,
              'user_list':user_list,
              'labels':labels
        }
    return render_to_response("CreateNewTask.html",Dict)


def Selected_TaskID_Analaysis(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Selected_Task_Analysis', '')

        query = "select tasks_title,tasks_description,cast(tasks_startingdate as text),cast(tasks_endingdate as text),tasks_priority,tasks_milestone,tasks_createdby,cast(tasks_creationdate as text),tasks_modifiedby,cast(tasks_modifydate as text),parent_id,status,tester,project_id from tasks where tasks_id = '%s'" % UserData
        Task_Info = DB.GetData(Conn, query, False)
        
        query = "select pul.user_names from tasks t,permitted_user_list pul where tasks_id = '%s' and t.tester::int=pul.user_id" % UserData
        tester = DB.GetData(Conn, query)
        
        query = "select pf.feature_path from feature_map fm, product_features pf where fm.id='%s' and fm.type='TASK' and fm.feature_id=pf.feature_id::text" % UserData
        feature = DB.GetData(Conn, query, False)
        
        query = "select distinct tc.tc_id, tc.tc_name from components_map btm, test_cases tc where btm.id1 = '%s' and btm.id2=tc.tc_id and type1='TASK' and type2='TC'" % UserData
        cases = DB.GetData(Conn,query,False)
        
        #query = "select mi.name from milestone_info mi, tasks t where mi.id::text=t.tasks_milestone and t.tasks_id='%s'" %UserData
        #milestone = DB.GetData(Conn,query)
        
        
        query = "select l.label_id,l.label_name,l.Label_color from labels l, label_map lm where l.label_id=lm.label_id and lm.id='%s' and lm.type='TASK' order by label_name" % UserData
        labels = DB.GetData(Conn,query)
        
        query = "select distinct r.requirement_id,r.requirement_title,r.status,mi.name from requirements r, milestone_info mi, components_map cm where r.requirement_milestone=mi.id::text and cm.id1=r.requirement_id and cm.id2='%s' and cm.type1='REQ' and cm.type2='TASK'" %UserData
        reqs = DB.GetData(Conn,query,False)
        
        #query = "select team_id from task_team_map where task_id='%s'" %UserData
        #team = DB.GetData(Conn,query)
        
        """query = "select task_path from task_sections where task_path ~ '*.%s'" %UserData.replace('-','_')
        section = DB.GetData(Conn,query)
        section = section.replace('_', '-')
        section = section.split('.')
        parents = []
        for each in section:
            query = "select ts.task_path, t.tasks_id, t.status, mi.name from tasks t, milestone_info mi, task_sections ts where t.tasks_id = '%s' and t.tasks_milestone=mi.id::text and ts.task_path ~ '*.%s'" %(each,each.replace('-','_'))
            temp = DB.GetData(Conn,query,False)
            parents.append(temp)"""

    Heading = ['Path','Task-ID','Status','Milestone']
    results = {'Task_Info':Task_Info, 'tester':tester, 'Feature':feature[0][0], 'labels':labels, 'cases':cases, 'reqs':reqs}
    json = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(json, mimetype='application/json')


def Selected_Requirement_Analaysis(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'req_id', '')

        query = "select requirement_title,status,requirement_description,cast(requirement_startingdate as text), cast(requirement_endingdate as text),requirement_priority,requirement_milestone from requirements where requirement_id = '%s'" % UserData
        Req_Info = DB.GetData(Conn, query, False)
        
        
        query = "select pf.feature_path from feature_map fm, product_features pf where fm.id='%s' and fm.type='REQ' and fm.feature_id=pf.feature_id::text" % UserData
        feature = DB.GetData(Conn, query, False)
        
        #query = "select mi.name from milestone_info mi, tasks t where mi.id::text=t.tasks_milestone and t.tasks_id='%s'" %UserData
        #milestone = DB.GetData(Conn,query)
        query = "select team_id from requirement_team_map where requirement_id='%s'" %UserData
        teams = DB.GetData(Conn,query)
        
        
        query = "select l.label_id,l.label_name,l.Label_color from labels l, label_map lm where l.label_id=lm.label_id and lm.id='%s' and lm.type='REQ' order by label_name" % UserData
        labels = DB.GetData(Conn,query)
        
        query = "select distinct t.tasks_id, tasks_title, tasks_description ,cast(tasks_startingdate as text),cast(tasks_endingdate as text),mi.name,t.status from components_map cm, tasks t, milestone_info mi where mi.id::text=t.tasks_milestone and id1='%s' and type1='REQ' and type2='TASK' and t.tasks_id=cm.id2" % UserData
        tasks = DB.GetData(Conn,query,False)
        
        query = "select distinct tc.tc_id, tc.tc_name from components_map btm, test_cases tc where btm.id1 = '%s' and btm.id2=tc.tc_id and type1='REQ' and type2='TC'" % UserData
        cases = DB.GetData(Conn,query,False)
        
        #query = "select team_id from task_team_map where task_id='%s'" %UserData
        #team = DB.GetData(Conn,query)
        
        """query = "select task_path from task_sections where task_path ~ '*.%s'" %UserData.replace('-','_')
        section = DB.GetData(Conn,query)
        section = section.replace('_', '-')
        section = section.split('.')
        parents = []
        for each in section:
            query = "select ts.task_path, t.tasks_id, t.status, mi.name from tasks t, milestone_info mi, task_sections ts where t.tasks_id = '%s' and t.tasks_milestone=mi.id::text and ts.task_path ~ '*.%s'" %(each,each.replace('-','_'))
            temp = DB.GetData(Conn,query,False)
            parents.append(temp)"""

    #Heading = ['Path','Task-ID','Status','Milestone']
    results = {'Req_Info':Req_Info, 'Feature':feature[0][0], 'labels':labels, 'teams':teams, 'tasks':tasks, 'cases':cases}
    json = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(json, mimetype='application/json')



def FetchProject(request):
    if request.is_ajax():
        if request.method=='GET':
            query="select project_id from projects"
            Conn=GetConnection()
            project=DB.GetData(Conn,query)
            query="select distinct value from config_values where type='Team'"
            team=DB.GetData(Conn,query)
            query="select distinct user_names from permitted_user_list where user_level='manager'"
            manager=DB.GetData(Conn,query)
            Conn.close()
    result={'project':project,'team':team,'manager':manager}
    result=simplejson.dumps(result)
    return HttpResponse(result,mimetype='application/json')
def ManageBug(request):
    now=datetime.datetime.now().date()
    query="select * from bugs"
    Conn=GetConnection()
    bugs=DB.GetData(Conn, query, False)
    """bugs = []
    for each in bugs_list:
        data = []
        for x in each:
            data.append(x)
        milestone=DB.GetData(Conn, "select mi.id, mi.name from bugs b, milestone_info mi where b.bug_milestone::int=mi.id and b.bug_id='"+each[0]+"'",False)
        data.append(milestone[0][0])
        data.append(milestone[0][1])
        #ago = (now-x[8]).days + " days ago by "
        #data.append(ago)
        bugs.append(data)"""
    query="select * from label_map"
    labels=DB.GetData(Conn, query, False)
    query="select * from milestone_info"
    milestones=DB.GetData(Conn, query, False)
    Dict={'bugs':bugs, 'labels':labels, 'milestones':milestones}
    Conn.close()
    return render_to_response('ManageBug.html',Dict)

def Bugs_List(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            team = request.GET.get(u'team', '')

        now=datetime.datetime.now().date()
        #query="select bug_id, bug_title, bug_description, cast(bug_startingdate as text), cast(bug_endingdate as text), bug_priority, bug_milestone, bug_createdby, cast(bug_creationdate as text), bug_modifiedby, cast(bug_modifydate as text), status, team_id, project_id, tester from bugs"
        query="select distinct bug_id,bug_title,bug_description,cast(bug_startingdate as text),cast(bug_endingdate as text),mi.name,b.status from bugs b, milestone_info mi where b.bug_milestone::int=mi.id order by b.bug_id desc"
        bugs=DB.GetData(Conn, query, False)
        
        query="select blm.bug_id,l.label_id,l.label_name,l.label_color from labels l, label_map blm where l.label_id=blm.label_id"
        labels=DB.GetData(Conn, query, False)
        #query="select * from milestone_info"
        #milestones=DB.GetData(Conn, query, False)
        
    Heading = ['Bug-ID','Title','Description','Starting Date','Due Date','Milestone', 'Status']    
    results = {'Heading':Heading,'bugs':bugs, 'labels':labels}
    json = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(json, mimetype='application/json')

def Tasks_List(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            project_id = request.GET.get(u'project_id', '')
            team_id = request.GET.get(u'team_id', '')

        now=datetime.datetime.now().date()
        tasks_list = []
        #query="select bug_id, bug_title, bug_description, cast(bug_startingdate as text), cast(bug_endingdate as text), bug_priority, bug_milestone, bug_createdby, cast(bug_creationdate as text), bug_modifiedby, cast(bug_modifydate as text), status, team_id, project_id, tester from bugs"
        #query="select distinct tasks_id,tasks_title,tasks_description,cast(tasks_startingdate as text),cast(tasks_endingdate as text),mi.name,t.status from tasks t, milestone_info mi,requirement_sections rs,task_team_map ttm where mi.id::text=t.tasks_milestone and t.project_id='"+project_id+"' and t.parent_id=rs.requirement_path_id::text and ttm.task_id=t.tasks_id and ttm.team_id='"+team_id+"' order by tasks_id desc"
        query="select distinct tasks_id,tasks_title,tasks_description,cast(tasks_startingdate as text),cast(tasks_endingdate as text),mi.name,t.status from tasks t, milestone_info mi where mi.id::text=t.tasks_milestone and t.project_id='"+project_id+"' and t.team_id='"+team_id+"' order by tasks_id desc"
        tasks=DB.GetData(Conn, query, False)
        
        query="select task_path from tasks t,task_sections rs where t.project_id='"+project_id+"' and t.parent_id=rs.task_path_id::text and t.team_id='"+team_id+"' order by tasks_id desc"
        parents=DB.GetData(Conn, query, False)
        
            
        for x in zip(tasks,parents):
            data = []
            for y in x[0]:
                data.append(y)
            temp=x[1][0].replace('_','-')
            temp=temp.replace('.','/')
            if temp==data[0]:
                data.append('None')
            else:
                data.append(temp)
            #data.append(x[1])
            tasks_list.append(data)
    
        
    Heading = ['Task-ID','Title','Description','Starting Date','Due Date','Milestone', 'Status', 'Parent']    
    results = {'Heading':Heading,'tasks':tasks_list}
    json = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(json, mimetype='application/json')


def Reqs_List(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            project_id = request.GET.get(u'project_id', '')

        now=datetime.datetime.now().date()
        reqs_list = []
        #query="select bug_id, bug_title, bug_description, cast(bug_startingdate as text), cast(bug_endingdate as text), bug_priority, bug_milestone, bug_createdby, cast(bug_creationdate as text), bug_modifiedby, cast(bug_modifydate as text), status, team_id, project_id, tester from bugs"
        query="select distinct requirement_id,requirement_title,requirement_description,cast(requirement_startingdate as text),cast(requirement_endingdate as text),mi.name,r.status from requirements r,milestone_info mi where project_id='"+project_id+"' and mi.id::text=r.requirement_milestone order by requirement_id desc"
        reqs=DB.GetData(Conn, query, False)
        
        query="select requirement_path from requirements r,requirement_sections rs where project_id='"+project_id+"' and r.parent_requirement_id=rs.requirement_path_id::text order by requirement_id desc"
        parents=DB.GetData(Conn, query, False)
        
            
        for x in zip(reqs,parents):
            data = []
            for y in x[0]:
                data.append(y)
            temp=x[1][0].replace('_','-')
            temp=temp.replace('.','/')
            if temp==data[0]:
                data.append('None')
            else:
                data.append(temp)
            #data.append(x[1])
            reqs_list.append(data)
    
        
    Heading = ['REQ-ID','Title','Description','Starting Date','Due Date','Milestone', 'Status', 'Parent']    
    results = {'Heading':Heading,'reqs':reqs_list}
    json = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(json, mimetype='application/json')


def CreateBug(request):
    query="select project_id from projects"
    Conn=GetConnection()
    project=DB.GetData(Conn,query)
    query="select distinct value from config_values where type='Team'"
    team=DB.GetData(Conn,query)
    query="select distinct user_names from permitted_user_list where user_level='manager'"
    manager=DB.GetData(Conn,query)
    query="select label_name, label_color, label_id from labels order by label_name"
    labels=DB.GetData(Conn,query,False)
    query="select distinct tc_id,tc_name from test_cases where tc_id not in (select id2 from components_map) order by tc_id"
    cases=DB.GetData(Conn,query,False)
    query="select id,value from config_values where type='milestone'"
    milestone_list=DB.GetData(Conn,query,False)
    Dict={'project':project,'team':team,'manager':manager,'labels':labels,'cases':cases,'milestone_list':milestone_list}
    Conn.close()
    return render_to_response('CreateBug.html',Dict)

def BugSearch(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        # Ignore queries shorter than length 3
        # if len(value) > 1:
        # results = DB.GetData(Conn,"Select DISTINCT name from test_case_tag where name != 'Dependency' and name Ilike '%" + value + "%'")
        # results = DB.GetData(Conn, "Select DISTINCT tc_id from test_cases")
        results = DB.GetData(Conn, "Select DISTINCT bug_id,bug_title from bugs where bug_id Ilike '%" + value + "%' or bug_title Ilike '%" + value + "%'", False)

    results = list(set(results))
    json = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(json, mimetype='application/json')

def Selected_BugID_Analaysis(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Selected_Bug_Analysis', '')

        query = "select distinct bug_id, bug_title, bug_description, cast(bug_startingdate as text), cast(bug_endingdate as text), bug_priority, bug_milestone, bug_createdby, cast(bug_creationdate as text), bug_modifiedby, cast(bug_modifydate as text), status, team_id, project_id, tester from bugs where bug_id = '%s'" % UserData
        Bug_Info = DB.GetData(Conn, query, False)
        
        query = "select distinct l.label_id from label_map blm, labels l where blm.id = '%s' and blm.label_id = l.label_id" % UserData
        Bug_Labels = DB.GetData(Conn, query)
        
        query = "select distinct tc.tc_id, tc.tc_name from components_map btm, test_cases tc where btm.id1 ilike '%s' and btm.id2=tc.tc_id" % UserData
        Bug_Cases = DB.GetData(Conn, query, False)
        
        query = "select distinct pul.user_names from bugs b,permitted_user_list pul where bug_id = '%s' and b.tester::int=pul.user_id" % UserData
        tester = DB.GetData(Conn, query)
        
        query = "select distinct tc.tc_id, tc.tc_name, tcr.status from test_case_results tcr, test_cases tc where tc.tc_id=tcr.tc_id and tcr.status='Failed' and tc.tc_id not in (select id2 from components_map) order by tc.tc_id"
        failed_cases = DB.GetData(Conn, query, False)
        
        query = "select pf.feature_path from feature_map fm, product_features pf where fm.id='%s' and fm.type='BUG' and fm.feature_id=pf.feature_id::text" % UserData
        feature = DB.GetData(Conn, query, False)

    results = {'Bug_Info':Bug_Info, 'Bug_Labels':Bug_Labels, 'Bug_Cases':Bug_Cases, 'tester':tester, 'Failed_Cases':failed_cases, 'Feature':feature[0][0] }
    json = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(json, mimetype='application/json')

def LogNewBug(request):
    if request.is_ajax():
        if request.method=='GET':
            #getting all the info from the messages
            try:
                Conn=GetConnection()
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team','')
                title=request.GET.get(u'title','')
                description=request.GET.get(u'description','')
                start_date=request.GET.get(u'start_date','')
                end_date=request.GET.get(u'end_date','')
                priority=request.GET.get(u'priority','')
                milestone=request.GET.get(u'milestone','')
                status=request.GET.get(u'status','')
                user_name=request.GET.get(u'user_name','')
                testers=request.GET.get(u'tester','')
                test_cases=request.GET.get(u'test_cases','')
                labels=request.GET.get(u'labels','')
                Feature_Path = request.GET.get(u'Feature_Path', '')
                
                
                test_cases=test_cases.split("|")
                labels=labels.split("|")
                #created_by=request.GET.get(u'created_by','')
                
                tester = DB.GetData(Conn, "select user_id from permitted_user_list where user_names = '"+testers+"'")
                
                start_date=start_date.split('-')
                starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
                end_date=end_date.split('-')
                ending_date=datetime.datetime(int(end_date[0].strip()),int(end_date[1].strip()),int(end_date[2].strip())).date()
    
                
                result=BugOperations.CreateNewBug(title,status,description,starting_date,ending_date,team_id,priority,milestone,project_id,user_name,tester[0],test_cases,labels,Feature_Path)
                if result!=False:
                    bug_id=result
                result=simplejson.dumps(bug_id)
                return HttpResponse(result,mimetype='application/json')
            except Exception,e:
                print "Exception:",e

def ModifyBug(request):
    if request.is_ajax():
        if request.method=='GET':
            #getting all the info from the messages
            try:
                Conn=GetConnection()
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team','')
                bug_id=request.GET.get(u'bug_id','')
                title=request.GET.get(u'title','')
                description=request.GET.get(u'description','')
                start_date=request.GET.get(u'start_date','')
                end_date=request.GET.get(u'end_date','')
                priority=request.GET.get(u'priority','')
                milestone=request.GET.get(u'milestone','')
                status=request.GET.get(u'status','')
                user_name=request.GET.get(u'user_name','')
                testers=request.GET.get(u'tester','')
                test_cases=request.GET.get(u'test_cases','')
                labels=request.GET.get(u'labels','')
                Feature_Path = request.GET.get(u'Feature_Path', '')
                
                
                test_cases=test_cases.split("|")
                labels=labels.split("|")
                #created_by=request.GET.get(u'created_by','')
                
                tester = DB.GetData(Conn, "select user_id from permitted_user_list where user_names = '"+testers+"'")
                
                start_date=start_date.split('-')
                starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
                end_date=end_date.split('-')
                ending_date=datetime.datetime(int(end_date[0].strip()),int(end_date[1].strip()),int(end_date[2].strip())).date()
    
                
                result=BugOperations.EditBug(bug_id,title,status,description,starting_date,ending_date,team_id,priority,milestone,project_id,user_name,tester[0],test_cases,labels,Feature_Path)
                if result!=False:
                    bugid=result
                result=simplejson.dumps(bugid)
                return HttpResponse(result,mimetype='application/json')
            except Exception,e:
                print "Exception:",e


def BugOperation(request):
    if request.is_ajax():
        if request.method == 'GET':
            now=datetime.datetime.now().date()
            Conn = GetConnection()
            operation = request.GET.get(u'operation', '')
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team','')
            title=request.GET.get(u'title','')
            description=request.GET.get(u'bug_desc','')
            start_date=request.GET.get(u'start_date','')
            end_date=request.GET.get(u'end_date','')
            priority=request.GET.get(u'priority','')
            milestone=request.GET.get(u'milestone','')
            status=request.GET.get(u'status','')
            user_name=request.GET.get(u'user_name','')
            testers=request.GET.get(u'testers','').split("|")
            created_by=request.GET.get(u'created_by','')
            confirm_message = ""
            error_message = ""
            """if operation == "2":
                new_name = request.GET.get(u'new_name', '')
                old_name = request.GET.get(u'old_name', '')
                old_name = old_name.strip()
                modified_by = request.GET.get(u'modified_by','')
                start_date = request.GET.get(u'start_date','').strip()
                end_date = request.GET.get(u'end_date','').strip()
                start_date=start_date.split('-')
                starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
                end_date=end_date.split('-')
                ending_date=datetime.datetime(int(end_date[0].strip()),int(end_date[1].strip()),int(end_date[2].strip())).date()
                query = "select count(*) from config_values where type='milestone' and value='%s'" % old_name
                available = DB.GetData(Conn, query)
                if(available[0] > 0):
                    condition = "where type='milestone' and value='%s'" % old_name
                    mid = DB.GetData(Conn,"select id from config_values where type='milestone' and value = '"+old_name+"'")
                    Dict = {'value':new_name.strip()}
                    print DB.UpdateRecordInTable(Conn, "config_values", condition, **Dict)            
                    mcondition = "where id='%s' and name='%s'" % (mid[0],old_name)
                    mDict = {'name':new_name, 'starting_date':starting_date, 'finishing_date':ending_date,'status':status,'description':description,'modified_by':modified_by,'modified_date':now}
                    print DB.UpdateRecordInTable(Conn, "milestone_info", mcondition, **mDict)
                    result = DB.DeleteRecord(Conn,"milestone_team_map",milestone_id=mid[0])
                    for each in team_id:
                        team_Dict={
                                   'milestone_id':mid[0],
                                   'team_id':each.strip(),
                        }
                        result=DB.InsertNewRecordInToTable(Conn,"milestone_team_map",**team_Dict)
                    confirm_message = "MileStone is modified"
                else:
                    confirm_message = "No milestone is found"    """
            # start Create Operation
            if operation == "1":
                query="select nextval('bugid_seq')"
                bug_id=DB.GetData(Conn, query)
                bug_id=('BUG-'+str(bug_id[0]))
                bug_id=bug_id.strip()
                query = "select count(*) from bugs where bug_title='%s'" % title
                available = DB.GetData(Conn, query)
                if(available[0] == 0):
                    Dict={
                          'bug_id':bug_id,
                          'bug_title':title,
                          'bug_description':description,
                          'bug_startingdate':start_date,
                          'bug_endingdate':end_date,
                          'bug_priority':priority,
                          'bug_milestone':milestone,
                          'bug_createdby':created_by,
                          'bug_creationdate':now,
                          'bug_modifiedby':user_name,
                          'bug_modifydate':now,
                          'status':status,
                          'tester':testers,
                          'team_id':team_id,
                          'project_id':project_id
                    }
                    result=DB.InsertNewRecordInToTable(Conn,"bugs",**Dict)
                    if(result):
                        confirm_message = "Bug is logged Successfully!"
                    else:
                        error_message = "Database Error!"
                else:
                    error_message = "Bug name exists. Can't create a new one!"
                # start  Operation
            """if operation == "3":
                new_name = request.GET.get(u'new_name', '')
                new_name = new_name.strip()
                query = "select count(*) from config_values where type='milestone' and value='%s'" % new_name
                available = DB.GetData(Conn, query)
                if(available[0] > 0):
                    Dict = {'type':'milestone', 'value':new_name.strip()}
                    print DB.DeleteRecord(Conn, "config_values", **Dict)
                    mid = DB.GetData(Conn,"select id from config_values where type='milestone' and value = '"+new_name+"'")
                    mDict = {'id':mid[0], 'name':new_name}
                    print DB.DeleteRecord(Conn, "milestone_info", **mDict)
                    confirm_message = "MileStone is deleted Successfully"
                else:
                    error_message = "MileStone Not Found"  """
    results = {'confirm_message':confirm_message,
             'error_message':error_message,
             'bug_id':bug_id
             }
    result = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(result, mimetype='application/json')    

def ManageLabel(request):
    query = "select label_name, label_color, label_id from labels order by label_name"
    Conn=GetConnection()
    labels=DB.GetData(Conn,query,False)
    Dict={'labels':labels}
    Conn.close()
    return render_to_response('ManageLabel.html',Dict)

def CreateLabel(request):
    if request.is_ajax():
        if request.method=='GET':
            label_name = request.GET.get(u'name','').strip()
            label_color = request.GET.get(u'color','').strip()
            Conn=GetConnection()
            query="select nextval('labelid_seq')"
            label_id=DB.GetData(Conn, query)
            label_id=('LABEL-'+str(label_id[0]))
            label_id=label_id.strip()
            final = []
            sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
            Dict = {
                    'label_id':label_id,
                    'label_name':label_name,
                    'label_color':label_color
                    }
            testConnection(Conn)
            result = DB.InsertNewRecordInToTable(Conn,"labels",**Dict)
            #result = DB.InsertNewRecordInToTable(Conn, "bugs", bug_id=bug_id, bug_title=title, bug_description=description, bug_startingdate=start_date, bug_endingdate=end_date,bug_priority=priority, bug_milestone=milestone, bug_createdby=creator, bug_creationdate=now, bug_modifiedby=user_name, bug_modifydate=now, status=status, tester=testers, team_id=team, project_id=project_id)
            if result==True:
                #add this line in the code from LogModule import PassMessage
                #log message successful here 
                #message format be PassMessage(sModuleInfo, message,1 for pass,2 for warning, 3 for error,debug=True)
                LogModule.PassMessasge(sModuleInfo,"Inserted "+label_id+" successfully", 1)
                final = 'success'
            else:
                final =  'meh'
    result=simplejson.dumps(final)
    Conn.close()
    return HttpResponse(result,mimetype='application/json')

def Get_Labels(request):
    if request.is_ajax():
        if request.method=='GET':
            value=request.GET.get(u'term','')
            query="select * from labels"
            Conn=GetConnection()
            labels=DB.GetData(Conn,query,False)
    result=simplejson.dumps(labels)
    Conn.close()
    return HttpResponse(result,mimetype='application/json')


def ManageRequirement(request):
    return render_to_response('ManageRequirement.html',{})
def ManageTeam(request):
    return render_to_response('ManageTeam.html',{})
def GetTesterManager(request):
    if request.is_ajax():
        if request.method=='GET':
            final=[]
            Filters=['assigned_tester','manager']
            Conn=GetConnection()
            for each in Filters:
                query="select distinct user_id,user_names from permitted_user_list where user_level='%s'"%each.strip()
                get_list=DB.GetData(Conn, query,False)
                final.append((each,get_list))
    result=simplejson.dumps(final)
    Conn.close()
    return HttpResponse(result,mimetype='application/json')
def Create_Team(request):
    message=""
    if request.is_ajax():
        if request.method=='GET':
            member_list=request.GET.get(u'member').split("|")
            team_name=request.GET.get(u'team_name','')
            print team_name
            Conn=GetConnection()
            #check for existing team
            query="select count(*) from config_values where type='Team' and value='%s'"%team_name.strip()
            available_count=DB.GetData(Conn, query)
            if(available_count[0]==0):
                #form dict
                Dict={'type':'Team','value':team_name.strip()}
                result=DB.InsertNewRecordInToTable(Conn,"config_values",**Dict)
                if result==True:
                    query="select id from config_values where type='Team' and value='%s'"%team_name.strip()
                    id_list=DB.GetData(Conn,query)
                    if (len(id_list)!=0):
                        id_list=str(id_list[0])
                        for each in member_list:
                            Dict={}
                            Dict.update({'team_id':id_list,'user_id':int(each.strip())})
                            if(DB.IsDBConnectionGood(Conn)==False):
                                time.sleep(1)
                                Conn=GetConnection()
                            result=DB.InsertNewRecordInToTable(Conn,"team_info",**Dict)
                            if result!=True:
                                message="Failed inserting the member"
                    else:
                        message="Failed.Can't retrieve the Team name."
                else:
                    message="Failed.Team name insert Failure"    
    result=simplejson.dumps(message)
    Conn.close()
    return HttpResponse(result,mimetype='application/json')
def GetAllTeam(request):
    if request.is_ajax():
        if request.method=='GET':
            value=request.GET.get(u'term','')
            if value=='':
                query="select id,value from config_values where type='Team'"
            else:
                query="select id,value from config_values where type='Team' and value Ilike '%%%s%%'"%value
            Conn=GetConnection()
            all_team=DB.GetData(Conn,query,False)
    result=simplejson.dumps(all_team)
    Conn.close()
    return HttpResponse(result,mimetype='application/json')
def GetTeamInfo(request):
    if request.is_ajax():
        if request.method=='GET':
            team=request.GET.get(u'team','')
            print team
            list_value=['leader','tester']
            other_value=['manager','assigned_tester']
            Conn=GetConnection()
            #Get team Id
            final=[]
            query="select id from config_values where type='Team' and value='%s'"%team.strip()
            team_id=DB.GetData(Conn,query)
            if len(team_id)==1:
                team_id=str(team_id[0]).strip()
                for each in zip(other_value,list_value):
                    query="select user_id,user_names,user_level from permitted_user_list where user_id in (select cast(user_id as int) from team_info where team_id =(select id from config_values where value='%s'  and type='Team')) and user_level='%s'"%(team,each[0].strip())
                    if(DB.IsDBConnectionGood(Conn)==False):
                        time.sleep(1)
                        Conn=GetConnection()
                    list_data=[]
                    list_data=DB.GetData(Conn,query,False)
                    final.append((each[1].strip(),list_data))
                message="Team Data Fetched"
            else:
                message="No team found"
                final=[]
    result_data={
                 'message':message.strip(),
                 'data':final,
                 'teamname':team
                 }    
    result=simplejson.dumps(result_data)
    Conn.close()
    return HttpResponse(result,mimetype='application/json')
def GetTestStepsAndTestCasesOnDriverValue(request):
    if request.is_ajax():
        if request.method == 'GET':
            ToDelete= request.GET.get('ToDelete', '')
            data_type=request.GET.get('data_type', '')
            if(data_type=='driver'):
                query='''
                SELECT  distinct  test_cases.tc_id , 
                      test_cases.tc_name, 
                      config_values.value, 
                      test_steps_list.step_id,
                      test_steps_list.stepname      
                    FROM 
                       public.config_values  join 
                       public.test_steps_list on config_values.value = test_steps_list.driver join
                       public.test_steps on test_steps.step_id = test_steps_list.step_id join
                       public.test_cases on test_steps.tc_id=test_cases.tc_id  join
                       public.test_case_tag on test_steps.tc_id=test_case_tag.tc_id 
    
                 WHERE
                       config_values.value ='%s' 
                    ''' %ToDelete 
                Conn=GetConnection()    
                tabledata= DB.GetData(Conn, query, False)                              
                Heading = ['ID', 'Test Case Name', 'Value', 'Step ID', 'Step Name']
            if(data_type=='feature'):
                query='''
                SELECT  distinct  test_cases.tc_id , 
                      test_cases.tc_name, 
                      config_values.value, 
                      test_steps_list.step_id,
                      test_steps_list.stepname      
                    FROM 
                       public.config_values  join 
                       public.test_steps_list on config_values.value = test_steps_list.stepfeature join
                       public.test_steps on test_steps.step_id = test_steps_list.step_id join
                       public.test_cases on test_steps.tc_id=test_cases.tc_id  join
                       public.test_case_tag on test_steps.tc_id=test_case_tag.tc_id 
    
                 WHERE
                       config_values.value ='%s' 
                    ''' %ToDelete 
                    
                tabledata= DB.GetData(Conn, query, False)                              
                Heading = ['ID', 'Test Case Name', 'Value', 'Step ID', 'Step Name ']
            results = {'Heading':Heading, 'TableData':tabledata}
            print results
    json = simplejson.dumps(results)
    Conn.close()
    return HttpResponse(json, mimetype='application/json')
def TeamData(request,team_name):
    team_name=team_name.replace('_',' ')
    #get the team name member
    #query="select name,rank from team_info where team_id =(select id from config_values where type='Team' and value='%s')"%team_name
    query="select user_id,user_names,user_level from permitted_user_list where user_id in(select cast(user_id as int) from team_info where team_id=(select id from config_values where type='Team' and value='%s'))"%team_name
    print query
    Conn=GetConnection()
    getData=DB.GetData(Conn,query,False)
    leader=[]
    tester=[]
    for each in getData:
        if each[2]=='manager':
            leader.append((each[0],each[1].strip()))
        if each[2]=='assigned_tester':
            tester.append((each[0],each[1].strip()))
    query="select user_id,user_names,user_level from permitted_user_list where user_level in ('assigned_tester','manager')"
    all_list=DB.GetData(Conn,query,False)
    rest_tester=[]
    rest_manager=[]
    for each in all_list:
        if (each[0],each[1].strip()) in leader or (each[0],each[1].strip()) in tester:
            continue
        else:
            if each[2]=='assigned_tester':
                rest_tester.append((each[0],each[1].strip()))
            if each[2]=='manager':
                rest_manager.append((each[0],each[1].strip()))
        
    Dict={
          'team_name':team_name.strip(),
          'leader':leader,
          'tester':tester,
          'rest_leader':rest_manager,
          'rest_tester':rest_tester
    }
    Conn.close()
    return render_to_response('Team_Edit.html',Dict)
def Add_Members(request):
    message=""
    if request.is_ajax():
        if request.method=='GET':
            member=request.GET.get(u'member','').split("|")
            team_name=request.GET.get(u'team_name','').strip()
            #check the validity for the team name
            query="select id from config_values where type='Team' and value='%s'"%team_name
            Conn=GetConnection()
            team_id=DB.GetData(Conn,query)
            if len(team_id)==0:
                message="Failed.No such Team Name"
            else:
                team_id=str(team_id[0])
                for each in member:
                    if DB.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    result=DB.InsertNewRecordInToTable(Conn,"team_info",team_id=team_id,user_id=each)
                    if result==False:
                        break
                    else:
                        message="Successfully Updated."
    result=simplejson.dumps(message)
    Conn.close()
    return HttpResponse(result,mimetype='application/json')
def Delete_Members(request):
    message=""
    if request.is_ajax():
        if request.method=='GET':
            member_list=request.GET.get(u'member','').split("|")
            team_name=request.GET.get(u'team_name','').strip()
            #check the validity for the team name
            query="select id from config_values where type='Team' and value='%s'"%team_name
            Conn=GetConnection()
            team_id=DB.GetData(Conn,query)
            if len(team_id)==0:
                message="Failed.No such Team Name"
            else:
                team_id=str(team_id[0])
                for each in member_list:
                    if DB.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    result=DB.DeleteRecord(Conn,"team_info",team_id=team_id,user_id=each)
                    if result==False:
                        break
                    else:
                        message="Successfully Updated."
    result=simplejson.dumps(message)
    Conn.close()
    return HttpResponse(result,mimetype='application/json')
def Delete_Team(request):
    message=""
    if request.is_ajax():
        if request.method=='GET':
            team_name=request.GET.get(u'team_name','').strip()
            #check the validity for the team name
            query="select id from config_values where type='Team' and value='%s'"%team_name
            Conn=GetConnection()
            team_id=DB.GetData(Conn,query)
            if len(team_id)==0:
                message="Failed.No such Team Name"
            else:
                team_id=str(team_id[0])
                result=DB.DeleteRecord(Conn, "team_info",team_id=team_id.strip())
                result1=DB.DeleteRecord(Conn,"config_values",id=team_id)
                if result==True and result1==True:
                    message="Success"
                else:
                    message="Failed."
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
def UpdateTeamName(request):
    if request.is_ajax():
        if request.method=='GET':
            message=""
            type_tag=request.GET.get(u'type','')
            new_name=request.GET.get(u'new_name','')
            old_name=request.GET.get(u'old_name','')
            print type_tag
            print new_name
            print old_name
            if type_tag=='TEAM':
                type_tag='Team'
            query="select count(*) from config_values where value='%s' and type='%s'"%(old_name.strip(),type_tag.strip())
            Conn=GetConnection()
            count=DB.GetData(Conn,query)
            
            if count[0]==1 and len(count)==1:
                sWhereQuery="where value='%s' and type='%s'"%(old_name.strip(),type_tag.strip())
                
                result=DB.UpdateRecordInTable(Conn, "config_values", sWhereQuery,value=new_name.strip())
                if result==True:
                    message="Success"
                else:
                    message="Failed"
            else:
                message="Failed"    
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
def SearchEditDev(request):
    templ = get_template('SearchEdit-Dev.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)
def CreateProject(request):
    try:
        print "Create project was called"
        query="select distinct value from config_values where type='Team'"
        try:
            team_name = []
            Conn=GetConnection()
            team_name=DB.GetData(Conn, query)
            print team_name
            Conn.close()
        except Exception,e:
            print "Exception:", e
        
        final=[]
        count=0
        temp=[]
        for x in team_name:
            temp.append(x)
            count+=1
            if count>5:
                final.append(temp)
                temp=[]
                count=0
        final.append(temp)
        team_name=final
        query="select distinct user_names,user_level from permitted_user_list where user_level in ('manager','assigned_tester')"
        try:
            owners = []
            Conn=GetConnection()
            owners=DB.GetData(Conn,query,False)
            print owners
            Conn.close()
            
        except Exception,e:
            print "Exception:", e       
            
            
        final=[]
        count=0
        temp=[]
        for x in owners:
            temp.append(x)
            count+=1
            if count>5:
                final.append(temp)
                temp=[]
                count=0
        final.append(temp)
        owners=final            
        Dict={'teams':team_name,'owners':owners}
        return render_to_response('Project.html',Dict)
    except Exception,e:
        print "Exception:", e
def Create_New_Project(request):
    try:
        if request.is_ajax():
            if request.method=='GET':
                message=""
                user_name=request.GET.get('user_name','')
                name=request.GET.get('project_name','')
                owners=request.GET.get('project_owner').strip()
                #generate Project id
                Conn=GetConnection()
                tmp_id = DB.GetData(Conn, "select nextval('projectid_seq')")
                Conn.close()
                print tmp_id
                project_id=('PROJ-')+str(tmp_id[0])
                query="select count(*) from projects where project_name='%s' and project_id='%s'"%(name.strip(),project_id.strip())
                count = []
                Conn=GetConnection()
                count=DB.GetData(Conn,query)
                Conn.close()
                print count
                now=datetime.datetime.now().date()
                current_date=now
                if len(count)==1 and count[0]==0:
                    #create the new projects
                    Dict={
                        'project_id':project_id.strip(),
                        'project_name':name.strip(),
                        'project_owners':owners.strip(),
                        'project_createdby':user_name.strip(),
                        'project_creationdate':current_date,
                        'project_modifiedby':user_name.strip(),
                        'project_modifydate':current_date,
                        'project_description':'',
                    }
                    Conn=GetConnection()
                    result = False
                    result=DB.InsertNewRecordInToTable(Conn, "projects",**Dict)
                    Conn.close()
                    if result==False:
                        message="Failed"
                        Conn=GetConnection()
                    else:
                        message="Success"
            result_dict={
                 'message':message,
                 'project_id':project_id.strip()
                 }                 
        result=simplejson.dumps(result_dict)
        return HttpResponse(result,mimetype='application/json')   
    except Exception,e:
        print "Exception:", e     
def Project_Detail(request,project_id):
    try:
        query="select * from projects where project_id='%s'"%project_id
        Conn=GetConnection()
        project_data = []
        project_data=DB.GetData(Conn,query,False)
        Conn.close()
        print project_data
        #time.sleep(0.5)
        query="select column_name from information_schema.columns where table_name='projects'"
        Conn=GetConnection()
        project_column=DB.GetData(Conn,query)
        print project_column
        Conn.close()
        Dict={}
        for eachitem in project_data:
            for each in zip(project_column,eachitem):
                Dict.update({each[0]:each[1]})
        temp=Dict['project_owners']
        first_colon=temp.find(":",0)
        second_colon=temp.find(":",first_colon+1)
        first_hiphen=temp.find("-",first_colon+1)
        testers=temp[first_colon+1:first_hiphen]
        testers=testers.split(",")
        managers=temp[second_colon+1:]
        managers=managers.split(",")
        del Dict['project_owners']
        #get top 5 comments
        query="select comment_id,attachment from comments where project_id='%s' order by comment_date desc limit 5"%(project_id)
        Conn=GetConnection()
        top_five_comment = False
        top_five_comment=DB.GetData(Conn,query,False)
        print top_five_comment
        Conn.close()
        final=[]
        for each in top_five_comment:
            temp=[]
            if each[1]==False:
                query="select comment_text,commented_by,comment_date,rank,c.attachment from comments c where c.comment_id='%s' and c.project_id='%s'"%(each[0],project_id)    
                Conn=GetConnection()
                temp_comment=DB.GetData(Conn,query,False)
                Conn.close()
                #time.sleep(0.5)
                for each in temp_comment:
                    for eachitem in each:
                        temp.append(eachitem)
                temp.append('')
                temp=tuple(temp)
            if each[1]==True:
                query="select comment_text,commented_by,comment_date,rank,c.attachment,ca.docfile from comments c,comment_attachment ca where  c.comment_id=ca.comment_id and c.comment_id='%s' and c.project_id='%s'"%(each[0],project_id)
                Conn=GetConnection()
                temp=DB.GetData(Conn,query,False)
                Conn.close()
                #time.sleep(0.5)
                temp=temp[0]
                temp=tuple(temp)
            final.append(temp)
        comment=Comment()
        print comment
        team_query="select distinct ptm.team_id,c.value from config_values c,project_team_map ptm  where cast(c.id as text) =ptm.team_id and ptm.project_id='%s'"%project_id
        Conn=GetConnection()
        team_number=DB.GetData(Conn,team_query,False)
        Conn.close()
        #time.sleep(0.5)
        fullTeamDetail=GetProjectTeamInfo(team_number)
        other_query="(select cast(id as text),value from config_values where type='Team') except (select distinct ptm.team_id,c.value from config_values c,project_team_map ptm  where cast(c.id as text) =ptm.team_id and project_id='%s')" %project_id
        Conn=GetConnection()
        restTeam=DB.GetData(Conn,other_query,False)
        Conn.close()
        #time.sleep(0.5)
        restTeamDetail=GetProjectTeamInfo(restTeam)
        Dict.update({'team_detail':fullTeamDetail,'rest_team':restTeamDetail})
        Dict.update({'comment':comment})
        Dict.update({'testers':testers,'managers':managers})        
        Dict.update({'final_comment':final})
        #time.sleep(1)
        return render_to_response('Project_Detail.html',Dict,context_instance=RequestContext(request))
    except Exception,e:
        print "Exception:", e
def GetProjectTeamInfo(team_number):
    try:
        fullTeamDetail=[]
        for each in team_number:
            team={}
            query="select name,rank from team_info where team_id='%s'"%int(each[0])
            Conn=GetConnection()
            team_members=DB.GetData(Conn,query,False)
            Conn.close()
            leader=[]
            tester=[]
            for eachitem in team_members:
                if eachitem[1]=='leader':
                    leader.append(eachitem[0])
                if eachitem[1]=='tester':
                    tester.append(eachitem[0])
            team.update({'leader':leader,'tester':tester})
            fullTeamDetail.append((each[0],each[1],each[1].replace(' ','_'),team))
        return fullTeamDetail
    except Exception,e:
        print "Exception:", e
def Small_Project_Detail(request):
    try:
        if request.is_ajax():
            if request.method=='GET':
                name=request.GET.get(u'name','')
                query="select * from projects where project_name='%s'"%name.strip()
                Conn=GetConnection()
                project_metadata=DB.GetData(Conn,query,False)
                Conn.close()
                #time.sleep(0.5)
                project_column_query="select column_name from information_schema.columns where table_name='projects'"
                Conn=GetConnection()
                project_column=DB.GetData(Conn,project_column_query)
                Conn.close()
                #time.sleep(0.5)
                Dict={}
                for each in project_metadata:
                    for eachitem in zip(project_column,each):
                        Dict.update({eachitem[0]:eachitem[1]})
                temp=Dict['project_owners']
                first_colon=temp.find(":",0)
                second_colon=temp.find(":",first_colon+1)
                first_hiphen=temp.find("-",first_colon+1)
                testers=temp[first_colon+1:first_hiphen]
                testers=testers.split(",")
                managers=temp[second_colon+1:]
                managers=managers.split(",")
                del Dict['project_owners']
                Dict.update({'testers':testers,'managers':managers})
                due_in=Dict['project_endingdate']-Dict['project_startingdate']
                if due_in.days==0:
                    due_message="Today"
                elif due_in.days<0:
                    if due_in.days<-1:
                        due_message="Over "+str(str(due_in.days)[1:])+" days"
                    else:
                        due_message="Over "+str(str(due_in.days)[1:])+" day"
                else:
                    if due_in.days>1:
                        due_message="In "+str(due_in.days)+" days"
                    else:
                        due_message="In "+str(due_in.days)+" days"
                query="select value from config_values where type='Team' and id in (select cast(team_id as int) from project_team_map where project_id='%s')"%(Dict['project_id'].strip())
                Conn=GetConnection()
                team_name=DB.GetData(Conn,query)
                Conn.close()
                Dict.update({
                             'project_startingdate':str(Dict['project_startingdate']),
                             'project_endingdate':str(Dict['project_endingdate']),
                             'project_creationdate':str(Dict['project_creationdate']),
                             'project_modifydate':str(Dict['project_modifydate']),
                             'due_message':due_message,
                             'team_name':team_name
                             })     
        result=simplejson.dumps(Dict)        
        return HttpResponse(result,mimetype='application/json')        
    except Exception,e:
        print "Exception:", e
def Get_Projects(request):
    try:
        if request.is_ajax():
            
            if request.method=='GET':
                try:
                    name=request.GET.get(u'team_name','')
                    if name=="":
                        query="select project_name from projects"
                    else:
                        query="select project_name from projects where project_name Ilike'%%%s%%'"%name.strip()
                    Conn=GetConnection()
                    team_name=[]
                    team_name=DB.GetData(Conn,query)
                    Conn.close()
                except Exception,e:
                    
                    print "Exception:",e
        result=simplejson.dumps(team_name)
        return HttpResponse(result,mimetype='application/json')
    except Exception,e:
        print "Exception:", e
def FileUpload(request,project_id):
    try:
        print request
        print project_id
        #Get the rank of the person
        query="select project_owners from projects where project_id='%s'"%(project_id)
        Conn=GetConnection()
        project_owners=DB.GetData(Conn, query)
        Conn.close()
        temp=project_owners[0]
        first_colon=temp.find(":",0)
        second_colon=temp.find(":",first_colon+1)
        first_hiphen=temp.find("-",first_colon+1)
        testers=temp[first_colon+1:first_hiphen]
        testers=testers.split(",")
        managers=temp[second_colon+1:]
        managers=managers.split(",")
        owners=[]
        for each in testers:
            if each not in owners:
                owners.append(each)
        for each in managers:
            if each not in owners:
                owners.append(each)
        query="select distinct name,rank from team_info where cast(team_id as text) in(select team_id from project_team_map where project_id='%s')"%project_id
        Conn=GetConnection()
        rest_rank=DB.GetData(Conn,query,False)
        Conn.close()
        members=[]
        for each in rest_rank:
            if each[0] not in owners:
                members.append(each[0])
        user_name=request.POST['commented_by']
        rank=""
        if user_name in owners:
            rank="Owner"
        if user_name in members:
            rank="Member"
        query="select project_createdby from projects where project_id='%s'"%project_id
        Conn=GetConnection()
        created_by=DB.GetData(Conn,query)
        Conn.close()
        if user_name in created_by:
            rank="Creator"
        #form file name
        if rank!="":
            now=datetime.datetime.now().date()
            dateFolder=os.path.join(MEDIA_ROOT,str(now.year))
            dateFolder=os.path.join(dateFolder,str(now.month))
            dateFolder=os.path.join(dateFolder,str(now.day))
            #fullfileName=(str(now.year)+'/'+str(now.month)+'/'+str(now.day)+'/'+request.FILES['docfile'])
            #print fullfileName
            comment_time=datetime.datetime.now()
            #Genereate Comment ID
            Conn=GetConnection()
            tmp_id = DB.GetData(Conn, "select nextval('commentid_seq')")
            Conn.close()
            comment_id=('COM-'+str(tmp_id[0]))
            if len(request.FILES)!=0 and request.POST['comment']!="":
                file_name=request.FILES['docfile']
                path=default_storage.save(os.path.join(dateFolder,str(file_name)),ContentFile(file_name.read()))
                print path
                #print "Attachment Comment"
                #new_path=
                path=path[len(PROJECT_ROOT):]
                Conn=GetConnection()
                result=DB.InsertNewRecordInToTable(Conn,"comment_attachment",comment_id=comment_id,docfile=path)
                Conn.close()
                if result==False:
                    print "unable to save the attachments"
                    attachment=False
    
                else:
                    attachment=True
                #form Dict
                Dict={
                      'project_id':project_id.strip(),
                      'comment_id':comment_id.strip(),
                      'comment_text':request.POST['comment'].strip(),
                      'commented_by':user_name.strip(),
                      'comment_date':comment_time,
                      'rank':rank.strip(),
                      'attachment':attachment
                      }
                Conn=GetConnection()
                result=DB.InsertNewRecordInToTable(Conn,"comments",**Dict)
                Conn.close()
                if result==True:
                    return HttpResponseRedirect(reverse('comment_view', kwargs={'project_id':project_id}))
            elif len(request.FILES)==0 and request.POST['comment']!="":
                #form Dict
                attachment=False
                Dict={
                      'project_id':project_id.strip(),
                      'comment_id':comment_id.strip(),
                      'comment_text':request.POST['comment'].strip(),
                      'commented_by':user_name.strip(),
                      'comment_date':comment_time,
                      'rank':rank.strip(),
                      'attachment':attachment
                      }
                Conn=GetConnection()
                result=DB.InsertNewRecordInToTable(Conn,"comments",**Dict)
                Conn.close()
                if result==True:
                    return HttpResponseRedirect(reverse('comment_view', kwargs={'project_id':project_id}))
            elif len(request.FILES)!=0 and request.POST['comment']=="":
                file_name=request.FILES['docfile']
                path=default_storage.save(os.path.join(dateFolder,str(file_name)),ContentFile(file_name.read()))
                print path
                #print "Attachment Comment"
                #new_path=
                path=path[len(PROJECT_ROOT):]
                Conn=GetConnection()
                result=DB.InsertNewRecordInToTable(Conn,"comment_attachment",comment_id=comment_id,docfile=path)
                Conn.close()
                if result==False:
                    print "unable to save the attachments"
                    attachment=False
                else:
                    attachment=True
                #form Dict
                Dict={
                      'project_id':project_id.strip(),
                      'comment_id':comment_id.strip(),
                      'comment_text':'',
                      'commented_by':user_name.strip(),
                      'comment_date':comment_time,
                      'rank':rank.strip(),
                      'attachment':attachment
                      }
                Conn=GetConnection()
                result=DB.InsertNewRecordInToTable(Conn,"comments",**Dict)
                Conn.close()
                if result==True:
                    return HttpResponseRedirect(reverse('comment_view', kwargs={'project_id':project_id}))
            else:
                print "no comment"
        else:
            print "not autorized to comment"
    except Exception,e:
        print "Exception:", e
def commentView(request,project_id):
    try:
        query="select comment_id,attachment from comments where project_id='%s' order by comment_date desc"%project_id
        Conn=GetConnection()
        all_comments=DB.GetData(Conn,query,False)
        Conn.close()
        final=[]
        for each in all_comments:
            if each[1]==False:
                query="select comment_text,commented_by,comment_date,rank,c.attachment from comments c where c.comment_id='%s' and c.project_id='%s'"%(each[0],project_id)    
                Conn=GetConnection()
                temp_comment=DB.GetData(Conn,query,False)
                Conn.close()
                temp=[]
                for each in temp_comment:
                    for eachitem in each:
                        temp.append(eachitem)
                temp.append('')
                temp=tuple(temp)
            if each[1]==True:
                query="select comment_text,commented_by,comment_date,rank,c.attachment,ca.docfile from comments c,comment_attachment ca where  c.comment_id=ca.comment_id and c.comment_id='%s' and c.project_id='%s'"%(each[0],project_id)
                Conn=GetConnection()
                temp=DB.GetData(Conn,query,False)
                Conn.close()
                temp=temp[0]
                temp=tuple(temp)
            final.append(temp)
        comment=Comment()
        query="select project_name from projects where project_id='%s'"%project_id
        Conn=GetConnection()
        project_name=DB.GetData(Conn,query)
        Conn.close()
        project_name=project_name[0]
        Dict={'all_comments':final,'comment':comment,'project_id':project_id,'project_name':project_name}
        return render_to_response('Project_Comment.html',Dict,context_instance=RequestContext(request))
    except Exception,e:
        print "Exception:", e
def AddTeamtoProject(request):
    try:
        if request.is_ajax():
            if request.method=='GET':
                
                teams=request.GET.get(u'teams').split("|")
                project_id=request.GET.get(u'project_id').strip()
                for each in teams:
                    query="select count(*) from project_team_map where project_id='%s' and team_id='%s'"%(project_id,str(each))
                    Conn=GetConnection()
                    project_count=DB.GetData(Conn,query)
                    Conn.close()
                    if len(project_count)==1 and project_count[0]==1:
                        continue
                    else:
                        #form Dict
                        Dict={
                              'project_id':project_id.strip(),
                              'team_id':str(each).strip(),
                              'status':False
                              }
                        result = False
                        Conn=GetConnection()
                        result=DB.InsertNewRecordInToTable(Conn,"project_team_map",**Dict)
                        Conn.close()
                        if result==False:
                            #time.sleep(1)
                            Conn=GetConnection()
        message="Success"
        result=simplejson.dumps(message)
        return HttpResponse(result,mimetype='application/json')
        #return HttpResponseRedirect(reverse('project_detail',kwargs={'project_id':project_id}))    
    except Exception,e:
        print "Exception:", e
def DetailRequirementView(request,project_id,req_id):
    
    Dict={'project_id':project_id}
    #data retrieval from requirements table
    cols=['requirement_id','requirement_title','requirement_description','start_date','end_date','priority','milestone','creator','creation_date','modifier','last_modified','project_id','status','requirement_path','team','color']
    requirement_query="select r.requirement_id,"
    requirement_query+="requirement_title,"
    requirement_query+="requirement_description,"
    requirement_query+="requirement_startingdate,"
    requirement_query+="requirement_endingdate,"
    requirement_query+="'P'||cast(requirement_priority as text),"
    requirement_query+="(select value from config_values where id=cast(requirement_milestone as int) and type='milestone'),"
    requirement_query+="requirement_createdby,"
    requirement_query+="requirement_creationdate,"
    requirement_query+="requirement_modifiedby,"
    requirement_query+="requirement_modifydate,"
    requirement_query+="project_id,"
    requirement_query+="case"
    requirement_query+=" when r.status='not_started' then 'Not Started'"
    requirement_query+=" when r.status='started' then 'Started'"
    requirement_query+=" when r.status='complete' then 'Complete'"
    requirement_query+=" when r.status='over_due' then 'Overdue'"
    requirement_query+=" end,"
    requirement_query+="parent_requirement_id,"
    requirement_query+="(select value from config_values where type='Team' and id= cast(rtm.team_id as int)),"
    requirement_query+="case"
    requirement_query+=" when r.status='not_started' then '#bbbbbb'"
    requirement_query+=" when r.status='started' then '#0000ff'"
    requirement_query+=" when r.status='complete' then '#00ff00'"
    requirement_query+=" when r.status='over_due' then '#ff0000'"
    requirement_query+=" end "
    requirement_query+="from requirements r,requirement_team_map rtm "
    requirement_query+="where r.requirement_id=rtm.requirement_id and r.requirement_id='%s'"%req_id
    try:
        Conn=GetConnection()
        requirement_data=DB.GetData(Conn,requirement_query,False)
        print requirement_data
        for each in requirement_data:
            for eachitem in zip(cols,each):
                Dict.update({eachitem[0]:eachitem[1]})
        requirement_path_id=Dict['requirement_path']
        parent_query="select requirement_path from requirement_sections where requirement_path_id=%d"%int(requirement_path_id)
        
        parent_path=DB.GetData(Conn,parent_query,False)
        parent_path=parent_path[0][0].split(".")
        if len(parent_path)>=2 and isinstance(parent_path,list):
            parent=str(parent_path[0][0].split(".")[-2]).replace('_','-')
            parent_name_id_query="select requirement_id,requirement_title from requirements where requirement_id='%s'"%parent
            
            parent_name_id=DB.GetData(Conn,parent_name_id_query,False)
            Dict.update({'parent_id':parent_name_id[0][0],'parent_name':parent_name_id[0][1],'parent':True})
        elif len(parent_path)==1 and isinstance(parent_path, list):
            Dict.update({'parent':False})
        else:
            Dict.update({'parent':False})        
    except Exception,e:
        print "Exception:",e
    try:
        if DB.IsDBConnectionGood(Conn)==False:
            time.sleep(1)
            Conn=GetConnection()
        query="select comment_id,attachment from comments where project_id='%s' order by comment_date desc"%req_id
        all_comments=DB.GetData(Conn,query,False)
        final=[]
        for each in all_comments:
            if each[1]==False:
                query="select comment_text,commented_by,comment_date,rank,c.attachment from comments c where c.comment_id='%s' and c.project_id='%s'"%(each[0],req_id)    
                temp_comment=DB.GetData(Conn,query,False)
                temp=[]
                for each in temp_comment:
                    for eachitem in each:
                        temp.append(eachitem)
                temp.append('')
                temp=tuple(temp)
            if each[1]==True:
                query="select comment_text,commented_by,comment_date,rank,c.attachment,ca.docfile from comments c,comment_attachment ca where  c.comment_id=ca.comment_id and c.comment_id='%s' and c.project_id='%s'"%(each[0],req_id)
                temp=DB.GetData(Conn,query,False)
                temp=temp[0]
                temp=tuple(temp)
            final.append(temp)
        Dict.update({'all_comments':final})
    except Exception,e:
        print "Exception:",e
    comment=Comment()
    Dict.update({'comment':comment})
    try:
        Conn = GetConnection()
        query = "select l.label_id,l.label_name,l.Label_color from labels l, label_map lm where l.label_id=lm.label_id and lm.id='"+req_id+"' and lm.type='REQ' order by label_name"
        labels = DB.GetData(Conn,query,False)
        Dict.update({'labels':labels})
    except Exception,e:
        print "Exception:",e
    #get all the comments of this requirement_id
    return render(request,'RequirementDetail.html',Dict)

def TeamWiseRequirementView(request,project_id,team_id):
    query="select project_name from projects where project_id='%s'"%project_id
    Conn=GetConnection()
    project_name=DB.GetData(Conn,query)
    if isinstance(project_name,list):
        project_name=project_name[0]
    else:
        project_name=""
    team_name_query="select c.value,ptm.status from project_team_map ptm,config_values c where cast(ptm.team_id as int)=c.id and ptm.project_id='%s' and ptm.team_id='%s'"%(project_id,team_id)
    team_name_status=DB.GetData(Conn,team_name_query,False)
    if isinstance(team_name_status,list):
        status=True
        url_name=str(team_name_status[0][0]).replace(' ', '_')
    else:
        status=False
        url_name=""
    if status==True:
        query="select r.requirement_title,r.requirement_description,"
        query+="case when requirement_endingdate-requirement_startingdate=0 then 'Due Today'"
        query+=" when requirement_endingdate-requirement_startingdate>0 and requirement_endingdate-requirement_startingdate<=1 then 'In ' ||requirement_endingdate-requirement_startingdate ||' day'"
        query+=" when requirement_endingdate-requirement_startingdate>1 then 'In ' ||requirement_endingdate-requirement_startingdate ||' days'"
        query+=" when requirement_endingdate-requirement_startingdate=-1 then 'Over ' || (requirement_startingdate-requirement_endingdate) ||' day ago'" 
        query+=" when requirement_endingdate-requirement_startingdate<=-1 then 'Over ' || (requirement_startingdate-requirement_endingdate) ||' days ago'"  
        query+=" end,"
        query+="case"
        query+=" when rtm.status='started' then 'Started'"
        query+=" when rtm.status='complete' then 'Complete'"
        query+=" when rtm.status='over_due' then 'Overdue'"
        query+=" end,(select value from config_values where cast(r.requirement_milestone as int)=id),r.requirement_id"
        query+=" from requirement_team_map rtm,requirements r" 
        query+=" where rtm.requirement_id=r.requirement_id and rtm.team_id='%s' and r.project_id='%s'"%(team_id,project_id)
        requirement_detail=DB.GetData(Conn,query,False)
    Dict={
          'project_id':project_id,
          'project_name':project_name,
          'url_name':url_name,
          'team_name':team_name_status[0][0].strip(),
          'requirements':requirement_detail
          }
    return render_to_response('TeamWiseRequirementView.html',Dict,context_instance=RequestContext(request))

#New Requirement Page Done Functions

#to the new requirement page

def ToNewRequirementPage(request,project_id):
    Conn=GetConnection()
    query="select project_id, project_name from projects"
    project_info=DB.GetData(Conn,query,False)
    query="select id,value from config_values where type='milestone'"
    milestone_info=DB.GetData(Conn,query,False)
    #get the current projects team info
    query="select c.id,c.value from project_team_map ptm, config_values c where cast(ptm.team_id as int)=c.id and ptm.project_id='%s'"%project_id
    team_info=DB.GetData(Conn,query,False)
    #get the existing requirement id for parenting
    query="select distinct requirement_id,requirement_title from requirements where project_id='%s' order by requirement_id"%project_id
    requirement_list=DB.GetData(Conn,query,False)
    
    query = "select label_id,label_name,Label_color from labels order by label_name"
    labels = DB.GetData(Conn,query)
    Dict={
          'project_id':project_id,
          'project_list':project_info,
          'milestone_list':milestone_info,
          'team_list':team_info,
          'requirement_list':requirement_list,
          'labels':labels
    }
    return render_to_response('CreateNewRequirement.html',Dict)

#getting the tree information for the requirements

def getRequirements(request,project_id):
    if request.method=='GET':
        if request.is_ajax():
            print project_id
            Conn=GetConnection()
            query="select * from requirement_sections"
            all_section=DB.GetData(Conn,query,False)
            parent_section=list(set(each[1].split('.')[0] for each in all_section))
            #filter at first for the current projects
            query="select distinct requirement_id from requirements where project_id='%s'"%project_id
            current_project_requirement_list=DB.GetData(Conn,query)
            for each in parent_section:
                if each.replace('_','-') not in current_project_requirement_list:
                    parent_section.remove(each)
            print parent_section
            temp_list=[]
            parent_listed=[]
            child_sections=[]
            result=[]
            for i in all_section:
                print all_section
                temp={}
                for section in parent_section:
                    if section==i[1]:
                        temp['id']=i[0]
                        temp['text']=i[1]
                        #temp['children']=True
                        temp['type'] = 'parent_section'
                        temp['undetermined'] = True
                        temp_list.append(temp)
                        parent_listed.append(i)
            parent_section=temp_list
            for each in parent_listed:
                all_section.remove(each)
            for each in parent_section:
                for eachitem in all_section:
                    if each['text'] in eachitem[1].split('.'):
                        each.update({'children':True})
            #now assigning the child
            for i in all_section:
                temp={}
                section = i[1].split('.')
                print section
                for section_element in parent_section:
                    if section[0] == section_element['text']:
                        temp['id'] = i[0]
                        temp['text'] = section[-1]
                        temp['type'] = 'section'
                        if len(section) == 2:
                            temp['parent'] = section_element['id']
                            temp['parent_text'] = section_element['text']
                        else:
                            temp['parent_text'] = section[-2]
                        child_sections.append(temp)
            for each in parent_section:
                each['text']=each['text'].replace('_','-')                
            requested_id=request.GET.get('id','')
            if requested_id=='#':
                result=simplejson.dumps(parent_section)
            else:
                for child_section in child_sections:
                    for parent_section in child_sections:
                        if 'parent' not in child_section.keys() and child_section['parent_text']==parent_section['text']:
                            child_section['parent']=parent_section['id']
                            parent_section['children']=True
                try:
                    if requested_id != '':
                        for section in child_sections:
                            if unicode(section['parent']) == requested_id:
                                for i in all_section:
                                    temp = i[1].split('.')[-1]
                                    if temp == section['text'] and section['id'] == i[0]:
                                        section['text'] = section['text'] + '<span style="display:none;">' + i[1] + '</span>'
                                        
                                        section['id'] = str(section['id'])
                                        section.pop('parent_text')
                                        section['text'] = section['text'].replace('_', '-')
                                        
                                        result.append(section)
                        result = json.dumps(result)
                except:
                    return HttpResponse("NULL")
            return HttpResponse(result,mimetype='application/json')
        else:
            return render(request,'ManageRequirement.html',{})
        
#function for creating the new requirements
def CreateRequirement(request):
    if request.is_ajax():
        if request.method=='GET':
            #getting all the info from the messages
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team','').split("|")
            title=request.GET.get(u'title','')
            description=request.GET.get(u'description','')
            start_date=request.GET.get(u'start_date','')
            end_date=request.GET.get(u'end_date','')
            priority=request.GET.get(u'priority','')
            milestone=request.GET.get(u'milestone','')
            status=request.GET.get(u'status','')
            user_name=request.GET.get(u'user_name','')
            feature_path=request.GET.get(u'feature_path','')
            parent_requirement_id=request.GET.get(u'requirement_id','')
            labels=request.GET.get(u'labels','')
            labels=labels.split("|")
            tasks=request.GET.get(u'tasks','')
            tasks=tasks.split("|")
            if parent_requirement_id=="":
                result=RequirementOperations.CreateParentRequirement(title, description, project_id, team_id, start_date, end_date, priority, status, milestone, user_name, feature_path,labels,tasks)
                if result!=False:
                    requirement_id=result
    result=simplejson.dumps(requirement_id)
    return HttpResponse(result,mimetype='application/json')
##getting required requirement and team info on the project_id change

def SubmitEditRequirement(request):
    if request.is_ajax():
        if request.method=='GET':
            #getting all the info from the messages
            req_id = request.GET.get(u'req_id','')
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team','').split("|")
            title=request.GET.get(u'title','')
            description=request.GET.get(u'description','')
            start_date=request.GET.get(u'start_date','')
            end_date=request.GET.get(u'end_date','')
            priority=request.GET.get(u'priority','')
            milestone=request.GET.get(u'milestone','')
            status=request.GET.get(u'status','')
            user_name=request.GET.get(u'user_name','')
            feature_path=request.GET.get(u'feature_path','')
            parent_requirement_id=request.GET.get(u'requirement_id','')
            labels=request.GET.get(u'labels','')
            labels=labels.split("|")
            tasks=request.GET.get(u'tasks','')
            tasks=tasks.split("|")
            result=RequirementOperations.EditRequirement(req_id, title, description, project_id, team_id, start_date, end_date, priority, status, milestone, user_name, feature_path,labels,tasks)
            if result!=False:
                requirement_id=result
    result=simplejson.dumps(requirement_id)
    return HttpResponse(result,mimetype='application/json')


def SubmitChildRequirement(request):
    if request.is_ajax():
        if request.method=='GET':
            #getting all the info from the messages
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team','').split("|")
            title=request.GET.get(u'title','')
            description=request.GET.get(u'description','')
            start_date=request.GET.get(u'start_date','')
            end_date=request.GET.get(u'end_date','')
            priority=request.GET.get(u'priority','')
            milestone=request.GET.get(u'milestone','')
            status=request.GET.get(u'status','')
            user_name=request.GET.get(u'user_name','')
            feature_path=request.GET.get(u'feature_path','')
            parent_requirement_id=request.GET.get(u'requirement_id','')
            labels=request.GET.get(u'labels','')
            labels=labels.split("|")
            tasks=request.GET.get(u'tasks','')
            tasks=tasks.split("|")
            result=RequirementOperations.CreateChildRequirement(title, description, project_id, team_id, start_date, end_date, priority, status, milestone, user_name, feature_path, parent_requirement_id, labels,tasks)
            if result!=False:
                requirement_id=result
    result=simplejson.dumps(requirement_id)
    return HttpResponse(result,mimetype='application/json')



def GetTeamInfoToCreateRequirement(request):
    if request.is_ajax():
        if request.method=='GET':
            project_id=request.GET.get('project_id','')
            team_query="select id,value from config_values c,project_team_map ptm where cast(c.id as text)=ptm.team_id and ptm.project_id='%s'"%project_id
            Conn=GetConnection()
            team_list=DB.GetData(Conn,team_query,False)
            Dict={'teams':team_list}
    result=simplejson.dumps(Dict)
    return HttpResponse(result,mimetype='application/json')


#function to get the small detail of the requirements
def SmallViewRequirements(request):
    if request.method=='GET':
        if request.is_ajax():
            Conn=GetConnection()
            project_id=request.GET.get('project_id','')
            decoded_string = json.loads(request.GET.get('selected_section_ids', []))
            requested_requirement_section_id=int(list(decoded_string)[0])
            query="select requirement_path from requirement_sections where requirement_path_id=%d"%(requested_requirement_section_id)
            requested_path=DB.GetData(Conn,query)
            requested_path=requested_path[0].split('.')
            if len(requested_path)==1:
                main_requirement=requested_path[0].replace('_','-')
                parent_requirement="No Parent"
            else:
                main_requirement=requested_path[-1].replace('_','-')
                parent_requirement=requested_path[-2].replace('_','-')
            query="select r.requirement_title,r.requirement_description,"
            query+="case when requirement_endingdate-requirement_startingdate=0 then 'Due Today'"
            query+=" when requirement_endingdate-requirement_startingdate>0 and requirement_endingdate-requirement_startingdate<=1 then 'In ' ||requirement_endingdate-requirement_startingdate ||' day'"
            query+=" when requirement_endingdate-requirement_startingdate>1 then 'In ' ||requirement_endingdate-requirement_startingdate ||' days'"
            query+=" when requirement_endingdate-requirement_startingdate=-1 then 'Over ' || (requirement_startingdate-requirement_endingdate) ||' day ago'" 
            query+=" when requirement_endingdate-requirement_startingdate<=-1 then 'Over ' || (requirement_startingdate-requirement_endingdate) ||' days ago'"  
            query+=" end,"
            query+="case"
            query+=" when r.status='not_started' then 'Not Started'"
            query+=" when r.status='started' then 'Started'"
            query+=" when r.status='complete' then 'Complete'"
            query+=" when r.status='over_due' then 'Overdue'"
            query+=" end,"
            query+="case"
            query+=" when r.status='not_started' then '#bbbbbb'"
            query+=" when r.status='started' then '#0000ff'"
            query+=" when r.status='complete' then '#00ff00'"
            query+=" when r.status='over_due' then '#ff0000'"
            query+=" end,"
            query+="(select value from config_values where cast(r.requirement_milestone as int)=id),r.requirement_id,(select value from config_values where type='Team' and id=cast(rtm.team_id as int))"
            query+=" from requirement_team_map rtm,requirements r" 
            query+=" where rtm.requirement_id=r.requirement_id and rtm.requirement_id='%s' and r.project_id='%s'"%(main_requirement,project_id)
            requirement_detail=DB.GetData(Conn,query,False)
            if parent_requirement!='No Parent':
                query="select requirement_id,requirement_title from requirements where requirement_id='%s'"%parent_requirement
                parent_requirement=DB.GetData(Conn,query,False)
            Dict={
                  'requirement_detail':requirement_detail,
                  'parent_id':parent_requirement
            }
    result=simplejson.dumps(Dict)
    return HttpResponse(result,mimetype='application/json') 

def PostRequirementComment(request,project_id,requirement_id):
    print request
    print project_id
    #Get the rank of the person
    query="select project_owners from projects where project_id='%s'"%(project_id)
    Conn=GetConnection()
    project_owners=DB.GetData(Conn, query)
    temp=project_owners[0]
    first_colon=temp.find(":",0)
    second_colon=temp.find(":",first_colon+1)
    first_hiphen=temp.find("-",first_colon+1)
    testers=temp[first_colon+1:first_hiphen]
    testers=testers.split(",")
    managers=temp[second_colon+1:]
    managers=managers.split(",")
    owners=[]
    for each in testers:
        if each not in owners:
            owners.append(each)
    for each in managers:
        if each not in owners:
            owners.append(each)
    query="select distinct name,rank from team_info where cast(team_id as text) in(select team_id from requirement_team_map where requirement_id='%s')"%requirement_id
    rest_rank=DB.GetData(Conn,query,False)
    members=[]
    for each in rest_rank:
        if each[0] not in owners:
            members.append(each[0])
    user_name=request.POST['commented_by']
    rank=""
    if user_name in owners:
        rank="Owner"
    if user_name in members:
        rank="Member"
    query="select requirement_createdby from requirements where requirement_id='%s'"%requirement_id
    created_by=DB.GetData(Conn,query)
    if user_name in created_by:
        rank="Creator"
    #form file name
    if rank!="":
        now=datetime.datetime.now().date()
        dateFolder=os.path.join(MEDIA_ROOT,str(now.year))
        dateFolder=os.path.join(dateFolder,str(now.month))
        dateFolder=os.path.join(dateFolder,str(now.day))
        #fullfileName=(str(now.year)+'/'+str(now.month)+'/'+str(now.day)+'/'+request.FILES['docfile'])
        #print fullfileName
        comment_time=datetime.datetime.now()
        #Genereate Comment ID
        tmp_id = DB.GetData(Conn, "select nextval('commentid_seq')")
        comment_id=('COM-'+str(tmp_id[0]))
        if len(request.FILES)!=0 and request.POST['comment']!="":
            file_name=request.FILES['docfile']
            path=default_storage.save(os.path.join(dateFolder,str(file_name)),ContentFile(file_name.read()))
            print path
            #print "Attachment Comment"
            #new_path=
            path=path[len(PROJECT_ROOT):]
            result=DB.InsertNewRecordInToTable(Conn,"comment_attachment",comment_id=comment_id,docfile=path)
            if result==False:
                print "unable to save the attachments"
                attachment=False

            else:
                attachment=True
            #form Dict
            Dict={
                  'project_id':requirement_id.strip(),
                  'comment_id':comment_id.strip(),
                  'comment_text':request.POST['comment'].strip(),
                  'commented_by':user_name.strip(),
                  'comment_date':comment_time,
                  'rank':rank.strip(),
                  'attachment':attachment
                  }
            result=DB.InsertNewRecordInToTable(Conn,"comments",**Dict)
            if result==True:
                return HttpResponseRedirect(reverse('detail_requirement', args=(project_id,requirement_id)))
        elif len(request.FILES)==0 and request.POST['comment']!="":
            #form Dict
            attachment=False
            Dict={
                  'project_id':requirement_id.strip(),
                  'comment_id':comment_id.strip(),
                  'comment_text':request.POST['comment'].strip(),
                  'commented_by':user_name.strip(),
                  'comment_date':comment_time,
                  'rank':rank.strip(),
                  'attachment':attachment
                  }
            result=DB.InsertNewRecordInToTable(Conn,"comments",**Dict)
            if result==True:
                return HttpResponseRedirect(reverse('detail_requirement', args=(project_id,requirement_id)))
        elif len(request.FILES)!=0 and request.POST['comment']=="":
            file_name=request.FILES['docfile']
            path=default_storage.save(os.path.join(dateFolder,str(file_name)),ContentFile(file_name.read()))
            print path
            #print "Attachment Comment"
            #new_path=
            path=path[len(PROJECT_ROOT):]
            result=DB.InsertNewRecordInToTable(Conn,"comment_attachment",comment_id=comment_id,docfile=path)
            if result==False:
                print "unable to save the attachments"
                attachment=False

            else:
                attachment=True
            #form Dict
            Dict={
                  'project_id':requirement_id.strip(),
                  'comment_id':comment_id.strip(),
                  'comment_text':'',
                  'commented_by':user_name.strip(),
                  'comment_date':comment_time,
                  'rank':rank.strip(),
                  'attachment':attachment
                  }
            result=DB.InsertNewRecordInToTable(Conn,"comments",**Dict)
            if result==True:
                return HttpResponseRedirect(reverse('detail_requirement', args=(project_id,requirement_id)))
        else:
            print "no comment"
    else:
        print "not autorized to comment"

#new Requirement page implementation(08.06.2014)
def RequirementPage(request,project_id):
    """
    TC_Id = request.GET.get('TC_Id', '')
    if TC_Id != "":
        return ViewTestCase(TC_Id)
    else:
        templ = get_template('CreateNewRequirement.html')
        variables = Context({ })
        output = templ.render(variables)
        return HttpResponse(output)"""
    #Get the teams for this projects
    Conn=GetConnection()
    query="select id,value from config_values where id in(select cast(team_id as int) from project_team_map where project_id='%s')"%project_id
    team_info=DB.GetData(Conn,query,False)
    query="select value from config_values where type='Priority'"
    priority=DB.GetData(Conn,query,False)
    query="select id,value from config_values where type='milestone'"
    milestone_list=DB.GetData(Conn,query,False)
    query = "select label_id,label_name,Label_color from labels order by label_name"
    labels = DB.GetData(Conn,query,False)
    Dict={
          'team_info':team_info,
          'priority_list':priority,
          'milestone_list':milestone_list,
          'labels':labels
    }
    return render_to_response("CreateNewRequirement.html",Dict)


def Edit_Requirement(request,project_id,req_id):
    """
    TC_Id = request.GET.get('TC_Id', '')
    if TC_Id != "":
        return ViewTestCase(TC_Id)
    else:
        templ = get_template('CreateNewRequirement.html')
        variables = Context({ })
        output = templ.render(variables)
        return HttpResponse(output)"""
    #Get the teams for this projects
    Conn=GetConnection()
    query="select id,value from config_values where id in(select cast(team_id as int) from project_team_map where project_id='%s')"%project_id
    team_info=DB.GetData(Conn,query,False)
    query="select value from config_values where type='Priority'"
    priority=DB.GetData(Conn,query,False)
    query="select id,value from config_values where type='milestone'"
    milestone_list=DB.GetData(Conn,query,False)
    query = "select label_id,label_name,Label_color from labels order by label_name"
    labels = DB.GetData(Conn,query,False)
    Dict={
          'team_info':team_info,
          'priority_list':priority,
          'milestone_list':milestone_list,
          'labels':labels
    }
    return render_to_response("CreateNewRequirement.html",Dict)


def Child_Requirement(request,project_id,req_id):
    """
    TC_Id = request.GET.get('TC_Id', '')
    if TC_Id != "":
        return ViewTestCase(TC_Id)
    else:
        templ = get_template('CreateNewRequirement.html')
        variables = Context({ })
        output = templ.render(variables)
        return HttpResponse(output)"""
    #Get the teams for this projects
    Conn=GetConnection()
    query="select id,value from config_values where id in(select cast(team_id as int) from project_team_map where project_id='%s')"%project_id
    team_info=DB.GetData(Conn,query,False)
    query="select value from config_values where type='Priority'"
    priority=DB.GetData(Conn,query,False)
    query="select id,value from config_values where type='milestone'"
    milestone_list=DB.GetData(Conn,query,False)
    query = "select label_id,label_name,Label_color from labels order by label_name"
    labels = DB.GetData(Conn,query,False)
    Dict={
          'team_info':team_info,
          'priority_list':priority,
          'milestone_list':milestone_list,
          'labels':labels
    }
    return render_to_response("CreateNewRequirement.html",Dict)

        
def TaskPage(request,project_id):
    Conn=GetConnection()
    query="select id,value from config_values where id in(select cast(team_id as int) from project_team_map where project_id='%s')"%project_id
    team_info=DB.GetData(Conn,query,False)
    query="select value from config_values where type='Priority'"
    priority=DB.GetData(Conn,query,False)
    query="select id,value from config_values where type='milestone'"
    milestone_list=DB.GetData(Conn,query,False)
    #get the names from permitted_user_list
    query="select pul.user_id,user_names,user_level from permitted_user_list pul,team_info ti where pul.user_level='assigned_tester' and pul.user_id=cast(ti.user_id as int) and team_id in (select cast(team_id as int) from project_team_map where project_id='%s')"%project_id 
    user_list=DB.GetData(Conn,query,False)
    query = "select label_id,label_name,Label_color from labels order by label_name"
    labels = DB.GetData(Conn,query,False)
    Dict={
          'team_info':team_info,
          'priority_list':priority,
          'milestone_list':milestone_list,
          'user_list':user_list,
          'labels':labels
    }
    return render_to_response("CreateNewTask.html",Dict)

def Get_RequirementSections(request):  #==================Returns Abailable User Name in List as user Type on Run Test Page==============================
    Conn = GetConnection()
    results = []
    # if request.is_ajax():
    if request.method == "GET":
        section = request.GET.get(u'section', '')
        if section == '':
            results = DB.GetData(Conn, "select distinct subpath(requirement_path,0,1) from requirement_sections", False)
            levelnumber = 0
        else:
            levelnumber = section.count('.') + 1
            results = DB.GetData(Conn, "select distinct subltree(requirement_path,%d,%d) FROM requirement_sections WHERE requirement_path ~ '*.%s.*' and nlevel(requirement_path) > %d" % (levelnumber, levelnumber + 1, section, levelnumber), False)

    results.insert(0, (str(levelnumber),))
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def convert_date_from_string(given_date):
    start_date=given_date.split('-')
    starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
    return starting_date                
#function for the new task
def SubmitNewTask(request):
    if request.is_ajax():
        if request.method=='GET':
            title=request.GET.get(u'title','')
            status=request.GET.get(u'status','')
            description=request.GET.get(u'description','')
            start_date=request.GET.get(u'starting_date','')
            end_date=request.GET.get(u'ending_date','')
            start_date=convert_date_from_string(start_date)
            end_date=convert_date_from_string(end_date)
            teams=request.GET.get(u'team','')
            tester=request.GET.get(u'tester','')
            priority=request.GET.get(u'priority','')
            milestone=request.GET.get(u'milestone','')
            project_id=request.GET.get(u'project_id','')
            section_path=request.GET.get(u'section_path','')
            feature_path=request.GET.get(u'feature_path','')
            user_name=request.GET.get(u'user_name','')
            labels = request.GET.get(u'labels','')
            labels=labels.split("|")
            test_cases=request.GET.get(u'test_cases','')
            test_cases=test_cases.split("|")
            requirements=request.GET.get(u'requirements','')
            requirements=requirements.split("|")
            result=TaskOperations.CreateNewTask(title,status,description,start_date,end_date,teams,tester,priority,milestone,project_id,section_path,feature_path,user_name,labels,test_cases,requirements)
    results=simplejson.dumps(result)
    return HttpResponse(results,mimetype='application/json')    

def SubmitEditedTask(request):
    if request.is_ajax():
        if request.method=='GET':
            task_id=request.GET.get(u'task_id','')
            title=request.GET.get(u'title','')
            status=request.GET.get(u'status','')
            description=request.GET.get(u'description','')
            start_date=request.GET.get(u'starting_date','')
            end_date=request.GET.get(u'ending_date','')
            start_date=convert_date_from_string(start_date)
            end_date=convert_date_from_string(end_date)
            teams=request.GET.get(u'team','')
            tester=request.GET.get(u'tester','')
            priority=request.GET.get(u'priority','')
            milestone=request.GET.get(u'milestone','')
            project_id=request.GET.get(u'project_id','')
            section_path=request.GET.get(u'section_path','')
            feature_path=request.GET.get(u'feature_path','')
            user_name=request.GET.get(u'user_name','')
            labels = request.GET.get(u'labels','')
            labels=labels.split("|")
            test_cases=request.GET.get(u'test_cases','')
            test_cases=test_cases.split("|")
            requirements=request.GET.get(u'requirements','')
            requirements=requirements.split("|")
            result=TaskOperations.ModifyTask(task_id,title,status,description,start_date,end_date,teams,tester,priority,milestone,project_id,section_path,feature_path,user_name,labels,test_cases,requirements)
    results=simplejson.dumps(result)
    return HttpResponse(results,mimetype='application/json')    


def SubmitChildTask(request):
    if request.is_ajax():
        if request.method=='GET':
            title=request.GET.get(u'title','')
            status=request.GET.get(u'status','')
            description=request.GET.get(u'description','')
            start_date=request.GET.get(u'starting_date','')
            end_date=request.GET.get(u'ending_date','')
            start_date=convert_date_from_string(start_date)
            end_date=convert_date_from_string(end_date)
            teams=request.GET.get(u'team','')
            tester=request.GET.get(u'tester','')
            priority=request.GET.get(u'priority','')
            milestone=request.GET.get(u'milestone','')
            project_id=request.GET.get(u'project_id','')
            section_path=request.GET.get(u'section_path','')
            feature_path=request.GET.get(u'feature_path','')
            user_name=request.GET.get(u'user_name','')
            labels = request.GET.get(u'labels','')
            labels=labels.split("|")
            test_cases=request.GET.get(u'test_cases','')
            test_cases=test_cases.split("|")
            requirements=request.GET.get(u'requirements','')
            requirements=requirements.split("|")
            result=TaskOperations.CreateChildTask(title,status,description,start_date,end_date,teams,tester,priority,milestone,project_id,section_path,feature_path,user_name,labels,test_cases,requirements)
    results=simplejson.dumps(result)
    return HttpResponse(results,mimetype='application/json')    


def ViewTaskPage(request,project_id):
    return HttpResponse(project_id)    
def GetProfileInfo(request, user_id, success):
    try:
        query="select distinct user_id,full_name,user_level,username from permitted_user_list pul,user_info usr where pul.user_names=usr.full_name and pul.user_id='%s'"%user_id
        Conn=GetConnection()
        user_column=["UserID","FullName","Designation","Username"]
        result=DB.GetData(Conn,query,False)
        temp_dict={}
        for idx,each in enumerate(zip(user_column,result[0])):
            if idx==2:
                temp_dict.update({each[0]:(" ").join(each[1].split("_")).title()})
            else:
                temp_dict.update({each[0]:each[1]})
        
        query="select project_id,project_name from projects"
        project_id=DB.GetData(Conn,query,False)
        temp_dict.update({'projects':project_id})
        #load default projects
        
        query="select default_project,default_team from default_choice where user_id='%s'"%user_id
        testConnection(Conn)
        projects=DB.GetData(Conn,query,False)
        if isinstance(projects,list) and len(projects)==0:
            temp_dict.update({'selected_project_id':"",'selected_team_id':""})
        else:
            temp_dict.update({'selected_project_id':projects[0][0],'selected_team_id':projects[0][1]})
        #get team for the definite projects
        if(temp_dict['selected_project_id']!=""):
            query="select id,value from config_values where id in(select cast(team_id as int) from project_team_map where project_id='%s')"%temp_dict['selected_project_id']
            testConnection(Conn)
            team_id=DB.GetData(Conn,query,False)
            temp_dict.update({'teams':team_id})
            
        temp_dict.update({'success': success})
        
        temp_dict = RequestContext(request, temp_dict)
        return render_to_response("AccountInfo.html",temp_dict)
    except Exception,e:
        print "Exception:",e
def GetTeamInfoPerProject(request):
    if request.is_ajax():
        if request.method=='GET':
            project_id=request.GET.get(u'project_id','')
            query="select id,value from project_team_map ptm,config_values c where cast(ptm.team_id as int)=c.id and ptm.project_id='%s'"%project_id
            Conn=GetConnection()
            try:
                testConnection(Conn)
                team_id=DB.GetData(Conn,query,False)
                Dict={'teams':team_id}
                message=simplejson.dumps(Dict)
                return HttpResponse(message,mimetype='application/json')
            except Exception,e:
                print "Exception:",e
def updateAccountInfo(request):
    if request.is_ajax():
        if request.method=='GET':
            old_full_name=request.GET.get(u'old_full_name','')
            full_name=request.GET.get(u'full_name','')
            user_name=request.GET.get(u'user_name','')
            project_id=request.GET.get(u'project_id','')
            team_id=request.GET.get(u'team_id','')
            user_id=request.GET.get(u'user_id','')
            try:
                Conn=GetConnection()
                #form dict according to the change
                temp_dict={}
                if full_name!="":
                    temp_dict.update({'full_name':full_name.strip()})
                if user_name!="":
                    temp_dict.update({'username':user_name.strip()})
                if len(temp_dict.keys())!=0:
                    
                    sWhereQuery="where full_name='%s'"%full_name
                    result=DB.UpdateRecordInTable(Conn,"user_info",sWhereQuery,**temp_dict)
                    if result==True:
                        testConnection(Conn)
                        if 'full_name' in temp_dict.keys() and 'username' in temp_dict.keys():
                            del temp_dict['username']
                        sWhereQuery="where user_id='%s'"%user_id
                        result=DB.UpdateRecordInTable(Conn,"permitted_user_list",sWhereQuery,**temp_dict)
                #check to update or create
                query="select count(*) from default_choice where user_id='%s'"%user_id
                testConnection(Conn)
                result=DB.GetData(Conn,query)
                if(isinstance(result,list) and result[0]==0):
                    #create a new dict
                    dict={
                          'user_id':user_id,
                          'default_project':project_id,
                          'default_team':team_id
                    }
                    testConnection(Conn)
                    result=DB.InsertNewRecordInToTable(Conn,"default_choice",**dict)
                    if result==True:
                        message= True
                    else:
                        message=False
                else:                    
                    dict={}
                    if project_id!="":
                        dict.update({'default_project':project_id})
                    if team_id!="":
                        dict.update({'default_team':team_id})
                    sWhereQuery="where user_id='%s'"%user_id
                    result=DB.UpdateRecordInTable(Conn,"default_choice",sWhereQuery,**dict)
                    if result==True:
                        message=True
                    else:
                        message=False
                result=simplejson.dumps(message)
                return HttpResponse(result,mimetype='application/json')
            except Exception,e:
                print "Exception:",e
                
def UpdateDefaultTeamForUser(request):
    if request.is_ajax():
        if request.method=='GET':
            user_id=request.GET.get(u'user_id','').strip()
            team_id=request.GET.get(u'team_id','').strip()
            sWhereQuery="where user_id='%s'"%user_id
            Conn=GetConnection()
            result=DB.UpdateRecordInTable(Conn, "default_choice", sWhereQuery,default_team=team_id)
            if result==True:
                message=True
            else:
                message=False
            result=simplejson.dumps(message)
            return HttpResponse(result,mimetype='application/json')
def UpdateDefaultProjectForUser(request):
    if request.is_ajax():
        if request.method=='GET':
            user_id=request.GET.get(u'user_id','').strip()
            project_id=request.GET.get(u'project_id','').strip()
            sWhereQuery="where user_id='%s'"%user_id
            Conn=GetConnection()
            result=DB.UpdateRecordInTable(Conn, "default_choice", sWhereQuery,default_project=project_id)
            if result==True:
                message=True
            else:
                message=False
            result=simplejson.dumps(message)
            return HttpResponse(result,mimetype='application/json')

#for the assign test PAGES
def assign_settings(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        return render_to_response('AssignSettings.html',{})
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
        
#myConfiguration Shetu don't change#        
success_tag=1
warning_tag=2
error_tag=3
DBError="Database Connection Error.Try Again.."
AjaxError="Ajax call is expected here"
PostError="Can't take any post request"
def multiple_instance(name,type_tag):
    return type_tag+":'"+name+"' already exists in the database"
def entry_success(name,type_tag):
    return type_tag+":'"+name+"' successfully inserted"
def entry_fail(name,type_tag):
    return type_tag+":'"+name+"' is failed  to insert"
def update_success(old_name,new_name,type_tag):
    return type_tag+":'"+old_name+"' is updated to '"+new_name+"'"
def update_fail(name,type_tag):
    return type_tag+":'"+name+"' is failed  to update"
def unavailable(name,type_tag):
    return type_tag+":'"+name+"' is not in database"
#myConfiguration Shetu don't change#

#get all the data from the assign settings page
def get_all_data_dependency_page(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                #dependency_tab
                query="select distinct d.id,d.dependency_name from dependency d,dependency_management dm where d.id=dm.dependency and dm.project_id='%s' and dm.team_id=%d"%(project_id.strip(),int(team_id.strip()))
                Conn=GetConnection()
                dependency_list=DB.GetData(Conn,query,False)
                Conn.close()
                query="select distinct d.id,d.dependency_name as name from dependency d except(select distinct d.id,d.dependency_name from dependency d,dependency_management dm where d.id=dm.dependency and dm.project_id='%s' and dm.team_id=%d) order by name"%(project_id.strip(),int(team_id.strip()))
                Conn=GetConnection()
                unused_dependency_list=DB.GetData(Conn,query,False)
                Conn.close()
                query="select distinct b.id,b.branch_name from branch b,branch_management bm where b.id=bm.branch and bm.project_id='%s' and bm.team_id=%d"%(project_id.strip(),int(team_id.strip()))
                Conn=GetConnection()
                branch_list=DB.GetData(Conn,query,False)
                Conn.close()
                query="select distinct id,branch_name from branch except (select distinct b.id,b.branch_name from branch b,branch_management bm where b.id=bm.branch and bm.project_id='%s' and bm.team_id=%d)"%(project_id.strip(),int(team_id.strip()))
                Conn=GetConnection()
                unused_branch_list=DB.GetData(Conn,query,False)
                Conn.close()
                query="select distinct subltree(feature_path,0,1),subltree(feature_path,0,1) from product_features f,feature_management fm where f.feature_id=fm.feature and fm.project_id='%s' and fm.team_id=%d"%(project_id.strip(),int(team_id.strip()))
                Conn=GetConnection()
                feature_list=DB.GetData(Conn,query,False)
                Conn.close()
                query="select distinct subltree(feature_path,0,1),subltree(feature_path,0,1) from product_features except (select distinct subltree(f.feature_path,0,1),subltree(f.feature_path,0,1) from product_features f,feature_management fm where f.feature_id=fm.feature and fm.project_id='%s' and fm.team_id=%d)"%(project_id.strip(),int(team_id.strip()))
                Conn=GetConnection()
                unused_feature_list=DB.GetData(Conn,query,False)
                Conn.close()
                result={
                    'dependency_list':dependency_list,
                    'unused_dependency_list':unused_dependency_list,
                    'branch_list':branch_list,
                    'unused_branch_list':unused_branch_list,
                    'feature_list':feature_list,
                    'unused_feature_list':unused_feature_list
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
    
#create new dependency in dependency tab
def add_new_dependency(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag="dependency"
                dependency=request.GET.get(u'dependency_name','')
                #check for the occurance
                query="select count(*) from dependency where dependency_name='%s'"%dependency.strip()
                Conn=GetConnection()
                count=DB.GetData(Conn,query)
                if isinstance(count,list):
                    if len(count)==1 and count[0]==0:
                        #form dict to insert 
                        Dict={
                              'dependency_name':dependency.strip()
                        }
                        Conn=GetConnection()
                        result=DB.InsertNewRecordInToTable(Conn,"dependency",**Dict)
                        Conn.close()
                        if result==True:
                            PassMessasge(sModuleInfo,entry_success(dependency,type_tag), success_tag)
                            message=True
                            log_message=entry_success(dependency,type_tag)
                        else:
                            PassMessasge(sModuleInfo, entry_fail(dependency, type_tag), error_tag)
                            message=False
                            log_message=entry_fail(dependency, type_tag)
                    if len(count)==1 and count[0]>0:
                        PassMessasge(sModuleInfo,multiple_instance(dependency, type_tag), error_tag)
                        message=False
                        log_message=multiple_instance(dependency, type_tag)
                else:
                    PassMessasge(sModuleInfo, DBError, error_tag)
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
            
def add_new_name_dependency(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag="Dependency Name"
                new_name=request.GET.get(u'new_name','')
                new_value=request.GET.get(u'new_value','')
                query="select count(*) from dependency_name where name='%s'"%(new_name.strip())
                Conn=GetConnection()
                count=DB.GetData(Conn,query)
                Conn.close()
                if isinstance(count,list):
                    if len(count)==1 and count[0]==0:
                        Dict={
                            'name':new_name.strip(),
                            'dependency_id':int(new_value.strip())
                        }
                        Conn=GetConnection()
                        result=DB.InsertNewRecordInToTable(Conn,"dependency_name",**Dict)
                        Conn.close()
                        if result==True:
                            PassMessasge(sModuleInfo,entry_success(new_name.strip(), type_tag), success_tag)
                            message=True
                            log_message=entry_success(new_name.strip(), type_tag)
                        else:
                            PassMessasge(sModuleInfo,entry_fail(new_name.strip(), type_tag),error_tag)
                            message=False
                            log_message=entry_fail(new_name.strip(), type_tag)
                    if len(count)==1 and count[0]>0:
                        PassMessasge(sModuleInfo,multiple_instance(new_name, type_tag), error_tag)
                        message=False
                        log_message=multiple_instance(new_name, type_tag)
                else:
                    PassMessasge(sModuleInfo,DBError,error_tag)
                    message=True
                    log_message=DBError
                Conn.close()
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)

def get_all_name_under_dependency(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                project_id=request.GET.get(u'project_id','')
                value=request.GET.get(u'value',''),
                team_id=request.GET.get(u'team_id','')
                print value[0]
                print project_id
                print team_id
                query="select dn.id,dn.name as name from dependency_name dn,dependency_management dm where dm.dependency=dn.dependency_id and project_id='%s' and team_id=%d and dm.dependency=%d order by name"%(project_id,int(team_id),int(value[0]))
                Conn=GetConnection()
                dependency_list=DB.GetData(Conn,query,False)
                Conn.close()
                #get the default list
                query="select default_choices from dependency_management where project_id ='%s' and team_id=%d and dependency=%d"%(project_id,int(team_id),int(value[0]))
                Conn=GetConnection()
                default_list=DB.GetData(Conn,query)
                Conn.close()
                result={
                    'dependency_list':dependency_list,
                    'default_list':default_list
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def rename_dependency(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag="dependency"
                old_name=request.GET.get(u'old_name','')
                new_name=request.GET.get(u'new_name','')
                query="select count(*) from dependency where dependency_name='%s'"%old_name.strip()
                Conn=GetConnection()
                old_name_count=DB.GetData(Conn,query)
                Conn.close()
                query="select count(*) from dependency where dependency_name='%s'"%new_name.strip()
                Conn=GetConnection()
                new_name_count=DB.GetData(Conn,query)
                Conn.close()
                if isinstance(old_name_count,list):
                    if len(old_name_count)==1 and old_name_count[0]>0:
                        if len(new_name_count)==1 and new_name_count[0]==0:
                            sWhereQuery="where dependency_name='%s'"%old_name.strip()
                            Dict={
                                'dependency_name':new_name.strip()
                            }
                            Conn=GetConnection()
                            result=DB.UpdateRecordInTable(Conn,"dependency", sWhereQuery,**Dict)
                            Conn.close()
                            if result==True:
                                PassMessasge(sModuleInfo,update_success(old_name, new_name, type_tag), success_tag)
                                message=True
                                log_message=update_success(old_name, new_name, type_tag)
                            else:
                                PassMessasge(sModuleInfo, update_fail(old_name, type_tag), error_tag)
                                message=False
                                log_message=update_fail(old_name, type_tag)
                        if len(new_name_count)==1 and new_name_count[0]>0:
                            PassMessasge(sModuleInfo,multiple_instance(new_name, type_tag),error_tag)
                            message=False
                            log_message=multiple_instance(new_name,type_tag)
                    if len(old_name_count)==1 and old_name_count[0]==0:
                        PassMessasge(sModuleInfo, unavailable(old_name,type_tag), error_tag)
                        message=False
                        log_message=unavailable(old_name, type_tag)
                else:
                    PassMessasge(sModuleInfo,DBError, error_tag)
                    message=False
                    log_message=DBError
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def add_new_version(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                bit=request.GET.get(u'bit','')
                version=request.GET.get(u'version','')
                value=request.GET.get(u'value','')
                #check for occurances
                query="select count(*) from dependency_values where bit_name='%s' and version='%s' and id=%d"%(bit,version,int(value))
                Conn=GetConnection()
                count=DB.GetData(Conn,query)
                Conn.close()
                if isinstance(count,list):
                    if len(count)==1 and count[0]==0:
                        Dict={
                            'id':int(value),
                            'version':version,
                            'bit_name':bit
                        }
                        Conn=GetConnection()
                        result=DB.InsertNewRecordInToTable(Conn,"dependency_values",**Dict)
                        if result==True:
                            PassMessasge(sModuleInfo, "Version '%s':%d bit is inserted successfully"%(version,int(bit)),success_tag)
                            message=True
                            log_message="Version '%s':%d bit is inserted successfully"%(version,int(bit))
                        else:
                            PassMessasge(sModuleInfo, "Version '%s':%d bit is failed to insert"%(version,int(bit)),error_tag)
                            message=False
                            log_message="Version '%s':%d bit is failed to insert"%(version,int(bit))
                    if len(count)==1 and count[0]>0:
                        PassMessasge(sModuleInfo, "Version '%s':%d bit is already in the database"%(version,int(bit)),error_tag)
                        message=False
                        log_message="Version '%s':%d bit is already in the database"%(version,int(bit))
                else:
                    PassMessasge(sModuleInfo,DBError,error_tag)
                    message=False
                    log_message=DBError
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def get_all_version_bit(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                value=request.GET.get(u'value','')
                query="select bit_name|| ' Bit' as bit,array_to_string(array_agg(distinct version),',') from dependency_values dv,dependency_name dn where dv.id=dn.id and dn.id=%d group by bit_name order by bit"%(int(value))
                Conn=GetConnection()
                version_list=DB.GetData(Conn,query,False)
                Conn.close()
                result={
                    'version_list':version_list
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
                
def link_dependency(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                value=request.GET.get(u'value','')
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                Dict={
                    'project_id':project_id,
                    'team_id':int(team_id),
                    'dependency':int(value)
                }
                Conn=GetConnection()
                result=DB.InsertNewRecordInToTable(Conn,"dependency_management",**Dict)
                Conn.close()
                if result==True:
                    PassMessasge(sModuleInfo,"Dependency %d is linked successfully"%int(value),error_tag )
                    message=True
                    log_message="Dependency is linked successfully"
                else:
                    PassMessasge(sModuleInfo,"Dependency %d is not linked successfully"%int(value),error_tag )
                    message=False
                    log_message="Dependency is not linked successfully"
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
        
def unlink_dependency(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                value=request.GET.get(u'value','')
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                Dict={
                    'project_id':project_id,
                    'team_id':int(team_id),
                    'dependency':int(value)
                }
                Conn=GetConnection()
                result=DB.DeleteRecord(Conn,"dependency_management",**Dict)
                Conn.close()
                if result==True:
                    PassMessasge(sModuleInfo,"Dependency %d is unlinked successfully"%int(value),error_tag )
                    message=True
                    log_message="Dependency is unlinked successfully"
                else:
                    PassMessasge(sModuleInfo,"Dependency %d is not unlinked successfully"%int(value),error_tag )
                    message=False
                    log_message="Dependency is not unlinked successfully"
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def rename_name(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag="dependency name"
                old_name=request.GET.get(u'old_name','')
                new_name=request.GET.get(u'new_name','')
                query="select count(*) from dependency_name where name='%s'"%old_name.strip()
                Conn=GetConnection()
                old_name_count=DB.GetData(Conn,query)
                Conn.close()
                query="select count(*) from dependency_name where name='%s'"%new_name.strip()
                Conn=GetConnection()
                new_name_count=DB.GetData(Conn,query)
                Conn.close()
                if isinstance(old_name_count,list):
                    if len(old_name_count)==1 and old_name_count[0]>0:
                        if len(new_name_count)==1 and new_name_count[0]==0:
                            sWhereQuery="where name='%s'"%old_name.strip()
                            Dict={
                                'name':new_name.strip()
                            }
                            Conn=GetConnection()
                            result=DB.UpdateRecordInTable(Conn,"dependency_name", sWhereQuery,**Dict)
                            Conn.close()
                            if result==True:
                                PassMessasge(sModuleInfo,update_success(old_name, new_name, type_tag), success_tag)
                                message=True
                                log_message=update_success(old_name, new_name, type_tag)
                            else:
                                PassMessasge(sModuleInfo, update_fail(old_name, type_tag), error_tag)
                                message=False
                                log_message=update_fail(old_name, type_tag)
                        if len(new_name_count)==1 and new_name_count[0]>0:
                            PassMessasge(sModuleInfo,multiple_instance(new_name, type_tag),error_tag)
                            message=False
                            log_message=multiple_instance(new_name,type_tag)
                    if len(old_name_count)==1 and old_name_count[0]==0:
                        PassMessasge(sModuleInfo, unavailable(old_name,type_tag), error_tag)
                        message=False
                        log_message=unavailable(old_name, type_tag)
                else:
                    PassMessasge(sModuleInfo,DBError, error_tag)
                    message=False
                    log_message=DBError
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)

def make_default_name(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                name=request.GET.get(u'name','')
                dependency=request.GET.get(u'dependency','')
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                tag=request.GET.get(u'tag','')
                #take out the default choices
                query="select default_choices from dependency_management where project_id='%s' and team_id=%d and dependency=%d"%(project_id,int(team_id),int(dependency))
                Conn=GetConnection()
                default_choice=DB.GetData(Conn,query)
                Conn.close()
                print default_choice
                if isinstance(default_choice,list):
                    if tag=="make_default":
                        if default_choice[0]==None:
                            modified_choice=name.strip()
                        else:
                            modified_choice=(default_choice[0]+","+name.strip()).strip()
                        #print modified_choice
                    if tag=='remove_default':
                        default_choice=default_choice[0].split(",")
                        #print default_choice
                        default_choice.remove(name)
                        modified_choice=(",").join(default_choice)
                        print modified_choice
                        
                    sWhereQuery="where project_id='%s' and team_id=%d and dependency=%d"%(project_id,int(team_id),int(dependency))
                    Dict={
                        'default_choices':modified_choice.strip()
                    }
                    Conn=GetConnection()
                    result=DB.UpdateRecordInTable(Conn,"dependency_management",sWhereQuery,**Dict)
                    Conn.close()
                    if result==True:
                        if tag=="make_default":
                            PassMessasge(sModuleInfo, "name %d under dependency '%s' is made default"%(int(name),dependency), success_tag)
                        if tag=='remove_default':
                            PassMessasge(sModuleInfo, "name %d under dependency '%s' is removed from default"%(int(name),dependency), success_tag)
                        message=True
                        log_message="Operation Successful"
                    else:
                        if tag=="make_default":
                            PassMessasge(sModuleInfo, "name %d under dependency '%s' is failed to make default"%(int(name),dependency), error_tag)
                        if tag=='remove_default':
                            PassMessasge(sModuleInfo, "name %d under dependency '%s' is failed to remove default"%(int(name),dependency), error_tag)
                        message=False
                        log_message="Operation Fail"
                else:
                    PassMessasge(sModuleInfo,DBError,error_tag)
                    message=False
                    log_message=DBError
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)

def get_default_settings(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            
            if request.is_ajax():
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                query="select distinct d.id,d.dependency_name,array_to_string(array_agg(distinct dn.name),',') from dependency d ,dependency_management dm, dependency_name dn where d.id=dm.dependency and dm.dependency=dn.dependency_id and dn.dependency_id =d.id and dm.project_id='%s' and dm.team_id=%d group by d.dependency_name,d.id order by d.dependency_name"%(project_id,int(team_id))
                Conn=GetConnection()
                result=DB.GetData(Conn,query,False)
                Conn.close()
                final_list=[]
                for each in result:
                    query="select default_choices from dependency_management where project_id='%s' and team_id=%d and dependency=%d"%(project_id,int(team_id),int(each[0]))
                    Conn=GetConnection()
                    default_choices=DB.GetData(Conn,query)
                    print default_choices
                    Conn.close()
                    temp=[]
                    if isinstance(default_choices,list):
                        if default_choices[0]!='':
                            for eachitem in default_choices[0].split(","):
                                query="select name from dependency_name where id=%d and dependency_id=%d"%(int(eachitem),int(each[0]))
                                Conn=GetConnection()
                                name_list=DB.GetData(Conn,query)
                                if isinstance(name_list,list):
                                    temp.append(name_list[0])
                        else:
                            temp=[]
                    final_list.append((each[1],each[2],temp))
                print final_list
                result={
                    'result':final_list
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)    
def add_new_branch(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag='Branch'
                branch_name=request.GET.get(u'dependency_name','')
                #check for the occurance
                query="select count(*) from branch where branch_name='%s'"%branch_name.strip()
                Conn=GetConnection()
                count=DB.GetData(Conn,query)
                if isinstance(count,list):
                    if len(count)==1 and count[0]==0:
                        #form dict to insert 
                        Dict={
                              'branch_name':branch_name.strip()
                        }
                        Conn=GetConnection()
                        result=DB.InsertNewRecordInToTable(Conn,"branch",**Dict)
                        Conn.close()
                        if result==True:
                            PassMessasge(sModuleInfo,entry_success(branch_name,type_tag), success_tag)
                            message=True
                            log_message=entry_success(branch_name,type_tag)
                        else:
                            PassMessasge(sModuleInfo, entry_fail(branch_name, type_tag), error_tag)
                            message=False
                            log_message=entry_fail(branch_name, type_tag)
                    if len(count)==1 and count[0]>0:
                        PassMessasge(sModuleInfo,multiple_instance(branch_name, type_tag), error_tag)
                        message=False
                        log_message=multiple_instance(branch_name, type_tag)
                else:
                    PassMessasge(sModuleInfo, DBError, error_tag)
                result={
                    'message':message,
                    'log_message':log_message
                }
                
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)    
def get_all_version_under_branch(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                project_id=request.GET.get(u'project_id','')
                value=request.GET.get(u'value',''),
                team_id=request.GET.get(u'team_id','')
                print value[0]
                print project_id
                print team_id
                query="select distinct version_name as name from branch_management bm, versions v where v.id=bm.branch and bm.project_id='%s' and bm.team_id=%d and bm.branch=%d order by name"%(project_id,int(team_id),int(value[0]))
                Conn=GetConnection()
                version_list=DB.GetData(Conn,query,False)
                Conn.close()
                result={
                    'version_list':version_list,
                    'default_list':[]
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def add_new_version_branch(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag="Branch Version"
                new_name=request.GET.get(u'new_name','')
                new_value=request.GET.get(u'new_value','')
                query="select count(*) from versions where version_name='%s'"%(new_name.strip())
                Conn=GetConnection()
                count=DB.GetData(Conn,query)
                Conn.close()
                if isinstance(count,list):
                    if len(count)==1 and count[0]==0:
                        Dict={
                            'version_name':new_name.strip(),
                            'id':int(new_value.strip())
                        }
                        Conn=GetConnection()
                        result=DB.InsertNewRecordInToTable(Conn,"versions",**Dict)
                        Conn.close()
                        if result==True:
                            PassMessasge(sModuleInfo,entry_success(new_name.strip(), type_tag), success_tag)
                            message=True
                            log_message=entry_success(new_name.strip(), type_tag)
                        else:
                            PassMessasge(sModuleInfo,entry_fail(new_name.strip(), type_tag),error_tag)
                            message=False
                            log_message=entry_fail(new_name.strip(), type_tag)
                    if len(count)==1 and count[0]>0:
                        PassMessasge(sModuleInfo,multiple_instance(new_name, type_tag), error_tag)
                        message=False
                        log_message=multiple_instance(new_name, type_tag)
                else:
                    PassMessasge(sModuleInfo,DBError,error_tag)
                    message=True
                    log_message=DBError
                Conn.close()
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def rename_branch(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag="Branch"
                old_name=request.GET.get(u'old_name','')
                new_name=request.GET.get(u'new_name','')
                query="select count(*) from branch where branch_name='%s'"%old_name.strip()
                Conn=GetConnection()
                old_name_count=DB.GetData(Conn,query)
                Conn.close()
                query="select count(*) from branch where branch_name='%s'"%new_name.strip()
                Conn=GetConnection()
                new_name_count=DB.GetData(Conn,query)
                Conn.close()
                if isinstance(old_name_count,list):
                    if len(old_name_count)==1 and old_name_count[0]>0:
                        if len(new_name_count)==1 and new_name_count[0]==0:
                            sWhereQuery="where branch_name='%s'"%old_name.strip()
                            Dict={
                                'branch_name':new_name.strip()
                            }
                            Conn=GetConnection()
                            result=DB.UpdateRecordInTable(Conn,"branch", sWhereQuery,**Dict)
                            Conn.close()
                            if result==True:
                                PassMessasge(sModuleInfo,update_success(old_name, new_name, type_tag), success_tag)
                                message=True
                                log_message=update_success(old_name, new_name, type_tag)
                            else:
                                PassMessasge(sModuleInfo, update_fail(old_name, type_tag), error_tag)
                                message=False
                                log_message=update_fail(old_name, type_tag)
                        if len(new_name_count)==1 and new_name_count[0]>0:
                            PassMessasge(sModuleInfo,multiple_instance(new_name, type_tag),error_tag)
                            message=False
                            log_message=multiple_instance(new_name,type_tag)
                    if len(old_name_count)==1 and old_name_count[0]==0:
                        PassMessasge(sModuleInfo, unavailable(old_name,type_tag), error_tag)
                        message=False
                        log_message=unavailable(old_name, type_tag)
                else:
                    PassMessasge(sModuleInfo,DBError, error_tag)
                    message=False
                    log_message=DBError
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
        
def unlink_branch(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                value=request.GET.get(u'value','')
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                Dict={
                    'project_id':project_id,
                    'team_id':int(team_id),
                    'branch':int(value)
                }
                Conn=GetConnection()
                result=DB.DeleteRecord(Conn,"branch_management",**Dict)
                Conn.close()
                if result==True:
                    PassMessasge(sModuleInfo,"Branch %d is unlinked successfully"%int(value),error_tag )
                    message=True
                    log_message="Branch is unlinked successfully"
                else:
                    PassMessasge(sModuleInfo,"Branch %d is not unlinked successfully"%int(value),error_tag )
                    message=False
                    log_message="Branch is not unlinked successfully"
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def link_branch(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                value=request.GET.get(u'value','')
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                Dict={
                    'project_id':project_id,
                    'team_id':int(team_id),
                    'branch':int(value)
                }
                Conn=GetConnection()
                result=DB.InsertNewRecordInToTable(Conn,"branch_management",**Dict)
                Conn.close()
                if result==True:
                    PassMessasge(sModuleInfo,"Branch %d is linked successfully"%int(value),error_tag )
                    message=True
                    log_message="Branch is linked successfully"
                else:
                    PassMessasge(sModuleInfo,"Branch %d is not linked successfully"%int(value),error_tag )
                    message=False
                    log_message="Branch is not linked successfully"
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
#feature tab code
def add_new_feature(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag="feature"
                dependency=request.GET.get(u'feature_path','')
                #check for the occurance
                query="select count(*) from product_features where feature_path='%s'"%dependency.strip()
                Conn=GetConnection()
                count=DB.GetData(Conn,query)
                if isinstance(count,list):
                    if len(count)==1 and count[0]==0:
                        #form dict to insert 
                        Dict={
                              'feature_path':dependency.strip()
                        }
                        Conn=GetConnection()
                        result=DB.InsertNewRecordInToTable(Conn,"product_features",**Dict)
                        Conn.close()
                        if result==True:
                            PassMessasge(sModuleInfo,entry_success(dependency,type_tag), success_tag)
                            message=True
                            log_message=entry_success(dependency,type_tag)
                        else:
                            PassMessasge(sModuleInfo, entry_fail(dependency, type_tag), error_tag)
                            message=False
                            log_message=entry_fail(dependency, type_tag)
                    if len(count)==1 and count[0]>0:
                        PassMessasge(sModuleInfo,multiple_instance(dependency, type_tag), error_tag)
                        message=False
                        log_message=multiple_instance(dependency, type_tag)
                else:
                    PassMessasge(sModuleInfo, DBError, error_tag)
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)

def link_feature(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag="Feature"
                value=request.GET.get(u'value','')
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                query="select feature_id from product_features where feature_path ~ '%s'"%value
                Conn=GetConnection()
                feature_id=DB.GetData(Conn,query)
                Conn.close()
                Dict={
                    'project_id':project_id,
                    'team_id':int(team_id),
                    'feature':int(feature_id[0])
                }
                value=feature_id[0]
                Conn=GetConnection()
                result=DB.InsertNewRecordInToTable(Conn,"feature_management",**Dict)
                nDict={
                    'project_id':project_id,
                    'team_id':int(team_id),
                    'parameters':int(feature_id[0]),
                    'type':"Feature"
                }
                result=DB.InsertNewRecordInToTable(Conn,"team_wise_settings",**nDict)
                Conn.close()
                if result==True:
                    PassMessasge(sModuleInfo,"%s %d is linked successfully"%(type_tag,int(value)),error_tag )
                    message=True
                    log_message="%s is linked successfully"%type_tag
                else:
                    PassMessasge(sModuleInfo,"%s %d is not linked successfully"%(type_tag,int(value)),error_tag )
                    message=False
                    log_message="%s is not linked successfully"%type_tag
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def unlink_feature(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag='Feature'
                value=request.GET.get(u'value','')
                project_id=request.GET.get(u'project_id','')
                team_id=request.GET.get(u'team_id','')
                query="select feature_id from product_features where feature_path ~ '%s'"%value
                Conn=GetConnection()
                feature_id=DB.GetData(Conn,query)
                Conn.close()
                Dict={
                    'project_id':project_id,
                    'team_id':int(team_id),
                    'feature':int(feature_id[0])
                }
                value=feature_id[0]
                Conn=GetConnection()
                result=DB.DeleteRecord(Conn,"feature_management",**Dict)
                nDict={
                    'project_id':project_id,
                    'team_id':int(team_id),
                    'parameters':int(feature_id[0]),
                    'type':"Feature"
                }
                result=DB.DeleteRecord(Conn,"team_wise_settings",**nDict)
                Conn.close()
                if result==True:
                    PassMessasge(sModuleInfo,"%s %d is unlinked successfully"%(type_tag,int(value)),error_tag )
                    message=True
                    log_message="%s is unlinked successfully"%type_tag
                else:
                    PassMessasge(sModuleInfo,"%s %d is not unlinked successfully"%(type_tag,int(value)),error_tag )
                    message=False
                    log_message="%s is not unlinked successfully"%type_tag
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def rename_feature(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag="Feature"
                old_name=request.GET.get(u'old_name','')
                new_name=request.GET.get(u'new_name','')
                query="select count(*) from product_features where feature_path='%s'"%old_name.strip()
                Conn=GetConnection()
                old_name_count=DB.GetData(Conn,query)
                Conn.close()
                query="select count(*) from product_features where feature_path='%s'"%new_name.strip()
                Conn=GetConnection()
                new_name_count=DB.GetData(Conn,query)
                Conn.close()
                if isinstance(old_name_count,list):
                    if len(old_name_count)==1 and old_name_count[0]>0:
                        if len(new_name_count)==1 and new_name_count[0]==0:
                            sWhereQuery="where feature_path='%s'"%old_name.strip()
                            Dict={
                                'feature_path':new_name.strip()
                            }
                            Conn=GetConnection()
                            result=DB.UpdateRecordInTable(Conn,"product_features", sWhereQuery,**Dict)
                            Conn.close()
                            if result==True:
                                PassMessasge(sModuleInfo,update_success(old_name, new_name, type_tag), success_tag)
                                message=True
                                log_message=update_success(old_name, new_name, type_tag)
                            else:
                                PassMessasge(sModuleInfo, update_fail(old_name, type_tag), error_tag)
                                message=False
                                log_message=update_fail(old_name, type_tag)
                        if len(new_name_count)==1 and new_name_count[0]>0:
                            PassMessasge(sModuleInfo,multiple_instance(new_name, type_tag),error_tag)
                            message=False
                            log_message=multiple_instance(new_name,type_tag)
                    if len(old_name_count)==1 and old_name_count[0]==0:
                        PassMessasge(sModuleInfo, unavailable(old_name,type_tag), error_tag)
                        message=False
                        log_message=unavailable(old_name, type_tag)
                else:
                    PassMessasge(sModuleInfo,DBError, error_tag)
                    message=False
                    log_message=DBError
                result={
                    'message':message,
                    'log_message':log_message
                }
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)

def get_all_first_level_sub_feature(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name 
    try:
        if request.method=='GET':
            if request.is_ajax():
                project_id=request.GET.get(u'project_id','')
                name=request.GET.get(u'name',''),
                team_id=request.GET.get(u'team_id','')
                print name
                print project_id
                print team_id
                level_count=name[0].count('.')+1
                query="select distinct subltree(feature_path,%d,%d) from product_features where nlevel(feature_path)>%d and feature_path ~'*.%s.*'"%(int(level_count),int(level_count)+1,int(level_count),name[0].strip())
                Conn=GetConnection()
                version_list=DB.GetData(Conn,query,False)
                Conn.close()
                result={
                        'version_list':version_list,
                        'default_list':[]
                        }
                 
                result=simplejson.dumps(result)
                return HttpResponse(result,mimetype='application/json')
    except Exception,e:
        PassMessasge(sModuleInfo, e, 3)
def CreateLevelWiseFeature(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                type_tag='Sub Feature'
                new_name=request.GET.get(u'name','')
                query="select count(*) from product_features where feature_path='%s'"%new_name.strip()
                Conn=GetConnection()
                count=DB.GetData(Conn,query)
                Conn.close()
                if isinstance(count,list):
                    if len(count)==1 and count[0]==0:
                        query="insert into product_features(feature_path) values('%s')"%new_name.strip()
                        Conn=GetConnection()
                        cur=Conn.cursor()
                        cur.execute(query)
                        Conn.commit()
                        cur.close()
                        Conn.close()
                        PassMessasge(sModuleInfo, entry_success(new_name, type_tag), success_tag)
                        result={'log_message':entry_success(new_name, type_tag),'message':True}
                        result=simplejson.dumps(result)
                        return HttpResponse(result,mimetype='application/json')    
                    if len(count)==1 and count[0]>0:
                        PassMessasge(sModuleInfo,multiple_instance(new_name, type_tag), error_tag)
                        message=False
                        log_message=multiple_instance(new_name, type_tag)
                        result={'message':message,'log_message':log_message}
                        result=simplejson.dumps(result)
                        return HttpResponse(result,mimetype='application/json')
                else:
                    PassMessasge(sModuleInfo, DBError, error_tag)
                    
            else:
                PassMessasge(sModuleInfo,AjaxError, error_tag)
        else:
            PassMessasge(sModuleInfo, PostError, error_tag)
    except Exception,e:
            PassMessasge(sModuleInfo, e, 3)
def AutoTestCasePass(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.method=='GET':
            if request.is_ajax():
                run_id=request.GET.get(u'run_id','')
                test_cases=request.GET.get(u'test_cases','').split('|')
                for each in test_cases:
                    query="select tsr.id, teststep_id from test_case_results tcr, test_step_results tsr where tcr.run_id=tsr.run_id and tsr.testcaseresulttindex=tcr.id and tcr.run_id='%s' and tcr.tc_id='%s'"%(run_id.strip(),each.strip())
                    Conn=GetConnection()
                    test_step_list=DB.GetData(Conn,query,False)
                    Conn.close()
                    Dict={'status':'Passed'}
                    for eachitem in test_step_list:
                        sWhereQuery="where id=%d and teststep_id=%d and run_id='%s' and tc_id='%s'"%(eachitem[0],eachitem[1],run_id.strip(),each.strip())
                        Conn=GetConnection()
                        print DB.UpdateRecordInTable(Conn, "test_step_results", sWhereQuery,**Dict)
                        Conn.close()
                    sWhereQuery="where run_id='%s' and tc_id='%s'"%(run_id.strip(),each.strip())
                    Conn=GetConnection()
                    Dict.update({'failreason':''})
                    print DB.UpdateRecordInTable(Conn,"test_case_results",sWhereQuery,**Dict)
                    Conn.close()
                message=True
                result=simplejson.dumps(message)
                return HttpResponse(result,mimetype='application/json')                        
    except Exception,e:
            PassMessasge(sModuleInfo, e, 3)
def specific_dependency_settings(request):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        if request.is_ajax():
            if request.method == 'GET':
                UserData = request.GET.get(u'Query', '')
                if UserData!='':
                    UserText = UserData.split(":");
                    project_id=request.GET.get(u'project_id','')
                    team_id=request.GET.get(u'team_id','')
                    QueryText = []
                    for eachitem in UserText:
                        if len(eachitem) != 0 and  len(eachitem) != 1 and eachitem.strip() not in QueryText:
                            QueryText.append(eachitem.strip())
                    print QueryText
                    Section_Tag = 'Section'
                    Feature_Tag = 'Feature'
                    Custom_Tag = 'CustomTag'
                    Section_Path_Tag = 'section_id'
                    Feature_Path_Tag = 'feature_id'
                    Priority_Tag = 'Priority'
                    set_type='set'
                    tag_type='tag'
                    Status='Status'
                    query="select distinct dependency_name from dependency d, dependency_management dm where d.id=dm.dependency and dm.project_id='%s' and dm.team_id=%d"%(project_id,int(team_id))
                    Conn=GetConnection()
                    dependency=DB.GetData(Conn,query)
                    Conn.close()
                    wherequery=""
                    for each in dependency:
                        wherequery+=("'"+each.strip()+"'")
                        wherequery+=','
                    wherequery+=("'"+Section_Tag+"','"+Feature_Tag+"','"+Custom_Tag+"','"+Section_Path_Tag+"','"+Feature_Path_Tag+"','"+Priority_Tag+"','"+Status+"','"+set_type+"','"+tag_type+"'")
                    print wherequery
                    TestIDList = []
                    for eachitem in QueryText:
                        Conn=GetConnection()
                        TestID = DB.GetData(Conn, "Select property from test_case_tag where name = '%s' " % eachitem)
                        Conn.close()
                        for eachProp in TestID:
                            if eachProp == 'tcid':
                                TestIDList.append(eachitem)
                                break
                    TableData = []
                    if len(TestIDList) > 0:
                        for eachitem in TestIDList:
                            query="select distinct tct.tc_id from test_case_tag tct,test_cases tc where tct.tc_id=tc.tc_id and tct.tc_id='%s' group by tct.tc_id,tc.tc_name HAVING COUNT(CASE WHEN name = '%s' and property='Project' THEN 1 END) > 0 and COUNT(Case when name='%s' and property='Team' then 1 end)>0"%(eachitem,project_id,team_id)
                            Conn=GetConnection()
                            tabledata = DB.GetData(Conn,query)
                            Conn.close()
                            print tabledata
                            if tabledata:
                                TableData.append(tabledata[0])
                    else:
                        count = 1
                        for eachitem in QueryText:
                            if count == 1:
                                Query = "HAVING COUNT(CASE WHEN name = '%s' and property in (%s) THEN 1 END) > 0 "%(eachitem.strip(),wherequery)
                                count=count+1
                            else:
                                Query+="AND COUNT(CASE WHEN name = '%s' and property in (%s) THEN 1 END) > 0 "%(eachitem.strip(),wherequery)
                                count=count+1
                        Query = Query + " AND COUNT(CASE WHEN property = 'Project' and name = '" + project_id + "' THEN 1 END) > 0"
                        Query = Query + " AND COUNT(CASE WHEN property = 'Team' and name = '" + team_id + "' THEN 1 END) > 0"
                        query = "select distinct tct.tc_id from test_case_tag tct,test_cases tc where tct.tc_id=tc.tc_id  group by tct.tc_id,tc.tc_name " + Query
                        Conn=GetConnection()
                        TableData = DB.GetData(Conn, query)        
                        Conn.close()
                    final_data=[]    
                    for each in TableData:
                        final_data.append("'"+each+"'")
                    test_case_ids="("+",".join(final_data)+")"
                    test_case_query="select property,array_agg(distinct name) from test_case_tag tct, dependency d where d.dependency_name=tct.property and tc_id in "+test_case_ids+" group by property" 
                    Conn=GetConnection()
                    final_list=DB.GetData(Conn,test_case_query,False)
                    Conn.close()
                    result=simplejson.dumps(final_list)
                    return HttpResponse(result,mimetype='application/json')        
    except Exception,e:
            PassMessasge(sModuleInfo, e, 3)
def admin_page(request):
    return render_to_response('superAdmin.html',{},context_instance=RequestContext(request))
def superAdminFunction(request):
    return render_to_response('superAdminFunction.html',{},context_instance=RequestContext(request))
def GetProjectOwner(request):
    if request.method=='GET':
        if request.is_ajax():
            value=request.GET.get(u'term','')
            print value
            query="select distinct user_id,user_names,case when user_level='assigned_tester' then 'Tester' when user_level='manager' then 'Manager' end  from permitted_user_list pul, user_info ui where pul.user_names=ui.full_name and user_level not in('email','admin') and user_names iLike '%%%s%%'"%(value.strip())
            Conn=GetConnection()
            owner_list=DB.GetData(Conn,query,False)
            Conn.close()
            result=simplejson.dumps(owner_list)
            return HttpResponse(result,mimetype='application/json')
def Create_New_User(request):
    if request.method=='GET':
        if request.is_ajax():
            full_name=request.GET.get(u'full_name','').strip()
            user_name=request.GET.get(u'user_name','').strip()
            email=request.GET.get(u'email','').strip()
            password=request.GET.get(u'password','').strip()
            user_level=request.GET.get(u'user_level','').strip()
            query="select count(*) from user_info where full_name='%s'"%(full_name.strip())
            Conn=GetConnection()
            count=DB.GetData(Conn,query)
            Conn.close()
            if len(count)==1 and count[0]==0:
                #insert the new user
                Dict={
                    'username':user_name,
                    'password':password,
                    'full_name':full_name
                }
                Conn=GetConnection()
                result=DB.InsertNewRecordInToTable(Conn,"user_info",**Dict)
                Conn.close()
                if result:
                    Dict={
                        'user_names':full_name,
                        'user_level':user_level,
                        'email':email
                    }
                    Conn=GetConnection()
                    result=DB.InsertNewRecordInToTable(Conn,"permitted_user_list",**Dict)
                    Conn=GetConnection()
                    if result:
                        message=True
                else:
                    message=False
            result=simplejson.dumps(message)
            return HttpResponse(result,mimetype='application/json')    
def ListAllUser(request):
    if request.method=='GET':
        if request.is_ajax():
            query="select username,full_name,password,case when user_level='assigned_tester' then 'Tester' when user_level='admin' then 'Admin' when user_level='manager' then 'Manager' end,email from permitted_user_list pul, user_info ui where ui.full_name=pul.user_names  and user_level not in('email') order by user_level,username"
            Conn=GetConnection()
            user_list=DB.GetData(Conn,query,False)
            Conn.close()
            Column=['User Name','Full Name','Password','Designation','Email']
            result={
                'user_list':user_list,
                'column':Column
            }
            result=simplejson.dumps(result)
            return HttpResponse(result,mimetype='application/json')
        
def AssignTesters(request):
    query="select pul.user_id,user_names,case when user_level='assigned_tester' then 'Tester' end as Designation,default_project,default_team from permitted_user_list pul, default_choice ds, user_info ui where ui.full_name=pul.user_names and cast(ds.user_id as int)=pul.user_id and user_level in ('assigned_tester')"
    Conn=GetConnection()
    user_with_project=DB.GetData(Conn, query,False)
    Conn.close()
    query="select distinct pul.user_id,user_names, case when user_level='assigned_tester' then 'Tester' end as Designation from permitted_user_list pul, user_info ui where ui.full_name=pul.user_names and user_level in ('assigned_tester')"
    Conn=GetConnection()
    user_without_project=DB.GetData(Conn,query,False)
    Conn.close()
    final=[]
    name_found=[]
    for each in user_with_project:
        final.append(each)
        name_found.append(each[1])
    for each in user_without_project:
        if each[1] not in name_found:
            each=list(each)
            each.append('')
            each.append('')
            final.append(tuple(each))
            name_found.append(each[1])
    print final
    query="select distinct projects"
    column=['User Name', 'Designation', "Project ID", 'Team']
    return render_to_response('AssignTesters.html',{'column':column,'data':final},context_instance=RequestContext(request))
'''
You must use @csrf_protect before any 'post' handling views
You must also add {% csrf_token %} just after the <form> tag as in:

    <form method="POST" enctype="multipart/form-data" action='/Home/FileUploader/'>
    {% csrf_token %}
        <input type="file" name="uploaded_file">
        <button name="upload_file_button">Upload</button>
    </form>

Also, ensure that you have set the attribute: enctype="multipart/form-data" in the form
'''
@csrf_protect
def FileUploadTest(request):
    if request.method == 'POST':
        # The path for saving the file
        path = os.path.join(os.getcwd(), 'site_media', 'file_uploads')

        '''
        Create the FileUploader object by sending the following parameters:
        ~ 'request' - The current request object of the view
        ~ name_of_html_file_element: string - See the comment before the view if you don't understand what I'm talking about
        ~ path: string - The path to save the file to
        ~ (extensions): tuple - You can also supply extensions if you want (strongly recommended)
        '''
        file_uploader = FileUploader(request, 'uploaded_file', path_to_uploaded_files, ('png', 'jpg', 'jpeg', 'gif'))
        
        '''
        The FileUploader.upload_file() returns a boolean indicating wheather it was a success or not
        '''
        if file_uploader.upload_file():
            '''
            You can get the file name of the uploaded file once it has been uploaded successfully
            NOTE: Always call this method once you've confirmed that the file has been uploaded,
                  otherwise, it may not have any file name and you may get unexpected results
            '''
            file_name = file_uploader.file_name()
            return HttpResponseRedirect('/Home/FileUploadSuccess/True/')
        else:
            return HttpResponseRedirect('/Home/FileUploadSuccess/False/')

    c = RequestContext(request, {})
    return render_to_response('FileUploader.html', c)

def FileUploadTestOnSuccess(request, success):
    print success
    if success == 'True':
        c = {'success': 'Successful'}
    else:
        c = {'success': 'Unsuccessful'}
    return render_to_response('FileUploadSuccess.html', c)

@csrf_protect
def UploadProfilePicture(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        user_id = request.POST.get('user_id', '')
        path = os.path.join(path_to_uploaded_files, 'profile_pictures', username)
    
        if username == '':
            return HttpResponseRedirect('/Home/User/%s/unsuccessful/' % user_id)
        else:
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except OSError as e:
#                     if e.errno == errno.EEXIST:  # This case should never be approached
#                         print "Directory already exists"
#                     else:
                    print "Could not make directory: %s" % path
                    
                    return HttpResponseRedirect('/Home/User/%s/unsuccessful/' % user_id)
        
        file_uploader = FileUploader(request, 'uploaded_file', path)
        if file_uploader.upload_file():
            file_name = file_uploader.file_name()
            query = '''
            UPDATE user_info SET profile_picture_name='%s' WHERE username='%s'
            ''' % (file_name, username)
            
            Conn = GetConnection()
            cur = Conn.cursor()
            
            try:
                cur.execute(query)
                Conn.commit()
            except Exception as e:
                print "###########################"
                print "Transaction unsuccessful:", e
                print "###########################"
                return HttpResponseRedirect('/Home/User/%s/unsuccessful/' % user_id)
            finally:
                Conn.close()
            
        else:
            print "Could not upload file"        
            return HttpResponseRedirect('/Home/User/%s/unsuccessful/' % user_id)
        
        return HttpResponseRedirect('/Home/User/%s/successful/' % user_id)
    
    return HttpResponseRedirect('/Home/User/%s/' % user_id)

def ServeProfilePictureURL(request):
    if request.method == 'GET' and request.is_ajax():
        username = request.GET.get('username', '')
        full_name = request.GET.get('full_name', '')
        
        if username == '':
            return HttpResponse('https://sigil.cupcake.io/%s/.png?w=24' % full_name)
        
        query = '''
        SELECT profile_picture_name FROM user_info WHERE username='%s'
        ''' % username

        Conn = GetConnection()
        cur = Conn.cursor()
        
        try:
            cur.execute(query)
            data = cur.fetchone()
            file_name = data[0]
            if file_name == '' or (not file_name):
                return HttpResponse('https://sigil.cupcake.io/%s/.png?w=24' % full_name)
            
            # Path to profile pictures
            path = '/site_media/file_uploads/profile_pictures/%s/%s' % (username, file_name)
            
            return HttpResponse(path)
        
        except Exception as e:
            print e
        finally:
            Conn.close()
    
    return HttpResponse('')

def RemoveProfilePicture(request):
    username = request.GET.get('username', None)
#     print "USERNAME: %s" % username
    
    Conn = GetConnection()
    cur = Conn.cursor()
    
    query = '''
    UPDATE user_info SET profile_picture_name = NULL WHERE username='%s'
    ''' % (username)

    try:
        cur.execute(query)
        Conn.commit()
    except Exception as e:
        print e
        # Return a serever error in case of i/o failure
        return HttpResponse(status=500)
    finally:
        Conn.close()
    
    return HttpResponse('')