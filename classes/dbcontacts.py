from .contact import Contact
from .dbcsv import DBbyCSV

SCHEMA = {
    'ID': {
        'type': 'autoincrement',
    }, 
    'NAME': {
        'type': 'string',
        'min_length': 3,
        'max_length': 50
    }, 
    'SURNAME': {
        'type': 'string',
        'min_length': 5,
        'max_length': 100
    }, 
    'EMAIL': {
        'type': 'string',
        'max_length': 254
    }, 
    'PHONE': {
        'type': 'int'
    }, 
    'BIRTHDAY': {
        'type': 'date'
    }
}

class DBContacts(DBbyCSV):

    def __init__(self):
        super().__init__(SCHEMA, 'contacts')

    
    def save_contact(self, contact):
        data = [contact.name, contact.surname, contact.email, contact.phone, contact.birthday]
        return self.insert(data)
    

    def update_contact(self):
        pass


    def delete_contact(self):
        pass


    def list_contacts(self):
        list_contacts = self.get_all()

        if not list_contacts:
            return None

        object_contacts = []
        # Convertimos los datos a objectos de tipo contact
        for contact in list_contacts:
            c = Contact(contact['ID'], contact['NAME'], contact['SURNAME'], contact['EMAIL'], contact['PHONE'], contact['BIRTHDAY'])
            object_contacts.append(c)

        return object_contacts

    
    def get_schema(self):
        return SCHEMA