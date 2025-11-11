from django import forms
#from django.db import connections

class AnswerForm(forms.Form):
    RATINGS5 = [ (0, "<Give rating>"),
                 (5, "Very good"),
                 (4, "Good"),
                 (3, "Okay"),
                 (2, "Not good"),
                 (1, "Not good at all"),
               ]
    name = forms.CharField(label = "Name", max_length = 80)
    city_county = forms.CharField(label = "City or County", max_length = 50)
    church_rating = forms.ChoiceField(label = "What did you think of the service", choices = RATINGS5)
    #pastor_rating = forms.ChoiceField(label = "What did you think of the pastor", choices = RATINGS5)
    comments = forms.CharField(label = "Comments", max_length = 500
        , widget = forms.Textarea(), required=False )

class AddChoiceForm(forms.Form):
    question = forms.ChoiceField(label = "Pick question") #, choices = getQuestions() )
    name = forms.CharField(label = "Choice Name", max_length = 200)

class ChoiceForm(forms.Form):
    name = forms.CharField(label = "Your Name", max_length = 80)
    #CH = [("1", "dummy value 1"), ("2", "dummy value 2")]
    choice_ = forms.ChoiceField(label = "Pick", widget = forms.RadioSelect) #, choices = CH )

class AuthForm(forms.Form):
    uname = forms.CharField(label = "Username", max_length = 20)
    pword = forms.CharField(label = "Password", max_length = 20
        , widget = forms.PasswordInput(attrs = { 'autocomplete': 'new-password' } ) )

class FileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField() #label = "File Name", max_length=30)

class PickerForm(forms.Form):
    WSITE = { "A": "Amazon",
              "E": "Ebay",
              "C": "Craigslist",
              "T": "Bring a Trailer",
            }
    #website = forms.ChoiceField(label = "Website", widget = forms.RadioSelect, choices = WSITE )
    website = forms.MultipleChoiceField(
        label = "Website"
        , widget = forms.CheckboxSelectMultiple
        , choices = WSITE )
    item = forms.CharField(label = "Item", max_length = 75)
    autorun = forms.BooleanField(label = "Add to Automatic Run", required = False)
