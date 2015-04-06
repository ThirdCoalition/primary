from django.conf.urls import patterns, include, url

import settings

urlpatterns = patterns('',
    url(r'^$', 'config.xcom.views.primary', name='primary'),
    *[url(r'^%s$' % s, 'config.xcom.views.%s' % s, name=s) for s in ('help', 'about', 'reform', 'related', 'freechange', 'news', 'blog', 'contact', 'vote', 'range', 'saverange', 'almanac', 'approval')]
)
