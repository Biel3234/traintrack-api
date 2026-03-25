from .serializers import ExerciseSerializer, WorkoutCreateSerializer, WorkoutViewSerializer, WorkoutTraineeViewSerializer

from rest_framework.decorators import api_view, permission_classes
from .models import Exercise, WorkoutExercise, Workout
from users.roles import IsAdmin, IsTrainee, IsTrainer, IsAdminOrTrainer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from .filters import WorkoutFilter

class CreateExercise(generics.ListCreateAPIView):

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAdmin | IsTrainer]

class DetailExercise(generics.RetrieveUpdateDestroyAPIView):

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAdmin | IsTrainer]

@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrTrainer])
def create_workout(request):

    if request.method == 'POST':
        data = request.data.copy()
        trainer = request.user.id
        data['trainer'] = trainer
        serializer = WorkoutCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        queryset = Workout.objects.all()
        filter = WorkoutFilter(request.GET, queryset=queryset)
        
        if not filter.is_valid():
            return Response(filter.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = WorkoutViewSerializer(filter.qs, many=True)
        if queryset:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Erro": "Não há treinos existentes"}, status=status.HTTP_404_NOT_FOUND)
    
class DetailWorkout(generics.RetrieveUpdateDestroyAPIView):

    queryset = Workout.objects.all()
    serializer_class = WorkoutViewSerializer
    permission_classes = [IsAdmin | IsTrainer]
    
class CreateWorkoutExercise(generics.ListCreateAPIView):

    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExercise
    permission_classes = [IsAdmin | IsTrainer]

class WorkoutTraineeView(generics.ListAPIView):
    
    serializer_class = WorkoutTraineeViewSerializer
    permission_classes = [IsTrainee]

    def get_queryset(self):
        return Workout.objects.filter(trainee=self.request.user)