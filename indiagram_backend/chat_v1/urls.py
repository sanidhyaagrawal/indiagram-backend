from django.urls import path, include
#from django.views.generic import TemplateView
#from django.contrib.auth.decorators import login_required
#from rest_framework.routers import DefaultRouter
#from chat_v1.api import MessageModelViewSet, UserModelViewSet
from . import api


urlpatterns = [
    path('chatHistory/', api.chatHistory, name='chatHistory'),
    path('getMessage/', api.getMessage, name='getMessage'),
    path('sendMessage/', api.sendMessage, name='sendMessage'),
    path('messageSeen/', api.messageSeen, name='messageSeen'),
    path('messageLike/', api.messageLike, name='messageLike'),
    path('chatUsers/', api.chatUsers, name='chatUsers'),
]