from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^panel/manager/list/$', views.manager_list, name='manager_list'),
    url(r'^panel/manager/delete/(?P<pk>\d+)/$', views.manager_delete, name='manager_delete'),
    url(r'^panel/manager/group/list/$', views.manager_group, name='manager_group'),
    url(r'^panel/manager/group/add/$', views.manager_group_add, name='manager_group_add'),
    url(r'^panel/manager/group/delete/(?P<pk>\d+)/$', views.manager_group_delete, name='manager_group_delete'),
    url(r'^panel/manager/groups/show/(?P<pk>\d+)/$', views.user_groups, name='user_groups'),
    url(r'^panel/manager/add/usertogroups/(?P<pk>\d+)/$', views.add_user_to_groups, name='add_user_to_groups'),
    url(r'^panel/manager/delete/usergroup/(?P<pk>\d+)/(?P<name>.*)/$', views.delete_user_groups, name='delete_user_groups'),
]
