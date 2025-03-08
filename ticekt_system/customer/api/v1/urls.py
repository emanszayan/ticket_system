from django.urls import path
from .views import CustomerCreateView, CustomerUpdateView, CustomerListView, CustomerDestroyView, CustomerRetrieveView

app_name = 'customer'

urlpatterns = [
    # customer model
    path('create', CustomerCreateView.as_view(), name='create-customer'),
    path('update/<int:pk>', CustomerUpdateView.as_view(), name='update-customer'),
    path('delete/<int:pk>', CustomerDestroyView.as_view(), name='delete-customer'),
    path('<int:pk>', CustomerRetrieveView.as_view(), name='get-customer'),
    path('list', CustomerListView.as_view(), name='list-customer'),
]
