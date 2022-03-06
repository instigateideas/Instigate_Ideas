from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^panel/news/subcategory/list/$', views.subcategory_list, name='subcategory_list'),
    url(r'^panel/news/subcategory/add/$', views.subcategory_add, name='subcategory_add'),
    url(r'^panel/news/subcategory/delete/(?P<pk>\d+)/$', views.subcategory_delete, name='subcategory_delete'),
]
