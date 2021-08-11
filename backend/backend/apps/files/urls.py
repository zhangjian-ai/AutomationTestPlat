from django.urls import path
from . import views

urlpatterns = [
    path('getImage/', views.SystemImageUrlView.as_view()),  # 账号注册
    path('uploadImage/', views.ImageView.as_view()),
]
