from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^contact/submit/$', views.contact_add, name='contact_add'),
    url(r'^panel/contact/list/$', views.contact_list, name='contact_list'),
    url(r'^panel/contact/delete/(?P<pk>\d+)/$', views.delete_contact, name='delete_contact'),
]
