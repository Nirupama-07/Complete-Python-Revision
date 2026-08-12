from django.urls import path
from . import views

app_name="python"

urlpatterns=[
    path('',views.home,name="home"),
    path("chapter/<int:chapter_number>/", views.chapter, name="chapter"),
    path("run-code/",views.run_code,name="run_code"),
    path("check-answer/",views.check_answer,name="check_answer"),
]