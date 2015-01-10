# Bismillahir Rahmanir Rahim, ALLAHU AKBAR

# Execute the SQL query directly, without using Model layer
# https://docs.djangoproject.com/en/1.3/topics/db/sql/#executing-custom-sql-directly

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

### Start of custom code ###

import DataBaseUtilities as DB
import Global

# import CommonUtil
ip = Global.get_ip(True)

def GetConnection():
    Conn = DB.ConnectToDataBase(sDbname="postgres", sUser="postgres", sPswd="password", sHost=ip)
    return Conn 
def GetColumnNames(sTableName):
    Conn = GetConnection()
    ColumnNames = DB.GetData(Conn, "SELECT column_name FROM INFORMATION_SCHEMA.Columns where TABLE_NAME = '%s'" % sTableName)
    Conn.close()
    return [Col.upper() for Col in ColumnNames]

### End of custom code ###

class Branch(models.Model):
    id = models.IntegerField(primary_key=True)
    branch_name = models.CharField(max_length=50, unique=True, blank=True)
    class Meta:
        db_table = 'branch'

class BranchManagement(models.Model):
    project_id = models.CharField(max_length=10, blank=True)
    team_id = models.IntegerField(null=True, blank=True)
    branch = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'branch_management'

class Bugs(models.Model):
    bug_id = models.CharField(max_length=20, blank=True)
    bug_title = models.CharField(max_length=100, blank=True)
    bug_description = models.TextField(blank=True)
    bug_startingdate = models.DateField(null=True, blank=True)
    bug_endingdate = models.DateField(null=True, blank=True)
    bug_priority = models.CharField(max_length=10, blank=True)
    bug_milestone = models.CharField(max_length=50, blank=True)
    bug_createdby = models.CharField(max_length=40, blank=True)
    bug_creationdate = models.DateField(null=True, blank=True)
    bug_modifiedby = models.CharField(max_length=40, blank=True)
    bug_modifydate = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, blank=True)
    team_id = models.CharField(max_length=50, blank=True)
    project_id = models.CharField(max_length=50, blank=True)
    tester = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'bugs'

class CommentAttachment(models.Model):
    comment_id = models.CharField(max_length=10, primary_key=True)
    docfile = models.CharField(max_length=300)
    class Meta:
        db_table = 'comment_attachment'

class CommentTrack(models.Model):
    child_comment = models.CharField(max_length=10, primary_key=True)
    parent_comment = models.CharField(max_length=300)
    class Meta:
        db_table = 'comment_track'

class Comments(models.Model):
    comment_id = models.CharField(max_length=10, primary_key=True)
    project_id = models.CharField(max_length=10)
    comment_text = models.TextField(blank=True)
    comment_date = models.DateTimeField(null=True, blank=True)
    commented_by = models.CharField(max_length=40)
    rank = models.CharField(max_length=40)
    attachment = models.NullBooleanField(null=True, blank=True)
    class Meta:
        db_table = 'comments'

class ComponentsMap(models.Model):
    id1 = models.CharField(max_length=50, blank=True)
    id2 = models.CharField(max_length=50, blank=True)
    type1 = models.CharField(max_length=100, blank=True)
    type2 = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'components_map'

class ConfigValues(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100)
    sub_type = models.CharField(max_length=100, blank=True)
    value = models.CharField(max_length=100)
    class Meta:
        db_table = 'config_values'

class ContainerTypeData(models.Model):
    id = models.IntegerField(primary_key=True)
    dataid = models.CharField(max_length=20, blank=True)
    curname = models.CharField(max_length=200, blank=True)
    newname = models.CharField(max_length=300, blank=True)
    items_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'container_type_data'

class DailyBuildStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    daily_build_user = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    last_checked_time = models.DateTimeField(null=True, blank=True)
    bundle = models.CharField(max_length=100)
    machine_os = models.CharField(max_length=100, blank=True)
    local_ip = models.CharField(max_length=30, blank=True)
    branch = models.CharField(max_length=30, blank=True)
    release = models.CharField(max_length=30, blank=True)
    run_id = models.CharField(max_length=100, blank=True)
    build_path = models.CharField(max_length=1000, blank=True)
    class Meta:
        db_table = 'daily_build_status'

class DefaultChoice(models.Model):
    user_id = models.CharField(max_length=5, primary_key=True)
    default_project = models.CharField(max_length=10, blank=True)
    default_team = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'default_choice'

