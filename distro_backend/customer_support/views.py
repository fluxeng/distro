from rest_framework import viewsets, permissions
from .models import Customer, Ticket
from .serializers import CustomerSerializer, TicketSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def confirm_resolution(self, request, pk=None):
        ticket = self.get_object()
        rating = request.data.get("rating")
        comment = request.data.get("comment", "")
        ticket.satisfaction_rating = rating
        ticket.satisfaction_comment = comment
        ticket.status = "closed"
        ticket.save()
        return Response({"message": "Resolution confirmed and ticket closed."})