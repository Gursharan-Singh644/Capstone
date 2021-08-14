# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class fundraiser(models.Model):
    fundraiser_id = models.AutoField(primary_key=True)
    fundraiser_name = models.CharField(max_length=255, default = '')
    fundraiser_type_id = models.CharField(max_length=255, default = "")
    fundraiser_user_id = models.CharField(max_length=255, default = "")
    fundraiser_goal = models.CharField(max_length=255, default = "")
    fundraiser_image = models.CharField(max_length=255, null = True)
    fundraiser_description = models.TextField(default = "")
    fundraiser_from_date = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.fundraiser_name    
