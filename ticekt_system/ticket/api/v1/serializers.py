from rest_framework import serializers
from ticket.models import Ticket
from customer.models import Customer

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'priority', 'price', 'event_date', 'customer']

    def update(self, instance, validated_data):
        request = self.context['request']

        # Handle customer assignment or creation
        customer_data = validated_data.pop('customer', None)
        if customer_data:
            customer, created = Customer.objects.get_or_create(**customer_data)
            instance.customer = customer
        # Automatically update fields
        instance.is_sold = True
        instance.assigned_to = request.user

        # Update other fields normally
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance