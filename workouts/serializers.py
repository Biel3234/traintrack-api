from rest_framework import serializers
from .models import Exercise, Workout, WorkoutExercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise

        fields = ['name']

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout

        fields = ['__all__']

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise

        fields = ['__all__']