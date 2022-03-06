from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^panel/news/category/list/$', views.category_list, name='category_list'),
    url(r'^panel/news/category/add/$', views.category_add, name='category_add'),
    url(r'^panel/news/category/delete/(?P<pk>\d+)/$', views.category_delete, name='category_delete'),
]
