from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import Employee

class EmployeeView(ViewSet):
    """Honey Rae API employees view"""
    def list(self, request):
        """handle GET requests for all employees"""
        employees = Employee.objects.all()
        serialized = EmployeeSerializer(employees, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """handle GET requests for individual employee"""
        employee = Employee.objects.get(pk=pk)
        serialized = EmployeeSerializer(employee)
        return Response(serialized.data, status=status.HTTP_200_OK)

class EmployeeSerializer(serializers.ModelSerializer):
    """json serializer for employees"""
    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'specialty')
