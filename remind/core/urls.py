# coding: UTF-8
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
        # Should be changed for production
    url
    (r'^static/(?P<path>.*)$',      'django.views.static.serve', {'document_root': 'remind/static/', 'show_indexes': True}),
    (r'cal/$',                      'remind.core.views.calendar'),
    (r'events.xml$',                'remind.core.views.eventsXML'),
    (r'dataprocessor.xml$',         'remind.core.views.dataprocessorXML'),

)