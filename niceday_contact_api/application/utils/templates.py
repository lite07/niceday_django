def GetNotValidErrorTemplate(msg=''):
    error_template = {
        'message' : msg or 'Request data is not valid:',
        'errors' : {}
    }
    return error_template 