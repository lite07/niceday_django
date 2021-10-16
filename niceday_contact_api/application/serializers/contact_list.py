from django.db import models
from rest_framework import serializers
from application.models.contact_list import ContactList
from application.serializers.contact import ContactListingSerializer

class ContactListSerializer(serializers.ModelSerializer):
    contacts = ContactListingSerializer(read_only=True, many=True)
    class Meta:
        model = ContactList
        fields = ('id', 'name', 'description', 'contacts')

class ContactListListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactList
        fields = ('id', 'name')

