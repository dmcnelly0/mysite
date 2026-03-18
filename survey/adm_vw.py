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
    def get(self, req, pageId):
        print("Check point:", "6")
        form = AuthForm()
        tmplt = loader.get_template("survey/store_pre.html")
        context = { "form": form, "pgId": pageId }
        return HttpResponse(tmplt.render(context, req))

    def post(self, req, pageId):
        ckpt = "6.1"
        try:
            pst = req.POST
            form = AuthForm(pst)
            if form.is_valid():
                ckpt = "6.2"
                unm = pst.get("uname")
                pw = pst.get("pword")
                u = authenticate(req, username = unm, password = pw)
                ctx = { "unm": unm }
                #except Exception as x:
                #    print("Error:", x, "Check point:", ckpt)
                if u is not None:
                    ckpt = "6.3"
                    f = open("survey/meta.log", "w")
                    for r in req.META:
                        f.write(r + ": " + str(req.META.get(r)) + "\n")
                    f.close()
                    ckpt = "6.4"
                    login(req, u)
                    #return HttpResponseRedirect("You got this hit.")
                else:
                    return HttpResponse("<html><h2><center>User with name or password does not exists.</html>")

            ckpt = "6.5"
            if pageId == 0:
                tmplt = loader.get_template("survey/adm.html")
                return HttpResponse(tmplt.render(ctx, req))
            if pageId == 1:
                return HttpResponseRedirect("/survey/" + unm + "/pick/")

            ckpt = "6.6"
        except Exception as x:
            print("LogIn method error:", x, "Check point:", ckpt)

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

