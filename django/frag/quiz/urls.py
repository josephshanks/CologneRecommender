from django.urls import path,include
from . import views

app_name = 'quiz'

urlpatterns = [
    path('',views.QuizList.as_view(),name='all'),
    path('new/',views.CreateQuiz.as_view(),name='create')

]