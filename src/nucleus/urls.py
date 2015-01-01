from django.conf.urls import patterns

urlpatterns = patterns ('nucleus.views',
    (r'^login/$', 'login_view'),
    (r'^logout/$', 'logout_view'),
    (r'^users/$', 'users'),
    (r'^users/(?P<user_id>[\w\-]+)/$', 'users'),
    (r'^groups/$', 'groups'),
    (r'^groups/(?P<group_id>[\w\-]+)/$', 'groups'),
)
