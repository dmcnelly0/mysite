from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("answercls/", views.AddAnswer.as_view(), name="AddAnswer"),
    path("list/", views.list, name="listAnswers")
]
