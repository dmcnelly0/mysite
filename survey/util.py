import re, subprocess
from cryptography.fernet import Fernet
import smtplib
from email.message import EmailMessage
from django.db import connections
from .forms import AnswerForm

def getRatingStr(num):
   FIRST_TUP_VAL = 0
   SECOND_TUP_VAL = 1
   str = ""
   for row in AnswerForm.RATINGS5:
      if ( row[FIRST_TUP_VAL] == num ):
         str = row[SECOND_TUP_VAL]
         break
   return str

def getConn():
    return connections['default']

def getQuestionText(question_id):
    with getConn().cursor() as cur:
        q = "select question_text from survey_question where id = " + str(question_id)
        cur.execute(q)
        dat = cur.fetchall()
        for item in dat:
            itemStr = str(item).strip("(,)")
    try:
        questionText = itemStr
    except UnboundLocalError as ulx:
        return "No record found."

    return questionText

def getQuestions():
    with getConn().cursor() as cur:
        q = "select id, question_text from survey_question where demo_record = false order by question_text"
        cur.execute(q)
        dat = cur.fetchall()
        # Add hint add head of list.
        dat.insert(0, (-1, "<Pick question>"))
    return dat

def getChoices(quest_id):
    with getConn().cursor() as cur:
        q = "select id, choice_text from survey_choice where demo_record = false and question_id = " + str(quest_id)
        cur.execute(q)
        dat = cur.fetchall()
    return dat

def getResponses():
    with getConn().cursor() as cur:
        q = "select r.name, q.question_text, c.choice_text, to_char(r.changedatetime, 'YYYY-fmMM-fmDD HH:MIam') change_time, r.demo_record"
        q += " from survey_choice c right join survey_question q on c.question_id = q.id left join survey_response r on c.id = r.choice_id"
        q += " where r.demo_record = false"
        q += " order by r.changedatetime desc, c.changedatetime desc"
        cur.execute(q)
        dat = cur.fetchall()
    return dat

def runFlSsRpt():
    FIRSTCOL = 0
    FIFTHCOL = 4
    head = "<html><body><h2><center>Store</center>"
    sub = subprocess.run(["./store.sh"], shell=True)
    print("Check point:", "50.0", "Shell script status:", sub)
    fl = open("df.out", "r")
    lin = []
    rpt = "<br>"
    #i = 0
    firstRow = True
    for ln in fl:
        if firstRow == False:
            col = re.split("\\s+", ln)
            ss = col[FIRSTCOL]
            u = col[FIFTHCOL]
            rpt += ss + "&emsp;" + u + "<br>"
            #lin.append(ln)
            #i += 1
            print(ln)
        else:
            print("Not showing column titles.")
        firstRow = False

    foot = "</body></html>"

    return head + rpt + foot
 
def runLogRpt():
   print("PENDING")
   # sub = subprocess.run(["./ngxlog.sh"], shell=True)

#########################################################################################
# Project Name: "Picker"

# class InvalidChoice(Exception):
   # def __init__(self, message="Invalid choice."):
       # self.message = message
       # super().__init__(self.message)

import requests
from rapidfuzz import fuzz

def sendEmail():
   ckpt = "1"
   try:
      msg = EmailMessage()
      msg['Subject'] = 'Project Test Email'
      msg['From'] = 'dsmcnelly@gmail.com'
      msg['To'] = 'trulyrural@aol.com'
      msg.set_content('Hi Chris, This is a test email sent from Python.')
      ckpt = "2"
      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: # Replace with your SMTP server and port
          # uwrr fsgg fcwn mxch
          smtp.login('dsmcnelly@gmail.com', 'uwrrfsggfcwnmxch') # Replace with your credentials
          smtp.send_message(msg)
   except Exception as x:
      print("Error:", x, "Check point:", ckpt)

def runFind(item, wsite):
   noMtchCt = flagIfItem(item, True, wsite)
   print("noMtchCt", noMtchCt)
   flagIfItem(item, False, wsite)