class Dependency(models.Model):
    id = models.IntegerField(primary_key=True)
    dependency_name = models.CharField(max_length=50, unique=True)
    class Meta:
        db_table = 'dependency'

class DependencyManagement(models.Model):
    project_id = models.CharField(max_length=10)
    team_id = models.IntegerField()
    dependency = models.IntegerField()
    default_choices = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'dependency_management'

class DependencyName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    dependency_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'dependency_name'

class DependencyValues(models.Model):
    id = models.IntegerField(primary_key=True)
    dv_id = models.IntegerField()
    version = models.CharField(max_length=50)
    bit_name = models.CharField(max_length=50)
    class Meta:
        db_table = 'dependency_values'

class ExecutionLog(models.Model):
    executionlogid = models.IntegerField(primary_key=True)
    logid = models.CharField(max_length=40, blank=True)
    modulename = models.CharField(max_length=60)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=100)
    loglevel = models.IntegerField()
    tstamp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'execution_log'

class FeatureManagement(models.Model):
    project_id = models.CharField(max_length=10, blank=True)
    team_id = models.IntegerField(null=True, blank=True)
    feature = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'feature_management'

class FeatureMap(models.Model):
    id = models.IntegerField(primary_key=True)
    fm_id = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)
    feature_id = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'feature_map'

class LabelMap(models.Model):
    id = models.IntegerField(primary_key=True)
    lm_id = models.CharField(max_length=50, blank=True)
    label_id = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'label_map'

class Labels(models.Model):
    label_id = models.CharField(max_length=50, primary_key=True)
    label_name = models.CharField(max_length=50, blank=True)
    label_color = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'labels'

class MachineDependencySettings(models.Model):
    machine_serial = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, blank=True)
    bit = models.IntegerField(null=True, blank=True)
    version = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'machine_dependency_settings'

class MachineProjectMap(models.Model):
    machine_serial = models.IntegerField(null=True, blank=True)
    project_id = models.CharField(max_length=10, blank=True)
    team_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'machine_project_map'

class MasterData(models.Model):
    id = models.IntegerField(primary_key=True)
    md_id = models.CharField(max_length=30)
    field = models.CharField(max_length=50)
    value = models.TextField()
    description = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = 'master_data'

class MilestoneInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    mi_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=500, blank=True)
    starting_date = models.DateField(null=True, blank=True)
    finishing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    created_by = models.TextField(blank=True)
    modified_by = models.TextField(blank=True)
    created_date = models.DateField(null=True, blank=True)
    modified_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'milestone_info'

class MilestoneTeamMap(models.Model):
    milestone_id = models.IntegerField(null=True, blank=True)
    team_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'milestone_team_map'

class PerformanceResults(models.Model):
    id = models.IntegerField(primary_key=True)
    product_version = models.CharField(max_length=300)
    tc = models.ForeignKey('TestCases')
    run_id = models.CharField(max_length=100, blank=True)
    duration = models.TextField(blank=True) # This field type is a guess.
    cpu_avg = models.IntegerField(null=True, blank=True)
    cpu_peak = models.IntegerField(null=True, blank=True)
    machine_os = models.CharField(max_length=100, blank=True)
    hw_model = models.CharField(max_length=50, blank=True)
    memory_delta = models.IntegerField(null=True, blank=True)
    cpu_peaktime = models.TimeField(null=True, blank=True)
    class Meta:
        db_table = 'performance_results'

