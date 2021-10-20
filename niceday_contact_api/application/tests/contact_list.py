from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock
import ast, uuid

from application.models.contact import Contact
from application.models.contact_list import ContactList

class ContactListTestCase(APITestCase):
    def setUp(self):
        Contact.objects.create(id = 'ee418c58-7625-4806-b51e-cf257d199e5e', name = 'John Doe', email = 'john@unkown.com', address = 'Forest Road', phone_number = '+9999999')
        Contact.objects.create(id = 'ae355d96-88a5-40cd-a298-7caaa75a794d', name = 'Alexis', email = 'alexis@company.com')
        Contact.objects.create(id = 'e3b59623-dc85-4f90-9c9f-52adfdf4aa32', name = 'Max', email = 'max@organization.org', address = 'Abbey Road')
        Contact.objects.create(id = '805357ba-1496-4253-b8fe-1facfeeeab8e', name = 'Maximus', email = 'max@agency.gov', phone_number='+123321456')
        ContactList.objects.create(id = '80441534-c75d-4c51-9950-5a7f6698c09b', name = 'Default')
        ContactList.objects.create(id = '8d7fb59a-c237-4efe-90b6-2a4645151c62', name = 'Highschool')

        contactlist_object = ContactList.objects.get(id=uuid.UUID('8d7fb59a-c237-4efe-90b6-2a4645151c62'))
        first_contact_object = Contact.objects.get(id=uuid.UUID('ee418c58-7625-4806-b51e-cf257d199e5e'))
        second_contact_object = Contact.objects.get(id=uuid.UUID('e3b59623-dc85-4f90-9c9f-52adfdf4aa32'))
        contactlist_object.contacts.add(first_contact_object)
        contactlist_object.contacts.add(second_contact_object)
        contactlist_object.save()

    #region create_contactlist test methods
    def test_createlist_validdata_returnok(self):
        request_data = {
            'name' : 'some name',
            'description' : 'some description'
        }
        response = self.client.post('/api/contact-lists', request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_createlist_noname_returnbadrequest(self):
        request_data = {
            'description' : 'some description'
        }
        response = self.client.post('/api/contact-lists', request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #endregion
    
    #region list_contactlist test methods
    def test_listlist_nofilter_returnall(self):
        response = self.client.get('/api/contact-lists')
        response_data = ast.literal_eval(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['totalCount'], 2)
    
    def test_listlist_filtername_returnmatch(self):
        request_data = {
            'name' : 'Default'
        }
        response = self.client.get('/api/contact-lists', request_data)
        response_data = ast.literal_eval(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['totalCount'], 1)
    #endregion

    #region delete_contactlist_test methods
    def test_deletelist_validid_returnok(self):
        response = self.client.delete('/api/contact-lists/8d7fb59a-c237-4efe-90b6-2a4645151c62')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_deletelist_invalidid_returnbadrequest(self):
        response = self.client.delete('/api/contact-lists/8d7123-2a4645151c62')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deletelist_wrongid_returnnotfoud(self):
        response = self.client.delete('/api/contact-lists/8e7fb59a-c666-4efe-90b6-2a4645151c63')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #endregion

    def test_getlist_validid_returnok(self):
        response = self.client.get('/api/contact-lists/8d7fb59a-c237-4efe-90b6-2a4645151c62')
        response_data = ast.literal_eval(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {'id' : '8d7fb59a-c237-4efe-90b6-2a4645151c62', 'name' : 'Highschool'})

    def test_getlist_invalidid_returnbadrequest(self):
        response = self.client.get('/api/contact-lists/8d7123-2a4645151c62')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_getlist_wrongid_returnnotfound(self):
        response = self.client.get('/api/contact-lists/8e7fb59a-c666-4efe-90b6-2a4645151c63')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
