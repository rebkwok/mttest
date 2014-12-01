from django.conf.urls import patterns, include, url
from webreport import views

urlpatterns = patterns('',
    url(r'^$', views.get_url),
)