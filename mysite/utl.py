from cryptography.fernet import Fernet

def getTok():
   # w = open("Where.txt", "w")
   # w.write("Here")
   # w.close()
   #print("Begin") 
   #f = open("text1.txt", "r")
   #k = f.readline()
   #p = f.readline()
   #f.close()
   #print("Check:", k, p)
   fnt = Fernet(b'0VisMn4Cz11kSO9gCYCKV1M4HOzSXVlDQKWj3W0XbGU=')
   tokb = fnt.decrypt(b'gAAAAABnSqVZte9rVbpxuxDzuauYxVc8uow_insi4Op1GJi9kOvvpYSrrCga5p6daABxAfs73FHpefwe3xoAQ_1Wg5YIq36ZKA==')
   tok = tokb.decode('utf-8')

   return tok
