from .models import User
import django_filters

class UserFilter(django_filters.FilterSet):

    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    role = django_filters.ChoiceFilter(choices = User.ROLES_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'role']