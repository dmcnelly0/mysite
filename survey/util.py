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

def getDoor():
   with getConn().cursor() as cur:
      q = "select name from survey_puzzle where cd = 'Door'"
      cur.execute(q)
      dat = cur.fetchall()
   return dat[0][0]

def convertDat(ls):
   fnt = Fernet(getDoor())
   dct = { }
   pos1st = 0
   pos2nd = 1
   # Convert data and put it into a dictionary (hash map).
   for i in range(0, len(ls)):
      bin = fnt.decrypt(ls[i][pos2nd])
      dct[ ls[i][pos1st] ] = bin.decode("utf-8")
   return dct

def getEmailInfo():
   with getConn().cursor() as cur:
      q = "select cd, name from survey_puzzle where cd != 'Door'"
      cur.execute(q)
      dat = cur.fetchall()
      emlDict = convertDat(dat)
   return emlDict

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

AMZ_URL = "https://www.amazon.com/s?k="
EBAY_URL = "https://www.ebay.com/sch/i.html?_nkw="
CL_URL = "https://washingtondc.craigslist.org/search/sss?query="
FBK_URL = "https://www.facebook.com/marketplace/dc/search/?query="
TLR_URL = "https://bringatrailer.com/search/?s="

from warnings import deprecated
import requests
#from rapidfuzz import fuzz
#from survey.models import Pick

def sendEmail(msgText, eml):
   ckpt = "U1"
   port = 465
   try:
      # In the case where the app is directly executed on-line the eml variable
      # will be empty because the email info is retrieved by getEmailInfo.
      # Otherwise, the cron program supplies the email info.
      if eml == None:
         emlInfo = getEmailInfo()
      else:
         emlInfo = eml
      ckpt = "U1.2"
      msg = EmailMessage()
      msg["Subject"] = "Picker Information"
      ckpt = "U1.3"
      msg["From"] = emlInfo["From"]
      msg["To"] = emlInfo["To"]
      #msg["To"] = "dsmcnelly0@gmail.com" # NOTE: TEMPORARILY SENDING TO ME
      msg.set_content(msgText)
      ckpt = "U1.5"
      with smtplib.SMTP_SSL(emlInfo["Send"], port) as smtp: # Replace with your SMTP server and port
          smtp.login(emlInfo["From"], emlInfo["Tok"]) # Replace with your credentials
          smtp.send_message(msg)
   except Exception as x:
      print("Error:", x, "Check point:", ckpt)

def runFind(item, wsite, eml, sim):
   saveData(item, wsite)
   flagIfItem(item, wsite, eml, sim)

# def cronRun():
   # Get the latest active record.
   # pick = Pick.objects.filter(active = True).order_by("changedatetime").reverse()
   # print(pick[0])
   #runFind(pick[0].item, pick[0].wsite_cd)

@deprecated("This version should not be used anymore.")
def flagIfItem(item):
   #item = "greengobbler"
   #url = "https://www.amazon.com/s?k=" + item
   url = "https://www.ebay.com/sch/i.html?_nkw=" + item
   print("URL:", url)
   f = open("EbayDprc.txt", "w")
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

def makeFile(filenm, url):
   res = requests.get(url)
   noMatchCnt = res.text.count("No exact matches found")
   print("No match count:", noMatchCnt)
   f = open(filenm, "w")
   i = 0
   for ln in res.iter_lines():
      f.write(str(ln) + "\n")
   f.close()
   res.close()

def saveData(item, webSite):
   noMatchCnt = -1
   filenm = ""
   #urls = []
   hits = 0
   # Create text files containing data.
   if 0 < webSite.count("A"):
      filenm = "amazon.txt"
      fullUrl = AMZ_URL + item
      makeFile(filenm, fullUrl)
   if 0 < webSite.count("E"):
      filenm = "ebay.txt"
      fullUrl = EBAY_URL + item
      makeFile(filenm, fullUrl)
   if 0 < webSite.count("C"):
      filenm = "craigs.txt"
      fullUrl = CL_URL + item
      makeFile(filenm, fullUrl)
   if 0 < webSite.count("M"):
      filenm = "meta.txt"
      fullUrl = FBK_URL + item
      makeFile(filenm, fullUrl)
   if 0 < webSite.count("T"):
      filenm = "trailer.txt"
      fullUrl = TLR_URL + item
      makeFile(filenm, fullUrl)
   if 0 < webSite.count("O"):
      pass

