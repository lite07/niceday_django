from django.db import models
from rest_framework import serializers
from application.models.contact import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'address', 'phone_number')

class ContactListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name')
