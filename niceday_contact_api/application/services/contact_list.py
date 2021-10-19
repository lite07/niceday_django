from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
import uuid, logging

import application.utils.constant as Constant
from application.models.contact_list import ContactList
from application.serializers.contact_list import ContactListSerializer, ContactListListingSerializer
from application.serializers.contact import ContactSerializer
from application.services.contact import get_contact_by_id
from application.utils.template import get_not_valid_error_template, get_listing_response_template
from application.utils.common import get_pagination_parameters, populate_filter, remove_null_from_dictionary



#region define private functions and variables
__logger = logging.getLogger(__name__)
#endregion
def get_contact_list_by_id(id) -> ContactList:
    try:
        contact = ContactList.objects.get(id=uuid.UUID(id))
        return contact
    except ObjectDoesNotExist:
        return None

def create_contactlist(request):
    __logger.info('create_contactlist starting.')
    serialized_data = ContactListSerializer(data = request.data, many=False)
    if serialized_data.is_valid():
        serialized_data.save()
    else:
        error_messages = get_not_valid_error_template()
        for error in serialized_data.errors:
            error_detail = serialized_data.errors[error][0]
            error_messages['errors'][error] = str(error_detail)
        return Response(data = error_messages, status=400)
    __logger.info('create_contactlist finished successfully.')
    return Response(data=request.data, status=200)

def list_contactlist(request):
    __logger.info('list_contactlist starting.')

    filter = populate_filter(request, ['name'])
    pagination_param = get_pagination_parameters(request)

    total_count = ContactList.objects.filter(**filter).count()
    contact_lists = ContactList.objects.all().filter(**filter)[pagination_param['skip']:pagination_param['take']]

    serialized_contact_lists = ContactListListingSerializer(contact_lists, many=True)  
    response_data = get_listing_response_template(serialized_contact_lists.data, total_count)
    
    __logger.info('list_contactlist finished successfully.')
    return Response(data = response_data, status = 200)

def get_contactlist(id):
    contact_list = get_contact_list_by_id(id)
    if contact_list is not None:
            serialized_contactlist = ContactListSerializer(contact_list, many=False)
            __logger.info('get_contactlist finished successfully.')
            return Response(data=remove_null_from_dictionary(serialized_contactlist.data), status=200)
    return Response(data = 'Unable to find contact list with id {0}'.format(id), status=404)

def delete_contactlist(id):
    contact_list = get_contact_list_by_id(id)
    if contact_list is not None:
        contact_list.delete()
        return Response(status=200)
    return Response(data = 'Unable to find contact list with id {0}'.format(id), status=404)

def get_assigned_contact(request, id):
    contact_list = get_contact_list_by_id(id)
    if contact_list is not None:
        filter = populate_filter(request, Constant.CONTACT_FILTERERED_FILEDS)
        pagination_param = get_pagination_parameters(request)

        total_count = contact_list.contacts.filter(**filter).count()
        contacts = contact_list.contacts.filter(**filter)[pagination_param['skip']:pagination_param['take']]

        serialized_contacts = ContactSerializer(contacts, many=True)
        response_data = get_listing_response_template(serialized_contacts.data, total_count)

        return Response(data = response_data, status = 200)           
    return Response(status = 200)

def assign_contact(list_id, contact_id):
    contact_list = get_contact_list_by_id(list_id)
    if contact_list is not None:
        contact = get_contact_by_id(contact_id)
        if contact is not None:
            contact_list.contacts.add(contact)
            contact_list.save()
        else:
            return Response('Unable to find contact with id {0}'.format(list_id), status=404)
    else:
        return Response('Unable to find contact list with id {0}'.format(list_id), status=404)
    return Response(status = 200)

def remove_contact(list_id, contact_id):
    contact_list = get_contact_list_by_id(list_id)
    if contact_list is not None:
        try:
            contact = contact_list.contacts.get(id = uuid.UUID(contact_id))
            contact_list.contacts.remove(contact)
            contact_list.save()
        except ObjectDoesNotExist:
            return Response('Unable to find contact with id {0} in list {1}'.format(contact_id, list_id), status= 404)
    else:
        return Response('Unable to find contact list with id {0}'.format(list_id), status=404)
    return Response(status = 200)

