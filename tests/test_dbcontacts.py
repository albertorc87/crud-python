import os
import unittest
from classes.contact import Contact
from classes.dbcontacts import DBContacts
import psycopg2

class TestDBContacts(unittest.TestCase):
    
    def setUp(self):
        self.db = DBContacts(True)
        self.db.save_contact(self._object_contact())


    def _object_contact(self):
        return Contact(None, 'Usertest', 'User Test', 'user@gmail.com', '999999999', '1987-11-23')


    def _dict_contact(self):
        return {
            'name':'Usertest2', 
            'surname':'User Test2', 
            'email':'user2@gmail.com', 
            'phone':900000000, 
            'birthday':'1987-11-24'
        }


    def test_save_contact(self):
        result = self.db.save_contact(self._object_contact())
        self.assertEqual(result, 1)


    def test_update_contact(self):
        
        contact = self._dict_contact()

        last_id = self.db.get_last_id()

        result = self.db.update_contact(last_id, contact)
        self.assertNotEqual(result, 0)

        ddbb_contact = self.db.get_by_id(last_id)

        self.assertEqual(contact['name'], ddbb_contact['name'])
        self.assertEqual(contact['surname'], ddbb_contact['surname'])
        self.assertEqual(contact['email'], ddbb_contact['email'])
        self.assertEqual(contact['phone'], ddbb_contact['phone'])
        self.assertEqual(contact['birthday'], ddbb_contact['birthday'].strftime("%Y-%m-%d"))


    def test_get_contact(self):
        
        try:
            last_id = self.db.get_last_id()
        except psycopg2.ProgrammingError as err:
            self.db.save_contact(self._object_contact())
            last_id = self.db.get_last_id()

        contact = self.db.get_by_id(last_id)
        self.assertNotEqual(contact, {})

        my_contact = self._object_contact()
        self.assertEqual(contact['name'], my_contact.name)
        self.assertEqual(contact['surname'], my_contact.surname)
        self.assertEqual(contact['email'], my_contact.email)
        self.assertEqual(str(contact['phone']), my_contact.phone)
        self.assertEqual(contact['birthday'].strftime("%Y-%m-%d"), my_contact.birthday)


    def test_search_contact(self):

        last_id = self.db.get_last_id()

        my_contact = self._object_contact()
        filters = {
            'name': my_contact.name,
            'surname': my_contact.surname,
            'email': my_contact.email
        }

        list_contacts = self.db.search_contacts(filters)
        self.assertNotEqual(list_contacts, [])
        for contact in list_contacts:
            self.assertIsInstance(contact, Contact)
            self.assertEqual(contact.name, my_contact.name)
            self.assertEqual(contact.surname, my_contact.surname)
            self.assertEqual(contact.email, my_contact.email)
            self.assertEqual(str(contact.phone), my_contact.phone)
            self.assertEqual(contact.birthday.strftime("%Y-%m-%d"), my_contact.birthday)
            break


    def test_list_contacts(self):

        list_contacts = self.db.list_contacts()
        self.assertNotEqual(list_contacts, [])

        for contact in list_contacts:
            self.assertIsInstance(contact, Contact)


    def test_remove_contact(self):

        try:
            last_id = self.db.get_last_id()
        except Exception as err:
            self.db.save_contact(self._object_contact())
            last_id = self.db.get_last_id()

        self.assertEqual(self.db.delete_contact(last_id), 1)
        contact = self.db.get_by_id(last_id)
        self.assertEqual(contact, {})


if __name__ == "__main__":
    unittest.main()