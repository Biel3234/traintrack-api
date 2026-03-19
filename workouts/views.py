from .serializers import ExerciseSerializer, WorkoutExerciseSerializer, WorkoutExerciseSerializer

from .models import Exercise, WorkoutExercise, Workout
from users.roles import IsAdmin, IsTrainee, IsTrainer
from rest_framework import generics

class ListCreateExercise(generics.ListCreateAPIView):

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAdmin | IsTrainer]