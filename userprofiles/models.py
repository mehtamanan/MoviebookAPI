
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name = 'profile')
    bio = models.TextField(blank = True, null = True)
    birth_date = models.DateField(blank = True, null = True)
    followings = models.ManyToManyField('self', related_name = 'followers', symmetrical=False,
                                        blank = True, null = True)
    blocked = models.ManyToManyField('self', related_name = 'blockedby', symmetrical=True,
                                     blank = True, null = True)
    following_count = models.IntegerField(default=0, blank = True, null = True)
    follower_count = models.IntegerField(default=0, blank = True, null = True)

    def __unicode__(self):
        return self.user.username

    def isFollowing(self, username):
        return self.followings.filter(user__username=username).exists()

    def isFollowedBy(self, username):
        return self.followers.filter(user__username=username).exists()

    def isBlocked(self, username):
        return self.blocked.filter(user__username=username).exists()

    def block(self, username):
        if self.isBlocked(username):
            return False
        else:
            other = User.objects.get(username=username).profile
            self.blocked.add(other)
            self.unfollow(other)
            other.unfollow(self)
            self.save()
            return True

    def unblock(self, username):
        if self.isBlocked(username):
            other = self.blocked.get(user__username=username)
            self.blocked.remove(other)
            self.save()
            other.save()
            return True
        else:
            return False

    def follow(self, username):
        if self.isFollowing(username) or self.isBlocked(username):
            return False
        else:
            other = User.objects.get(username=username).profile
            self.followings.add(other)
            self.following_count = self.followings.all().count()
            self.follower_count = self.followers.all().count()
            other.following_count = other.followings.all().count()
            other.follower_count = other.followers.all().count()
            other.save()
            self.save()
            return True

    def unfollow(self, username):
        if self.isFollowing(username):
            other = self.followings.get(user__username=username)
            self.followings.remove(other)
            self.following_count = self.followings.all().count()
            self.follower_count = self.followers.all().count()
            other.following_count = other.followings.all().count()
            other.follower_count = other.followers.all().count()
            other.save()
            self.save()
            return True
        else:
           return False
    
class Post(models.Model):
    owner = models.ForeignKey(UserProfile, related_name = 'post')
    movie_title = models.CharField(max_length = 200, null = True, blank = True)
    movie_id = models.CharField(max_length = 20)
    caption = models.CharField(max_length = 200, blank = True, null = True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.movie_title
