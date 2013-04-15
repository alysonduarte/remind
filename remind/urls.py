from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('remind.views',
    url(r'^core/',              include('remind.core.urls',               namespace='core')),
)

urlpatterns += patterns('',
   (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': settings.MEDIA_ROOT}))