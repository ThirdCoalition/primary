from django.conf.urls import patterns, include, url

import settings

urlpatterns = patterns('',
    url(r'^$', 'config.xcom.views.primary', name='primary'),
    *[url(r'^%s$' % s, 'config.xcom.views.%s' % s, name=s) for s in ('about', 'npos', 'platform', 'regions', 'vote', 'random', 'range', 'saverange', 'approval')]
)
