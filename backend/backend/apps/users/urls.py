from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view()),  # 登陆
    path('logon/', views.UserRegisterView.as_view()),  # 账号注册
    path('userCount/', views.CheckUserCount.as_view()),  # 检查用户数数量
    path('userList/', views.UserListView.as_view()),  # 检查用户数数量
    re_path('getConstants/(?P<name>[A-Z_]+)/', views.GetConstantsAttrsView.as_view())  # 发送短信验证码
]
