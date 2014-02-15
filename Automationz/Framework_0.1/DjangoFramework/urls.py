from django.conf.urls import *

import settings, os
from MySite.views import *
site_media = os.path.join(os.path.dirname(__file__),'site_media')

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    
    #Home Page
	url(r'^$', HomePage),
    url(r'^Home/$',HomePage),
    
    
    #Result Page
    #url(r'^Home/Search/$',Search),
    url(r'^Home/Results/$',ResultPage),
    url(r'^Home/RunID/(?P<Run_Id>[^/]*)/$',Search2),
    url(r'^Home/RunID/(?P<Run_Id>[^/]*)/TC/(?P<TC_Id>[^/]*)/$',RunIDTestCases),
    url(r'^Home/.*/DataFetchForTestCases/$',DataFetchForTestCases),
    url(r'^Home/.*/TestDataFetch/$',TestDataFetch),
    url(r'^Home/.*/UpdateData/$',UpdateData),
    url(r'^Home/.*/LogFetch/$',LogFetch),
    url(r'^Home/.*/ResultTableFetch/$',ResultTableFetch),
    url(r'^Home/.*/RunIDStatus/$',RunIDStatus),
    #url(r'^Home/.*/RunIDFailReason/$',RunIDFailReason),
    #url(r'^Home/.*/UpdateFailReason/$',UpdateFailReason),
    #url(r'^Home/.*/Edit/$',RunIDEdit),
    url(r'^Home/RunID/$',ExceptionSearch),
    url(r'^Home/.*/AutoCompleteTestCasesSearch/$', AutoCompleteTestCasesSearch),
    url(r'^Home/.*/AutoCompleteUsersSearch/$', AutoCompleteUsersSearch),
    url(r'^Home/.*/AutoCompleteEmailSearch/$', AutoCompleteEmailSearch),
    url(r'^Home/.*/AutoCompleteTesterSearch/$',AutoCompleteTesterSearch),
    url(r'^Home/.*/Table_Data_TestCases/$', Table_Data_TestCases),
    url(r'^Home/.*/Table_Data_TestResult/$', Table_Data_TestResult), 
    url(r'^Home/.*/RunId_TestCases/$', RunId_TestCases),
    url(r'^Home/.*/FailStep_TestCases/$', FailStep_TestCases),
    url(r'^Home/.*/TestCase_TestSteps/$', TestCase_TestSteps),
    url(r'^Home/.*/TestCase_TestSteps_SearchPage/$', TestCase_TestSteps_SearchPage),
    url(r'^Home/.*/TestCase_Detail_Table/$', TestCase_Detail_Table),
    url(r'^Home/.*/TestStep_Detail_Table/$', TestStep_Detail_Table),
    url(r'^Home/.*/createTablefromString/$', createTablefromString),
    
    #Create Test
    url(r'^Home/ManageTestCases/$',ManageTestCases),
    url(r'^Home/ManageTestCases/CreateProductSections/$', CreateProductSections),
    url(r'^Home/ManageTestCases/CreateProductSections/ProductSectionsCreated/$', ProductSectionsCreated),
    url(r'^Home/ManageTestCases/Create/[^/]*$',Create),
    url(r'^Home/ManageTestCases/Edit/Edit_TestCase$', EditTestCase),
    url(r'^Home/ManageTestCases/Edit/[^/]*$',Edit),
    url(r'^Home/ManageTestCases/Edit/AutoCompleteTagSearch/$', AutoCompleteTagSearch),
    url(r'^Home/ManageTestCases/Edit/AutoCompleteTestStepSearch/$', AutoCompleteTestStepSearch),
    
    url(r'^Home/ManageTestCases/CreateNew/[^/]*$',CreateNew),
    #url(r'^Home/.*/TestCase_EditData/$', ViewTestCase),
    url(r'^Home/ManageTestCases/SearchEdit/$',SearchEdit),
    url(r'^Home/ManageTestCases/Create/AutoCompleteTagSearch/$', AutoCompleteTagSearch),
    url(r'^Home/ManageTestCases/Create/AutoCompleteTestStepSearch/$', AutoCompleteTestStepSearch),
    url(r'^Home/ManageTestCases/Create/Submit_New_TestCase/$', Create_Submit_New_TestCase),
    url(r'^Home/.*/GetSections/$', Get_Sections),
    url(r'^Home/.*/GetSubSections/$', Get_SubSections),
    url(r'^Home/.*/GetBrowsers/$', Get_Browsers),
    url(r'^Home/.*/GetVersions/$', Get_Versions),
    url(r'^Home/ManageTestCases/DeleteExisting/$', DeleteExisting),
    #Test Set Management Section
    url(r'^Home/ManageTestCases/TestSet/$', TestSet),
    url(r'^Home/.*/TestSet_Auto/$',TestSet_Auto),
    url(r'^Home/.*/TestTag_Auto/$',TestTag_Auto),
    url(r'^Home/.*/TestCase_Auto/$',TestCase_Auto),
    url(r'^Home/ManageTestCases/TestSet/Process/$',Data_Process),
    url(r'^Home/ManageTestCases/TestSet/AddTestCase/$', AddTestCasesToSet),
    url(r'^Home/ManageTestCases/TestSet/DeleteTestCase/$', DeleteTestCasesFromSet),
    #Test Step Management Section
    url(r'^Home/ManageTestCases/TestStep/$',TestStep),
    url(r'^Home/.*/TestStep_Auto/$',TestStep_Auto),
    url(r'^Home/.*/TestFeature_Auto/$',TestFeature_Auto),
    url(r'^Home/.*/TestDriver_Auto/$',TestDriver_Auto),
    url(r'^Home/.*/TestFeatureDriver_Auto/$',TestFeatureDriver_Auto),
    url(r'^Home/.*/TestCase_Results/$',TestCase_Results),
    url(r'^Home/.*/TestSteps_Results/$',TestSteps_Results),
    url(r'^Home/.*/Populate_info_div/$',Populate_info_div),
    url(r'^Home/.*/TestStep_Delete/$',TestStep_Delete),
    url(r'^Home/.*/FeatureDriver_Delete/$',FeatureDriver_Delete),
    url(r'^Home/ManageTestCases/FeatureDriverDelete/$',FeatureDriverDelete),
    url(r'^Home/ManageTestCases/TestStepDelete/$',TestStepDelete),
    url(r'^Home/ManageTestCases/Process_TestStep/$',Process_TestStep),
    url(r'^Home/ManageTestCases/Process_FeatureDriver/$',Process_FeatureDriver),
    url(r'^Home/.*/TestStepAutoComplete/$',TestStepAutoComplete),
    url(r'^Home/.*/TestStep_TestCases/$',TestStep_TestCases),
    url(r'^Home/.*/TestStepWithTypeInTable/$',TestStepWithTypeInTable),
    #Run Test Page
    url(r'^Home/RunTest/$',RunTest),
    url(r'^Home/.*/Verify_Query/$', Verify_Query),
    url(r'^Home/.*/Run_Test/$', Run_Test),
    url(r'^Home/.*/ReRun_Fail_TestCases/$', ReRun_Fail_TestCases),
    url(r'^Home/.*/Table_Data_UserList/$', Table_Data_UserList), 
    url(r'^Home/.*/Auto_MachineName/$',Auto_MachineName),
    url(r'Home/.*/CheckMachine/$',CheckMachine),
    url(r'^Home/.*/AddManualTestMachine/$',AddManualTestMachine),
    url(r'^Home/.*/GetOS/$',GetOS),
    url(r'^Home/.*/chartDraw/$',chartDraw),
    #Performance Page
    url(r'^Home/Performance/$',Performance),
    url(r'^Home/Performance/PerformanceResult/$',PerformanceResult), 
    url(r'^Home/.*/Performance_ClickedBundle_Details_(?P<type>.)/$',Performance_ClickedBundle_Details),
    #url(r'^Home/PerformanceGraph_Window/$',PerformanceGraph_Window),
    
    
    #Daily Build Page
    url(r'^Home/DailyBuildResults/$',Daily_Build),
    url(r'^Home/.*/Table_Data_DailyBuild/$',Table_Data_DailyBuild),
    
    #MKS Report Page
    url(r'^Home/MKS-Report/$',MKSReport),
    url(r'^Home/.*/MKS_Report_Table/$', MKS_Report_Table),
    
    
    #Analysis Page
    url(r'^Home/Analysis/$', Analysis),
    url(r'^Home/.*/TestCaseSearch/$', TestCaseSearch),
    url(r'^Home/.*/Selected_TestCaseID_Analaysis/$', Selected_TestCaseID_Analaysis),
    
    #Execution Report Page
    url(r'^Home/ExecutionReport/$',ExecutionReport),
    url(r'^Home/.*/Execution_Report_Table/$', Execution_Report_Table),
    
    #Test Type Status Page                                #minar09
    url(r'^Home/TestTypeStatus/$', TestTypeStatus),
    url(r'^Home/.*/TestTypeStatus_Report/$',TestTypeStatus_Report),
    
    #Bundle Report Page                                #minar09
    url(r'^Home/BundleReport/$', BundleReport),
    url(r'^Home/.*/BundleReport_Table/$',BundleReport_Table),
    url(r'^Home/.*/Bundle_Report/$',Bundle_Report),
    #url(r'^Home/.*/Single_Env/$',Single_Env),
    
    #Documentation Page
    url(r'^Home/Documentation/$',Documentation),
    
    #Admin Page
    url(r'^Home/Admin/$',Admin),
    url(r'^Home/.*/Process_Git/$',Process_Git),
    
    
    
    
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
    
)


