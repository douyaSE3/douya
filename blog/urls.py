
from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',

    url(r'^(?P<article_id>\d+)/$', view_article), 
    url(r'^add_article/(?P<place_id>\d+)/$', add_article), 
    url(r'^edit_article/(?P<article_id>\d+)/$', edit_article), 
    url(r'^del_article/(?P<article_id>\d+)/$', del_article), 

)