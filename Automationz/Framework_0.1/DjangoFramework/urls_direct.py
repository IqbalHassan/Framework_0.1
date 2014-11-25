from django.conf.urls import *
from MySite.views import *  # @UnusedWildImport

urlpatterns = patterns('',
    # Home Page
    url(r'^(?P<Run_Id>[^/]*)/TC/(?P<TC_Id>[^/]*)/Execute/$', RunIDTestCases),
    url(r'^(?P<Run_Id>[^/]*)/TC/(?P<TC_Id>[^/]*)/View/$', ViewRunIDTestCases),
    )