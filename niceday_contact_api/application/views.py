from django.shortcuts import render
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view
import uuid, logging

from application.models.contact import Contact
from application.serializers.contact import ContactSerializer, ContactListingSerializer



#region define private functions and variables
__logger = logging.getLogger(__name__)

def __populate_contact_filter(request):
    FILTERED_CONTACT_PROPERTIES = ['name', 'address', 'email', 'phone_number']

    filter = {}
    for property_name in FILTERED_CONTACT_PROPERTIES:
        property_value = request.GET.get(property_name, None)
        if property_value is not None:
            filterKey = '{0}__contains'.format(property_name)
            filter[filterKey] = property_value
    __logger.debug('list_contacts with filter {0}'.format(filter))
    return filter

def __get_contact_by_id(id):
    try:
        contact = Contact.objects.get(id=uuid.UUID(id))
        return contact
    except ObjectDoesNotExist:
        return None
#endregion

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List Contact' : '/api/contacts',
        'Get Contact' : '/api/contacts/{contact-id}',
        'Create Contact' : '/api/contacts/create'
    }
    return Response(api_urls)

@api_view(['GET'])
def list_contact(request):
    __logger.info('list_contacts starting.')
    contact_filter = __populate_contact_filter(request)
    contacts = Contact.objects.all().filter(**contact_filter)
    serialized_contacts = ContactListingSerializer(contacts, many=True)
    __logger.info('list_contacts finished successfully.')
    return Response(serialized_contacts.data)

@api_view(['GET', 'DELETE'])
def detail_contact(request, id):
    contact = __get_contact_by_id(id)
    if contact is not None:
        if request.method == 'GET':
            serialized_contact = ContactSerializer(contact, many=False)
            return Response(data=serialized_contact.data, status=200)
        elif request.method == 'DELETE':
            contact.delete()
            return Response(data='Deleted contact with id {0}'.format(id), status=200)
        else:
            return Response(status=405)
    else:
        return Response(data = 'Unable to find contact with id {0}'.format(id), status=404)

@api_view(['POST'])
def create_contact(request):
    __logger.info('create_contact starting.')

    __logger.debug('create_contact with content {0}'.format(request.data))
    serializer = ContactSerializer(data=request.data, many=False)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response('Request data is not valid: {0}'.format(request.data), status=400)

    __logger.info('create_contact finished successfully.')
    return Response(request.data)

