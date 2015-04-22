from django.conf.urls import patterns, include, url

import settings

urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^$', 'config.xcom.views.primary', name='primary'),
    *[url(r'^%s$' % s, 'config.xcom.views.%s' % s, name=s) for s in ('about', 'npos', 'platform', 'regions', 'vote', 'random', 'saverange', 'approval')]
)
