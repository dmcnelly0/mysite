from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required

from .util import runFlSsRpt

class flSs(View):
    @login_required
    def get(self, req, unm):
        print("Check point:", "7", unm)
        doc = runFlSsRpt()

        return HttpResponse(doc)
