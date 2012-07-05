from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.myna',
                       url(r'^$', 'first',
                           name='gstudio_myna'),

                       )
