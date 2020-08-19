from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic

from review.models import Review,ReviewMember
from . import models

class CreateReview(LoginRequiredMixin,generic.CreateView):
    fields = ('name')
    model = Review

class SingleReview(generic.DetailView):
    model = Review

class ListReviews(generic.ListView):
    model = Review