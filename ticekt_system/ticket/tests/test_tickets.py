from rest_framework.test import APITestCase
from rest_framework import status
from ticket.models import Ticket
from customer.models import Customer
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class TicketAPITestCase(APITestCase):

    def setUp(self):
        """Setup test data before each test."""
        self.user = User.objects.create_user(username='testuser', password='testpassword',is_superuser=True)
        self.customer = Customer.objects.create(name="ttesst2")
        self.ticket_data = {
            "title": "Test Ticket",
            "customer": self.customer,
            "is_sold": False,
            "assigned_to": None,
            "description": "This is a test ticket",
            "priority": 3,
            "price": "100.00",
            "event_date": (now() + timedelta(days=5)).isoformat(),
        }

    def test_create_ticket(self):
        """Test API endpoint for creating a ticket."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/ticket/create', self.ticket_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.first().title, "Test Ticket")

    def test_get_tickets(self):
        """Test API endpoint to list tickets."""
        ticket = Ticket.objects.create(**self.ticket_data)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/ticket/list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    # # def test_ticket_priority_filter(self):
    # #     """Test API filtering based on priority."""
    # #     Ticket.objects.create(**self.ticket_data, priority=1)
    # #     Ticket.objects.create(**self.ticket_data, priority=3)
    # #
    # #     self.client.force_authenticate(user=self.user)
    # #     response = self.client.get('/api/tickets/?priority=1')
    # #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    # #     self.assertEqual(len(response.json()), 1)
    #
    def test_update_ticket(self):
        """Test updating a ticket."""
        ticket = Ticket.objects.create(**self.ticket_data)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/v1/ticket/update/{ticket.id}', {"title": "Updated Title"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket.refresh_from_db()
        self.assertEqual(ticket.title, "Updated Title")

    def test_concurrent_ticket_updates(self):
        """Test concurrent ticket updates handling."""
        ticket = Ticket.objects.create(**self.ticket_data)

        # Simulate two users updating the ticket at the same time
        self.client.force_authenticate(user=self.user)

        response1 = self.client.patch(f'/api/v1/ticket/update/{ticket.id}', {"priority": 1}, format='json')
        response2 = self.client.patch(f'/api/v1/ticket/update/{ticket.id}', {"priority": 5}, format='json')

        ticket.refresh_from_db()
        self.assertIn(ticket.priority, [1, 5])  # Ensure only one update succeeded
    #
    def test_delete_ticket(self):
        """Test deleting a ticket."""
        ticket = Ticket.objects.create(**self.ticket_data)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/v1/ticket/delete/{ticket.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ticket.objects.count(), 0)


class AssignTicketsToAgentTest(APITestCase):

    def setUp(self):
        """Setup test data before each test."""
        # Create an agent user
        self.agent = User.objects.create_user(username='agent1', password='testpass', is_staff=True)
        self.agent.is_agent = True  # Manually adding `is_agent` since it's not a built-in field
        self.agent.save()

        # Create a customer
        self.customer = Customer.objects.create(name="eman zayan")

        # Create unassigned tickets
        self.tickets = [
            Ticket.objects.create(
                title=f"Ticket {i}",
                customer=self.customer,
                is_sold=False,
                assigned_to=None,
                description="Test Ticket",
                priority=3,
                price="100.00",
                event_date=now() + timedelta(days=5)
            ) for i in range(10)  # Creating 10 tickets
        ]

        # API URL
        self.url = "/api/v1/ticket/fetch"

    def test_assign_tickets_success(self):
        """Test successful ticket assignment to an agent."""
        self.client.force_authenticate(user=self.agent)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Assigned", response.data["message"])
        self.assertEqual(Ticket.objects.filter(assigned_to=self.agent).count(), 10)

    def test_assign_tickets_agent_already_has_15(self):
        """Test that an agent with 15 tickets cannot receive more."""
        # Assign 15 tickets to the agent
        for i in range(15):
            Ticket.objects.create(
                title=f"Preassigned Ticket {i}",
                customer=self.customer,
                is_sold=False,
                assigned_to=self.agent,
                description="Preassigned Ticket",
                priority=3,
                price="50.00",
                event_date=now() + timedelta(days=3)
            )

        self.client.force_authenticate(user=self.agent)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Agent already has 15 tickets")

    def test_no_unassigned_tickets_available(self):
        """Test when no unassigned tickets are left."""
        Ticket.objects.all().update(assigned_to=self.agent)  # Assign all tickets to the agent

        self.client.force_authenticate(user=self.agent)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "No unassigned tickets available")

    def test_agent_not_found(self):
        """Test case where an agent does not exist."""
        # Create a normal user (not an agent)
        normal_user = User.objects.create_user(username="normal_user", password="testpass", is_staff=False)

        self.client.force_authenticate(user=normal_user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Agent not found")