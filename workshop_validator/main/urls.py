from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('git_workshop', views.main_page, name='question_one')
]