from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms




class UserProfile(models.Model):
        # ROLE_CHOICES = (
        #    ('Teacher', 'Teacher'),
        #    ('Student', 'Student')
        # )

        # This field is required.
        user = models.OneToOneField(User)
        # These fields are optional
        isStudent = models.BooleanField()
        def __unicode__(self):
                return self.user.username
