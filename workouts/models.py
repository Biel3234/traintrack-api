from users.models import User
from django.db import models

class Exercise(models.Model):

    name =  models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Workout(models.Model):

    WEEK = [
        ('mon', 'Segunda-Feira'),
        ('tue', 'Terça-Feira'),
        ('wed', 'Quarta-Feira'),
        ('thu', 'Quinta-Feira'),
        ('fri', 'Sexta-Feira'),
        ('sat', 'Sábado'),
        ('sun', 'Domingo'),
    ]

    name = models.CharField(max_length=50)
    description = models.TextField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer')
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainee')
    exercises = models.ManyToManyField(
        Exercise,
        through='WorkoutExercise'
    )
    day_of_week = models.CharField(max_length=3, choices=WEEK)


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.trainee} - Matricula: {self.trainee.id} -{self.day_of_week}"


class WorkoutExercise(models.Model):

    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()

    def __str__(self):
        return f"{self.workout.name} {self.workout.trainee} - Matricula: {self.workout.trainee.id} | {self.exercise.name} - {self.sets}x{self.reps}"
