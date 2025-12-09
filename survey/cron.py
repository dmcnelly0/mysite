#from /home/ec2-user/mysite.survey.models import Pick
#from /home/ec2-user/mysite.survey.util import runFind

def run_():
   ckpt = "C0"
   try:
      ckpt = "C1"
      import psycopg2
      ckpt = "C1.3"
      from mysite import utl
      ckpt = "C1.5"
      from survey.util import runFind, convertDat
      tok = utl.getTok()
      specs = {
         "dbname": "postgres",
         "user": "postgres",
         "password": tok,
         "port": 5432,
         "host": "db-django1.czoou22skoun.us-east-2.rds.amazonaws.com"
         }
      ckpt = "C1.7"
      con = psycopg2.connect(**specs)
      print("con:", con)
      cur = con.cursor()
      q = "select wsite_cd, item from survey_pick where active = true order by changedatetime desc"
      cur.execute(q)
      res = cur.fetchall()
      print("Check point:", ckpt)
      # Get the latest active record.
      wsite_cd = res[0][0]
      item = res[0][1]
      ckpt = "C1.9"
      cur.close()
      print("Check point:", ckpt)
      ############################################################
      q = "select cd, name from survey_puzzle where cd != 'Door'"
      cur = con.cursor()
      ckpt = "C1.93"
      cur.execute(q)
      ckpt = "C1.97"
      dat = cur.fetchall()
      print("dat:", dat)
      ckpt = "C1.98"
      emlDict = convertDat(dat)
      ckpt = "C1.99"
      cur.close()
      ############################################################
      ckpt = "C2"
      print("Values-", wsite_cd, item)
      fRan = open("didrun.out", "a")
      fRan.write("Job ran- " + item)
      fRan.close()
      ckpt = "C2.5"
      print("con:", con)
      ckpt = "C3"
      runFind(item, wsite_cd, emlDict)
      con.close()
   except Exception as x:
      fWrite = open("CronErr.out", "w")
      fWrite.write("Error at " + ckpt + ": " + str(x) + "\n")
      fWrite.close()

if __name__ == "__main__":
   run_()