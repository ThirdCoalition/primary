from django.conf.urls import patterns, include, url

import settings

urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^$', 'primary.views.primary', name='primary'),
    url(r'^vote/(?P<region>\w+)$', 'primary.views.vote', name='voteurl'),
    url(r'^delegate/user/(?P<handle>\w+)$', 'primary.views.delegate', name='delegate'),
    *[url(r'^%s$' % s, 'primary.views.%s' % s, name=s) for s in ('about', 'npos', 'platform', 'regions', 'vote', 'saverange', 'account', 'release')]
)
