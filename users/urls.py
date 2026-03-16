from django.urls import path
from .views import *

urlpatterns = [
    path('createuser/', CreateUser),
    path('listuser/', ViewUser),
    path('detailuser/<int:pk>', DetailUser),
    path('deleteuser/<int:pk>', DeleteUser)
]
