from django.urls import path, re_path
from . import views

urlpatterns = [
    path('testJob/', views.JobView.as_view()),  # 测试任务
    path('jobList/', views.JobListView.as_view()),
    path('dispatchJob/', views.DispatchJobView.as_view()),
    path('testResult/', views.TestResultView.as_view()),
    re_path('jobCaseDetail/(?P<id>\d+)/', views.JobCaseListView.as_view())
]
