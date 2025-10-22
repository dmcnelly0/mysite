from django.test import TestCase
#from survey.util import flagIfItem, flagIfItemWide  #, getPosList
#from survey.util import flagIfItemWide
#from survey.util import padSpace
#from survey.util import hasAllWords
import survey.util

# Create your tests here.
print("Run test(s).")

class UtilCase(TestCase):

   def testFlagIfItemWrite(self):
      #flagIfItem("Drone with Camera", True)
      #flagIfItem("Drone with Camera", False)
      #flagIfItem("Drone", True)
      #flagIfItem("Drone", False)
      #flagIfItem("Drone put together", False)
      #flagIfItem("Drone", False)
      #flagIfItem("snoop   silly oop  oh really", False)
      #flagIfItem("henry .357 rifle", True)
      #flagIfItem("henry .357 rifle", False)
      # flagIfItem("henry  .357     rifle", True)
      #flagIfItemWide(".357     rifle henry")
      #survey.util.flagIfItem("drone  Programmable", True)
      #survey.util.flagIfItemWide("drone  Programmable")
      # cnt = survey.util.flagIfItem("defgzwvts  klzhv", True, "E")
      # print("No match count", cnt)
      #survey.util.flagIfItemWide("defgzwvts  klzhv", "E")
      #cnt = survey.util.flagIfItem("massage chair", True, "E")
      #print("No match count", cnt)
      #survey.util.flagIfItemWide("massage chair", "E")

      # cnt = survey.util.flagIfItem("bckwmcomw rljjvneiqovn", True, "E")
      #cnt = survey.util.flagIfItem("henry  .357     rifle", True, "E")
      #cnt = survey.util.flagIfItem("chair   massage", True, "E")
      # cnt = survey.util.flagIfItem("hdtv    samsung", True, "C")
      # cnt = survey.util.flagIfItem(".300 AR-15", True, "C")
      # print("No match count", cnt)

      #survey.util.flagIfItemWide("chair   massage", "ebay - chair.txt")
      #survey.util.flagIfItemWide("defgzwvts  klzhv", "ebay - Copy (2).txt")
      #survey.util.flagIfItemWide("bckwmcomw rljjvneiqovn", "ebay - Copy (3).txt")
      #survey.util.flagIfItemWide(".357     rifle henry", "ebay - henry.txt")
      #survey.util.flagIfItemCraigs("hdtv    samsung", "craigs - samsung.txt")
      #survey.util.flagIfItemCraigs("AR-15  .300", "craigs - 300.txt")

      #survey.util.flagIfItem("Drone   AI", False, "E")
      #survey.util.flagIfItem("adult stuffed animals", True, "M")
      survey.util.flagIfItem("classic cars", True, "T")

   #def testPadSpace(self):
      #padList = padSpace("That guy    Doug cracks   me up")
      # newText = padSpace("rifle   henry  .357"
         # , "b'r>\n        <a href=/>craigslist</a>\n            <h1>For Sale &quot;henry .357 rifle&quot; in Washington, DC</h1>\n    </div>\n\n'")
      # print(newText)

   #def testHasAllWords(self):
      #has = hasAllWords("rifle   henry  .357"
      #   , "b'r>\n        <a href=/>craigslist</a>\n            <h1>For Sale &quot;henry .357 rifle&quot; in Washington, DC</h1>\n    </div>\n\n'")
   #   has = hasAllWords("rifle   henry  .357"
   #      , "Did you see this .rIFLE  funny Henry .358  or not.")
   #   print(has)

   # def testgetPosList(self):
      # lineClean = " really silly oop snoop oh how did you put up with that or did you snoop silly oop oh really not please help out if you can"
      # print(getPosList(lineClean))

   # def testConcatPrev(self):
      # fRead = open("Craigs.txt", "r")
      # prev = ""
      # for ln in fRead:
         # twoLn = prev + ln
         # print(twoLn)
         # prev = ln[100:].replace("\n", " ")
