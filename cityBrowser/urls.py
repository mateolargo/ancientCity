from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'test', 'direct_to_template', {'template': 'mytemplate.html'}),

)

urlpatterns += patterns('ancientCity.cityBrowser',
    (r'^$', 'views.index'),
    (r'^rome', 'views.rome'),
    (r'^(?P<mon_id>\d+)$', 'views.monument'),
)
