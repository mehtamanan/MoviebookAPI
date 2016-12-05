# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 03:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.CharField(blank=True, max_length=200, null=True)),
                ('movie_id', models.CharField(max_length=20)),
                ('caption', models.CharField(blank=True, max_length=200, null=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('followers', models.ManyToManyField(blank=True, null=True, related_name='following', to='userprofiles.UserProfile')),
                ('followings', models.ManyToManyField(blank=True, null=True, related_name='follower', to='userprofiles.UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='userprofiles.UserProfile'),
        ),
    ]
