from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    GenericAPIView
from rest_framework.permissions import IsAuthenticated
from agent.api.v1.permissions import IsSuperUser, OwnProfileOrAdminPermission, IsAgent
from ticket.models import Ticket
from rest_framework.response import Response
from rest_framework import status
from .serializers import TicketSerializer, TicketSellSerializer
from django.db.models import Count
from django.contrib.auth import get_user_model

User = get_user_model()


# Ticket
class TicketCreateView(CreateAPIView):
    """
    Ticket create view class for superuser only
    """
    permission_classes = [IsSuperUser]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class TicketListView(ListAPIView):
    """
    Ticket list view class for superuser only
    """
    permission_classes = [IsSuperUser | IsAgent]
    serializer_class = TicketSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Ticket.objects.all()
        if self.request.user.is_agent:
            return Ticket.objects.filter(assigned_to=self.request.user)


class TicketRetrieveView(RetrieveAPIView):
    """
    Ticket get view class for superuser only
    """
    permission_classes = [IsSuperUser | IsAgent]
    serializer_class = TicketSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Ticket.objects.all()
        if self.request.user.is_agent:
            return Ticket.objects.filter(assigned_to=self.request.user)


class TicketDestroyView(DestroyAPIView):
    """
    Ticket delete view class for superuser only
    """
    permission_classes = [IsSuperUser]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': '{}'.format(e)},
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )


class TicketUpdateView(UpdateAPIView):
    """
    Ticket update view class for superuser only
    """
    permission_classes = [IsSuperUser]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class TicketFilter(GenericAPIView):
    """
    all data needed in create form ticket
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            return Response(
                {
                    "type": [{"label": priorty[1], "value": priorty[0]} for priorty in Ticket.PRIORITY_CHOICES],
                }
            )
        except Exception as e:
            print(e)
            return Response({"data": "not found"})


class TicketListAgentView(GenericAPIView):
    """
    Ticket list view class for agent only
    """
    permission_classes = [IsAgent]
    serializer_class = TicketSerializer

    def get(self, request, *args, **kwargs):
        try:
            # return
            return Response(
                {"data": "{}".format(Ticket.objects.filter(assigned_to=None).aggregate(Count('id'))['id__count'])})

        except Exception as e:
            print(e)
            return Response({"data": "not found"})


class AssignTicketsToAgentView(GenericAPIView):
    permission_classes = [IsAgent]

    # serializer_class = TicketSerializer
    def post(self, request):
        try:
            agent = User.objects.get(is_agent=True, id=request.user.id)
        except User.DoesNotExist:
            return Response({"error": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the tickets already assigned to the agent
        assigned_tickets = list(Ticket.objects.filter(assigned_to=request.user, is_sold=False))

        if len(assigned_tickets) == 15:
            return Response({"message": "Agent already has 15 tickets",
                             "tickets": TicketSerializer(assigned_tickets, many=True).data}, status=status.HTTP_200_OK)

        # Calculate how many more tickets to assign
        tickets_needed = 15 - len(assigned_tickets)

        # Get unassigned tickets
        available_tickets = Ticket.objects.filter(assigned_to=None)[:tickets_needed]

        if not available_tickets:
            return Response({"message": "No unassigned tickets available"}, status=status.HTTP_404_NOT_FOUND)

        # Assign tickets to the agent
        for ticket in available_tickets:
            ticket.is_assigned = agent
            ticket.save()
            assigned_tickets.append(ticket)

        return Response(
            {"message": f"Assigned {len(available_tickets)} tickets to agent {agent.username}",
             "tickets": TicketSerializer(assigned_tickets, many=True).data},
            status=status.HTTP_200_OK
        )


class SellTicket(UpdateAPIView):
    serializer_class = TicketSellSerializer
    permission_classes = [IsAgent]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Ticket.objects.all()
        if self.request.user.is_agent:
            return Ticket.objects.filter(assigned_to=self.request.user)

    def perform_update(self, serializer):
        # Ensure `is_sold` is set to True and assign to the logged-in user
        serializer.save(is_sold=True, assigned_to=self.request.user)
