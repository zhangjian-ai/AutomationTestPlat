from django.urls import path, re_path
from . import views

urlpatterns = [
    path('jobInductions/', views.JobInductions.as_view()),  # 测试任务
]