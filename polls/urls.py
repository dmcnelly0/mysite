from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("home/", views.home, "Home"),
    path("choose/", views.choose_, "Choose")
    #path("list/", views.list, name="listAnswers"),
]
