from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login

from .forms import AuthForm
from .util import runFlSsRpt

class flSs(View):
    def get(self, req):
        print("Check point:", "7")
        doc = runFlSsRpt()

        return HttpResponse(doc)
