from django.urls import path, re_path
from . import views

urlpatterns = [
    path('dingTalk/', views.DingTalkAuth.as_view()),  # 钉钉登陆认证
    path('getPublicKey/', views.CipherView.as_view()),  # 获取服务器公钥
    re_path('sendSmsCode/(?P<mobile>1[3-9]\d{9})/', views.SmsCodeView.as_view())  # 发送短信验证码
]
