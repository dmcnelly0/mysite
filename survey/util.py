import re, subprocess
from cryptography.fernet import Fernet
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
            col = re.split("\s+", ln)
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
 
