from django.urls import path
from . import views

urlpatterns = [
    # path('uploadManyCase/', views.ScriptUploadCaseView.as_view()),  # 批量导入用例
    path('modules/', views.ModuleView.as_view()),
    path('caseList/', views.CaseListView.as_view()),
    path('case/', views.CaseView.as_view()),
    path('uploadXmindCase/', views.XmindUploadCaseView.as_view()),
    path('caseTree/', views.CaseTreeView.as_view()),
]
