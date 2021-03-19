from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from . import views

app_name = 'api'

ro_router = DefaultRouter()
ro_router.register('courses', views.CoursesViewSet)
ro_router.register('teachers', views.TeachersViewSet)

rw_router = DefaultRouter()
rw_router.register('courses', views.CourseAdminViewSet)
rw_router.register('teachers', views.TeacherAdminViewSet)
rw_router.register('messages', views.MessageAdminViewSet)

urlpatterns = [
    path('token/', token_obtain_pair, name='token_obtain_pair'),
    path('token/refresh/', token_refresh, name='token_refresh'),
    path('view/', include((ro_router.urls, app_name), namespace='view_models')),
    path('full-access/', include((rw_router.urls, app_name), namespace='full_access')),
    path('', views.RootView.as_view())
]
