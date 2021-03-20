from django.urls import path

from .import views

app_name = 'frontend'

urlpatterns = [
    path('',
         views.FrontendTestView.as_view(), name='test'),
]
