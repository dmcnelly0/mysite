from .models import Pick
from .util import runFind

def cronRun():
   # Get the latest active record.
   pick = Pick.objects.filter(active = True).order_by("changedatetime").reverse()
   print(pick[0])
   runFind(pick[0].item, pick[0].wsite_cd)
