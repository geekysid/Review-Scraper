from django.urls import path
from .views2 import AddJobView,ShowJobStatusView,ShowJobReviewsView,ShowlogView,ShowRecentJobView

urlpatterns = [
    path('add/', AddJobView.as_view(), name=''),
    path('status/<int:job_id>/', ShowJobStatusView.as_view(), name=''),
    path('reviews/<int:job_id>/', ShowJobReviewsView.as_view(), name=''),
    path('logs/<int:job_id>/', ShowlogView.as_view(), name=''),
    path('recent-jobs/', ShowRecentJobView.as_view(), name=''),
]
