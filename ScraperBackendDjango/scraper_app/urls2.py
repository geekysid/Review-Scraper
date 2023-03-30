from django.urls import path
from .views2 import AddJobView,ShowJobStatusView,ShowJobReviewsView,ShowlogView,ShowRecentLogView

urlpatterns = [
    path('add/', AddJobView.as_view(), name=''),
    path('status/<int:job_id>/', ShowJobStatusView.as_view(), name=''),
    path('reviews/<int:job_id>/', ShowJobReviewsView.as_view(), name=''),
    path('logs/<int:job_id>/', ShowlogView.as_view(), name=''),
    path('recent-logs/', ShowRecentLogView.as_view(), name=''),
]
