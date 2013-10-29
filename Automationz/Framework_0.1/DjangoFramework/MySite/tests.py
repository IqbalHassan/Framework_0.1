# Create your views here.
import datetime
import json
import time

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils import simplejson

import DataBaseUtilities as DB
from models import GetConnection


#from django.shortcuts import render_to_response
#from django.template import RequestContext
#from CommonUtil import GetLocalOS,GetRegistryValue,TimeStamp,GetLocalUser
#import DjangoConstants
#import os
#import FileUtilities as FL
#import MKS_Report 
Conn = GetConnection()
tabledata = []
UserData = ""
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
                            "from test_env_results tr, test_run_env te where tr.run_id = te.run_id and tr.status = 'In-Progress'  and (cast (now() AS timestamp without time zone)-teststarttime ) < interval '%s day' ORDER BY tr.teststarttime DESC)"
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

print results
