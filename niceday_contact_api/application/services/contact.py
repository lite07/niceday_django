from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.response import Response
import uuid, logging

from application.models.contact import Contact
from application.serializers.contact import ContactSerializer, ContactListingSerializer
from application.utils.templates import GetNotValidErrorTemplate

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

def __get_pagination_parameters(request):
    page = int(request.GET.get('page', 1))
    pageSize = int(request.GET.get('pageSize', 10))
    return {'skip' : (page-1)*pageSize , 'take' : pageSize}
#endregion
def get_contact_by_id(id) -> Contact:
    try:
        contact = Contact.objects.get(id=uuid.UUID(id))
        return contact
    except ObjectDoesNotExist:
        return None

def list_contact(request):
    __logger.info('list_contact starting.')
    contact_filter = __populate_contact_filter(request)
    pagination_param = __get_pagination_parameters(request)
    contacts = Contact.objects.all().filter(**contact_filter)[pagination_param['skip']:pagination_param['take']]
    serialized_contacts = ContactListingSerializer(contacts, many=True)
    __logger.info('list_contact finished successfully.')
    return Response(data=serialized_contacts.data, status=200)

def create_contact(request): 
    __logger.info('create_contact starting.')
    serializer = ContactSerializer(data=request.data, many=False)
    if serializer.is_valid():
        serializer.save()
    else:
        error_messages = GetNotValidErrorTemplate()
        for error in serializer.errors:
            error_detail = serializer.errors[error][0]
            error_messages['errors'][error] = str(error_detail)
        __logger.error('create_contact finished with an error: {0}'.format(error_messages['errors']))
        return Response(data = error_messages, status=400)
    __logger.info('create_contact finished successfully.')
    return Response(data=request.data, status=200)

def get_contact(id):
    __logger.info('get_contact starting.')
    contact = get_contact_by_id(id)
    if contact is not None:
            serialized_contact = ContactSerializer(contact, many=False)
            __logger.info('get_contact finished successfully.')
            return Response(data=serialized_contact.data, status=200)
    return Response(data = 'Unable to find contact with id {0}'.format(id), status=404)

def delete_contact(id):
    __logger.info('delete_contact starting.')
    contact = get_contact_by_id(id)
    if contact is not None:
        contact.delete()
        __logger.info('delete_contact finished successfully.')
        return Response(data='Deleted contact with id {0}'.format(id), status=200)
    return Response(data = 'Unable to find contact with id {0}'.format(id), status=404)

def update_contact(request, id):
    __logger.info('update_contact starting.')
    contact = get_contact_by_id(id)
    if contact is not None:
        if 'name' in request.data: 
            contact.name = request.data['name']
        if 'email' in request.data:
            contact.email = request.data['email']
        if 'address' in request.data:
            contact.address = request.data['address']
        if 'phone_number' in request.data:
            contact.phone_number = request.data['phone_number']
        try:
            contact.full_clean()
            contact.save()
        except ValidationError as ex:
            error_messages = GetNotValidErrorTemplate()
            for error_key in ex.error_dict:
                error_messages['errors'][error_key] = ','.join(ex.error_dict[error_key][0])
            __logger.error('update_contact finished with an error: {0}'.format(error_messages['errors']))
            return Response(data = error_messages, status=400)
        __logger.info('update_contact finished successfully.')       
        return Response(data = request.data, status=200)