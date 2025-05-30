from rest_framework import serializers

from .models import Customer
# from .models import Customer, VocRecord

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# class VocRecordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=VocRecord
#         fields='__all__'
