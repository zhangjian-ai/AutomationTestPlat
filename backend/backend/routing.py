from django.urls import path

from .apps.files import consumers

urlpatterns = [
    path(r'ws/upload/', consumers.SourceUploadConsumer.as_asgi()),
    path(r'ws/download/', consumers.SourceDownloadConsumer.as_asgi())
]
