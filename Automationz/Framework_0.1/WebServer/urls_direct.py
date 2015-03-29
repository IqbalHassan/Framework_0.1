from django.conf.urls import *
from MySite.views import *  # @UnusedWildImport

urlpatterns = patterns('',
    # Home Page
    url(r'^RunID/(?P<Run_Id>[^/]*)/TC/(?P<TC_Id>[^/]*)/Execute/$', RunIDTestCases),
    url(r'^RunID/(?P<Run_Id>[^/]*)/TC/(?P<TC_Id>[^/]*)/View/$', ViewRunIDTestCases),
    url(r'^.*/AutoTestCasePass/$',AutoTestCasePass),
    url(r'^.*/specific_dependency_settings/$',specific_dependency_settings),
    url(r'^superAdmin/',admin_page),
    url(r'^superAdminFunction/Project/$',CreateProject),
    url(r'^superAdminFunction/ListProject/$',ListProject),
    url(r'^.*/GetProjectOwner/$',GetProjectOwner),
    url(r'^superAdminFunction/AddUser/$',AddUser),
    #url(r'^superAdminFunction/ListUser/$',superAdminFunction),
    url(r'^superAdminFunction/AssignMembers/$',AssignMembers),
    url(r'^.*/Create_New_User/$',Create_New_User),
    url(r'^superAdminFunction/ListUser/$',ListAllUser),
    #url(r'^superAdminFunction/ListProject/$',superAdminFunction),
    url(r'^.*/ListProjects/$',ListProject),
    url(r'^AssignTesters/$',AssignTesters),
    url(r'.*/get_projects/$',get_projects),
    url(r'.*/update_team_project/$',update_team_project),
)