from django.shortcuts import render
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view

import application.services.contact as ContactService
import application.services.contact_list as ContactListService

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List Contact' : '[GET] /api/contacts',    
        'Create Contact' : '[POST] /api/contacts',
        'Get Contact Detail' : '[GET] /api/contacts/{contact-id}',
        'Delete Contact' : '[DELETE] /api/contacts/{contact-id}',
        'Update Contact' : '[PATCH] /api/contacts/{contact-id}',
        'List ContactList' : '[GET] /api/contact-lists',
        'Create ContactList' : '[POST] /api/contact-lists',
        'Get ContactList Detail' : '[GET] /api/contacts-lists/{contactlist-id}',
        'Delete ContactList Detail' : '[DELETE] /api/contacts-lists/{contactlist-id}',
        'Get Contacts in ContactList' : '[GET] /api/contacts-lists/{contactlist-id}/contacts',
        'Assign Contact to ContactList' : '[POST] /api/contacts-lists/{contactlist-id}/contacts',
        'Remove Contact from ContactList' : '[POST] /api/contacts-lists/{contactlist-id}/contacts'
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

@api_view(['GET', 'POST'])
def contact_list_view(request):
    if request.method == 'GET':
        return ContactListService.list_contactlist(request)
    elif request.method == 'POST':
        return ContactListService.create_contactlist(request)
    return Response(status=405)

@api_view(['GET', 'DELETE'])
def single_contact_list_view(request, id):
    if request.method == 'GET':
        return ContactListService.get_contactlist(id)
    if request.method == 'DELETE':
        return ContactListService.delete_contactlist(id)
    return Response(status=405)

@api_view(['GET', 'POST'])
def assigned_contact_view(request, list_id):
    if request.method == 'GET':
        return ContactListService.get_assigned_contact(request, list_id)
    if request.method == 'POST':
        return ContactListService.assign_contact(list_id, request.data['contact_id'])
    if request.method == 'DELETE':
        return ContactListService.remove_contact(list_id, request.data['contact_id'])
    return Response(status=405)


