from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^login/$', views.mylogin, name='mylogin'),
    url(r'^logout/$', views.mylogout, name='mylogout'),
    url(r'^register/$', views.registeruser, name='registeruser'),
    url(r'^forgot-password/$', views.forgot_password, name='forgot_password'),
    url(r'^panel/admin/$', views.admin_panel, name='admin_panel'),
    url(r'^panel/settings/$', views.mysettings, name='mysettings'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^panel/change-password/$', views.change_password, name='change_password'),
]
