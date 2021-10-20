from django.shortcuts import render
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view

import application.services.contact as ContactService
import application.services.contact_list as ContactListService

@api_view(['GET'])
def api_overview(request):
    """
        All listing endpoints will support pagination.
        Add 'page' and 'pageSize' in query parameter to control the pagination of your request.
        Default value for 'page' is 1 and 'pageSize' is 10.
    """
    api_urls = {
        'List Contact' : '[GET] /api/contacts',    
        'Create Contact' : '[POST] /api/contacts',
        'Get Contact Detail' : '[GET] /api/contacts/{id}',
        'Delete Contact' : '[DELETE] /api/contacts/{id}',
        'Update Contact' : '[PATCH] /api/contacts/{id}',
        'List ContactList' : '[GET] /api/contact-lists',
        'Create ContactList' : '[POST] /api/contact-lists',
        'Get ContactList Detail' : '[GET] /api/contacts-lists/{id}',
        'Delete ContactList Detail' : '[DELETE] /api/contacts-lists/{id}',
        'Get Contacts in ContactList' : '[GET] /api/contacts-lists/{list-id}/contacts',
        'Assign Contact to ContactList' : '[POST] /api/contacts-lists/{list-id}/contacts',
        'Remove Contact from ContactList' : '[DELETE] /api/contacts-lists/{list-id}/contacts/{contact-id}'
    }
    return Response(api_urls)

@api_view(['GET','POST'])
def contact_view(request):
    """
        This endpoint will cover both listing and filter contact with GET and create contact with POST

        [GET] For listing purpose, will only return the id and name of the contact. Dtail can be fetched using another endpoint.
        Support 'name', 'email', 'address', and 'phone_number' as filter parameter. Add the filter in the query parameter.

        [POST] Example request data for creating contact:
        {
            "name" : "some name",
            "email" : "name@domain.com",
            "address" : "some string",
            "phone_number" : "+123123123"
        } 
        'name' and 'email' are mandatory. 'phone_number' should be in a format of "+1231231231" with up to 15 digit. 
    """
    if request.method == 'GET':
        return ContactService.list_contact(request)
    elif request.method == 'POST':
        return ContactService.create_contact(request)
    return Response(status=405)

@api_view(['GET', 'DELETE', 'PATCH'])
def single_contact_view(request, id):
    """
        This endpoint will cover the detail (GET), update (PATCH), and delete (DELETE) of a contact.

        [PATCH] Example request data for creating contact:
        {
            "name" : "some name",
            "email" : "name@domain.com",
            "address" : "some string",
            "phone_number" : "+123123123"
        } 
       'name' and 'email' are mandatory. 'phone_number' should be in a format of "+1231231231" with up to 15 digit. 
    """
    if request.method == 'GET':
        return ContactService.get_contact(id)
    elif request.method == 'DELETE':
        return ContactService.delete_contact(id)
    elif request.method == 'PATCH':
        return ContactService.update_contact(request, id)
    return Response(status=405)

@api_view(['GET', 'POST'])
def contact_list_view(request):
    """
        This endpoint will cover both listing and filter contact list with GET and create contact list with POST

        [GET] For listing purpose, will only return the id and name of the contact lists. Detail can be fetched using the another endpoint.
        Support 'name' and 'description' as filter parameter. Add the filter in the query parameter.

        [POST] Example request body for creating contact list:
        {
            "name" : "some name",
            "description" : "description of the contact list here"
        } 
        'name' is mandatory.
    """
    if request.method == 'GET':
        return ContactListService.list_contactlist(request)
    elif request.method == 'POST':
        return ContactListService.create_contactlist(request)
    return Response(status=405)

@api_view(['GET', 'DELETE'])
def single_contact_list_view(request, id):
    """
        This endpoint will cover the detail (GET) and delete (DELETE) of a contact.
    """
    if request.method == 'GET':
        return ContactListService.get_contactlist(id)
    if request.method == 'DELETE':
        return ContactListService.delete_contactlist(id)
    return Response(status=405)

@api_view(['GET', 'POST'])
def assigned_contact_view(request, list_id):
    """
        This endpoint will cover listing and filter of assigned contact with GET and assignment of a contact to a list wit POST.

        [POST] Example of the request body:
        {
            "contact_id" : "some-guid-string"
        }
        'contact_id' is mandatory.
    """
    if request.method == 'GET':
        return ContactListService.get_assigned_contact(request, list_id)
    if request.method == 'POST':
        return ContactListService.assign_contact(request, list_id)
    return Response(status=405)

@api_view(['DELETE'])
def remove_contact_view(request, list_id, contact_id):
    """
        This endpoint will handle the removal of a certain contact from a list.
    """
    if request.method == 'DELETE':
        return ContactListService.remove_contact(list_id, contact_id)
    return Response(status=405)