class PermittedUserList(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_names = models.CharField(max_length=255)
    user_level = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    class Meta:
        db_table = 'permitted_user_list'

class ProductFeatures(models.Model):
    feature_id = models.IntegerField()
    feature_path = models.TextField(unique=True) # This field type is a guess.
    class Meta:
        db_table = 'product_features'

class ProductSections(models.Model):
    section_id = models.IntegerField(primary_key=True)
    section_path = models.TextField() # This field type is a guess.
    class Meta:
        db_table = 'product_sections'

class ProjectTeamMap(models.Model):
    project = models.ForeignKey('Projects', null=True, blank=True)
    team_id = models.CharField(max_length=10, blank=True)
    status = models.NullBooleanField(blank=True)
    class Meta:
        db_table = 'project_team_map'

class Projects(models.Model):
    project_id = models.CharField(max_length=10, primary_key=True)
    project_name = models.CharField(max_length=100)
    project_description = models.CharField(max_length=200)
    project_startingdate = models.DateField(null=True, blank=True)
    project_endingdate = models.DateField(null=True, blank=True)
    project_owners = models.TextField(blank=True)
    project_createdby = models.CharField(max_length=40)
    project_creationdate = models.DateField()
    project_modifiedby = models.CharField(max_length=40)
    project_modifydate = models.DateField()
    class Meta:
        db_table = 'projects'

class RequirementSections(models.Model):
    requirement_path_id = models.IntegerField(primary_key=True)
    requirement_path = models.TextField() # This field type is a guess.
    class Meta:
        db_table = 'requirement_sections'

class RequirementTeamMap(models.Model):
    requirement = models.ForeignKey('Requirements', null=True, blank=True)
    team_id = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'requirement_team_map'

class Requirements(models.Model):
    requirement_id = models.CharField(max_length=10, primary_key=True)
    requirement_title = models.CharField(max_length=100)
    requirement_startingdate = models.DateField()
    requirement_endingdate = models.DateField()
    requirement_priority = models.CharField(max_length=10, blank=True)
    requirement_milestone = models.CharField(max_length=50, blank=True)
    requirement_createdby = models.CharField(max_length=40)
    requirement_creationdate = models.DateField()
    requirement_modifiedby = models.CharField(max_length=40)
    requirement_modifydate = models.DateField()
    project_id = models.CharField(max_length=10, blank=True)
    requirement_description = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=30, blank=True)
    parent_requirement_id = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'requirements'

class ResultContainerTypeData(models.Model):
    id = models.IntegerField(primary_key=True)
    rctd_id = models.IntegerField()
    run_id = models.CharField(max_length=100)
    dataid = models.CharField(max_length=20, blank=True)
    curname = models.CharField(max_length=200, blank=True)
    newname = models.CharField(max_length=300, blank=True)
    items_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'result_container_type_data'

class ResultMasterData(models.Model):
    id = models.IntegerField(primary_key=True)
    run_id = models.CharField(max_length=100)
    rmd_id = models.CharField(max_length=30)
    field = models.CharField(max_length=50)
    value = models.TextField()
    description = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = 'result_master_data'

class ResultTestCaseDatasets(models.Model):
    run = models.ForeignKey('ResultTestCases')
    tcdatasetid = models.CharField(max_length=20)
    tc_id = models.CharField(max_length=10, blank=True)
    execornot = models.CharField(max_length=10)
    data_type = models.TextField()
    class Meta:
        db_table = 'result_test_case_datasets'

class ResultTestCaseTag(models.Model):
    run = models.ForeignKey('ResultTestCases')
    tc_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    property = models.CharField(max_length=100)
    class Meta:
        db_table = 'result_test_case_tag'

class ResultTestCases(models.Model):
    run_id = models.CharField(max_length=100)
    tc_id = models.CharField(max_length=10)
    tc_name = models.CharField(max_length=100)
    tc_type = models.CharField(max_length=10)
    tc_executiontype = models.CharField(max_length=20, blank=True)
    tc_priority = models.CharField(max_length=10, blank=True)
    tc_localization = models.CharField(max_length=10)
    tc_createdby = models.CharField(max_length=40)
    tc_creationdate = models.DateField()
    tc_modifiedby = models.CharField(max_length=40)
    tc_modifydate = models.DateField()
    defectid = models.CharField(max_length=15, blank=True)
    prd_no = models.CharField(max_length=15, blank=True)
    class Meta:
        db_table = 'result_test_cases'

class ResultTestSteps(models.Model):
    id = models.IntegerField(primary_key=True)
    rts_id = models.IntegerField()
    run = models.ForeignKey('ResultTestStepsList')
    tc_id = models.CharField(max_length=10, blank=True)
    step_id = models.IntegerField()
    teststepsequence = models.IntegerField(null=True, blank=True)
    test_step_type = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = 'result_test_steps'

class ResultTestStepsData(models.Model):
    run = models.ForeignKey(ResultTestCaseDatasets)
    id = models.IntegerField()
    tcdatasetid = models.CharField(max_length=20, blank=True)
    testdatasetid = models.CharField(max_length=20)
    teststepseq = models.IntegerField()
    class Meta:
        db_table = 'result_test_steps_data'

