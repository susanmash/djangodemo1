from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.index),
    url(r'^all_quotes$', views.quotes),
    url(r'^guest_quotes$', views.guestQuotes),
    url(r'^register$', views.register),
    url(r'^loginForm$', views.loginForm),
    url(r'^login$', views.login),
    url(r'^logout$', views.log_out),
]
