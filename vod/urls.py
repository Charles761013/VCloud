from django.conf.urls import url
from django.conf import settings
from vod import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^personal_videos$', views.personal_videos, name='personal_videos'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^search$', views.search, name='search'),
    url(r'^videoplay$', views.videoplay, name='videoplay'),
    url(r'^like_video/$', views.like_video, name='like_video'),
    url(r'^delete_video/$', views.delete_video, name='delete_video'),
    url(r'^review/$', views.review, name='review')

]

