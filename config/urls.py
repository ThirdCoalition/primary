from django.conf.urls import patterns, include, url

import settings

urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^$', 'primary.views.blog', name='blog'),
    *[url(r'^%s$' % s, 'primary.views.%s' % s, name=s) for s in ('platform', 'almanac')]
)
