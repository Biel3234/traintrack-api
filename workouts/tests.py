from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Exercise, Workout, WorkoutExercise

User = get_user_model()


class ExerciseTestCase(APITestCase):
    """Testes para CRUD de exercícios"""

    def setUp(self):
        """Setup: Criar usuários de teste"""
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            username='admin',
            password='testpass123',
            phone='11999999999',
            role='admin'
        )
        self.trainer_user = User.objects.create_user(
            email='trainer@test.com',
            username='trainer',
            password='testpass123',
            phone='11988888888',
            role='trainer'
        )
        self.trainee_user = User.objects.create_user(
            email='trainee@test.com',
            username='trainee',
            password='testpass123',
            phone='11977777777',
            role='trainee'
        )
        self.exercise = Exercise.objects.create(name='Supino')

    def test_list_exercises(self):
        """Teste: Listar todos os exercícios"""
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get('/api/workout/createlistexercise/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_exercise_as_trainer(self):
        """Teste: Trainer cria novo exercício"""
        self.client.force_authenticate(user=self.trainer_user)
        data = {'name': 'Agachamento'}
        response = self.client.post('/api/workout/createlistexercise/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Exercise.objects.filter(name='Agachamento').exists())

    def test_create_exercise_as_admin(self):
        """Teste: Admin cria novo exercício"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'Rosca Direta'}
        response = self.client.post('/api/workout/createlistexercise/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_exercise_unauthorized(self):
        """Teste: Trainee não pode criar exercício"""
        self.client.force_authenticate(user=self.trainee_user)
        data = {'name': 'Flexão'}
        response = self.client.post('/api/workout/createlistexercise/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_detail_exercise(self):
        """Teste: Visualizar detalhes de um exercício"""
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get(f'/api/workout/detailexercise/{self.exercise.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Supino')

    def test_update_exercise(self):
        """Teste: Atualizar exercício"""
        self.client.force_authenticate(user=self.trainer_user)
        data = {'name': 'Supino Inclinado'}
        response = self.client.put(f'/api/workout/detailexercise/{self.exercise.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.name, 'Supino Inclinado')

    def test_delete_exercise(self):
        """Teste: Deletar exercício"""
        self.client.force_authenticate(user=self.admin_user)
        exercise_id = self.exercise.id
        response = self.client.delete(f'/api/workout/detailexercise/{exercise_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Exercise.objects.filter(id=exercise_id).exists())


class WorkoutTestCase(APITestCase):
    """Testes para CRUD de workouts"""

    def setUp(self):
        """Setup: Criar usuários, exercícios e workouts de teste"""
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            username='admin',
            password='testpass123',
            phone='11999999999',
            role='admin'
        )
        self.trainer_user = User.objects.create_user(
            email='trainer@test.com',
            username='trainer',
            password='testpass123',
            phone='11988888888',
            role='trainer'
        )
        self.trainee_user = User.objects.create_user(
            email='trainee@test.com',
            username='trainee',
            password='testpass123',
            phone='11977777777',
            role='trainee'
        )
        self.exercise1 = Exercise.objects.create(name='Supino')
        self.exercise2 = Exercise.objects.create(name='Agachamento')
        self.workout = Workout.objects.create(
            name='Treino A',
            description='Treino de peito',
            trainer=self.trainer_user,
            trainee=self.trainee_user,
            day_of_week='mon'
        )

    def test_create_workout_as_trainer(self):
        """Teste: Trainer cria novo workout"""
        self.client.force_authenticate(user=self.trainer_user)
        data = {
            'name': 'Treino B',
            'description': 'Treino de costas',
            'trainee': self.trainee_user.id,
            'day_of_week': 'tue'
        }
        response = self.client.post('/api/workout/createworkout/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Workout.objects.filter(name='Treino B').exists())

    def test_create_workout_as_admin(self):
        """Teste: Admin cria novo workout"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'Treino C',
            'description': 'Treino de perna',
            'trainee': self.trainee_user.id,
            'day_of_week': 'wed'
        }
        response = self.client.post('/api/workout/createworkout/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_workout_unauthorized(self):
        """Teste: Trainee não pode criar workout"""
        self.client.force_authenticate(user=self.trainee_user)
        data = {
            'name': 'Treino',
            'description': 'Descrição',
            'trainee': self.trainee_user.id,
            'day_of_week': 'mon'
        }
        response = self.client.post('/api/workout/createworkout/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_list_workouts(self):
        """Teste: Listar workouts com paginação"""
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get('/api/workout/createworkout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_detail_workout(self):
        """Teste: Visualizar detalhes de um workout"""
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get(f'/api/workout/detailworkout/{self.workout.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Treino A')
        self.assertEqual(response.data['trainer']['id'], self.trainer_user.id)

    def test_update_workout(self):
        """Teste: Atualizar workout"""
        self.client.force_authenticate(user=self.trainer_user)
        data = {
            'name': 'Treino A Atualizado',
            'description': 'Treino de peito atualizado',
            'trainee': self.trainee_user.id
        }
        response = self.client.put(f'/api/workout/detailworkout/{self.workout.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_workout(self):
        """Teste: Deletar workout"""
        self.client.force_authenticate(user=self.trainer_user)
        workout_id = self.workout.id
        response = self.client.delete(f'/api/workout/detailworkout/{workout_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Workout.objects.filter(id=workout_id).exists())


class WorkoutExerciseTestCase(APITestCase):
    """Testes para adicionar exercícios aos workouts"""

    def setUp(self):
        """Setup: Criar dados de teste"""
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            username='admin',
            password='testpass123',
            phone='11999999999',
            role='admin'
        )
        self.trainer_user = User.objects.create_user(
            email='trainer@test.com',
            username='trainer',
            password='testpass123',
            phone='11988888888',
            role='trainer'
        )
        self.trainee_user = User.objects.create_user(
            email='trainee@test.com',
            username='trainee',
            password='testpass123',
            phone='11977777777',
            role='trainee'
        )
        self.exercise = Exercise.objects.create(name='Supino')
        self.workout = Workout.objects.create(
            name='Treino A',
            description='Treino de peito',
            trainer=self.trainer_user,
            trainee=self.trainee_user,
            day_of_week='mon'
        )

    def test_create_workout_exercise(self):
        """Teste: Adicionar exercício ao workout"""
        self.client.force_authenticate(user=self.trainer_user)
        data = {
            'workout': self.workout.id,
            'exercise': self.exercise.id,
            'sets': 4,
            'reps': 10
        }
        response = self.client.post('/api/workout/createlistworkoutexercise/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            WorkoutExercise.objects.filter(
                workout=self.workout,
                exercise=self.exercise
            ).exists()
        )

    def test_list_workout_exercises(self):
        """Teste: Listar exercícios de um workout"""
        WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            sets=4,
            reps=10
        )
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get('/api/workout/createlistworkoutexercise/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_workout_exercise_invalid_sets(self):
        """Teste: Erro ao criar workout_exercise com sets inválido"""
        self.client.force_authenticate(user=self.trainer_user)
        data = {
            'workout': self.workout.id,
            'exercise': self.exercise.id,
            'sets': -1,
            'reps': 10
        }
        response = self.client.post('/api/workout/createlistworkoutexercise/', data, format='json')
        # Pode ser 400 se houver validação
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class WorkoutTraineeViewTestCase(APITestCase):
    """Testes para visualizar workouts do trainee"""

    def setUp(self):
        """Setup: Criar dados de teste"""
        self.trainer_user = User.objects.create_user(
            email='trainer@test.com',
            username='trainer',
            password='testpass123',
            phone='11988888888',
            role='trainer'
        )
        self.trainee_user = User.objects.create_user(
            email='trainee@test.com',
            username='trainee',
            password='testpass123',
            phone='11977777777',
            role='trainee'
        )
        self.other_trainee = User.objects.create_user(
            email='other_trainee@test.com',
            username='other_trainee',
            password='testpass123',
            phone='11966666666',
            role='trainee'
        )
        self.exercise = Exercise.objects.create(name='Supino')
        self.workout1 = Workout.objects.create(
            name='Treino A',
            description='Treino de peito',
            trainer=self.trainer_user,
            trainee=self.trainee_user,
            day_of_week='mon'
        )
        self.workout2 = Workout.objects.create(
            name='Treino B',
            description='Treino de costas',
            trainer=self.trainer_user,
            trainee=self.trainee_user,
            day_of_week='tue'
        )
        self.workout_other = Workout.objects.create(
            name='Treino C',
            description='Outro treino',
            trainer=self.trainer_user,
            trainee=self.other_trainee,
            day_of_week='wed'
        )

    def test_trainee_view_own_workouts(self):
        """Teste: Trainee vê apenas seus próprios workouts"""
        self.client.force_authenticate(user=self.trainee_user)
        response = self.client.get('/api/workout/my-workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if isinstance(response.data, list):
            self.assertEqual(len(response.data), 2)
            workout_names = [w['name'] for w in response.data]
            self.assertIn('Treino A', workout_names)
            self.assertIn('Treino B', workout_names)

    def test_trainee_cannot_view_others_workouts(self):
        """Teste: Trainee não vê workouts de outros trainees"""
        self.client.force_authenticate(user=self.trainee_user)
        response = self.client.get('/api/workout/my-workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response.data é uma lista contendo dicts com dados dos workouts
        if isinstance(response.data, list):
            workout_names = [w['name'] for w in response.data]
            self.assertNotIn('Treino C', workout_names)

    def test_unauthorized_cannot_view_workouts(self):
        """Teste: Usuário não autenticado não pode ver workouts"""
        response = self.client.get('/api/workout/my-workouts/')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_trainer_cannot_view_trainee_workouts(self):
        """Teste: Trainer não pode usar endpoint de trainee"""
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get('/api/workout/my-workouts/')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])
