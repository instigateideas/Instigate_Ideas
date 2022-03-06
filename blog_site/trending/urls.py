from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^panel/trending/$', views.add_trending, name='add_trending'),
    url(r'^panel/trending/delete/(?P<pk>\d+)/$', views.delete_trending, name='delete_trending'),
    url(r'^panel/trending/edit/(?P<pk>\d+)/$', views.edit_trending, name='edit_trending'),
]
