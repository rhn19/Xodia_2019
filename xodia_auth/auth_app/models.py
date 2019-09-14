# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=10)
    college_name = models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    gwon = models.IntegerField(default=0)
    glost = models.IntegerField(default=0)
    gdrawn = models.IntegerField(default=0)

    class Meta:
        ordering = ('-score',)

    def __str__(self):
        return self.user.username
