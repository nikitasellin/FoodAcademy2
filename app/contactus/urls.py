from django.urls import path

from .import views

app_name = 'contactus'

urlpatterns = [
    path('', views.ContactUsView.as_view(), name='send_message'),
]
