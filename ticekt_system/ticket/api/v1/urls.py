from django.urls import path
from .views import TicketCreateView, TicketListView, TicketRetrieveView, TicketDestroyView, TicketUpdateView, \
    TicketFilter,AssignTicketsToAgentView,TicketListAgentView

app_name = 'ticket'

urlpatterns = [
    # Ticket model
    path('create', TicketCreateView.as_view(), name='create-ticket'),
    path('update/<int:pk>', TicketUpdateView.as_view(), name='update-ticket'),
    path('delete/<int:pk>', TicketDestroyView.as_view(), name='delete-ticket'),
    path('<int:pk>', TicketRetrieveView.as_view(), name='get-ticket'),
    path('list', TicketListView.as_view(), name='list-ticket'),
    path('filter', TicketFilter.as_view(), name='filter-ticket'),
    path('fetch_ticket', TicketListAgentView.as_view(), name='fetch-ticket'),
    path('assign_ticket', AssignTicketsToAgentView.as_view(), name='assign-ticket'),
]
