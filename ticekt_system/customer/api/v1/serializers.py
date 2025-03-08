from rest_framework import serializers
from customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    # created_by = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['created_by']

    def validate(self, attrs):
        attrs['created_by'] = self.context.get('request').user
        return attrs

    # def get_created_by(self, obj):
    #     if obj.created_by:
    #         return obj.created_by.username
