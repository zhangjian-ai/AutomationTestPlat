#!/bin/bash
# 从第一行到最后一行分别表示：
# 1. 生成数据库迁移文件
# 2. 根据数据库迁移文件来修改数据库
# 3. 用 uwsgi启动 django 服务, 不再使用python manage.py runserver

# 收集静态文件到指定目录。settings.py 中配置的 STATIC_ROOT
# python3 manage.py collectstatic --noinput

# django-es 生成初始索引
# python3 manage.py rebuild_index --noinput

# 迁移数据库
# python3 manage.py makemigrations
# python3 manage.py migrate

# 添加定时任务
python3 manage.py crontab add  --noinput
#uwsgi  --enable-threads uwsgi.ini
nohup uwsgi --ini uwsgi.ini &
nohup daphne -b 0.0.0.0 -p 8001 backend.asgi:application
# 保持容器内部有一个前台进程在运行,这里用消息队列保持
while true
do
  sleep 1
done
# celery 暂时不使用
#celery -A celery_tasks.main worker -l info
