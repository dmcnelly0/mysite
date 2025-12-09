#from /home/ec2-user/mysite.survey.models import Pick
#from /home/ec2-user/mysite.survey.util import runFind
from cryptography.fernet import Fernet

def getDoor(con):
    q = "select name from survey_puzzle where cd = 'Door'"
    cur = con.cursor()
    cur.execute(q)
    dat = cur.fetchall()
    cur.close()
    return dat[0][0]

def convertDat(ls, con):
    fnt = Fernet(getDoor(con))
    dct = { }
    pos1st = 0
    pos2nd = 1
    # Convert data and put it into a dictionary (hash map).
    for i in range(0, len(ls)):
        bin = fnt.decrypt(ls[i][pos2nd])
        dct[ ls[i][pos1st] ] = bin.decode("utf-8")
    return dct

def run_():
   ckpt = "C0"
   try:
      ckpt = "C1"
      import psycopg2
      ckpt = "C1.3"
      from mysite import utl
      ckpt = "C1.5"
      from survey.util import runFind#, convertDat
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
      ckpt = "C1.92"
      cur.execute(q)
      ckpt = "C1.94"
      dat = cur.fetchall()
      ckpt = "C1.96"
      cur.close()
      #print("dat:", dat)
      print("Type dat:", type(dat))
      ckpt = "C1.98"
      emlDict = convertDat(dat, con)
      con.close()
      ############################################################
      ckpt = "C2"
      print("Values-", wsite_cd, item)
      fRan = open("didrun.out", "a")
      fRan.write("Job ran- " + item)
      fRan.close()
      ckpt = "C2.5"
      #print("con:", con)
      ckpt = "C3"
      runFind(item, wsite_cd, emlDict)
   except Exception as x:
      fWrite = open("CronErr.out", "w")
      fWrite.write("Error at " + ckpt + ": " + str(x) + "\n")
      fWrite.close()

if __name__ == "__main__":
   run_()
