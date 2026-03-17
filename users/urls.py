from django.urls import path
from .views import *

urlpatterns = [
    path('createtrainee/', create_trainee),
    path('listuser/', view_users),
    path('detailuser/<int:pk>', detail_user),
    path('deleteuser/<int:pk>', delete_user),
    path('updateuser/<int:pk>', update_user),
    path('createtrainer/', create_trainer),
]
