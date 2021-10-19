def get_not_valid_error_template(msg=''):
    error_template = {
        'message' : msg or 'Request data is not valid:',
        'errors' : {}
    }
    return error_template

def get_listing_response_template(data = '', total_counts = 0):
    response = {
        'data' : data,
        'totalCount' : total_counts
    }
    return response