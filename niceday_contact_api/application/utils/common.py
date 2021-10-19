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