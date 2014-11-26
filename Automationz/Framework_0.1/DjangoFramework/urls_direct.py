from django.conf.urls import *
from MySite.views import *  # @UnusedWildImport

urlpatterns = patterns('',
    # Home Page
    url(r'^RunID/(?P<Run_Id>[^/]*)/TC/(?P<TC_Id>[^/]*)/Execute/$', RunIDTestCases),
    url(r'^RunID/(?P<Run_Id>[^/]*)/TC/(?P<TC_Id>[^/]*)/View/$', ViewRunIDTestCases),
    url(r'.*/AutoTestCasePass/$',AutoTestCasePass),
    url(r'.*/specific_dependency_settings/$',specific_dependency_settings),
)