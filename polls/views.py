from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Question
import os

# Create your views here.

def home(req):
    quest = Question.objects.all() #("question_text")
    tmplt = loader.get_template("polls/index.html")
    ctx = { "quest": quest }

    #return HttpResponse("hear this " + str(quest) + " " + os.getcwd())
    return HttpResponse(tmplt.render(ctx))

def choose_(req, question_id):
    return HttpResponse("This is where you choose.")


#def list(req):
