from django.urls import path
from . import views
from .views import ping

urlpatterns = [
    path('hello/', views.say_hello),
    path('ping/', ping, name='ping'),
]