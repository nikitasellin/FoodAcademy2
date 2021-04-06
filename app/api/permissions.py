from rest_framework import permissions

from users.utils import get_user_role


class IsStudent(permissions.BasePermission):
    user_role = 'student'

    def has_permission(self, request, view):
        user_role = get_user_role(request.user)
        return user_role == self.user_role


class IsRealSubscriber(permissions.BasePermission):
    def has_permission(self, request, view):
        new_student_id = request.data['newStudent']
        return new_student_id == request.user.id
