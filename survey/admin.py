from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Response


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5

class ResponseInline(admin.StackedInline):
    model = Response
    extra = 5

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

class ResponseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["choice", "name"]})
    ]
    inlines = [ResponseInline]
    list_display = ["choice", "name"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Response, ResponseAdmin)
