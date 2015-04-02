from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import settings

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^$', 'config.xcom.views.primary', name='primary'),
    *[url(r'^%s$' % s, 'config.xcom.views.%s' % s, name=s) for s in ('help', 'about', 'reform', 'related', 'freechange', 'news', 'blog', 'contact', 'vote', 'range', 'saverange')]
)
