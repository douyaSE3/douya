
from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',

    url(r'^(?P<user_id>\d+)/$', traveller_index), 

    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),

    url(r'^register/$', register),
    url(r'^modify/$', modify),

)