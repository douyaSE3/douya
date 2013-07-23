from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'place.views.index'),

    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^place/', include('place.urls')), 

    url(r'^traveller/', include('traveller.urls')),

    url(r'^blog/', include('blog.urls')), 

    url(r'^tinymce/', include('tinymce.urls')),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT, }),
)


