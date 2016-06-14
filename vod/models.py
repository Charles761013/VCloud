from __future__ import unicode_literals

from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User


class Video(models.Model):
    user = models.ForeignKey(User, verbose_name='video_user', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    upload_date = models.DateField(auto_now_add=True)
    duration = models.DurationField(default=timedelta())
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, verbose_name='user_reviews', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name='video_reviews', on_delete=models.CASCADE)
    text = models.CharField(max_length=512, null=True)
    likes = models.BooleanField()

    def __unicode__(self):
        return self.text

class LikeReview(models.Model):
    user = models.ForeignKey(User, verbose_name='user_likes', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, verbose_name='review_likes', on_delete=models.CASCADE)
    likes = models.BooleanField()

    def __unicode__(self):
        if self.review != None:
            return self.review
        else:
            return self.likes



