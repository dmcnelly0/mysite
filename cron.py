#from /home/ec2-user/mysite.survey.models import Pick
#from /home/ec2-user/mysite.survey.util import runFind
from cryptography.fernet import Fernet

def connDB():
   import psycopg2
   from mysite import utl
   tok = utl.getTok()
   specs = {
      "dbname": "postgres",
      "user": "postgres",
      "password": tok,
      "port": 5432,
      "host": "db-django1.czoou22skoun.us-east-2.rds.amazonaws.com"
      }
   con = psycopg2.connect(**specs)

   return con

def getEmlInfo(con):
   q = "select cd, name from survey_puzzle where cd != 'Door'"
   cur = con.cursor()
   cur.execute(q)
   dat = cur.fetchall()
   cur.close()

   return dat

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
      from survey.util import runFind
      # Establish database connection
      conn = connDB()
      print("conn:", conn)
      # Query picker sites and item
      q = "select wsite_cd, item from survey_pick where active = true order by changedatetime desc"
      cur = conn.cursor()
      cur.execute(q)
      rec = cur.fetchall()
      # Get the latest active record.
      wsite_cd = rec[0][0]
      item = rec[0][1]
      cur.close()
      ############################################################
      ckpt = "C1.3"
      print("Check point:", ckpt)
      # Get email info
      dat = getEmlInfo(conn)
      #print("dat:", dat)
      print("Type dat:", type(dat))
      ckpt = "C1.7"
      emlDict = convertDat(dat, conn)
      conn.close()
      ############################################################
      ckpt = "C2"
      print("Values-", wsite_cd, item)
      fRan = open("didrun.out", "a")
      fRan.write("Job ran- " + item)
      fRan.close()
      ckpt = "C3"
      runFind(item, wsite_cd, emlDict)
   except Exception as x:
      fWrite = open("CronErr.out", "w")
      fWrite.write("Error at " + ckpt + ": " + str(x) + "\n")
      fWrite.close()

if __name__ == "__main__":
   run_()