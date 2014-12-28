from django.conf.urls import patterns

urlpatterns = patterns ('nucleus.views',
    (r'^login/$', 'login_view'),
    (r'^logout/$', 'logout_view'),
)
