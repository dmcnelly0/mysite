from django.http import HttpResponse
from django.views import View

from .util import runFlSsRpt

class flSs(View):
    def get(self, req):
        print("Check point:", "7")
        doc = runFlSsRpt()

        return HttpResponse(doc)
