from rest_framework import permissions

from users.models import User


class ModulePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            user_id = request.user.id
            try:
                User.objects.get(id=user_id, groups=1)  # 这里配置的是操作权限组 ID 为1 的组 具有模块的创建权限
                return True
            except User.DoesNotExist:
                return False

'''
has_object_permission方法在has_permission方法返回值True之后调用，除了在POST方法中（在POST方法中仅执行has_permission）。
当从permission_classes方法返回False值时，请求不会获得任何权限，也不会循环更多，否则，它会检查循环的所有权限。
has_permission方法将对所有请求调用（GET，POST，PUT，DELETE）HTTP。
has_object_permission方法不会对HTTP POST请求调用，因此对POST的校验在 has_permission 方法中完成。
'''