# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-15 16:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vod', '0003_video_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_videolikes')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vod.Video', verbose_name='video_likes')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=512, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='review',
            name='likes',
        ),
        migrations.AlterField(
            model_name='likereview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_reviewlikes'),
        ),
        migrations.AlterUniqueTogether(
            name='likereview',
            unique_together=set([('user', 'review')]),
        ),
        migrations.AddField(
            model_name='responsereview',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vod.Review', verbose_name='review_response'),
        ),
        migrations.AddField(
            model_name='responsereview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_response'),
        ),
        migrations.AlterUniqueTogether(
            name='likevideo',
            unique_together=set([('user', 'video')]),
        ),
    ]
