from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('getImage/(?P<scope>[a-z]+)/', views.SystemImageView.as_view()),
    path('image/', views.ImageView.as_view()),
]
