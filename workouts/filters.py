import django_filters
from .models import Workout

class WorkoutFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    trainer = django_filters.CharFilter(lookup_expr='icontains')
    trainee = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Workout
        fields = ['name', 'trainer', 'trainee']