def flagIfItem(item):
   #item = "greengobbler"
   #url = "https://www.amazon.com/s?k=" + item
   url = "https://www.ebay.com/sch/i.html?_nkw=" + item
   print("URL:", url)
   f = open("Ebay.txt", "w")
   res = requests.get(url)
   i = 0
   for ln in res:
      #i += 1
      #print(i)
      row = str(ln)
      #f.write(row)
      wlist = row.split()
      f.write(str(wlist) + "\n")
      for w in wlist:
         if fuzz.token_sort_ratio(w.lower(), item) == 100:
            i += 1
            print(w)

   print("Hits:", i)
   f.close()

   #return url

# Overloaded to give option to create text file of web page or read text file and scrape.
def flagIfItem(item, wrMode, webSite):
   noMatchCnt = -1
   filenm = ""
   #url = ""
   hits = 0
   if wrMode:
      if webSite == "A":
         filenm = "amazon.txt"
         url = "https://www.amazon.com/s?k=" + item
      elif webSite == "E":
         filenm = "ebay.txt"
         url = "https://www.ebay.com/sch/i.html?_nkw=" + item
      elif webSite == "C":
         filenm = "craigs.txt"
         url = "https://washingtondc.craigslist.org/search/sss?query=" + item
      else:
         raise Exception("Invalid choice for website.")
      print("URL:", url)
      res = requests.get(url)
      noMatchCnt = res.text.count("No exact matches found")
      f = open(filenm, "w")
      i = 0
      for ln in res.iter_lines():
         f.write(str(ln) + "\n")
         #i += 1
         #print(i)
      f.close()
      return noMatchCnt
   else:
      if webSite == "A":
         pass
      elif webSite == "E":
         flagIfItemWide(item, "ebay.txt")
      elif webSite == "C":
         flagIfItemCraigs(item, "craigs.txt")

      return None

def flagIfItemWide(item, filenm):
   fRead = open(filenm, "r")
   hits = 0
   lnNum = 0
   for ln in fRead:
      lnNum += 1
      start = 0
      # Loop through occurences of 'alt=' in entire line.
      while True:
         altPos = ln.find("alt=", start)
         if altPos == -1:
            break
         # The start of text begins 5 spaces after 'alt='.
         start = altPos + 5
         end = ln.find("\">", start)
         tx = ln[start : end]
         print(start, end, tx)
         # Find if text contains all of the item words.
         if hasAllWords(item, tx):
            hits += 1
            print(lnNum, tx)
   fRead.close()
   print("Hits:", hits)

def flagIfItemCraigs(item, filenm):
   fRead = open(filenm, "r")
   hits = 0
   lnNum = 0
   for ln in fRead:
      lnNum += 1
      # Find search text.
      srchPos = ln.find("search-result\" title")
      if srchPos > -1:
         # The start of text begins 22 spaces after search text.
         start = srchPos + 22
         end = ln.find("\">", start)
         tx = ln[start : end]
         print(start, end, tx)
         # Find if text contains all of the item words.
         if hasAllWords(item, tx):
            hits += 1
            print(lnNum, tx)
   fRead.close()
   print("Hits:", hits)

def hasAllWords(item, tx):
   wordList = item.split()
   #cnt = 0
   i = 0
   newTx = tx
   for word in wordList:
      if tx.lower().find(word.lower()) == -1:
         return False
      print(word)

   return True
  
def padSpace(item, tx):
   wordList = item.split()
   newList = [ ]
   i = 0
   newTx = tx
   for word in wordList:
      #newList.insert(i, " " + word + " ")
      newTx = newTx.replace(word, " " + word + " ")
      i += 1
   return newTx

def getPosList(tx):
   posList = [ ]
   i = 0
   if tx[0 : 1] != " ":
      posList.insert(i, 0)
   else:
      posList.insert(i, tx.find(" "))
   while True:  #posList[i] > -1:
      #print(i, posList[i])
      curr = i
      i += 1
      # find next position starting after current position (spacebar)
      posList.insert(i, tx.find(" ", posList[curr] + 1))
      # exit when no more positions are found
      if posList[i] == -1:
         break

   return posList
