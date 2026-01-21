import datetime
from django.db import models
from django.utils import timezone
#from .forms import AnswerForm
from .util import getRatingStr


#r = AnswerForm.RATINGS5

# Create your models here.

class Answer(models.Model):
    changedate = models.DateField(default=timezone.now)
    name = models.CharField(max_length=80)
    city_county = models.CharField(max_length=50)
    church_rating = models.IntegerField(default=0)
    #pastor_rating = models.IntegerField(default=0)
    comments = models.CharField(max_length=500, blank=True)
    demo_record = models.BooleanField(default = False)
    def __str__(self):
        tx = self.name + " from " + self.city_county + " rates " + str(getRatingStr(self.church_rating)) + " and says " + self.comments
        return tx

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    demo_record = models.BooleanField(default = False)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def fullSelf(self):
        return str(self.pub_date) + " " + self.question_text
    #str(id) + " " +

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    changedatetime = models.DateTimeField(default=timezone.now)
    demo_record = models.BooleanField(default = False)
    def __str__(self):
        return str(self.question) + "- " + self.choice_text
        #return question + " Answer- " + self.choice_text
 
class Response(models.Model):
    choice = models.ForeignKey(Choice, on_delete = models.CASCADE)
    name = models.CharField(max_length = 80, default = "Unknown")
    changedatetime = models.DateTimeField(default = timezone.now)
    texta = models.TextField(blank=True)
    demo_record = models.BooleanField(default = False)
    def __str__(self):
        return self.name + " chose " + str(self.choice) + " - " + self.texta

class Pick(models.Model):
    wsite_cd = models.CharField(max_length = 200)
    changedatetime = models.DateTimeField(default = timezone.now)
    item = models.CharField(max_length = 75)
    active = models.BooleanField(default = False)
    def __str__(self):
        return self.wsite_cd + " " + self.item + " " + str(self.changedatetime) + " " + str(self.active)