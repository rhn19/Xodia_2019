# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length = 50, blank = True)
    college_name = models.CharField(max_length = 20, blank = True)
    score = models.IntegerField(default = 0)

    class Meta:
        ordering = ('-score',)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender = User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
    else:
        instance.profile.save()
