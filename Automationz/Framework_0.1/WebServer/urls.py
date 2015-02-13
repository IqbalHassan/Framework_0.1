import os

from django.conf.urls import *  # @UnusedWildImport 
import urls_direct
from MySite.views import *  # @UnusedWildImport
from MySite.views import select2

site_media = os.path.join(os.path.dirname(__file__), 'site_media')

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Home Page
	url(r'^$', HomePage),
    url(r'^Home/$', HomePage),
    url(r'^Home/Dashboard/$', HomePage),
    #url(r'^Home/User/(?P<user_id>[^/]+)/*(?P<success>[A-Za-z]+)*/$',GetProfileInfo),
    url(r'^Home/User/$',AccountInfo),
    url(r'^GetProjectNameForTopBar/$',GetProjectNameForTopBar),
    url(r'^Home/.*/GetProjectNameForTopBar/$',GetProjectNameForTopBar),
    url(r'^Home/Contact/$', contact_page),
    url(r'^Home/Contact/URL/(?P<url>.+)/$', contact_page_with_url),
    url(r'^Home/FileUploader/$', FileUploadTest),
    url(r'^Home/FileUploadSuccess/(?P<success>.+)/$', FileUploadTestOnSuccess),
    url(r'^Home/UserInfo/UploadProfilePicture/$', UploadProfilePicture),
    url(r'^Home/UserInfo/ServeProfilePictureURL/$', ServeProfilePictureURL),
    url(r'^Home/RemoveProfilePicture/', RemoveProfilePicture),
    url(r'^truncate_tables/$', truncate_all_tables),
    )

