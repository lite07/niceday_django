from django.shortcuts import render
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view

import application.services.contact as ContactService

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List Contact' : '[GET] /api/contacts',    
        'Create Contact' : '[POST] /api/contacts',
        'Get Contact' : '[GET] /api/contacts/{contact-id}',
        'Delete Contact' : '[DELETE] /api/contacts/{contact-id}',
        'Update Contact' : '[PATCH] /api/contacts/{contact-id}'
    }
    return Response(api_urls)

@api_view(['GET','POST'])
def contact_view(request):
    if request.method == 'GET':
        return ContactService.list_contact(request)
    elif request.method == 'POST':
        return ContactService.create_contact(request)
    return Response(status=405)

@api_view(['GET', 'DELETE', 'PATCH'])
def single_contact_view(request, id):
    if request.method == 'GET':
        return ContactService.get_contact(id)
    elif request.method == 'DELETE':
        return ContactService.delete_contact(id)
    elif request.method == 'PATCH':
        return ContactService.update_contact(request, id)
    return Response(status=405)

