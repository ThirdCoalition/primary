from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'config.xcom.views.home', name='home'),
    *[url(r'^%s$' % s, 'config.xcom.views.%s' % s, name=s) for s in ('help', 'about', 'reform', 'related', 'freechange', 'news', 'blog', 'contact', 'vote')]
)
