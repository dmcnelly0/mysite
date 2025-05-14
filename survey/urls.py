from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, fil

urlpatterns = [
    path("", views.index, name="index"),
    path("answercls/", views.AddAnswer.as_view(), name="AddAnswer"),
    path("list/", views.list, name="listAnswers"),
    path("poll/", views.pollHome, name="pollHome"),
    path("addchoice/", views.addChoice, name="AddChoice"),
    path("<int:question_id>/choice/", views.choice, name="Choice"),
    path("resp/", views.respRpt, name="RespRpt"),
    #path("choice/", views.choice, name="Choice"),
    #path("prestore/", views.authstore, name="authflSs"),
    path("store/", fil.flSs.as_view(), name="flSs"),
    path("upld/", views.uploadFile, name="uploadFile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)