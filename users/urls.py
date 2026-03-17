from django.urls import path
from .views import *

urlpatterns = [
    path('createtrainee/', create_trainee),
    path('listuser/', view_trainee),
    path('detailuser/<int:pk>', detail_trainee),
    path('deleteuser/<int:pk>', delete_trainee)
]
