from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        isStudent = models.BooleanField()
        def __unicode__(self):
                return self.user.username

class QuestionBank(models.Model):
        question_text = models.CharField(max_length = 500)
        train_file = models.CharField(max_length = 50)
        def __unicode__(self):
            return self.question_text

class Test(models.Model):
        test_code = models.CharField(max_length = 6, unique = True)
        question_nos = models.CharField(max_length = 20)
        date_created = models.DateTimeField(auto_now_add = True)
        created_by = models.ForeignKey(User, on_delete=models.CASCADE)
        def __unicode__(self):
            return self.test_code


class Test_Result(models.Model):
        test = models.ForeignKey(Test, on_delete = models.CASCADE)
        user_email = models.CharField(max_length = 50, unique = False)
        test_marks = models.CharField(max_length = 50)
        reload_count = models.CharField(max_length = 10)
        back_pressed = models.CharField(max_length = 10)
        tab_switch_count = models.CharField(max_length = 10)
        def __unicode__(self):
            return self.test.test_code
