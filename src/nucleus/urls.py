from django.conf.urls import patterns

urlpatterns = patterns ('nucleus.views',
    (r'^login/$', 'login_view'),
    (r'^logout/$', 'logout_view'),
    (r'^users/$', 'users'),
    (r'^users/(?P<user_id>[\w\-]+)/$', 'users'),
    (r'^groups/$', 'groups'),
    (r'^groups/(?P<group_id>[\w\-]+)/$', 'groups'),
    (r'^groups/(?P<group_id>[\w\-]+)/members/$', 'group_members'),
    (r'^groups/(?P<group_id>[\w\-]+)/add/(?P<member_id>[\w\-]+)/$', 'group_add'),
    (r'^groups/(?P<group_id>[\w\-]+)/remove/(?P<member_id>[\w\-]+)/$', 'group_remove'),
)
