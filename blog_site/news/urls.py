from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^news/(?P<word>.*)/$', views.news_detail, name='news_detail'),
    url(r'^panel/news/list/$', views.news_list, name='news_list'),
    url(r'^panel/news/add/$', views.news_add, name='news_add'),
    url(r'^panel/news/error/$', views.error_news, name='error_news'),
    url(r'^panel/news/edit/(?P<pk>\d+)/$', views.news_edit, name='news_edit'),
    url(r'^panel/news/delete/(?P<pk>\d+)/$', views.delete_news, name='delete_news'),
]
