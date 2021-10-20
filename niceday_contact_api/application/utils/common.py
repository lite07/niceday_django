from rest_framework.response import Response
import uuid

def populate_filter(request, filter_fields):
    filter = {}
    for field in filter_fields:
        property_value = request.GET.get(field, None)
        if property_value is not None:
            filterKey = '{0}__contains'.format(field)
            filter[filterKey] = property_value
    return filter

def get_pagination_parameters(request):
    page = int(request.GET.get('page', 1))
    pageSize = int(request.GET.get('pageSize', 10))
    return {'skip' : (page-1)*pageSize , 'take' : pageSize}

def remove_null_from_dictionary(dict):
    return {k : v for k, v in dict.items() if v is not None}

def check_invalid_uuid(id):
    try:
        uuid.UUID(id)
        return False
    except ValueError:
        return True

def return_invalid_uuid_response(id_var_name):
    return Response(data = '{0} is not in a valid uuid format'.format(id_var_name), status=400)
