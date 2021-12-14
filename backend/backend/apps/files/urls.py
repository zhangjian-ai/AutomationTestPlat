from django.urls import path
from . import views

urlpatterns = [
    path('image/', views.ImageView.as_view()),
    path('file/', views.FileView.as_view()),
    path('sourceList/', views.SourceListView.as_view()),
]
