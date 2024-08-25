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
