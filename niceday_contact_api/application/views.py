from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging

from application.models.contact import Contact
from application.serializers import ContactSerializer

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

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List Contact' : '/api/contacts',
        'Create Contact' : '/api/contacts/create'
    }
    return Response(api_urls)

@api_view(['GET'])
def list_contacts(request):
    __logger.info('list_contacts starting.')
    contact_filter = __populate_contact_filter(request)
    contacts = Contact.objects.all().filter(**contact_filter)
    serialized_contacts = ContactSerializer(contacts, many=True)
    __logger.info('list_contacts finished successfully.')
    return Response(serialized_contacts.data)

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

@api_view(['DELETE'])
def delete_contact(request):
    __logger.info('delete_contact starting.')
    contact_id = request.data['id']

    __logger.debug('delete_contact with id {0}'.format(contact_id))
    try:
        contact = Contact.objects.get(id=contact_id)
        contact.delete()
    except ObjectDoesNotExist:
        return Response(data = 'Unable to find contact with id {0}'.format(contact_id), status=404)

    __logger.info('delete_contact finished successfully.')
    return Response(request.data)