class ResultTestStepsList(models.Model):
    run_id = models.CharField(max_length=100)
    step_id = models.IntegerField()
    stepname = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    driver = models.CharField(max_length=200)
    steptype = models.CharField(max_length=100)
    data_required = models.NullBooleanField(blank=True)
    stepfeature = models.CharField(max_length=200, blank=True)
    stepenable = models.NullBooleanField(blank=True)
    step_editable = models.NullBooleanField(blank=True)
    case_desc = models.CharField(max_length=200, blank=True)
    expected = models.CharField(max_length=200, blank=True)
    verify_point = models.NullBooleanField(blank=True)
    step_continue = models.NullBooleanField(blank=True)
    estd_time = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'result_test_steps_list'

class TaskSections(models.Model):
    task_path_id = models.IntegerField(primary_key=True)
    task_path = models.TextField() # This field type is a guess.
    class Meta:
        db_table = 'task_sections'

class Tasks(models.Model):
    tasks_id = models.CharField(max_length=10, primary_key=True)
    tasks_title = models.CharField(max_length=100)
    tasks_description = models.TextField(blank=True)
    tasks_startingdate = models.DateField()
    tasks_endingdate = models.DateField()
    tasks_priority = models.CharField(max_length=10, blank=True)
    tasks_milestone = models.CharField(max_length=50, blank=True)
    tasks_createdby = models.CharField(max_length=40)
    tasks_creationdate = models.DateField()
    tasks_modifiedby = models.CharField(max_length=40)
    tasks_modifydate = models.DateField()
    parent_id = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=30, blank=True)
    tester = models.CharField(max_length=10, blank=True)
    project_id = models.TextField(blank=True)
    team_id = models.TextField(blank=True)
    class Meta:
        db_table = 'tasks'

class TeamInfo(models.Model):
    team_id = models.IntegerField(null=True, blank=True)
    user_id = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'team_info'

class TeamWiseSettings(models.Model):
    project_id = models.CharField(max_length=10, blank=True)
    team_id = models.IntegerField(null=True, blank=True)
    parameters = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'team_wise_settings'

class Test(models.Model):
    tc_id = models.CharField(max_length=10, blank=True)
    tc_name = models.CharField(max_length=100, blank=True)
    tc_type = models.CharField(max_length=10, blank=True)
    tc_executiontype = models.CharField(max_length=20, blank=True)
    tc_priority = models.CharField(max_length=10, blank=True)
    tc_localization = models.CharField(max_length=10, blank=True)
    tc_createdby = models.CharField(max_length=40, blank=True)
    tc_creationdate = models.DateField(null=True, blank=True)
    tc_modifiedby = models.CharField(max_length=40, blank=True)
    tc_modifydate = models.DateField(null=True, blank=True)
    defectid = models.CharField(max_length=15, blank=True)
    prd_no = models.CharField(max_length=15, blank=True)
    class Meta:
        db_table = 'test'

class TestCaseDatasets(models.Model):
    tcdatasetid = models.CharField(max_length=20, primary_key=True)
    tc = models.ForeignKey('TestCases', null=True, blank=True)
    execornot = models.CharField(max_length=10)
    data_type = models.TextField()
    class Meta:
        db_table = 'test_case_datasets'

class TestCaseResults(models.Model):
    id = models.IntegerField(primary_key=True)
    run = models.ForeignKey(ResultTestCases)
    tc_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20, blank=True)
    teststarttime = models.DateTimeField(null=True, blank=True)
    testendtime = models.DateTimeField(null=True, blank=True)
    duration = models.TextField(blank=True) # This field type is a guess.
    failreason = models.CharField(max_length=200, blank=True)
    faildetail = models.TextField(blank=True)
    logid = models.CharField(max_length=150, blank=True)
    screenshotsid = models.CharField(max_length=40, blank=True)
    automationlogid = models.CharField(max_length=40, blank=True)
    class Meta:
        db_table = 'test_case_results'

class TestCaseTag(models.Model):
    tc = models.ForeignKey('TestCases')
    name = models.CharField(max_length=100)
    property = models.CharField(max_length=100)
    class Meta:
        db_table = 'test_case_tag'