# Overloaded to give option to create text file of web page or read text file and scrape.
def flagIfItem(item, webSite, eml, sim):
   print(webSite)
   msgText = ""
   if 0 < webSite.count("A"):
      pass
   if 0 < webSite.count("E"):
      msgText += flagIfItemWide(item, "ebay.txt")
   if 0 < webSite.count("C"):
      msgText += flagIfItemCraigs(item, "craigs.txt")
   if 0 < webSite.count("T"):
      msgText += flagIfItemWide(item, "trailer.txt")
   if 0 < webSite.count("O"):
      msgText += flagIfItemOAI(item)
   #print(msgText)
   print("sim: ", sim)
   if sim:
      msgFl = open("msgText.txt", "w")
      msgFl.write(msgText)
      msgFl.close()
   else:
      sendEmail(msgText, eml)

def flagIfItemWide(item, filenm):
   if filenm == "ebay.txt":
      site = "Ebay"
      url = EBAY_URL
   elif filenm == "trailer.txt":
      site = "Bring a Trailer"
      url = TLR_URL
   else:
      site = "Unknown"
      url = "Unknown"
   # match filenm:
      # case "ebay.txt":
         # site = "Ebay"
         # url = EBAY_URL
      # case "trailer.txt":
         # site = "Bring a Trailer"
         # url = TLR_URL
      # case _:
         # site = "Unknown"
         # url = "Unknown"
   fRead = open(filenm, "r")
   msgTx = ""
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
         #print(start, end, tx)
         # Find if text contains all of the item words.
         if hasAllWords(item, tx):
            hits += 1
            print(lnNum, hits, tx)
            # Display hyperling of the source after text.
            fullUrl = url + tx.rstrip("\" />'").replace(" ", "+")
            msgTx += str(hits) + "-  " + tx + "  " + fullUrl + "\n"
   fRead.close()
   hitsStr = str(hits)
   head = "The results of your request regarding '" + item + "' yielded " + hitsStr
   head += " results from " + site + "...\n\n"
   print("Hits:", hits)
   print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
   print(head + msgTx)

   return head + msgTx + "\n"

def flagIfItemCraigs(item, filenm):
   fRead = open(filenm, "r")
   msgTx = ""
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
         #print(start, end, tx)
         # Find if text contains all of the item words.
         if hasAllWords(item, tx):
            hits += 1
            #print(lnNum, hits, tx)
            fullUrl = CL_URL + tx.rstrip("\" />'").replace(" ", "+")
            msgTx += str(hits) + "-  " + tx + "  " + fullUrl + "\n"
   fRead.close()
   hitsStr = str(hits)
   head = "The results of your request regarding '" + item + "' yielded " + hitsStr
   head += " results from Craigs List...\n\n"
   print("Hits:", hits)
   print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
   print(head + msgTx)

   return head + msgTx + "\n"

def flagIfItemOAI(item):
   ckpt = "U2.0"
   try:
      import os
      from dotenv import load_dotenv
      from openai import OpenAI
      load_dotenv()
      ckpt = "u2.2"
      #print(ckpt)
      client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
      ckpt = "u2.4"
      response = client.responses.create(
         model = "gpt-5.4",
         input = "is " + item + " in the market"
      )
      #print(ckpt, str(response))
      ckpt = "u2.6"
      head = "The results of your request regarding whether '" + item
      head += "' is in the market yielded this from Open AI:\n\n"
      ckpt = "u2.8"
      msgTx = response.output_text
      #print(ckpt, msgTx)

      return head + msgTx + "\n"
   except Exception as x:
      #print("Error:", x, "Check point:", ckpt)
      return "Error: " + str(x) + " at check point " + ckpt

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

def rptXpn():
   import traceback
   from datetime import datetime
   f = open("Xpn.txt", "a")
   f.write(str(datetime.now()) + "- " + traceback.format_exc() + "\n")
   f.close()
   print("Check point:", "U3.0")