urlpatterns += patterns('',
    url(r'^Home/select2/$', select2),
        
    # Result Page
    # url(r'^Home/Search/$',Search),
    url(r'^Home/Login/$', LoginPage),
    url(r'^User_Login/$', User_Login),
    # url(r'^Home/Results/(?P<Page_No>[^/]*)/$',ResultPage),
    url(r'^Home/Results/$', Result),
    url(r'^Home/.*/GetResultAuto/$', GetResultAuto),
    url(r'^Home/.*/GetFilteredDataResult/$', GetFilteredDataResult),
    url(r'^Home/RunID/(?P<Run_Id>[^/]*)/$', Search2),
    url(r'^Home/.*/RunID_New/$', RunID_New),
    url(r'^Home/', include('urls_direct')),
    url(r'^Home/.*/DataFetchForTestCases/$', DataFetchForTestCases),
    url(r'^Home/.*/TestDataFetch/$', TestDataFetch),
    url(r'^Home/.*/UpdateData/$', UpdateData),
    url(r'^Home/.*/LogFetch/$', LogFetch),
    url(r'^Home/.*/ResultFilter/$', ResultFilter),
    url(r'^Home/.*/GetPageCount/$', GetPageCount),
    # url(r'^Home/.*/ResultTableFetch/$',ResultTableFetch),
    url(r'^Home/.*/RunIDStatus/$', RunIDStatus),
    url(r'^Home/.*/FilterDataForRunID/$', FilterDataForRunID),
    # url(r'^Home/.*/RunIDFailReason/$',RunIDFailReason),
    # url(r'^Home/.*/UpdateFailReason/$',UpdateFailReason),
    # url(r'^Home/.*/Edit/$',RunIDEdit),
    url(r'^Home/.*/AutoCompleteTag/$', AutoCompleteTag),
    url(r'^Home/RunID/$', ExceptionSearch),
    url(r'^Home/.*/AutoCompleteTestCasesSearch/$', AutoCompleteTestCasesSearch),
    url(r'^Home/.*/AutoCompleteUsersSearch/$', AutoCompleteUsersSearch),
    url(r'^Home/.*/AutoCompleteEmailSearch/$', AutoCompleteEmailSearch),
    url(r'^Home/.*/AutoCompleteTesterSearch/$', AutoCompleteTesterSearch),
    url(r'^Home/.*/Table_Data_TestCases/$', Table_Data_TestCases),
    url(r'^Home/.*/TableDataTestCasesOtherPages/$', TableDataTestCasesOtherPages),
    url(r'^Home/.*/Table_Data_TestResult/$', Table_Data_TestResult),
    url(r'^Home/.*/RunId_TestCases/$', RunId_TestCases),
    url(r'^Home/.*/Update_RelatedItems/$', Update_RelatedItems),
    url(r'^Home/.*/FailStep_TestCases/$', FailStep_TestCases),
    url(r'^Home/.*/TestCase_TestSteps/$', TestCase_TestSteps),
    url(r'^Home/.*/TestCase_TestSteps_SearchPage/$', TestCase_TestSteps_SearchPage),
    url(r'^Home/.*/TestCase_Detail_Table/$', TestCase_Detail_Table),
    url(r'^Home/.*/TestStep_Detail_Table/$', TestStep_Detail_Table),
    url(r'^Home/.*/createTablefromString/$', createTablefromString),
    
    url(r'^Home/ManageTestCases/$', manage_test_cases),
    url(r'^Home/ManageTestCases/getData/$', manage_tc_data),
    url(r'^Home/ManageTestCases/setData/createSection/$', create_section),
    url(r'^Home/ManageTestCases/setData/renameSection/$', rename_section),
    url(r'^Home/ManageTestCases/setData/deleteSection/[^/]*$', delete_section),
    
    # For now, let's keep away this buggy page
    url(r'^Home/ManageTestCases/CreateProductSections/$', CreateProductSections),
    url(r'^Home/ManageTestCases/CreateProductSections/ProductSectionsCreated/$', ProductSectionsCreated),
    url(r'^Home/ManageTestCases/Create/[^/]*$', Create),
    url(r'^Home/.*/Edit_TestCase$', EditTestCase),
    url(r'^Home/ManageTestCases/Edit/AutoCompleteTagSearch/$', AutoCompleteTagSearch),
    url(r'^Home/.*/AutoCompleteTestCasesSearchOtherPages/$', AutoCompleteTestCasesSearchOtherPages),
    url(r'^Home/.*/AutoCompleteTestStepSearch/$', AutoCompleteTestStepSearch),
    url(r'^Home/.*/GetProductSection/$', getProductSection),
    url(r'^Home/.*/GetProductFeature/$', getProductFeature),
    url(r'^Home/ManageTestCases/CreateNewTestCase/$', CreateNew),
    url(r'^Home/ManageTestCases/CreateNew/(?P<tc_id>[^/]*)/$', CopyTestCase),
    url(r'^Home/ManageTestCases/Edit/(?P<tc_id>[^/]*)/$', Edit),
    url(r'^Home/.*/TestCase_EditData/$', ViewTestCase),
    url(r'^Home/ManageTestCases/SearchEdit/$', SearchEdit),
    url(r'^Home/ManageTestCases/Create/AutoCompleteTagSearch/$', AutoCompleteTagSearch),
    url(r'^Home/ManageTestCases/Create/AutoCompleteTestStepSearch/$', AutoCompleteTestStepSearch),
    url(r'^Home/ManageTestCases/Create/Submit_New_TestCase/$', Create_Submit_New_TestCase),
    url(r'^Home/.*/Submit_New_TestCase/$', Create_Submit_New_TestCase),
    url(r'^Home/.*/GetSections/$', Get_Sections),
    url(r'^Home/.*/GetFeatures/$', Get_Features),
    url(r'^Home/.*/GetBrowsers/$', Get_Browsers),
    url(r'^Home/.*/GetVersions/$', Get_Versions),
    url(r'^Home/.*/GetTesters/$', Get_Testers),
    url(r'^Home/.*/GetRunTypes/$', Get_RunTypes),
    url(r'^Home/.*/GetStatus/$', Get_Status),
    url(r'^Home/.*/GetUsers/$', Get_Users),
    url(r'^Home/.*/GetMileStones/$', Get_MileStones),
    url(r'^Home/.*/GetMileStoneID/$', Get_MileStone_ID),
    url(r'^Home/.*/GetMileStoneByID/$', Get_MileStone_By_ID),
    url(r'^Home/EditMilestone/(?P<ms_id>[^/]*)/$', EditMilestone),
    url(r'^Home/.*/MilestoneRequirements/$', Milestone_Requirements),
    url(r'^Home/.*/MilestoneTeams/$', Milestone_Teams),
    url(r'^Home/.*/MilestoneTasks/$', Milestone_Tasks),
    url(r'^Home/.*/MilestoneBugs/$', Milestone_Bugs),
    url(r'^Home/.*/MilestoneTestings/$', Milestone_Testings),
    url(r'^Home/.*/MilestoneReport/$', Milestone_Report),
    url(r'^Home/.*/Send_Report/$', Send_Report),
    url(r'^Home/.*/GetAssignedTests/$', Get_AssignedTests),
    url(r'^Home/.*/GetRequirements/$', Get_Requirements),
    url(r'^Home/.*/Auto_Step_Create/$', Auto_Step_Create),
    url(r'^Home/ManageTestCases/DeleteExisting/$', DeleteExisting),
    url(r'^Home/.*/DeleteTestCase/$', DeleteTestCase),
    url(r'^Home/.*/GetStepNameType/$', GetStepNameType),
    url(r'^Home/.*/Go_TestCaseID/$', Go_TestCaseID),
    url(r'^Home/.*/Go_TestCaseStatus/$', Go_TestCaseStatus),
    # Test Set Management Section
    #url(r'^Home/ManageTestCases/TestSet/$', TestSet),
    url(r'^Home/.*/TestSet_Auto/$', TestSet_Auto),
    url(r'^Home/.*/TestTag_Auto/$', TestTag_Auto),
    url(r'^Home/.*/TestCase_Auto/$', TestCase_Auto),
    url(r'^Home/ManageSetTag/$',TestSetTagHome),
    url(r'^Home/.*/GetSetTag/$',GetSetTag),
    url(r'^Home/ManageSetTag/(?P<type>[^/]*)/(?P<name>[^/]*)/$',SetTagEdit),
    url(r'^Home/.*/createNewSetTag/$',createNewSetTag),
    url(r'^Home/.*/DeleteSetTag/$',DeleteSetTag),
    url(r'^Home/.*/AddTestCasesSetTag/$',AddTestCasesSetTag),
    url(r'^Home/.*/DeleteTestCasesSetTag/$',DeleteTestCasesSetTag),
    url(r'^Home/.*/UpdateSetTag/$',UpdateSetTag),
    #url(r'^Home/ManageTestCases/TestSet/Process/$', Data_Process),
    #url(r'^Home/ManageTestCases/TestSet/AddTestCase/$', AddTestCasesToSet),
    #url(r'^Home/ManageTestCases/TestSet/DeleteTestCase/$', DeleteTestCasesFromSet),
    # Test Step Management Section
    url(r'^Home/ManageTestCases/TestStep/$', TestStep),
    url(r'^Home/ManageTestCases/CreateStep/$', CreateStep),
    url(r'^Home/ManageTestCases/CreateStep/Process_CreateStep/$', Process_CreateStep),
    url(r'^Home/.*/TestStep_Auto/$', TestStep_Auto),
    url(r'^Home/.*/TestFeature_Auto/$', TestFeature_Auto),
    url(r'^Home/.*/TestDriver_Auto/$', TestDriver_Auto),
    url(r'^Home/.*/GetFeature/$', Get_Feature),
    url(r'^Home/.*/GetDriver/$', Get_Driver),
    url(r'^Home/.*/TestFeatureDriver_Auto/$', TestFeatureDriver_Auto),
    url(r'^Home/.*/TestCase_Results/$', TestCase_Results),
    url(r'^Home/.*/TestSteps_Results/$', TestSteps_Results),
    url(r'^Home/.*/Populate_info_div/$', Populate_info_div),
    url(r'^Home/.*/TestStep_Delete/$', TestStep_Delete),
    url(r'^Home/.*/FeatureDriver_Delete/$', FeatureDriver_Delete),
    url(r'^Home/ManageTestCases/FeatureDriverDelete/$', FeatureDriverDelete),
    url(r'^Home/ManageTestCases/TestStepDelete/$', TestStepDelete),
    url(r'^Home/ManageTestCases/Process_TestStep/$', Process_TestStep),
    url(r'^Home/ManageTestCases/Process_FeatureDriver/$', Process_FeatureDriver),
    url(r'^Home/.*/TestStepAutoComplete/$', TestStepAutoComplete),
    url(r'^Home/.*/TestStep_TestCases/$', TestStep_TestCases),
    url(r'^Home/.*/TestStepWithTypeInTable/$', TestStepWithTypeInTable),
    # Run Test Page
    url(r'^Home/CreateMilestone/$',manageMilestone),
    url(r'^Home/ManageMilestone/$',Milestone),
    url(r'^Home/RunTest/$', RunTest),
    url(r'^Home/.*/AutoMileStone/$', AutoMileStone),
    url(r'^Home/.*/AutoCompleteMilestoneSearch/$', AutoCompleteMilestoneSearch),
    url(r'^Home/.*/MileStoneOperation/$', MileStoneOperation),
    # url(r'^Home/Run_Test/Milestone_Process/$',Milestone_Process),
    # url(r'^Home/.*/Milestone_Auto/$',Milestone_Auto),
    url(r'^Home/.*/Verify_Query/$', Verify_Query),
    url(r'^Home/.*/Run_Test/$', Run_Test),
    url(r'^Home/.*/ReRun_Fail_TestCases/$', ReRun_Fail_TestCases),
    url(r'^Home/.*/Table_Data_UserList/$', Table_Data_UserList),
    url(r'^Home/.*/Auto_MachineName/$', Auto_MachineName),
    url(r'Home/.*/CheckMachine/$', CheckMachine),
    url(r'^Home/.*/AddManualTestMachine/$', AddManualTestMachine),
    url(r'^Home/.*/GetOS/$', GetOS),
    url(r'^Home/.*/chartDraw/$', chartDraw),
    url(r'^Home/.*/ReRun/$', ReRun),
    # Performance Page
    url(r'^Home/Performance/$', Performance),
    url(r'^Home/Performance/PerformanceResult/$', PerformanceResult),
    url(r'^Home/.*/Performance_ClickedBundle_Details_(?P<type>.)/$', Performance_ClickedBundle_Details),
    # url(r'^Home/PerformanceGraph_Window/$',PerformanceGraph_Window),
    
    
    # Daily Build Page
    url(r'^Home/DailyBuildResults/$', Daily_Build),
    url(r'^Home/.*/Table_Data_DailyBuild/$', Table_Data_DailyBuild),
    
    # MKS Report Page
    url(r'^Home/MKS-Report/$', MKSReport),
    url(r'^Home/.*/MKS_Report_Table/$', MKS_Report_Table),
    
    
    # Analysis Page
    url(r'^Home/Analysis/$', Analysis),
    url(r'^Home/.*/TestCaseSearch/$', TestCaseSearch),
    url(r'^Home/.*/Selected_TestCaseID_Analaysis/$', Selected_TestCaseID_Analaysis),
    url(r'^Home/.*/Selected_TestCaseID_History/$', Selected_TestCaseID_History),
    
    # Execution Report Page
    url(r'^Home/ExecutionReport/$', ExecutionReport),
    url(r'^Home/.*/Execution_Report_Table/$', Execution_Report_Table),
    
    # Test Type Status Page                                #minar09
    url(r'^Home/TestTypeStatus/$', TestTypeStatus),
    url(r'^Home/TestTypeStatus/get?$', TestTypeStatus),
    url(r'^Home/.*/TestTypeStatus_Report/$', TestTypeStatus_Report),
    
    # Bundle Report Page                                #minar09
    url(r'^Home/BundleReport/$', BundleReport),
    url(r'^Home/BundleReport/get?$', BundleReport),
    url(r'^Home/.*/BundleReport_Table/$', BundleReport_Table),
    url(r'^Home/.*/BundleReport_Table_Latest/$', BundleReport_Table_Latest),
    url(r'^Home/.*/Bundle_Report/$', Bundle_Report),
    # url(r'^Home/.*/Single_Env/$',Single_Env),
    
    # Documentation Page
    url(r'^Home/Documentation/$', Documentation),
    
    # Admin Page
    url(r'^Home/Admin/$', Admin),
    url(r'^Home/.*/Process_Git/$', Process_Git),
    url(r'^Home/FeaDri/$', TestStep),
    url(r'^Home/ManageStep/$', ManageStep),
    # url(r'^Home/FeaDri/$',FeaDri),
    # url(r'^Home/FeaDri/Process_FeatureDriver/$',Process_FeatureDriver),
    url(r'^Home/FeaDri/FeatureDriverOperation/$', FeatureDriverOperation),
    url(r'^Home/FeaDri/FeatureDriverDelete/$', FeatureDriverDelete),
    # url(r'^Home/.*/myview/$',myview), 
    
    #For TaskManageMent
    url(r'^Home/ManageTask/$',ManageTask),
    url(r'^Home/.*/Selected_TaskID_Analaysis/$',Selected_TaskID_Analaysis),
    url(r'^Home/.*/FetchProject/$',FetchProject),
    url(r'^Home/ManageBug/$',ManageBug),
    url(r'^Home/CreateNewBug/$',CreateBug),
    url(r'^Home/.*/BugSearch/$', BugSearch),
    url(r'^Home/.*/Selected_BugID_Analaysis/$', Selected_BugID_Analaysis),
    url(r'^Home/EditBug/(?P<bug_id>[^/]*)/$', EditBug),
    url(r'^Home/.*/LogNewBug/$',LogNewBug),
    url(r'^Home/.*/Bugs_List/$',Bugs_List),
    url(r'^Home/.*/ModifyBug/$',ModifyBug),
    url(r'^Home/.*/BugOperation/$',BugOperation),
    url(r'^Home/ManageLabel/$',ManageLabel),
    url(r'^Home/.*/CreateLabel/$',CreateLabel),
    #url(r'^Home/.*/GetLabels/$',Get_Labels),
    url(r'^Home/ManageRequirement/$',ManageRequirement),
    url(r'^Home/ManageTeam/$',ManageTeam),
    url(r'^Home/.*/GetTesterManager/$',GetTesterManager),
    url(r'^Home/.*/Create_Team/$',Create_Team),
    url(r'^Home/.*/GetAllTeam/$',GetAllTeam),
    url(r'^Home/.*/GetTeamInfo/$',GetTeamInfo),
    url(r'^Home/Team/(?P<team_name>[^/]*)/$',TeamData),
    url(r'^Home/.*/Add_Members/$',Add_Members),
    url(r'^Home/.*/Delete_Members/$',Delete_Members),
    url(r'^Home/.*/Delete_Team/$',Delete_Team),
    url(r'^Home/.*/UpdateTeamName/$',UpdateTeamName),
    url(r'^Home/CreateProject/$',CreateProject),
    url(r'^Home/.*/Create_New_Project/$',Create_New_Project),
    url(r'^Home/Project/(?P<project_id>[^/]*)/$',Project_Detail,name='project_detail'),
    url(r'^Home/.*/Small_Project_Detail/$',Small_Project_Detail),
    url(r'^Home/.*/Get_Projects/$',Get_Projects),
    url(r'^Home/.*/AddTeamtoProject/$',AddTeamtoProject),
    #url(r'^Home/.*/GetTeamInfoToCreateRequirement/$',GetTeamInfoToCreateRequirement),
    url(r'^Home/.*/SmallViewRequirements/$',SmallViewRequirements),
    url(r'^Home/.*/Reqs_List/$',Reqs_List),
    url(r'^Home/(?P<project_id>[^/]*)/CreateNewRequirement/$',ToNewRequirementPage),
    url(r'^Home/(?P<project_id>[^/]*)/getRequirements/$',getRequirements),
    url(r'^Home/(?P<project_id>[^/]*)/Requirements/(?P<req_id>[^/]*)/$',DetailRequirementView,name='detail_requirement'),
    url(r'^Home/Projects/(?P<project_id>[^/]*)/Requirements/(?P<team_id>[^/]*)/$',TeamWiseRequirementView),
    url(r'^Home/(?P<project_id>[^/]*)/Requirements/(?P<requirement_id>[^/]*)/post_comment/$',PostRequirementComment),    
    url(r'^Home/Project/(?P<project_id>[^/]*)/comment_post/$',FileUpload),
    url(r'^Home/Project/(?P<project_id>[^/]*)/comments/$',commentView,name='comment_view'),
    
    url(r'^Home/ManageTestCases/SearchEdit-Dev/$',SearchEditDev),
    url(r'^Home/FeaDri/GetTestStepsAndTestCasesOnDriverValue/$', GetTestStepsAndTestCasesOnDriverValue),
    
    
    #new requirement page implemenation ulrls
    
    url(r'^Home/(?P<project_id>[^/]*)/CreateRequirement/[^/]*$',RequirementPage),
    url(r'^Home/.*/SubmitCreateRequirement/$',CreateRequirement),
    url(r'^Home/(?P<project_id>[^/]*)/Task/[^/]*$',ViewTaskPage),
    #function for the task management page
    url(r'^Home/(?P<project_id>[^/]*)/CreateTask/[^/]*$',TaskPage),
    url(r'^Home/.*/Get_RequirementSections/$',Get_RequirementSections),
    url(r'^Home/.*/SubmitNewTask/$',SubmitNewTask),
    url(r'^Home/.*/SubmitEditedTask/$',SubmitEditedTask),
    url(r'^Home/.*/SubmitChildTask/$',SubmitChildTask),
    url(r'^Home/(?P<project_id>[^/]*)/EditTask/(?P<task_id>[^/]*)/$', EditTask),
    url(r'^Home/(?P<project_id>[^/]*)/ChildTask/(?P<task_id>[^/]*)/$', ChildTask),
    url(r'^Home/.*/Tasks_List/$',Tasks_List),
    #url(r'^Home/.*/GetTeamInfoPerProject/$',GetTeamInfoPerProject),
    url(r'^Home/.*/UpdateAccountInfo/$',updateAccountInfo),
    
    #updating the default project and team 
    url(r'^Home/.*/UpdateDefaultTeamForUser/$',UpdateDefaultTeamForUser),
    url(r'^Home/.*/UpdateDefaultProjectForUser/$',UpdateDefaultProjectForUser),
    
    #pages for the assignment of the team settings
    url(r'^Home/AssignSettings/$', assign_settings),
    url(r'^Home/.*/get_all_data_dependency_page/$',get_all_data_dependency_page),
    url(r'^Home/.*/add_new_dependency/$',add_new_dependency),
    url(r'^Home/.*/add_new_name_dependency/$',add_new_name_dependency),
    url(r'^Home/.*/get_all_name_under_dependency/$',get_all_name_under_dependency),
    url(r'^Home/.*/rename_dependency/$',rename_dependency),
    url(r'^Home/.*/add_new_version/$',add_new_version),
    url(r'^Home/.*/get_all_version_bit/$',get_all_version_bit),
    url(r'^Home/.*/link_dependency/$',link_dependency),
    url(r'^Home/.*/unlink_dependency/$',unlink_dependency),
    url(r'^Home/.*/rename_name/$',rename_name),
    url(r'^Home/.*/make_default_name/$',make_default_name),
    url(r'^Home/.*/add_new_branch/$',add_new_branch),
    url(r'^Home/.*/get_all_version_under_branch/$',get_all_version_under_branch),
    url(r'^Home/.*/add_new_version_branch/$',add_new_version_branch),
    url(r'^Home/.*/rename_branch/$',rename_branch),
    url(r'^Home/.*/unlink_branch/$',unlink_branch),
    url(r'^Home/.*/link_branch/$',link_branch),
    url(r'^Home/.*/add_new_feature/$',add_new_feature),
    url(r'^Home/.*/link_feature/$',link_feature),
    url(r'^Home/.*/unlink_feature/$',unlink_feature),
    #url(r'^Home/.*/rename_feature/$',rename_feature),
    #url(r'^Home/.*/first_level_sub_feature/$',first_level_sub_feature),
    url(r'^Home/.*/get_all_first_level_sub_feature/$',get_all_first_level_sub_feature),
    url(r'^Home/.*/CreateLevelWiseFeature/$',CreateLevelWiseFeature),
    #pages for the test case new implementation
    url(r'^Home/.*/get_default_settings/$',get_default_settings),
    url(r'^Home/Machine/(?P<machine_id>[^/]*)/$',edit_machine),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
    
)

