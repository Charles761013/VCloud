from __future__ import unicode_literals

from django.db import models
from datetime import timedelta, date
from django.contrib.auth.models import User


class Video(models.Model):
    user = models.ForeignKey(User, verbose_name='video_user', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    upload_date = models.DateField(auto_now_add=True)
    duration = models.DurationField(default=timedelta())
    views = models.IntegerField(default=0)
    url = models.URLField(null=True)

    def __unicode__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, verbose_name='user_reviews', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name='video_reviews', on_delete=models.CASCADE)
    text = models.CharField(max_length=512, null=True)
    date = models.DateField(auto_now=True, null=True)

    def __unicode__(self):
        return self.text

class LikeVideo(models.Model):
    user = models.ForeignKey(User, verbose_name='user_videolikes', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name='video_likes', on_delete=models.CASCADE)
    likes = models.BooleanField()

    class Meta:
        unique_together = ('user', 'video',)

    def __unicode__(self):
        return str(self.likes)

class ResponseReview(models.Model):
    user = models.ForeignKey(User, verbose_name='user_response', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, verbose_name='review_response', on_delete=models.CASCADE)
    response = models.CharField(max_length=512, null=True)
    date = models.DateField(auto_now=True, null=True)

    def __unicode__(self):
        return self.response

class LikeReview(models.Model):
    user = models.ForeignKey(User, verbose_name='user_reviewlikes', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, verbose_name='review_likes', on_delete=models.CASCADE)
    likes = models.BooleanField()

    class Meta:
        unique_together = ('user', 'review',)

    def __unicode__(self):
        return str(self.likes)



