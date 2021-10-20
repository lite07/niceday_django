from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock
import ast

from application.models.contact import Contact

class ContactTestCase(APITestCase):
    def setUp(self):
        Contact.objects.create(id = 'ee418c58-7625-4806-b51e-cf257d199e5e', name = 'John Doe', email = 'john@unkown.com', address = 'Forest Road', phone_number = '+9999999')
        Contact.objects.create(id = 'ae355d96-88a5-40cd-a298-7caaa75a794d', name = 'Alexis', email = 'alexis@company.com')
        Contact.objects.create(id = 'e3b59623-dc85-4f90-9c9f-52adfdf4aa32', name = 'Max', email = 'max@organization.org', address = 'Abbey Road')
        Contact.objects.create(id = '805357ba-1496-4253-b8fe-1facfeeeab8e', name = 'Maximus', email = 'max@agency.gov', phone_number='+123321456')

    #region list_contact test methods
    def test_listcontact_nofilter_returnall(self):
        response = self.client.get('/api/contacts')
        response_data = ast.literal_eval(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['totalCount'], 4)

    def test_listcontact_filtername_returnmatch(self):
        request_data = {
            'name' : 'max'
         }
        response = self.client.get('/api/contacts', request_data)
        response_data = ast.literal_eval(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['totalCount'], 2)
        self.assertEqual(response_data['data'], [{'id': mock.ANY, 'name':'Max'}, {'id':mock.ANY, 'name' : 'Maximus'}])
    
    def test_listcontact_filteremail_returnmactch(self):
        request_data = {
            'email' : 'max'
         }
        response = self.client.get('/api/contacts', request_data)
        response_data = ast.literal_eval(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['totalCount'], 2)
        self.assertEqual(response_data['data'], [{'id': mock.ANY, 'name':'Max'}, {'id':mock.ANY, 'name' : 'Maximus'}])
    
    def test_listcontact_filteraddress_returnmactch(self):
        request_data = {
            'address' : 'abbey'
         }
        response = self.client.get('/api/contacts', request_data)
        response_data = ast.literal_eval(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['totalCount'], 1)
        self.assertEqual(response_data['data'], [{'id': mock.ANY, 'name':'Max'}])
    
    def test_listcontact_filterphone_returnmactch(self):
        request_data = {
            'phone_number' : '9999'
         }
        response = self.client.get('/api/contacts', request_data)
        response_data = ast.literal_eval(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['totalCount'], 1)
        self.assertEqual(response_data['data'], [{'id': mock.ANY, 'name':'John Doe'}])
    #endregion

    #region create_contact test methods
    def test_createcontact_validdata_returnok(self):
        request_data = {
            'name' : 'John Doe',
            'email' : 'john@unknown.com',
            'address' : 'Null Road',
            'phone_number' : '+123123123'
        }
        response = self.client.post('/api/contacts', request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_createcontact_noemail_returnbadrequest(self):
        request_data = {
            'name' : 'John Doe'
        }
        response = self.client.post('/api/contacts', request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_createcontact_invalidemail_returnbadrequest(self):
        request_data = {
            'name' : 'John Doe',
            'email' : 'not_an_email_format123123'
        }
        response = self.client.post('/api/contacts', request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_createcontact_noname_returnbadrequest(self):
        request_data = {
            'email' : 'john@unknown.com'
        }
        response = self.client.post('/api/contacts', request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_createcontact_invalidphoneformat_returnbadrequest(self):
        request_data = {
            'name' : 'John Doe',
            'email' : 'john@unknown.com',
            'phone_number': '12123'
        }
        response = self.client.post('/api/contacts', request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_createcontact_nonnumericphone_returnbadrequest(self):
        request_data = {
            'name' : 'John Doe',
            'email' : 'john@unknown.com',
            'phone_number': '+asdasd12123'
        }
        response = self.client.post('/api/contacts', request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_createcontact_toolongphone_returnbadrequest(self):
        request_data = {
            'name' : 'John Doe',
            'email' : 'john@unknown.com',
            'phone_number': '+132123123123312312123'
        }
        response = self.client.post('/api/contacts', request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #endregion

    #region get_contact test methods
    def test_getcontact_validid_returncontact(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75a794d'
        response = self.client.get('/api/contacts/{0}'.format(id))
        response_data = ast.literal_eval(response.content.decode('UTF-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {'id' : 'ae355d96-88a5-40cd-a298-7caaa75a794d', 'name' : 'Alexis', 'email' : 'alexis@company.com'})
    
    def test_getcontact_invalidid_returnnotfound(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75d314d'
        response = self.client.get('/api/contacts/{0}'.format(id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #endregion

    #region delete_contact test methods
    def test_deletecontact_validid_returnok(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75a794d'
        response = self.client.delete('/api/contacts/{0}'.format(id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_deletecontact_invalidid_returnnotfound(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75d314d'
        response = self.client.delete('/api/contacts/{0}'.format(id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #endregion

    #region update_contact test methods
    def test_updatecontact_validid_returnok(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75a794d'
        response = self.client.patch('/api/contacts/{0}'.format(id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updatecontact_invalidid_returnnotfound(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75d314d'
        response = self.client.patch('/api/contacts/{0}'.format(id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_updatecontact_validdata_returnok(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75a794d'
        request_data = {
            'name': 'some name',
            'email' : 'email@email.com',
            'address' : '123123',
            'phone_number' : '+123123123'
        }
        response = self.client.patch('/api/contacts/{0}'.format(id), request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updatecontact_blankname_returnbadrequest(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75a794d'
        request_data = {
            'name' : '',
            'email' : 'email@email.com',
            'address' : '123123',
            'phone_number' : '+123123123'
        }
        response = self.client.patch('/api/contacts/{0}'.format(id), request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_updatecontact_invalidemail_returnbadrequest(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75a794d'
        request_data = {
            'name' : 'some name',
            'email' : 'email123email.com',
            'address' : '123123',
            'phone_number' : '+123123123'
        }
        response = self.client.patch('/api/contacts/{0}'.format(id), request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_updatecontact_invalidphone_returnbadrequest(self):
        id = 'ae355d96-88a5-40cd-a298-7caaa75a794d'
        request_data = {
            'name' : 'some name',
            'email' : 'email@email.com',
            'address' : '123123',
            'phone_number' : '+asdasd213'
        }
        response = self.client.patch('/api/contacts/{0}'.format(id), request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #endregion

