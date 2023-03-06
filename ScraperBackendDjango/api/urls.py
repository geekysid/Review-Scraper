from django.urls import path,include
from .scraper_views import * 

urlpatterns = [
    path('test', test.as_view() , name=''),
    path('add', addView , name=''),
    path('status/<int:job_id>/', statusView.as_view() , name=''),
    path('reviews/<int:job_id>/', reviewsView.as_view() , name=''),
    path('logs/<int:job_id>/', logView.as_view() , name=''),


]