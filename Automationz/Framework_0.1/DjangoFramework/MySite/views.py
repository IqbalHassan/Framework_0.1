
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
#>>>>>>> 79295d8a9281fee2054c6e15061b281b41f17493

from django.template import Context
from django.template import RequestContext

from django.template.loader import get_template
from django.utils import simplejson
import json
from models import GetData, GetColumnNames, GetQueryData, GetConnection
import DataBaseUtilities as DB

from CommonUtil import TimeStamp
import itertools, operator
#import DjangoConstants
import TestCaseOperations
import re
import time
from TestCaseOperations import Cleanup_TestCase
from django.core.context_processors import csrf

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

def Search(request):
    templ = get_template('SearchResults.html')
    variables = Context({ })
    output = templ.render(variables)
    return HttpResponse(output)

def Search2(request):
    RunId = request.GET.get('ClickedRunId', '')
    if RunId != "":
        return RunId_TestCases(request)
    else:
        templ = get_template('SearchResults.html')
        variables = Context({ })
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
        templ = get_template('CreateTest.html')
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

        if Environment == "PC":
            Section = "Section"
            Test_Run_Type = "test_run_type"
            Priority = "Priority"
            TCStatusName = "Status"
            CustomTag = "CustomTag"

        results = DB.GetData(Conn, "select distinct name from test_case_tag "
                                   "where name Ilike '%" + value + "%' "
                                     "and property in('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "') "
                                     "and tc_id in (select tc_id from test_case_tag where name = '" + Environment + "' and property = 'machine_os' ) "
                                     )

        tcidresults = DB.GetData(Conn, "select distinct name || ' - ' || tc_name from test_case_tag tct,test_cases tc "
                                   "where tct.tc_id = tc.tc_id and (tct.tc_id Ilike '%" + value + "%' or tc.tc_name Ilike '%" + value + "%')"
                                     "and property in('tcid') "
                                     "and tct.tc_id in (select tc_id from test_case_tag where name = '" + Environment + "' and property = 'machine_os' ) "
                                     )

        results = list(set(results + tcidresults))

        if len(results) > 0:
            results.append("*Dev")

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

        results = DB.GetData(Conn, "Select  DISTINCT tester_id from test_run_env where status = 'Unassigned' and tester_id Ilike '%" + value + "%'")

    json = simplejson.dumps(results)
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


        results = DB.GetData(Conn, "select distinct name from test_case_tag where name Ilike '%" + value + "%' "
                                    + "and property in ('" + CustomTag + "') order by name")

        mastertags = DB.GetData(Conn, "select distinct value from config_values where type = 'tag' order by value")

        results = list(set(results + mastertags))

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def AutoCompleteTestStepSearch(request):
    Conn = GetConnection()
    results = []
    #if request.is_ajax():
    if request.method == "GET":
        value = request.GET.get(u'term', '')

        results = DB.GetData(Conn, "select stepname,data_required from test_steps_list where stepname Ilike '%" + value + "%' order by stepname", False)

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

            if Environment == "PC":
                Section = "Section"
                Test_Run_Type = "test_run_type"
                Priority = "Priority"
                TCStatusName = "Status"
                CustomTag = "CustomTag"

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
                Query = "HAVING COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "') THEN 1 END) > 0 "
                count = count + 1
            elif count >= 2:
                Query = Query + "AND COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "') THEN 1 END) > 0 "
        Query = Query + " AND COUNT(CASE WHEN name = '%s' and property = '%s' THEN 1 END) > 0 " % (TCStatusName, propertyValue)
        Query = Query + " AND COUNT(CASE WHEN property = 'machine_os' and name = '" + Environment + "' THEN 1 END) > 0"
        TableData = DB.GetData(Conn, "select distinct tct.tc_id,tc.tc_name from test_case_tag tct, test_cases tc "
                        "where tct.tc_id = tc.tc_id group by tct.tc_id,tc.tc_name " + Query, False)

    Heading = ['TestCase_ID', 'TestCase_Name']

    #results = {"Section":Section, "TestType":Test_Run_Type,"Priority":Priority}         
    results = {'Heading':Heading, 'TableData':TableData}

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
                                    "te.machine_os,"
                                    "te.machine_ip, "
                                    "te.client "
                                    "from test_env_results tr, test_run_env te where tr.run_id = te.run_id and tr.status = 'In-Progress'   and (cast (now() AS timestamp without time zone)-teststarttime ) < interval '%s day' ORDER BY tr.teststarttime DESC)"
                                    " union all "
                                    "(Select te.run_id,"
                                    "te.test_objective, "
                                    "te.tester_id,"
                                    "tr.status,"
                                    "to_char(tr.duration,'HH24:MI:SS'), "
                                    "te.product_version,"
                                    "te.machine_os,"
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

            if RunID != '':
                Result = DB.GetData(Conn, "Select stepname from test_steps tst,test_steps_list tsl where tst.step_id = tsl.step_id and tc_id  = '%s' order by teststepsequence" % RunID)

    results = {'Result':Result

               }
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def RunId_TestCases(request): #==================Returns Test Cases When User Click on Run ID On Test Result Page===============================

    Conn = GetConnection()
    results = {}
    Env_Details = ""
    Env_Details_Data = ""
    Env_Details_Col = ""
    Col = ""
    AllTestCases = ""
    Pass_TestCases = ""
    Fail_TestCases = ""
    failsteps = ""
    FailStep_TestCases = ""
    failsteps_Col = ""
    FailsStepsWithCount = ""
    if request.is_ajax():
         if request.method == 'GET':

            #If User Click on Test Case ID 
            RunId = request.GET.get('ClickedRunId', '')
            if RunId != "":
                RunId = str(RunId.strip())
                #"tr.duration",

                Env_Details = DB.GetData(Conn, "Select DISTINCT "
                                               "run_id,"
                                               "tester_id, "
                                               "product_version, "
                                               "machine_os, "
                                               "client, "
                                               "data_type "
                                               "from test_run_env "
                                               "Where run_id = '%s'" % RunId, False
                                            )
                D = list(Env_Details[0])
                for Dta in range(len(D)):
                    if D[Dta] == None:
                        D[Dta] = ""
                Env_Details_Data = (D[0], D[1], D[2], D[3], D[4], D[5])
                Env_Details_Data = [Env_Details_Data]
                Env_Details_Col = [
                                   "Run ID",
                                   "Tester",
                                   "Product",
                                   "Machine OS",
                                   "Client",
                                   "Data Type"

                                   ]
                AllTestCases = DB.GetData(Conn, "(select "
                                            "tct.name as MKSId, "
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



                Pass_TestCases = DB.GetData(Conn, "select "
                                            "tct.name as mksid, "
                                            "tc.tc_name, "
                                            "tr.status, "
                                            "to_char(tr.duration,'HH24:MI:SS'), "
                                            "tr.failreason, "
                                            "tr.logid, "
                                            "tc.tc_id "
                                            "from test_case_results tr, test_cases tc, test_case_tag tct "
                                            "where tr.run_id = '%s' and tr.status = 'Passed' and "
                                            "tr.tc_id = tc.tc_id and tc.tc_id = tct.tc_id and tct.property = 'MKS' ORDER BY tr.id" % (RunId), False)



                Fail_TestCases = DB.GetData(Conn, "select "
                                            "tct.name as mksid, "
                                            "tc.tc_name, "
                                            "tr.status, "
                                            "to_char(tr.duration,'HH24:MI:SS'), "
                                            "tr.failreason, "
                                            "tr.logid, "
                                            "tc.tc_id "
                                            "from test_case_results tr, test_cases tc, test_case_tag tct "
                                            "where tr.run_id = '%s' and tr.status = 'Failed' and "
                                            "tr.tc_id = tc.tc_id and tc.tc_id = tct.tc_id and tct.property = 'MKS' ORDER BY tr.id" % RunId, False)



                Col = ['MKS ID', 'Test Case', 'Status', 'Duration', 'Fail Reason', 'Test Log', 'Automation ID']


                failsteps = DB.GetData(Conn, "select DISTINCT tsl.stepname from test_case_results tr, test_step_results tsr, test_steps_list tsl, test_cases tc "

                          "where tr.run_id = '%s' and tr.status = 'Failed' and tr.run_id = tsr.run_id and tr.tc_id = tsr.tc_id "

                           "and tsr.status = 'Critical' and tsr.teststep_id = tsl.step_id and tr.tc_id = tc.tc_id" % RunId, False
                    )

                #Adding Test Case Count with Fails Steps Name
                FailsStepsWithCount = []
                for eachstep in failsteps:
                    failstep = list(eachstep)[0]
                    FailStep_TestCases = DB.GetData(Conn, "select tc.tc_name from test_case_results tr, test_step_results tsr, test_steps_list tsl, test_cases tc "
                                                "where tr.run_id = '%s' and tr.status = 'Failed' and tr.run_id = tsr.run_id "
                                                "and tr.tc_id = tsr.tc_id and tsr.status in ('Critical') and tsr.teststep_id = tsl.step_id "
                                                "and tr.tc_id = tc.tc_id and tsl.stepname = '%s' " % (RunId, failstep)
                                            )
                    Count = len(FailStep_TestCases)
                    L = []
                    L.append("%s (%s)" % (failstep, Count))
                    FailsStepsWithCount.append(L)

                failsteps_Col = ["Step Name"]




                results = {
                           'Env_Details_Data':Env_Details_Data,
                           'Env_Details_Col':Env_Details_Col,
                           'Column':Col,
                           'AllTestCases':AllTestCases,
                           'Pass':Pass_TestCases,
                           'Fail':Fail_TestCases,
                           'failsteps':FailsStepsWithCount,
                           'failsteps_Col':failsteps_Col
                           }
                json = simplejson.dumps(results)
                return HttpResponse(json, mimetype='application/json')


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


                TestCase_Detail_Data = DB.GetData(Conn, "(select "
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

#                DB.GetData(Conn,"Select    "
#                                                        "tl.stepname,"
#                                                        " tr.status, "
#                                                        "to_char(tr.duration,'HH24:MI:SS'), "
#                                                        " tr.memory_consumed " 
#                                   "from  test_step_results tr, test_cases tc, test_steps_list tl  where tr.run_id = '%s' and tc.tc_id = '%s' " 
#                                   "and tc.tc_id = tr.tc_id and tr.teststep_id = tl.step_id " 
#                                   "ORDER BY tr.stepstarttime ASC" % (RunId, TC_ID),False
#                              )

                TestCase_Detail_Col = ['Test Step Name', 'Status', 'Duration', 'Memory Usage']

    results = {
               'TestCase_Detail_Data':TestCase_Detail_Data,
               'TestCase_Detail_Col' :TestCase_Detail_Col

               }
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def TestStep_Detail_Table(request): #==================Returns Test Step Details Table When User Click on Test Step Name On Test Result Page=======
    Conn = GetConnection()
    results = {}
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

                TestCaseId = DB.GetData(Conn, "Select tc_id from test_cases where tc_name = '%s'" % TestCaseName)
                TestCaseId = str(TestCaseId[0])

                StepSeqId = DB.GetData(Conn, "Select tst.teststepsequence "
                                            " from test_steps tst,test_steps_list tsl "
                                            " where tc_id = '%s' and "
                                            "tst.step_id = tsl.step_id "
                                            "order by teststepsequence" % (TestCaseId)
                                        )
                TestStepSeqId = str(StepSeqId[TestStepSeqId - 1])
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
    results = {

               'TestStep_Details':TestStep_Details,
               'TestStep_Col':TestStep_Col,

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
                                                 "and tr.tc_id = tsr.tc_id and tsr.status in ('Critical') and tsr.teststep_id = tsl.step_id "
                                                 "and tr.tc_id = tc.tc_id and tc.tc_id = tct.tc_id and tct.property = 'MKS' and tsl.stepname = '%s' "
                                                 "order by tr.id " % (RunId, FailStep), False
                                                 )

#                DB.GetData(Conn,"select tc.tc_name, "
#                                                      "tr.status, "
#                                                      "to_char(tr.duration,'HH24:MI:SS'), "
#                                                      "tr.failreason, "
#                                                      "tr.logid from test_case_results tr, test_step_results tsr, test_steps_list tsl, test_cases tc "
#                                "where tr.run_id = '%s' and tr.status = 'Failed' and tr.run_id = tsr.run_id " 
#                                "and tr.tc_id = tsr.tc_id and tsr.status in ('Critical') and tsr.teststep_id = tsl.step_id " 
#                                "and tr.tc_id = tc.tc_id and tsl.stepname = '%s' " % (RunId,FailStep), False
#                            )
                FailStep_TC_Col = ['MKS ID', 'Failed Test Case', 'Status', 'Duration', 'Fail Reason', 'Test Log', 'Autmation ID']
    results = {
               'FailStep_TestCases':FailStep_TestCases,
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
                Query = "HAVING COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "') THEN 1 END) > 0 "
                count = count + 1
            elif count >= 2:
                Query = Query + "AND COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "') THEN 1 END) > 0 "
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

            if UserData == "True":

                tabledata = DB.GetData(Conn, "Select  tester_id,machine_os,client,last_updated_time,machine_ip from test_run_env where status = 'Unassigned' and machine_os ilike '%" + Environment + "%'", False)
                Heading = ["Tester ID", "Machine OS", "Client", "Last Updated Time", "Machine IP"]
                #Heading.reverse()
    results = {'Heading':Heading, 'TableData':tabledata}
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

            DependencyText = request.GET.get('DependencyText', '')
            DependencyText = str(DependencyText.replace(u'\xa0', u''))

            TestDataType = request.GET.get('TestDataType', '')
            TestDataType = str(TestDataType.replace(u'\xa0', u''))

            TestObjective = request.GET.get('TestObjective', '')
            TestObjective = str(TestObjective.replace(u'\xa0', u''))

            Environment = request.GET.get(u'Env', '')
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

            UserText = UserData.split(":");
            EmailIds = EmailIds.split(":")
            DependencyText = DependencyText.split(":")
            Emails = []
            for eachitem in EmailIds :
                if eachitem != "":
                    Eid = DB.GetData(Conn, "Select email from permitted_user_list where user_names = '%s'" % str(eachitem))
                if len(Eid) > 0:
                    Emails.append(Eid[0])


            stEmailIds = ','.join(Emails)

            for eachitem in UserText:
                if len(eachitem) != 0 and  len(eachitem) != 1:
                    QueryText.append(str(eachitem.strip()))

    if "*Dev" in QueryText:
        QueryText.remove("*Dev")
        propertyValue = "Dev"

    TesterId = QueryText.pop() # pop function will remove last item of the list (userid) and will assign to Testerid

    #Creating Runid and assigning test cases to it in "testrun" table
    runid = TimeStamp("string")
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
                Query = "HAVING COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "') THEN 1 END) > 0 "
                count = count + 1
            elif count >= 2:
                #Query = Query + "AND COUNT(CASE WHEN name = '%s' THEN 1 END) > 0 " %eachitem
                Query = Query + "AND COUNT(CASE WHEN name = '" + eachitem + "' and property in ('" + Section + "','" + CustomTag + "','" + Test_Run_Type + "','" + Priority + "') THEN 1 END) > 0 "
        Query = Query + " AND COUNT(CASE WHEN name = '%s' and property = '%s' THEN 1 END) > 0" % (TCStatusName, propertyValue)
        Query = Query + " AND COUNT(CASE WHEN property = 'machine_os' and name = '" + Environment + "' THEN 1 END) > 0"
        TestCasesIDs = DB.GetData(Conn, "select distinct tct.tc_id from test_case_tag tct, test_cases tc "
                "where tct.tc_id = tc.tc_id group by tct.tc_id,tc.tc_name " + Query)

    for eachitem in TestCasesIDs:
        Dict = {'run_id':runid, 'tc_id':str(eachitem)}
        Result = DB.InsertNewRecordInToTable(Conn, "test_run", **Dict)

    #Finding Client info from TestRenEnv for selected machine
    ClientInfo = DB.GetData(Conn, "Select client from test_run_env Where  tester_id = '%s' and status = 'Unassigned' " % TesterId)
    ClientInfo = ClientInfo[0].split(",")
    #Adding tag values to "testrunevn" table columns
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
            if eachitem in iclient:
                eachitem = iclient

        if TagName == Section or TagName == CustomTag or TagName == Priority or TagName == 'tcid':
            query = "Where  tester_id = '%s' and status = 'Unassigned' " % TesterId
            TestSetName = TestSetName + " " + eachitem
            TestSetName = TestSetName.strip()
            Dict = {'run_id':runid, 'rundescription': TestSetName}
        else:
            query = "Where  tester_id = '%s' and status = 'Unassigned' " % TesterId
            TestSetName = TestSetName + " " + eachitem
            TestSetName = TestSetName.strip()
            Dict = {'run_id':runid, 'rundescription': TestSetName , '%s' % (TagName) : '%s' % (eachitem)}
        Result = DB.UpdateRecordInTable(Conn, "test_run_env", query , **Dict)
    Result = DB.UpdateRecordInTable(Conn, "test_run_env", query,
                                     email_notification=stEmailIds,
                                     test_objective=TestObjective,
                                     Status='Submitted',
                                     data_type=TestDataType
                                     )
    #NJ-Insert into run env results to display submitted runs
    now = DB.GetData(Conn, "SELECT CURRENT_TIMESTAMP;", False)
    sTestSetStartTime = str(now[0][0])
    print sTestSetStartTime

    Dict = {'run_id':runid, 'tester_id':str(TesterId), 'status': 'Submitted', 'rundescription':TestObjective, 'teststarttime':sTestSetStartTime}
    EnvResults = DB.InsertNewRecordInToTable(Conn, "test_env_results", **Dict)
#    Result = DB.UpdateRecordInTable(Conn, "test_run_env", query, test_objective = TestObjective  )
#    Result = DB.UpdateRecordInTable(Conn, "test_run_env", query , Status = 'Submitted' ) 

    results = {'Result': Result }

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

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
        results = DB.GetData(Conn, "Select DISTINCT tc_id from test_cases")
        results = DB.GetData(Conn, "Select  DISTINCT tc_id from test_cases where tc_id Ilike '%" + value + "%'")


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

def TestCase_ParseData(temp, Steps_Name_List):
    Steps_Data_List = []
    # s = step # d = data # t = tuple # a = address
    d = 0
    index = -1
    for name in Steps_Name_List:
        #init step array
        Steps_Data_List.insert(d, (name.strip(), []))

        index = Steps_Name_List.index(name, index + 1)
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
            Status = request.GET.get(u'Status', 'Dev')
            Is_Edit = request.GET.get(u'Is_Edit', 'create')
            Section_Path = request.GET.get(u'Section_Path', '')
            Steps_Data_List = TestCase_ParseData(temp, Steps_Name_List)

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
            test_case_step_details = DB.GetData(Conn, "select ts.step_id,stepname,teststepsequence,data_required from test_steps ts, test_steps_list tsl where ts.step_id = tsl.step_id and tc_id = '%s' order by teststepsequence" % TC_Id, False)
            for each_test_step in test_case_step_details:
                Step_Id = each_test_step[0]
                Step_Name = each_test_step[1]
                Step_Seq = each_test_step[2]
                Step_Data = []
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
                Steps_Data_List.append((Step_Name, Step_Data))

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
            Steps_Data_List = TestCase_ParseData(temp, Steps_Name_List)
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

    results = {'ReportTable':ReportTable, 'DefectTable': DefectTable}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

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
        results = DB.GetData(Conn, "select  value from config_values where value Ilike '%" + value + "%' and type='"+data_type+"'")
        #test_tag=DB.GetData(Conn,"")
        #results=list(set(results+test_tag))
        if len(results) > 0:
            results.append("*Dev")
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
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
        if data_type=="tag":
            return general_work(request,data_type)
        if data_type=="set":
            return general_work(request,data_type)
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
        operation=request.POST['operation']
        command=request.POST['submit_button']
        if operation=="2" and command=="Rename":
            temp=Check_instance('inputName',data_type)
            if(temp==0):
                if request.POST['inputName']!="":
                    output="no such test "+data_type+ " with name '"+request.POST['inputName']+"'"
                    return TestSet(request,output)
                else:
                    output="Name field is empty"
                    return TestSet(request,output)
            if(temp>0):
                first_name=request.POST['inputName']
                second_name=request.POST['inputName2']
                if(first_name!="" and second_name!=""):
                    return rename(request,first_name,second_name,data_type)
                else:
                    output="Name field is empty"
                    return TestSet(request,output)
        if operation=="1" and command=="Create":
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
        if operation=="3" and command=="Edit":
            temp=Check_instance('inputName',data_type)
            if(temp>0):
                name=request.POST['inputName']
                if(name!=""):
                    return edit(request,name,data_type)
                else:
                    output="Name field is empty"
                    return TestSet(request,output)    
            # output+=edit(name)
        if operation=="4" and command=="Delete":
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
            #output+=delete(name)
    #return output
def TestCases_InSet(name,data_type):
    conn=GetConnection()
    result=DB.GetData(conn,"select tc_id,tc_name from test_cases where tc_id in (select tc_id from test_case_tag where name='"+name+"' and property='"+data_type+"')",False)
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
            ex_lst=TestCases_InSet(test_set_name)
            output={}
            output.update({'ex_lst':ex_lst})
            output.update({'error_message':"No check box selected",'name':test_set_name,'type':test_type})
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
            ex_lst=TestCases_InSet(test_set_name)
            output={}
            output.update({'ex_lst':ex_lst})
            output.update({'error_message':"No check box selected",'name':test_set_name,'type':test_type})
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
        results = DB.GetData(Conn, "select  distinct value from config_values where value Ilike '%" + value + "%' and type='feature'")
        if len(results)>0:
            results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def TestDriver_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct value from config_values where value Ilike '%" + value + "%' and type='driver'")
        if len(results)>0:
            results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def TestStep_Auto(request):
    Conn = GetConnection()
    results = []
    if request.method == "GET":
        value = request.GET.get(u'term', '')
        results = DB.GetData(Conn, "select  distinct stepname from test_steps_list where stepname Ilike '%" + value + "%'")
        if len(results)>0:
            results.append("*Dev")
    json=simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def TestCase_Results(request):
    conn=GetConnection()
    TableData = []
    if request.is_ajax():
        if request.method == 'GET':
            UserData = request.GET.get(u'Query', '')
            sQuery="select tc_id,tc_name from test_cases where tc_id in (SELECT distinct tc_id FROM test_steps where step_id=(SELECT distinct step_id FROM test_steps_list WHERE stepname='"+UserData+"'))"
            TableData=DB.GetData(conn, sQuery, False)
    Heading = ['TestCase_ID', 'TestCase_Name']
    results = {'Heading':Heading, 'TableData':TableData}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

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
        if step_name!="" and step_desc!="" and step_feature!="" and step_data!="0":
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
                    query = "Where  stepname = '"+step_name+"'"
                    testrunenv=DB.UpdateRecordInTable(conn, "test_steps_list",query,description=step_desc,data_required=data,steptype=s_type,driver=step_driver,stepfeature=step_feature)
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
                    testrunenv=DB.InsertNewRecordInToTable(conn, "test_steps_list",stepname=step_name,description=step_desc,data_required=data,steptype=s_type,driver=step_driver,stepfeature=step_feature)
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