class TestCases(models.Model):
    tc_id = models.CharField(max_length=10, primary_key=True)
    tc_name = models.CharField(max_length=100)
    tc_type = models.CharField(max_length=10)
    tc_executiontype = models.CharField(max_length=20, blank=True)
    tc_priority = models.CharField(max_length=10, blank=True)
    tc_localization = models.CharField(max_length=10)
    tc_createdby = models.CharField(max_length=40)
    tc_creationdate = models.DateField()
    tc_modifiedby = models.CharField(max_length=40)
    tc_modifydate = models.DateField()
    defectid = models.CharField(max_length=15, blank=True)
    prd_no = models.CharField(max_length=15, blank=True)
    class Meta:
        db_table = 'test_cases'

class TestEnvResults(models.Model):
    id = models.IntegerField(primary_key=True)
    run_id = models.TextField()
    tester_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, blank=True)
    teststarttime = models.DateTimeField(null=True, blank=True)
    testendtime = models.DateTimeField(null=True, blank=True)
    duration = models.TextField(blank=True) # This field type is a guess.
    rundescription = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = 'test_env_results'

class TestRun(models.Model):
    id = models.IntegerField(primary_key=True)
    run = models.ForeignKey(ResultTestCases)
    tc_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20, blank=True)
    executiontime = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'test_run'

class TestRunEnv(models.Model):
    id = models.IntegerField(primary_key=True)
    run_id = models.CharField(max_length=100, blank=True)
    rundescription = models.CharField(max_length=200, blank=True)
    tester_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, blank=True)
    last_updated_time = models.CharField(max_length=255, blank=True)
    machine_ip = models.CharField(max_length=30, blank=True)
    email_notification = models.TextField(blank=True)
    test_objective = models.CharField(max_length=50, blank=True)
    assigned_tester = models.CharField(max_length=50, blank=True)
    run_type = models.CharField(max_length=50, blank=True)
    test_milestone = models.CharField(max_length=100, blank=True)
    branch_version = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'test_run_env'

class TestStepResults(models.Model):
    id = models.IntegerField(primary_key=True)
    run = models.ForeignKey(ResultTestCases)
    tc_id = models.CharField(max_length=20)
    teststep_id = models.IntegerField()
    status = models.CharField(max_length=20, blank=True)
    stepstarttime = models.DateTimeField(null=True, blank=True)
    stependtime = models.DateTimeField(null=True, blank=True)
    duration = models.TextField(blank=True) # This field type is a guess.
    failreason = models.CharField(max_length=200, blank=True)
    faildetail = models.TextField(blank=True)
    logid = models.CharField(max_length=100, blank=True)
    start_memory = models.CharField(max_length=100, blank=True)
    end_memory = models.CharField(max_length=100, blank=True)
    memory_consumed = models.CharField(max_length=100, blank=True)
    teststepsequence = models.IntegerField(null=True, blank=True)
    testcaseresulttindex = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'test_step_results'

class TestSteps(models.Model):
    id = models.IntegerField(primary_key=True)
    tc = models.ForeignKey(TestCases, null=True, blank=True)
    step = models.ForeignKey('TestStepsList')
    teststepsequence = models.IntegerField(null=True, blank=True)
    test_step_type = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = 'test_steps'

class TestStepsData(models.Model):
    id = models.IntegerField(primary_key=True)
    tcdatasetid = models.ForeignKey(TestCaseDatasets, null=True, db_column='tcdatasetid', blank=True)
    testdatasetid = models.CharField(max_length=20)
    teststepseq = models.IntegerField()
    class Meta:
        db_table = 'test_steps_data'

class TestStepsList(models.Model):
    step_id = models.IntegerField(primary_key=True)
    stepname = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    driver = models.CharField(max_length=200)
    steptype = models.CharField(max_length=100)
    data_required = models.NullBooleanField(blank=True)
    stepfeature = models.CharField(max_length=200, blank=True)
    stepenable = models.NullBooleanField(blank=True)
    step_editable = models.NullBooleanField(blank=True)
    case_desc = models.CharField(max_length=200, blank=True)
    expected = models.CharField(max_length=200, blank=True)
    verify_point = models.NullBooleanField(blank=True)
    step_continue = models.NullBooleanField(blank=True)
    estd_time = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'test_steps_list'

class UserInfo(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=511, blank=True)
    profile_picture_name = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = 'user_info'

class Versions(models.Model):
    id = models.IntegerField(primary_key=True)
    v_id = models.IntegerField(null=True, blank=True)
    version_name = models.CharField(max_length=50, unique=True, blank=True)
    class Meta:
        db_table = 'versions'

