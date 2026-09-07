from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, adm_vw, fil

urlpatterns = [
   path("", views.index, name="index"),
   path("<int:pageId>/adm/", adm_vw.LogIn.as_view(), name="AdminView"),
   path("answercls/", views.AddAnswer.as_view(), name="AddAnswer"),
   path("list/", views.list, name="listAnswers"),
   path("poll/", views.pollHome, name="pollHome"),
   path("addchoice/", adm_vw.AddChoice.as_view(), name="Add Choice"),
   path("<int:choice_id>/deactivatechoice/", adm_vw.deactivateChoice, name="Deactivate Choice"),
   path("<int:question_id>/choice/", views.choice, name="Choice"),
   path("resp/", views.respRpt, name="RespRpt"),
   #path("choice/", views.choice, name="Choice"),
   #path("prestore/", views.authstore, name="authflSs"),
   path("<unm>/store/", fil.flSs, name="flSs"),
   path("upld/", views.uploadFile, name="uploadFile"),
   path("<unm>/pick/", views.picker, name="Picker"),
   path("plist/", views.pList, name="Pick History"),
   path("helppkr/", views.helpPicker, name="Help Picker"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)