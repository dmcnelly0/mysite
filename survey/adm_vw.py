from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login

from .forms import AuthForm

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
            #except Exception as x:
            #    print("Error:", x, "Check point:", ckpt)
            if u is not None:
                print("Check point:", "6.7")
                login(req, u)
                #return HttpResponseRedirect("You got this hit.")
            else:
                return HttpResponse("<html><h2><center>User with name or password does not exists.</html>")

        print("Check point:", "6.9", str(u))
        tmplt = loader.get_template("survey/adm.html")
        return HttpResponse(tmplt.render())
