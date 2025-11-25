#from /home/ec2-user/mysite.survey.models import Pick
#from /home/ec2-user/mysite.survey.util import runFind

def run_():
   ckpt = "0"
   try:
      ckpt = "1"
      from survey.models import Pick
      from survey.util import runFind
      # Get the latest active record.
      ckpt = "2"
      pick = Pick.objects.filter(active = True).order_by("changedatetime").reverse()
      print(pick[0])
      ckpt = "3"
      runFind(pick[0].item, pick[0].wsite_cd)
   except Exception as x:
      fWrite = open("Err.out", "a")
      fWrite.write("Error at " + ckpt + ": " + str(x) + "\n")
      fWrite.close()

# if __name__ == "__main__":
   # run_()