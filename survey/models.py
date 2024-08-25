from django.db import models
from django.utils import timezone
from .forms import AnswerForm
from .util import getRatingStr


r = AnswerForm.RATINGS5

# Create your models here.

class Answer(models.Model):
    changedate = models.DateField(default=timezone.now)
    name = models.CharField(max_length=80)
    city_county = models.CharField(max_length=50, blank=True)
    church_rating = models.IntegerField(default=0)
    #pastor_rating = models.IntegerField(default=0)
    comments = models.CharField(max_length=500, blank=True)
    def __str__(self):
        tx = self.name + " from " + self.city_county + " rates " + str(getRatingStr(self.church_rating)) + " and says " + self.comments
        return tx
