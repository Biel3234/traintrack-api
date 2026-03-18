from django.urls import path
from .views import *

urlpatterns = [
    path('listcreateexercise/', ListCreateExercise.as_view())
]
