from django_filters import FilterSet, filters

from api.models import Todo


class TodoFilter(FilterSet):
    user = filters.NumberFilter(field_name="user")
    state = filters.BooleanFilter(field_name="state")

    # content = filters.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = Todo
        fields = ['user', 'state']

    def __init__(self, *args, **kwargs):
        super(TodoFilter, self).__init__(*args, **kwargs)
