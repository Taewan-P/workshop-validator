from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('git_workshop/', views.main_page, name='main'),
    path('git_workshop/question1/', views.question_one, name="q1"),
    path('git_workshop/question2/', views.question_two, name="q2"),
    path('git_workshop/question3/', views.question_three, name="q3"),
    path('git_workshop/question4/', views.question_four, name="q4"),
    path('git_workshop/question5/', views.question_five, name="q5"),
    path('git_workshop/question6/', views.question_six, name="q6"),
    path('git_workshop/question7/', views.question_seven, name="q7"),
    path('git_workshop/question8/', views.question_eight, name="q8"),
    path('git_workshop/question9/', views.question_nine, name="q9"),
    path('git_workshop/question10/', views.question_ten, name="q10"),
    path('git_workshop/finished/', views.finished, name="fin"),
    path('forbidden/', views.forbidden, name="403"),
    path('404-not-found/', views.not_found, name="404")
]