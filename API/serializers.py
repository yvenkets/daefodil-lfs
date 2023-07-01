from rest_framework import serializers
 
# import model from models.py
from daefodilapp.models import *
 
# Create a model serializer
class dlmcust(serializers.ModelSerializer):
    # specify model and fields
    class Meta:
        model = DlmCust
        fields = '__all__'