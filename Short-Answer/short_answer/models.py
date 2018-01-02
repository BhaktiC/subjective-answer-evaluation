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

class QuestionBank(models.Model):
        question_text = models.CharField(max_length = 500)
        def __unicode__(self):
            return self.question_text

class Test(models.Model):
        test_code = models.CharField(max_length = 6, unique = True)
        question_nos = models.CharField(max_length = 20)
        date_created = models.DateTimeField(auto_now_add = True)
        created_by = models.ForeignKey(User, on_delete=models.CASCADE)
        def __unicode__(self):
            return self.test_code
