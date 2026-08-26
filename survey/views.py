from datetime import datetime
#from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
#from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
#import django.contrib.auth.models.User

from .models import Answer, Question, Response, Pick
from .forms import AnswerForm, ChoiceForm, FileForm, PickerForm #, AddChoiceForm ChoiceFormAnlz1
from .util import getChoices, getQuestionText, getResponses, runFind

# Create your views here.

def index(req):
   #return HttpResponse("<html><h2>Hi there!!! I'm Snoop Dougie Doug</h2></html>")
   f = open("reqinfo.log", "a")
   f.write("Date and Time: " + str(datetime.now()) + "\n")
   f.write("REMOTE_ADDR: " + str(req.META.get('REMOTE_ADDR')) + "\n")
   f.write("REMOTE_HOST: " + str(req.META.get('REMOTE_HOST')) + "\n")
   f.write("HTTP_REFERER: " + str(req.META.get('HTTP_REFERER')) + "\n")
   f.write("USERNAME: " + str(req.META.get('USERNAME')) + "\n")
   f.close()
   #usr = models.User.objects.get(username="dmcnelly")
   #print("Authenticated:", usr.is_authenticated)
   tmplt = loader.get_template("survey/index.html")
   return HttpResponse(tmplt.render())

class AddAnswer(View):
   def get(self, req):
      form = AnswerForm()
      print("Valid:", form.is_valid())
      tmplt = loader.get_template("survey/answer_add.html")
      context = {"form": form}
      return HttpResponse(tmplt.render(context, req))

   def post(self, req):
      pst = req.POST
      form = AnswerForm(pst)
      print("Valid:", form.is_valid())
      if form.is_valid():
         nm = pst.get("name")
         place = pst.get("city_county")
         church = pst.get("church_rating")
         #pastor = pst.get("pastor_rating")
         comments = pst.get("comments")
         a = Answer(name = nm, city_county = place, church_rating = church
            , comments = comments, demo_record = False)
         a.save()
      else:
         print("Not a valid form.")

      return HttpResponse("<html><h2><center>Thank you for your responce</html>")

def list(req):
   ans = Answer.objects.order_by("pk")
   print("ans type:", type(ans))
   tmplt = loader.get_template("survey/list.html")
   ctx = { "answer": ans, }

   return HttpResponse(tmplt.render(ctx))

def pollHome(req):
   try:
      print("Check point:", "1")
      quest = Question.objects.all() #("question_text")
      tmplt = loader.get_template("survey/poll_listd.html")
      ctx = { "quest": quest }
   except:
      import traceback
      from .util import rptXpn
      rptXpn(traceback.format_exc() + "\n")
      return HttpResponse("<html><h2><center>Oops, something went wrong.</html>")

   return HttpResponse(tmplt.render(ctx))

def choice(req, question_id):
   print("Check point:", "1.3", "req:", type(req))
   if req.method == "POST":
      pst = req.POST
      form = ChoiceForm(pst)
      form.fields["choice_"].choices = getChoices(question_id)
      #print("Valid:", form.is_valid(), "form:", form)
      if form.is_valid():
         nm = pst.get("name")
         chce = pst.get("choice_")
         #print("Check point:", "5.1", "chce:", chce)
         r = Response(name = nm, choice_id = chce, texta = "x", demo_record = False)
         r.save()
      else:
         print("Check point:", "5.5", "Not a valid form.")
      return HttpResponseRedirect("/survey/poll/")
   else:
      ckpt = "2"
      try:
         print("Check point:", ckpt)
         form = ChoiceForm() #ChoiceFormAnlz1()
         form.fields["choice_"].choices = getChoices(question_id)
         quest_text = getQuestionText(question_id)
         form.fields["choice_"].label = quest_text
         tmplt = loader.get_template("survey/choice.html")
         ckpt = "3"
         print("Check point:", ckpt)
         ctx = { "form": form, "quest_id": question_id } #, "quest_text": quest_text }
      except Exception as x:
         print("Inner Error:", x, "Check point:", ckpt)

   print("Check point:", "4")
   return HttpResponse(tmplt.render(ctx, req))

def uploadFile(req):
   if req.method == "POST":
      form = FileForm(req.POST, req.FILES)
      if form.is_valid():
         print("Check point:", "7.4", "Type:", type(req.FILES["file"]))
         handleFile(req.FILES["file"])
         return HttpResponseRedirect("/survey/")
      else:
         return HttpResponse("NOT VALID FORM")
   else:
      print("Check point:", "7")
      form = FileForm()
      tmplt = loader.get_template("survey/upload.html")
      ctx = { "form": form }

   return HttpResponse(tmplt.render(ctx, req))

def handleFile(fil):
   with open(fil.name, "wb+") as dest:
      print("Check point:", "7.5")
      for chunk in fil.chunks():
         dest.write(chunk)

def respRpt(req):
   resp = getResponses()
   #print(resp)
   tmplt = loader.get_template("survey/responses.html")
   ctx = { "responses": resp, }

   return HttpResponse(tmplt.render(ctx))


#########################################################################################

# Project Name: "Picker"

# Project Description: An Application for Iphone and Android and other platforms that
# utilizes a AI driven Large Language Model scrap based on a customer driven fillable
# taxonomy that allows the customer to receive an alert when a particular item is placed
# for sale on the web across multiple websites which serve as data sources like: Craigslist,
# Bring a Trailer, ebay, Facebook marketplace etc.

def pList(req):
   ckpt = "3"
   try:
      # print("Check point:", ckpt)
      # pick = Pick.objects.order_by("changedatetime").reverse()
      ckpt = "3.3"
      print("Check point:", ckpt)
      tmplt = loader.get_template("survey/pickrpt.html")
      # ckpt = "3.5"
      # print("Check point:", ckpt)
      # ctx = { "hist": pick, }
      ckpt = "3.7"

   except Exception as x:
      print("Inner Error:", x, "Check point:", ckpt)

   print("Check point:", ckpt)
   return HttpResponse(tmplt.render())

@login_required
def picker(req, unm):
   if req.method == "POST":
      res = ""
      pst = req.POST
      form = PickerForm(pst)
      print("Valid:", form.is_valid())
      if form.is_valid():
         wsite = form.cleaned_data.get("website")
         print("wsite:", wsite)
         item = pst.get("item")
         autorun = form.cleaned_data.get("autorun")
         print("autorun:", autorun, type(autorun))
         if autorun:
            Pick.objects.filter(active = True).update(active = False)
            res = "The results of your query should arrive after next automatic run."
         p = Pick(wsite_cd = wsite, item = item, active = autorun)
         p.save()
         sim = form.cleaned_data.get("simulate")
         if not autorun:
            if sim:
              res = "An email will NOT arrive because you chose Simulate Mode."
            else:
              res = "An email should arrive shortly."
            print("autorun:", autorun)
            runFind(item, wsite, None, sim)
      return HttpResponse("<html><h2><center>" + res + "</html>")
   else:
      form = PickerForm()
      pick = Pick.objects.order_by("changedatetime").reverse()
      ctx = {"form": form, "hist": pick, "uNm": unm}
      tmplt = loader.get_template("survey/picker.html")

   return HttpResponse(tmplt.render(ctx, req))

def helpPicker(req):
   if req.method == "POST":
      print("Oops .. somehow POST method was called")
   else:
      tmplt = loader.get_template("survey/help_picker.html")
      
   return HttpResponse(tmplt.render())
