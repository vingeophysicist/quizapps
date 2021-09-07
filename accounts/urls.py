from .api import LoginAPI, RegisterAPI, UserAPI
from django.urls import path



urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('user/', UserAPI.as_view())
]



























