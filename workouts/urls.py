from django.urls import path
from .views import *

urlpatterns = [
    path('createlistexercise/', CreateExercise.as_view()),
    path('detailexercise/<int:pk>', DetailExercise.as_view()),
    path('createworkout/', create_workout),
]
