from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice
from .forms import AuthForm, AddChoiceForm
from .util import getQuestions, runLogRpt

class LogIn(View):
    def get(self, req):
        print("Check point:", "6")
        form = AuthForm()
        tmplt = loader.get_template("survey/store_pre.html")
        context = {"form": form}
        return HttpResponse(tmplt.render(context, req))

    def post(self, req):
        pst = req.POST
        form = AuthForm(pst)
        if form.is_valid():
            unm = pst.get("uname")
            pw = pst.get("pword")
            u = authenticate(req, username = unm, password = pw)
            ctx = { "unm": unm }
            #except Exception as x:
            #    print("Error:", x, "Check point:", ckpt)
            if u is not None:
                f = open("survey/meta.log", "w")
                for r in req.META:
                    f.write(r + ": " + str(req.META.get(r)) + "\n")
                f.close()
                print("Check point:", "6.7")
                login(req, u)
                #return HttpResponseRedirect("You got this hit.")
            else:
                return HttpResponse("<html><h2><center>User with name or password does not exists.</html>")

        print("Check point:", "6.9", str(u))
        tmplt = loader.get_template("survey/adm.html")
        return HttpResponse(tmplt.render(ctx, req))

#class AddChoice(View):
class AddChoice(LoginRequiredMixin, TemplateView):
    raise_exception = True
    #@login_required
    def get(self, req):
        form = AddChoiceForm()
        form.fields["question"].choices = getQuestions()
        tmplt = loader.get_template("survey/add_choice.html")
        ctx = { "form": form }

        return HttpResponse(tmplt.render(ctx, req))

    #@login_required
    def post(self, req):
        pst = req.POST
        form = AddChoiceForm(pst)
        form.fields["question"].choices = getQuestions()
        if form.is_valid():
            quest_id = pst.get("question")
            #print("quest_id type:", type(quest_id))
            nm = pst.get("name")
            c = Choice(question_id = int(quest_id), choice_text = nm )
            c.save()
        else:
            print("Not a valid form.")

        return HttpResponseRedirect("/survey/addchoice/")

# def gotLog(req):
    #PENDING
    # runLogRpt()
    # fl = open("ngxlog.txt", "r")

