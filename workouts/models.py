from users.models import User
from django.db import models

class Exercise(models.Model):

    name =  models.CharField(max_length=100)

class Workout(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer')
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainee')

    created_at = models.DateTimeField(auto_now_add=True)

class WorkoutExercise(models.Model):

    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()