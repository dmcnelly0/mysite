from django.test import TestCase
from survey.util import flagIfItem

# Create your tests here.
print("Hello there.")

class UtilCase(TestCase):

   def testFlagIfItemWrite(self):
      #flagIfItem("Drone with Camera", True)
      flagIfItem("Drone with Camera", False)
