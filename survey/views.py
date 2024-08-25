from datetime import datetime
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import Answer
from .forms import AnswerForm

# Create your views here.

def index(req):
    #return HttpResponse("<html><h2>Hi there!!! I'm Snoop Dougie Doug</h2></html>")
    f = open("reqinfo.log", "a")
    f.write("Date and Time: " + str(datetime.now()) + "\n")
    f.write("REMOTE_ADDR: " + str(req.META.get('REMOTE_ADDR')) + "\n")
    f.write("REMOTE_HOST: " + str(req.META.get('REMOTE_HOST')) + "\n")
    f.write("HTTP_REFERER: " + str(req.META.get('HTTP_REFERER')) + "\n")
    f.close()
    tmplt = loader.get_template("survey/index1.html")
    return HttpResponse(tmplt.render())

class AddAnswer(View):
    def get(self, req):
        form = AnswerForm()
        tmplt = loader.get_template("survey/answer_add.html")
        context = {"form": form}
        return HttpResponse(tmplt.render(context, req))

    def post(self, req):
        pst = req.POST
        form = AnswerForm(pst)
        if form.is_valid():
           nm = pst.get("name")
           place = pst.get("city_county")
           church = pst.get("church_rating")
           #pastor = pst.get("pastor_rating")
           comments = pst.get("comments")
           a = Answer(name = nm, city_county = place, church_rating = church, comments = comments)
           a.save()
        else:
           print("Not a valid form.")

        return HttpResponse("<html><h2><center>Thank you for your responce</html>")
           #("<html><h2>Hi there!!! I'm Snoop Dougie Doug</h2></html>")

def list(req):
    ans = Answer.objects.order_by("pk")
    tmplt = loader.get_template("survey/list.html")
    ctx = { "answer": ans, }

    return HttpResponse(tmplt.render(ctx))
