
# -*- coding: utf-8 -*-

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
##
from django.db import connection
#=======
#>>>>>>> parent of 5208765... Create Test Set added with create,update and delete function
#from django.shortcuts import render_to_response
#=======
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
#>>>>>>> 79295d8a9281fee2054c6e15061b281b41f17493

from django.template import Context
from django.template import RequestContext

from django.template.loader import get_template
from django.utils import simplejson
import json
from models import GetData, GetColumnNames, GetQueryData, GetConnection
import DataBaseUtilities as DB

from CommonUtil import TimeStamp
#import DjangoConstants
import TestCaseOperations
import re
import time
from TestCaseOperations import Cleanup_TestCase
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
# from pylab import * #http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib and http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
# import pylab


Conn = GetConnection()
#import logging

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





""" Main Pages functions """
#@login_required(login_url='/Home/Login/')
def HomePage(req):
    templ = get_template('HomePage.html')
    variables = Context(
                        {}
                        )
    output = templ.render(variables)
    return HttpResponse(output)

def RunTest(request):
    templ = get_template('RunTest.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

"""def Search(request):
    templ = get_template('SearchResults.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)"""
def make_array(get_list):
    refined_list=[]
    for each in get_list:
        temp=[]
        #print temp
        for eachitem in each:
            temp.append(eachitem)
        temp.insert(4,"status")
        temp=tuple(temp)
        refined_list.append(temp)
    print refined_list
    return refined_list        
def make_status_array(refined_list):
    pass_list=[]
    for each in refined_list:
        #print each
        run_id=each[0]
        temp=[]
        total_query="select count(*) from test_run where run_id='%s'" %run_id
        pass_query="select count(*) from test_case_results where run_id='%s' and status='Passed'" %run_id
        fail_query="select count(*) from test_case_results where run_id='%s' and status='Failed'" %run_id
        blocked_query="select count(*) from test_case_results where run_id='%s' and status='Blocked'"%run_id
        progress_query="select count(*) from test_case_results where run_id='%s' and status='In-Progress'" %run_id
        notrun_query="select count(*) from test_case_results where run_id='%s' and status='Submitted'" %run_id
        skipped_query="select count(*) from test_case_results where run_id='%s' and status='Skipped'" %run_id
        Conn=GetConnection()
        total=DB.GetData(Conn,total_query)
        passed=DB.GetData(Conn,pass_query)
        failed=DB.GetData(Conn,fail_query)
        blocked=DB.GetData(Conn,blocked_query)
        progress=DB.GetData(Conn,progress_query)
        submitted=DB.GetData(Conn,notrun_query)
        skipped=DB.GetData(Conn,skipped_query)
        pass_percent = str((passed[0]*100/total[0]))+'%'
        fail=str((failed[0]*100/total[0]))+'%'
        block=str((blocked[0]*100/total[0]))+'%'
        progress=str((progress[0]*100/total[0]))+'%'
        submitted=str((submitted[0]*100/total[0]))+'%'
        pending=str((skipped[0]*100/total[0]))+'%'
        temp.append(pass_percent)
        temp.append(fail)
        temp.append(block)
        temp.append(progress)
        temp.append(submitted)
        temp.append(pending)
        temp=tuple(temp)
        Conn.close()    
        pass_list.append(temp)
    print pass_list
    return pass_list
def ResultTableFetch(index):
    Conn=GetConnection()
    #interval="1"
    step=2
    limit="limit "+str(step)
    ########Code for selecting offset#########
    index=int(index)
    index=index-1
    index=index*step
    offset="offset "+str(index)
    offset=offset.strip()
    progress_query="(select ter.run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(now()-ter.teststarttime,'HH24:MI:SS') as Duration,tre.product_version from test_run_env tre, test_env_results ter where tre.run_id=ter.run_id and ter.status=tre.status and ter.status in ('Submitted','In-Progress') order by ter.teststarttime desc)"
    completed_query="(select ter.run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(ter.testendtime-ter.teststarttime,'HH24:MI:SS') as Duration,tre.product_version from test_run_env tre, test_env_results ter where tre.run_id=ter.run_id and ter.status=tre.status and ter.status not in ('Submitted','In-Progress') order by ter.teststarttime desc)"
    total_query=progress_query+' union all '+completed_query+ limit+" "+offset
    get_list=DB.GetData(Conn,total_query,False)
    get_list=set(get_list)
    total_run=make_array(get_list)
    print total_run
    """completed_query="select  ter.run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(ter.testendtime-ter.teststarttime,'HH24:MI:SS') as Duration,tre.product_version,tre.client from test_run_env tre, test_env_results ter where tre.run_id=ter.run_id and ter.status=tre.status and ter.status ='Complete' order by ter.teststarttime desc"
    complete_list=DB.GetData(Conn,completed_query,False)
    complete_run=make_array(set(complete_list))
    cancelled_query="select ter.run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(ter.testendtime-ter.teststarttime,'HH24:MI:SS') as Duration,tre.product_version,tre.client from test_run_env tre, test_env_results ter where tre.run_id=ter.run_id and ter.status=tre.status and ter.status ='Cancelled' order by ter.teststarttime desc"
    cancelled_list=DB.GetData(Conn,cancelled_query,False)
    cancelled_run=make_array(set(cancelled_list))
    interval="7"
    progress_query="(select ter.run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(now()-ter.teststarttime,'HH24:MI:SS') as Duration,tre.product_version,tre.client from test_run_env tre, test_env_results ter where tre.run_id=ter.run_id and ter.status=tre.status and ter.status ='In-Progress' and (cast(now() as timestamp without time zone)-ter.teststarttime)<interval '%s day' order by ter.teststarttime desc)"%interval
    progress_list=DB.GetData(Conn,progress_query,False)
    progress_run=make_array(set(progress_list))
    interval="7"
    submitted_query="select ter.run_id,tre.test_objective,tre.run_type,tre.assigned_tester,tre.status,to_char(now()-ter.teststarttime,'HH24:MI:SS') as Duration,tre.product_version,tre.client from test_run_env tre, test_env_results ter where tre.run_id=ter.run_id and ter.status=tre.status and ter.status ='Submitted' and (cast(now() as timestamp without time zone)-ter.teststarttime)<interval '%s day' order by ter.teststarttime desc"%interval
    submitted_list=DB.GetData(Conn,submitted_query,False)
    submitted_run=make_array(set(submitted_list))
    all_status=make_status_array(total_run)
    complete_status=make_status_array(complete_run)
    cancelled_status=make_status_array(cancelled_run)
    progress_status=make_status_array(progress_run)
    submitted_status=make_status_array(submitted_run)"""
    all_status=make_status_array(total_run)
    ###########Code for getting the total entry##############
    query="select count(*) from test_run_env tre,test_env_results ter where ter.run_id=tre.run_id"
    totalCount=DB.GetData(Conn,query)
    data={
          'total':total_run,
          'all_status':all_status,
          'totalCount':totalCount[0],
          'start':index+1,
          'end':index+step
          }
    return data
def zipdata(data_array,status_array):
    data=[]
    for each in zip(data_array,status_array):
        temp=[]
        temp.append(each[0])
        temp.append(each[1])
        temp=tuple(temp)
        data.append(temp)
    return data
def GetPageCount(request):
    totalPage=0
    if request.is_ajax():
        if request.method=='GET':
            Conn=GetConnection()
            query="select count(*) from test_run_env tre,test_env_results ter where tre.run_id=ter.run_id"
            totalEntry=DB.GetData(Conn,query)
            totalPage=totalEntry[0]/2
            if((totalEntry[0]%2)>0):
                totalPage+=1
    result=simplejson.dumps(totalPage)
    return HttpResponse(result,mimetype='application/json')
def ResultPage(request,Page_No):
    print Page_No
    Page_No=str(Page_No)
    index=Page_No.split('-')[1].strip()
    print index
    data=ResultTableFetch(index)
    print data
    Column=["Run ID","Objective","Run Type","Assigned Tester","Report","Status","Duration","Product Version"]
    template=get_template('Result.html')
    all_data=zipdata(data['total'], data['all_status'])
    """complete_data=zipdata(data['complete'],data['complete_status'])
    progress_data=zipdata(data['progress'],data['progress_status'])
    cancelled_data=zipdata(data['cancelled'],data['cancelled_status'])
    submitted_data=zipdata(data['submitted'],data['submitted_status'])"""
    Dict={
        'column':Column,
        'all':all_data,
        'start':data['start'],
        'end':data['end'],
        'total_count':data['totalCount']        
        }
    variables=Context(Dict)
    output=template.render(variables)
    return HttpResponse(output)

def Result_Table(request):
    Conn=GetConnection()
    results = []
    if request.method == "GET":
        tester = request.GET.get(u'tester', '')
        status = request.GET.get(u'status', '')
        version = request.GET.get(u'version', '')
        run_type = request.GET.get(u'run_type', '')
        

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Search2(request,Run_Id):
    #RunId = request.GET.get('ClickedRunId', '')
    if Run_Id != "":
        return RunId_TestCases(request,Run_Id)
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
    TC_Id = request.GET.get('TC_Id', '')
    if TC_Id != "":
        return ViewTestCase(TC_Id)
    else:
        templ = get_template('CreateTestCase.html')
        variables = Context({ })
        output = templ.render(variables)
        return HttpResponse(output)

def ManageTestCases(request):
    templ = get_template('ManageTestCases.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

@csrf_protect
def DeleteExisting(request):
    if request.method == 'GET':
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

def Edit(request):
    TC_Id = request.GET.get('TC_Id', '')
    if TC_Id != "":
        return ViewTestCase(TC_Id)
    else:
        templ = get_template('CreateTestCase.html')
        variables = Context({ })
        output = templ.render(variables)
        return HttpResponse(output)

def Performance(request):
    templ = get_template('Performance.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

#def Performance_Details_NewWindow(request):
#    templ = get_template('Performance_Details_NewWindow.html')
#    variables = Context( { } )
#    output = templ.render(variables)
#    return HttpResponse(output)

#def PerformanceGraph_Window(request):
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

    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        Environment = request.GET.get(u'Env', '')
        if Environment == "Mac":
            Section = "MacSection"
            Test_Run_Type = "Mac_test_run_type"
            Priority = "MacPriority"
            TCStatusName = "MacStatus"
            CustomTag = "MacCustomTag"
            CustomSet="set"
            Tag='tag'
        if Environment == "PC":
            Section = "Section"
            Test_Run_Type = "test_run_type"
            Priority = "Priority"
            TCStatusName = "Status"
            CustomTag = "CustomTag"
            CustomSet="set"
            Tag='tag'

        results = DB.GetData(Conn, "select distinct name,property from test_case_tag "
                                   "where name Ilike '%" + value + "%' "
                                     "and property in('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','"+CustomSet+"','"+Tag+"') "
                                     "and tc_id in (select tc_id from test_case_tag where name = '" + Environment + "' and property = 'machine_os' ) ",False
                                     )

        tcidresults = DB.GetData(Conn, "select distinct name || ' - ' || tc_name,'Test Case' from test_case_tag tct,test_cases tc "
                                   "where tct.tc_id = tc.tc_id and (tct.tc_id Ilike '%" + value + "%' or tc.tc_name Ilike '%" + value + "%')"
                                     "and property in('tcid') "
                                     "and tct.tc_id in (select tc_id from test_case_tag where name = '" + Environment + "' and property = 'machine_os' ) ",False
                                     )

        results = list(set(results + tcidresults))

        if len(results) > 0:
            results.append(("*Dev","Status"))

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
def AutoCompleteTestCasesSearchOtherPages(request):#===============Returns Available Test Case in other page without the platform =========================#
    if request.is_ajax():
        if request.method=='GET':
            final_results=[]
            value=request.GET.get(u'term','')
            platform=["PC","Mac"]
            for Environment in platform:
                if Environment == "Mac":
                    Section = "MacSection"
                    Test_Run_Type = "Mac_test_run_type"
                    Priority = "MacPriority"
                    TCStatusName = "MacStatus"
                    CustomTag = "MacCustomTag"

                if Environment == "PC":
                    Section = "Section"
                    Test_Run_Type = "test_run_type"
                    Priority = "Priority"
                    TCStatusName = "Status"
                    CustomTag = "CustomTag"
                    CustomSet="set"
                    Tag='tag'
                Client='client'
                tag_query="select distinct name,property from test_case_tag where name Ilike '%" + value + "%' and property in('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','"+CustomSet+"','"+Tag+"','"+Client+"') and tc_id in (select tc_id from test_case_tag where name = '" + Environment + "' and property = 'machine_os' ) "
                id_query="select distinct name || ' - ' || tc_name,'Test Case' from test_case_tag tct,test_cases tc where tct.tc_id = tc.tc_id and (tct.tc_id Ilike '%" + value + "%' or tc.tc_name Ilike '%" + value + "%') and property in('tcid') and tct.tc_id in (select tc_id from test_case_tag where name = '" + Environment + "' and property = 'machine_os' ) "            
                Conn=GetConnection()
                results=DB.GetData(Conn, tag_query, False)
                tcidresults=DB.GetData(Conn,id_query,False)
                results=list(set(results+tcidresults))
                for eachitem in results:
                    final_results.append(eachitem)
            final_results=list(set(final_results))
            results=final_results
            if len(results) > 0:
                results.append(("*Dev","Status"))

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteUsersSearch(request):  #==================Returns Abailable User Name in List as user Type on Run Test Page==============================

    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        #Ignore queries shorter than length 3
        #if len(value) > 1:

        #Deleting Unassigned Machine which is not updated since 3 mint
#        AvalMachineID = DB.GetData(Conn,"Select  id from test_run_env where status = 'Unassigned'",False)
#        for eachMachineID in AvalMachineID:
#            MachineTime = DB.GetData(Conn,"Select  last_updated_time from test_run_env where status = 'Unassigned' and id = %s" %eachMachineID,False)
#            MachineTime = str(MachineTime[0][0])
#            t = TimeDiff(MachineTime)
#            if t > 3:
#                DB.DeleteRecord(Conn, "test_run_env", id=str(eachMachineID[0]))
        #query="Select  DISTINCT tester_id,status from test_run_env where status = 'Unassigned' and tester_id Ilike '%" + value + "%'"
        """query= "(select distinct tre.tester_id,pul.user_level from test_run_env tre,permitted_user_list pul where tre.tester_id=pul.user_names and tre.status='Unassigned' and pul.user_level in('Manual','Automation')) union all (select distinct tre.tester_id,pul.user_level from test_run_env tre,permitted_user_list pul where tre.tester_id=pul.user_names and tre.status!='In-Progress' and pul.user_level in('Manual'))"
        results = DB.GetData(Conn, query,False)"""
        print value
        Env = request.GET.get(u'Env', '')
        if Env == u"PC": Environment = "Windows"
        if Env == u"Mac": Environment = "Darwin"
        Usable_Machine=[]
        query= "select distinct tre.tester_id,pul.user_level from test_run_env tre,permitted_user_list pul where tre.tester_id Ilike '%"+value+"%' and tre.tester_id=pul.user_names and tre.status='Unassigned' and pul.user_level in('Automation')" 
        Automation_Machine=DB.GetData(Conn,query,False)
        for each in Automation_Machine:
            Usable_Machine.append(each)
        query="select distinct user_names,user_level from permitted_user_list where user_level='Manual' and user_names Ilike '%"+value+"%'"
        print query
        Manual_Machine=DB.GetData(Conn,query,False)
        for each in Manual_Machine:
            query="select distinct status from test_run_env where tester_id='%s'" %each[0].strip()
            machine_status=DB.GetData(Conn,query)
            if len(machine_status)==0:
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
    #if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        #Ignore queries shorter than length 3
        #if len(value) > 1:
        results = DB.GetData(Conn, "Select  DISTINCT user_names from permitted_user_list where user_names Ilike '%" + value + "%' and user_level = 'email'")

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteTag(request):
    if request.is_ajax():
        if request.method=='GET':
            value=request.GET.get(u'term','')
            print value
            Conn=GetConnection()
            query="select value,type from config_values where value Ilike '%%%s%%' and type='tag'"%value
            tag_list=DB.GetData(Conn,query,False)
    json=simplejson.dumps(tag_list)
    return HttpResponse(json,mimetype='application/json')
 
def AutoCompleteTesterSearch(request):
    if request.is_ajax():
        if request.method=='GET':
            value=request.GET.get(u'term','')
            results=DB.GetData(Conn, "Select  DISTINCT user_names from permitted_user_list where user_names Ilike '%" + value + "%' and user_level = 'assigned_tester'")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def AutoCompleteTagSearch(request):
    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        Environment = request.GET.get(u'Env', '')
        if Environment == "Mac":
            Section = "MacSection"
            CustomTag = "MacCustomTag"

        if Environment == "PC":
            Section = "Section"
            CustomTag = "CustomTag"


        #results = DB.GetData(Conn, "select distinct name,property from test_case_tag where name Ilike '%" + value + "%' "
        #                           + "and property in ('" + CustomTag + "') order by name",False)

        query="select distinct value,type from config_values where type='tag' order by value"
        mastertags = DB.GetData(Conn,query,False)

        #results = list(set(results + mastertags))

    json = simplejson.dumps(mastertags)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteTestStepSearch(request):
    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')

        results = DB.GetData(Conn, "select stepname,data_required,steptype,description,step_editable from test_steps_list where stepname Ilike '%" + value + "%' order by stepname", False)

    json = simplejson.dumps(results)
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
                CustomSet="set"
                Tag='tag'
            if Environment == "PC":
                Section = "Section"
                Test_Run_Type = "test_run_type"
                Priority = "Priority"
                TCStatusName = "Status"
                CustomTag = "CustomTag"
                CustomSet="set"
                Tag='tag'
            QueryText = []
            for eachitem in UserText:
                if len(eachitem) != 0 and  len(eachitem) != 1:
                    QueryText.append(eachitem.strip())

    if "*Dev" in QueryText:
        QueryText.remove("*Dev")
        propertyValue = "Dev"


    #In case if user search test cases using test case ids    
    TestIDList = []
    for eachitem in QueryText:
        TestID = DB.GetData(Conn, "Select property from test_case_tag where name = '%s' " % eachitem)
        for eachProp in TestID:
            if eachProp == 'tcid':
                TestIDList.append(eachitem)
                break


    RefinedData=[]
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
                Query = "HAVING COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','"+CustomSet+"','"+Tag+"') THEN 1 END) > 0 "
                count = count + 1
            elif count >= 2:
                Query = Query + "AND COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','"+ Test_Run_Type + "','" + Priority + "','"+CustomSet+"','"+Tag+"') THEN 1 END) > 0 "
        Query = Query + " AND COUNT(CASE WHEN name = '%s' and property = '%s' THEN 1 END) > 0 " % (TCStatusName, propertyValue)
        Query = Query + " AND COUNT(CASE WHEN property = 'machine_os' and name = '" + Environment + "' THEN 1 END) > 0"
        query="select distinct tct.tc_id,tc.tc_name from test_case_tag tct,test_cases tc where tct.tc_id=tc.tc_id group by tct.tc_id,tc.tc_name "+Query
        TableData = DB.GetData(Conn, "select distinct tct.tc_id,tc.tc_name from test_case_tag tct, test_cases tc "
                        "where tct.tc_id = tc.tc_id group by tct.tc_id,tc.tc_name " + Query, False)
    TempTableData=[]
    Check_TestCase(TableData, RefinedData)
    for each in RefinedData:
        temp=[]
        for eachitem in each:
            temp.append(eachitem)
        query="select name from test_case_tag where tc_id='%s' and property='machine_os'"%each[0]
        platform=DB.GetData(Conn,query)
        temp.append(platform[0])
        temp=tuple(temp)
        TempTableData.append(temp)
    RefinedData=TempTableData
    Heading = ['Test Case ID', 'Test Case Name','Test Case Type','Platform']

    #results = {"Section":Section, "TestType":Test_Run_Type,"Priority":Priority}         
    results = {'Heading':Heading, 'TableData':RefinedData}

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


def TestCase_TestSteps(request): #==================Returns Test Steps When User Click on Test Case on Test Run Page===============================
    Conn = GetConnection()
    results = {}
    if request.is_ajax():
         if request.method == 'GET':

            #If User Click on Test Case ID 
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

def TestCase_TestSteps_SearchPage(request): #==================Returns Test Steps When User Click on Test Case on Test Search Page===============================
    Conn = GetConnection()
    results = {}
    if request.is_ajax():
         if request.method == 'GET':

            #If User Click on Test Case ID 
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
            result=[]
            if RunID != '':
                Result = DB.GetData(Conn, "Select stepname from test_steps tst,test_steps_list tsl where tst.step_id = tsl.step_id and tc_id  = '%s' order by teststepsequence" % RunID)
            for each in Result:
                query="select '"+each+"-'||steptype from test_steps_list where stepname='"+each+"'"
                Result_type=DB.GetData(Conn, query)
                result.append(Result_type[0])
    results = {'Result':result}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
def GetRunIDStatus(RunId):
    run_status=""
    query="select status from test_case_results where run_id='%s'" %RunId
    Conn=GetConnection()
    status_list=DB.GetData(Conn, query)
    for each in status_list:
        if each!='Submitted':
            run_status='Not Submitted'
            break
    if run_status=='Not Submitted':
        if 'In-Progress' in status_list:
            run_status='In-Progress'
        elif 'Submitted' in status_list:
            run_status='In-Progress'
        else:
            run_status='Complete'
    else:
        run_status='Submitted'
    return run_status
def Modify(AllTestCases1):
        AllTestCases=[]
        AllTestCases2=[]
        Check_TestCase(AllTestCases1, AllTestCases2)
        for each in zip(AllTestCases1,AllTestCases2):
            temp=[]
            for eachitem in each[0]:
                temp.append(eachitem)
            temp.insert(2,each[1][2])
            temp=tuple(temp)
            AllTestCases.append(temp)
        return AllTestCases
def ConvertTime(total_time):
    seconds=total_time%60
    minuates=total_time/60
    minuate=minuates%60
    hour=minuates/60
    if seconds<10:
        seconds=('0'+str(seconds))
    else:
        seconds=str(seconds)
    if minuate<10:
        minuate=('0'+str(minuate))
    else:
        minuate=str(minuate)
    if hour<10:
        hour=('0'+str(hour))
    else:
        hour=str(hour)
    timeformat=hour+':'+minuate+':'+seconds
    timeformat=timeformat.strip()
    return timeformat
def AddEstimatedTime(TestCaseList):
    ModifiedTestCaseList=[]
    for each in TestCaseList:
        print each[0]
        query="select count(*) from test_steps where tc_id='%s'" %each[0]
        Conn=GetConnection()
        step_count=DB.GetData(Conn,query)
        total_time=0
        for eachstep in range(1,step_count[0]+1):
            step_id=each[0]+'_s'+str(eachstep)
            time_query="select description from master_data where field='estimated' and value='time' and id='%s'"%step_id
            step_time=DB.GetData(Conn,time_query)
            total_time+=int(step_time[0])
        format_time=ConvertTime(total_time)
        temp=[]
        for eachitem in each:
            temp.append(eachitem)
        temp.insert(5,format_time)
        temp=tuple(temp)
        ModifiedTestCaseList.append(temp)
    return ModifiedTestCaseList
def RunId_TestCases(request,RunId): #==================Returns Test Cases When User Click on Run ID On Test Result Page===============================
    Conn=GetConnection()
    RunId=RunId.strip()
    print RunId
    Env_Details_Col = ["Run ID","Mahchine","Tester","Estd. Time","Status","Product","Machine OS","Client","Machine IP","Objective","MileStone","Email"]
    run_id_status=GetRunIDStatus(RunId)
    query="Select DISTINCT run_id,tester_id,assigned_tester,'"+run_id_status+"',product_version,os_name||' '||os_version||' - '||os_bit as machine_os,client,machine_ip,test_objective,test_milestone from test_run_env Where run_id = '%s'" % RunId
    Env_Details_Data=DB.GetData(Conn, query, False)
    #Code for the total estimated time for the RUNID
    totalRunIDTime=0
    query="select tc_id from test_run where run_id='%s'"%RunId
    test_case_list=DB.GetData(Conn,query)
    for each in test_case_list:
        #Get the step_count
        query="select count(*) from test_steps where tc_id='%s'"%each
        step_count=DB.GetData(Conn,query)
        for eachstep in range(1,step_count[0]+1):
            temp_id=each+'_s'+str(eachstep)
            query="select description from master_data where field='estimated' and value='time' and id='%s'"%temp_id
            step_time=DB.GetData(Conn,query)
            totalRunIDTime+=int(step_time[0])
    formatTime=ConvertTime(totalRunIDTime) 
    ################################################
    #code for fetching email notification
    email_query= "select email_notification from test_run_env where run_id='%s'"%RunId
    email_list=DB.GetData(Conn,email_query,False)
    print email_list
    emails=email_list[0][0]
    email_list=emails.split(",")
    email_list=list(set(email_list))
    print email_list
    email_receiver=[]
    for each in email_list:
        if each!="":
            query="select user_names from permitted_user_list where user_level='email' and email='%s'"%each
            name=DB.GetData(Conn,query)
            email_receiver.append(name[0])
    print email_receiver
    email_name=",".join(email_receiver)
    temp=[]
    for each in Env_Details_Data[0]:
        temp.append(each)
    temp.insert(3,formatTime)
    temp.append(email_name)
    temp=tuple(temp)
    Env_Details_Data=[]
    Env_Details_Data.append(temp)
    print Env_Details_Data
    #####################################
    AllTestCases1 = DB.GetData(Conn, "(select "
                                            "tc.tc_id as MKSId, "
                                            "tc.tc_name, "
                                            "tr.status, "
                                            "to_char(tr.duration,'HH24:MI:SS'), "
                                            "tr.failreason, "
                                            "tr.logid, "
                                            "tc.tc_id "
                                            "from test_case_results tr, test_cases tc, test_case_tag tct "
                                            "where tr.run_id = '%s' and "
                                            "tr.tc_id = tc.tc_id and tc.tc_id = tct.tc_id and tct.property = 'MKS' ORDER BY tr.id) "
                                            "union all "
                                            "(select tct.name as MKSId,tc.tc_name,'Pending','','','',tc.tc_id "
                                            "from test_run tr,test_cases tc, test_case_tag tct "
                                            "where tr.tc_id = tc.tc_id and tc.tc_id = tct.tc_id and tct.property = 'MKS' and tr.run_id = '%s' and "
                                            "tr.tc_id not in (select tc_id from test_case_results where run_id = '%s') )" % (RunId, RunId, RunId) , False)
    Col = ['ID', 'Title','Type', 'Status', 'Duration', 'Estd. Time','Comment', 'Log', 'Automation ID']
    AllTestCases=Modify(AllTestCases1)
    AllTestCases=AddEstimatedTime(AllTestCases)
    Pass_TestCases1 = DB.GetData(Conn, "select "
                                            "tc.tc_id as mksid, "
                                            "tc.tc_name, "
                                            "tr.status, "
                                            "to_char(tr.duration,'HH24:MI:SS'), "
                                            "tr.failreason, "
                                            "tr.logid, "
                                            "tc.tc_id "
                                            "from test_case_results tr, test_cases tc, test_case_tag tct "
                                             "where tr.run_id = '%s' and tr.status = 'Passed' and "
                                            "tr.tc_id = tc.tc_id and tc.tc_id = tct.tc_id and tct.property = 'MKS' ORDER BY tr.id" % (RunId), False)


    Pass_TestCases=Modify(Pass_TestCases1)
    Pass_TestCases=AddEstimatedTime(Pass_TestCases)
    Fail_TestCases1= DB.GetData(Conn, "select "
                                            "tc.tc_id as mksid, "
                                            "tc.tc_name, "
                                            "tr.status, "
                                            "to_char(tr.duration,'HH24:MI:SS'), "
                                            "tr.failreason, "
                                            "tr.logid, "
                                            "tc.tc_id "
                                            "from test_case_results tr, test_cases tc, test_case_tag tct "
                                            "where tr.run_id = '%s' and tr.status in('Failed','Blocked') and "
                                            "tr.tc_id = tc.tc_id and tc.tc_id = tct.tc_id and tct.property = 'MKS' ORDER BY tr.id" % RunId, False)
    Fail_TestCases=Modify(Fail_TestCases1)
    Fail_TestCases=AddEstimatedTime(Fail_TestCases)
    Submitted_TestCases1=DB.GetData(Conn,"select "
                                            "tc.tc_id as mksid, "
                                            "tc.tc_name, "
                                            "tr.status, "
                                            "to_char(tr.duration,'HH24:MI:SS'), "
                                            "tr.failreason, "
                                            "tr.logid, "
                                            "tc.tc_id "
                                            "from test_case_results tr, test_cases tc, test_case_tag tct "
                                            "where tr.run_id = '%s' and tr.status ='Submitted' and "
                                            "tr.tc_id = tc.tc_id and tc.tc_id = tct.tc_id and tct.property = 'MKS' ORDER BY tr.id" % RunId, False)
    Submitted_TestCases=Modify(Submitted_TestCases1)
    Submitted_TestCases=AddEstimatedTime(Submitted_TestCases)
    failsteps = DB.GetData(Conn, "select DISTINCT tsl.stepname from test_case_results tr, test_step_results tsr, test_steps_list tsl, test_cases tc "

                          "where tr.run_id = '%s' and tr.status = 'Failed' and tr.run_id = tsr.run_id and tr.tc_id = tsr.tc_id "

                           "and tsr.status = 'Failed' and tsr.teststep_id = tsl.step_id and tr.tc_id = tc.tc_id" % RunId, False
                    )

    #Adding Test Case Count with Fails Steps Name
    FailsStepsWithCount = []
    for eachstep in failsteps:
        failstep = list(eachstep)[0]
        FailStep_TestCases = DB.GetData(Conn, "select tc.tc_name from test_case_results tr, test_step_results tsr, test_steps_list tsl, test_cases tc "
                                                "where tr.run_id = '%s' and tr.status = 'Failed' and tr.run_id = tsr.run_id "
                                                "and tr.tc_id = tsr.tc_id and tsr.status in ('Failed') and tsr.teststep_id = tsl.step_id "
                                                "and tr.tc_id = tc.tc_id and tsl.stepname = '%s' " % (RunId, failstep)
                                            )
        Count = len(FailStep_TestCases)
        L = []
        L.append("%s (%s)" % (failstep, Count))
        FailsStepsWithCount.append(L)

    failsteps_Col = ["Step Name"]
    ReRunColumn=['Test Case ID','Test Case Name','Type','Status']
    query="select tc.tc_id,tc.tc_name,tcr.status from test_cases tc,test_case_results tcr where tc.tc_id=tcr.tc_id and tcr.run_id='%s'"%RunId
    ReRunList=DB.GetData(Conn,query,False)
    ReRun=Modify(ReRunList)
    results={
             'Env_Details_Col':Env_Details_Col,
             'Env_Details_Data':Env_Details_Data,
             'Env_length':len(Env_Details_Data),
             'Column':Col,
             'AllTestCases':AllTestCases,
             'All_length':len(AllTestCases),
             'Pass_length':len(Pass_TestCases),
             'Pass':Pass_TestCases,
             'Fail_length':len(Fail_TestCases),
             'Fail':Fail_TestCases,
             'Submitted':Submitted_TestCases,
             'submitted_length':len(Submitted_TestCases),
             'failsteps':FailsStepsWithCount,
             'failsteps_col':failsteps_Col,
             'fail_length':len(FailsStepsWithCount),
             'rerun_col':ReRunColumn,
             'rerun_list':ReRun
             }
    return render_to_response('RunID_Detail.html',results)

def TestCase_Detail_Table(request): #==================Returns Test Steps and Details Table When User Click on Test Case Name On Test Result Page========
    Conn = GetConnection()
    results = {}
    TC_ID = ""
    TestCase_Detail_Data = []
    TestCase_Detail_Col = []
    if request.is_ajax():
        if request.method == 'GET':
            #If User Click on Fail Step 
            RunId = request.GET.get('RunID', '')
            TestCaseName = request.GET.get('TestCaseName', '')
            TestCaseName = str(TestCaseName.strip())
            TC_ID = TestCaseName

            #TC_NameID = DB.GetData(Conn,"select  tc.tc_name, tr.tc_id from test_run tr, test_cases tc where tr.tc_id = tc.tc_id and tr.run_id = '%s'" %RunId,False)

            #for eachitem in TC_NameID:
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
                query="select tsl.stepname, tsr.status,to_char(tsr.duration,'HH24:MI:SS') as duration,tsr.memory_consumed as MemoryUsage from test_step_results tsr,test_steps_list tsl where tsr.teststep_id=tsl.step_id and tsr.run_id='%s' and tsr.tc_id='%s' order by tsr.id"%(RunId,TC_ID)
                TestCase_Detail_Data=DB.GetData(Conn, query, False)
                TestCase_Detail_Col = ['Test Step Name', 'Status', 'Duration', 'Memory Usage']

    results = {
               'TestCase_Detail_Data':TestCase_Detail_Data,
               'TestCase_Detail_Col' :TestCase_Detail_Col,
               }
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def TestStep_Detail_Table(request): #==================Returns Test Step Details Table When User Click on Test Step Name On Test Result Page=======
    Conn = GetConnection()
    results = {}
    TestStep_Details=""
    TestStep_Col=""
    TestStep_Description_Col=""
    TestStep_Description=""
    data_col=""
    data_val=""
    data_val_comp=""
    dataset=""
    data_required=""
    if request.is_ajax():
        if request.method == 'GET':

            #If User Click on Fail Step 
            RunId = request.GET.get('RunID', '')
            TestCaseName = request.GET.get('TestCaseName', '')
            TestStepName = request.GET.get('TestStepName', '')
            TestStepSeqId = request.GET.get('TestStepSeqID', '')

            if RunId != '' and TestCaseName != '' and TestStepName != '' and TestStepSeqId != '':
                RunId = str(RunId.strip())
                TestCaseName = str(TestCaseName.strip())
                TestStepName = str(TestStepName.strip())
                TestStepSeqId = int(TestStepSeqId.strip())
                StepSequence=str(TestStepSeqId)
                query="select tc_id from test_cases where tc_name='"+TestCaseName+"'"
                TestCaseId = DB.GetData(Conn,query)
                TestCaseId = str(TestCaseId[0])
                TestStep_Details=[]
                StepSeqId = DB.GetData(Conn, "Select tst.teststepsequence "
                                            " from test_steps tst,test_steps_list tsl "
                                            " where tc_id = '%s' and "
                                            "tst.step_id = tsl.step_id and "
                                            "tsl.stepname='%s'" % (TestCaseId,TestStepName)
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
                TestStep_Description_Col=['StepSequence','Description','Purpose']
                TestStep_Description=[]
                TestStep_Description.append(StepSequence)
                query="select description,data_required from test_steps_list where stepname='"+TestStepName+"'"
                step_desc=DB.GetData(Conn,query,False)
                TestStep_Description.append(step_desc[0][0])
                query="select tc_id from test_cases where tc_name='"+TestCaseName+"'"
                tc_id=DB.GetData(Conn,query,False)
                test_case_step_length=DB.GetData(Conn,"select count(*) from test_steps where tc_id='%s'" %(tc_id[0][0]),False)
                datasetid=""
                if int(StepSequence)<test_case_step_length[0][0]+int(1):
                    datasetid=tc_id[0][0]+"_s"+StepSequence
                else:
                    query="select teststepsequence from test_steps where tc_id='%s'" %tc_id[0][0]
                    test_sequence=DB.GetData(Conn,query)
                    stepsequence=1
                    for each in test_sequence:
                        if StepSeqId[0]==each:
                            break
                        else:
                            stepsequence+=1
                    datasetid=tc_id[0][0]+"_s"+str(stepsequence)
                query="select description from master_data where id='"+datasetid+"' and field='step' and value='description'"
                purpose=DB.GetData(Conn,query,False)
                TestStep_Description.append(purpose[0][0])
                TestStep_Description=tuple(TestStep_Description)
                TestStep_Description=[TestStep_Description]
                data_required=""
                if step_desc[0][1]==True:
                    data_required="yes"
                else:
                    data_required="no"
                data_col=["DataSetId","Data"]
                data_val=[]
                data_val_comp=[]
                dataset=[]
                if data_required=="yes":
                    datasetid+='_d'
                    query="select distinct id from master_data where id Ilike '"+datasetid+"%'"
                    dataset_temp=DB.GetData(Conn,query)
                    for each in dataset_temp:
                        if len(each)==14:
                            dataset.append(each)
                    count=1
                    for each in dataset:
                        data_val.append((count,""))
                        count+=1
                        print str(count)+" - "+each
                        query="select field,value from master_data where id Ilike'"+each+"%' and field!=''"
                        data_set_val=DB.GetData(Conn,query,False)
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


def FailStep_TestCases(request): #==================Returns Test Cases When User Click on Fail Step On Test Result Page===============================
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':

            #If User Click on Fail Step 
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
                FailStep_TestCases1=Modify(FailStep_TestCases)
                FailStep_TC_Col = ['Test Case ID', 'Failed Test Case','Test Case Type','Status', 'Duration', 'Fail Reason', 'Test Log', 'Autmation ID']
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

            if Environment == "PC":
                Section = "Section"
                Test_Run_Type = "test_run_type"
                Priority = "Priority"
                Env_Dependency = "Dependency"
                TCStatusName = "Status"
                CustomTag = "CustomTag"
                CustomSet='set'
                Tag='tag'

            QueryText = []
            for eachitem in UserText:
                if len(eachitem) != 0 and  len(eachitem) != 1:
                    QueryText.append(eachitem.strip())

    if "*Dev" in QueryText:
        QueryText.remove("*Dev")
        propertyValue = "Dev"

#    Response = ""
#    Result = 'Pass'
#    DepandList = []

    #==========Depandency Checking=============

    #Making list of test case id ( when user selects only test case)
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

        DepandencyNamesValues = DB.GetData(Conn, "select distinct t1.property, t2.property from test_case_tag t1, test_case_tag t2 "
                                 "where t1.tc_id = t2.tc_id and t1.property = t2.name and t1.name = '" + Env_Dependency + "' and (%s)" % query, False)
    elif len(QueryText) > 0:
        count = 1
        for eachitem in QueryText:
            if count == 1:
                Query = "HAVING COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','"+CustomSet+"','"+Tag+"') THEN 1 END) > 0 "
                count = count + 1
            elif count >= 2:
                Query = Query + "AND COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','"+CustomSet+"','"+Tag+"') THEN 1 END) > 0 "
        Query = Query + "AND COUNT(CASE WHEN name = '" + TCStatusName + "' and property = '" + propertyValue + "' THEN 1 END) > 0 "
        Query = Query + "AND COUNT(CASE WHEN property = 'machine_os' and name = '" + Environment + "' THEN 1 END) > 0 "
        DepandencyNamesValues = DB.GetData(Conn, "Select distinct t1. property,t2. property from test_case_tag t1, test_case_tag t2 "
                                        "where t1.tc_id = t2.tc_id and t1.property = t2.name and t1.name = '" + Env_Dependency + "' and t1.tc_id in ("
                                        "select distinct tct.tc_id from test_case_tag tct, test_cases tc "
                                        "where tct.tc_id = tc.tc_id "
                                        "group by tct.tc_id,tc.tc_name %s ) " % Query, False
                                  )
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


def Table_Data_UserList(request): #==================Returns Available user list When there is no error in depandency ==============================
    Conn = GetConnection()
    results = {}
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'UserListRequest', '')
            Env = request.GET.get(u'Env', '')
            if Env == u"PC": Environment = "Windows"
            if Env == u"Mac": Environment = "Darwin"
            Machine_List=[]
            Usable_Machine=[]
            if UserData == "True":
                query= "select distinct tre.tester_id,pul.user_level from test_run_env tre,permitted_user_list pul where tre.tester_id=pul.user_names and tre.status='Unassigned' and pul.user_level in('Automation')" 
                Automation_Machine=DB.GetData(Conn,query,False)
                for each in Automation_Machine:
                    Usable_Machine.append(each)
                query="select distinct user_names,user_level from permitted_user_list where user_level='Manual'"
                Manual_Machine=DB.GetData(Conn,query,False)
                for each in Manual_Machine:
                    query="select distinct status from test_run_env where tester_id='%s'" %each[0].strip()
                    machine_status=DB.GetData(Conn,query)
                    if len(machine_status)==0:
                        Usable_Machine.append(each)
                    else:
                        if 'In-Progress' in machine_status or 'Submitted' in machine_status:
                            continue
                        else:
                            Usable_Machine.append(each)
                for each in Usable_Machine:
                    query="Select  distinct tester_id,os_name ||' '||os_version||' - '||os_bit as machine_os,client,last_updated_time,machine_ip from test_run_env where tester_id='"+each[0]+"' and os_name ='" + Environment + "'"
                    tabledata = DB.GetData(Conn, query, False)
                    if len(tabledata)==0:
                        continue
                    else:
                        temp=[]
                        for eachitem in tabledata[0]:
                            temp.append(eachitem)
                        temp.insert(1, each[1])
                        Machine_List.append(temp)
                Heading = ["Machine Name", "Machine Type","Machine OS", "Client", "Last Updated Time", "Machine IP"]
                #Heading.reverse()
    results = {'Heading':Heading, 'TableData':Machine_List}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def Run_Test(request): #==================Returns True/Error Message  When User Click on Run button On Test Run Page==============================
    Conn = GetConnection()
    results = {}
    Eid = []
    QueryText = []
    propertyValue = "Ready"
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get('RunTestQuery', '')
            UserData = str(UserData.replace(u'\xa0', u''))

            EmailIds = request.GET.get('EmailIds', '')
            EmailIds = str(EmailIds.replace(u'\xa0', u''))
            
            TesterIds = request.GET.get('TesterIds', '')
            TesterIds = str(TesterIds.replace(u'\xa0', u''))
            
            DependencyText = request.GET.get('DependencyText', '')
            DependencyText = str(DependencyText.replace(u'\xa0', u''))

            """TestDataType = request.GET.get('TestDataType', '')
            TestDataType = str(TestDataType.replace(u'\xa0', u''))"""

            TestObjective = request.GET.get('TestObjective', '')
            TestObjective = str(TestObjective.replace(u'\xa0', u''))
            TestMileStone = request.GET.get('TestMileStone', '')
            TestMileStone = str(TestMileStone.replace(u'\xa0', u''))
            is_rerun=request.GET.get(u'ReRun','')
            previous_run=request.GET.get('RunID','')    
            Environment = request.GET.get('Env', '')
            if Environment == "Mac":
                Section = "MacSection"
                Test_Run_Type = "Mac_test_run_type"
                Priority = "MacPriority"
                TCStatusName = "MacStatus"
                CustomTag = "MacCustomTag"

            if Environment == "PC":
                Section = "Section"
                Test_Run_Type = "test_run_type"
                Priority = "Priority"
                TCStatusName = "Status"
                CustomTag = "CustomTag"
                CustomSet='set'
                Tag='tag'

            UserText = UserData.split(":");
            EmailIds = EmailIds.split(":")
            DependencyText = DependencyText.split(":")
            TesterIds=TesterIds.split(":")
            Emails = []
            for eachitem in EmailIds :
                if eachitem != "":
                    Eid = DB.GetData(Conn, "Select email from permitted_user_list where user_names = '%s'" % str(eachitem))
                if len(Eid) > 0:
                    Emails.append(Eid[0])


            stEmailIds = ','.join(Emails)
            Testers=[]
            for each in TesterIds:
                if each !="" and each !=":":
                    Testers.append(each)
            if is_rerun=='rerun':
                Testers.remove(" ")
                if len(Testers)==1:
                    Testers=Testers[0]
                else:
                    Testers=','.join(Testers)
            else:
                Testers=','.join(Testers)
            for eachitem in UserText:
                if len(eachitem) != 0 and  len(eachitem) != 1:
                    QueryText.append(str(eachitem.strip()))

    if "*Dev" in QueryText:
        QueryText.remove("*Dev")
        propertyValue = "Dev"

    TesterId = QueryText.pop() # pop function will remove last item of the list (userid) and will assign to Testerid
    #Add the manual Test Machine to the test_run_env table
    if is_rerun=='rerun':
        sWhereQuery={'tester_id':TesterId,'status':'Unassigned'}
        print DB.DeleteRecord(Conn, "test_run_env",**sWhereQuery)
    TesterId=TesterId.strip()
    runid = TimeStamp("string")
    #Changing for the ReRun
    if is_rerun=='rerun':
        query="select * from test_run_env where tester_id='%s' and run_id='%s'"%(TesterId,previous_run)
        Machine_Detail=DB.GetData(Conn, query,False)
        print Machine_Detail[0]
        each=Machine_Detail[0]
        status="Unassigned"
        updateTime=TimeStamp("string")
        print status
        print updateTime
        machine_os=(each[15]+" "+each[14]+" - "+each[16]).strip()
        print machine_os
        client=each[7].strip()
        print client
        ip=each[11]
        Dict={'run_id':runid,'tester_id':TesterId,'status':status,'machine_ip':ip,'last_updated_time':updateTime,'machine_os':machine_os,'client':client,'os_name':each[15],'os_version':each[14],'os_bit':each[16],'test_objective':TestObjective}
        #sWhereQuery="where tester_id='%s'" %TesterId
        print DB.InsertNewRecordInToTable(Conn,"test_run_env",**Dict)
    query="select user_level from permitted_user_list where user_names='%s'" %TesterId
    Machine_Status=DB.GetData(Conn,query,False)
    if Machine_Status[0][0]=='Manual' and is_rerun!='rerun':
        query="select * from test_run_env where tester_id='%s'"%TesterId
        Machine_Detail=DB.GetData(Conn, query,False)
        print Machine_Detail[0]
        each=Machine_Detail[0]
        status="Unassigned"
        updateTime=TimeStamp("string")
        print status
        print updateTime
        machine_os=(each[15]+" "+each[14]+" - "+each[16]).strip()
        print machine_os
        client=each[7].strip()
        print client
        ip=each[11]
        Dict={'run_id':runid,'status':status,'machine_ip':ip,'last_updated_time':updateTime,'machine_os':machine_os,'client':client,'os_name':each[15],'os_version':each[14],'os_bit':each[16],'test_objective':TestObjective}
        sWhereQuery="where tester_id='%s' and run_id='%s'" %(TesterId,runid)
        print DB.UpdateRecordInTable(Conn,"test_run_env",sWhereQuery,**Dict)    
    #Creating Runid and assigning test cases to it in "testrun" table
    TestIDList = []
    for eachitem in QueryText:
        TestID = DB.GetData(Conn, "Select property from test_case_tag where name = '%s' " % eachitem)
        for eachProp in TestID:
            if eachProp == 'tcid':
                TestIDList.append(eachitem)
                break



    if len(TestIDList) > 0:
        TestCasesIDs = TestIDList

    elif len(QueryText) > 0:
        count = 1
        for eachitem in QueryText:
            if count == 1:
                #Query = "HAVING COUNT(CASE WHEN name = '%s' THEN 1 END) > 0 " %eachitem
                Query = "HAVING COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','"+CustomSet+"','"+Tag+"') THEN 1 END) > 0 "
                count = count + 1
            elif count >= 2:
                #Query = Query + "AND COUNT(CASE WHEN name = '%s' THEN 1 END) > 0 " %eachitem
                Query = Query + "AND COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "','"+CustomSet+"','"+Tag+"') THEN 1 END) > 0 "
        Query = Query + " AND COUNT(CASE WHEN name = '%s' and property = '%s' THEN 1 END) > 0" % (TCStatusName, propertyValue)
        Query = Query + " AND COUNT(CASE WHEN property = 'machine_os' and name = '" + Environment + "' THEN 1 END) > 0"
        TestCasesIDs = DB.GetData(Conn, "select distinct tct.tc_id from test_case_tag tct, test_cases tc "
                "where tct.tc_id = tc.tc_id group by tct.tc_id,tc.tc_name " + Query)
    #The Run ID and test case may be given a status of submitted here.    
    for eachitem in TestCasesIDs:
        Dict = {'run_id':runid, 'tc_id':str(eachitem)}
        Result = DB.InsertNewRecordInToTable(Conn, "test_run", **Dict)

    #Finding Client info from TestRenEnv for selected machine
    #if is_rerun=='rerun':
     #   query="select client from test_run_env where tester_id='%s' and run_id='%s'"%(TesterId,previous_run)
    #else:
    query="Select client from test_run_env Where  tester_id = '%s' and status = 'Unassigned' " % TesterId
    ClientInfo = DB.GetData(Conn, query)
    ClientInfo = ClientInfo[0].split(",")
    #Adding tag values to "testrunevn" table columns
    if is_rerun=='rerun':
        tempdependency=[]
        for each in DependencyText:
            temp=each.split('(')
            tempdependency.append(temp[0].strip())
        DependencyText=tempdependency
    for each in DependencyText:
        QueryText.append(each.strip())
    QueryText.remove("")

    TestSetName = ""
    for eachitem in QueryText:
        TagName = DB.GetData(Conn, "Select DISTINCT property from test_case_tag where name = '%s' and property in ('%s','%s')" % (eachitem, Section, CustomTag))
        if len(TagName) > 0:
            TagName = TagName[0]
        else:
            TagName = DB.GetData(Conn, "Select DISTINCT property from test_case_tag where name = '%s'" % (eachitem))
            if len(TagName) > 0:
                TagName = TagName[0]


        #Checking if QuestyText has Client name. if yes geting client name and version from ClientInfo
        for iclient in ClientInfo:
            print "eachitem:"+eachitem
            print "iclient:"+iclient
            if eachitem in iclient:
                eachitem = iclient
                print "eachitem:"+eachitem

        if TagName == Section or TagName == CustomTag or TagName == Priority or TagName == 'tcid' or TagName==CustomSet or TagName==Tag:
            query = "Where  tester_id = '%s' and status = 'Unassigned' " % TesterId
            if is_rerun=='rerun':
                query="where tester_id='%s' and run_id='%s' and status='Unassigned'" %(TesterId,runid)
            
            TestSetName = TestSetName + " " + eachitem
            TestSetName = TestSetName.strip()
            Dict = {'run_id':runid, 'rundescription': TestSetName}
        else:
            query = "Where  tester_id = '%s' and status = 'Unassigned' " % TesterId
            if is_rerun=='rerun':
                query="where tester_id='%s' and run_id='%s' and status='Unassigned'" %(TesterId,runid)
    
            TestSetName = TestSetName + " " + eachitem
            TestSetName = TestSetName.strip()
            Dict = {'run_id':runid, 'rundescription': TestSetName , '%s' % (TagName) : '%s' % (eachitem)}
        Result = DB.UpdateRecordInTable(Conn, "test_run_env", query , **Dict)
    AddInfo(runid)
    if is_rerun=='rerun':
        query="where tester_id='%s' and run_id='%s' and status='Unassigned'" %(TesterId,runid)
        productversion_query="select product_version from test_run_env where run_id='%s'" %previous_run
        product_version=DB.GetData(Conn,productversion_query)
        Dict={'product_version':product_version[0].strip()}
        print DB.UpdateRecordInTable(Conn,"test_run_env",query,**Dict)
    #####Code for adding MileStone
    if is_rerun=='rerun':
        milestone_query="select test_milestone from test_run_env where run_id='%s'"%previous_run
        milestone_list=DB.GetData(Conn,milestone_query)
        TestMileStone=milestone_list[0]
    Result = DB.UpdateRecordInTable(Conn, "test_run_env", query,
                                     email_notification=stEmailIds,
                                     assigned_tester=Testers,
                                     test_objective=TestObjective,
                                     Status='Submitted',
                                     run_type='Manual',
                                     test_milestone=TestMileStone
                                     )
    print DB.UpdateRecordInTable(Conn, "test_run_env", query,
                                     email_notification=stEmailIds,
                                     assigned_tester=Testers,
                                     test_objective=TestObjective,
                                     Status='Submitted',
                                     run_type='Manual',
                                     test_milestone=TestMileStone
                                     )
    #NJ-Insert into run env results to display submitted runs
    now = DB.GetData(Conn, "SELECT CURRENT_TIMESTAMP;", False)
    sTestSetStartTime = str(now[0][0])
    print sTestSetStartTime

    Dict = {'run_id':runid, 'tester_id':str(TesterId), 'status': 'Submitted', 'rundescription':TestObjective, 'teststarttime':sTestSetStartTime}
    EnvResults = DB.InsertNewRecordInToTable(Conn, "test_env_results", **Dict)
#    Result = DB.UpdateRecordInTable(Conn, "test_run_env", query, test_objective = TestObjective  )
#    Result = DB.UpdateRecordInTable(Conn, "test_run_env", query , Status = 'Submitted' ) 
    
    results = {'Result': Result,'runid':runid}

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
def AddInfo(run_id):
    conn=GetConnection()
    query="select tc_id from test_run where run_id='"+run_id+"'"
    TestCaseList=DB.GetData(conn, query)
    for eachcase in TestCaseList:
        print eachcase
        print DB.InsertNewRecordInToTable(conn, "test_case_results",run_id=run_id,tc_id=eachcase,status="Submitted")
        TestStepsList = DB.GetData(conn, "Select ts.step_id,stepname,teststepsequence,tsl.driver,ts.test_step_type From Test_Steps ts,test_steps_list tsl where TC_ID = '%s' and ts.step_id = tsl.step_id Order By teststepsequence" % eachcase, False)
        for eachstep in TestStepsList:
            print eachcase +"step_sequence:"+str(eachstep[2])+" - "+str(eachstep[0])
            Dict={'run_id':run_id,'tc_id':eachcase,'teststep_id':eachstep[0],'status':"Submitted"}
            print DB.InsertNewRecordInToTable(conn, "test_step_results",**Dict)
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
            #Checking if the status of the user is not In-Progress or Submitted
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

                #Adding fail test cases in test_sets table to make TestSet
                for eachTC in ReRunTestCases:
                    CreateFailedTestSet = DB.InsertNewRecordInToTable(Conn, "test_run",

                                                              run_id="%s" % NewRunID,
                                                              tc_id=str(eachTC),
                                                              )

                #Deleting entry of "Unassinged" if there is one
                try:
                    DeleteUnassignedRecord = DB.DeleteRecord(Conn, "test_run_env",

                                                            tester_id=TesterID,
                                                            status="Unassigned"
                                                            )
                except:
                    pass

                #Creating test run in testrunenv table for fail test cases of selected run id    
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
        #sum divided by number of elements
        sum = 0
        for num in rawlist:
            sum += num
        return round (float(sum) / len(rawlist))

    def median(rawlist):
        #first sort the list
        rawlist.sort()
        #if list has even number of elements, then get the average of middle two elements
        if len(rawlist) % 2 == 0:
            #have to take avg of middle two
            mid = len(rawlist) / 2
            return (rawlist[mid - 1] + rawlist[mid]) / 2.0
        #if the list has odd number of elements, then get the middle element
        else:
            #find the middle (remembering that lists start at 0)
            mid = len(rawlist) / 2
            return rawlist[mid]

    def CleanRawData(rawlist):
        #return a list with good data removing data which are further away from median
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
            #removing Performance from 'Media Performance' for eg
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



            #Finding All Duration Testing Cases Ran on Clicked Environment
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


                        #Finding All Duration Testing Cases Ran on Clicked Environment
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

            #Creating Folder for Graph if request is for Graph
            if  GraphRequest == "Graph":

                    FL.DelFolderWithExpTime("C:\Python27\WorkSpace\DjangoFramework10\site_media", "Graph", 1)
                    GraphFolderName = "Graph_%s" % str(time.time())
                    FL.CreateEmptyFolder("C:\Python27\WorkSpace\DjangoFramework10\site_media", GraphFolderName)
                    #FL.CreateEmptyFolder("W:\site_media", GraphFolderName)


            #Duration Table Data    
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

                        #Duration = (str(list(Duration[0])[0]))
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



                #Memory Table Data
            for eachTC_ID in Memory_TC_ID:

                MemoryTempTable.append(eachTC_ID)
                TC_Name = DB.GetData(Conn, "select tc_name from test_cases where tc_id = '%s'" % (eachTC_ID))
                MemoryTempTable.append(TC_Name[0])

                for eachBun in Bun:

                    Memory = DB.GetData(Conn, "Select memory_delta from performance_results where tc_id = '%s' and product_version = '%s'" % (eachTC_ID, eachBun), False)
                    #MemoryCount = DB.GetData(Conn,"Select count( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    #MemoryMax = DB.GetData(Conn,"Select MAX( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    #MemoryMin = DB.GetData(Conn,"Select MIN( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
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


            #CPU Table Data
            for eachTC_ID in CPU_TC_ID:
                CPUTempTable.append(eachTC_ID)
                TC_Name = DB.GetData(Conn, "select tc_name from test_cases where tc_id = '%s'" % (eachTC_ID))
                CPUTempTable.append(TC_Name[0])

                for eachBun in Bun:
                    CPU = DB.GetData(Conn, "Select cpu_avg from performance_results where tc_id = '%s' and product_version = '%s'" % (eachTC_ID, eachBun), False)
                    #MemoryCount = DB.GetData(Conn,"Select count( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    #MemoryMax = DB.GetData(Conn,"Select MAX( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
                    #MemoryMin = DB.GetData(Conn,"Select MIN( memory_peak ) from performance_results where tc_id = '%s' and product_version = '%s'" %(eachTC_ID,eachBun),False )
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

        #To make lenght of tables one, if they have nothing  
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
        #BundleNumber = BundleNumber.replace("B","")
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
        #floor(extract('epoch' from pr.cpu_peaktime))::integer"



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
        #Ignore queries shorter than length 3
        #if len(value) > 1:
        #results = DB.GetData(Conn,"Select DISTINCT name from test_case_tag where name != 'Dependency' and name Ilike '%" + value + "%'")
        #results = DB.GetData(Conn, "Select DISTINCT tc_id from test_cases")
        results = DB.GetData(Conn, "Select  DISTINCT tc_id,tc_name,'Test Case' from test_cases where tc_id Ilike '%" + value + "%'",False)


    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')



def Selected_TestCaseID_Analaysis(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Selected_TC_Analysis', '')


    TestCase_Analysis_Result = DB.GetData(Conn, "select run_id,tc.tc_name,status,failreason,logid from test_case_results tcr,test_cases tc where tcr.tc_id = '%s' and tcr.tc_id = tc.tc_id" % UserData, False)
    Col = ["Run ID", "Test Case Name", "Status", "Fail Reason", "Product logid"]

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
    #find latest bundles for PC
    PCBundles = DB.GetData(Conn, "select split_part(split_part(product_version, E',',1),E':',2) from test_run_env where status in ('Complete') and product_version ilike '%Version:%'  and machine_os ilike 'Windows%' order by id desc" , False)
    BundleList = []
    BundleListFinal = []
    for eachbundle in PCBundles:
        BundleList.append(eachbundle[0])

    for eachbundle in BundleList:
        if eachbundle not in BundleListFinal:
            BundleListFinal.append(eachbundle)

    #for each bundle, get passed, failed, total and add it to the results table
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

def TestCase_ParseData(temp, Steps_Name_List,Step_Description_List,Step_Expected,Step_Verification_Point,Step_Time_List):
    print Step_Expected
    Steps_Data_List = []
    # s = step # d = data # t = tuple # a = address
    d = 0
    index = -1
    for name in zip(Steps_Name_List,Step_Description_List,Step_Expected,Step_Verification_Point,Step_Time_List):
        #init step array
        Steps_Data_List.insert(d, (name[0].strip(), [],name[1].strip(),name[2].strip(),name[3].strip(),name[4].strip()))

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
            #init data array
            Steps_Data_List[d][1].insert(t, [])

            if '#' in data:
                editList = []
                et = 0
                for dataEach in data.split("#"):
                    editList.insert(et, [])
                    #contact parse
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
                                #init tuple array
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
                #contact parse
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
                            #init tuple array
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
    @param Dependency_List: List of dependent clients
    @param Priority_List: P1, P2, P3
    @param Steps_Data_List: [(Step1,Data1),(Step2,Data2),(Step3,Data3)]. Step1 = stepname, Data1 = [(Field,value)] format depends on the step
    """

    def returnResult(string):
        json = simplejson.dumps(string)
        return HttpResponse(json, mimetype='application/json')

    try:
        Conn = GetConnection()
        error = ''
        if request.is_ajax() and request.method == 'GET':
            Platform = request.GET.get(u'Platform', '')
            Manual_TC_Id = request.GET.get(u'Manual_TC_Id', '').split(',')
            TC_Name = request.GET.get(u'TC_Name', '')
            TC_Creator = request.GET.get(u'TC_Creator', '')
            TC_Type = request.GET.get(u'TC_Type', '').split('|')
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
            Step_Description_List = request.GET.get(u'Steps_Description_List','')
            print Step_Description_List
            Step_Description_List=Step_Description_List.split('|')
            Step_Expected_Result=request.GET.get(u'Steps_Expected_List','').split('|')
            Step_Verification_Point=request.GET.get(u'Steps_Verify_List','').split('|')
            Step_Time_List=request.GET.get(u'Steps_Time_List','').split('|')
            Steps_Data_List = TestCase_ParseData(temp, Steps_Name_List,Step_Description_List,Step_Expected_Result,Step_Verification_Point,Step_Time_List)

        #1
        ##########Data Validation: Check if all required input fields have data
        test_case_validation_result = TestCaseOperations.TestCase_DataValidation(Platform, TC_Name, TC_Type, Priority, Tag_List, Dependency_List, Steps_Data_List, Section_Path)
        if test_case_validation_result != "Pass":
            return returnResult(test_case_validation_result)

        #2
        ##########Test Case Id & Name
        if 'create' in Is_Edit:
            #Automation Test Case Id - automatically picked up from db
            tmp_id = DB.GetData(Conn, "select nextval('testcase_testcaseid_seq')")
            TC_Id = TestCaseOperations.Generate_TCId(Section_Path, tmp_id[0])

            #Check if test case id is used before
            tmp_id = DB.GetData(Conn, "select tc_id from test_cases where tc_id = '%s'" % TC_Id)
            if len(tmp_id) > 0:
                #Implement finding a new id
                #just fail it for now
                print "Error. Test case id already used"
                error = "TEST CASE CREATION Failed. Test case id already used:%s***********************" % (TC_Name)
                return returnResult(error)
            #Insert Test Case
            test_cases_result = TestCaseOperations.Insert_TestCaseName(Conn, TC_Id, TC_Name, TC_Creator)
            if test_cases_result != 'Pass':
                TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
                return returnResult(test_cases_result)
        else:
            TC_Id = Is_Edit
        ######

        #3
        ##########Test Case DataSet
        #tcdatasetid should be unique. And creating a test case, make sure there is no tcdatasetid existing for that test case
        #Test case dataset format of TC_Idds eg if TC_Id is 100, dataset id will be 100ds
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
            print "Error. Test case Dataset id error"
            TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
            return returnResult("Unable to create dataset for this test case")

        #Insert Test Case DataSet
        test_case_dataset_result = TestCaseOperations.Insert_TestCaseDataSet(Conn, Test_Case_DataSet_Id, TC_Id)
        if test_case_dataset_result != 'Pass':
            TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
            return returnResult(test_case_dataset_result)

        #4
        ##########Test Steps
        #Make sure test steps do no exist for the current TC_Id
        tmp_id = DB.GetData(Conn, "select step_id from test_steps where tc_id = '%s'" % TC_Id)
        if len(tmp_id) > 0:
            #We should be able to clean up test steps for this TC_Id
            #for now, just error out
            print "Error. Test case steps already existing error"
            TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
            return returnResult("Test Case steps already exists for this test case")

        #Insert Test Case Steps & Data
        test_case_steps_result = TestCaseOperations.Insert_TestSteps_StepsData(Conn, TC_Id, Test_Case_DataSet_Id, Steps_Data_List)

        if test_case_steps_result != 'Pass':
            TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
            return returnResult(test_case_steps_result)

        #5
        ##########Test Case Tags
        #Enter tags for the test case
        #Insert Test Case Tags
        test_case_tags_result = TestCaseOperations.Insert_TestCase_Tags(Conn, TC_Id, Platform, Manual_TC_Id, TC_Type, Tag_List, Dependency_List, Priority, Associated_Bugs_List, Status, Section_Path, Requirement_ID_List)

        if test_case_steps_result == "Pass":
            return returnResult(TC_Id)
        else:
            TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
            return returnResult(test_case_tags_result)

    except Exception, e:
        print "Exception:", e
        TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
        return "Critical"

def ViewTestCase(TC_Id):
    def returnResult(string):
        json = simplejson.dumps(string)
        return HttpResponse(json, mimetype='application/json')

    try:
        Conn = GetConnection()
        err_msg = ''

        #Search for TC_ID
        tmp_id = DB.GetData(Conn, "select tc_id from test_cases where tc_id = '%s'" % TC_Id)
        if len(tmp_id) > 0:
            #TestCaseOperations.LogMessage(sModuleInfo,"TEST CASE id is found:%s"%(TC_Id),4)

            #find all the details about test case
            test_case_details = DB.GetData(Conn, "select tc_name,tc_createdby from test_cases where tc_id = '%s'" % TC_Id, False)
            TC_Name = test_case_details[0][0]
            TC_Creator = test_case_details[0][1]

            #Test Case dataset details
            test_case_dataset_details = DB.GetData(Conn, "select tcdatasetid,data_type from test_case_datasets where tc_id = '%s'" % TC_Id, False)
            if len(test_case_dataset_details) > 0:
                Test_Case_DataSet_Id = test_case_dataset_details[0][0]
            else:
                Test_Case_DataSet_Id = ''

            #find all the tag details about test case
            test_case_tag_details = DB.GetData(Conn, "select name,property from test_case_tag where tc_id = '%s'" % TC_Id, False)
            Manual_TC_Id_List = [x[0] for x in test_case_tag_details if x[1] == 'MKS']
            Manual_TC_Id = ','.join(Manual_TC_Id_List)

            Platform = [x[0] for x in test_case_tag_details if x[1] == 'machine_os']
            TC_Type = [x[0] for x in test_case_tag_details if x[1] == 'test_run_type' or x[1] == 'Mac_test_run_type']
            Tag_List = [x[0] for x in test_case_tag_details if x[1] == 'CustomTag' or x[1] == 'MacCustomTag']
            Dependency_List = [x[1] for x in test_case_tag_details if x[0] == 'Dependency' or x[0] == 'MacDependency']
            Priority_List = [x[0] for x in test_case_tag_details if x[1] == 'Priority' or x[1] == 'MacPriority']
            Priority = ''.join(Priority_List)
            Associated_Bugs_List = [x[0] for x in test_case_tag_details if x[1] == 'JiraId']
            Requirement_ID_List = [x[0] for x in test_case_tag_details if x[1] == 'PRDId']
            Status_List = [x[1] for x in test_case_tag_details if x[0] == 'Status' or x[0] == 'MacStatus']
            Status = ''.join(Status_List)
            Section_Id = [x[0] for x in test_case_tag_details if x[1] == 'section_id' or x[1] == 'mac_section_id']
            if len(Section_Id) > 0:
                Section_Path = DB.GetData(Conn, "select section_path from product_sections where section_id = '%d'" % int(Section_Id[0]), False)
                if len(Section_Path) > 0:
                    Section_Path = Section_Path[0][0]
                else:
                    Section_Path = ''
            else:
                Section_Path = ''

            
            #find all steps and data for the test case
            Steps_Data_List = []
            test_case_step_details = DB.GetData(Conn, "select ts.step_id,stepname,teststepsequence,data_required,steptype from test_steps ts, test_steps_list tsl where ts.step_id = tsl.step_id and tc_id = '%s' order by teststepsequence" % TC_Id, False)
            Step_Iteration=1
            for each_test_step in test_case_step_details:
                print "step %s - %s" %(Step_Iteration,each_test_step[1])
                Step_Id = each_test_step[0]
                Step_Name = each_test_step[1]
                Step_Seq = each_test_step[2]
                Step_Type=each_test_step[4]
                Step_Data = []
                query="select description from master_data where id Ilike '%s_s" % (TC_Id)
                query+="%s"% (str(Step_Iteration))
                query+="%' and field='step' and value='description'"
                #query="select description from master_data where id Ilike '%s_s%s%' and field='step' and value='description'" %(TC_Id,str(Step_Iteration))
                Step_Description=DB.GetData(Conn,query,False)
                print Step_Description[0][0]
                #select expected Result from the master data
                query="select description from master_data where id Ilike '%s_s" % (TC_Id)
                query+="%s"% (str(Step_Iteration))
                query+="%' and field='expected' and value='result'"
                Step_Expected=DB.GetData(Conn,query,False)
                #select verification point from master_data
                query="select description from master_data where id Ilike '%s_s" % (TC_Id)
                query+="%s"% (str(Step_Iteration))
                query+="%' and field='verification' and value='point'"
                Step_Verified=DB.GetData(Conn,query,False)
                query="select description from test_steps_list where stepname='%s'"%(Step_Name.strip())
                Step_General_Description=DB.GetData(Conn,query,False)
                query="select description from master_data where id Ilike '%s_s" % (TC_Id)
                query+="%s"% (str(Step_Iteration))
                query+="%' and field='estimated' and value='time'"
                Step_Time=DB.GetData(Conn,query,False)
                Step_Iteration=Step_Iteration+1
                #is data required for this step
                if each_test_step[3]:
                    #Is this a verify step
                    if 'Verify' not in Step_Name:
                        container_data_id_details = DB.GetData(Conn, "select ctd.curname,ctd.newname from test_steps_data tsd, container_type_data ctd "
                         "where tsd.testdatasetid = ctd.dataid and tcdatasetid = '%s' and teststepseq = %s" % (Test_Case_DataSet_Id, Step_Seq), False)

                        #check if its a edit step
                        if 'Edit' in Step_Name:
                            for each_data_id in container_data_id_details:
                                From_Data = TestCaseOperations.Get_PIM_Data_By_Id(Conn, each_data_id[0])
                                To_Data = TestCaseOperations.Get_PIM_Data_By_Id(Conn, each_data_id[1])
                                Step_Data.append((From_Data, To_Data))
                        else:
                            #curname contains the data id
                            for each_data_id in container_data_id_details:
                                From_Data = TestCaseOperations.Get_PIM_Data_By_Id(Conn, each_data_id[0])
                                Step_Data.append(From_Data)

                    else:
                        exp_container_data_id_details = DB.GetData(Conn, "select ctd.curname from expected_datasets ed, expected_container ec, container_type_data ctd "
                         "where ed.expectedrefid = ec.exprefid and ec.container_name = ctd.dataid and ed.datasetid = '%s' and ed.stepsseq = %s" % (Test_Case_DataSet_Id, Step_Seq), False)

                        for each_data_id in exp_container_data_id_details:
                            From_Data = TestCaseOperations.Get_PIM_Data_By_Id(Conn, each_data_id[0])
                            Step_Data.append(From_Data)

                #append step name and data to send it back
                Steps_Data_List.append((Step_Name, Step_Data,Step_Type,Step_Description[0][0],Step_Expected[0][0],Step_Verified[0][0],Step_General_Description[0][0],Step_Time[0][0]))

            #return values
            results = {'TC_Id':TC_Id, 'TC_Name': TC_Name, 'TC_Creator': TC_Creator, 'Manual_TC_Id': Manual_TC_Id, 'Platform': Platform, 'TC Type': TC_Type, 'Tags List': Tag_List, 'Priority': Priority, 'Dependency List': Dependency_List, 'Associated Bugs': Associated_Bugs_List, 'Status': Status, 'Steps and Data':Steps_Data_List, 'Section_Path':Section_Path, 'Requirement Ids': Requirement_ID_List}

            json = simplejson.dumps(results)
            return HttpResponse(json, mimetype='application/json')

        else:
            err_msg = "TEST CASE id is not found:%s" % (TC_Id)
            return returnResult(err_msg)

    except Exception, e:
        err_msg = "TEST CASE search failed due to exception: %s" % (TC_Id)
        return returnResult(err_msg)

#def EditTestCase(TC_Id,Platform,Manual_TC_Id, TC_Name, TC_Creator, TC_Type,Tag_List,Dependency_List,Priority,Steps_Data_List,Associated_Bugs_List,Status):
def EditTestCase(request):
    def returnResult(string):
        json = simplejson.dumps(string)
        return HttpResponse(json, mimetype='application/json')

    try:
        Conn = GetConnection()
        err_msg = ''
        if request.is_ajax() and request.method == 'GET':
            TC_Id = request.GET.get(u'TC_Id', '')
            Platform = request.GET.get(u'Platform', '')
            Manual_TC_Id = request.GET.get(u'Manual_TC_Id', '')
            TC_Name = request.GET.get(u'TC_Name', '')
            TC_Creator = request.GET.get(u'TC_Creator', '')
            TC_Type = request.GET.get(u'TC_Type', '')
            Tag_List = request.GET.get(u'Tag_List', '').split('|')
            Dependency_List = request.GET.get(u'Dependency_List', '').split('|')
            Priority = request.GET.get(u'Priority', '')
            temp = request.GET.get(u'Steps_Data_List', '').split('|')
            Steps_Name_List = request.GET.get(u'Steps_Name_List', '').split('|')
            Associated_Bugs_List = request.GET.get(u'Associated_Bugs_List', '')
            Requirement_ID_List = request.GET.get(u'Requirement_ID_List', '')
            Status = request.GET.get(u'Status', '')
            Step_Description_List = request.GET.get(u'Steps_Description_List','')
            print Step_Description_List
            Step_Description_List=Step_Description_List.split('|')
            Step_Expected_Result=request.GET.get(u'Steps_Expected_List','').split('|')
            Step_Verification_Point=request.GET.get(u'Steps_Verify_List','').split('|')
            Steps_Time_List=request.GET.get(u'Steps_Time_List','').split('|')
            Steps_Data_List = TestCase_ParseData(temp, Steps_Name_List,Step_Description_List,Step_Expected_Result,Step_Verification_Point,Steps_Time_List)
            Section_Path = request.GET.get(u'Section_Path', '')
        #LogMessage(sModuleInfo,"TEST CASE Edit START:%s"%(TC_Name),4)

        #0
        ##########Data Validation: Check if all required input fields have data
        test_case_validation_result = TestCaseOperations.TestCase_DataValidation(Platform, TC_Name, TC_Type, Priority, Tag_List, Dependency_List, Steps_Data_List, Section_Path)
        if test_case_validation_result != "Pass":
            return returnResult(test_case_validation_result)

        #1
        #Find if this is a new format test case created from web page or a manually created test case in backend
        DeleteTestCaseData = False
        if '-' in TC_Id:
            #this is a new format test case
            DeleteTestCaseData = True
            New_TC_Id = TC_Id
            TestCaseOperations.Cleanup_TestCase(Conn, TC_Id, True, False, TC_Id)
            #if we are recreating a new format test case, then update details in test_case table
            test_cases_result = TestCaseOperations.Update_TestCaseDetails(Conn, New_TC_Id, TC_Name, TC_Creator)
        else:
            #this is an old format test case
            tmp_id = DB.GetData(Conn, "select nextval('testcase_testcaseid_seq')")
            New_TC_Id = TestCaseOperations.Generate_TCId(Section_Path, tmp_id[0])
            test_cases_result = TestCaseOperations.Insert_TestCaseName(Conn, New_TC_Id, TC_Name, TC_Creator)
            TestCaseOperations.Cleanup_TestCase(Conn, TC_Id, True, True, New_TC_Id)


        #3
        #Recreate the new test case

        if test_cases_result != 'Pass':
            TestCaseOperations.Cleanup_TestCase(Conn, New_TC_Id)
            return test_cases_result

        GET_values = request.GET.copy()
        GET_values['Is_Edit'] = New_TC_Id
        request.GET = GET_values
        return Create_Submit_New_TestCase(request)

    except Exception, e:
        print "Exception:", e
        TestCaseOperations.Cleanup_TestCase(Conn, TC_Id)
        return "Critical"

def Documentation(request):
    templ = get_template('Documentation.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def Get_Sections(request):  #==================Returns Abailable User Name in List as user Type on Run Test Page==============================

    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        section = request.GET.get(u'section', '')
        if section == '':
            results = DB.GetData(Conn, "select distinct subpath(section_path,0,1) from product_sections", False)
            levelnumber = 0
        else:
            levelnumber = section.count('.') + 1
            results = DB.GetData(Conn, "select distinct subltree(section_path,%d,%d) FROM product_sections WHERE section_path ~ '*.%s.*' and nlevel(section_path) > %d" % (levelnumber, levelnumber + 1, section, levelnumber), False)

    results.insert(0, (str(levelnumber),))
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_SubSections(request):  #==================Returns Abailable User Name in List as user Type on Run Test Page==============================

    Conn = GetConnection()
    results = []
    #if request.is_ajax():
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

def Get_Browsers(request):
    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        browser = request.GET.get(u'browser', '')
        if browser == '':
            results = DB.GetData(Conn, "select value from config_values where type = 'Browser'", False)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Users(request):
    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        username = request.GET.get(u'user', '').strip()
        password = request.GET.get(u'pwd', '').strip()
        #if username=='':
        results = DB.GetData(Conn, "select full_name from user_info where username='"+username+"' and password='"+password+"'", False)

    if len(results)>0:
        message = results[0]
    else:
        message = "User Not Found!"

    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')

def Get_RunTypes(request):
    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        runtype = request.GET.get(u'run_type', '')
        if runtype == '':
            results = DB.GetData(Conn, "select distinct run_type from test_run_env", False)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Testers(request):
    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        tester = request.GET.get(u'tester', '')
        if tester == '':
            results = DB.GetData(Conn, "select distinct assigned_tester from test_run_env", False)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Status(request):
    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        status = request.GET.get(u'status', '')
        if status == '':
            results = DB.GetData(Conn, "select distinct status from test_run_env", False)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Get_Versions(request):
    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        ver = request.GET.get(u'term', '')
        if ver == '':
            versions = DB.GetData(Conn, "select distinct product_version from test_run_env order by product_version", False)
        else:
            versions = DB.GetData(Conn, "select distinct product_version from test_run_env where product_version='"+ver+"' order by product_version", False)
        
        flag1 = 0
        flag2 = 0
        flag3 = 0
        for i in versions:
            if i[0] == '':
                flag1 = 1
            elif i[0] == ' ':
                flag3 = 3
            elif i[0] == None:
                flag2 = 1     #2
            else:
                results.append(i)
        if flag1==1:
            Nil = ['Nil']
            results.append(Nil)
        if flag2==2:
            Nil = ['Nil(None)']
            results.append(Nil)
        if flag3==3:
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
            os_query = "select distinct machine_os from test_run_env where machine_os ~ '"+OSName+".*' and product_version = '"+version+"' order by machine_os"
            browser_query = "select distinct client from test_run_env where machine_os ~ '"+OSName+".*' and product_version = '"+version+"' order by client"
            section_query = "select distinct subpath(section_path,0,1) from product_sections"
            sect_sub_q = "select product_sections.section_path from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path"
            OS_client_query = "select distinct machine_os,client from test_run_env where machine_os ~ '"+OSName+".*' and product_version = '"+version+"' order by machine_os"
            OS = DB.GetData(Conn, os_query, False)
            browsers = DB.GetData(Conn, browser_query, False)
            env_details = DB.GetData(Conn, OS_client_query, False)
            sections = DB.GetData(Conn, sect_sub_q, False)
            #env_details.append("Total")
            #Total = ["Total"]
            #sections.append(Total)
            
    """for each in OS:
        for item in browsers:
            temp = []
            temp.append(each[0])
            temp.append(item[0])
            env_details.append(tuple(temp))"""
    for i in env_details:
        #CountPerSection(sections,sel_cases,ReportTable)
        Data = []
        for s in sections:
            temp = []
            temp.append(s[0])
            #selected_cases_q = "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os like '"+i[0]+"%' and tre.product_version='"+i[1]+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and tcr.status = 'Passed'"
            passed_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '"+i[0]+"' and tre.client = '"+i[1]+"' and tre.product_version = '"+version+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and tcr.status = 'Passed'" , False)
            pass_count = len(passed_cases)
            temp.append(pass_count)
            failed_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '"+i[0]+"' and tre.client = '"+i[1]+"' and tre.product_version = '"+version+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and tcr.status = 'Failed'" , False)
            same = 0
            for j in failed_cases:
                for k in passed_cases:
                    if j[0]==k[0]:
                        same = same+1
            fail_count = len(failed_cases)
            temp.append(fail_count - same)
            blocked_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '"+i[0]+"' and tre.client = '"+i[1]+"' and tre.product_version = '"+version+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and tcr.status = 'Blocked'" , False)
            same1 = 0
            for j in blocked_cases:
                for k in passed_cases:
                    if j[0]==k[0]:
                        same1 = same1 + 1
                for h in failed_cases:
                    if j[0]==h[0]:
                        same1 = same1 + 1                        
            block_count = len(blocked_cases)
            temp.append(block_count - same1)
            notrun_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '"+i[0]+"' and tre.client = '"+i[1]+"' and tre.product_version = '"+version+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and (tcr.status = 'In-Progress' or tcr.status = 'Skipped' or tcr.status = 'Submitted')" , False)
            notrun_count = len(notrun_cases)
            temp.append(notrun_count)
            defected_cases = DB.GetData(Conn, "select distinct tcr.tc_id from test_case_results tcr,test_run_env tre, test_case_tag tct, product_sections ps where tcr.run_id = tre.run_id and tre.machine_os = '"+i[0]+"' and tre.client = '"+i[1]+"' and tre.product_version = '"+version+"' and tcr.tc_id = tct.tc_id and tct.property = 'section_id' and tct.name::int = ps.section_id and ps.section_path = '"+s[0]+"' and tct.property = 'JiraId' and tct.name != ''" , False)
            defect_count = len(defected_cases)
            temp.append(defect_count)
            temp.append(pass_count + fail_count - same + block_count - same1 + notrun_count + defect_count)
            
            Data.append(tuple(temp))
        sum = []
        Total = ["Total"]
        sum.append(Total)
        for y in range(1,len(temp)):
            huda = 0
            for z in range(len(sections)):
                huda = huda + Data[z][y]
            sum.append(huda)
        Data.append(sum)
        ReportTable.append(tuple(Data))
      
                    
    Heading = ['Section','Passed','Failed','Blocked','Not run','Defected','Total']
    results = {'Heading':Heading,'Env':env_details, 'ReportTable':ReportTable}
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
    #if request.is_ajax():
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
                #Call Jira api to get open defects list by passing all list
                OpenDefectList = DefectList

                #add the open defect count for this section to the Execution count results table
                QueryResult.append((eachDataGroup[0][0], 'Defects', len(OpenDefectList)))
                SectionOpenDefectsGroup.append((eachDataGroup[0][0], OpenDefectList))

            QueryResult.sort(cmp=None, key=operator.itemgetter(0), reverse=False)

            SectionDataGroup = []
            for key, group in itertools.groupby(QueryResult, operator.itemgetter(0)):
                SectionDataGroup.append(list(group))

            ReportTable = []
            for eachDataGroup in SectionDataGroup:
                SectionPath = eachDataGroup[0][0]
                #for eachtup in eachDataGroup:

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
                #Call jira api to get defect title by passing a list of jira ids
                DefectDetail = eachDataGroup[1]
                for eachDefect in DefectDetail:
                    #commenting till jira api is implemented
                    #DefectTable.append((eachDefect[0],eachDefect[1],FormattedSectionName))
                    DefectTable.append((eachDefect[0], FormattedSectionName))

    Heading = ['Section','Passed','Failed','Blocked','Never run','Total']
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

def Process_Git(request):
    #Conn = GetConnection()
    import GitApi
    #if request.is_ajax():
    if request.method == "GET":
        command = request.GET.get(u'command', '')
        if command == 'Pull':
            GitApi.pull_latest_git()
            message = 'git pull'
        elif command == 'Log':
            GitApi.git_log(-10)
            message = 'git log'

    return render_to_response('Admin.html',{'error_message':message},context_instance=RequestContext(request))

def DeleteExistingTestCase(TC_Ids):
    conn = Conn
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
#Test Set and Tag Management section

def TestSet_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        data_type=request.GET.get(u'data_type','')
        results = DB.GetData(Conn, "select  value,type from config_values where value Ilike '%" + value + "%' and type='"+data_type+"'",False)
        #test_tag=DB.GetData(Conn,"")
        #results=list(set(results+test_tag))
        #if len(results) > 0:
         #   results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestFeatureDriver_Auto(request):               #minar09
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        data_type=request.GET.get(u'data_type','')
        results = DB.GetData(Conn, "select distinct value,type from config_values where value Ilike '%" + value + "%' and type='"+data_type+"'",False)
        #if len(results)>0:
            #results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def TestTag_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select tc_id from test_cases where tc_id in(select  tc_id from test_case_tag where property Ilike '%"+value+"%'")
        if len(results)>0:
            results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def TestCase_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct tc_name from test_cases where tc_name Ilike '%" + value + "%'")
        if len(results)>0:
            results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def TestSet(request,message=""):
    return render_to_response('TestSet_Tag.html',{'error_message':message},context_instance=RequestContext(request))

def Data_Process(request):
    #output="in the post processing page"
    if request.method=='POST':
        data_type=request.POST['type']
        operation=request.POST['operation']
        command=request.POST['submit_button']
        first_name=request.POST['inputName']
        second_name=request.POST['inputName2']
        if data_type=="tag":
            return general_work(request,data_type)
        elif data_type=="set":
            return general_work(request,data_type)
        elif data_type=="":
            return TestSet(request,"data is not posted successfully")
        elif data_type!="" and (first_name=="" or operation=="" or second_name=="" or command==""):
            return TestSet(request,"data is not posted successfully")
        else:
            return render_to_response('TestSet_Tag.html',{'error_message':"data is not posted successfully"},context_instance=RequestContext(request))
    return TestSet(request,"data is not posted successfully")
def general_work(request,data_type):
    def Check_instance(x,data_type):
        if x in request.POST:
            name=request.POST[x]
            conn=GetConnection()
            result=DB.GetData(conn, "SELECT count(*) FROM config_values WHERE value='"+name+"' AND type='"+data_type+"'")
            return result[0]
        else:
            return -1
    temp=0
    if request.method=='POST':
        datatype=request.POST['type']
        operation=request.POST['operation']
        command=request.POST['submit_button']
        first_name=request.POST['inputName']
        second_name=request.POST['inputName2']
        if operation=="2"  and first_name!="" and second_name!="" and datatype!="":
            temp=Check_instance('inputName',data_type)
            if(temp==0):
                if request.POST['inputName']!="":
                    output="no such test "+data_type+ " with name '"+request.POST['inputName']+"'"
                    return TestSet(request,output)
                else:
                    output="Name field is empty"
                    return TestSet(request,output)
            if(temp>0):
                if(first_name!="" and second_name!=""):
                    return rename(request,first_name,second_name,data_type)
                else:
                    output="Name field is empty"
                    return TestSet(request,output)
        if operation=="1" and first_name!="" and second_name=="" and datatype!="":
            temp=Check_instance('inputName',data_type)
            if(temp==0):
                name=request.POST['inputName']
                if(name!=""):
                    return create(request,name,data_type)
                else:
                    output="Name field is empty"
                    return TestSet(request,output)
            if(temp>0):
                output="Test "+data_type+" with name '"+request.POST['inputName']+"' is already in the database"
                return TestSet(request,output)
        if operation=="3" and first_name!="" and second_name=="" and datatype!="":
            temp=Check_instance('inputName',data_type)
            if(temp>0):
                name=request.POST['inputName']
                if(name!=""):
                    return edit(request,name,data_type)
                else:
                    output="Name field is empty"
            # output+=edit(name)
        if operation=="4" and first_name!="" and second_name=="" and datatype!="":
            temp=Check_instance('inputName',data_type)
            if(temp>0):
                name=request.POST['inputName']
                if(name!=""):
                    return delete(request,name,data_type)
                else:
                    output="Name field is empty"
                    TestSet(request,output)
            if(temp==0):
                output="No such test "+data_type+" with the name '"+request.POST['inputName']+"'"
                return TestSet(request,output)
        if datatype=="":
            return TestSet(request,"data is not posted successfully")
            #output+=delete(name)
    #return output
def TestCases_InSet(name,data_type):
    conn=GetConnection()
    query="select tc_id,tc_name from test_cases where tc_id in (select tc_id from test_case_tag where name='"+name+"' and property='"+data_type+"')"
    result=DB.GetData(conn,query,False)
    ex_tc_ids=[]
    ex_tc_names=[]
    for x in result:
        ex_tc_ids.append(x[0])
        ex_tc_names.append(x[1])
    ex_lst=[{'item1':t[0],'item2':t[1]} for t in zip(ex_tc_ids,ex_tc_names)]
    conn.close()
    return ex_lst
def edit(request,name,data_type,error_message=""):
    output={}
    ex_lst=TestCases_InSet(name,data_type)
    output.update({'name':name,'data_type':data_type})
    output.update({'ex_lst':ex_lst,'error_message':error_message})
    return render_to_response('ManageTestSet.html',output,context_instance=RequestContext(request))

def rename(request,first,second,data_type):
    conn=GetConnection()
    if first != second and first!="" and second!="":
        query = "Where  value = '"+first+"' and type='"+data_type+"'"
        testrunenv=DB.UpdateRecordInTable(conn,"config_values",query,value=second)
        result=DB.GetData(conn, "SELECT count(*) FROM test_case_tag WHERE name='"+first+"'")
        if result[0]>0:
            query="Where name='"+first+"' and property='"+data_type+"'"
            testrunenv_2=DB.UpdateRecordInTable(conn,"test_case_tag",query,name=second)
            if testrunenv_2==True:
                query=""
        conn.close()
        if testrunenv==True:
            return render_to_response('TestSet_Tag.html',{'error_message':"Old Test "+data_type+" name \""+first+"\" is updated to \""+second+"\""},context_instance=RequestContext(request))
           
    return render_to_response('TestSet_Tag.html',{'error_message':"Check the input fields or Same name in both fields"},context_instance=RequestContext(request))
    
def create(request,name,data_type):
    conn=GetConnection()
    testrunenv = DB.InsertNewRecordInToTable(conn, "config_values", value=name,type=data_type)
    conn.close()
    if testrunenv==True:
        return render_to_response('TestSet_Tag.html',{'error_message':"Test "+data_type+" with name "+name+" is created successfully"},context_instance=RequestContext(request))
    else:
        return render_to_response('TestSet_Tag.html',{'error_message':"Check the input fields"},context_instance=RequestContext(request))
    

def delete(request,inputName,data_type):
    conn=GetConnection()
    testrunenv=DB.DeleteRecord(conn,"config_values",value=inputName,type=data_type)
    result=DB.GetData(conn, "SELECT count(*) FROM test_case_tag WHERE name='"+inputName+"'")
    if result[0]>0:
        testrunenv_2=DB.DeleteRecord(conn,"test_case_tag",name=inputName,property=data_type)
    conn.close()
    if testrunenv==True:
        return render_to_response('TestSet_Tag.html',{'error_message':"Test "+data_type +" name with \""+inputName+"\" is deleted successfully."},context_instance=RequestContext(request))

def AddTestCasesToSet(request):
    #output="in the add test case page"
    output=""
    if request.method=='POST':
        selected_tc=request.POST.getlist('selectTCAdd')
        test_set_name=request.POST['set_name']
        test_type=request.POST['set_type']
        if(len(selected_tc)==0):
            ex_lst=TestCases_InSet(test_set_name,test_type)
            output={}
            output.update({'ex_lst':ex_lst})
            output.update({'error_message':"No check box selected",'name':test_set_name,'data_type':test_type})
            return render_to_response('ManageTestSet.html',output,context_instance=RequestContext(request))
        else:
            conn=GetConnection()
            tc_cases=[]
            available_tc=DB.GetData(conn, "SELECT tc_id FROM test_case_tag WHERE name='"+test_set_name+"'", False)
            for x in available_tc:
                tc_cases.append(x[0])
            count=0
            for x in selected_tc:
                if x not in tc_cases:
                    testrunenv=DB.InsertNewRecordInToTable(conn,"test_case_tag",tc_id=x,name=test_set_name,property=test_type)
                    if testrunenv==True:
                        count+=1
            conn.close()
            if count==0:
                    message="No test cases are added to Test "+test_type+" '"+test_set_name+"'"
            if count>0:
                message=str(count) +" test cases are added to Test "+test_type+" '"+test_set_name+"',"+str(len(selected_tc)-count)+" test cases are left"
            return edit(request, test_set_name, test_type, message)
    return edit(request, test_set_name, test_type, output)
    
def DeleteTestCasesFromSet(request):
    output=""
    if request.method=='POST':
        selected_tc=request.POST.getlist('selectTCremove')
        test_set_name=request.POST['set_name']
        test_type=request.POST['set_type']
        if(len(selected_tc)==0):
            ex_lst=TestCases_InSet(test_set_name,test_type)
            output={}
            output.update({'ex_lst':ex_lst})
            output.update({'error_message':"No check box selected",'name':test_set_name,'data_type':test_type})
            return render_to_response('ManageTestSet.html',output,context_instance=RequestContext(request))
        else:
            conn=GetConnection()
            count=0
            for x in selected_tc:
                testrunenv=DB.DeleteRecord(conn, "test_case_tag",tc_id=x,name=test_set_name,property=test_type)
                if testrunenv==True:
                    count+=1
            conn.close()
            if count==0:
                    message="No test cases are deleted from Test "+test_type+" '"+test_set_name+"'"
            if count>0:
                message=str(count) +" test cases are deleted from Test "+test_type+" '"+test_set_name+"'"
            return edit(request, test_set_name, test_type, message)
    return edit(request,test_set_name,test_type,output)


#Test Step Management Section Functions
def TestStep_Delete(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select count(*) from test_steps where step_id=(select step_id from test_steps_list where stepname='"+value+"')")
        if(results[0]==0):
            testrunenv=DB.DeleteRecord(Conn, "test_steps_list",stepname=value)
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def TestFeature_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct value,type from config_values where value Ilike '%" + value + "%' and type='feature'",False)
        #if len(results)>0:
            #results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def Get_Feature(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        feature = request.GET.get(u'feature', '')
        if feature=='':
            results = DB.GetData(Conn, "select  distinct value from config_values where type='feature'",False)
        #if len(results)>0:
            #results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def ResultFilter(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select distinct assigned_tester,run_type from test_run_env",False)
        #if len(results)>0:
            #results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def TestDriver_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct value,type from config_values where value Ilike '%" + value + "%' and type='driver'",False)
        #if len(results)>0:
            #results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def Get_Driver(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        driver = request.GET.get(u'driver', '')
        if driver=='':
            results = DB.GetData(Conn, "select  distinct value from config_values where type='driver'",False)
        #if len(results)>0:
            #results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def TestStep_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct stepname,steptype from test_steps_list where stepname Ilike '%" + value + "%'",False)
        # if len(results)>0:
        #  results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

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
    conn=GetConnection()
    TableData = []
    RefinedData=[]
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Query', '')
            sQuery="select tc_id,tc_name from test_cases where tc_id in (SELECT distinct tc_id FROM test_steps where step_id=(SELECT distinct step_id FROM test_steps_list WHERE stepname='"+UserData+"'))"
            TableData=DB.GetData(conn, sQuery, False)
            Check_TestCase(TableData, RefinedData)
    Heading = ['TestCase_ID', 'TestCase_Name','TestCase_Type']
    results = {'Heading':Heading, 'TableData':RefinedData}
    #results={'TableData':TableData}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def TestSteps_Results(request):
    conn=GetConnection()
    TableData = []
    #RefinedData=[]
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Query', '')
            sQuery="select stepname from test_steps_list where stepFeature='"+UserData+"' or driver='"+UserData+"'" 
            TableData=DB.GetData(conn, sQuery, False)
            #Check_TestCase(TableData, RefinedData)
    Heading = ['TestStep_Name']
    results = {'Heading':Heading, 'TableData':TableData}
    #results={'TableData':TableData}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def Check_TestCase(TableData,RefinedData):
    conn=GetConnection()
    test_type=[u'automated',u'manual',u'performance']
    type_selector=[]
    query = "select tc_id from test_case_tag where name like '%Status%' and property='Forced'"
    forced = DB.GetData(conn, query, False)
    for each in TableData:
        type_selector=[]
        data=[]
        data.append(each[0])
        data.append(each[1])
        for item in test_type:
            sQuery="select count(*) from test_steps_list where step_id in(select step_id from test_steps where tc_id='"+each[0]+"') and steptype='"+item+"'"
            result=DB.GetData(conn, sQuery, False)
            type_selector.append(result[0])
        #a = type_selector[0]
        b = type_selector[1]
        c = type_selector[2]
        if b[0]>0L and c[0]==0L:
            data.append(test_type[1])
            each=tuple(data)
            RefinedData.append(each)
        elif c[0]>0L and b[0]==0L:
            #print "performance"
            data.append(test_type[2])
            each=tuple(data)
            RefinedData.append(each)
        elif b[0]>0L and c[0]>0L:
            data.append(test_type[1])
            each=tuple(data)
            RefinedData.append(each)
        else:
            # print "automated"
            man = 0
            for f in forced:
                if f[0]==each[0]:
                    man = 1
            if man==1:
                data.append(test_type[1])
            else:
                data.append(test_type[0])
            each=tuple(data)
            RefinedData.append(each)
            
def Populate_info_div(request):
    conn=GetConnection()
    if request.method=='GET':
        value=request.GET.get(u'term','')
        sQuery="SELECT * from test_steps_list where stepname='"+value+"'"
    results=DB.GetData(conn, sQuery,False)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
def TestStepDelete(request):
    error_message="Test Step is deleted successfully"
    return TestStep(request,error_message)
def TestStep(request,error_message=""):
    """templ=get_template('TestStep.html')
    variables=Context({})
    output=templ.render(variables)
    return HttpResponse(output)"""
    output={'error_message':error_message}
    return render_to_response('TestStep.html',output,context_instance=RequestContext(request))

def Process_TestStep(request):
    output="in the processing page"
    if request.method=='POST':
        step_name=request.POST['step_name']
        step_desc=request.POST['step_desc']
        step_feature=request.POST['step_feature']
        step_data=request.POST['step_data']
        step_type=request.POST['step_type']
        step_driver=request.POST['step_driver'] 
        step_enable=request.POST['step_enable']
        if step_name!="" and step_desc!="" and step_feature!="" and step_data!="0" and step_enable!="0":
            if step_type!="0" and step_driver!="":
                conn=GetConnection()
                sQuery="select count(*) from test_steps_list where stepname='"+step_name+"'"
                result=DB.GetData(conn, sQuery)
                if(result[0]>0):
                    if(step_data=="1"):
                        data="true"
                    if(step_data=="2"):
                        data="false"
                    if(step_type=="1"):
                        s_type="automated"
                    if(step_type=="2"):
                        s_type="manual"
                    if(step_type=="3"):
                        s_type="performance"
                    if(step_enable=="1"):
                        enable="true"
                    if(step_enable=="2"):
                        enable="false"
                    query = "Where  stepname = '"+step_name+"'"
                    testrunenv=DB.UpdateRecordInTable(conn, "test_steps_list",query,description=step_desc,data_required=data,steptype=s_type,driver=step_driver,stepfeature=step_feature,stepenable=enable)
                    query="SELECT count(*) FROM config_values where type='feature' and value='"+step_feature+"'"
                    feature_count=DB.GetData(conn,query)
                    if(feature_count[0]<1):
                        testrunenv=DB.InsertNewRecordInToTable(conn, "config_values",type='feature',value=step_feature)
                    query="SELECT count(*) FROM config_values where type='driver' and value='"+step_driver+"'"
                    driver_count=DB.GetData(conn, query)
                    if(driver_count[0]<1):
                        testrunenv=DB.InsertNewRecordInToTable(conn, "config_values",type='driver',value=step_driver)
                    if testrunenv==True:
                        message="Test Step with name '"+step_name+"' is updated"
                        return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                    else:
                        message="Test Step with name '"+step_name+"' is not updated.Please Try again"
                        return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                else:
                    if(step_data=="1"):
                        data="true"
                    if(step_data=="2"):
                        data="false"
                    if(step_type=="1"):
                        s_type="automated"
                    if(step_type=="2"):
                        s_type="manual"
                    if(step_type=="3"):
                        s_type="performance"
                    if(step_enable=="1"):
                        enable="true"
                    if(step_enable=="2"):
                        enable="false"
                    
                    testrunenv=DB.InsertNewRecordInToTable(conn, "test_steps_list",stepname=step_name,description=step_desc,data_required=data,steptype=s_type,driver=step_driver,stepfeature=step_feature,stepenable=enable)
                    query="SELECT count(*) FROM config_values where type='feature' and value='"+step_feature+"'"
                    feature_count=DB.GetData(conn,query)
                    if(feature_count[0]<1):
                        testrunenv=DB.InsertNewRecordInToTable(conn, "config_values",type='feature',value=step_feature)
                    query="SELECT count(*) FROM config_values where type='driver' and value='"+step_driver+"'"
                    driver_count=DB.GetData(conn, query)
                    if(driver_count[0]<1):
                        testrunenv=DB.InsertNewRecordInToTable(conn, "config_values",type='driver',value=step_driver)
                    if testrunenv==True:
                        message="Test Step with name '"+step_name+"' is created"
                        return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                    else:
                        message="Test Step with name '"+step_name+"' is not created.Please Try again"
                        return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))         
            else:
                error_message="Input Fields are empty.Check the input fields"
                error={'error_message':error_message}
                return render_to_response('TestStep.html',error,context_instance=RequestContext(request))
        else:
                error_message="Input Fields are empty.Check the input fields"
                error={'error_message':error_message}
                return render_to_response('TestStep.html',error,context_instance=RequestContext(request))
    return HttpResponse(output)

def Process_FeatureDriver(request):                    #minar09
    output="in the processing page"
    if request.method=='POST':
        data_type=request.POST['type']
        operation=request.POST['operation']
        input1=request.POST['inputName']        
        if data_type!="" and operation!="" and input1!="":
            if data_type!="0":
                conn=GetConnection()
                if operation=="1":                                       
                    query="SELECT count(*) FROM config_values where type='"+data_type+"' and value='"+input1+"'"
                    count=DB.GetData(conn,query)
                    if(count[0]<1):
                        testrunenv=DB.InsertNewRecordInToTable(conn, "config_values",type=data_type,value=input1)
                        if testrunenv==True:
                            message=""+data_type+" with name '"+input1+"' is created."
                            return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                        else:
                            message=""+data_type+" with name '"+input1+"' is not created. Please Try again."
                            return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request)) 
                    else:
                        message=""+data_type+" with name '"+input1+"' is already created."
                        return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                if operation=="2":
                    input2=request.POST['inputName2']
                    if input2=="":
                        error_message="Input Fields are empty.Check the input fields"
                        error={'error_message':error_message}
                        return render_to_response('TestStep.html',error,context_instance=RequestContext(request))
                    else:  
                        query="SELECT count(*) FROM config_values where type='"+data_type+"' and value='"+input1+"'"
                        count=DB.GetData(conn,query)
                        if(count[0]<1):
                            message=""+data_type+" with name '"+input1+"' is not found."
                            return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))                            
                        else:
                            srquery = "SELECT count(*) FROM test_steps_list where driver='"+input1+"' or stepfeature='"+input1+"'"
                            searchCount = DB.GetData(Conn, srquery)
                            if (searchCount[0]<1):
                                whereQuery = "where type='"+data_type+"' and value = '"+input1+"' "
                                testrunenv=DB.UpdateRecordInTable(conn, "config_values",whereQuery,value=input2,type=data_type) 
                                if testrunenv==True:
                                    message=""+data_type+" with name '"+input1+"' is updated to '"+input2+"'."
                                    return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                                else:
                                    message=""+data_type+" with name '"+input1+"' is not updated. Please Try again."
                                return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                            else:  
                                whereQuery = "where type='"+data_type+"' and value = '"+input1+"' "
                                testrunenv=DB.UpdateRecordInTable(conn, "config_values",whereQuery,value=input2,type=data_type)                                                                                                                    
                                whereQuery = "where driver='"+input1+"'"
                                testrunenv1=DB.UpdateRecordInTable(conn, "test_steps_list",whereQuery,driver=input2)
                                whereQuery = "where stepfeature='"+input1+"'"
                                testrunenv2=DB.UpdateRecordInTable(conn, "test_steps_list",whereQuery,stepfeature=input2)
                                if (testrunenv==True and testrunenv1==True) or (testrunenv==True and testrunenv2==True) or (testrunenv==True and testrunenv1==True and testrunenv2==True):
                                    message=""+data_type+" with name '"+input1+"' is updated to '"+input2+"'."
                                    return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))
                                else:
                                    message=""+data_type+" with name '"+input1+"' is not updated. Please Try again."
                                    return render_to_response('TestStep.html',{'error_message':message},context_instance=RequestContext(request))                             
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
                error_message="Input Fields are empty.Check the input fields"
                error={'error_message':error_message}
                return render_to_response('TestStep.html',error,context_instance=RequestContext(request))
        else:
                error_message="Input Fields are empty.Check the input fields"
                error={'error_message':error_message}
                return render_to_response('TestStep.html',error,context_instance=RequestContext(request))
    return HttpResponse(output)
    
def FeatureDriver_Delete(request):                              #minar09
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        data_type = request.GET.get(u'term', '')
        input1 = request.GET.get(u'inputName', '')
        results = DB.GetData(Conn, "select count(*) from test_steps_list where driver='"+input1+"' or stepFeature='"+input1+"'")
        if(results[0]==0):
            testrunenv=DB.DeleteRecord(Conn, "config_values",type=data_type,value=input1)
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def FeatureDriverDelete(request):                               #minar09
    error_message="Feature/Driver is deleted successfully"
    return TestStep(request,error_message)

def myview(request):
    import RenderPDF
    #Retrieve data or whatever you need
    results = []
    return RenderPDF.render_to_pdf(
            'TestTypeStatus.html',
            {
                'pagesize':'A4',
                'mylist': results,
            }
        )

def TestTypeStatus_Report(request):                     #minar09
    Conn = GetConnection()
    sections = []
    priority = ["P1","P2","P3","P4","Total"]
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
            if UserData=="All":
                sectionQuery="select product_sections.section_path from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path"
                testCasesQuery="select test_case_tag.tc_id, product_sections.section_path from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' group by test_case_tag.tc_id, product_sections.section_path"
                totalCaseQuery="select count(test_case_tag.tc_id) from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path"
            else:
                sectionQuery="select product_sections.section_path from product_sections,test_case_tag where product_sections.section_id::text = test_case_tag.name and product_sections.section_path ~ '"+UserData+".*' and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path"
                testCasesQuery="select test_case_tag.tc_id, product_sections.section_path from product_sections, test_case_tag where product_sections.section_id::text = test_case_tag.name and test_case_tag.property='section_id' and product_sections.section_path ~ '"+UserData+".*' group by test_case_tag.tc_id, product_sections.section_path"
                totalCaseQuery="select count(test_case_tag.tc_id) from product_sections,test_case_tag where product_sections.section_id::text = test_case_tag.name and product_sections.section_path ~ '"+UserData+".*' and test_case_tag.property='section_id' group by product_sections.section_path order by product_sections.section_path" 
        sections=DB.GetData(Conn, sectionQuery, False)        
        totalCases=DB.GetData(Conn, totalCaseQuery, False)
        testCases=DB.GetData(Conn, testCasesQuery, False)
        progress=DB.GetData(Conn, "select tc_id from test_case_tag where property='Dev'", False)
        p1Priority=DB.GetData(Conn, "select tc_id from test_case_tag where property='Priority' and name='P1'", False)
        p2Priority=DB.GetData(Conn, "select tc_id from test_case_tag where property='Priority' and name='P2'", False)
        p3Priority=DB.GetData(Conn, "select tc_id from test_case_tag where property='Priority' and name='P3'", False)
        p4Priority=DB.GetData(Conn, "select tc_id from test_case_tag where property='Priority' and name='P4'", False)
        
    #sections.append('Summary Global')
    for each in sections:     
        for y in priority:
            data=[]
            data.append(each[0].replace(".","-"))
            data.append(y)
            Table.append(tuple(data))
            
    #Table = zip(sections,priority)
    Check_TestCase(testCases, RefinedData)
    #manual 
    for each in RefinedData:
        Data = []
        Data.append(each[0])
        Data.append(each[1])
        if each[2] == 'manual':
            this = True
            for x in progress:
                if x[0] == each[0]:
                    this = False
            if this==True:
                manTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0]==p1[0]:
                        manP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0]==p2[0]:
                        manP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0]==p3[0]:
                        manP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0]==p4[0]:
                        manP4Tab.append(tuple(Data))
            elif this==False:
                manIPTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0]==p1[0]:
                        manIPP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0]==p2[0]:
                        manIPP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0]==p3[0]:
                        manIPP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0]==p4[0]:
                        manIPP4Tab.append(tuple(Data))
        elif each[2] == 'automated':
            this = True
            for x in progress:
                if x[0] == each[0]:
                    this = False
            if this==True:
                autoTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0]==p1[0]:
                        autoP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0]==p2[0]:
                        autoP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0]==p3[0]:
                        autoP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0]==p4[0]:
                        autoP4Tab.append(tuple(Data))
            elif this==False:
                autoIPTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0]==p1[0]:
                        autoIPP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0]==p2[0]:
                        autoIPP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0]==p3[0]:
                        autoIPP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0]==p4[0]:
                        autoIPP4Tab.append(tuple(Data))
        elif each[2] == 'performance':
            this = True
            for x in progress:
                if x[0] == each[0]:
                    this = False
            if this==True:
                perTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0]==p1[0]:
                        perP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0]==p2[0]:
                        perP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0]==p3[0]:
                        perP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0]==p4[0]:
                        perP4Tab.append(tuple(Data))
            elif this==False:
                perIPTab.append(tuple(Data))
                for p1 in p1Priority:
                    if each[0]==p1[0]:
                        perIPP1Tab.append(tuple(Data))
                for p2 in p2Priority:
                    if each[0]==p2[0]:
                        perIPP2Tab.append(tuple(Data))
                for p3 in p3Priority:
                    if each[0]==p3[0]:
                        perIPP3Tab.append(tuple(Data))
                for p4 in p4Priority:
                    if each[0]==p4[0]:
                        perIPP4Tab.append(tuple(Data))
                
    Count_Per_Section(manTab,sections,manCount)
    Count_Per_Section(manP1Tab,sections,manP1Count)
    Count_Per_Section(manP2Tab,sections,manP2Count)
    Count_Per_Section(manP3Tab,sections,manP3Count)
    Count_Per_Section(manP4Tab,sections,manP4Count)
    Count_Per_Section(manIPTab,sections,manIPCount) 
    Count_Per_Section(manIPP1Tab,sections,manIPP1Count)
    Count_Per_Section(manIPP2Tab,sections,manIPP2Count)
    Count_Per_Section(manIPP3Tab,sections,manIPP3Count)
    Count_Per_Section(manIPP4Tab,sections,manIPP4Count)
    Count_Per_Section(autoTab,sections,autoCount) 
    Count_Per_Section(autoP1Tab,sections,autoP1Count)
    Count_Per_Section(autoP2Tab,sections,autoP2Count)
    Count_Per_Section(autoP3Tab,sections,autoP3Count)
    Count_Per_Section(autoP4Tab,sections,autoP4Count)
    Count_Per_Section(autoIPTab,sections,autoIPCount)
    Count_Per_Section(autoIPP1Tab,sections,autoIPP1Count)
    Count_Per_Section(autoIPP2Tab,sections,autoIPP2Count)
    Count_Per_Section(autoIPP3Tab,sections,autoIPP3Count)
    Count_Per_Section(autoIPP4Tab,sections,autoIPP4Count)
    Count_Per_Section(perTab,sections,perCount) 
    Count_Per_Section(perP1Tab,sections,perP1Count)
    Count_Per_Section(perP2Tab,sections,perP2Count)
    Count_Per_Section(perP3Tab,sections,perP3Count)
    Count_Per_Section(perP4Tab,sections,perP4Count)
    Count_Per_Section(perIPTab,sections,perIPCount)
    Count_Per_Section(perIPP1Tab,sections,perIPP1Count)
    Count_Per_Section(perIPP2Tab,sections,perIPP2Count)
    Count_Per_Section(perIPP3Tab,sections,perIPP3Count)
    Count_Per_Section(perIPP4Tab,sections,perIPP4Count)
    Append_array(Table,manP1Count,manP2Count,manP3Count,manP4Count,manCount,Table1) 
    Append_array(Table1,manIPP1Count,manIPP2Count,manIPP3Count,manIPP4Count,manIPCount,Table2)
    Append_array(Table2,autoP1Count,autoP2Count,autoP3Count,autoP4Count,autoCount,Table3)
    Append_array(Table3,autoIPP1Count,autoIPP2Count,autoIPP3Count,autoIPP4Count,autoIPCount,Table4)
    Append_array(Table4,perP1Count,perP2Count,perP3Count,perP4Count,perCount,Table5)
    Append_array(Table5,perIPP1Count,perIPP2Count,perIPP3Count,perIPP4Count,perIPCount,Table6)
    #Append_array(Table4,totalCases,TableData)
    x=1
    a=0
    b=0
    c=0
    d=0
    e=0   
    for each in Table6:
        data=[]
        for y in each:
            data.append(y)
        if x==1:
            count = manP1Count[a] + manIPP1Count[a] + autoP1Count[a] + autoIPP1Count[a] + perP1Count[a] + perIPP1Count[a]
            a=a+1
            data.append(count)
            totalP1Count.append(count)
        elif x==2:
            count = manP2Count[b] + manIPP2Count[b] + autoP2Count[b] + autoIPP2Count[b] + perP2Count[b] + perIPP2Count[b]
            b=b+1
            data.append(count)
            totalP2Count.append(count)
        elif x==3:
            count = manP3Count[c] + manIPP3Count[c] + autoP3Count[c] + autoIPP3Count[c] + perP3Count[c] + perIPP3Count[c]
            c=c+1
            data.append(count)
            totalP3Count.append(count)
        elif x==4:
            count = manP4Count[d] + manIPP4Count[d] + autoP4Count[d] + autoIPP4Count[d] + perP4Count[d] + perIPP4Count[d]
            d=d+1
            data.append(count)
            totalP4Count.append(count)
        elif x==5:
            count = manCount[e] + manIPCount[e] + autoCount[e] + autoIPCount[e] + perCount[e] + perIPCount[e]
            e=e+1
            data.append(count)
            totalCount.append(count)
        TableData.append(tuple(data))
        if x==5:
            x=1
        elif x<5:
            x=x+1
    
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
        
    Heading = ['Section','Priority','Manual','Manual in-progress','Automated','Automated in-progress','Performance','Performance in-progress','Total']
    results = {'Heading':Heading, 'TableData':TableData, 'Summary':tuple(temp)}
    #results = {'Heading':Heading, 'TableData':RefinedData}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def count_Sum(caseCount):
    count = 0
    for each in caseCount:
        count = count + each
    return count

def Count_Per_Section(testCases,sections,caseCount):                    #minar09
    for each in sections:
        x = 0
        z = each[0]
        for case in testCases:
            y = case[1]
            if y==z:
                x=x+1
        caseCount.append(x)
            
def Append_array(TableData,P1,P2,P3,P4,Total,RefinedData):          #minar09
    x=1
    a=0
    b=0
    c=0
    d=0
    e=0                    
    for each in TableData:
        data=[]
        for y in each:
            data.append(y)
        if x==1:
            data.append(P1[a])
            a=a+1
        elif x==2:
            data.append(P2[b])
            b=b+1
        elif x==3:
            data.append(P3[c])
            c=c+1
        elif x==4:
            data.append(P4[d])
            d=d+1
        elif x==5:
            data.append(Total[e])
            e=e+1
        RefinedData.append(tuple(data))
        if x==5:
            x=1
        elif x<5:
            x=x+1


def TestStepAutoComplete(request):
    Conn = GetConnection()
    results = []
    test=[]
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        field=[u'stepname',u'stepfeature',u'steptype',u'driver']
        for each in field:
            statement=""
            if each=='stepname':
                statement='step'
            if each=='stepfeature':
                statement='feature'
            if each=='steptype':
                statement='type'
            if each=='driver':
                statement='driver'
            test = DB.GetData(Conn, "select  distinct "+each+"||' - "+statement+"' from test_steps_list where "+ each+" Ilike '%" + value + "%'")
            results=list(results+test)    
    if len(results)>0:
        results.append("*Dev")    
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json') 

def TestStep_TestCases(request):
    Conn=GetConnection()
    fields=[u'stepfeature',u'driver',u'steptype']
    TableData=[]
    RefinedData=[]
    if request.is_ajax():
        if request.method=="GET":
            search_query=request.GET.get(u'Query','')
            search_value=search_query.split(":")
            for each_item in search_value:
                each_item=each_item.strip();
                if each_item!="":
                    query=" where stepname='"+each_item+"'"
                    for each in fields:
                        query+=" or "+each+"='"+each_item+"'"
                    query="SELECT distinct tc_id,tc_name FROM test_cases where tc_id in (SELECT distinct tc_id from test_steps where step_id in(SELECT distinct step_id from test_steps_list "+query+"))"
                    TableData_1=DB.GetData(Conn, query,False)
                    TableData.append(TableData_1)
            resultData=TableData[0]
            for each in TableData:
                setData=set(resultData).intersection(set(each))
                resultData=list(setData)
            Check_TestCase(resultData, RefinedData)
        Heading = ['TestCase_ID', 'TestCase_Name','TestCase_Type']
        results = {'Heading':Heading, 'TableData':RefinedData}
        json=simplejson.dumps(results)
        return HttpResponse(json,mimetype='application/json')
def TestStepWithTypeInTable(request):
    Conn = GetConnection()
    if request.is_ajax():
        if request.method == 'GET':
            #TestCaseName = request.GET.get('ClickedTC', '')
            RunID = request.GET.get('RunID', '')
            print RunID
            RunID = str(RunID.strip())
            RunID = str(RunID.replace(u'\xa0', u''))
            result=[]
            if RunID != '':
                Result = DB.GetData(Conn, "Select stepname from test_steps tst,test_steps_list tsl where tst.step_id = tsl.step_id and tc_id  = '%s' order by teststepsequence" % RunID)
            for each in Result:
                query="select steptype from test_steps_list where stepname='"+each+"'"
                Result_type=DB.GetData(Conn, query)
                result.append((each,Result_type[0]))
    column=['Step Name','Step Type']
    results = {'Result':result,'column':column}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def RunIDTestCases(request,Run_Id,TC_Id):
    print Run_Id
    print TC_Id
    Conn=GetConnection()
    query="select tc_name from test_cases where tc_id='%s'" %TC_Id
    testcasename=DB.GetData(Conn, query, False)
    return render_to_response('RunIDEditTestCases.html',{'runid':Run_Id,'testcaseid':TC_Id,'testcasename':testcasename[0][0]})

def DataFetchForTestCases(request):
    #message="in the DataFetchForTestCases"
    if request.is_ajax():
        if request.method=='GET':
            run_id=request.GET.get(u'run_id','').strip()
            test_case_id=request.GET.get(u'test_case_id','').strip()
            print run_id
            print test_case_id
            #Get the test steps from test_step_results
            Conn=GetConnection()
            query="select test_steps.step_id from test_step_results,test_steps where test_step_results.tc_id=test_steps.tc_id and test_step_results.teststep_id=test_steps.step_id and test_step_results.tc_id='%s' and test_step_results.run_id='%s' order by test_steps.teststepsequence;"%(test_case_id,run_id)
            TestStepList=DB.GetData(Conn, query)
            DataCollected=[]
            Conn.close()
            for each in range(0,len(TestStepList)):
                Conn=GetConnection()
                #Get the stepname fromt test_steps_list
                query="select stepname,steptype,data_required from test_steps_list where step_id=%d" %TestStepList[each]
                StepName=DB.GetData(Conn,query,False)
                Temp_Data=[]
                Temp_Data.append(each+1)
                Temp_Data.append(StepName[0][0])
                Temp_Data.append(StepName[0][1])
                if StepName[0][2]==True:
                    Temp_Data.append("true")
                else:
                    Temp_Data.append("false")
                datasetid=test_case_id+"_s"+str((each+1))
                print datasetid
                #Get the description from the master_data
                query="select description from master_data where id='%s' and field='step' and value='description'" %datasetid
                step_description=DB.GetData(Conn,query,False)
                Temp_Data.append(step_description[0][0])
                query="select description from master_data where id='%s' and field='expected' and value='result'" %datasetid
                step_expected=DB.GetData(Conn,query,False)
                Temp_Data.append(step_expected[0][0])
                #Get the expected Result from the master data
                #Get the failreson from the test_step_results
                #Get the steps status from the test_step_results
                query="select status,failreason from test_step_results where tc_id='%s' and run_id='%s' and teststep_id=%d" %(test_case_id,run_id,(TestStepList[each])) 
                Status=DB.GetData(Conn,query,False) 
                Temp_Data.append(Status[0][1]) #FailReason
                Temp_Data.append(Status[0][0])
                Conn.close()
                print Temp_Data
                #Temp_Data.append("Log")
                Temp_Data=tuple(Temp_Data)
                DataCollected.append(Temp_Data)
    DataColumn=["#","Step","Type","Data","Description","Expected","Comment","Status"]
    query="select status from test_case_results where tc_id='%s' and run_id='%s'" %(test_case_id,run_id)
    Conn=GetConnection()
    test_case_status=DB.GetData(Conn,query,False)
    print DataColumn
    print DataCollected
    message={
             'data_column':DataColumn,
             'data_collected':DataCollected,
             'test_case_status':test_case_status[0][0]
             }
    results=simplejson.dumps(message)
    return HttpResponse(results,mimetype='application/json')
def TestDataFetch(request):
    if request.is_ajax():
        if request.method=='GET':
            data_set_id=request.GET.get(u'data_set_id','')
            Conn=GetConnection()
            query="select distinct id from master_data where id Ilike '%s" %data_set_id
            query+="_%'"
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
                query="select field,value from master_data where id Ilike '%s" %each
                query+="%%' and field!='step' and field!='' and value!='description'"
                data=DB.GetData(Conn,query,False)
                data_array.append(data)
    results={
             'data_array':data_array,
             'row_array': row_array
             }
    results=simplejson.dumps(results)
    return HttpResponse(results,mimetype='application/json')


def LogFetch(request):
    if request.is_ajax():
        if request.method=='GET':
            run_id=request.GET.get(u'run_id','').strip()
            test_case_id=request.GET.get(u'test_case_id','').strip()
            step_name=request.GET.get(u'step_name','').strip()
            print run_id
            print test_case_id
            print step_name
            Conn=GetConnection()
            query="select step_id from test_steps_list where stepname='%s'" %step_name
            step_id=DB.GetData(Conn,query,False)
            query="Select  el.status, el.modulename, el.details from test_step_results tsr, execution_log el where run_id = '%s' and tc_id = '%s' and teststep_id='%s' and tsr.logid = el.logid" % (run_id,test_case_id,str(step_id[0][0]))
            log=DB.GetData(Conn,query,False)
            column=["Status","ModuleName","Details"]
    message={
             'column':column,
             'log':log,
             'step':step_name
             }
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
def RunIDStatus(request):
    if request.is_ajax():
        if request.method=='GET':
                run_id=request.GET.get(u'run_id','')
                temp=[]
                total_query="select count(*) from test_run where run_id='%s'" %run_id
                pass_query="select count(*) from test_case_results where run_id='%s' and status='Passed'" %run_id
                fail_query="select count(*) from test_case_results where run_id='%s' and status='Failed'" %run_id
                blocked_query="select count(*) from test_case_results where run_id='%s' and status='Blocked'"%run_id
                progress_query="select count(*) from test_case_results where run_id='%s' and status='In-Progress'" %run_id
                submitted_query="select count(*) from test_case_results where run_id='%s' and status='Submitted'" %run_id
                Conn=GetConnection()
                total=DB.GetData(Conn,total_query)
                passed=DB.GetData(Conn,pass_query)
                failed=DB.GetData(Conn,fail_query)
                blocked=DB.GetData(Conn,blocked_query)
                progress=DB.GetData(Conn,progress_query)
                submitted=DB.GetData(Conn,submitted_query)
                #pending=total[0]-(passed[0]+failed[0]+progress[0]+not_run[0])
                temp.append(total[0])
                temp.append(passed[0])
                temp.append(failed[0])
                temp.append(blocked[0])
                temp.append(progress[0])
                temp.append(submitted[0])
    message={
             'message':temp
             }
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
def Make_List(step_name,step_reason,step_status,test_case_id):
    ListAll=[]
    if  isinstance(step_status, list):
        for name in zip(step_name,step_reason,step_status):
            ListAll.append((name[0].strip(),name[1].strip(),name[2].strip()))
    if isinstance(step_status,basestring):
        for name in zip(step_name,step_reason,step_status):
            ListAll.append((name[0].strip(),name[1].strip(),step_status))
    print ListAll
    Conn=GetConnection()
    query="select step_id from test_steps where tc_id='%s'" %test_case_id
    test_step_sequence_list=DB.GetData(Conn,query)
    print test_step_sequence_list
    Refined_List=[]
    for each in test_step_sequence_list:
        query="select stepname from test_steps_list where step_id='%s'" %each
        stepName=DB.GetData(Conn,query,False)
        for each in ListAll:
            if each[0]==stepName[0][0]:
                Refined_List.append(each)
                break
    return Refined_List

def update_runid(run_id,test_case_id):
    oConn=GetConnection()
    squery="select distinct status from test_case_results where run_id='%s'" %run_id
    run_id_status=DB.GetData(oConn, squery)
    submit_count=0
    count=0
    progress=0
    for each in run_id_status:
        if each=='Submitted':
            submit_count+=1
        elif each=='In-Progress':
            progress+=1
        else:
            count+=1
    Dict={}
    Dict1={}
    if progress==0 and submit_count==0 and count==len(run_id_status):
        status='Complete'
        endtime=DB.GetData(oConn,"select current_timestamp",False)
        Dict.update({'testendtime':str(endtime[0][0])})
    elif progress>0 or submit_count>0:
        status='In-Progress'
        Dict.update({'status':status})
    else:
        if count==0 and progress==0 and submit_count==len(run_id_status):
            status='Submitted'
            starttime=DB.GetData(oConn,"select current_timestamp",False)
            endtime=""
            Dict.update({'testendtime':endtime,'teststartime':str(starttime[0][0])})
    sWhereQuery="where run_id='%s'" %run_id

    Dict1.update({'status':status})
    print DB.UpdateRecordInTable(oConn, "test_run_env", sWhereQuery,**Dict1)
    print DB.UpdateRecordInTable(oConn, "test_env_results", sWhereQuery,**Dict)
    print DB.UpdateRecordInTable(oConn, "test_env_results", sWhereQuery,**Dict1)
def UpdateTestStepStatus(List,run_id,test_case_id,test_case_status,failReason):
    for each in List:
        print each
        query="select step_id from test_steps_list where stepname='%s'" %each[0].strip()
        Conn=GetConnection()
        step_id=DB.GetData(Conn, query, False)
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
def UpdateData(request):
    if request.is_ajax():
        if request.method=='GET':
            step_name=request.GET.get(u'step_name','').split("|")
            step_status=request.GET.get(u'step_status','').split("|")
            step_reason=request.GET.get(u'step_reason','').split("|")
            run_id=request.GET.get(u'run_id','')
            test_case_id=request.GET.get(u'test_case_id','')
            if(len(step_status)==1):
                Refined_List=Make_List(step_name, step_reason, step_status[0], test_case_id)
            else:
                Refined_List=Make_List(step_name, step_reason, step_status, test_case_id)
            print step_name
            print step_reason
            print step_status
            print run_id
            print test_case_id
            step_sequence=[]
            FailReason=[]
            for each in Refined_List:
                step_sequence.append(each[2])
                FailReason.append(each[1])
            print step_sequence
            failReason=""
            found="No-Status"
            index=1
            for each in step_sequence:
                if each=='In-Progress' or each=='Submitted' or each=='Failed':
                    found=each
                    break
                else:
                    index+=1
            if found=="No-Status":
                pass_count=0
                skipped_count=0
                for each in step_sequence:
                    if each=='Passed':
                        pass_count+=1
                    if each=='Skipped':
                        skipped_count+=1
                if (pass_count+skipped_count)==len(step_sequence) or skipped_count==0:
                    test_case_status='Passed'
                    #failReason=""
                if skipped_count==len(step_sequence) and pass_count==0:
                    test_case_status='Skipped'
            else:
                if found!='Submitted':
                    test_case_status=found
                    if found!='Failed':
                        rest_step_status='Submitted'
                        #failReason=""
                    else:
                        rest_step_status='Skipped'
                        failReason=Refined_List[index-1][1]
                else:
                    if found=='Submitted' and index==1:
                        test_case_status='Submitted'
                        rest_step_status='Submitted'
                    else:
                        test_case_status='In-Progress'
                        rest_step_status='Submitted'
            print test_case_status
            if test_case_status=='Failed':
                datasetid=test_case_id+'_s'+str(index)
                query="select description from master_data where field='verification' and value='point' and id='%s'"%datasetid
                Conn=GetConnection()
                verification=DB.GetData(Conn,query,False)
                if verification[0][0]=="no":
                    test_case_status='Blocked'
                else:
                    test_case_status='Failed'
                print test_case_status
            for each in range(index,len(step_sequence)):
                step_sequence[each]=rest_step_status
                FailReason[each]=""
                print step_sequence
            index=0
            Final_List=[]
            for each in zip(step_sequence,FailReason):
                temp=list(Refined_List[index])
                temp[2]=each[0]
                temp[1]=each[1]
                temp=tuple(temp)
                Final_List.append(temp)
                index+=1
            print Final_List
            message=UpdateTestStepStatus(Final_List,run_id,test_case_id,test_case_status,failReason)
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')
def GetOS(request):
    if request.is_ajax():
        if request.method=='GET':
            Conn=GetConnection()
            name=request.GET.get(u'os','')
            refined_list=[]
            ostype='OS'
            if name=='':
                query="select distinct value from config_values where type='%s'" %ostype
                os_list=DB.GetData(Conn,query,False)
                for each in os_list:
                    query="select distinct value from config_values where type='%s Version'"%each[0]
                    os_verison=DB.GetData(Conn,query)
                    temp=[]
                    temp.append(each[0])
                    temp.append(os_verison)
                    temp=tuple(temp)
                    refined_list.append(temp)
                browser_data=[]
                browsertype='Browser'
                query="select value from config_values where type='%s'" %browsertype
                browser_list=DB.GetData(Conn,query)
                for each in browser_list:
                    temp=[]
                    query="select value from config_values where type='%s Version'"%each
                    browser=DB.GetData(Conn,query)
                    temp.append(each)
                    temp.append(browser)
                    temp=tuple(temp)
                    browser_data.append(temp)
                #Get the productVersion
                productVersion='Product Version'
                query="select value from config_values where type='%s'"%productVersion
                productVersion=DB.GetData(Conn,query)
    results={'os':refined_list,'browser':browser_data,'productVersion':productVersion}
    results=simplejson.dumps(results)
    return HttpResponse(results,mimetype='application/json')
def Auto_MachineName(request):
    if request.is_ajax():
        if request.method=='GET':
            machine_name=request.GET.get(u'term','')
            Conn=GetConnection()
            query="select user_names,user_level from permitted_user_list where user_names Ilike '%%%s%%' and user_level='Manual'"%machine_name
            machine_list=DB.GetData(Conn,query,False)
    result=simplejson.dumps(machine_list)
    return HttpResponse(result,mimetype='application/json')
def CheckMachine(request):
    if request.is_ajax():
        if request.method=='GET':
            name=request.GET.get(u'name','')
            print name
            Conn=GetConnection()
            query="select os_name,os_version,os_bit,machine_ip,client,product_version from test_run_env,permitted_user_list where user_names=tester_id and user_level='Manual' and tester_id='%s'"%name
            machine_info=DB.GetData(Conn,query,False)
            print machine_info
    result=simplejson.dumps(machine_info)
    return HttpResponse(result,mimetype='application/json')
def AddManualTestMachine(request):
    if request.is_ajax():
        if request.method=='GET':
            machine_name=request.GET.get(u'machine_name','').strip()
            os_name=request.GET.get(u'os_name','').strip()
            os_version=request.GET.get(u'os_version','').strip()
            os_bit=request.GET.get(u'os_bit','').strip()
            browser=request.GET.get(u'browser','').strip()
            browser_version=request.GET.get(u'browser_version','').strip()
            machine_ip=request.GET.get(u'machine_ip','').strip()
            product_version=request.GET.get(u'product_version','').strip()
            print machine_name
            print os_name
            print os_version
            print os_bit
            print browser
            print browser_version
            print machine_ip
            Conn=GetConnection()
            query="select count(*) from permitted_user_list where user_names='%s' and user_level='Manual'"%machine_name
            count=DB.GetData(Conn,query)
            if count[0]>0:
                #update will go here.
                print "yes"
                status = DB.GetData(Conn, "Select status from test_run_env where tester_id = '%s'" % machine_name)
                for eachitem in status:
                    if eachitem == "In-Progress":
                        DB.UpdateRecordInTable(Conn, "test_run_env", "where tester_id = '%s' and status = 'In-Progress'" % machine_name, status="Cancelled")
                        DB.UpdateRecordInTable(Conn, "test_env_results", "where tester_id = '%s' and status = 'In-Progress'" % machine_name, status="Cancelled")
                    elif eachitem == "Submitted":
                        DB.UpdateRecordInTable(Conn, "test_run_env", "where tester_id = '%s' and status = 'Submitted'" % machine_name, status="Cancelled")
                    elif eachitem == "Unassigned":
                        DB.DeleteRecord(Conn, "test_run_env", tester_id=machine_name, status='Unassigned')
                machine_os=os_name+' '+os_version+' - '+os_bit
                Client=browser+'('+browser_version+';'+os_bit+' Bit)'
                updated_time=TimeStamp("string")
                Dict={'tester_id':machine_name.strip(),'status':'Unassigned','machine_os':machine_os.strip(),'client':Client.strip(),'last_updated_time':updated_time.strip(),'os_bit':os_bit,'os_name':os_name,'os_version':os_version,'machine_ip':machine_ip,'product_version':product_version.strip()}
                tes2= DB.InsertNewRecordInToTable(Conn,"test_run_env",**Dict)
                if tes2==True:
                    message="Machine is updated successfully"
            else:
                print "none"
                #new Entry will be inserted.
                machine_os=os_name+' '+os_version+' - '+os_bit
                Client=browser+'('+browser_version+';'+os_bit+' Bit)'
                updated_time=TimeStamp("string")
                Dict={'user_names':machine_name.strip(),'user_level':'Manual','email':machine_name+'@machine.com'}
                tes1= DB.InsertNewRecordInToTable(Conn,"permitted_user_list",**Dict)
                Dict={'tester_id':machine_name.strip(),'status':'Unassigned','machine_os':machine_os.strip(),'client':Client.strip(),'last_updated_time':updated_time.strip(),'os_bit':os_bit,'os_name':os_name,'os_version':os_version,'machine_ip':machine_ip,'product_version':product_version.strip()}
                tes2= DB.InsertNewRecordInToTable(Conn,"test_run_env",**Dict)
                if(tes1==True and tes2==True):
                    message="Machine Successfully Registered"
                else:
                    message="Machine is not registered successfully"
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')    
def chartDraw(request):
    if request.is_ajax():
        if request.method=='GET':
            run_id=request.GET.get(u'runid','')
            print run_id
            Conn=GetConnection()
            list=[]
            total_query="select count(*) from test_case_results where run_id='%s'"%run_id
            total=DB.GetData(Conn,total_query)
            list.append(total[0])
            pass_query="select count(*) from test_case_results where run_id='%s' and status='Passed'"%run_id
            passed=DB.GetData(Conn,pass_query)
            list.append(passed[0])
            fail_query="select count(*) from test_case_results where run_id='%s' and status='Failed'"%run_id
            fail=DB.GetData(Conn,fail_query)
            list.append(fail[0])
            blocked_query="select count(*) from test_case_results where run_id='%s' and status='Blocked'"%run_id
            blocked=DB.GetData(Conn,blocked_query)
            list.append(blocked[0])
            progress_query="select count(*) from test_case_results where run_id='%s' and status='In-Progress'"%run_id
            progress=DB.GetData(Conn,progress_query)
            list.append(progress[0])
            submitted_query="select count(*) from test_case_results where run_id='%s' and status='Submitted'"%run_id
            submitted=DB.GetData(Conn,submitted_query)
            list.append(submitted[0])
            skipped_query="select count(*) from test_case_results where run_id='%s' and status='Skipped'"%run_id
            skipped=DB.GetData(Conn,skipped_query)
            list.append(skipped[0])
    result=simplejson.dumps(list)
    return HttpResponse(result,mimetype='application/json')

def ReRun(request):
    if request.is_ajax():
        if request.method=='GET':
            run_id=request.GET.get(u'RunID','')
            status_name=request.GET.get(u'status','').split(',')
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
            Conn=GetConnection()
            """if len(status)==0:
                query="select tc.tc_id,tc.tc_name,tcr.status from test_cases tc,test_case_results tcr where tc.tc_id=tcr.tc_id and run_id='%s'"%run_id
                tc_list=DB.GetData(Conn, query,False)
                test_case_list=Modify(tc_list)
                print test_case_list
            else:"""
            tc_list=[]
            for each in status_name:
                query="select tc.tc_id,tc.tc_name,tcr.status from test_cases tc,test_case_results tcr where tc.tc_id=tcr.tc_id and tcr.run_id='%s' and tcr.status='%s'"%(run_id,each)
                get_list=DB.GetData(Conn,query,False)
                for eachitem in get_list:
                    tc_list.append(eachitem)
            print tc_list
            tc_list=list(set(tc_list))
            test_case_list=Modify(tc_list)
            print test_case_list
        print test_case_list    
        Column=['Test Case ID','Test Case Name','Type','Status']
    result={'col':Column,'list':test_case_list}
    result=simplejson.dumps(result)
    return HttpResponse(result,mimetype='application/json')       

def LoginPage(request):
    return render_to_response('login.html',{},context_instance=RequestContext(request))

"""def ProcessLogin(request):
    from django.contrib.auth.models import User
    from django.http import HttpResponse
    import AuthBackEnd
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        print username
        print password
        if AuthBackEnd.Get_User(username):
            user=AuthBackEnd.authenticate_user(username=username,password=password)
        print user
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/Home/')
            else:
                return HttpResponse("User Disabled")
        else:    
            return HttpResponse("User not present")
        
def checkusername(request):
    from django.contrib.auth.models import User
    from django.http import HttpResponse
    username = request.GET.get(u'username', '')
    if username:
        u = User.objects.filter(username=username).count()
        if u != 0:
            res = "Already In Use"
        else:
            res = "OK"
    else:
        res = ""

    return HttpResponse('%s' % res)"""

def User_Login(request):
    
    if request.is_ajax() and request.method=='GET':
        username=request.GET.get[u'username','']
        password=request.GET.get[u'password','']
    
    Conn = GetConnection()
    
    user = DB.GetData(Conn,"select full_name from user_info where username='"+username+"' and password='"+password+"'")
    if(len(user)==1):
        message = "User Logged In"
    else:
        message = "User Not Found"
        
    result=simplejson.dumps(message)
    return HttpResponse(result,mimetype='application/json')

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
    Conn=GetConnection()
    if request.is_ajax():
        if request.method=='GET':
            section=request.GET.get(u'section','')
            if section=="":
                query="select distinct subpath(section_path,0,1) from product_sections"
                section_path=DB.GetData(Conn,query)
    result=simplejson.dumps(section_path)
    return HttpResponse(result,mimetype='application/json')
##########MileStone Code####################
def AutoMileStone(request):
    if request.is_ajax():
        if request.method=='GET':
            Conn=GetConnection()
            milestone=request.GET.get(u'term','')
            print milestone
            query="select value,type from config_values where type='milestone' and value ilike'%%%s%%'"%milestone
            milestone_list=DB.GetData(Conn,query,False)
    result=simplejson.dumps(milestone_list)
    return HttpResponse(result,mimetype='application/json')
def MileStoneOperation(request):
    if request.is_ajax():
        if request.method=='GET':
            Conn=GetConnection()
            operation=request.GET.get(u'operation','')
            confirm_message=""
            error_message=""
            if operation=="2":
                new_name=request.GET.get(u'new_name','')
                old_name=request.GET.get(u'old_name','')
                old_name=old_name.strip()
                query="select count(*) from config_values where type='milestone' and value='%s'"%old_name
                available=DB.GetData(Conn,query)
                if(available[0]>0):
                    #check if old name is given again:
                    againQuery="select count(*) from config_values where type='milestone' and value='%s'"%new_name
                    again=DB.GetData(Conn,againQuery)
                    if(again[0]>0):
                        error_message="MileStone already exists,can't rename"
                    else:
                        #start Rename Operation
                        condition="where type='milestone' and value='%s'"%old_name
                        Dict={'value':new_name.strip()}
                        print DB.UpdateRecordInTable(Conn, "config_values", condition,**Dict)
                        confirm_message="MileStone is renamed"
                else:
                    confirm_message="No milestone is found"
            #start Create Operation
            if operation=="1":
                new_name=request.GET.get(u'new_name','')
                new_name=new_name.strip()
                query="select count(*) from config_values where type='milestone' and value='%s'"%new_name
                available=DB.GetData(Conn,query)
                if(available[0]==0):
                    Dict={'type':'milestone','value':new_name.strip()}
                    print DB.InsertNewRecordInToTable(Conn, "config_values",**Dict)
                    confirm_message="MileStone is created Successfully"
                else:
                    error_message="MileStone name exists.Can't create a new one"
                #start Delete Operation
            if operation=="3":
                new_name=request.GET.get(u'new_name','')
                new_name=new_name.strip()
                query="select count(*) from config_values where type='milestone' and value='%s'"%new_name
                available=DB.GetData(Conn,query)
                if(available[0]>0):
                    Dict={'type':'milestone','value':new_name.strip()}
                    print DB.DeleteRecord(Conn, "config_values",**Dict)
                    confirm_message="MileStone is deleted Successfully"
                else:
                    error_message="MileStone Not Found"
    results={'confirm_message':confirm_message,
             'error_message':error_message
             }
    result=simplejson.dumps(results)
    return HttpResponse(result,mimetype='application/json')    
############################################