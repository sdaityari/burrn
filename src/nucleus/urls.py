from django.conf.urls import patterns

urlpatterns = patterns ('nucleus.views',
    (r'^login/$', 'login_view'),
    (r'^logout/$', 'logout_view'),
    (r'^users/$', 'users'),
    (r'^users/(?P<user_id>[\w\-]+)/$', 'users'),
    (r'^users/(?P<contact>.+?)/$', 'users_contact'),
    (r'^groups/$', 'groups'),
    (r'^groups/(?P<group_id>[\w\-]+)/$', 'groups'),
    (r'^groups/(?P<group_id>[\w\-]+)/members/$', 'group_members'),
    (r'^groups/(?P<group_id>[\w\-]+)/add/(?P<member_id>[\w\-]+)/$', 'group_add'),
    (r'^groups/(?P<group_id>[\w\-]+)/remove/(?P<member_id>[\w\-]+)/$', 'group_remove'),
    (r'^posts/$', 'posts'),
    (r'^posts/(?P<post_id>[\w\-]+)/$', 'posts'),
    (r'^posts_about_me/$', 'posts_about_me'),
    (r'^posts/(?P<post_id>[\w\-]+)/comments/$', 'post_comments'),
    (r'^posts/(?P<post_id>[\w\-]+)/comments/(?P<comment_id>[\w\-]+)/$', 'post_comments'),
)
