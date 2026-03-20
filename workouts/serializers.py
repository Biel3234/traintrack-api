from .models import Exercise, Workout, WorkoutExercise
from users.models import User
from rest_framework import serializers


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise

        fields = ['name']

class WorkoutExerciseViewSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)
    class Meta:
        model = WorkoutExercise

        fields = ['id', 'exercise', 'sets', 'reps']

class WorkoutCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout

        fields = ['name', 'description', 'trainee', 'trainer']

class WorkoutViewSerializer(serializers.ModelSerializer):
    trainer = UserSimpleSerializer(read_only=True)
    trainee = UserSimpleSerializer(read_only=True)

    exercises = WorkoutExerciseViewSerializer(
        source='workoutexercise_set',
        many = True,
        read_only = True,
    )
    class Meta:
        
        model = Workout

        fields = ['name', 'description', 'trainee', 'trainer', 'exercises', 'created_at']

