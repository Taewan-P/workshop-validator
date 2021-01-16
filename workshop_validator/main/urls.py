from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('d65cedf', views.question_one, name='question_one')
]