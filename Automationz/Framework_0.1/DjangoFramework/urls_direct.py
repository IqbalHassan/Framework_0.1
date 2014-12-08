from django.conf.urls import *
from MySite.views import *  # @UnusedWildImport

urlpatterns = patterns('',
    # Home Page
    url(r'^RunID/(?P<Run_Id>[^/]*)/TC/(?P<TC_Id>[^/]*)/Execute/$', RunIDTestCases),
    url(r'^RunID/(?P<Run_Id>[^/]*)/TC/(?P<TC_Id>[^/]*)/View/$', ViewRunIDTestCases),
    url(r'^.*/AutoTestCasePass/$',AutoTestCasePass),
    url(r'^.*/specific_dependency_settings/$',specific_dependency_settings),
    url(r'^superAdmin/',admin_page),
    url(r'^superAdminFunction/Project/$',superAdminFunction),
    url(r'^.*/GetProjectOwner/$',GetProjectOwner),
    url(r'^superAdminFunction/AddUser/$',superAdminFunction),
    url(r'^superAdminFunction/ListUser/$',superAdminFunction),
    url(r'^.*/Create_New_User/$',Create_New_User),
    url(r'^.*/ListAllUsers/$',ListAllUser),
    url(r'^AssignTesters/$',AssignTesters),
)