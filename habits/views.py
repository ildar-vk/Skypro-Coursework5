from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Habit
from .serializers import HabitSerializer
from .paginators import HabitPaginator
from .permissions import IsOwnerOrReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'public':
            return Habit.objects.filter(is_public=True)
        if self.action == 'list':
            return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def public(self, request):
        """Список публичных привычек."""
        return self.list(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)