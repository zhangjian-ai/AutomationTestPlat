"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from .routing import urlpatterns

# 配置文件上线时需要修改为线上配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.prod')

import django
django.setup()

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(urlpatterns)
})
