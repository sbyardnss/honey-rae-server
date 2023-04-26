from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Customer

class TicketView(ViewSet):
    """honey rae api ticket view"""
    def list(self, request):
        """handle GET request for all tickets"""
        # tickets = ServiceTicket.objects.all()
        tickets = []
        if request.auth.user.is_staff:
            tickets = ServiceTicket.objects.all()
        else:
            tickets = ServiceTicket.objects.filter(customer__user=request.auth.user)
        serialized = TicketSerializer(tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """handle GET request for individual ticket"""
        ticket = ServiceTicket.objects.get(pk=pk)
        serialized = TicketSerializer(ticket)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        """handle POST request for service ticket"""
        new_ticket = ServiceTicket()
        new_ticket.customer = Customer.objects.get(user=request.auth.user)
        new_ticket.description = request.data['description']
        new_ticket.emergency = request.data['emergency']
        new_ticket.save()
        serialized = TicketSerializer(new_ticket)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

class TicketSerializer(serializers.ModelSerializer):
    """json serializer for tickets"""
    class Meta:
        model = ServiceTicket
        fields = ('id', 'customer', 'employee', 'description', 'emergency', 'date_completed')
        depth = 1