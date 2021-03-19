from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .import views

app_name = 'users'

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(), name='logout'),
    path('teacher/list/',
         views.TeacherListView.as_view(), name='teacher_list'),
    path('teacher/detail/<int:pk>/',
         views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('teacher/add/',
         views.TeacherAddView.as_view(), name='teacher_add'),
    path('teacher/edit/<int:pk>/',
         views.TeacherEditView.as_view(), name='teacher_edit'),
    path('teacher/delete/<int:pk>/',
         views.TeacherDeleteView.as_view(), name='teacher_delete'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
]
