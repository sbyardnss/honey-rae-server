from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Customer, Employee

class TicketView(ViewSet):
    """honey rae api ticket view"""
    def list(self, request):
        """handle GET request for all tickets"""
        # tickets = ServiceTicket.objects.all()
        tickets = []
        if request.auth.user.is_staff:
            tickets = ServiceTicket.objects.all()
            if "status" in request.query_params:
                if request.query_params['status'] == "done":
                    tickets = tickets.filter(date_completed__isnull=False)
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

    def update(self, request, pk=None):
        """handle PUT request for tickets"""
        ticket = ServiceTicket.objects.get(pk=pk)
        employee_id = request.data['employee']
        assigned_employee = Employee.objects.get(pk=employee_id)
        ticket.employee = assigned_employee
        ticket.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class TicketEmployeeSerializer(serializers.ModelSerializer):
    """serialize employee property on tickets"""
    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'specialty')

class TicketCustomerSerializer(serializers.ModelSerializer):
    """serialize customer property on tickets"""
    class Meta:
        model = Customer
        fields = ('id', 'full_name', 'address')

class TicketSerializer(serializers.ModelSerializer):
    """json serializer for tickets"""
    employee = TicketEmployeeSerializer(many=False)
    customer = TicketCustomerSerializer(many=False)
    class Meta:
        model = ServiceTicket
        fields = ('id', 'customer', 'employee', 'description', 'emergency', 'date_completed')
        depth = 1