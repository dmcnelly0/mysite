from django import forms

class AnswerForm(forms.Form):
    RATINGS5 = [ (None, ""),
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
