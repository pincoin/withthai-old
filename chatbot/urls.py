from django.urls import path

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('callback/',
         views.callback, name='callback'),
    ]