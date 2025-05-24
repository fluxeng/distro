from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from customer_support.models import Ticket
from infrastructure.models import Asset
from maintenance.models import Issue, MaintenanceTask, WorkOrder

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_field_agent:
            return User.objects.filter(id=user.id)
        return User.objects.all()

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        stats = {
            'total_tickets': Ticket.objects.count(),
            'open_tickets': Ticket.objects.filter(status='open').count(),
            'total_assets': Asset.objects.count(),
            'critical_assets': Asset.objects.filter(condition_score__lte=3).count(),
            'open_issues': Issue.objects.filter(status__in=['reported', 'verified', 'assigned', 'in_progress']).count(),
            'pending_tasks': MaintenanceTask.objects.filter(status__in=['scheduled', 'in_progress']).count(),
            'active_work_orders': WorkOrder.objects.filter(status__in=['approved', 'in_progress']).count(),
        }
        if user.is_field_agent:
            stats['my_tasks'] = MaintenanceTask.objects.filter(assigned_to=user, status__in=['scheduled', 'in_progress']).count()
            stats['my_issues'] = Issue.objects.filter(assigned_to=user, status__in=['assigned', 'in_progress']).count()
        return Response(stats)