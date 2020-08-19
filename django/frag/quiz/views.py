from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


class QuizList(SelectRelatedMixin,generic.ListView):
    model = models.Quiz
    select_related = ('user','user') # group in tuple

class UserQuiz(generic.ListView):
    model = models.Quiz
    template_name = 'quiz/user_quiz_list.html'

    def get_queryset(self):
        try:
            self.quiz_user = User.objects.prefetch_related('quiz').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.quiz_user.posts.all()
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_user'] = self.quiz_user
        return context

class QuizDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Quiz
    select_rated = ('user') #review in tuple

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__name__iexact=self.kwargs.get('username'))

class CreateQuiz(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ('sex','age','signature','season','day','sillage','longevity','forwhom','price','review')
    model = models.Quiz

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


