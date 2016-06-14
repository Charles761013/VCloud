from django.conf.urls import url
from vod import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^personal_videos$', views.personal_videos, name='personal_videos'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^search$', views.search, name='search'),


]