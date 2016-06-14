import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vod_system.settings")
import django
django.setup()

from datetime import timedelta
from django.contrib.auth.models import User
from vod.models import Video, Review


def populate(user):
    for i in range(5):
        video_instance = add_video(user=user,
            title='test video' + str(i),
            description='this is first video' + str(i) + ' created by populate',
            duration=timedelta(seconds=500+i),
            views=100+i)
        for y in range(5):
            add_review(user=user,
                video=video_instance,
                text='review' + str(y),
                likes=y)


def add_review(user, video, text, likes):
    r = Review.objects.get_or_create(user=user, video=video, text=text, likes=likes)[0]
    r.user = user
    r.video = video
    r.text = text
    r.likes = likes
    r.save()
    return r


def add_video(user, title, description, duration, views):
    v = Video.objects.get_or_create(user=user, title=title,
                                    description=description, duration=duration, views=views)[0]
    v.user = user
    v.title = title
    v.description = description
    v.duration = duration
    v.views = views
    v.save()
    return v


if __name__ == '__main__':
    print "Starting vod population script..."
    user = User.objects.first()
    populate(user)