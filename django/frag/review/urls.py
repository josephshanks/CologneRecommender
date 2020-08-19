from django.urls import path,include
from . import views

app_name = 'reviews'

urlpatterns = [
    path('',views.ListReviews.as_view(),name='all'),
    path('new/',views.CreateReview.as_view(),name='create'),
    path('review/',views.SingleReview.as_view(),name='single') #slugify path part 8 3min
]