urlpatterns += patterns('',
    url(r'^Home/.*/GetSubSections/$', Get_SubSections),
    url(r'^Home/.*/GetSubFeatures/$', Get_SubFeatures),  
    url(r'^Home/(?P<project_id>[^/]*)/EditRequirement/(?P<req_id>[^/]*)/$',Edit_Requirement),
    url(r'^Home/(?P<project_id>[^/]*)/ChildRequirement/(?P<req_id>[^/]*)/$',Child_Requirement),
    url(r'^Home/.*/Selected_Requirement_Analaysis/$',Selected_Requirement_Analaysis), 
    url(r'^Home/.*/SubmitEditRequirement/$',SubmitEditRequirement), 
    url(r'^Home/.*/SubmitChildRequirement/$',SubmitChildRequirement),
    url(r'^Home/.*/AutoCompleteLabel/$',AutoCompleteLabel),
    url(r'^Home/.*/AutoCompleteTask/$',AutoCompleteTask), 
    url(r'^Home/.*/AutoCompleteRequirements/$',AutoCompleteRequirements),
    url(r'^Home/ViewMilestone/$',ViewMilestone),
    url(r'^Home/.*/New_Execution_Report/$',New_Execution_Report),
    url(r'^Home/.*/get_all_machine/$',get_all_machine),
    url(r'^Home/.*/Get_MileStone_Names/$',Get_MileStone_Names),
    url(r'^Home/.*/Get_Feature_Path/$',Get_Feature_Path),
    url(r'^Home/.*/Check_Feature_Path/$',Check_Feature_Path),
    url(r'^Home/.*/SearchTestCase/$',SearchTestCase),
    url(r'^Home/RunHistory/(?P<tc_id>[^/]*)/$',CaseRunHistory),
    url(r'^Home/ViewSteps/$',ViewSteps),
    url(r'^Home/.*/Steps_List/$',Steps_List),
	url(r'^Home/.*/TestCaseDataFromMainDriver/$',TestCaseDataFromMainDriver),
	url(r'^Home/.*/get_feature_path/$',get_feature_path),
    url(r'^Home/User/ProfileDetail/$',ProfileDetail),
    url(r'^Home/ManageTestCases/EditStep/(?P<stepname>[^/]*)/$',EditStep),
    url(r'^Home/.*/CreateEditStep/$',CreateEditStep),
    url(r'^Home/.*/TestStepSearch/$',TestStepSearch),
	)

