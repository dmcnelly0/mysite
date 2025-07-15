from django.test import TestCase
from survey.util import flagIfItem, getPosList

# Create your tests here.
print("Run test(s).")

class UtilCase(TestCase):

   def testFlagIfItemWrite(self):
      # lineClean = "really silly oop snoop oh how did you put up with that or did you snoop silly oop oh really not please help out if you can"
      # print(getPosList(lineClean))

      #flagIfItem("Drone with Camera", True)
      #flagIfItem("Drone with Camera", False)
      #flagIfItem("Drone", True)
      #flagIfItem("Drone", False)

      fRead = open("Craigs.txt", "r")
      prev = ""
      for ln in fRead:
         twoLn = prev + ln
         print(twoLn)
         prev = ln[100:].replace("\n", " ")
