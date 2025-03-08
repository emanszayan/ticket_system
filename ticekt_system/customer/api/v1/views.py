from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    GenericAPIView
from rest_framework.permissions import IsAuthenticated
from agent.api.v1.permissions import IsSuperUser, OwnProfileOrAdminPermission, IsAgent
from customer.models import Customer
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.db.models import Count
from django.contrib.auth import get_user_model

User = get_user_model()


# Customer
class CustomerCreateView(CreateAPIView):
    """
    Customer create view class
    """
    permission_classes = [IsSuperUser | IsAgent]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerListView(ListAPIView):
    """
    Customer list view class for superuser only
    """
    permission_classes = [IsSuperUser | IsAgent]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerRetrieveView(RetrieveAPIView):
    """
    Customer get view class for superuser only
    """
    permission_classes = [IsSuperUser | IsAgent]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerDestroyView(DestroyAPIView):
    """
    Customer delete view class for superuser only
    """
    permission_classes = [IsSuperUser | IsAgent]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': '{}'.format(e)},
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )


class CustomerUpdateView(UpdateAPIView):
    """
    Customer update view class for superuser only
    """
    permission_classes = [IsSuperUser | IsAgent]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

