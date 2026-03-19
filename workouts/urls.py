from django.urls import path
from .views import *

urlpatterns = [
    path('createlistexercise/', ListCreateExercise.as_view())
]
