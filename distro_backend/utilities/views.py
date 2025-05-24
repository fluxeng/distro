from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from .models import User
from .serializers import UserLocationUpdateSerializer
from maintenance.models import Issue
from customer_support.models import Ticket
from django.utils.timezone import now
from django.db.models import Count

class UserLocationLoggerView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = UserLocationUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(last_location_update=now())
        return Response({'status': 'location updated'})

class DashboardStatsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "open_issues": Issue.objects.filter(status__in=["reported", "in_progress"]).count(),
            "open_tickets": Ticket.objects.filter(status__in=["open", "in_progress"]).count(),
            "total_customers": User.objects.filter(role="customer_service").count(),
            "sla_breaches": Ticket.objects.filter(is_sla_breached=True).count(),
        })
