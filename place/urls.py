
from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',

    url(r'^$', place_index), 
    url(r'^search/$', place_search), 
    url(r'^(?P<place_id>\d{6})/$', place_intro), 

    url(r'^(?P<place_id>\d{6})/add_relationship/(?P<operation>\d)/$', add_relationship), 
    url(r'^(?P<place_id>\d{6})/modify_relationship/$', modify_relationship),
    url(r'^(?P<place_id>\d{6})/del_relationship/$', del_relationship), 

    url(r'^plan/add_photo/(?P<plan_id>\d+)/$', add_photo), 
    url(r'^plan/del_photo/(?P<photo_id>\d+)/$', del_photo), 

    url(r'^add_plan/$', add_plan), 
    url(r'^edit_plan/(?P<plan_id>\d+)/$', edit_plan), 
    url(r'^copy_plan/(?P<origin_plan_id>\d+)/$', copy_plan), 
    url(r'^plan/(?P<plan_id>\d+)/$', view_plan), 

    url(r'^edit_plan_search/$', edit_plan_search), 
    url(r'^add_play/(?P<plan_id>\d+)/$', add_play), 
    url(r'^edit_play/(?P<play_id>\d+)/$', edit_play), 
    url(r'^del_play/(?P<play_id>\d+)/$', del_play), 

    url(r'^edit_route/(?P<route_id>\d+)/$', edit_route),
    url(r'^del_route/(?P<route_id>\d+)/$', del_route),
)

