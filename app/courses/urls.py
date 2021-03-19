from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('',
         views.CourseListView.as_view(), name='index'),
    path('courses/details/<int:pk>/',
         views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/addcourse/',
         views.CourseAddView.as_view(), name='course_add'),
    path('courses/editcourse/<int:pk>/',
         views.CourseEditView.as_view(), name='course_edit'),
    path('courses/deletecourse/<int:pk>/',
         views.CourseDeleteView.as_view(), name='course_delete')
]
